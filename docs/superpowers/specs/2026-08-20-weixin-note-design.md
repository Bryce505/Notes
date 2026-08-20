# 微信公众号文章剪藏助手 —— 设计文档

- 日期：2026-08-20
- 状态：待评审
- 项目目录：`E:\dev-workspace\weixin-note`

## 1. 背景与目标

在手机微信里读到感兴趣但来不及看的公众号文章，目前存到 flowus，但后续查找不便、无会员看不了正文、必须点开链接才知道讲了什么。

本项目要做的是：手机上两步把文章送出去，之后由自动化流水线抓取正文、调用 AI 消化，并把结构化结果同时写入 Notion 数据库与 GitHub md 归档，使得**不点开原文链接就能判断一篇文章值不值得读，并能直接读到全文**。

### 成功标准

1. 手机端剪藏操作不超过两步（复制链接 + 点一次快捷方式）。
2. 剪藏后 2 分钟内，Notion 数据库出现该文章条目，含摘要、关键词、洞见、AI 优先级与全文快照。
3. GitHub 仓库中 `notes/YYYY-MM.md` 同步更新，新条目位于当月标题正下方。
4. 同一链接重复剪藏不会产生重复记录。
5. 原文被删除后，仍可从快照读到全文。

## 2. 非目标（明确不做）

- 不做微信个人号自动化（hook PC 微信读取"文件传输助手"）：违反微信用户协议、有封号风险、微信版本升级即失效。
- 不做公众号服务器回调方案：需要额外的公网服务，且微信不支持从文章界面直接转发到公众号会话，操作步数反而更多。
- 不做全文检索服务、不做推荐算法、不做多用户支持。
- 不做阅读时长估算、不单独记录公众号账号名（评审时明确排除；日后需要可低成本补充，抓取阶段本就拿得到）。

## 3. 关键决策记录

| 决策 | 选择 | 理由 |
|---|---|---|
| 手机入口 | Android + HTTP Shortcuts 桌面小组件 | 免费开源、零封号风险、可注册为系统分享目标 |
| 触发方式 | GitHub `repository_dispatch` | 即时触发，无需任何常驻服务器或中间件 |
| 运行载体 | GitHub Actions | 免费额度充足（私有仓库 2000 分钟/月，单次运行 < 1 分钟） |
| 存储 | Notion 数据库 + GitHub md 双写 | Notion 负责查询与移动端阅读，GitHub 负责长期归档与防锁定 |
| 分月依据 | **剪藏时间** | 符合"稍后阅读清单"语义；文章发布时间同时保存但不用于分组 |
| AI 服务 | OpenAI 兼容接口，默认 DeepSeek | 成本约 ¥0.005/篇；改配置即可切换服务商 |
| 仓库可见性 | 私有 | 正文快照涉及他人版权，不宜公开托管 |

## 4. 系统架构

```
【Android】微信文章 → "…" → 复制链接
        │
        ▼  点桌面小组件（HTTP Shortcuts），HTTPS POST + 细粒度 PAT
【GitHub API】POST /repos/<owner>/weixin-note/dispatches
              event_type: "clip"   client_payload: { url }
        │
        ▼
【GitHub Actions · Python 3.11+】
   store.is_duplicate()  →  fetcher.fetch()  →  ai.digest()
        →  notion_writer.create_page()  →  md_writer.append()  →  git commit
        │
        ▼ 任一步异常
   自动创建 GitHub Issue 记录失败链接与堆栈，便于人工重试
```

## 5. 组件划分

采用 `src/` 布局，每个模块单一职责、可独立测试。

| 模块 | 职责 | 依赖 |
|---|---|---|
| `src/clipper/models.py` | 数据类 `Article`（抓取结果）、`Digest`（AI 结果）、`Entry`（落库记录） | 无 |
| `src/clipper/fetcher.py` | 输入 URL，输出 `Article`（标题、发布时间、正文纯文本）；负责 URL 规范化、UA 伪装、重试 | requests, beautifulsoup4 |
| `src/clipper/ai.py` | 输入 `Article`，输出 `Digest`；负责超长文截断、JSON 解析与校验、失败重试 | openai（兼容端点） |
| `src/clipper/notion_writer.py` | 输入 `Entry`，在 Notion 数据库建页并分批写入正文快照块 | requests（Notion REST API） |
| `src/clipper/md_writer.py` | 输入 `Entry`，更新 `notes/YYYY-MM.md` 与 `archive/YYYY-MM/<slug>.md` | 标准库 |
| `src/clipper/store.py` | `data/index.json` 的读写、按 URL 指纹查重 | 标准库 |
| `src/clipper/cli.py` | 命令行入口：`clip <url>` 单条、`clip --batch <file>` 批量 | 上述模块 |
| `.github/workflows/clip.yml` | `repository_dispatch` 与 `workflow_dispatch` 触发，装依赖、跑 CLI、提交变更 | — |

模块间只通过上表中的数据类通信，不共享全局状态；`fetcher` / `ai` / `notion_writer` 三者互不感知。

## 6. 数据模型

### 6.1 Notion 数据库属性

| 属性 | 类型 | 来源 |
|---|---|---|
| 标题 | Title | 抓取，失败时由 AI 推断 |
| 链接 | URL | 剪藏输入 |
| 剪藏时间 | Date | 流水线运行时刻（分组依据） |
| 发布时间 | Date | 抓取；取不到留空 |
| 摘要 | Rich text | AI |
| 关键词 | Multi-select | AI（3–6 个） |
| 洞见 | Rich text | AI（2–4 条，换行分隔） |
| AI优先级 | Select：高 / 中 / 低 | AI |
| 优先级理由 | Rich text | AI |
| 阅读状态 | Select：未读 / 在读 / 已读 / 已放弃 | 默认"未读"，人工维护 |

**页面正文**写入全文快照。默认视图：按「剪藏时间」所属月份分组、时间倒序；另建「待读」视图过滤 `阅读状态 = 未读` 且按 AI优先级排序。

### 6.2 `data/index.json`

```json
{
  "<url_fingerprint>": {
    "url": "https://mp.weixin.qq.com/s/xxx",
    "title": "……",
    "clipped_at": "2026-08-20T19:44:00+08:00",
    "notion_page_id": "……",
    "md_path": "notes/2026-08.md"
  }
}
```

`url_fingerprint` 取链接 path 中的 `s/<id>` 段；无该结构时回退为去掉 query 后整串的 sha1。

### 6.3 md 归档格式

`notes/2026-08.md`，新条目插入 `# 2026年08月` 标题正下方：

```markdown
# 2026年08月

## 为什么大模型的上下文窗口越来越长
- **剪藏**：2026-08-20 19:44 ｜ **发布**：2026-08-18
- **优先级**：高 ｜ **状态**：未读
- **关键词**：长上下文 / 注意力机制 / 推理成本
- **摘要**：……
- **洞见**：
  - ……
- **链接**：[原文](https://mp.weixin.qq.com/s/xxx) ｜ [全文快照](../archive/2026-08/xxx.md)
```

全文快照存 `archive/YYYY-MM/<slug>.md`，`slug` 由标题清洗生成（去非法字符、限长 60 字符，冲突时追加指纹前 6 位）。索引文件只保留摘要级信息以保持翻阅速度。

## 7. 处理流程与错误处理

1. **查重**：命中 `index.json` 则记录一条日志后正常退出（退出码 0），不重复写入。
2. **抓取**：3 次重试、指数退避；命中"环境异常"验证页时判定为抓取失败。
3. **AI**：要求 JSON 输出；解析失败重试 1 次；仍失败则以"AI 处理失败"占位，但仍完成后续落库（保住链接与正文，不丢内容）。
4. **写 Notion**：单个 rich text 块上限 2000 字符、单次 append 上限 100 块 → 正文按段落切块、分批提交。Notion 失败不阻断 md 写入。
5. **写 md 与提交**：`git commit` 后 push；并发冲突时 rebase 重试一次。
6. **失败上报**：整体异常时通过 GitHub API 创建 Issue，标题含链接、正文含堆栈，标签 `clip-failed`。

**超长文截断策略**：正文超过配置阈值时，保留头部 60% 与尾部 40%，中间以省略标记连接——公众号文章结论常在末尾，只读开头会误判优先级。

## 8. 批量导入（存量迁移）

`clip --batch links.txt`：每行一个链接，逐条走同一条流水线，条目之间间隔 3–5 秒以避开微信频控；单条失败不中断整体，最后汇总打印成功/失败清单。同时在 workflow 中提供 `workflow_dispatch` 手动触发入口，可直接贴入链接列表运行。

存量文章的「剪藏时间」统一使用导入运行时刻，因此会集中落在当月——如需保留原始收藏日期，可在 `links.txt` 中用 `<url>\t<YYYY-MM-DD>` 格式指定，解析时优先采用。

## 9. 配置与密钥

存于 GitHub Secrets：

| 名称 | 用途 |
|---|---|
| `AI_BASE_URL` / `AI_API_KEY` / `AI_MODEL` | AI 服务，默认 DeepSeek |
| `NOTION_TOKEN` | Notion 集成令牌 |
| `NOTION_DATABASE_ID` | 目标数据库 |

手机端持有的是**细粒度 PAT**，仅授权本仓库的 contents 写权限，泄露面可控；泄露时在 GitHub 设置里单独吊销即可。

## 10. 测试策略

- `fetcher`：用保存下来的真实微信文章 HTML 作为 fixture，断言标题/正文/发布时间解析正确；另加一份"环境异常"页面 fixture，断言正确判定为失败。
- `ai`：以 stub 客户端返回预置 JSON，覆盖正常、字段缺失、非 JSON 三种情况。
- `md_writer`：给定既有月度文件，断言新条目插入到标题正下方且原有内容不变；覆盖"当月文件尚不存在"的分支。
- `store`：查重与指纹生成，覆盖带 query 参数、不同 query 同一文章的情况。
- `notion_writer`：以 fake HTTP 层断言切块逻辑（>2000 字符、>100 块）。
- 端到端：`--dry-run` 模式跑通全流程但不写外部服务。

测试用 pytest，配置 `pythonpath = ["src"]`，遵循工作空间共享规范。

## 11. 部署步骤（需人工完成的部分）

1. 在 GitHub 创建私有仓库 `weixin-note`，推送本项目。
2. 在 Notion 建数据库（属性见 6.1），创建集成并把数据库共享给它，取得 token 与 database id。
3. 在仓库 Settings → Secrets 填入第 9 节的密钥。
4. 生成细粒度 PAT（仅本仓库、contents 写）。
5. 手机安装 HTTP Shortcuts，新建一个 POST 请求指向 dispatches 接口，body 取剪贴板内容，放到桌面小组件。

## 12. 本地开发环境

- 解释器固定为 `D:\Anaconda\envs\dev\python.exe`，运行前设置 `$env:PYTHONNOUSERSITE='1'`，遵循工作空间的环境隔离约定。
- 安装依赖一律带代理参数：
  `pip install <包名> --proxy http://127.0.0.1:7897 --trusted-host pypi.org --trusted-host files.pythonhosted.org`
- 环境检查、依赖安装与测试执行统一走 `python-env-manager` 流程，不使用裸 `python` / `pip` 命令。
- 本地调试用 `--dry-run` 跑通抓取与 AI 环节，避免污染 Notion 与仓库历史。

## 13. 风险与对策

| 风险 | 影响 | 对策 |
|---|---|---|
| 微信抓取频控 | 抓取失败 | 个人日均几篇不触发；批量导入加间隔；失败开 Issue 可重试 |
| 微信页面结构调整 | 解析失效 | 解析逻辑集中在 `fetcher`，有 fixture 测试，改一处即可 |
| Notion API 限流 | 写入失败 | 分批提交 + 重试；md 写入不受影响，数据不丢 |
| 手机 PAT 泄露 | 仓库被写 | 细粒度 PAT，权限最小化，可单独吊销 |
| AI 输出不稳定 | 字段缺失 | JSON 校验 + 重试 + 占位降级，不阻断落库 |

## 14. 后续可选扩展（当前不做）

- 每周自动生成"本周待读 Top N"汇总，推送到 Notion 或 Issue。
- 电脑常开时叠加"文件传输助手"监听，实现真正的一步转发（需自行承担微信协议风险）。
- 关键词聚类，自动维护主题索引页。

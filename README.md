# Notes —— 公众号文章 / X 帖子剪藏助手

手机上看到来不及读的**微信公众号文章**或 **X（原推特）帖子**，复制链接、点一下桌面小组件，约一分钟后 Notion 里就出现一条带 **AI 摘要、关键词、洞见、阅读优先级**的记录，页面正文是全文快照；同时在本仓库留一份 Markdown 归档。

**解决的问题**：稍后阅读清单里全是标题和链接，不点开就不知道讲了什么，也判断不出值不值得花时间读。

两个来源共用一条流水线、**同一个桌面小组件**，按链接域名自动分流；Notion 各用一个数据库，仓库里各用一套目录，互不干扰。

---

## 目录

- [工作原理](#工作原理)
- [仓库结构](#仓库结构)
- [一、首次配置](#一首次配置)
  - [1. 配置 Notion](#1-配置-notion)
  - [2. 配置 GitHub Secrets](#2-配置-github-secrets)
  - [3. 生成手机用的访问令牌](#3-生成手机用的访问令牌)
  - [4. 配置手机触发器](#4-配置手机触发器)
  - [5. 验收测试](#5-验收测试)
  - [6. 开启 X 帖子剪藏](#6-开启-x-帖子剪藏)
- [二、日常使用](#二日常使用)
- [三、批量导入](#三批量导入)
- [四、排错手册](#四排错手册)
- [五、已知限制](#五已知限制)
- [六、本地开发](#六本地开发)
- [七、设计取舍](#七设计取舍)

---

## 工作原理

```
微信文章 ··· → 复制链接   ／   X 帖子 → 复制链接
      ↓ 点同一个桌面小组件（HTTP Shortcuts）
GitHub API：POST /repos/Bryce505/Notes/dispatches
      ↓ repository_dispatch 事件
GitHub Actions（Python，约 15 秒）
      ├─ 查重（data/index.json）
      ├─ 抓取正文 ── 按域名分流
      │     ├─ mp.weixin.qq.com → 解析文章页面
      │     └─ x.com / twitter.com → fxtwitter 镜像（失败回退 X 官方嵌入接口）
      ├─ AI 消化（摘要 / 关键词 / 洞见 / 优先级；X 帖子额外要求拟中文标题）
      ├─ 写 Notion（公众号库 / X 库，按来源选）
      └─ 写 md 归档并自动提交（notes/ 与 notes/x/）
```

不需要服务器，不需要电脑常开，全部跑在 GitHub Actions 免费额度内。AI 成本约 **¥0.005/篇**。

## 仓库结构

| 路径 | 内容 |
|---|---|
| `notes/YYYY-MM.md` | 公众号月度索引，按剪藏时间分组，最新的在最上面 |
| `archive/YYYY-MM/*.md` | 每篇公众号文章的全文快照 |
| `notes/x/YYYY-MM.md` | X 帖子月度索引，格式同上 |
| `archive/x/YYYY-MM/*.md` | 每条 X 帖子的全文快照 |
| `data/index.json` | 剪藏索引，用于查重 |
| `src/clipper/` | 处理流水线源码 |
| `tests/` | 单元测试（96 项） |
| `docs/superpowers/specs/` | 设计文档 |

---

# 一、首次配置

全程约 20 分钟。按顺序做，中间有几个坑标了 ⚠️，跳过会白折腾。第 6 节是 X 剪藏，只想剪公众号可以跳过。

## 1. 配置 Notion

### 1.1 创建集成

1. 打开 <https://www.notion.so/my-integrations>
2. 点「**+ 新连接**」
3. 连接名称随意（例如 `Claude code`）
4. 验证方式选 「**访问令牌**」

> [!IMPORTANT]
> **验证方式必须选「访问令牌」，不要选 OAuth。**
> 访问令牌是工作区范围的静态密钥，适合这种无人值守的自动化；OAuth 需要浏览器授权跳转、回调地址和令牌刷新，跑在 GitHub Actions 里根本没法用。

5. 创建后复制令牌（`ntn_` 开头），**它只显示一次**

### 1.2 授权页面（最容易漏的一步）

在 Notion 里新建一个空白页面（例如「公众号剪藏 AI」），然后：

**页面右上角 `···` → 连接 → 添加刚才创建的集成**

> [!WARNING]
> 不做这一步，令牌是有效的，但集成看不见任何内容，所有 API 调用都会返回 **404**。
> 排查时很容易误判成"令牌错了"，实际是没授权。

复制该页面 URL 末尾的 32 位字符，这是 **页面 ID**（下一步要用）。

### 1.3 创建数据库

在本地跑一次（需要先装好[本地开发环境](#六本地开发)）：

```bash
NOTION_TOKEN=<你的令牌> python -m clipper init-notion --parent-page <页面ID>
```

命令会自动建好带 10 个属性的数据库，并打印 **数据库 ID**。

| 属性 | 类型 | 来源 |
|---|---|---|
| 标题 | Title | 抓取 |
| 链接 | URL | 剪藏输入 |
| 剪藏时间 | Date | 流水线运行时刻（分月依据） |
| 发布时间 | Date | 抓取 |
| 摘要 | Rich text | AI |
| 关键词 | Multi-select | AI |
| 洞见 | Rich text | AI |
| AI优先级 | Select：高 / 中 / 低 | AI |
| 优先级理由 | Rich text | AI |
| 阅读状态 | Select：未读 / 在读 / 已读 / 已放弃 | 默认未读，人工维护 |

> [!NOTE]
> **页面 ID ≠ 数据库 ID**，两者长得一模一样，极易混淆。拿页面 ID 去调数据库接口会直接 400。
> 填进 Secrets 的是 **数据库 ID**，也就是上面命令打印出来的那个。

### 1.4 ⚠️ 千万不要做的事

> [!CAUTION]
> **绝对不要在这个数据库里点「添加数据源」（Add data source）。**
>
> Notion 新版数据模型允许一个数据库挂多个数据源，但一旦挂上第二个，`2022-06-28` 版本的 API 就会对这个库的**所有**读写返回：
>
> ```
> 400 Databases with multiple data sources are not supported in this API version.
> ```
>
> 而且**无法挽救**：把多余的数据源归档（`in_trash: true`）也没用，Notion 仍然认定这个库是多数据源。唯一的出路是**重建数据库**，然后更新 `NOTION_DATABASE_ID`。
>
> 这个坑在实际使用中踩过一次，症状是剪藏全部"成功"、md 归档正常、Actions 全绿，但 Notion 里一条都没有。

### 1.5 建议的视图配置

Notion API 不支持创建视图，需要手动设置：

- **默认视图**：按「剪藏时间」分组 + 倒序 → 就是「2026年08月」这样的分月效果
- **待读视图**：过滤 `阅读状态 = 未读`，按 `AI优先级` 排序 → 每天从这里挑要读的

## 2. 配置 GitHub Secrets

仓库 → **Settings → Secrets and variables → Actions → New repository secret**

| 名称 | 值 | 必填 |
|---|---|---|
| `AI_API_KEY` | AI 服务密钥 | ✅ |
| `AI_BASE_URL` | 默认 `https://api.deepseek.com`，用别家才填 | |
| `AI_MODEL` | 默认 `deepseek-chat` | |
| `NOTION_TOKEN` | 1.1 生成的令牌 | ✅ |
| `NOTION_DATABASE_ID` | 1.3 打印的数据库 ID | ✅ |
| `NOTION_X_DATABASE_ID` | X 帖子用的数据库 ID，见[第 6 节](#6-开启-x-帖子剪藏) | |

关于模型：

- 模型 ID 必须和服务商文档**逐字一致**，差一个字符就是 400
- 换服务商时 `AI_BASE_URL` 要一起改，ID 写法也不同（例如硅基流动是 `deepseek-ai/DeepSeek-V3` 这种带前缀的形式）
- `AI_BASE_URL` 填 `https://api.example.com` 或 `https://api.example.com/v1` 都可以，代码会自动拼对
- 模型不支持强制 JSON 输出时会自动降级重试，不用管
- 不配 `NOTION_TOKEN` / `NOTION_DATABASE_ID` 也能跑，只是只写 md 不写 Notion
- 不配 `NOTION_X_DATABASE_ID` 时，X 帖子只写 md 归档，公众号那条链路不受影响

## 3. 生成手机用的访问令牌

在**手机浏览器**里做，方便直接粘进 App：<https://github.com/settings/personal-access-tokens/new>

| 项目 | 填什么 |
|---|---|
| Token name | 随意，例如 `手机剪藏` |
| Expiration | 建议 1 年（到期后触发器失效，需重新生成并替换） |
| Repository access | `Only select repositories` → 勾选 `Bryce505/Notes` |
| Permissions | Repository permissions → **Contents: Read and write** |

其他权限一律不给。

> [!WARNING]
> **令牌只显示一次**，关掉页面就再也看不到，只能重新生成。先做完第 4 步把它粘进 App，或者先存进密码管理器。

万一手机丢失，在 GitHub 设置里吊销这一个令牌即可，它只对这一个私有仓库有写权限，不影响其他任何东西。

## 4. 配置手机触发器

以 Android + [HTTP Shortcuts](https://http-shortcuts.rmy.ch/)（免费开源，Google Play / F-Droid 均有）为例。

### 4.1 新建请求

App 右下角 **➕ → 从头创建**（英文版 Create from scratch）。如果接着让你选类型，选 **HTTP 请求**那一类，不要选「浏览器快捷方式」或「脚本快捷方式」。

> [!TIP]
> **捷径**：看 ➕ 菜单里有没有「从 cURL 导入」。有的话选它，粘贴下面这段，方法、地址、请求头、请求体会一次性填好（把「你的令牌」换成第 3 步生成的那串）：
>
> ```bash
> curl -X POST https://api.github.com/repos/Bryce505/Notes/dispatches -H "Authorization: Bearer 你的令牌" -H "Accept: application/vnd.github+json" -d '{"event_type":"clip","client_payload":{"url":""}}'
> ```

手工填的话，四项如下：

| 字段 | 值 |
|---|---|
| 方法 · Method | `POST` |
| 地址 · URL | `https://api.github.com/repos/Bryce505/Notes/dispatches` |
| 请求头 · Headers | `Authorization: Bearer <你的令牌>`<br>`Accept: application/vnd.github+json` |
| 请求体 · Body（类型选自定义文本 / JSON） | `{"event_type":"clip","client_payload":{"url":""}}` |

末尾那对空引号先留着，下一步要往里面塞变量。

### 4.2 插入剪贴板变量（整个配置里最容易卡住的一步）

1. 左上角菜单 → **变量**（Variables）→ ➕ 新建
2. 类型选 **Clipboard Content**（剪贴板内容），命名 `clipboard`，保存
3. 回到请求体，把光标放进 `"url": ""` 的**两个引号中间**
4. 点输入框旁边的 `{ }` 图标 → 选中 `clipboard` 插入

插好后大致是这样（花括号里是 App 生成的占位符，不同版本显示略有差异）：

```
{"event_type":"clip","client_payload":{"url":"{{clipboard}}"}}
```

> [!IMPORTANT]
> **手打变量名无效**，必须用 `{ }` 按钮插入才会真正绑定。用 cURL 导入也省不掉这一步——粘贴文本里的花括号 App 不认。
>
> 这一步没做对的症状是：请求发得出去，但 Actions 日志里 `CLIP_URL:` 是空的，什么也不会发生。

### 4.3 配置成功提示（不配会以为一直失败）

编辑该快捷方式 → **响应处理**（Response Handling）→ 成功时显示 **Toast**，文案自定义为「已发送剪藏」；失败时显示对话框。

> [!IMPORTANT]
> GitHub 的 dispatches 接口成功时返回 **204 No Content**——成功，但不返回任何内容。
> App 默认设置下没东西可显示，于是静默执行完毕，**看起来像完全没反应**。
>
> 实际使用中因为这个误以为配置失败、反复点了 6 次，结果后 5 次全被正确判为重复。配上提示就不会再有这种困惑。

### 4.4 放到桌面

长按桌面空白处 → **小组件** → HTTP Shortcuts → 拖一个到桌面 → 选择刚建的快捷方式。建议放在从微信切出来一眼能看到的位置。

### 4.5 备选方案：走分享菜单

如果剪贴板方案不稳（Android 对后台读剪贴板有限制），把变量类型从 **Clipboard Content** 换成 **Shared Text**，并打开快捷方式的「加入分享菜单」。

用法变成：微信文章 `···` → **在浏览器打开** → 浏览器分享 → 选该快捷方式。多一步，但不依赖剪贴板权限。

## 5. 验收测试

1. 微信里打开任意一篇公众号文章
2. 右上角 `···` → **复制链接**
3. 回桌面点小组件，看到 **204** 提示即为成功
4. 打开 [Actions 页](https://github.com/Bryce505/Notes/actions)，应该有一条新运行
5. 约一分钟后，Notion 库里出现新条目，仓库里出现新提交

## 6. 开启 X 帖子剪藏

只做一件事：**再建一个 Notion 数据库**。手机端不用动——同一个小组件复制什么链接就剪什么，流水线按域名自己分流。

```bash
NOTION_TOKEN=<你的令牌> python -m clipper init-notion --parent-page <页面ID> --title "X 剪藏"
```

把打印出来的 ID 填进 Secrets 的 **`NOTION_X_DATABASE_ID`**（注意不是 `NOTION_DATABASE_ID`）。属性和公众号库完全一样，1.5 节那套视图配置照搬即可。

> [!IMPORTANT]
> 父页面同样要先「`···` → 连接 → 添加集成」，否则一样 404。可以复用公众号那个页面，也可以另建一个。
> 1.4 节那条「绝对不要加第二个数据源」的警告对这个库同样适用。

**为什么单独建一个库而不是混在一起**：给正在正常使用的库加「来源」属性属于 schema 变更，风险不小；而且 X 帖子短、条数多，混进文章列表会把文章淹掉。两个库分开后，两边的视图和筛选各调各的。

### 支持的链接形式

`x.com` 与 `twitter.com`（含 `www.` / `mobile.` 前缀）都认，链接尾巴上的 `?s=20` 之类追踪参数不影响查重——同一条帖子换域名、换用户名大小写再剪一次，仍然会被判为重复。

一条帖子会抓到：正文（**长推文取完整全文**，不是被截断的那段）、作者、发布时间、它引用的帖子、它回复的上一条；图片和视频以 `[图片]` / `[视频]` 占位，`t.co` 短链还原成原始链接。

**X 长文（Article）**也支持。这类帖子本体只有一个指向文章的链接，正文在 `x.com/i/article/<id>` 里，标题直接用作者写的那个。

---

# 二、日常使用

**剪藏**：微信文章 `···` → 复制链接 → 点桌面小组件。约一分钟后完成。

**剪藏 X 帖子**：帖子右上角 `···` → 复制链接（或直接复制地址栏链接）→ 点**同一个**小组件。结果进 Notion 的 X 库和 `notes/x/`。

**阅读筛选**：在 Notion 的「待读」视图里，先看摘要和洞见判断值不值得读；要读全文直接点进页面，正文快照就在里面，**不用回微信**。读完把「阅读状态」改成已读或已放弃。

**几个自动行为**：

- 同一篇文章重复剪藏不会产生重复记录，会被索引跳过
- 原文被删除后，快照仍在，内容不丢
- 抓取或 AI 失败时，仓库会自动开一个带 `clip-failed` 标签的 Issue，里面有链接和运行日志地址
- Notion 写入失败时，md 归档照写（内容不丢），但运行会标记为失败并开 Issue，不会静默

---

# 三、批量导入

用来一次性导入历史存量文章。

## 用法 A：GitHub 网页（推荐）

1. 打开 [Actions](https://github.com/Bryce505/Notes/actions)
2. **点左侧栏的「剪藏公众号文章」**——`Run workflow` 按钮只在单个工作流页面里出现，All workflows 聚合页上没有
3. 右上 **Run workflow** → 把链接粘进输入框 → 跑

**输入格式**

```
https://mp.weixin.qq.com/s/xxxx
https://mp.weixin.qq.com/s/yyyy	2026-07-15
https://x.com/someone/status/1878571238879473738
# 井号开头是注释，会被跳过
```

- 每行一个链接，两种来源可以混在一起，按域名自动分流
- 行尾用 **TAB** 加日期，可指定原始收藏时间，那篇就归到那个月的档里；不写就算今天剪的
- 已剪藏过的自动跳过
- 条目之间自动间隔 4 秒，避开微信频控
- 单条失败不中断，运行结束会列出失败清单，补跑时只粘失败的那几条

> [!TIP]
> 一次别粘太多行，输入框对超长文本可能截断，**建议每批 30 条以内**。
> 微信对高频抓取有风控，云端 IP 风险更高，大批量建议先试跑 10 条看成功率。

## 用法 B：本地命令行

```bash
python -m clipper batch links.txt --interval 4
```

加 `--dry-run` 只跑抓取和 AI、不写任何存储，用来试水。单篇用 `python -m clipper clip <url>`。

---

# 四、排错手册

## 手机端返回的状态码

| 状态码 | 含义 | 怎么办 |
|---|---|---|
| **204** | 成功 | 正常，GitHub 不返回内容。去 Actions 页看运行记录 |
| **401** | 令牌无效 | Header 必须是 `Bearer ` 加空格再加令牌；检查有没有多复制空格或换行 |
| **404** | 仓库看不见 | 令牌没勾到 `Bryce505/Notes`，或 Contents 权限不是 Read and write。**GitHub 对无权限的私有仓库返回 404 而不是 403**，别被误导 |
| **422** | Body 格式不对 | 多半是 JSON 引号被输入法改成了中文引号，或变量插错位置 |
| 完全没反应 | 两种可能 | ① 没配成功提示（见 4.3），其实成功了；② 剪贴板是空的 |

## Notion 相关

| 症状 | 原因 | 解决 |
|---|---|---|
| 所有调用返回 404 | 页面没添加集成连接 | 页面 `···` → 连接 → 添加集成 |
| 返回 400 `multiple data sources` | 数据库被加了第二个数据源 | **只能重建数据库**并更新 `NOTION_DATABASE_ID`，归档多余数据源无效 |
| 返回 400 `validation_error` | 把页面 ID 当数据库 ID 用了 | 换成 `init-notion` 打印的那个 ID |
| md 有内容但 Notion 没有 | Notion 写入失败被降级处理 | 看运行日志和自动开的 Issue，里面有具体错误 |

## 查看运行情况

```bash
gh run list --repo Bryce505/Notes --limit 5          # 最近几次运行
gh run view <运行ID> --repo Bryce505/Notes --log     # 完整日志
gh issue list --repo Bryce505/Notes --label clip-failed   # 失败记录
```

日志里几个关键行：`CLIP_URL:`（收到的链接，为空说明变量没插好）、`[created]` / `[duplicate]` / `[failed]`、`汇总：新增 x，重复 x，失败 x`。

---

# 五、已知限制

**并发冲突**：连续快速剪藏两篇不同文章（间隔十几秒）时，两次运行可能同时读到同一份索引，后一次 push 会撞车失败并开 Issue。日常间隔几分钟不会触发。`concurrency` 配置没能完全兜住这种情况，待修。

**AI 优先级区分度不足**：目前实测倾向于把专业文章都判为「高」，这一列的筛选作用有限。可通过调整 `src/clipper/ai.py` 里的提示词改善。

**抓取依赖页面结构**：微信改版可能导致解析失效。解析逻辑集中在 `src/clipper/fetcher.py`，有 HTML fixture 测试兜底，改一处即可。X 同理，改 `src/clipper/x_fetcher.py`。

**X 只抓当前这一条**：不做整串 thread 回溯。X 没有免鉴权的会话接口，要拿全串得引 headless 浏览器或付费 API，成本远超收益。帖子本身的长推文全文、引用的帖子、回复的上一条都会抓到（这三样在同一份响应里就有）。

**X 抓取主要依赖社区镜像 `api.fxtwitter.com`**：X 官方的嵌入接口虽然更"正统"，但实测正文残缺得厉害——超过 280 字符的长推文被直接截断且不给补全字段，长文只返回标题和约 80 字预览。三条真实帖子对照下来官方接口全军覆没，所以镜像被排在第一顺位，官方接口降为兜底。

代价有两条，都摆在明面上：

1. **可用性不由自己掌控**。`api.fxtwitter.com` 是第三方志愿服务，不保证长期可用。它挂掉时会自动退回官方接口，普通短帖照常，但**长推文会被截断在 280 字符、长文只剩标题和预览**。
2. **隐私**。你剪藏了哪些帖子，这个第三方服务能看到（它只看得到推文 ID，看不到你是谁、也看不到你的 Notion）。

**怎么改回官方接口优先**：改一处，把 `src/clipper/x_fetcher.py` 的 `fetch()` 里 `targets` 那两行对调：

```python
    targets = (
        (MIRROR.format(post_id=post_id), parse_mirror),                              # ← 把这两行
        (f"{SYNDICATION}?id={post_id}&lang=zh-cn&token={_token(post_id)}", parse),   # ← 上下对调
    )
```

对调后隐私问题没了（只有官方接口失败时才碰镜像），代价是**长推文和长文都只能拿到残缺正文**——这正是当初调换主次的原因，见 [`docs/superpowers/specs/2026-08-25-x-post-clipping-design.md`](docs/superpowers/specs/2026-08-25-x-post-clipping-design.md) 附二里的三条实测对照。改完记得跑 `python -m pytest -q`，有两个用例锁着抓取顺序，会提示你哪些断言需要跟着改。

受保护账号、已删除的帖子两个接口都抓不到，会开 Issue 记录。

**图片不入库**：正文中的图片以 `[图片]` 占位，微信图床有防盗链，存链接也显示不出来。

---

# 六、本地开发

```bash
python -m pytest -q      # 96 项测试
```

本机固定使用 `D:\Anaconda\envs\dev\python.exe`，运行前设 `PYTHONNOUSERSITE=1`；安装依赖须带代理参数：

```bash
pip install -r requirements.txt --proxy http://127.0.0.1:7897 --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

模块划分（每个单一职责，可独立测试）：

| 模块 | 职责 |
|---|---|
| `fetcher.py` | 抓取并解析微信页面 |
| `x_fetcher.py` | 抓取并解析 X 帖子（镜像优先 + 官方嵌入接口兜底） |
| `ai.py` | 调 AI 生成摘要 / 关键词 / 洞见 / 优先级 |
| `notion_writer.py` | 写 Notion 属性与正文块（含 2000 字符、100 块的分批处理） |
| `md_writer.py` | 写月度索引与全文快照 |
| `store.py` | 查重索引 |
| `pipeline.py` | 编排单篇处理流程 |
| `cli.py` | 命令行入口 |

---

# 七、设计取舍

**为什么要复制链接而不是直接转发**：微信的转发列表不包含公众号会话，也没有开放个人号消息接口。能读微信消息的方案都要逆向 hook 客户端，违反用户协议且有封号风险，所以选了复制链接这条完全合规的路径。

**为什么 Notion 和 md 都写**：Notion 负责查询和手机阅读，md 负责长期归档与防平台锁定。两份数据同源，成本几乎为零——实际使用中，正是因为有 md 归档，Notion 出故障时数据一条没丢。

**为什么 X 帖子单独一套目录和数据库**：短帖量大，混进文章索引会把文章淹掉；而且给一个正在用的 Notion 库加属性属于 schema 变更，那个库踩过多数据源的坑，不值得再冒险。代码层面两条链路共用同一条流水线，只有抓取器、AI 提示词的补充段落、归档目录和目标数据库不同。

**为什么按剪藏时间分月**：这是稍后阅读清单，本月收的就该出现在本月，不会因为剪了篇旧文而沉到下面找不到。文章发布时间同时保存，只是不用于分组。

**AI 挂了怎么办**：摘要降级为提示文案，正文和链接照常入库，不丢内容。

**Notion 挂了怎么办**：md 照写，但运行会标记失败并开 Issue——早期版本这里是静默的，导致故障持续了半小时才被发现，现在不会了。

# X（原推特）帖子剪藏 —— 设计文档

- 日期：2026-08-25
- 状态：已评审，待实现
- 关联：[`2026-08-20-weixin-note-design.md`](2026-08-20-weixin-note-design.md)

## 1. 背景与目标

公众号剪藏已稳定运行。日常另一个信息来源是 X 上的帖子，同样存在「收藏了但不知道讲了什么、要不要花时间读」的问题。

本次要做的是：**给现有流水线加一个内容来源**，让 X 帖子链接走同一条自动化链路——抓正文、AI 消化、写 Notion、写 md 归档——但结果落在与公众号并行、互不干扰的存储里。

### 成功标准

1. 手机端操作不变：复制 X 链接后点**同一个**桌面小组件即可，不需要新建快捷方式或新令牌。
2. 剪藏后 Notion 的 X 库出现条目，含摘要、关键词、洞见、优先级；英文帖子输出中文。
3. 仓库出现 `notes/x/YYYY-MM.md` 与 `archive/x/YYYY-MM/*.md`，公众号的两份索引不受影响。
4. 同一条帖子重复剪藏被跳过；x.com 与 twitter.com、不同用户名大小写视为同一条。
5. 公众号剪藏的行为与产物**零变化**（提示词、路径、Notion 库均不动）。

## 2. 非目标（明确不做）

- **不做整串 thread 回溯**。X 没有免鉴权的会话接口，要拿全串就得引 headless 浏览器或官方 API 付费档，成本远超收益。只抓当前这一条（含其长推文全文）、它引用的帖子、以及它回复的上一条——这三样在同一份响应里就有，是免费的。
- 不做媒体文件下载。图片/视频以 `[图片]` / `[视频]` 占位，与公众号一致。
- 不做作者维度的聚合、不做时间线抓取、不做点赞转发数留档。
- 不为 X 单独做一套 CLI / workflow / 数据模型。能复用的一律复用。

## 3. 关键决策记录

| 决策 | 选择 | 理由 |
|---|---|---|
| 代码结构 | 只新增 `x_fetcher.py`，其余模块复用 | 现有流水线里只有 `fetcher` / `fingerprint` / AI 提示词是微信专属的，`ai` / `notion_writer` / `md_writer` / `store` / `pipeline` / `cli` 全部与来源无关 |
| 手机触发 | 沿用 `clip` 事件，按域名自动分发 | 手机端零改动。误把 X 链接发给公众号流水线也不会出错 |
| Notion 存储 | 新建独立数据库，`NOTION_X_DATABASE_ID` | 不对正在正常使用的库做 schema 变更（Notion 多数据源那个坑只能重建库）；两边视图各自调 |
| md 归档 | `notes/x/` 与 `archive/x/` | X 帖子短且量大，混进文章索引会把文章淹掉 |
| 抓取接口 | `cdn.syndication.twimg.com/tweet-result`，失败回退 `api.fxtwitter.com` | 前者是 X 网页嵌入推文用的公开接口，免鉴权、免 Cookie；后者是社区镜像，做兜底 |
| 标题 | 由 AI 拟中文标题，抓取侧留首句作降级 | 帖子本身没有标题；英文帖子取首句当标题在列表里没法扫读 |

## 4. 数据流

```
X 链接 ··· → 复制 → 点同一个桌面小组件
      ↓ repository_dispatch: clip
pipeline.clip()
      ├─ store.is_duplicate()        指纹 = x-<tweet_id>
      ├─ x_fetcher.fetch()           ← 按域名分发，公众号链接仍走 fetcher.fetch()
      │     ├─ cdn.syndication.twimg.com/tweet-result
      │     └─ 失败 → api.fxtwitter.com/i/status/<id>
      ├─ ai.digest()                 系统提示词追加 X 专用段落
      ├─ notion_writer.create_page() → NOTION_X_DATABASE_ID
      ├─ md_writer.write()           → notes/x/ 与 archive/x/
      └─ store.add()
```

## 5. 改动清单

| 文件 | 改动 |
|---|---|
| `src/clipper/x_fetcher.py` | **新增**。`is_x_url()` / `fetch()` / `parse()`，输出与公众号同一个 `Article` |
| `src/clipper/models.py` | `Article` 增加 `source` 字段（默认 `weixin`）；`Entry` 的归档路径按 source 加 `x/` 前缀；`fingerprint()` 认 `/status/<id>` |
| `src/clipper/pipeline.py` | 两行按域名选 fetcher；X 帖子优先采用 AI 标题；Notion 库按 source 选 |
| `src/clipper/config.py` | 增加 `notion_x_database_id`；`notion_enabled` 改为 `notion_enabled_for(source)` |
| `src/clipper/ai.py` | X 帖子在系统提示词后追加专用段落；公众号提示词一字不动 |
| `src/clipper/notion_writer.py` | 建页时按 `entry.article.source` 选数据库 |
| `src/clipper/md_writer.py` | 快照头部标签按来源（公众号 / 作者）；索引里的快照相对链接改用 `posixpath.relpath` 计算，兼容多一层目录 |
| `src/clipper/cli.py` | `init-notion` 的提示文案同时说明两个 Secret 名 |
| `.github/workflows/clip.yml` | 传入 `NOTION_X_DATABASE_ID` |

## 6. 正文渲染格式

一条帖子渲染成如下纯文本（段落间空行），再交给 AI 与两个 writer：

```
↰ 回复 @someone：被回复的那条帖子正文……

本帖正文，t.co 短链已还原成原始链接。

[图片] [图片]

↳ 引用 @another：被引用的帖子正文……
```

- 长推文（note tweet）取完整正文，不取被截断的 `text`。
- `entities.urls` 里的 `t.co` 短链替换为 `expanded_url`；剩下的裸 `t.co`（图片/视频自指链接）直接删掉。

## 7. 错误处理

沿用公众号那套，不新增机制：

| 情况 | 行为 |
|---|---|
| 两个接口都抓不到 | `FetchError`，流水线返回 failed，Actions 自动开 `clip-failed` Issue |
| 帖子已删除 / 账号已锁 | 同上，报文里带原因 |
| AI 失败 | 降级为提示文案，正文与链接照常入库（与公众号一致） |
| Notion 失败 | md 照写，运行标记失败并开 Issue（与公众号一致） |
| 未配 `NOTION_X_DATABASE_ID` | X 帖子只写 md，不阻断 |

## 8. 测试策略

沿用公众号 fetcher 的做法：**接口响应存成 JSON fixture，解析逻辑做纯函数单测**，不在测试里发真实网络请求。

- `tests/fixtures/x_post.json`：普通帖子 + 图片 + 引用 + t.co 短链
- `tests/fixtures/x_note.json`：长推文 + 回复上一条
- `tests/fixtures/x_fxtwitter.json`：镜像接口响应
- 新增 `tests/test_x_fetcher.py`；`test_models` / `test_pipeline` / `test_md_writer` / `test_ai` 各补 X 分支用例
- 公众号原有 50 项测试必须全部保持通过

### 已知的验证缺口

开发所在的沙箱网络策略拦截了 `cdn.syndication.twimg.com` 与 `api.fxtwitter.com`（CONNECT 403），**真实抓取无法在开发环境验证**。fixture 依据的是这两个接口的公开响应结构。首条真实链接的验证要在 GitHub Actions 里做；若字段名对不上，改动集中在 `x_fetcher.parse()` 一个函数内。

---

## 附：X 长文（Article）—— 实测补充

首次真实剪藏（[run 32813566222](https://github.com/Bryce505/Notes/actions/runs/32813566222)）用的是一条 X 长文，暴露出设计时没预料到的一类形态：

**长文帖子的本体只有一个指向文章的链接**，正文属于 `x.com/i/article/<id>` 这个独立对象。按原设计只会归档下这么一行：

```
https://x.com/i/article/2092012262596780032
```

用一次性调试 workflow 打出两个接口的原始响应（看完即删）后确认：

| 接口 | 长文正文 | 给了什么 |
|---|---|---|
| `cdn.syndication.twimg.com` | ❌ | `article.title` + 约 80 字 `article.preview_text` + 封面图 |
| `api.fxtwitter.com` | ✅ | `tweet.article.content.blocks[]`，Draft.js 风格的完整正文块 |

**处理方式**：`parse()` 一旦发现 `article` 字段就抛 `FetchError`，让 `fetch()` 现成的回退逻辑接着去试镜像；`parse_mirror()` 从 `content.blocks` 拼正文，`atomic` 块渲染成 `[图片]`，标题直接用作者写的 `article.title`。取不到块时退回 `preview_text`，再退回推文本身。

**顺带简化**：抓取侧不再为普通帖子自造标题（`_fallback_title` 删掉），改由 `Entry.title` 统一兜底 —— 抓取标题 → AI 标题 → 正文首句 → 「无标题」。这样长文用作者的真标题、普通帖子用 AI 拟的中文标题，`pipeline` 里那条 X 特判也随之删除，两个来源共用一条规则。

**代价**：长文的全文只有镜像有。镜像挂掉时长文会剪藏失败并开 Issue，普通帖子不受影响。

---

## 附二：两个接口的主次调换 —— 实测补充

用三条真实帖子对照两个接口，官方嵌入接口的正文全都残缺：

| 帖子 | `cdn.syndication.twimg.com` | `api.fxtwitter.com` |
|---|---|---|
| dotey 长文 | 标题 + 约 80 字预览 | 全文 |
| 0xMortyx 长文 | 标题 + 预览 | 全文 |
| 0xSizer 长推文 + 视频 | **截断在 280 字符**，且没有 `note_tweet` 可补 | 全文（`is_note_tweet: true`） |

原设计假设「官方接口给全文，长推文在 `note_tweet` 里」——这个假设只在部分响应里成立，实测的三条一条都不成立。

**改法**：`fetch()` 里两个 target 的顺序对调，镜像排第一，官方接口降为兜底；`parse()` 不再对长文抛错让位，而是退化成「标题 + 预览」，因为它现在是最后一道防线，抛错就等于什么都不剩。

**没有选的方案**：保持官方接口优先，加一个「正文长度 ≥ 280 且没有 note_tweet 就判为截断」的启发式。放弃的理由是那个 280 是魔法数字，X 改一次截断长度它就会静默失效，而调换顺序没有任何需要猜的东西。

**代价**：抓取的主路径落在第三方志愿服务上——可用性不由自己掌控，且对方能看到剪藏了哪些帖子。两条都写进了 README 的已知限制。想换回官方优先，把 `targets` 那两行调回来即可。

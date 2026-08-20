# Notes —— 微信公众号文章剪藏助手

手机上看到来不及读的公众号文章，复制链接点一下，剩下的交给这个仓库：
自动抓正文、调 AI 生成摘要 / 关键词 / 洞见 / 阅读优先级，写进 Notion 数据库，并在这里留一份 Markdown 归档和全文快照。

**解决的问题**：稍后阅读清单里全是标题和链接，不点开就不知道讲了什么，也不知道值不值得读。

## 工作方式

```
微信文章 → 复制链接 → 点桌面小组件（HTTP Shortcuts）
        → GitHub repository_dispatch → Actions 跑 Python
        → 抓正文 → AI 消化 → 写 Notion + 写本仓库 md → 自动提交
```

约 1 分钟后，Notion 里就能看到这篇文章的摘要、关键词、洞见和优先级，页面正文是全文快照，**不用回微信点链接也能读完**；原文被删也不丢。

## 目录结构

| 路径 | 内容 |
|---|---|
| `notes/YYYY-MM.md` | 月度索引，按剪藏时间分组，最新的在最上面 |
| `archive/YYYY-MM/*.md` | 每篇文章的全文快照 |
| `data/index.json` | 剪藏索引，用于查重 |
| `src/clipper/` | 处理流水线源码 |
| `tests/` | 单元测试 |
| `docs/` | 设计文档 |

## 一次性配置

### 1. Notion（可选，不配就只写 md）

1. 打开 <https://www.notion.so/my-integrations>，新建 internal integration，复制 token。
2. 在 Notion 里建一个空白页面（例如「公众号剪藏」），右上 `···` → **Connections** → 添加刚才的 integration。
3. 复制该页面 URL 末尾那串 32 位字符，就是 parent page id。
4. 本地跑一次，自动建好带全部属性的数据库：

   ```bash
   NOTION_TOKEN=<你的token> python -m clipper init-notion --parent-page <页面ID>
   ```

   命令会打印 database id，下一步要用。

数据库属性：标题、链接、剪藏时间、发布时间、摘要、关键词、洞见、AI优先级（高/中/低）、优先级理由、阅读状态（未读/在读/已读/已放弃）。
建议建两个视图：默认视图按「剪藏时间」分组 + 倒序；「待读」视图过滤 `阅读状态 = 未读`，按 AI优先级排序。

### 2. GitHub Secrets

仓库 Settings → Secrets and variables → Actions，添加：

| 名称 | 说明 |
|---|---|
| `AI_API_KEY` | AI 服务密钥（必填） |
| `AI_BASE_URL` | 默认 `https://api.deepseek.com`，换服务商时填 |
| `AI_MODEL` | 默认 `deepseek-chat` |
| `NOTION_TOKEN` | Notion integration token（不填则只写 md） |
| `NOTION_DATABASE_ID` | 上一步得到的 database id |

### 3. 手机端触发器（Android · HTTP Shortcuts）

装 [HTTP Shortcuts](https://http-shortcuts.rmy.ch/)（免费开源），新建一个 shortcut：

- **Method**：`POST`
- **URL**：`https://api.github.com/repos/Bryce505/Notes/dispatches`
- **Headers**：
  - `Authorization: Bearer <细粒度PAT>`
  - `Accept: application/vnd.github+json`
  - `X-GitHub-Api-Version: 2022-11-28`
- **Body**（JSON）：

  ```json
  {"event_type": "clip", "client_payload": {"url": "剪贴板变量"}}
  ```

  `url` 的值用 HTTP Shortcuts 的 **Insert Variable → Clipboard** 插入，别写死。

PAT 在 GitHub → Settings → Developer settings → **Fine-grained tokens** 生成，
Repository access 只选 `Bryce505/Notes`，权限只给 **Contents: Read and write**。

最后把 shortcut 放到桌面小组件。日常用法：微信文章 `···` → 复制链接 → 点小组件。

## 命令行用法

```bash
# 单篇
python -m clipper clip https://mp.weixin.qq.com/s/xxxx

# 只跑抓取和 AI，不写任何存储，用来验证配置
python -m clipper clip https://mp.weixin.qq.com/s/xxxx --dry-run

# 批量导入（flowus 等历史存量），格式见 links.example.txt
python -m clipper batch links.txt --interval 4
```

批量导入也可以不用命令行：Actions → 「剪藏公众号文章」→ Run workflow，把链接粘进输入框即可。

## 设计取舍

- **为什么要复制链接而不是直接转发**：微信的转发列表不包含公众号会话，也没有开放个人号消息接口。能读微信消息的方案都要逆向 hook 客户端，违反用户协议且有封号风险，所以选择了复制链接这条完全合规的路径。
- **为什么 Notion 和 md 都写**：Notion 负责查询和手机阅读，md 负责长期归档与防平台锁定，两份数据同源，成本几乎为零。
- **为什么按剪藏时间分月**：这是稍后阅读清单，本月收的就该出现在本月，不会因为剪了篇旧文而沉到下面找不到。
- **AI 挂了怎么办**：摘要降级为提示文案，但正文和链接照常入库，不丢内容。
- **Notion 挂了怎么办**：md 照写，不阻断。

## 本地开发

```bash
python -m pytest -q
```

本机固定使用 `D:\Anaconda\envs\dev\python.exe`，运行前设 `PYTHONNOUSERSITE=1`；
安装依赖须带代理参数：`--proxy http://127.0.0.1:7897 --trusted-host pypi.org --trusted-host files.pythonhosted.org`。

# Obsidian 平替来了：这次连服务器都不要钱

- 原文链接：https://mp.weixin.qq.com/s/4Gk-BmpIyDZ-yhL4HyUkdg
- 公众号：草稿鸭
- 发布时间：2026-10-26
- 剪藏时间：2026-11-08 07:35

---

"

别人的房子 ，说到底住得不踏实。笔记该有个 一分钱租金不用交 的住处。

—— 草稿鸭

如果你正在用 Obsidian，或者眼馋别人家的“第二大脑”但 懒得折腾 ，这篇是写给你的。

一句话结论放这。GitHub 上有个叫 EdgeEver 的开源笔记工具，今天凌晨刚发布 v2.5.0，星标 2.7k，能整个跑在 Cloudflare 免费额度里， 服务器一分钱不花 ，AI 还能 直接读你的笔记 。

！丑话说前头 🕳

Cloudflare 有个步骤要 绑支付方式 ，iOS 客户端要 中国区以外的 Apple ID ，免费额度大约 15 万条短笔记加 5 万张图 ，超了就得加钱，或者换 Docker 自己搭。

这三条能接受，再往下看。接受不了， 现在关掉 ，不耽误时间。

📌 本文看点

01

白嫖 Cloudflare 的真相

02

三条部署路挑一条

03

别急着卸 Obsidian

WHAT

Obsidian 平替，平在哪

EdgeEver 是个开源的笔记和知识库工具。GitHub 仓库里的定位原话是， 印象笔记和 Obsidian 的替代品 ，多端即时同步，原生支持 MCP。

打开还是那个熟悉的三栏。左边目录、中间列表、右边写笔记。但 同步不要钱 ，AI 能直接进来翻你的东西。

客户端也铺得全。macOS、Windows、Linux、iOS、Android，加一个网页版，应用商店能直接下载。一个开源项目把 六个端凑齐 ，不多见。

我截图那会儿，GitHub 仓库页面显示星标 2.7k、fork 1.4k。提交历史里， 两小时前还有更新 。

fork 数 超过星标的一半 ，这事在 GitHub 上不多见。

点星是动动手指，fork 是真把代码拉回自己机器上。一半以上的人选择 拉走而不是点个赞 ，是真搭起来了。

[图片]

— GitHub 仓库页面显示星标 2.7k、fork 1.4k，两小时前仍有提交

FREE

连服务器都不要钱，是真的吗

先给结论。真的，但 有前提 。

EdgeEver 能整个跑在 Cloudflare 的免费额度里。个人使用，README 写的数是大约 15 万条短笔记加 5 万张图 ，一个月 $0 。

15 万条是什么概念？从今天起每天记 10 条， 能记 40 年 。

Cloudflare 那套名词，小白听着头大。翻译一下， 就三样东西 。

Workers 是跑腿的。你的网站、接口、逻辑，全靠它在全球节点跑， 不用你买机器 。

D1 是账本。笔记的目录、标题、内容，全记在这本 云端小账 上。

R2 是仓库。图片、附件，堆在这个 云端仓库 里。

EdgeEver 就是把这三样拼成一个完整的笔记应用。你访问的是一个网址，背后 没有一台属于你的服务器 ，只有 Cloudflare 全球的节点。

容量不够怎么办？换 Docker。笔记跑在自家 NAS 或者小主机上，存储看硬盘有多大，README 的说法是 百万条笔记 也撑得住。一个工具，两种活法。白嫖路线管个人，自托管路线管胃口。

忘了说协议。EdgeEver 用的是 AGPL-3.0 ， 代码全公开 。嫌 Cloudflare 不放心，可以把整个项目搬回自己机器，连“官方”这个词都不用认。

再说数据归属。云笔记说没就没的故事，大家都听过。数据 寄人篱下 ，说到底住的是别人的房子。

EdgeEver 的底子是标准 SQLite，能无损导出 ZIP，Markdown 随时导出导入。翻译一下，真不想用了，你的笔记是 一整套搬得走的文件 ，不是锁死在格式里的二进制。

我先替你跑了一趟。官方有个 demo 站， 账号密码就摆在登录页上 ，打开就能逛。

登录进去，70 多条演示笔记躺在那。五个笔记本分组，多维表格、思维导图、海报都建好了。我随手打了段字存进去，顶部弹出提示，笔记 已同步到云端 。这是个共享环境，我操作的功夫还有别人在建笔记，时间戳一分钟一刷新。

顺带说个细节。官方的演示笔记里自带一张对比表，把 Evernote、Obsidian 和 EdgeEver 摆在一行比。代码是闭环还是开源，云同步收不收费，一眼看完。敢把 对比表放进自己 demo 的项目，不多见。

一个人一个独立工作区，逛完拍屁股走人， 不欠服务器一分钱 。

[图片]

— demo 站登录页，账号密码公开

[图片]

— demo 工作区实测：三栏界面，70 多条演示笔记

[图片]

— 我打的字存进去后，顶部弹出云端同步提示

！丑话环节 🕳

R2 这个仓库，用之前要先在 Cloudflare 开通 R2 订阅、绑定支付方式。国内的双标卡、Visa、万事达都认，PayPal、Apple Pay 也行。

注意，是 绑定，不是扣费 。免费额度内，Cloudflare 的说法是不会扣你钱。但少了这一步，部署到第三步就卡死。

「这就是“连服务器都不要钱”的代价。钱可以不给，卡得先押那。」

DEPLOY

三条部署路，挑一条

部署有三条路。我按省事程度排了个序。

STEP 01 路一，甩给 AI Agent

标着推荐，也挺邪门。仓库里现成有一段 prompt。复制粘贴给任何一个 AI Agent，Codex、Claude、Cursor、WorkBuddy 都行。它自己会去 Fork 仓库、建数据库、配密钥、部署、验证，最后把一个能用的网址还给你。

你出的力就四样。 复制、粘贴、等、设密码 。这段是仓库里现成的，直接复制粘贴，不用看懂。

. . . PROMPT

Deploy EdgeEver entirely through GitHub and Cloudflare:

1. Fork https://github.com/tianma-if/edgeever.

2. Create D1 `edgeever` and R2 `edgeever-resources` in Cloudflare.

3. In Workers & Pages, create a Worker named `edgeever` from the Fork's `main` branch.

Use the repository root, keep Cloudflare's default Workers Builds deploy command,

and ensure its API token can read and edit D1. Select Save and Deploy.

4. After the Worker is created, add the user's chosen password as the runtime Secret

`EDGE_EVER_AUTH_PASSWORD` (preferably at least 32 characters).

The username defaults to `admin`.

If the user specifies another, set `EDGE_EVER_AUTH_USERNAME` as a Workers Builds

variable before the next build.

5. Run the build again, verify `/api/health` and `/api/openapi.json`, then log in

with that administrator username and password.

6. Enable and manually run the GitHub Actions workflow named `Update deployed EdgeEver`

once so the Fork can automatically receive future stable releases and fixes.

STEP 02 路二，手动部署

六步，适合想搞清楚每一步的人。

Fork 仓库 —— 点 GitHub 右上角 Fork，把 EdgeEver 复制到自己账号下

建两个资源 —— 在 Cloudflare 建 D1 数据库 edgeever 和 R2 存储 edgeever-resources

创建 Worker —— 用 Fork 的 main 分支建名为 edgeever 的 Worker，构建命令保持默认

设管理员密码 —— 至少 32 位，存成运行时密钥 EDGE_EVER_AUTH_PASSWORD，用户名默认 admin

构建并验证 —— 第一次如果因为缺密码失败，是预期行为，补上密钥重试；部署完看 /api/health 返回 200

打开自动更新 —— 去 Fork 的 Actions 页面，手动跑一次更新工作流，以后稳定版自动跟进

第一次构建失败，别慌。README 的原话是，初始构建主要用来初始化 Worker 实例，没设密码它当然起不来。补上密钥再点一次重试，这事就翻篇。

STEP 03 路三，Docker 一条命令

适合有 NAS 或者家里小主机的人。装好 Docker Compose v2，把这行贴进终端。

. . . BASH

curl -fsSL https://edgeever.org/install.sh | bash

回车。你的笔记就跑在自己家硬盘上， 拉代码跟领快递一样 ，领完即用。

三条路，一个终点。一个你自己的笔记网址，加一套 完全属于你的数据 。

MCP

换过来之后，AI 真能读笔记吗

能。这是 EdgeEver 跟 Obsidian 拉开身位 的地方。

先说 MCP 是什么。一句话， AI 世界的插座标准 。

以前的 AI 助手想碰你的笔记，得靠插件和导入导出，像隔着一层玻璃聊天。MCP 就是 把玻璃拆了 ，AI 可以直接读写笔记库。整理、打标签、写摘要、按你的笔记回答问题，全是原生支持。

桌面端还支持 ACP ，能直连你电脑上的本地编程 Agent。Codex、Claude Code、DeepSeek、WorkBuddy， 喊一声就能过来干活 。演示里有个活例子：选中一段笔记让 Agent 分析，思维导图的分支直接长在笔记里。

不想用第三方 AI，也行。EdgeEver 支持 BYOK ，自带钥匙。OpenAI、Claude、Gemini 或者你自己的接口，填进去就能用。 家钥匙攥自己手里 ，比住民宿安心。

侧边栏还常驻一个 AI 助手。划一段文字，解释、翻译、校对、改写， 随叫随到 。半夜赶稿卡在一个词上，它比翻群聊记录快得多。

再说剪藏，这是个 刚需 。

EdgeEver 的浏览器剪藏扩展，Chrome、Edge、Firefox 都有。看到好文章一键存，存的是干净 Markdown。X、小红书、公众号、知乎、B 站、YouTube、豆瓣、Reddit， 20 多个平台 做了深度适配，不是整页截图那种糙活。

小红书上那些“收藏从未停止”的干货，终于有个 正经去处 。

还有些活它在行。RSS 每天自动摘要，噪音先过筛子。一句话生成多维表格，标签日期选项自动分好列。 功能是真铺了 ，值不值另说。

老用户迁移，也替你想好了。印象笔记的老库，用现成的 ENEX 导入脚本，配合 MCP 整个搬过来。Obsidian 用户更简单，你的 Markdown 文件本来就能 直接导入 。

[图片]

— 官网功能区：AI 画图、本机 ACP 协同、常驻侧边栏

WHO

别急着卸 Obsidian

吹完了，说点冷静的。

EdgeEver 适合这些人

同步收费受害者

Obsidian 官方同步是订阅制，这笔钱从此是零

AI 原生党

MCP 和 ACP 内置，不用满世界翻插件

剪藏重度患者

20 多个平台深度适配，有人维护

白嫖爱好者

Cloudflare 免费额度，个人用大概率够

下面几类人，劝你先按住卸载的手

本地 Markdown 原教旨

Obsidian 的笔记是赤裸裸的 .md 文件，EdgeEver 的底子是 SQLite，能导出但格式不同

插件生态依赖者

Obsidian 市场几千个插件，EdgeEver 的插件体系刚起步

完全离线党

EdgeEver 需要服务端组件，想本地跑，走 Docker

iOS 国区用户

App Store 只上架了外区，国区账号下不到

团队协作需求

多账号是每人一个独立工作区，不是多人同编一篇

15 万条以上重度用户

免费额度装不下，走 Docker 自己扩容

想稳一手，就并行用

老库先别动，两边一起用两周。新笔记往 EdgeEver 记，老笔记留 Obsidian 查。等哪天你开 Obsidian 的次数 一周不超过三次 ，再动手搬家。ENEX 和 Markdown 导入都现成，搬个家比搬家公司还省事。

说回我自己。老库我不会搬，几年的笔记搬一次伤筋动骨。但下次开新选题库，我会拿它试。白嫖的服务器，不用白不用。

v2.5.0 的更新说三个

远程图床，NAS 玩家的图片流打通了。17 个真机演示，云体验不要钱。俄语是社区捐的。这种活有人接，说明 项目还活着 。

插件和主题也开放了。官方市场、GitHub、Manifest URL 都能装，开发者可以用 @edgeever/plugin-api 自己扩。生态刚发芽，但 门是开着的 。

THE END

写到最后

Obsidian 是好东西，没人否认。但 “好”和“合适”是两回事 。当你只是想安安静静记点笔记、让 AI 搭把手、还不想每月掏同步费的时候，多个选择总不是坏事。

EdgeEver 现在 2.7k 星，一半以上的人 fork 下来真部署了。热度能不能持续，不好说。但至少今天，它是那个 “不要钱还开放” 的选项。

你可以先不删 Obsidian。去 demo.edgeever.org 点两下，或者复制那段 prompt 让 AI 帮你部署一个。反正不要钱， 试错成本就是一段复制粘贴 。

一个工具值不值得换，别人说一万句，不如自己搭一次。

把这篇 转给那个还在为同步付费、又嫌自建麻烦的朋友 。他可能只是还不知道有这条路。

评论区聊聊。你现在用什么笔记工具，被什么劝退过。同步费、插件山，还是同步失败，挑一个聊聊。

END

我是草稿鸭，专注把 AI 圈的大事用大白话讲清楚。

如果你觉得今天这篇有收获，欢迎 点赞、在看、转发 三连，我们下篇见。

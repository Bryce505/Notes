# 给 Claude Code 装上这 17 个插件，效率直接翻几倍

- 原文链接：https://mp.weixin.qq.com/s/1MgpVBHn1OLAjfCKM83ImA
- 公众号：GoldenSpider.AI
- 发布时间：2026-07-04
- 剪藏时间：2026-08-22 10:16

---

[图片]

Claude Code 开箱即用已经是地表最强的 AI 工具之一。但真正拉开差距的，是往里面加 skill、CLI 和插件。

问题是，能往 Claude Code 上装的东西有好几百个。哪些值得花时间，尤其对新手来说？这篇就挑出 17 个作者自己在用、并且认为值得的，分成设计、效率、数据三类，每个都讲清楚它是什么、怎么用、为什么值得装。

设计类：专治 Claude 写出来的“AI 味”

Taste Skill —— 给 AI 补上“审美”。 你大概常听到一句话：AI 没有品味。Taste Skill 就是来解决这件事的开源项目，主打消灭 AI 生成的那股廉价感。它内部其实打包了好几个子 skill，比如 image to code（截图转代码）、redesign（重做设计）、output 等，目标都是把前端设计做得更好看。它不挑工具，不只服务 Claude Code，任何 agent 都能用。作者展示了用它做出的网站：有带滚动动画的，也有偏传统 SaaS 风格的——观感明显不同于 Claude Code 默认产出的那种。如果你常用 AI 做落地页或任何偏设计的东西，想跳出 Anthropic 自带的前端设计 skill，值得看看。

Impeccable —— 被 GitHub 直接收编的设计 skill。 同样是开源前端设计 skill，同样冲着干掉“AI 味”、在 Anthropic 给的基础上再提升。它最近的分量在于：几天前 GitHub 把它做成了 Copilot 应用里所有人都能用的内置层——GitHub 自己看了觉得做得够好，干脆原生集成进自家 AI 工具。它是单个 skill，但内含 23 条命令，从记录改了什么、点评已有成果，到打磨、让它更大胆、更克制等等，命令多到有点让人摸不着头脑。最直观的看法是上它官网 impeccable.style：左边列出所有命令和简短说明，右边直接对比 Claude Code 的产出和 Impeccable 的产出。比如 distill 命令，能把一个信息密集的小型仪表盘剥到最精简，但同样的信息呈现得更干净。

Impeccable 还有个亮点是浏览器编辑器（目前 beta）。你可以在电脑上打开自己的网站，不用钻进终端改代码，而是在网页上直接选中元素、说“我想把这块改成 XYZ”，改动实时可见。这种可视化的上手感，正是它跟 Taste Skill 拉开差距的地方。想动手做设计的人，强烈建议试。

Awesome Design.md —— 把现成网站当模板。 这个工具的思路是：拿已经存在的网站当模板来搭你自己的站。它基于 Google Stitch 的 design.md 原则——如果你没用过 Google Stitch，这是个完全免费的前端设计工具，值得一试。所谓 design.md，是 Google 摸索出的、能让 AI 产出强前端设计的“完美 prompt”格式。Awesome Design.md 把这套模板套用到现有网站上：它收录了一大批网站，比如你喜欢 Airtable 的官网，点进去就能拿到它整站的结构拆解——配色、表面、文字、字体、间距、按钮，全都列出来，作为你搭自己网站的积木。注意：不是克隆它的网站，而是克隆它的设计语言再套到你自己身上。这些拆解还按用途分类，金融科技、加密、创意工具、效率类 SaaS……如果你就是想把“已经被验证有效的东西”搬到自己网站上，这个很合适。

效率类：让 Claude Code 更快、更省、更能干

Ponytail —— 现在全球涨得最快的 AI 仓库之一。 它能让 Claude Code 更高效：更快、更便宜、写更少的代码却保持同样的产出。具体数字（对比基线）：少写 50% 代码、少用 22% token、成本低 20%、速度快 27%。原理是写任何代码前先反问几个问题：这东西真的需要存在吗？代码库里是不是已经有了？标准库能不能做？平台原生功能是不是自带？是不是已装依赖里一行就能解决？问完这一圈，才动手写，而且只写“能跑的最少量”。因为 Claude Code 本身偏啰嗦、爱从零造轮子，哪怕东西早就有了。补一句：上面这些数字是用 Haiku 测的；作者用 Opus 跑同样基准时，差距更夸张。想省 token，强烈推荐。

notebooklm-py —— 把 Claude Code 接到 NotebookLM。 NotebookLM 是 Google 最好的产品之一，完全免费：你把任何资料丢给它——PDF、文档、YouTube 视频，或让它自己去找——然后就能跟 AI 聊这些内容，还能让它产出交付物：幻灯片、图片、信息图、视频等等。NotebookLM 没有官方 API，但这个 CLI 绕过了这点，让你在终端里做到网页端能做的一切，方便你搭把 NotebookLM 接进去的工作流，同时把活儿免费甩给 Google 的服务器。更妙的是，CLI 给的工具比网页端还多：批量下载、导出测验和闪卡、把对话存成笔记等等。作者用得最多的是配 YouTube：抓视频链接、拿到字幕转写、回答关于它的任何问题——在终端里完成，体验很爽。

Playwright CLI —— 让 Claude Code 像人一样操作浏览器。 作者认为这是今天最强的之一，核心是浏览器自动化。碰到“没有 API、但我想让 Claude Code 像真人一样上网站点按钮、填表单”的场景，Playwright CLI 就能干。除了自动化，它对前端设计也很有用——作者一度想把它归到设计类。比如你做了个带表单的网站，与其自己手动一个个试边界情况，不如开 Playwright CLI，它会拉起一大堆浏览器，几分钟内帮你全测完，你完全不用插手。注意别和 Playwright MCP 搞混：CLI 比 MCP 有效得多，而且省 token 得多。

Codex 插件 —— 把 OpenAI 拉来给 Claude 挑刺。 这是 OpenAI 出的官方插件，能把 Codex 和 GPT 模型接进 Claude Code。它特别适合代码审查、对抗式审查——大家都知道 Claude Code 偏爱自己写的代码，有时我们需要第二双眼睛看看它干了什么。这个插件就提供这个能力，还带 Codex Rescue 这样的命令，能把整个功能甩给 Codex：让 Claude Code 做应用的一部分、同时让 Codex 做另一部分，两边各取所长。

GWS（Google Workspace CLI）—— 那个把作者搞到被开除的工具。 它不是 Google 官方产品，由一名 Google 开发者做出来，火到把这哥们儿弄丢了工作。如果你天天泡在 Google Workspace 里、又嫌官方 Google Connector 功能不够（比如 Connector 干不了发邮件这种事），GWS 能补上，还内含 40 多个 skill：周报摘要、站会报告、会议准备、邮件转任务，一堆预置工作流开箱即用。它的安装和配置会稍微麻烦些，但想给 Google 这套配上 Claude Code 的火力，选它不会错。

GitHub CLI —— 这个现在人人都该有了。 如果还没装，它该是你第一个装的。只要你用 Claude Code 做东西，迟早要推到 GitHub，这个 CLI 让推送变得极其简单。

Skill Creator —— 作者眼里最重要的那个 skill。 这是 Anthropic 官方 skill，能做的不止创建新 skill，还能修改、改进已有 skill，以及衡量 skill 的表现。skill 很强，但有时我们根本不知道某个 skill 是否真有存在必要，或者改完到底有没有变好。Skill Creator 能自动对“第一版”和“所谓改进版”做 A/B 测试，也能测“用这个 skill”对比“不用”的差别，从而拿到客观证据。考虑到 skill 是 Claude Code 里最强的东西之一，作者认为这是最重要的 skill。安装也简单：进 Claude Code 后输入 /plugin ，搜 skill creator，装上即可，在 installed 里能看到它。

数据类：抓取、研究、记忆与变现

这一类围绕数据库、研究、抓信息存信息、以及“记忆”。

Last 30 Days —— 曾经的 GitHub 第一仓库。 它做的是用 Claude Code 做研究，而且远不止简单网搜——它在一批特定来源上深挖：Reddit、Twitter、YouTube、TikTok、Reels、Hacker News、Polymarket 等等，让你对某个主题、以及人们在各平台上怎么聊它，拿到很深的视角。适合在 Claude Code 里做每日简报，或做任何依赖真实数据的交付物。它也是个好替代——省得你对什么都甩一句“深度研究”然后烧掉一堆 token。

Firecrawl CLI —— 抓网页的利器，尤其是带反爬的。 Firecrawl 是抓取领域最好的工具之一，特别擅长那些有大量机器人防护的页面。它分付费版和开源版：付费版靠自家专有模型，破反爬最强；但开源版也能拿到很多同样的能力。如果你只是想要一个专做特定抓取的工具，不需要 Last 30 Days 那种一次轰一堆来源，Firecrawl 很合适，且明显强过 Claude Code 标准网搜——因为它不止抓取，还能跟页面交互、发现并爬取网站上所有 URL，设置项很多，能精细控制你想抓什么。

Autoresearch —— 来自 Karpathy 的“盒装机器学习”。 思路是：拿一个你想优化的应用丢给它，它就自动一轮接一轮地跑，努力改进你设定的目标。比如有个 Python 应用你想让它跑更快——这是个跟时间挂钩的明确成功标准（1 秒 → 0.99 秒），丢进 Autoresearch，它就一个实验接一个实验地试，直到把运行时间压到最低。作者给的例子里它跑了 83 个实验，每次都试点新东西，并记录哪些有效哪些没用，83 次下来拿到 15 处改进，全自动完成。这个项目还挺轻量。但记住：它不是万能的，你得是在做某种有明确、客观成功标准的应用或任务上用它——想想时间和数字这类可量化的指标。

Supabase CLI —— 一站搞定数据库和登录。 作者喜欢 Supabase，因为免费额度大方，能覆盖建应用时的很多基础需求。比如你做个带表单提交、要收集邮箱的网站，这些邮箱得存进数据库——Supabase 能搞定，直接从 Claude Code 用自然语言建库：“用 Supabase CLI 建个合理的数据库”，它就全自动做完。它还能处理鉴权，网站需要登录功能它也能给。复杂的东西，靠 Claude Code 加上 Supabase 这套工具、用自然语言就能被一步步引导着做完。Supabase 也支持本地运行。

Obsidian —— 给 Claude Code 加记忆最简单的方式之一。 Obsidian 能把电脑上的文件夹设为 vault，这些 vault 成为你往里塞信息的宝库。在 vault 里打开 Claude Code，它就接入了你加进去的各种文档构成的知识图谱。配置得当的话（作者说他有大量相关内容），它等于给 Claude Code 一张你全部文档的地图，于是它能很高效地回答关于这些文档的问题。另外还有专门的 skill 帮 Claude Code 更好地用 Obsidian：去 GitHub 搜 Obsidian skills，这个仓库由 Obsidian 创始人本人建立，专门教 Claude Code 如何最佳地融入你的 Obsidian 体系。

LightRAG —— 来真的知识图谱：RAG。 说到记忆就要聊 RAG（检索增强生成）。相比 Obsidian，这是一个台阶上的升级——因为它不是那种“伪知识图谱”，而是真正意义上的知识图谱加 embedding。LightRAG 是作者最喜欢的搭建这类知识图谱 RAG 系统的工具之一：轻量、快，且是进入更复杂 RAG 系统的好入门。一切都能跑在 Claude Code 里，查询也都从 Claude Code 走，两者连起来很容易。等你熟悉了 LightRAG，可以进阶到 RAG-Anything 这类更高级的东西——它不再局限于 PDF 和文本，能纳入图片、图表这些传统 RAG 系统（甚至 Obsidian）通常更难处理的内容。

Stripe CLI —— 想让应用赚钱就装它。 如果你做的应用想真正变现、要处理任何交易，就会需要 Stripe CLI，它让对接 Stripe 省事得多。Stripe 的网页后台用起来挺折腾，而任何能让你通过终端、用自然语言在 Claude Code 里控制和修改应用的东西，对你都是巨大的加分。

怎么挑

17 个工具，三类需求：要把界面做得不像“AI 默认产物”，看设计类；要让 Claude Code 更快更省、或接通 OpenAI、Google、GitHub 这些外部能力，看效率类；要做研究、抓数据、给 AI 加记忆、乃至接入支付，看数据类。

不必一次全装。从你当下最痛的那一类入手，挑一两个先用起来，比囤一堆插件更实在。

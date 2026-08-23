# 用 Claude Code 搭一套 7×24 工作环境

- 原文链接：https://mp.weixin.qq.com/s/8e15DME8RMYMWzj0YvsG_g
- 公众号：AI智闻说
- 发布时间：2026-06-29
- 剪藏时间：2026-08-23 17:12

---

装好了 CLAUDE.md、Skills、Hooks，AI 能帮你干活了，但每次还得你先开口。7×24 的关键是你不在的时候它还能自己跑。

早上到公司，打开电脑，发现昨晚定的代码审查已经跑完了、PR 也提了、CI 也过了。你走之前设好了 5 层配置：cron 定时跑、Hooks 监听事件、Memory 记住了上次审到哪、tmux + SSH 让你在地铁上用手机看了一眼结果。5 层拼起来，Claude Code 就从"你叫才动"变成"自己会跑"。

这篇讲的方案全部基于 CLI + API key，不需要 claude.ai 账号登录。Routines、Remote Control、Channels 这些需要官方认证的功能，文末统一提一笔。

5 层都是什么，一张图看全

层

解决什么问题

API key 用户能用的方案

定时触发

AI 自己醒来干活

+ cron + /loop

事件响应

AI 内部事件桥接到外部通知

Hooks（Notification / PostToolUse / Stop）

持久记忆

关机再开记忆不丢

CLAUDE.md + auto memory + --resume + loop.md + SessionStart(compact) Hook

远程操控

人不在电脑前也能指挥

tmux + SSH + 手机终端 / Hooks 推送通知

隔离执行

多任务并行不冲突

Worktrees + --worktree

[图片]

第 1 层：定时触发：让 AI 自己醒来干活

"到点就干"是 7×24 最基本的要求。两种方式：会话内轻量定时，和系统级定时。

/loop：会话内轻量定时

/loop 5m check the deploy — 固定 5 分钟间隔

/loop check the deploy — Claude 自选间隔（1 分钟 ~ 1 小时）

/loop — 内置维护：继续未完成工作 + 处理 PR 评论 + 跑清理

/loop 适合临时轮询，比如盯着一个部署或者等 CI 结果。7 天自动过期，不会忘了关。

自定义默认提示词：在 .claude/loop.md （项目级）或 ~/.claude/loop.md （用户级）里写你要做的事，每次 /loop 自动读取。

claude -p + cron：系统级定时

/loop 只在会话内有效，关了终端就停。想要更持久的定时，用 claude -p （非交互模式）搭配系统 cron。

一个最简的例子：每天早上 9 点跑一次代码审查。

# 编辑 crontab

crontab -e

# 每天早上 9 点跑代码审查

# 注意：cron 的 PATH 很精简，需要 source shell 配置让 claude 命令可用

0 9 * * * source ~/.zshrc 2>/dev/null; cd /path/to/project && claude -p "审查昨天所有的 commit，生成审查报告" --allowedTools "Read,Bash(git log *),Bash(git diff *)" --output-format text >> ~/claude-reviews.log 2>&1

source ~/.zshrc 是关键：cron 环境不会自动加载你的 shell 配置，不 source 的话 claude 命令找不到。如果你用的是 bash，换成 source ~/.bashrc 。也可以不 source，直接写 claude 的全路径（如 /Users/你/.local/bin/claude ），效果一样。

-p 模式的关键参数：

--allowedTools — 预批准工具，不弹权限确认，脚本才能跑完

--output-format text — 纯文本输出，方便重定向到日志文件

--bare — 跳过所有本地配置（hooks、skills、plugins、MCP），保证结果可复现。适合 CI/CD 管线

--continue — 接着上次的会话继续，适合多轮任务

更实际的用法：把 cron 触发 + 日志 + 通知串起来。

# 每小时检查一次依赖是否有安全漏洞

0 * * * * source ~/.zshrc 2>/dev/null; cd /path/to/project && claude --bare -p "检查项目依赖是否有已知安全漏洞，如果有的话列出漏洞名称和修复版本" --allowedTools "Read,Bash(npm audit *)" --output-format text | tee -a ~/dependency-audit.log

claude -p 也能用在 CI/CD 管线里。GitHub Actions 的 schedule 触发器调 claude -p ，等于在云端跑了定时任务。

第 2 层：事件响应：AI 内部事件桥接到外部通知

定时触发是"到点就干"，事件响应是"有事就通知你"，让你能在第一时间介入。

需要说明：API key 模式下，真正的"外部事件推着 AI 走"（CI 失败了主动推到 AI 会话里）做不到——这需要 Channels 或 Routines GitHub 触发器，都得 claude.ai 认证。Hooks 能做的是反过来的：Claude Code 内部发生事件时，桥接到你的外部通知渠道。

Notification Hook：AI 等你的时候通知你

Claude 等你审批时，会话就卡住了。如果你不在终端前，这个等待可能拖很久。挂一个 Notification Hook，审批等待时自动推通知。

在 .claude/settings.json 里配置：

{

"hooks" : {

"Notification" : [

{

"matcher" : "permission_prompt" ,

"hooks" : [

{

"type" : "command" ,

"command" : "osascript -e 'display notification \"Claude Code 等你审批\" with title \"Claude Code\"'"

}

]

}

]

}

macOS 用 osascript ，Linux 用 notify-send 。通知弹出来了，你才知道 AI 在等你。

更进阶的：接一个 Bark 或者 Server酱 的 webhook，推送通知到手机。Hook 里的 command 换成 curl 推一下，手机上就收到了。这样人不在电脑前也能第一时间知道。

Stop Hook：Claude 干完活自动通知

Stop Hook 在 Claude 每次回复结束时触发，适合跑完长任务后通知你：

{

"hooks" : {

"Stop" : [

{

"hooks" : [

{

"type" : "command" ,

"command" : "curl -s 'https://sct-api.ftqq.com/YOUR_KEY.send?title=Claude+Code&desp=任务完成'"

}

]

}

]

}

Stop 事件不支持 matcher，每次回复结束都会触发。如果只想在特定任务完成时通知，可以在 command 脚本里加判断逻辑。

SessionStart Hook：会话开始时自动注入上下文

每次新会话开始或者上下文被压缩后，最怕丢的是项目约束。用 SessionStart(compact) Hook，压缩完自动重新注入关键信息：

{

"hooks" : {

"SessionStart" : [

{

"matcher" : "compact" ,

"hooks" : [

{

"type" : "prompt" ,

"prompt" : "项目约定：用 Bun 不用 npm；跑 bun test 再提交；commit message 用中文。"

}

]

}

]

}

记忆断了也有兜底。这个 Hook 的价值在第 3 层（持久记忆）里更明显，但在事件响应这层先提一句：它解决的是"上下文被压缩后关键信息丢失"这个事件。

第 3 层：持久记忆：关机再开记忆不丢

7×24 真正的坑是跑着跑着忘了上次干了什么。三层记忆保底：

CLAUDE.md ：项目规范、代码风格、工作流，每会话自动加载，不用重复交代。项目级、用户级、组织级各一层，团队共享也不冲突。

Auto memory ：你纠正过的事，Claude 自动记住，下次不犯。"行动项用表格不用列表""不要废话"，教一次就记住。

--resume / --continue ：直接接上上次会话，上下文无缝延续。

再进一步： SessionStart(compact) Hook 。上下文压缩时最怕丢关键约束，挂一个 Hook，压缩完自动重新注入："用 Bun 不用 npm""跑 bun test 再提交"。记忆断了也有兜底。

loop.md ： /loop 的默认提示词，写一次每次 /loop 都读。跟 CLAUDE.md 互补：CLAUDE.md 管"所有会话的规矩"，loop.md 管"/loop 的时候具体干什么"。

第 4 层：远程操控：人不在电脑前也能指挥

AI 自己跑没问题，但有时候它需要你：审批一个文件写入、回答一个二选一。你不在电脑前怎么办？

tmux + SSH：最通用的远程方案

把 Claude Code 跑在 tmux 会话里，SSH 连上去就能操控。手机上装一个终端 App（iOS 用 Termius，安卓用 JuiceSSH），随时随地连上去。

# 在服务器或开发机上开一个 tmux 会话

tmux new -s claude-code

# 在 tmux 里启动 Claude Code

claude

# 断开 tmux（不会关掉 Claude Code）

# Ctrl+B 然后按 D

# 手机上 SSH 连回来，重新接入

tmux attach -t claude-code

tmux 会话不会因为 SSH 断开就消失。网络抖了一下，重连后 tmux attach 回来，Claude Code 还在跑，会话还在继续。

把这一步和第 1 层的 cron 结合：cron 在后台跑 claude -p ，把结果输出到日志文件。你地铁上 SSH 连进来， tail -f ~/claude-reviews.log 看结果，有问题就 tmux attach 进去用交互模式人工介入。

Hooks 推送通知到手机

第 2 层的 Notification Hook 推桌面通知，但人不在电脑前看不到。换成推手机：

{

"hooks" : {

"Notification" : [

{

"matcher" : "permission_prompt" ,

"hooks" : [

{

"type" : "command" ,

"command" : "curl -s 'https://sct-api.ftqq.com/YOUR_KEY.send?title=Claude+Code&desp=AI%E7%AD%89%E4%BD%A0%E5%AE%A1%E6%89%B9'"

}

]

}

]

}

这个例子用的是 Server酱，Bark、PushPlus、钉钉机器人同理。手机收到推送，打开终端 App，SSH 连进去回一句，AI 接着干。

更简单的：Git 仓库当通信管道

如果手机终端也懒得开，还有一个更轻量的方案：用 Git 仓库本身当通信管道。

Claude Code 跑在服务器上，cron 定时触发，它把审查结果和需要你决策的问题写到一个 AI-REPORT.md 文件里，自动 commit 并 push。你在手机上用浏览器看 GitHub 仓库，读 AI-REPORT.md 。需要回复的话，直接在 GitHub 上编辑 AI-REPORT.md 写上你的指示，push 回去。

要让这个管道生效，在 CLAUDE.md 里加一句规则："开始任务前先读 AI-REPORT.md，如果有人类指示就优先执行"。这样下一次 cron 触发 claude -p 时，Claude 读到你的指示，接着干。

没有手机终端、没有推送服务，Git 仓库本身就是一个异步通信管道，而 Claude Code 天然擅长读写 Git 仓库。

前置条件：服务器上需要配好 git 身份（user.name / user.email）和 push 权限（SSH key 或 PAT），否则 cron 跑的 claude -p 没法自动 commit 和 push。

第 5 层：隔离执行：多任务并行不冲突

7×24 不意味着一次只干一件事。多个 cron 任务同时跑，改同一个文件就乱套。

Worktrees ： --worktree 让每个任务在一个独立 Git worktree 里运行，互不干扰。

# cron 里的两个任务各跑各的 worktree

0 9 * * * source ~/.zshrc 2>/dev/null; cd /path/to/project && claude -p "审查代码" --worktree --allowedTools "Read,Edit,Bash(git *)" 2>&1 >> ~/review.log

0 10 * * * source ~/.zshrc 2>/dev/null; cd /path/to/project && claude -p "审计依赖" --worktree --allowedTools "Read,Bash(npm audit *)" 2>&1 >> ~/audit.log

加了 --worktree ，每个任务在独立的工作目录里跑，不会互相踩文件。各自 push 时 git 会自动处理，不用担心 merge 冲突。

判断标准很简单：任务之间可能改同一文件 → 加 --worktree ；任务只读不改 → 直接跑。

拼起来：一个真实的 7×24 场景

用一个完整场景把 5 层串起来。

场景：每日自动代码审查 + 依赖审计

每天早上 9 点，cron 触发 claude -p （第 1 层：定时），Claude 自动审查昨天的 commit，生成的审查报告写进 AI-REPORT.md 并自动 commit、push。CLAUDE.md 里有规则："开始任务前先读 AI-REPORT.md，优先执行人类指示"。

审查过程中遇到需要人判断的安全问题，Claude 把问题写进报告。Notification Hook 通过 Server酱 推送通知到手机（第 2 层：事件 + 第 4 层：远程）。你在外开会，手机弹了一条通知，打开 GitHub 看 AI-REPORT.md ，直接在文件里写上"这个没问题，放行"，push 回去。

下一次 cron 触发时，Claude 读了 AI-REPORT.md 里你的指示，继续推进。Claude 记住了你对这类安全问题的判断，写进 auto memory（第 3 层：记忆），下次遇到同类问题不再来问你。

同时，另一个 cron 任务在跑依赖审计（第 1 层 + 第 5 层：定时 + 隔离），加了 --worktree ，和代码审查跑在不同的工作目录里，互不干扰。审计结果也 push 到各自的分支。

你在通勤路上用手机浏览器看了一眼 GitHub，审查、审计全跑完了，该 approve 的 approve 了，需要你决策的已经等你回复。

5 层都到位了。你一整天没坐在电脑前，但代码审查和依赖审计全跑完了。

有官方订阅的话

前面 5 层全部基于 CLI + API key，不需要 claude.ai 认证。如果你有 Pro/Max 计划并且网络环境允许，还有这些能力可以叠加上去：

功能

解决什么问题

和 API key 方案的对应关系

Routines（云）

电脑关了也在跑的定时任务

替代 cron + claude -p ，不需要电脑一直开着

Remote Control

手机直接操控本地会话

替代 tmux + SSH，体验更好，有推送通知

Channels

Telegram/Discord/iMessage 消息推入会话

替代 Hooks 推通知，双向通信更自然

Desktop 定时任务

本地跑但不用开终端的定时

替代 cron，有 GUI 管理，有补跑机制

这些功能需要 claude.ai OAuth 认证，API key 用户用不了。但 5 层架构的思路不变，只是每层的实现工具换了。

写在最后

CLAUDE.md、Skills、Hooks 让 AI 能帮你干活，cron、tmux、Hooks 推送让它自己会跑。5 层配齐，Claude Code 能在你不在的时候自己跑起来。

打开 Claude Code，跑一次 /loop 5m check the deploy 。5 分钟后 Claude 自动检查一次部署状态，不用你盯着。这是 7×24 最轻量的起步，先让 AI 自己跑起来，再加层。

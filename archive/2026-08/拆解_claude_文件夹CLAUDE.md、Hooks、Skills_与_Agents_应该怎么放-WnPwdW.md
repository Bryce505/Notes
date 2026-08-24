# 拆解 claude 文件夹CLAUDE.md、Hooks、Skills 与 Agents 应该怎么放

- 原文链接：https://mp.weixin.qq.com/s/WnPwdWSHrFmAtfEfI1ymJw
- 公众号：AITestingLogs
- 发布时间：2026-07-16
- 剪藏时间：2026-08-24 11:58

---

CLAUDE CODE · GUIDE

拆解 .claude 文件夹

CLAUDE.md、Hooks、Skills 与 Agents 应该怎么放

从团队指令到个人偏好，从权限边界到自动化钩子，一次看清 Claude Code 的项目控制目录。

导 语

很多 Claude Code 用户见过项目里的 .claude/ ，却很少系统查看它。这个目录决定 Claude 在项目中读取哪些指令、可以执行哪些操作、何时触发自动检查，以及如何调用可复用流程和专用智能体。

配置清楚之后，团队可以减少重复说明，让 Claude 在不同会话中持续遵守同一套工程规则。

[图片]

01

两个目录，两种作用范围

开始配置前，先分清两个位置：

your-project/.claude/

~/.claude/

项目级目录服务整个团队。它通常进入 Git，成员可以共享同一套规则、命令和权限策略。

用户主目录下的 ~/.claude/ 保存个人偏好和本机状态，例如全局指令、个人 Skills、Agents、会话记录与自动记忆。

[图片]

项目配置由团队共享，全局配置只影响个人环境。

核心原则

需要团队共同遵守的配置进入项目目录；只属于个人习惯或本机环境的内容留在全局目录。

02

CLAUDE.md：项目说明书

Claude Code 启动会话时会读取 CLAUDE.md ，并把其中的内容作为持续生效的项目指令。它适合记录模型无法仅靠代码快速判断的信息。

适合写入：

✔ 构建、测试、检查与启动命令

✔ 关键架构选择和模块边界

✔ 容易忽略的编译、测试和运行限制

✔ 导入、命名、校验与错误处理约定

不建议写入：

— 已经由 linter 或 formatter 自动执行的规则

— 可以通过链接访问的整篇文档

— 与当前项目无关的长篇原理说明

建议把 CLAUDE.md 控制在约 200 行以内。重点在于高密度记录关键约束，避免大量背景文字占用上下文。

# Project: Acme API ## Commands npm run dev          # Start dev server npm run test         # Run tests (Jest) npm run lint         # ESLint + Prettier check npm run build        # Production build ## Architecture - Express REST API, Node 20 - PostgreSQL via Prisma ORM - All handlers live in src/handlers/ - Shared types in src/types/ ## Conventions - Use zod for request validation in every handler - Return shape is always { data, error } - Never expose stack traces to the client - Use the logger module, not console.log ## Watch out for - Tests use a real local DB, not mocks. Run `npm run db:test:reset` first - Strict TypeScript: no unused imports, ever

个人项目偏好可以放进 CLAUDE.local.md 。它与团队 CLAUDE.md 一起加载，并应留在本机，避免把个人设置提交到仓库。

03

指令如何叠加

Claude 会合并多个层级的指令。可以概括为以下四层：

1. 组织托管策略 ：由组织统一部署，优先级最高。

2. ~/.claude/CLAUDE.md ：个人跨项目偏好。

3. ./CLAUDE.md ：当前项目的团队指令。

4. CLAUDE.local.md ：当前项目里的个人覆盖。

这些内容会在会话开始时合并。发生冲突时，更具体、优先级更高的配置生效。

▦ 配图 02

[图片]

组织策略、全局偏好、项目规则和个人覆盖共同组成最终指令。

04

rules/：把指令拆成模块

当 CLAUDE.md 越写越长，可以把规则按关注点拆进 .claude/rules/ ：

.claude/rules/

testing.md

code-style.md

api-conventions.md

security.md

每个文件只负责一个主题，维护者可以独立更新。带有路径范围的规则只在 Claude 操作匹配文件时启用：

-

没有设置路径范围的规则会在每次会话中生效。对于大型项目，这种拆分方式更容易维护，也能减少与当前文件无关的指令干扰。

05

Hooks：让关键动作自动执行

写在 CLAUDE.md 里的内容仍然需要模型理解并执行。对于安全拦截、格式化、测试门禁和完成通知，可以用 Hooks 调用确定性的脚本。

工具调用通常会经过两个关键检查点：

PreToolUse ：工具运行前触发，适合阻止危险命令。

PostToolUse ：工具成功后触发，适合格式化或检查输出。

▦ 配图 03

[图片]

执行前负责拦截，执行后负责整理与校验。

三个退出码需要记住：

exit 0

成功，继续执行。

exit 1

报告错误，但工具调用继续。

exit 2

阻止执行，并把标准错误返回给 Claude。

安全 Hook 最常见的问题，是错误使用 exit 1。它只记录错误，无法真正拦截操作；需要阻止命令时应返回 exit 2。

{ "hooks": { "PostToolUse": [ { "matcher": "Write|Edit|MultiEdit", "hooks": [ { "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null" } ] } ], "PreToolUse": [ { "matcher": "Bash", "hooks": [ { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash-firewall.sh" } ] } ] } }

常用事件还包括 Stop、UserPromptSubmit、Notification、SessionStart 和 SessionEnd。Hooks 在会话启动时读取配置，中途修改后通常需要重新开启会话。

Stop Hook 要检查 stop_hook_active ，否则可能出现“阻止结束—再次尝试—再次阻止”的循环。Hook 脚本拥有当前用户权限，必须校验输入、引用变量并使用明确的脚本路径。

06

Skills 与 Agents：复用流程，隔离任务

Skills 用于封装可重复执行的工作流。每个 Skill 拥有独立目录和 SKILL.md，还可以附带参考资料、模板或脚本。

.claude/skills/

security-review/

SKILL.md

DETAILED_GUIDE.md

deploy/

SKILL.md

templates/

Skill 的描述告诉 Claude 何时使用它。适用场景出现时，Claude 可以按描述调用；用户也可以显式指定。

Agents 用于定义专门的子智能体角色。每个 Agent 有自己的系统提示、工具权限与模型选择，并在隔离的上下文中完成任务。

[图片]

Skills 打包可复用流程，Agents 在独立上下文中承担专门任务。

子智能体会吸收大量搜索与分析过程，只把压缩后的结论返回主会话。这样可以保护主上下文，并通过 tools 字段把能力限制在任务所需范围内。

07

settings.json：配置权限边界

项目级 .claude/settings.json 用于配置工具权限和 Hooks。权限一般分为三类：

allow ：无需再次确认即可运行。

deny ：始终阻止。

未匹配项 ：执行前询问用户。

明确区分允许、询问与拒绝，让自动化保持在可控范围内。

加入 $schema 后，VS Code 或 Cursor 可以提供补全与配置校验。适合直接放行的通常是项目脚本、只读 Git 命令和常规文件操作；破坏性命令、网络下载命令与敏感文件读取应进入 deny。

个人权限调整可以放在 .claude/settings.local.json ，并留在本机。

08

完整目录长什么样

把前面的模块放在一起，项目级和全局级配置大致形成下面的结构：

指令、规则、钩子、流程、角色与权限共同组成项目协作协议。

09

从零开始的落地顺序

1 运行 /init 生成初始 CLAUDE.md，再删减到关键内容。

2 创建 .claude/settings.json，配置适合当前技术栈的 allow 与 deny。

3 把高频工作封装成一两个 Commands 或 Skills，例如代码审查、问题修复。

4 当 CLAUDE.md 变长时，按主题拆进 rules/，需要时增加路径范围。

5 在 ~/.claude/CLAUDE.md 中记录跨项目生效的个人偏好。

对于大多数项目，先完成前两步就能获得明显收益。Skills 与 Agents 适合在重复流程已经稳定、任务确实需要隔离时再逐步增加。

★ 总 结

.claude/ 可以理解为一份项目协作协议：CLAUDE.md 描述项目，rules/ 拆分约束，Hooks 自动执行关键检查，Skills 固化流程，Agents 隔离专门任务，settings.json 划定权限边界。先把 CLAUDE.md 写清楚，再根据真实需求逐步增加其他模块。

从一份短而准确的 CLAUDE.md 开始。

配置会随着项目一起演进。每次增加一条规则，都应对应一个真实发生过的问题或稳定复用的流程。

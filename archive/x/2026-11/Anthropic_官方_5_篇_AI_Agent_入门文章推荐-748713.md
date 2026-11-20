# Anthropic 官方 5 篇 AI Agent 入门文章推荐

- 原文链接：https://x.com/xiaomovps/status/2123605050014748713?a=lsd7Fh2BdjlQTX1Ndtg&s=19
- 作者：小墨同学 @xiaomovps
- 发布时间：2026-11-20
- 剪藏时间：2026-11-21 07:54

---

虽然我很讨厌 Anthropic，但这 5 篇文章真的值得所有 AI 新手阅读

Anthropic 这家公司虽然真的很让人讨厌，要不就是直接给你封号，要不就是直接让你不能使用，但是你不能说他写的内容差

昨天我搜索资料的时候，发现 Anthropic 官网上提供了非常多优秀的文章，尤其是针对 AI 领域的内容都写得比较好，而且最大的优点就是通俗易懂

我从里面选了 5 篇最值得新手阅读的文章，如果你也想学习 AI Agent，可以从这里面开始看

1、Building effective agents｜构建高效的 AI Agent

我最推荐新手阅读的一篇文章，讲清楚了 Agent 和 Workflow 的区别，以及 5 种常见的工作流设计模式，适合刚开始学习 Agent 的人

https://www.anthropic.com/engineering/building-effective-agents

2、Claude Code: Best practices for agentic coding｜AI 编程最佳实践

主要介绍怎么正确使用 Claude Code，包括项目配置、任务规划、工具调用和代码验证，适合想学习 AI Coding 的新手

https://www.anthropic.com/engineering/claude-code-best-practices

3、Equipping agents for the real world with Agent Skills｜Agent Skills 入门

如果你还不理解 Skill 是什么，可以看看这篇，讲清楚了 Skill 的基本结构、SKILL.md 和按需加载机制，以及怎么给 Agent 扩展能力

https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

4、Effective context engineering for AI agents｜Agent 上下文工程

主要讲解上下文管理，为什么上下文不是越长越好，以及怎么通过信息检索、工具管理和上下文压缩，让 Agent 运行得更加稳定

https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

5、How Anthropic teams use Claude Code｜Anthropic 内部 AI 使用案例

这篇更偏向实际应用，分享 Anthropic 内部不同团队怎么使用 Claude Code，包括编程、产品、设计和日常工作，即使没有编程基础也可以参考

https://www.anthropic.com/news/how-anthropic-teams-use-claude-code

最后我想说的是，公司虽然很垃圾，但是内容还是值得看的，取其精华，去其糟粕

尤其是刚开始学习 AI Agent 的新手，我觉得这 5 篇文章已经足够作为一个不错的入门起点了

[图片] [图片]

↳ 引用 @xiaomovps：想了解 Personal Agent，可以从这里开始

我研究和使用过很多 Agent，比如 Hermes Agent、OpenClaw、GrokBot 等

慢慢地，我就在思考一个问题：到底该怎么去构建一个成熟的 Personal Agent？

我总结了一下社区讨论比较多的内容，再结合自己的实际使用体验，把它分成了三个方向

1、实际使用场景和自动化能力

Personal Agent 到底能帮我们做什么？除了日常聊天、写代码，能不能真正接管一些重复性的工作，比如信息收集、任务调度、自动化执行等

2、长期记忆和个性化能力

这是我觉得 Personal Agent 和普通 AI 聊天工具最大的区别之一，能不能长期记住你的使用习惯、项目背景和个人需求，并且在不同任务中正确调用这些记忆

3、长期运行的稳定性、成本和安全

这一点也是实际使用过程中最容易遇到问题的地方，比如长任务中断、Token 消耗过高、执行过程没有反馈，以及工具调用的权限和安全问题

根据这三个方向，其实就可以慢慢推导出，一个成熟的 Personal Agent 应该由哪些核心能力构成，哪一部分需要优先保证稳定性，哪一部分还需要持续优化

有了这些基础认识之后，我们就可以去接触一些开源项目，结合自己的实际需求，慢慢 DIY 出一个真正适合自己的 Personal Agent，而不是单纯地安装一个项目就结束了

如果你也对 Personal Agent 感兴趣，我推荐先看 Anthropic 的这篇文章：

Building Effective Agents

https://www.anthropic.com/research/building-effective-agents

这是我比较推荐的一篇入门文章，它讲清楚了 Agent、Workflow、工具调用之间的区别，同时强调了一个很重要的原则：

尽可能从简单的方案开始，能用单一 Agent 或固定工作流解决的问题，就没必要一开始就设计复杂的多 Agent 系统

我觉得先理解这些基础概念，再去研究不同的开源项目，会比一上来就安装各种插件和 Skills 更有帮助

# 分享5个小众但非常实用的Claude Code斜杠命令

- 原文链接：https://mp.weixin.qq.com/s/bx0Z7egWCvnjEkRn0UdtQQ
- 公众号：AI编程实验室
- 发布时间：2026-08-19
- 剪藏时间：2026-08-23 17:07

---

大家好，我是鲁工。

斜杠命令（slash command）一直是Claude Code日常使用最高频的功能操作。比如用/model切换模型、/usage查看用量、/context查看上下文、/mcp查看MCP配置、/skills查看已安装的skills列表等。

[图片]

随着Claude Code频繁更新，不断引入新的斜杠命令功能，以及大量Skills也通过斜杠命令来调用，这使得Claude Code斜杠命令越来越多。

今天我想分享几个日常相对小众、但功能却又非常实用的五个官方斜杠命令给大家。

分别是： /subtask 、 /insights 、 /artifact-design 、 /dataviz 、 /design 。

对这五个命令先分个类：/subtask和/insights是功能命令，一个用于分派任务，一个是根据你日常使用Claude Code的数据进行体检；而 /artifact-design、 /dataviz、/design本质上是系统内置的skill，分别用于数据可视化、工件交付和日常设计。

1. /insights：给你的Claude Code用法做一次体检

用法直接输入/insights，不带参数。它分析你这台机器上的近期会话，产出一份HTML报告：在哪些项目上干活、哪里出了问题、还有什么功能值得一试。官方文档特意拿它跟/usage对照，/usage看的是日常用量和配额，/insights则是研究你使用Claude Code的方式并提出改进建议。

[图片]

几个要点：单次最多分析200个新会话，太短的会直接跳过；会话体检报告保存到~/.claude/usage-data/report.html，每次另存带时间戳副本；只能用于本地会话诊断。

我用/insights分析了我近一个月的Claude Code会话数据，给了一份完整详实的Claude Code用法体检报告，包括好的方面、存在的问题、立刻可以改善的解决方案、以及未来更高效的工作方式。

[图片]

这个建议每个Claude Code用户都试一下，对于改进日常使用方式和习惯非常有帮助，让Claude Code更高效的服务于我们日常工作。

2. /subtask：分派Subagent，仅交付结果

五个里面我认为最实用的一个。用法也很直接：

官方对这个功能的描述是：Send a subagent off with your full context; its result comes back here。带着完整上下文派出一个subagent，返回结果回到当前会话。非常符合subagent的特性。

重点有两个。一是完整上下文：普通的subagent是一张白纸，背景要在任务描述里全部交代一遍，而/subtask派出去的subagent继承当前会话的全部对话历史，任务描述一句话即可。二是只有结果回来：子代理在后台跑，读的几十个文件都留在它自己的上下文里，回到主会话的只有任务完成后的结论。

前几天读Anthropic讲会话成本的那篇技术博客，里面反复强调不要让一次性的探索任务混淆主会话上下文，/subtask等于把这条最佳实践做成了命令。比如我在做一个MICCAI竞赛，主会话正在做推理评测，然后我想让Claude同步看一下竞赛官网和论坛有没有什么更新，那么就可以直接使用subtask把这个活派出去，把结果返回来就行。

[图片]

/subtask跟/fork有点像，/fork是把当前会话复制成一个新的后台会话。区别在于/subtask的结果会回流主会话，/fork复制出去就各走各路了，想顺手查个事用/subtask，想另外开辟一条任务路线换方案执行用/fork。

3. /artifact-design：工件设计与交付

从 /artifact-design 开始都是skill类的斜杠命令。 我之前专门写过，具体可参考：

Claude Code artifacts，随时交付和分享效果页面

这个也是我日常非常喜欢用的一个命令，在做一些论文调研、方案设计或者项目完成后的总结，用这个会非常丝滑。

artifacts可以直接理解为交付物或者工件，就是Claude Code把会话里的工作成果发布成claude.ai上的一个网页，有独立URL，默认私有，而且是一直可访问的，并且不会影响会话本身继续干活，页面也会随时更新。我们日常生成的artifacts，可以统一用/artifacts命令来查看和管理。

[图片]

/artifact-design还有一个点值得提一下，是一段AI设计俗套清单，点名了当前AI做设计最喜欢用的模板：米色底（原文精确到色号 #F4F1EA ）配衬线大标题和赤陶色点缀、近黑背景配一个荧光绿高亮、紫蓝渐变的首屏大图、Inter或Space Grotesk当保险字体、emoji当小节标记、所有东西居中、圆角卡片等。并明确要求：用户没指定风格时，禁用这些AI味的设计和配色。

4. /dataviz：基于设计的数据可视化

/dataviz的定位是图表和仪表盘设计指南，使用时会自动触发/artifact-design来进行设计，最终的交付物也是artifacts形式。

/dataviz的覆盖面很广，官方定义明确写了任何介质：HTML图表、inline SVG、matplotlib、plotly、d3的绘图代码，甚至要渲染成PNG发出去的图，都可以做。

我做了个实测，让它用kaggle上科比职业生涯投篮数据集，做一份数据可视化报告。

分析得非常漂亮，你们感受一下效果。

[图片]

还可以按照科比职业生涯不同赛季查看，一些经典的投篮我甚至都可以找到当年的比赛场次和视频。比如2009-2010常规赛科比第四节绝杀国王队队一个边线三分球：

[图片]

当时这一球的投篮照片：

[图片]

5. /design：在Claude Code里直接出设计稿

/design算是五个里最厚重的一个，是Claude Design（claude.ai/design在Claude Code里的早期预览。关于Claude Design，我之前也专门写过，具体可参考：

Claude Design发布后，留给AI设计厂商的时间不多了

这个没啥好说的，就是把Claude Design直接跟Claude Code打通，通过/design即可调用Claude Design的强大专业设计能力。

简单总结一下就是：/subtask值得日常高频用，/dataviz、/artifact-design、/degisn都是跟设计相关的工具，/dataviz侧重于数据可视化，/artifact-design聚焦前端工件交付，/degisn则是直接调用Claude Design的专业设计能力。/insights可以每个月跑一次，就当给自己的Claude Code用法做个体检，不断改进用法。

如果觉得有用，点个赞或者在看，也方便更多朋友看到。

感谢您阅读我的文章。我是鲁工，九年AI算法老兵，AI全栈开发者，深耕AI编程赛道与AI科研赛道。

>/ 作者：鲁工

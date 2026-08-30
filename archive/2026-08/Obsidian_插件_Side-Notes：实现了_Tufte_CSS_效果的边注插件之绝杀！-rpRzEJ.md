# Obsidian 插件 Side-Notes：实现了 Tufte CSS 效果的边注插件之绝杀！

- 原文链接：https://mp.weixin.qq.com/s/rpRzEJ2AQrBq2FXZTO5boQ
- 公众号：PKMer 知识社区
- 发布时间：2026-08-29
- 剪藏时间：2026-08-30 08:53

---

[图片]

由于微信限制， 公众号文章内无法添加可跳转的外部链接 ，如果想要了解文内提到的更多信息，请点击文末的 阅读原文 ，查看本期内容

[图片]

PKMer

[图片]

插件名片

插件名称 ：Side-Notes

插件作者 ：Fried Fishsticks

插件版本 ：0.5.0（2026 年 1 月 30 日首发，截止至 2026 年 8 月 20 日，共发 39 版）

插件概述 ： Side-Notes 插件受到设计界大神 Edward Tufte 的 CSS 的启发，有效利用了横屏两侧的空白部分实现了类实体图书的边注效果，边注在编辑器内会随着相关正文滚动，且可通过 Obsidian 原生脚注语法实现，有效避免了 html 语法对文本的污染

插件项目地址： https://github.com/cparsell/sidenotes

国内下载地址： https://pkmer.cn/products/plugin/pluginMarket/?

术语解说

Side-Notes插件受到了 Sidenotes In Web Design 一文中 关于 Tufte CSS 的启发，笔者几年前发现了这篇文章，然而由于自己是计算机小白无法实现，曾经有一个 CSS 在一定程度上实现了这一效果， 笔者也曾撰文介绍 ，但终究与我的期待有所出入，这次发现这个插件非常高兴，再次推荐对出版或排版感兴趣的网友都去阅读 Sidenotes In Web Design 一文

插件跟 Tufte CSS 一样，对 sidenote 和 margin note 进行了区分，前者为自动带有连续编码的边注，后者为不带连续编码的边注，详见 此文

如图所示，边注可显示在正文的两侧，在实时预览模式下可直接在边注位置修改文本，支持 加粗 、斜体、 行内代码 和内外部链接语法

[图片]

如在 Obsidian 设置→编辑器→显示中启用 限制行宽 选项，则在阅读模式下插件的显示效果很差

基本用法

如何添加 sidenote ？

在插件设置→ Sidenote format 中选择在正文中批注要以 html 还是脚注的语法添加，前者更适合需要网页发布的情况， 后者为 Obsidian 原生语法，对文本的污染更小

如选择 html，则语法为被标注文本 <span class="sidenote">标注文本</span> ，在想要标注的文本后执行命令面板中的 Side-notes: Insert sidenote 命令

如选择脚注，则语法为 被标注文本[^1] ，既可执行以上命令，也可在命令面板中直接执行系统自带的 插入脚注 命令

也可手写语法，就是比较麻烦且容易出错

如果想将边注添加于插件设置默认位置的对侧，语法为 <span class="sidenote right">text</span> （左侧加 left ）或 被标注文本[^1-l] （右侧加 -r ）或在命令面板中执行 Side-notes: Insert sidenote (opposite margin) 命令

如何添加 margin note ？

如选择 html，则语法为 <span class="sidenote margin-note"> 在想要标注的文本后执行命令面板中的 Side-notes: Insert margin note 命令

如选择脚注，则语法为 [^mn-1] 或 [^mn-kitchen] ，既可执行以上命令，也可在命令面板中直接执行系统自带的 插入脚注 命令

如果想将边注添加于插件设置默认位置的对侧，写法同 sidenote，或在命令面板中执行 Side-notes: Insert margin note (opposite margin) 命令

插件作者使用 Digital-Garden 发布它的笔记，在 Obsidian 库下的 /digital-garden/custom-styles.css 文件似乎可以用来为其实现相同的边注效果（笔者未验证）

设置说明

Sidenote format

Sidenote format ：在下拉菜单中选择在正文中批注要以 html 还是脚注的语法添加

If using footnotes

Hide footnotes ：如启用，则在正文末尾不显示脚注内容

Hide footnote numbers in text ：如启用，则在正文中不显示传统脚注序号[^数字]

Display

Sidenote position ：在下拉菜单中选择边注是显示在正文的左边还是右边

Show sidenote numbers ：如启用，则边注和正文中都会显示批注编码

Number style ：在下拉菜单中选择编码的格式（数字、罗马数字、英文字母）

Number badge style ：在下拉菜单中选择编码的样式

Number color ：在空白栏中填入编码的颜色，留空则为主题默认

Width & Spacing

Sidenote anchor ：在下拉菜单中选择边注是靠近文本还是编辑器边缘

Minimum/Maximum sidenote width ：在拖动条中选择边注的最小/最大宽度

Minimum gap between sidenote and text ：在拖动条中选择边注与正文的最小间隔

Minimum gap between sidenote and editor edge ：在拖动条中选择边注与编辑器边缘的最小间隔

Gap drift factor ：在拖动条中选择间隔随编辑器的宽度变化的变化比率

Breakpoints

Hide below width ：在空白栏中填入一个数，如果边注的宽度小于此数，则隐藏边注（单位：像素）

Compact below width ：在空白栏中填入一个数，如果边注的宽度小于此数，则使用紧凑排版（单位：像素）

Full width above ：在空白栏中填入一个数，如果边注的宽度大于此数，则显示完全宽度（单位：像素）

Typography

Font size ：在拖动条中选择字体的尺寸百分比

Font size (compact mode) ：在拖动条中选择字体在紧凑排版下的尺寸百分比

Lineheight ：在拖动条中选择行高

Sidenote text color ：在空白栏中填入边注内容的字体颜色

Sidenote hover color ：在空白栏中填入悬浮窗中边注内容的字体颜色

Text alignment ：选择边注内容的对齐方式

Behavior

Collision spacing ：在拖动条中选择相邻边注之间的最小间距（单位：像素）

Enable smooth transitions ：

Reset numberings per heading ：如启用，则每过一个小标题，边注自动重新编号

Include sidenotes in PDF export ：如启用，则在导出 PDF 时，保持边注排版导出

Margin note

Margin note display ：在下拉菜单中选择是显示margin note还是仅在正文中显示一个标注符号，鼠标点击后方显示批注内容

Margin note popover icon ：如在上一选项中选择仅在正文中显示标注符号，则在此选项空白栏中填入的 Unicode 字符将被视为该标注符号

- THE END -

// 长按二维码·加入我们

[图片]

QQ群

[图片]

微信群

[图片]

作者 ：血海狂屠

来源 ：PKMer

排版 ：Wis_Ocean

[图片]

点击阅读原文查看更多

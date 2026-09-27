# AI阅读书籍：逐页PDF知识提取器和摘要器

- 原文链接：https://mp.weixin.qq.com/s/Kcu-kUXPbg-EqwpbbcsanQ
- 公众号：ITBOX
- 发布时间：2026-09-18
- 剪藏时间：2026-09-27 17:02

---

这个项目把「AI 读书」拆成了最朴素的一步

前阵子我推荐过几个本地 RAG 工具，比如 GoldPan、AnythingLLM，能力都很全。但每次介绍完，总有人问：「我就是想读一本书留个笔记，有没有更轻的？」

还真有。

今天翻到一个仓库叫 AI reads books: Page-by-Page PDF Knowledge Extractor & Summarizer ，作者 echohive42。它的思路极简：单脚本、4 个依赖、零向量、零前端。用 PyMuPDF 把 PDF 一页一页拆出来，每页调一次 OpenAI 兼容接口提取「知识点」，累加到一个 JSON 知识库；跑完 N 页生成一次阶段总结，跑完整本再来一份全本总结。

这个思路其实绕过了「AI 读 PDF」的两种主流路线：

• 第一种——把整本 PDF 一次性塞给 LLM。优点是上下文连贯；缺点是超过几十页就爆。

• 第二种——上 RAG（向量库 + 检索）。优点是可跨文档；缺点是搭环境就得半天。

这个项目走的是第三条路：逐页提取 + 累加知识库 + 阶段性总结。它没想做跨文档问答，也没打算读一次性上下文，就只做一件事——把一本书读成结构化笔记。

[图片]

它到底能跑出什么东西

跑通之后你会拿到三个目录的产物：

• book_analysis/knowledge_bases/ ：JSON 知识库，记录每页提取的知识点

• book_analysis/summaries/ ：阶段总结 + 最终总结（Markdown 格式）

• book_analysis/pdfs/ ：原 PDF 副本

我比较喜欢的是「每页保存一次 JSON」这个细节。这意味着你跑到第 137 页 API 突然限流了，重启脚本时它会自动从第 138 页接着跑， 前面的 137 页知识点都还在 JSON 里 。这种断点续传能力，很多类似的脚本都没有。

四个依赖，单文件跑通

requirements.txt 只有四行：

• pymupdf ：PDF 拆页 + 文本提取（速度比 pdfplumber 快一档）

• openai ：OpenAI 兼容客户端——注意「兼容」两个字，你可以改 base_url 指向 Ollama、LM Studio 或者任何兼容服务

• pydantic ：结构化输出校验，强制 LLM 按 PageContent 模型（ has_content: bool + knowledge: list[str] ）返回

• termcolor ：终端进度条上色

整个项目就一个 read_books.py 文件，加上两个示例 PDF（ infinite_math.pdf 和 meditations.pdf ）。零前端、零数据库、零向量库——这点对学 LLM 应用的人特别友好，因为它强迫你只关注「怎么把 LLM 用好」这一件事。

十分钟跑通的体感

然后用编辑器打开 read_books.py ，改一行：

跑 python read_books.py ，终端会用绿字告诉你跑到第几页、提取了几条知识点、阶段总结生成成功。

我推荐第一次跑的时候设 TEST_PAGES = 5 ，先验证流程通；确认没问题再设回 None 跑全本。

跟同类项目的区别

我把这阵子用过的「AI 读 PDF」工具列了一下：

工具

这个项目的区别

AI reads books（这个）

单脚本 + 4 依赖 + 零向量 + 零前端；面向「自己改代码」的人

NotebookLM

Google 官方、云端、闭源、不能装本地

Humata

商业 SaaS、订阅制、按页收费

ChatPDF

在线服务、闭源

GoldPan

全家桶 RAG 工作台：向量库 + 多模态 + 双写 Markdown；复杂度高一档

Marker / Nougat

更专业的 PDF → Markdown 转换器，适合做学术 PDF 的预处理

自建 LangChain + FAISS

自由度高，但所有 UI/并发/存储都得自己写

一句话概括：它是「想 DIY 一个 AI 读 PDF 脚本」的最小可行版本，定位给愿意自己改代码的工程师。

要不要现在就试

如果你符合下面任一情况：

• 想学「LLM + 结构化输出 + 持久化」的最小工程范本

• 只想读一本书留个总结，不想搞向量库和前端

• 想拿一个能跑通的脚本当骨架，自己加功能

那这个项目值得 clone 下来玩一遍。代码量小、依赖轻、好读、好改，正好适合拆开学。

但如果你的需求是「跨文档问答」或者「企业内部知识库」，建议直接看 GoldPan 或 AnythingLLM——这个脚本就干一件事，干得干净，但不打算扩展成全家桶。

最后小总结一下：这个项目解决的是「我只想读完一本书留个结构化笔记」这种具体场景。RAG 太重、整本塞不下，它正好卡在中间。

[图片]

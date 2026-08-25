# Notes

剪藏助手:抓取**微信公众号文章**与 **X(原推特)帖子**正文,AI 生成摘要 / 关键词 / 洞见 / 优先级,写入 Notion,并在本仓库归档 Markdown 快照。详见 [`README.md`](README.md)。

两条链路共用一条流水线,按链接域名自动分流(`pipeline.clip()`),只有抓取器、AI 提示词补充段落、归档目录和 Notion 数据库是分开的。

## 仓库结构

| 路径 | 内容 |
|---|---|
| `notes/YYYY-MM.md` | 公众号月度索引,按剪藏时间分组,最新的在最上面 |
| `archive/YYYY-MM/*.md` | 每篇公众号文章的全文快照 |
| `notes/x/YYYY-MM.md` | X 帖子月度索引,格式同上 |
| `archive/x/YYYY-MM/*.md` | 每条 X 帖子的全文快照 |
| `data/index.json` | 剪藏索引,用于查重 |
| `src/clipper/` | 处理流水线源码 |
| `tests/` | 单元测试 |
| `docs/superpowers/specs/` | 设计文档 |
| `.github/workflows/` | GitHub Actions(`clip.yml` 剪藏流水线,`test.yml` 测试) |

## Python 开发环境

各子项目使用 Python 开发,且彼此独立。进入某个子文件夹开始工作时:

- 若该目录下有 `requirements.txt` / `pyproject.toml`,先为该子项目创建独立虚拟环境(优先用 `uv venv`,没有 `uv` 则用 `python3 -m venv`),再在该虚拟环境里安装依赖。
- 不要在仓库根目录或跨子项目共用虚拟环境,避免依赖互相污染。

## 提交与推送

- 完成一次改动后(而不是每改一行就提交),及时 `commit` + `push`,避免云端 VM 回收后未提交的改动丢失。
- commit message 用中文。
- push 到当前工作分支,不要直接推送到默认分支 `master`(修改仓库级配置文件如本文件除外,需用户明确要求)。

## 分支

默认分支是 `master`(没有 `main`)。

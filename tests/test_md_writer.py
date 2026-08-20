import os
from datetime import datetime

from clipper import md_writer
from clipper.models import Entry
from clipper.pipeline import CST


def test_首次写入创建月份标题(entry, tmp_path):
    md_writer.write(entry, str(tmp_path))
    content = (tmp_path / "notes" / "2026-08.md").read_text(encoding="utf-8")
    assert content.startswith("# 2026年08月")
    assert "## 为什么大模型的上下文窗口越来越长" in content


def test_新条目插入到标题正下方且旧内容保留(entry, tmp_path, article, digest):
    md_writer.write(entry, str(tmp_path))

    newer = Entry(
        article=type(article)(
            url="https://mp.weixin.qq.com/s/NewOne",
            title="更新的一篇",
            content="正文",
        ),
        digest=digest,
        clipped_at=datetime(2026, 8, 21, 9, 0, tzinfo=CST),
    )
    md_writer.write(newer, str(tmp_path))

    content = (tmp_path / "notes" / "2026-08.md").read_text(encoding="utf-8")
    lines = content.splitlines()
    assert lines[0] == "# 2026年08月"
    assert content.index("## 更新的一篇") < content.index("## 为什么大模型的上下文窗口越来越长")


def test_写入全文快照(entry, tmp_path):
    _, snapshot = md_writer.write(entry, str(tmp_path))
    path = tmp_path / snapshot
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "第一段正文。" in text
    assert "机器之心" in text


def test_条目包含全部字段(entry):
    rendered = md_writer.render_entry(entry)
    assert "**剪藏**：2026-08-20 19:44" in rendered
    assert "**发布**：2026-08-18" in rendered
    assert "**优先级**：高" in rendered
    assert "**状态**：未读" in rendered
    assert "长上下文 / 注意力机制" in rendered
    assert "- **洞见**：" in rendered
    assert "[原文](https://mp.weixin.qq.com/s/AbCdEf123)" in rendered


def test_缺少发布时间时显示未知(entry):
    entry.article.published_at = None
    assert "**发布**：未知" in md_writer.render_entry(entry)

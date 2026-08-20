"""写 GitHub 归档：月度索引 notes/YYYY-MM.md 与全文快照 archive/YYYY-MM/*.md。"""

from __future__ import annotations

import os

from .models import Entry


def write(entry: Entry, repo_dir: str = ".") -> tuple[str, str]:
    """写入快照与索引，返回 (索引路径, 快照路径)。"""
    snapshot_path = _write_snapshot(entry, repo_dir)
    notes_path = _prepend_to_month_file(entry, repo_dir)
    return notes_path, snapshot_path


def render_entry(entry: Entry) -> str:
    """渲染月度索引里的单条记录。"""
    article, digest = entry.article, entry.digest
    published = article.published_at or "未知"
    keywords = " / ".join(digest.keywords) if digest.keywords else "无"

    lines = [
        f"## {entry.title}",
        f"- **剪藏**：{entry.clipped_at.strftime('%Y-%m-%d %H:%M')} ｜ **发布**：{published}",
        f"- **优先级**：{digest.priority} ｜ **状态**：未读",
        f"- **关键词**：{keywords}",
        f"- **摘要**：{digest.summary}",
    ]

    if digest.insights:
        lines.append("- **洞见**：")
        lines.extend(f"  - {insight}" for insight in digest.insights)
    if digest.priority_reason:
        lines.append(f"- **是否值得读**：{digest.priority_reason}")

    relative_snapshot = f"../{entry.snapshot_path}"
    lines.append(
        f"- **链接**：[原文]({article.url}) ｜ [全文快照]({relative_snapshot})"
    )
    return "\n".join(lines) + "\n"


def render_snapshot(entry: Entry) -> str:
    """渲染全文快照文件。"""
    article = entry.article
    header = [
        f"# {entry.title}",
        "",
        f"- 原文链接：{article.url}",
        f"- 发布时间：{article.published_at or '未知'}",
        f"- 剪藏时间：{entry.clipped_at.strftime('%Y-%m-%d %H:%M')}",
    ]
    if article.account:
        header.insert(3, f"- 公众号：{article.account}")
    header += ["", "---", "", article.content, ""]
    return "\n".join(header)


def _write_snapshot(entry: Entry, repo_dir: str) -> str:
    path = os.path.join(repo_dir, entry.snapshot_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(render_snapshot(entry))
    return entry.snapshot_path


def _prepend_to_month_file(entry: Entry, repo_dir: str) -> str:
    """把新条目插入到当月标题正下方，保证最新的在最上面。"""
    path = os.path.join(repo_dir, entry.notes_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    heading = f"# {entry.month_heading}"
    block = render_entry(entry)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(f"{heading}\n\n{block}")
        return entry.notes_path

    with open(path, encoding="utf-8") as fh:
        existing = fh.read()

    if existing.lstrip().startswith(heading):
        head, _, rest = existing.partition("\n")
        updated = f"{head}\n\n{block}\n{rest.lstrip(chr(10))}"
    else:
        # 文件存在但没有月份标题（异常情况），补一个标题再插入
        updated = f"{heading}\n\n{block}\n{existing}"

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(updated)
    return entry.notes_path

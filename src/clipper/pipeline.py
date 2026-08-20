"""编排单篇文章的完整处理流程。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from . import ai, fetcher, md_writer
from .config import Config
from .models import Entry
from .store import Store

CST = timezone(timedelta(hours=8))


@dataclass
class Result:
    url: str
    status: str  # created / duplicate / failed
    title: str = ""
    message: str = ""
    notion_page_id: Optional[str] = None


def clip(
    url: str,
    config: Config,
    store: Store,
    clipped_at: Optional[datetime] = None,
    dry_run: bool = False,
) -> Result:
    """处理一条链接：查重 → 抓取 → AI → Notion → md → 记账。"""
    url = url.strip()
    if not url:
        return Result(url=url, status="failed", message="空链接")

    if store.is_duplicate(url):
        existing = store.get(url) or {}
        return Result(
            url=url,
            status="duplicate",
            title=existing.get("title", ""),
            message="已剪藏过，跳过",
        )

    try:
        article = fetcher.fetch(url, timeout=config.request_timeout)
    except Exception as exc:  # noqa: BLE001 - 统一上报抓取失败
        return Result(url=url, status="failed", message=f"抓取失败：{exc}")

    digest = ai.digest(article, config)
    if not article.title and digest.title:
        article.title = digest.title

    entry = Entry(article=article, digest=digest, clipped_at=clipped_at or datetime.now(CST))

    if dry_run:
        return Result(
            url=url,
            status="created",
            title=entry.title,
            message=f"dry-run：优先级 {digest.priority}，正文 {len(article.content)} 字",
        )

    notion_page_id = None
    notion_error = ""
    if config.notion_enabled:
        try:
            from .notion_writer import NotionWriter

            notion_page_id = NotionWriter(config).create_page(entry)
        except Exception as exc:  # noqa: BLE001 - Notion 失败不阻断 md 写入
            notion_error = f"（Notion 写入失败：{exc}）"

    notes_path, snapshot_path = md_writer.write(entry, config.repo_dir)
    store.add(entry, notion_page_id)

    message = f"已写入 {notes_path} 与 {snapshot_path}{notion_error}"
    if digest.failed:
        message += "（AI 降级处理）"
    return Result(
        url=url,
        status="created",
        title=entry.title,
        message=message,
        notion_page_id=notion_page_id,
    )

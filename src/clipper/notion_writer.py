"""写 Notion 数据库：一篇文章一页，属性放结构化信息，页面正文放全文快照。"""

from __future__ import annotations

from typing import List, Optional

import requests

from .config import Config
from .models import Entry

API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

TEXT_LIMIT = 2000    # 单个 rich_text 上限
BLOCK_LIMIT = 100    # 单次 children 追加上限

# 数据库属性定义，init_database 与写入共用同一套名称
PROPERTIES = {
    "标题": {"title": {}},
    "链接": {"url": {}},
    "剪藏时间": {"date": {}},
    "发布时间": {"date": {}},
    "摘要": {"rich_text": {}},
    "关键词": {"multi_select": {}},
    "洞见": {"rich_text": {}},
    "AI优先级": {
        "select": {
            "options": [
                {"name": "高", "color": "red"},
                {"name": "中", "color": "yellow"},
                {"name": "低", "color": "gray"},
            ]
        }
    },
    "优先级理由": {"rich_text": {}},
    "阅读状态": {
        "select": {
            "options": [
                {"name": "未读", "color": "blue"},
                {"name": "在读", "color": "orange"},
                {"name": "已读", "color": "green"},
                {"name": "已放弃", "color": "gray"},
            ]
        }
    },
}


class NotionError(RuntimeError):
    """Notion API 调用失败。"""


class NotionWriter:
    def __init__(self, config: Config):
        if not config.notion_token:
            raise NotionError("未配置 NOTION_TOKEN")
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {config.notion_token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def create_page(self, entry: Entry) -> str:
        """建页并写入全文快照，返回 page id。"""
        blocks = build_blocks(entry)
        payload = {
            "parent": {"database_id": self.config.database_id_for(entry.article.source)},
            "properties": build_properties(entry),
            "children": blocks[:BLOCK_LIMIT],
        }
        page = self._request("POST", "/pages", payload)
        page_id = page["id"]

        for chunk in _chunks(blocks[BLOCK_LIMIT:], BLOCK_LIMIT):
            self._request("PATCH", f"/blocks/{page_id}/children", {"children": chunk})
        return page_id

    def init_database(self, parent_page_id: str, title: str = "公众号剪藏") -> str:
        """在指定父页面下创建带全部属性的数据库，返回 database id。"""
        payload = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": PROPERTIES,
        }
        return self._request("POST", "/databases", payload)["id"]

    def _request(self, method: str, path: str, payload: dict) -> dict:
        response = requests.request(
            method,
            f"{API}{path}",
            headers=self.headers,
            json=payload,
            timeout=self.config.request_timeout,
        )
        if response.status_code >= 400:
            raise NotionError(f"{method} {path} 失败 {response.status_code}：{response.text[:300]}")
        return response.json()


def build_properties(entry: Entry) -> dict:
    digest = entry.digest
    properties = {
        "标题": {"title": [{"text": {"content": entry.title[:200]}}]},
        "链接": {"url": entry.article.url},
        "剪藏时间": {"date": {"start": entry.clipped_at.isoformat()}},
        "摘要": {"rich_text": _rich_text(digest.summary)},
        "关键词": {"multi_select": [{"name": k[:100]} for k in digest.keywords]},
        "洞见": {"rich_text": _rich_text("\n".join(f"· {i}" for i in digest.insights))},
        "AI优先级": {"select": {"name": digest.priority}},
        "优先级理由": {"rich_text": _rich_text(digest.priority_reason)},
        "阅读状态": {"select": {"name": "未读"}},
    }
    if entry.article.published_at:
        properties["发布时间"] = {"date": {"start": entry.article.published_at}}
    return properties


def build_blocks(entry: Entry) -> List[dict]:
    """全文快照转成 Notion 段落块，超长段落自动切分。"""
    blocks: List[dict] = []
    for paragraph in entry.article.content.split("\n\n"):
        text = paragraph.strip()
        if not text:
            continue
        for piece in _split_text(text, TEXT_LIMIT):
            blocks.append(
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": piece}}]},
                }
            )
    return blocks


def _rich_text(content: Optional[str]) -> List[dict]:
    if not content:
        return []
    return [{"type": "text", "text": {"content": piece}} for piece in _split_text(content, TEXT_LIMIT)]


def _split_text(text: str, limit: int) -> List[str]:
    return [text[i : i + limit] for i in range(0, len(text), limit)] or [""]


def _chunks(items: List[dict], size: int):
    for i in range(0, len(items), size):
        yield items[i : i + size]

"""核心数据模型：抓取结果、AI 消化结果、落库条目。"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from urllib.parse import parse_qs, urlparse

# 文件名中的非法字符
_ILLEGAL_CHARS = re.compile(r'[\/:*?"<>|\r\n\t]+')

# X 的域名，含 www. / mobile. 等前缀
_X_HOST = re.compile(r"(^|\.)(x|twitter)\.com$", re.I)


@dataclass
class Article:
    """从公众号页面抓取到的原始内容。"""

    url: str
    title: str
    content: str
    published_at: Optional[str] = None  # YYYY-MM-DD
    account: Optional[str] = None       # 公众号名 / X 作者，抓到就留档
    source: str = "weixin"              # weixin / x，决定归档目录与 Notion 库


@dataclass
class Digest:
    """AI 消化后的结构化信息。"""

    summary: str
    keywords: List[str] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)
    priority: str = "中"
    priority_reason: str = ""
    title: Optional[str] = None  # 抓取失败时由 AI 推断的标题
    failed: bool = False         # AI 环节降级标记


@dataclass
class Entry:
    """一次剪藏的完整记录，是写 Notion 与写 md 的唯一输入。"""

    article: Article
    digest: Digest
    clipped_at: datetime

    @property
    def title(self) -> str:
        return self.article.title or self.digest.title or "无标题"

    @property
    def month(self) -> str:
        """归档月份，按剪藏时间。"""
        return self.clipped_at.strftime("%Y-%m")

    @property
    def month_heading(self) -> str:
        return self.clipped_at.strftime("%Y年%m月")

    @property
    def fingerprint(self) -> str:
        return fingerprint(self.article.url)

    @property
    def slug(self) -> str:
        """快照文件名：清洗标题 + 6 位指纹，避免重名与非法字符。

        推文 ID 是雪花号，同一时期的前缀完全相同，所以 X 取尾 6 位才有区分度。
        """
        clean = _ILLEGAL_CHARS.sub("", self.title).strip().replace(" ", "_")
        mark = self.fingerprint[-6:] if self.article.source == "x" else self.fingerprint[:6]
        return f"{clean[:60] or 'untitled'}-{mark}"

    @property
    def path_prefix(self) -> str:
        """X 帖子归档到独立子目录：短帖量大，混进文章索引会把文章淹掉。"""
        return "x/" if self.article.source == "x" else ""

    @property
    def snapshot_path(self) -> str:
        return f"archive/{self.path_prefix}{self.month}/{self.slug}.md"

    @property
    def notes_path(self) -> str:
        return f"notes/{self.path_prefix}{self.month}.md"


def fingerprint(url: str) -> str:
    """生成稳定的文章指纹，用于查重。

    公众号：优先取短链的 ``/s/<id>``；其次取 query 中的 ``sn``（文章唯一标识）。
    X：取 ``/status/<id>``，这样 x.com 与 twitter.com、大小写不同的用户名指向同一条。
    都取不到时回退为去掉 query 后整串的 sha1。
    """
    parsed = urlparse(url)
    match = re.match(r"^/s/([A-Za-z0-9_\-]+)", parsed.path)
    if match:
        return match.group(1)

    if _X_HOST.search(parsed.netloc):
        match = re.search(r"/status/(\d+)", parsed.path)
        if match:
            return f"x-{match.group(1)}"

    query = parse_qs(parsed.query)
    if query.get("sn"):
        return query["sn"][0]
    if query.get("mid") and query.get("idx"):
        return f"{query['mid'][0]}-{query['idx'][0]}"

    base = f"{parsed.netloc}{parsed.path}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()

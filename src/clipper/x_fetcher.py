"""抓取 X（原推特）帖子。

两个免鉴权接口，**镜像优先**：实测官方嵌入接口把长推文截断在 280 字符
（且不给 note_tweet 补），长文只给标题和一小段预览，正文只有镜像拿得到。
官方接口降为兜底，镜像挂掉时至少还有短帖全文、长文标题与预览。

接口响应结构变化时只需要改这一个文件，测试有 JSON fixture 兜底。
"""

from __future__ import annotations

import math
import re
import time
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import requests

from .fetcher import FetchError
from .models import Article

MIRROR = "https://api.fxtwitter.com/i/status/{post_id}"
# ponytail: 官方接口的正文残缺，只当兜底用；哪天它肯给全文了，就把它调回第一顺位
SYNDICATION = "https://cdn.syndication.twimg.com/tweet-result"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

_URL = re.compile(r"^https?://(?:[\w-]+\.)*(?:x|twitter)\.com/[^/]+/status/(\d+)", re.I)
_BARE_TCO = re.compile(r"\s*https?://t\.co/\w+")
_CST = timezone(timedelta(hours=8))


def is_x_url(url: str) -> bool:
    return bool(_URL.match(url.strip()))


def tweet_id(url: str) -> Optional[str]:
    match = _URL.match(url.strip())
    return match.group(1) if match else None


def fetch(url: str, timeout: int = 30, retries: int = 3) -> Article:
    """先试镜像（正文最全），失败再试官方接口；两条路都不通才算抓取失败。"""
    post_id = tweet_id(url)
    if not post_id:
        raise FetchError(f"不是 X 帖子链接：{url}")

    errors: List[str] = []
    targets = (
        (MIRROR.format(post_id=post_id), parse_mirror),
        (f"{SYNDICATION}?id={post_id}&lang=zh-cn&token={_token(post_id)}", parse),
    )
    for target, parser in targets:
        try:
            return parser(_get_json(target, timeout, retries), url)
        except Exception as exc:  # noqa: BLE001 - 记下原因，换下一条路
            errors.append(str(exc))
    raise FetchError(f"两个接口都没拿到内容：{url}（{'；'.join(errors)}）")


def parse(data: dict, url: str) -> Article:
    """解析官方嵌入接口的响应。"""
    if data.get("__typename") in ("TweetTombstone", "TweetUnavailable"):
        raise FetchError(f"帖子已删除或不可见：{url}")

    # 长文的正文这个接口给不了，只能退到预览；长推文拿到的也只有前 280 字符
    article = data.get("article") or {}
    text = str(article.get("preview_text") or "").strip() if article else _clean(data)
    if not text:
        raise FetchError(f"帖子正文为空：{url}")

    sections = []
    parent = data.get("parent")
    if parent:
        sections.append(f"↰ 回复 @{_handle(parent)}：{_clean(parent)}")
    sections.append(text)
    sections.append(_media_marks(data))
    quote = data.get("quoted_tweet")
    if quote:
        sections.append(f"↳ 引用 @{_handle(quote)}：{_clean(quote)}")

    return Article(
        url=url,
        # 长文有作者写的真标题；普通帖子没有标题，留空由 AI 拟
        title=str(article.get("title") or "").strip(),
        content="\n\n".join(s for s in sections if s),
        published_at=_date(data.get("created_at")),
        account=_account(data.get("user")),
        source="x",
    )


def parse_mirror(data: dict, url: str) -> Article:
    """解析镜像接口的响应，字段名与官方接口不同。"""
    tweet = data.get("tweet") or {}
    article = tweet.get("article") or {}
    # 长文的正文在 article.content.blocks 里；退一步取预览，再退一步取推文本身
    text = _article_body(article) or str(article.get("preview_text") or "").strip()
    text = text or _strip_tco(tweet.get("text"))
    if not text:
        raise FetchError(f"镜像接口没有返回正文：{url}")

    sections = []
    if tweet.get("replying_to"):
        sections.append(f"↰ 回复 @{tweet['replying_to']}")
    sections.append(text)

    media = tweet.get("media") or {}
    marks = ["[图片]"] * len(media.get("photos") or []) + ["[视频]"] * len(media.get("videos") or [])
    sections.append(" ".join(marks))

    quote = tweet.get("quote")
    if quote:
        sections.append(f"↳ 引用 @{_handle(quote)}：{_strip_tco(quote.get('text'))}")

    stamp = tweet.get("created_timestamp")
    return Article(
        url=url,
        title=str(article.get("title") or "").strip(),  # 长文有真标题，普通帖子留空给 AI
        content="\n\n".join(s for s in sections if s),
        published_at=datetime.fromtimestamp(int(stamp), _CST).strftime("%Y-%m-%d") if stamp else None,
        account=_account(tweet.get("author")),
        source="x",
    )


def _get_json(target: str, timeout: int, retries: int) -> dict:
    last_error: Optional[Exception] = None
    for attempt in range(retries):
        try:
            response = requests.get(
                target,
                headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
                timeout=timeout,
            )
            response.raise_for_status()
            return response.json()
        except Exception as exc:  # noqa: BLE001 - 网络异常统一重试
            last_error = exc
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    raise RuntimeError(last_error)


def _token(post_id: str) -> str:
    """复刻 X 嵌入组件的 token 算法：(id/1e6)×π 转 36 进制后去掉 0 与小数点。"""
    return _base36((int(post_id) / 1e6) * math.pi).replace("0", "").replace(".", "")


def _base36(value: float, precision: int = 12) -> str:
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    whole, frac = int(value), value - int(value)
    head = ""
    while whole:
        whole, remainder = divmod(whole, 36)
        head = digits[remainder] + head
    tail = ""
    for _ in range(precision):
        frac *= 36
        tail += digits[int(frac)]
        frac -= int(frac)
    return f"{head or '0'}.{tail}"


def _note(node: dict) -> dict:
    """长推文正文。官方接口两种结构都出现过，都认。"""
    note = node.get("note_tweet") or {}
    nested = (note.get("note_tweet_results") or {}).get("result") or {}
    return nested or note


def _clean(node: dict) -> str:
    """取完整正文，t.co 短链还原成原始链接，图片/视频的自指短链直接删掉。"""
    note = _note(node)
    text = str(note.get("text") or node.get("text") or "")
    entity_sets = [node.get("entities") or {}, note.get("entity_set") or {}]
    for entities in entity_sets:
        for item in entities.get("urls") or []:
            if item.get("url") and item.get("expanded_url"):
                text = text.replace(item["url"], item["expanded_url"])
    return _strip_tco(text)


def _strip_tco(text: Optional[str]) -> str:
    return _BARE_TCO.sub("", str(text or "")).strip()


def _media_marks(node: dict) -> str:
    marks = ["[图片]"] * len(node.get("photos") or [])
    if node.get("video"):
        marks.append("[视频]")
    return " ".join(marks)


def _handle(node: dict) -> str:
    user = node.get("user") or node.get("author") or {}
    return str(user.get("screen_name") or "")


def _account(user: Optional[dict]) -> Optional[str]:
    user = user or {}
    handle = user.get("screen_name")
    if not handle:
        return None
    name = str(user.get("name") or "").strip()
    return f"{name} @{handle}" if name else f"@{handle}"


def _date(created_at: Optional[str]) -> Optional[str]:
    if not created_at:
        return None
    try:
        stamp = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
    except ValueError:
        return None
    return stamp.astimezone(_CST).strftime("%Y-%m-%d")


def _article_body(article: dict) -> str:
    """X 长文正文：Draft.js 风格的块数组，atomic 块是图片等富媒体。"""
    lines = []
    for block in (article.get("content") or {}).get("blocks") or []:
        if block.get("type") == "atomic":
            lines.append("[图片]")
            continue
        text = str(block.get("text") or "").strip()
        if text:
            lines.append(text)
    return "\n\n".join(lines)

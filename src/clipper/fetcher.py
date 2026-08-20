"""抓取并解析微信公众号文章页面。

微信页面结构变化时只需要改这一个文件，测试有 HTML fixture 兜底。
"""

from __future__ import annotations

import re
import time
from datetime import datetime, timezone, timedelta
from typing import Optional

import requests
from bs4 import BeautifulSoup

from .models import Article

# 用手机端 UA，拿到的页面结构最稳定
USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40"
)

# 命中这些文案说明被风控拦下了，不是正常文章页
_BLOCKED_MARKERS = ("环境异常", "去验证", "请在微信客户端打开链接", "参数错误")

_CT_PATTERNS = (
    re.compile(r"var\s+ct\s*=\s*[\"'](\d{10})[\"']"),
    re.compile(r"var\s+create_time\s*=\s*[\"'](\d{10})[\"']"),
)
_CREATE_TIME_TEXT = re.compile(r"createTime\s*=\s*[\"']([\d\-: ]+)[\"']")
_NICKNAME = re.compile(r"var\s+nickname\s*=\s*[\"']([^\"']+)[\"']")

_CST = timezone(timedelta(hours=8))


class FetchError(RuntimeError):
    """抓取或解析失败。"""


def fetch(url: str, timeout: int = 30, retries: int = 3) -> Article:
    """抓取文章页面，失败时指数退避重试。"""
    last_error: Optional[Exception] = None
    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                headers={"User-Agent": USER_AGENT, "Accept-Language": "zh-CN,zh;q=0.9"},
                timeout=timeout,
            )
            response.raise_for_status()
            response.encoding = response.apparent_encoding or "utf-8"
            return parse(response.text, url)
        except FetchError:
            raise  # 解析类错误重试也没用
        except Exception as exc:  # noqa: BLE001 - 网络异常统一重试
            last_error = exc
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    raise FetchError(f"抓取失败：{url}（{last_error}）")


def parse(html: str, url: str) -> Article:
    """从页面 HTML 中提取标题、正文、发布时间与公众号名。"""
    soup = BeautifulSoup(html, "html.parser")

    body = soup.select_one("#js_content") or soup.select_one("div.rich_media_content")
    title = _extract_title(soup)

    if body is None:
        page_text = soup.get_text(" ", strip=True)[:200]
        if any(marker in page_text for marker in _BLOCKED_MARKERS):
            raise FetchError(f"被微信风控拦截或链接已失效：{url}")
        raise FetchError(f"页面中找不到正文节点：{url}")

    content = _extract_content(body)
    if not content.strip():
        raise FetchError(f"正文为空：{url}")

    return Article(
        url=url,
        title=title,
        content=content,
        published_at=_extract_published_at(html),
        account=_extract_account(soup, html),
    )


def _extract_title(soup: BeautifulSoup) -> str:
    node = soup.select_one("#activity-name") or soup.select_one("h1.rich_media_title")
    if node:
        return node.get_text(strip=True)
    meta = soup.select_one('meta[property="og:title"]')
    if meta and meta.get("content"):
        return meta["content"].strip()
    if soup.title:
        return soup.title.get_text(strip=True)
    return ""


def _extract_content(body) -> str:
    """把正文转成纯文本，图片用占位符表示（微信图片有防盗链，存链接没意义）。"""
    for img in body.find_all("img"):
        img.replace_with("[图片]")

    lines = []
    for element in body.find_all(["p", "section", "h1", "h2", "h3", "li", "blockquote"]):
        # 只取叶子块，避免嵌套 section 导致正文重复
        if element.find(["p", "section", "h1", "h2", "h3", "li", "blockquote"]):
            continue
        text = element.get_text(" ", strip=True)
        if text:
            lines.append(text)

    if not lines:
        lines = [line.strip() for line in body.get_text("\n").splitlines() if line.strip()]

    # 去掉相邻重复行（微信模板常有重复的引导语）
    deduped = [line for i, line in enumerate(lines) if i == 0 or line != lines[i - 1]]
    return "\n\n".join(deduped)


def _extract_published_at(html: str) -> Optional[str]:
    for pattern in _CT_PATTERNS:
        match = pattern.search(html)
        if match:
            stamp = int(match.group(1))
            return datetime.fromtimestamp(stamp, _CST).strftime("%Y-%m-%d")
    match = _CREATE_TIME_TEXT.search(html)
    if match:
        return match.group(1).strip().split(" ")[0]
    return None


def _extract_account(soup: BeautifulSoup, html: str) -> Optional[str]:
    node = soup.select_one("#js_name")
    if node:
        return node.get_text(strip=True)
    match = _NICKNAME.search(html)
    return match.group(1) if match else None

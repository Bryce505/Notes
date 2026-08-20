from pathlib import Path

import pytest

from clipper.fetcher import FetchError, parse

FIXTURES = Path(__file__).parent / "fixtures"
URL = "https://mp.weixin.qq.com/s/AbCdEf123"


@pytest.fixture
def html() -> str:
    return (FIXTURES / "article.html").read_text(encoding="utf-8")


def test_解析标题(html):
    assert parse(html, URL).title == "为什么大模型的上下文窗口越来越长"


def test_解析正文段落(html):
    content = parse(html, URL).content
    assert "过去两年，主流模型的上下文窗口从 4K 一路涨到 200K。" in content
    assert "结论：窗口长度是手段，检索质量才是目的。" in content


def test_图片替换为占位符(html):
    content = parse(html, URL).content
    assert "[图片]" in content
    assert "mmbiz.qpic.cn" not in content


def test_解析发布时间(html):
    assert parse(html, URL).published_at == "2026-08-18"


def test_解析公众号名(html):
    assert parse(html, URL).account == "机器之心"


def test_风控页面判定为失败():
    blocked = (FIXTURES / "blocked.html").read_text(encoding="utf-8")
    with pytest.raises(FetchError, match="风控|失效"):
        parse(blocked, URL)


def test_没有正文节点时报错():
    with pytest.raises(FetchError):
        parse("<html><body><p>无关页面</p></body></html>", URL)

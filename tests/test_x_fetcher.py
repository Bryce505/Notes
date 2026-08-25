import json
from pathlib import Path

import pytest

from clipper import x_fetcher
from clipper.fetcher import FetchError

FIXTURES = Path(__file__).parent / "fixtures"
URL = "https://x.com/simonw/status/1878571238879473738"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.fixture
def post() -> dict:
    return _load("x_post.json")


@pytest.fixture
def note() -> dict:
    return _load("x_note.json")


@pytest.mark.parametrize(
    "url",
    [
        "https://x.com/simonw/status/1878571238879473738",
        "https://twitter.com/simonw/status/1878571238879473738",
        "https://www.x.com/simonw/status/1878571238879473738?s=20",
        "https://mobile.twitter.com/simonw/status/1878571238879473738",
    ],
)
def test_识别_x_帖子链接(url):
    assert x_fetcher.is_x_url(url) is True
    assert x_fetcher.tweet_id(url) == "1878571238879473738"


@pytest.mark.parametrize(
    "url",
    [
        "https://mp.weixin.qq.com/s/AbCdEf123",
        "https://x.com/simonw",
        "https://example.com/simonw/status/123",
    ],
)
def test_非_x_帖子链接不识别(url):
    assert x_fetcher.is_x_url(url) is False


def test_解析正文与作者(post):
    article = x_fetcher.parse(post, URL)
    assert "整理成一篇笔记" in article.content
    assert article.account == "Simon Willison @simonw"
    assert article.source == "x"
    assert article.url == URL


def test_短链还原为原始链接(post):
    content = x_fetcher.parse(post, URL).content
    assert "https://simonwillison.net/2026/hooks/" in content
    assert "t.co/aBcDeF1234" not in content


def test_图片自指短链删除并替换为占位符(post):
    content = x_fetcher.parse(post, URL).content
    assert "[图片]" in content
    assert "t.co/mEdIa0001" not in content
    assert "pbs.twimg.com" not in content


def test_引用的帖子附在正文后(post):
    content = x_fetcher.parse(post, URL).content
    assert "引用 @karpathy" in content
    assert "The best way to learn is to build the thing." in content
    assert content.index("整理成一篇笔记") < content.index("引用 @karpathy")


def test_发布时间按东八区计算(post):
    # UTC 是 8-19 17:30，东八区已经是 8-20
    assert x_fetcher.parse(post, URL).published_at == "2026-08-20"


def test_标题降级取首句(post):
    assert x_fetcher.parse(post, URL).title.startswith("刚把 Claude Code")


def test_长推文取完整正文而非截断正文(note):
    content = x_fetcher.parse(note, URL).content
    assert "结论——先做减法，再谈扩容" in content
    assert "长文见下" not in content, "note_tweet 存在时不应再用被截断的 text"


def test_长推文兼容扁平结构():
    data = {
        "id_str": "1",
        "text": "截断的正文 https://t.co/x",
        "user": {"name": "N", "screen_name": "n"},
        "note_tweet": {"text": "完整的长正文。"},
    }
    assert "完整的长正文。" in x_fetcher.parse(data, URL).content


def test_回复的上一条附在正文前(note):
    content = x_fetcher.parse(note, URL).content
    assert "回复 @asker" in content
    assert content.index("回复 @asker") < content.index("第一段")


def test_视频替换为占位符(note):
    assert "[视频]" in x_fetcher.parse(note, URL).content


def test_正文为空时报错():
    data = {"id_str": "1", "text": "  ", "user": {"screen_name": "n"}}
    with pytest.raises(FetchError):
        x_fetcher.parse(data, URL)


def test_帖子已删除时报错():
    with pytest.raises(FetchError, match="已删除|不可见"):
        x_fetcher.parse({"__typename": "TweetTombstone", "tombstone": {}}, URL)


def test_镜像接口响应也能解析():
    article = x_fetcher.parse_mirror(_load("x_fxtwitter.json"), URL)
    assert "镜像接口返回的正文" in article.content
    assert article.account == "Simon Willison @simonw"
    assert article.published_at == "2026-08-20"
    assert "[图片]" in article.content
    assert "引用 @karpathy" in article.content
    assert "回复 @asker" in article.content
    assert "t.co" not in article.content


def test_官方接口失败时回退到镜像(monkeypatch):
    calls = []

    class FakeResponse:
        def __init__(self, status, data):
            self.status_code, self._data = status, data

        def json(self):
            return self._data

        def raise_for_status(self):
            if self.status_code >= 400:
                raise RuntimeError(f"HTTP {self.status_code}")

    def fake_get(url, **kwargs):
        calls.append(url)
        if "syndication" in url:
            return FakeResponse(404, {})
        return FakeResponse(200, _load("x_fxtwitter.json"))

    monkeypatch.setattr(x_fetcher.requests, "get", fake_get)
    article = x_fetcher.fetch(URL, retries=1)

    assert "镜像接口返回的正文" in article.content
    assert any("syndication" in c for c in calls), "必须先试官方接口"
    assert any("fxtwitter" in c for c in calls)


def test_两个接口都失败时抛出抓取错误(monkeypatch):
    def fake_get(url, **kwargs):
        raise RuntimeError("connection refused")

    monkeypatch.setattr(x_fetcher.requests, "get", fake_get)
    with pytest.raises(FetchError):
        x_fetcher.fetch(URL, retries=1)


def test_token_不含零与小数点():
    token = x_fetcher._token("1878571238879473738")
    assert token and "0" not in token and "." not in token
    assert x_fetcher._token("1878571238879473738") == token, "同一条帖子的 token 必须稳定"

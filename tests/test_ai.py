import json

import pytest

from clipper import ai
from clipper.models import Digest

RAW = json.dumps(
    {
        "title": "标题",
        "summary": "这是摘要。",
        "keywords": ["A", "B", "C"],
        "insights": ["洞见一", "洞见二"],
        "priority": "高",
        "priority_reason": "值得读。",
    },
    ensure_ascii=False,
)


def test_解析正常返回():
    result = ai._parse(RAW)
    assert result.summary == "这是摘要。"
    assert result.keywords == ["A", "B", "C"]
    assert result.priority == "高"
    assert result.failed is False


def test_解析被代码块包裹的返回():
    assert ai._parse(f"```json\n{RAW}\n```").summary == "这是摘要。"


def test_非法优先级归一为中():
    assert ai._parse(json.dumps({"summary": "x", "priority": "非常高"})).priority == "中"


def test_缺少摘要视为失败():
    with pytest.raises(ai.AIError):
        ai._parse(json.dumps({"keywords": ["a"]}))


def test_完全不是_json_时报错():
    with pytest.raises(ai.AIError):
        ai._parse("我无法处理这篇文章")


def test_超长正文保留首尾():
    content = "头" * 1000 + "中" * 1000 + "尾" * 1000
    truncated = ai.truncate(content, 200)
    assert truncated.startswith("头")
    assert truncated.endswith("尾")
    assert "省略" in truncated


def test_短正文不截断():
    assert ai.truncate("短文", 100) == "短文"


def test_调用失败时降级不抛异常(article, config, monkeypatch):
    monkeypatch.setattr(ai, "_call", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("超时")))
    result = ai.digest(article, config)
    assert isinstance(result, Digest)
    assert result.failed is True
    assert "AI 处理失败" in result.summary


def test_端点兼容两种_base_url_写法():
    assert ai.endpoint("https://api.deepseek.com") == "https://api.deepseek.com/v1/chat/completions"
    assert ai.endpoint("https://api.deepseek.com/") == "https://api.deepseek.com/v1/chat/completions"
    assert ai.endpoint("https://api.x.com/v1") == "https://api.x.com/v1/chat/completions"


def test_模型不支持_json_模式时自动去掉该参数重试(config, monkeypatch):
    calls = []

    class FakeResponse:
        def __init__(self, status, text, data=None):
            self.status_code, self.text, self._data = status, text, data

        def json(self):
            return self._data

    def fake_post(payload, cfg):
        calls.append(payload.copy())
        if "response_format" in payload:
            return FakeResponse(400, '{"error":"response_format not supported"}')
        return FakeResponse(200, "", {"choices": [{"message": {"content": RAW}}]})

    monkeypatch.setattr(ai, "_post", fake_post)
    assert ai._call("prompt", config) == RAW
    assert len(calls) == 2
    assert "response_format" in calls[0] and "response_format" not in calls[1]


def _captured_system(monkeypatch, art, config):
    seen = {}

    def fake_call(prompt, cfg, system):
        seen["system"] = system
        return RAW

    monkeypatch.setattr(ai, "_call", fake_call)
    ai.digest(art, config)
    return seen["system"]


def test_x_帖子追加专用提示词(x_article, config, monkeypatch):
    system = _captured_system(monkeypatch, x_article, config)
    assert ai.X_PROMPT_HINT in system


def test_公众号提示词保持原样(article, config, monkeypatch):
    assert _captured_system(monkeypatch, article, config) == ai.SYSTEM_PROMPT

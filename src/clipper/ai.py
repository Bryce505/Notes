"""调用 AI 消化文章，产出摘要、关键词、洞见与阅读优先级。

走 OpenAI 兼容的 /chat/completions 接口，换服务商只改环境变量。
"""

from __future__ import annotations

import json
import re
from typing import Optional

import requests

from .config import Config
from .models import Article, Digest

SYSTEM_PROMPT = """你是一位帮助读者做「稍后阅读」筛选的中文助手。
用户会给你一篇微信公众号文章的正文，你要读完并输出结构化信息，帮助用户在不打开原文的情况下
判断这篇文章值不值得花时间精读。

只输出一个 JSON 对象，不要输出任何解释文字或 Markdown 代码块标记，字段如下：
{
  "title": "文章标题，若正文中能判断则填写，否则填空字符串",
  "summary": "150-250 字摘要：文章讲了什么、用了什么论据、结论是什么",
  "keywords": ["3-6 个关键词，单个词或短语"],
  "insights": ["2-4 条洞见，每条一句话：核心观点、反直觉结论或可迁移的方法"],
  "priority": "高、中、低 三者之一",
  "priority_reason": "一句话说明为什么值得或不值得精读"
}

判断优先级的标准：信息密度高、有独到观点或可操作方法的为「高」；常规科普、观点重复的为「中」；
营销软文、纯资讯罗列、标题党的为「低」。"""

X_PROMPT_HINT = """

本条来源是 X（原推特）帖子，不是长文，按下面几点调整：
- 摘要压到 50-120 字，说清楚作者主张什么、给了什么依据或例子；
- 原文常是英文，输出一律用中文；
- title 字段必填：给这条帖子拟一个 20 字以内的中文标题；
- 只是转发链接、纯情绪表达或广告的帖子，优先级判「低」。"""

_JSON_BLOCK = re.compile(r"\{.*\}", re.S)


class AIError(RuntimeError):
    """AI 调用或解析失败。"""


def digest(article: Article, config: Config, retries: int = 2) -> Digest:
    """消化文章。彻底失败时返回降级 Digest，保证链接与正文仍能落库。"""
    content = truncate(article.content, config.max_content_chars)
    prompt = f"标题：{article.title or '（未抓取到）'}\n\n正文：\n{content}"
    system = SYSTEM_PROMPT + (X_PROMPT_HINT if article.source == "x" else "")

    last_error: Optional[Exception] = None
    for _ in range(retries):
        try:
            raw = _call(prompt, config, system)
            return _parse(raw)
        except Exception as exc:  # noqa: BLE001 - 网络与解析异常都重试
            last_error = exc

    return Digest(
        summary=f"AI 处理失败（{last_error}），正文已完整保存，请直接查看快照。",
        keywords=[],
        insights=[],
        priority="中",
        priority_reason="AI 未能处理，优先级待人工判断。",
        failed=True,
    )


def truncate(content: str, limit: int) -> str:
    """超长正文保留头部 60%、尾部 40%。

    公众号文章的结论常在末尾，只截开头会导致优先级误判。
    """
    if len(content) <= limit:
        return content
    head = int(limit * 0.6)
    tail = limit - head
    return f"{content[:head]}\n\n……（此处省略中间内容）……\n\n{content[-tail:]}"


def endpoint(base_url: str) -> str:
    """兼容填 https://api.x.com 和 https://api.x.com/v1 两种写法。"""
    base = base_url.rstrip("/")
    return f"{base}/chat/completions" if base.endswith("/v1") else f"{base}/v1/chat/completions"


def _call(prompt: str, config: Config, system: str = SYSTEM_PROMPT) -> str:
    if not config.ai_api_key:
        raise AIError("未配置 AI_API_KEY")

    payload = {
        "model": config.ai_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
    }
    response = _post(payload, config)

    # 有些模型不支持强制 JSON 模式，去掉该参数重试一次；
    # 系统提示词本身已要求只输出 JSON，_parse 也能从代码块里抠出来
    if response.status_code == 400 and "response_format" in response.text:
        payload.pop("response_format")
        response = _post(payload, config)

    if response.status_code >= 400:
        raise AIError(f"HTTP {response.status_code}：{response.text[:200]}")
    return response.json()["choices"][0]["message"]["content"]


def _post(payload: dict, config: Config):
    return requests.post(
        endpoint(config.ai_base_url),
        headers={
            "Authorization": f"Bearer {config.ai_api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=config.request_timeout * 4,
    )


def _parse(raw: str) -> Digest:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        match = _JSON_BLOCK.search(raw)
        if not match:
            raise AIError(f"返回内容不是 JSON：{raw[:120]}")
        data = json.loads(match.group(0))

    summary = str(data.get("summary", "")).strip()
    if not summary:
        raise AIError("返回结果缺少 summary 字段")

    priority = str(data.get("priority", "中")).strip()
    if priority not in ("高", "中", "低"):
        priority = "中"

    return Digest(
        summary=summary,
        keywords=[str(k).strip() for k in data.get("keywords", []) if str(k).strip()][:6],
        insights=[str(i).strip() for i in data.get("insights", []) if str(i).strip()][:4],
        priority=priority,
        priority_reason=str(data.get("priority_reason", "")).strip(),
        title=str(data.get("title", "")).strip() or None,
    )

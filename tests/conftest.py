from datetime import datetime

import pytest

from clipper.config import Config
from clipper.models import Article, Digest, Entry
from clipper.pipeline import CST


@pytest.fixture
def article() -> Article:
    return Article(
        url="https://mp.weixin.qq.com/s/AbCdEf123",
        title="为什么大模型的上下文窗口越来越长",
        content="第一段正文。\n\n第二段正文。",
        published_at="2026-08-18",
        account="机器之心",
    )


@pytest.fixture
def digest() -> Digest:
    return Digest(
        summary="文章分析了上下文窗口变长的原因与代价。",
        keywords=["长上下文", "注意力机制"],
        insights=["窗口长度是手段不是目的。", "检索质量决定实际效果。"],
        priority="高",
        priority_reason="有明确结论且可迁移。",
    )


@pytest.fixture
def entry(article, digest) -> Entry:
    return Entry(
        article=article,
        digest=digest,
        clipped_at=datetime(2026, 8, 20, 19, 44, tzinfo=CST),
    )


@pytest.fixture
def config(tmp_path) -> Config:
    return Config(ai_api_key="test-key", repo_dir=str(tmp_path))


@pytest.fixture
def x_article() -> Article:
    return Article(
        url="https://x.com/simonw/status/1878571238879473738",
        title="刚把 Claude Code 的 hooks 用法整理成一篇笔记",
        content="刚把 Claude Code 的 hooks 用法整理成一篇笔记\n\n[图片]",
        published_at="2026-08-20",
        account="Simon Willison @simonw",
        source="x",
    )


@pytest.fixture
def x_entry(x_article, digest) -> Entry:
    return Entry(
        article=x_article,
        digest=digest,
        clipped_at=datetime(2026, 8, 20, 19, 44, tzinfo=CST),
    )

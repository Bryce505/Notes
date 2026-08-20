from datetime import datetime

import pytest

from clipper import pipeline
from clipper.models import Article
from clipper.pipeline import CST, clip
from clipper.store import Store


@pytest.fixture
def fake_fetch(monkeypatch, article):
    def _fetch(url, timeout=30, retries=3):
        return Article(
            url=url,
            title=article.title,
            content=article.content,
            published_at=article.published_at,
            account=article.account,
        )

    monkeypatch.setattr(pipeline.fetcher, "fetch", _fetch)


@pytest.fixture
def fake_ai(monkeypatch, digest):
    monkeypatch.setattr(pipeline.ai, "digest", lambda article, config: digest)


def test_完整流程写入_md_与索引(config, fake_fetch, fake_ai, tmp_path):
    store = Store(config.repo_dir)
    result = clip("https://mp.weixin.qq.com/s/AbCdEf123", config, store)

    assert result.status == "created"
    assert (tmp_path / "notes" / "2026-08.md").exists() or (
        tmp_path / "notes"
    ).exists()
    assert store.is_duplicate("https://mp.weixin.qq.com/s/AbCdEf123")


def test_重复链接直接跳过(config, fake_fetch, fake_ai):
    store = Store(config.repo_dir)
    url = "https://mp.weixin.qq.com/s/AbCdEf123"
    clip(url, config, store)
    result = clip(url, config, store)
    assert result.status == "duplicate"


def test_抓取失败时不写入任何内容(config, monkeypatch, fake_ai, tmp_path):
    def _boom(url, timeout=30, retries=3):
        raise RuntimeError("被拦截")

    monkeypatch.setattr(pipeline.fetcher, "fetch", _boom)
    store = Store(config.repo_dir)
    result = clip("https://mp.weixin.qq.com/s/Broken", config, store)

    assert result.status == "failed"
    assert "被拦截" in result.message
    assert not (tmp_path / "notes").exists()
    assert not store.is_duplicate("https://mp.weixin.qq.com/s/Broken")


def test_未配置_notion_时只写_md(config, fake_fetch, fake_ai):
    assert config.notion_enabled is False
    store = Store(config.repo_dir)
    result = clip("https://mp.weixin.qq.com/s/AbCdEf123", config, store)
    assert result.status == "created"
    assert result.notion_page_id is None


def test_指定剪藏日期用于分月(config, fake_fetch, fake_ai, tmp_path):
    store = Store(config.repo_dir)
    clip(
        "https://mp.weixin.qq.com/s/OldOne",
        config,
        store,
        clipped_at=datetime(2026, 7, 3, 10, 0, tzinfo=CST),
    )
    assert (tmp_path / "notes" / "2026-07.md").exists()


def test_dry_run_不落盘(config, fake_fetch, fake_ai, tmp_path):
    store = Store(config.repo_dir)
    result = clip("https://mp.weixin.qq.com/s/AbCdEf123", config, store, dry_run=True)
    assert result.status == "created"
    assert not (tmp_path / "notes").exists()
    assert not store.is_duplicate("https://mp.weixin.qq.com/s/AbCdEf123")

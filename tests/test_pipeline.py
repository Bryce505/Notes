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
    assert config.notion_enabled_for("weixin") is False
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


def test_notion_失败时记录原因但仍写_md(config, fake_fetch, fake_ai, tmp_path, monkeypatch):
    """Notion 挂了不能丢内容，但失败原因必须留在结果里，好让上层报错。"""
    config.notion_token = "t"
    config.notion_database_id = "db"

    import clipper.notion_writer as nw

    class Boom:
        def __init__(self, cfg):
            pass

        def create_page(self, entry):
            raise RuntimeError("multiple data sources not supported")

    monkeypatch.setattr(nw, "NotionWriter", Boom)
    result = clip("https://mp.weixin.qq.com/s/AbCdEf123", config, Store(config.repo_dir))

    assert result.status == "created"
    assert "multiple data sources" in result.notion_error
    assert (tmp_path / "notes" / "2026-08.md").exists()


@pytest.fixture
def fake_x_fetch(monkeypatch, x_article):
    """X 抓取器返回固定内容，同时保证公众号抓取器一旦被调用就炸掉。"""

    def _boom(url, timeout=30, retries=3):
        raise AssertionError("X 链接不应该走公众号抓取器")

    monkeypatch.setattr(pipeline.fetcher, "fetch", _boom)
    monkeypatch.setattr(
        pipeline.x_fetcher,
        "fetch",
        lambda url, timeout=30, retries=3: Article(
            url=url,
            title="",  # 普通帖子没有标题，与真实抓取器一致
            content=x_article.content,
            published_at=x_article.published_at,
            account=x_article.account,
            source="x",
        ),
    )


X_URL = "https://x.com/simonw/status/1878571238879473738"


def test_x_链接走_x_抓取器并归档到独立目录(config, fake_x_fetch, fake_ai, tmp_path):
    result = clip(X_URL, config, Store(config.repo_dir))

    assert result.status == "created"
    assert (tmp_path / "notes" / "x" / "2026-08.md").exists()
    assert not (tmp_path / "notes" / "2026-08.md").exists()


def test_x_帖子采用_ai_拟的中文标题(config, fake_x_fetch, monkeypatch, digest):
    digest.title = "Claude Code hooks 用法笔记"
    monkeypatch.setattr(pipeline.ai, "digest", lambda article, config: digest)

    result = clip(X_URL, config, Store(config.repo_dir))
    assert result.title == "Claude Code hooks 用法笔记"


def test_ai_没给标题时用正文首句兜底(config, fake_x_fetch, monkeypatch, digest):
    digest.title = None
    monkeypatch.setattr(pipeline.ai, "digest", lambda article, config: digest)

    result = clip(X_URL, config, Store(config.repo_dir))
    assert result.title.startswith("刚把 Claude Code")


def test_x_帖子写入独立的_notion_库(config, fake_x_fetch, fake_ai, monkeypatch):
    config.notion_token = "t"
    config.notion_database_id = "db-weixin"
    config.notion_x_database_id = "db-x"

    import clipper.notion_writer as nw

    seen = {}

    class Recorder:
        def __init__(self, cfg):
            self.cfg = cfg

        def create_page(self, entry):
            seen["db"] = self.cfg.database_id_for(entry.article.source)
            return "page-id"

    monkeypatch.setattr(nw, "NotionWriter", Recorder)
    result = clip(X_URL, config, Store(config.repo_dir))

    assert seen["db"] == "db-x"
    assert result.notion_page_id == "page-id"


def test_没配_x_库时_x_帖子只写_md(config, fake_x_fetch, fake_ai, tmp_path):
    config.notion_token = "t"
    config.notion_database_id = "db-weixin"

    result = clip(X_URL, config, Store(config.repo_dir))
    assert result.status == "created"
    assert result.notion_page_id is None
    assert result.notion_error == ""
    assert (tmp_path / "notes" / "x" / "2026-08.md").exists()

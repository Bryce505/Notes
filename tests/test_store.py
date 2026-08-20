from clipper.store import Store


def test_首次链接不算重复(entry, tmp_path):
    store = Store(str(tmp_path))
    assert store.is_duplicate(entry.article.url) is False


def test_记录后判定为重复(entry, tmp_path):
    store = Store(str(tmp_path))
    store.add(entry, notion_page_id="page-1")
    assert store.is_duplicate(entry.article.url) is True
    assert Store(str(tmp_path)).is_duplicate(entry.article.url) is True


def test_追踪参数不同仍判定为重复(entry, tmp_path):
    store = Store(str(tmp_path))
    store.add(entry)
    assert store.is_duplicate(entry.article.url + "?from=groupmessage") is True


def test_索引内容可读回(entry, tmp_path):
    store = Store(str(tmp_path))
    store.add(entry, notion_page_id="page-1")
    record = store.get(entry.article.url)
    assert record["title"] == entry.title
    assert record["notion_page_id"] == "page-1"
    assert record["md_path"] == "notes/2026-08.md"

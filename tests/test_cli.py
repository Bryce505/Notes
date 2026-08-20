from clipper.cli import _report
from clipper.pipeline import Result


def test_全部成功时返回零():
    assert _report([Result(url="u", status="created", title="t")]) == 0


def test_抓取失败时返回非零():
    assert _report([Result(url="u", status="failed", message="超时")]) == 1


def test_notion_失败时也返回非零(capsys):
    """否则 Actions 一片绿，人不会发现文章没进 Notion。"""
    code = _report([
        Result(url="u", status="created", title="某文章", notion_error="400 多数据源不支持")
    ])
    assert code == 1
    out = capsys.readouterr().out
    assert "Notion 写入失败" in out
    assert "400 多数据源不支持" in out
    assert "内容未丢失" in out


def test_重复不算失败():
    assert _report([Result(url="u", status="duplicate", title="t")]) == 0

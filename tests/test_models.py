from clipper.models import fingerprint


def test_短链接取路径中的标识():
    assert fingerprint("https://mp.weixin.qq.com/s/AbCdEf123") == "AbCdEf123"


def test_带参数链接取_sn_参数():
    url = "https://mp.weixin.qq.com/s?__biz=MzA5&mid=2650&idx=1&sn=abc123&chksm=xyz"
    assert fingerprint(url) == "abc123"


def test_同一文章不同追踪参数视为同一篇():
    a = "https://mp.weixin.qq.com/s/AbCdEf123?from=timeline"
    b = "https://mp.weixin.qq.com/s/AbCdEf123?scene=27&key=xx"
    assert fingerprint(a) == fingerprint(b)


def test_无法识别时回退到哈希():
    value = fingerprint("https://example.com/post/1")
    assert len(value) == 40


def test_条目按剪藏时间分月(entry):
    assert entry.month == "2026-08"
    assert entry.month_heading == "2026年08月"
    assert entry.notes_path == "notes/2026-08.md"
    assert entry.snapshot_path.startswith("archive/2026-08/")


def test_快照文件名清洗非法字符(entry):
    entry.article.title = 'a/b:c*d?"e<f>g|h'
    assert "/" not in entry.slug.replace("archive/", "")
    assert ":" not in entry.slug


def test_x_帖子按推文_id_查重():
    a = "https://x.com/simonw/status/1878571238879473738?s=20&t=abc"
    b = "https://twitter.com/SimonW/status/1878571238879473738"
    assert fingerprint(a) == fingerprint(b) == "x-1878571238879473738"


def test_x_条目归档到独立目录(x_entry):
    assert x_entry.notes_path == "notes/x/2026-08.md"
    assert x_entry.snapshot_path.startswith("archive/x/2026-08/")


def test_公众号条目路径不受影响(entry):
    assert entry.notes_path == "notes/2026-08.md"
    assert entry.snapshot_path.startswith("archive/2026-08/")


def test_同期两条帖子的快照文件名不同(x_entry, digest):
    """推文 ID 是雪花号，同一时期前缀完全相同，文件名后缀必须取尾号才有区分度。"""
    from datetime import datetime

    from clipper.models import Article, Entry
    from clipper.pipeline import CST

    other = Entry(
        article=Article(
            url="https://x.com/simonw/status/1878571238879999999",
            title=x_entry.title,
            content="另一条帖子",
            source="x",
        ),
        digest=digest,
        clipped_at=datetime(2026, 8, 20, 20, 0, tzinfo=CST),
    )
    assert other.slug != x_entry.slug


def test_其他站点的_status_路径不当成_x_帖子():
    value = fingerprint("https://example.com/foo/status/123")
    assert not value.startswith("x-")
    assert len(value) == 40

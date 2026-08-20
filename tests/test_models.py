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

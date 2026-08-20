from clipper.models import Entry
from clipper.notion_writer import BLOCK_LIMIT, TEXT_LIMIT, build_blocks, build_properties


def test_属性映射完整(entry):
    props = build_properties(entry)
    assert props["标题"]["title"][0]["text"]["content"] == entry.title
    assert props["链接"]["url"] == entry.article.url
    assert props["AI优先级"]["select"]["name"] == "高"
    assert props["阅读状态"]["select"]["name"] == "未读"
    assert [k["name"] for k in props["关键词"]["multi_select"]] == ["长上下文", "注意力机制"]
    assert props["发布时间"]["date"]["start"] == "2026-08-18"


def test_没有发布时间时不写该属性(entry):
    entry.article.published_at = None
    assert "发布时间" not in build_properties(entry)


def test_超长摘要切分到两千字以内(entry):
    entry.digest.summary = "字" * 5000
    chunks = build_properties(entry)["摘要"]["rich_text"]
    assert len(chunks) == 3
    assert all(len(c["text"]["content"]) <= TEXT_LIMIT for c in chunks)


def test_正文按段落转成块(entry):
    blocks = build_blocks(entry)
    assert len(blocks) == 2
    assert blocks[0]["paragraph"]["rich_text"][0]["text"]["content"] == "第一段正文。"


def test_超长段落切成多个块(entry):
    entry.article.content = "字" * 4500
    blocks = build_blocks(entry)
    assert len(blocks) == 3
    assert all(
        len(b["paragraph"]["rich_text"][0]["text"]["content"]) <= TEXT_LIMIT for b in blocks
    )


def test_长文章块数可超过单次上限(entry):
    entry.article.content = "\n\n".join(f"第{i}段" for i in range(250))
    assert len(build_blocks(entry)) > BLOCK_LIMIT

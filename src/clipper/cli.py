"""命令行入口：单条剪藏、批量导入、初始化 Notion 数据库。"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from typing import List, Optional, Tuple

from .config import Config
from .pipeline import CST, Result, clip
from .store import Store


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="clipper", description="微信公众号文章剪藏助手")
    sub = parser.add_subparsers(dest="command", required=True)

    one = sub.add_parser("clip", help="剪藏单篇文章")
    one.add_argument("url")
    one.add_argument("--dry-run", action="store_true", help="只跑抓取与 AI，不写任何存储")

    batch = sub.add_parser("batch", help="批量导入：每行一个链接，可用 TAB 指定剪藏日期")
    batch.add_argument("file")
    batch.add_argument("--interval", type=float, default=4.0, help="条目间隔秒数，避开微信频控")
    batch.add_argument("--dry-run", action="store_true")

    init = sub.add_parser("init-notion", help="在指定 Notion 页面下创建数据库")
    init.add_argument("--parent-page", required=True, help="父页面 ID（32 位十六进制）")
    init.add_argument("--title", default="公众号剪藏")

    args = parser.parse_args(argv)
    config = Config.from_env()

    if args.command == "init-notion":
        return _init_notion(config, args.parent_page, args.title)

    store = Store(config.repo_dir)

    if args.command == "clip":
        return _report([clip(args.url, config, store, dry_run=args.dry_run)])

    entries = _read_batch_file(args.file)
    results = []
    for index, (url, clipped_at) in enumerate(entries):
        results.append(clip(url, config, store, clipped_at=clipped_at, dry_run=args.dry_run))
        print(f"[{index + 1}/{len(entries)}] {results[-1].status} {url}", flush=True)
        if index < len(entries) - 1:
            time.sleep(args.interval)
    return _report(results)


def _read_batch_file(path: str) -> List[Tuple[str, Optional[datetime]]]:
    """解析批量文件。支持 `<url>` 或 `<url>\t<YYYY-MM-DD>` 指定原始收藏日期。"""
    entries: List[Tuple[str, Optional[datetime]]] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            url = parts[0].strip()
            clipped_at = None
            if len(parts) > 1 and parts[1].strip():
                clipped_at = datetime.strptime(parts[1].strip(), "%Y-%m-%d").replace(tzinfo=CST)
            entries.append((url, clipped_at))
    return entries


def _init_notion(config: Config, parent_page: str, title: str) -> int:
    from .notion_writer import NotionWriter

    database_id = NotionWriter(config).init_database(parent_page, title)
    print(f"数据库已创建，请把下面这行填进 GitHub Secrets 的 NOTION_DATABASE_ID：\n{database_id}")
    return 0


def _report(results: List[Result]) -> int:
    created = [r for r in results if r.status == "created"]
    duplicate = [r for r in results if r.status == "duplicate"]
    failed = [r for r in results if r.status == "failed"]

    for result in results:
        print(f"[{result.status}] {result.title or result.url} —— {result.message}")

    print(f"\n汇总：新增 {len(created)}，重复 {len(duplicate)}，失败 {len(failed)}")
    if failed:
        print("失败链接：")
        for result in failed:
            print(f"  {result.url} —— {result.message}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

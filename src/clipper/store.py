"""剪藏索引：查重与记录，落在 data/index.json。"""

from __future__ import annotations

import json
import os
from typing import Dict, Optional

from .models import Entry, fingerprint


class Store:
    def __init__(self, repo_dir: str = "."):
        self.path = os.path.join(repo_dir, "data", "index.json")
        self._data: Dict[str, dict] = self._load()

    def _load(self) -> Dict[str, dict]:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, encoding="utf-8") as fh:
            content = fh.read().strip()
        return json.loads(content) if content else {}

    def is_duplicate(self, url: str) -> bool:
        return fingerprint(url) in self._data

    def get(self, url: str) -> Optional[dict]:
        return self._data.get(fingerprint(url))

    def add(self, entry: Entry, notion_page_id: Optional[str] = None) -> None:
        self._data[entry.fingerprint] = {
            "url": entry.article.url,
            "title": entry.title,
            "clipped_at": entry.clipped_at.isoformat(),
            "notion_page_id": notion_page_id,
            "md_path": entry.notes_path,
            "snapshot_path": entry.snapshot_path,
        }
        self.save()

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(self._data, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")

"""运行配置，全部来自环境变量，便于在 GitHub Actions 中用 Secrets 注入。"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    ai_base_url: str = "https://api.deepseek.com"
    ai_api_key: str = ""
    ai_model: str = "deepseek-chat"
    notion_token: Optional[str] = None
    notion_database_id: Optional[str] = None
    repo_dir: str = "."
    max_content_chars: int = 20000
    request_timeout: int = 30

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            ai_base_url=os.getenv("AI_BASE_URL", "https://api.deepseek.com").rstrip("/"),
            ai_api_key=os.getenv("AI_API_KEY", ""),
            ai_model=os.getenv("AI_MODEL", "deepseek-chat"),
            notion_token=os.getenv("NOTION_TOKEN") or None,
            notion_database_id=os.getenv("NOTION_DATABASE_ID") or None,
            repo_dir=os.getenv("REPO_DIR", "."),
            max_content_chars=int(os.getenv("MAX_CONTENT_CHARS", "20000")),
            request_timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
        )

    @property
    def notion_enabled(self) -> bool:
        """未配置 Notion 时自动降级为只写 md，不阻断流程。"""
        return bool(self.notion_token and self.notion_database_id)

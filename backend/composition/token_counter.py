from __future__ import annotations

import re
from typing import Iterable


try:
    import tiktoken  # type: ignore
except ImportError:  # pragma: no cover - exercised implicitly in environments without tiktoken
    tiktoken = None


class TokenCounter:
    def __init__(self) -> None:
        self._encoding = None
        if tiktoken is not None:
            self._encoding = tiktoken.get_encoding("cl100k_base")

    def count_text(self, text: str) -> int:
        if not text:
            return 0
        if self._encoding is not None:
            return len(self._encoding.encode(text))
        tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
        return max(1, int(len(tokens) * 1.9))

    def count_total(self, parts: Iterable[str]) -> int:
        return sum(self.count_text(part) for part in parts)

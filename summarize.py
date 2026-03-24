"""LLM summarization + importance scoring for PulseWatch diffs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from openai_client import summarize_diff_json


MAX_INPUT_TOKENS = 500
# Rough heuristic without tokenizer dependency.
APPROX_CHARS_PER_TOKEN = 4
MAX_INPUT_CHARS = MAX_INPUT_TOKENS * APPROX_CHARS_PER_TOKEN
CACHE_PATH = Path("data") / "_summary_cache.json"


def _truncate_diff(diff_text: str) -> str:
    return diff_text[:MAX_INPUT_CHARS]


def _diff_hash(diff_text: str) -> str:
    return hashlib.sha256(diff_text.encode("utf-8")).hexdigest()


def _load_cache() -> dict[str, dict[str, Any]]:
    if not CACHE_PATH.exists():
        return {}
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _save_cache(cache: dict[str, dict[str, Any]]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def _extract_json_object(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    # Handle fenced blocks if model returns markdown.
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            cleaned = part.strip()
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
            if cleaned.startswith("{") and cleaned.endswith("}"):
                text = cleaned
                break
    data = json.loads(text)
    return data


def summarize(diff_text: str, api_key: str) -> dict[str, Any]:
    """Summarize diff text and return normalized summary payload."""
    diff_text = diff_text.strip()
    diff_hash = _diff_hash(diff_text)

    cache = _load_cache()
    if diff_hash in cache:
        return cache[diff_hash]

    truncated = _truncate_diff(diff_text)
    prompt = (
        "You are an analyst for website monitoring. Given a unified diff, output ONLY JSON "
        "with keys: summary, importance, category.\n"
        "Rules:\n"
        "- summary: 2-3 sentences describing what changed.\n"
        "- importance: float from 0 to 1 (0=trivial noise, 1=major business-impacting change).\n"
        "- category: one of pricing, product, contact, legal, other.\n"
        "- Be concise and factual.\n\n"
        f"DIFF:\n{truncated}"
    )

    raw = summarize_diff_json(prompt, api_key=api_key)
    parsed = _extract_json_object(raw)

    result = {
        "diff_hash": diff_hash,
        "summary": str(parsed.get("summary", "")).strip(),
        "importance": max(0.0, min(1.0, float(parsed.get("importance", 0.0)))),
        "category": str(parsed.get("category", "other")).strip().lower() or "other",
    }

    if result["category"] not in {"pricing", "product", "contact", "legal", "other"}:
        result["category"] = "other"

    cache[diff_hash] = result
    _save_cache(cache)
    return result


def write_summary_file(summary: dict[str, Any], capture_dir: Path) -> Path:
    """Persist summary payload in capture directory as summary.json."""
    capture_dir.mkdir(parents=True, exist_ok=True)
    summary_path = capture_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary_path

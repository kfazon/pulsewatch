"""Digest scheduler helpers for PulseWatch."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from alerts.discord import send_digest

logger = logging.getLogger(__name__)


def _iter_summary_files(data_dir: Path) -> list[Path]:
    return list(data_dir.glob("**/summary.json"))


def _parse_capture_date(path: Path, data_dir: Path) -> datetime | None:
    """Infer capture date from data/<host>/<YYYY-MM-DD>/<capture_id>/summary.json."""
    try:
        rel = path.relative_to(data_dir)
    except ValueError:
        return None

    parts = rel.parts
    if len(parts) < 4:
        return None

    date_str = parts[1]
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def _target_url_for_summary(summary_path: Path) -> str:
    meta_path = summary_path.with_name("metadata.json")
    if not meta_path.exists():
        return "unknown"

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "unknown"

    return str(meta.get("url", "unknown"))


def check_and_send_digest(data_dir: str = "data") -> int:
    """Collect last 7 days of summaries and send Discord weekly digest.

    Returns number of summaries included.
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook_url:
        logger.warning("DISCORD_WEBHOOK_URL not set; skipping digest send")
        return 0

    base = Path(data_dir)
    now = datetime.utcnow()
    cutoff = now - timedelta(days=7)

    digest_items: list[dict[str, Any]] = []

    for summary_path in _iter_summary_files(base):
        capture_date = _parse_capture_date(summary_path, base)
        if capture_date is None or capture_date < cutoff:
            continue

        try:
            payload = json.loads(summary_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            logger.warning("Skipping malformed summary file: %s", summary_path)
            continue

        digest_items.append(
            {
                "target_url": _target_url_for_summary(summary_path),
                "category": payload.get("category", "other"),
                "importance": payload.get("importance", 0.0),
                "summary": payload.get("summary", ""),
            }
        )

    if not digest_items:
        logger.info("No summaries found in last 7 days; digest not sent")
        return 0

    send_digest(webhook_url=webhook_url, summaries=digest_items)
    return len(digest_items)

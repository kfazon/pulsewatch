"""Discord webhook delivery for PulseWatch alerts."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any
from urllib import error, request

logger = logging.getLogger(__name__)


def _importance_bar(score: float, blocks: int = 10) -> str:
    score = max(0.0, min(1.0, float(score)))
    filled = round(score * blocks)
    return "█" * filled + "░" * (blocks - filled)


def _embed_color(score: float) -> int:
    if score > 0.7:
        return 0xE74C3C  # red
    if score > 0.4:
        return 0xF1C40F  # yellow
    return 0x2ECC71  # green


def _post_webhook(webhook_url: str, payload: dict[str, Any]) -> None:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=15) as resp:
            if resp.status >= 400:
                raise RuntimeError(f"Discord webhook failed with HTTP {resp.status}")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Discord webhook HTTPError {exc.code}: {body}") from exc


def send_alert(webhook_url: str, summary: dict[str, Any], target_url: str) -> None:
    """Send one high-importance change alert as a Discord embed."""
    importance = max(0.0, min(1.0, float(summary.get("importance", 0.0))))
    category = str(summary.get("category", "other"))
    summary_text = str(summary.get("summary", "")).strip() or "No summary text provided."

    payload = {
        "embeds": [
            {
                "title": "🔔 Competitor change detected",
                "color": _embed_color(importance),
                "fields": [
                    {"name": "Target", "value": target_url[:1024], "inline": False},
                    {"name": "Category", "value": category[:1024], "inline": True},
                    {
                        "name": "Importance",
                        "value": f"{_importance_bar(importance)}  ({importance:.2f})",
                        "inline": True,
                    },
                    {"name": "Summary", "value": summary_text[:1024], "inline": False},
                ],
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        ]
    }

    _post_webhook(webhook_url, payload)
    logger.info("Sent Discord alert for %s (importance %.2f)", target_url, importance)


def send_digest(webhook_url: str, summaries: list[dict[str, Any]]) -> None:
    """Send weekly digest with all summaries from the last 7 days."""
    if not summaries:
        logger.info("No summaries provided for weekly digest; skipping send")
        return

    lines: list[str] = []
    for idx, item in enumerate(summaries, start=1):
        target = str(item.get("target_url", "unknown target"))
        category = str(item.get("category", "other"))
        importance = max(0.0, min(1.0, float(item.get("importance", 0.0))))
        text = str(item.get("summary", "")).strip().replace("\n", " ")
        if len(text) > 180:
            text = text[:177] + "..."
        lines.append(f"{idx}. **{category}** • {importance:.2f} • <{target}>\n{text}")

    joined = "\n\n".join(lines)
    max_len = 4000
    if len(joined) > max_len:
        joined = joined[: max_len - 3] + "..."

    payload = {
        "embeds": [
            {
                "title": "📊 Weekly PulseWatch Digest",
                "description": joined,
                "color": 0x3498DB,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        ]
    }

    _post_webhook(webhook_url, payload)
    logger.info("Sent Discord weekly digest with %s summaries", len(summaries))

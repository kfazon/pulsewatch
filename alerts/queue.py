"""In-process queue for Discord alert delivery (MVP, no Redis)."""

from __future__ import annotations

import logging
import os
import queue
import threading
import time
from typing import Any

from alerts.discord import send_alert

logger = logging.getLogger(__name__)

_ALERT_QUEUE: queue.Queue[tuple[dict[str, Any], str]] = queue.Queue()
_WORKER_STARTED = False
_WORKER_LOCK = threading.Lock()


def _alert_worker() -> None:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook_url:
        logger.warning("DISCORD_WEBHOOK_URL not set; queued alerts will be dropped")

    while True:
        summary, target_url = _ALERT_QUEUE.get()
        try:
            if webhook_url:
                send_alert(webhook_url=webhook_url, summary=summary, target_url=target_url)
            else:
                logger.info("Dropped alert for %s because DISCORD_WEBHOOK_URL is missing", target_url)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Failed sending queued alert for %s: %s", target_url, exc)
        finally:
            _ALERT_QUEUE.task_done()
            time.sleep(1.0)  # max 1 msg/sec


def _ensure_worker_started() -> None:
    global _WORKER_STARTED
    if _WORKER_STARTED:
        return

    with _WORKER_LOCK:
        if _WORKER_STARTED:
            return
        thread = threading.Thread(target=_alert_worker, name="discord-alert-worker", daemon=True)
        thread.start()
        _WORKER_STARTED = True
        logger.info("Started Discord alert queue worker thread")


def enqueue_alert(summary: dict[str, Any], target_url: str) -> None:
    """Add an alert to the async queue and ensure worker is running."""
    _ensure_worker_started()
    _ALERT_QUEUE.put((summary, target_url))
    logger.info("Queued alert for %s", target_url)

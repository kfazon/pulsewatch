"""Capture utilities for PulseWatch PoC Week 1."""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Dict

from playwright.sync_api import sync_playwright

from storage import capture_directory_for_url, save_capture_artifacts


DEFAULT_TIMEOUT_MS = 30000
logger = logging.getLogger(__name__)


def capture_html_and_screenshot(url: str, output_dir: Path) -> Dict[str, str]:
    """Capture page HTML and full-page screenshot for a URL.

    Args:
        url: Target URL to capture.
        output_dir: Directory where artifacts are saved.

    Returns:
        Dict containing captured html and screenshot_path.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = output_dir / "screenshot.png"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto(url, wait_until="networkidle", timeout=DEFAULT_TIMEOUT_MS)
            html = page.content()
            page.screenshot(path=str(screenshot_path), full_page=True)
        finally:
            context.close()
            browser.close()

    return {"html": html, "screenshot_path": str(screenshot_path)}


def capture_batch(urls: list[str], output_dir: str = "data") -> dict:
    """Capture and persist artifacts for a list of URLs with retries.

    Retries each failed URL up to 2 additional times with linear backoff.
    Continues processing after failures and returns summary details.
    """
    total = len(urls)
    captured_count = 0
    failed: list[str] = []

    for url in urls:
        max_attempts = 3  # initial + 2 retries
        success = False

        for attempt in range(1, max_attempts + 1):
            try:
                capture_dir = capture_directory_for_url(url, base_dir=Path(output_dir))
                captured = capture_html_and_screenshot(url, capture_dir)
                save_capture_artifacts(
                    capture_dir=Path(capture_dir),
                    url=url,
                    html=captured["html"],
                    screenshot_path=captured["screenshot_path"],
                )
                captured_count += 1
                success = True
                break
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "Capture failed for %s (attempt %s/%s): %s",
                    url,
                    attempt,
                    max_attempts,
                    exc,
                )
                if attempt < max_attempts:
                    time.sleep(attempt)

        if not success:
            failed.append(url)
            logger.error("Capture failed after retries for %s", url)

    return {
        "captured": captured_count,
        "total": total,
        "failed": failed,
    }

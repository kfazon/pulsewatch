"""Capture utilities for PulseWatch PoC Week 1."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from playwright.sync_api import sync_playwright


DEFAULT_TIMEOUT_MS = 30000


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

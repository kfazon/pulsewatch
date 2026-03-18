"""Filesystem storage helpers for PulseWatch PoC Week 1."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


def _sanitize_domain(domain: str) -> str:
    return domain.replace(":", "_")


def capture_directory_for_url(url: str, base_dir: Path | None = None) -> Path:
    """Build capture directory path as data/{domain}/{date}/{page_hash}."""
    base = base_dir or Path("data")
    parsed = urlparse(url)
    domain = _sanitize_domain(parsed.netloc or "unknown")
    date_str = datetime.now().strftime("%Y-%m-%d")
    page_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    return base / domain / date_str / page_hash


def save_capture_artifacts(capture_dir: Path, url: str, html: str, screenshot_path: str) -> dict:
    """Persist HTML and metadata in the capture directory."""
    capture_dir.mkdir(parents=True, exist_ok=True)

    html_path = capture_dir / "page.html"
    html_path.write_text(html, encoding="utf-8")

    metadata = {
        "url": url,
        "captured_at": datetime.now().isoformat(timespec="seconds"),
        "html_path": str(html_path),
        "screenshot_path": screenshot_path,
    }
    metadata_path = capture_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return {
        "capture_dir": str(capture_dir),
        "html_path": str(html_path),
        "screenshot_path": screenshot_path,
        "metadata_path": str(metadata_path),
    }

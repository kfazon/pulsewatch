"""Basic text diff utilities for PulseWatch PoC Week 1."""

from __future__ import annotations

import difflib
from pathlib import Path


HTML_FILENAME = "page.html"


def diff_capture_dirs(old_dir: Path, new_dir: Path) -> dict:
    """Compare two capture directories and write a unified diff.

    Args:
        old_dir: Directory containing old capture artifacts.
        new_dir: Directory containing new capture artifacts.

    Returns:
        Dict with changed_lines_count and diff_path.
    """
    old_html_path = old_dir / HTML_FILENAME
    new_html_path = new_dir / HTML_FILENAME

    old_lines = old_html_path.read_text(encoding="utf-8").splitlines()
    new_lines = new_html_path.read_text(encoding="utf-8").splitlines()

    unified = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=str(old_html_path),
            tofile=str(new_html_path),
            lineterm="",
        )
    )

    changed_lines_count = sum(
        1
        for line in unified
        if (line.startswith("+") and not line.startswith("+++"))
        or (line.startswith("-") and not line.startswith("---"))
    )
    diff_path = new_dir / "diff.txt"
    diff_path.write_text("\n".join(unified) + ("\n" if unified else ""), encoding="utf-8")

    return {"changed_lines_count": changed_lines_count, "diff_path": str(diff_path)}

"""PulseWatch executive report generation."""

from typing import Any

__all__ = ["render_report"]


def __getattr__(name: str) -> Any:
    """Load the renderer lazily so ``python -m reports.render`` stays clean."""
    if name == "render_report":
        from reports.render import render_report

        return render_report
    raise AttributeError(name)

from pathlib import Path

LANDING = Path(__file__).resolve().parents[1] / "public-landing" / "index.html"


def test_landing_uses_current_early_access_status() -> None:
    html = LANDING.read_text(encoding="utf-8")

    assert "Early Access" in html
    assert "Launching Q2 2026" not in html
    assert "Q2 2026" not in html

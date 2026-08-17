from __future__ import annotations

import json
from pathlib import Path

from pypdf import PdfReader

from reports.render import render_json, render_report

EXAMPLE = Path("reports/examples/grama_market_pulse.json")
BAT_EXAMPLE = Path("reports/examples/bat_market_pulse.json")


def test_example_report_renders_pdf(tmp_path: Path) -> None:
    output = tmp_path / "report.pdf"

    result = render_json(EXAMPLE, output)

    assert result == output
    assert output.read_bytes().startswith(b"%PDF-")
    assert output.stat().st_size > 20_000

    reader = PdfReader(output)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 6
    assert reader.metadata.title == "GRAMA MARKET PULSE"
    assert reader.metadata.author.startswith("INMAR društvo")
    assert "Izvršni sažetak" in text
    assert "Povjerljivi digitalni signal" in text
    assert "Čakovec" in text
    assert "IZRADIO I IZDAJE" in text
    assert "INMAR društvo s ograničenom odgovornošću" in text
    assert "OIB: 33281217245" in text
    assert "MBS: 070096926" in text
    assert "Kristijan Fažon" in text
    assert "+385 91 45 46 013" in text


def test_report_supports_croatian_unicode(tmp_path: Path) -> None:
    payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    payload["title"] = "Čakovec — tržišni izvještaj"
    output = tmp_path / "unicode.pdf"

    render_report(payload, output)

    assert output.exists()
    assert output.stat().st_size > 20_000


def test_bat_example_report_renders_six_page_pdf(tmp_path: Path) -> None:
    output = tmp_path / "bat-report.pdf"

    render_json(BAT_EXAMPLE, output)

    reader = PdfReader(output)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 6
    assert reader.metadata.title == "BAT MARKET PULSE"
    assert reader.metadata.author.startswith("INMAR društvo")
    assert "Rudolfa Steinera 2" in text
    assert "Narančasta subota" in text
    assert "Dva prioritetna konkurenta" in text
    assert "Ovo je početni baseline" in text


def test_report_render_is_byte_stable(tmp_path: Path) -> None:
    first = tmp_path / "first.pdf"
    second = tmp_path / "second.pdf"

    render_json(BAT_EXAMPLE, first)
    render_json(BAT_EXAMPLE, second)

    assert first.read_bytes() == second.read_bytes()

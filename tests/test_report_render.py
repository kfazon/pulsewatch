from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader

from reports.render import render_json, render_report

EXAMPLE = Path("reports/examples/grama_market_pulse.json")
BAT_EXAMPLE = Path("reports/examples/bat_market_pulse.json")


def _pages(output: Path) -> list[str]:
    return [page.extract_text() or "" for page in PdfReader(output).pages]


def test_grama_v2_report_renders_decision_first_pdf(tmp_path: Path) -> None:
    output = tmp_path / "grama.pdf"
    assert render_json(EXAMPLE, output) == output
    reader = PdfReader(output)
    pages = _pages(output)
    text = "\n".join(pages)
    assert output.read_bytes().startswith(b"%PDF-")
    assert 6 <= len(reader.pages) <= 8
    assert reader.metadata.title == "GRAMA MARKET PULSE"
    assert reader.metadata.author == "INMAR d.o.o."
    assert "Najvažnije odluke" in text
    assert "ŠTO SMO VIDJELI" in text
    assert "ZAŠTO JE VAŽNO — NAŠA PROCJENA" in text
    assert "Kako ćemo mjeriti korist pilota" in text
    assert "Tko treba što napraviti" in text
    assert "Povjerljivi digitalni signal" in text
    assert "Prijedlog probnog rada — 30 dana" in text
    assert "Konačna cijena: 1.500 €" in text
    assert "INMAR d.o.o. nije u sustavu PDV-a" in text
    assert "+ PDV" not in text


def test_cover_limits_publisher_identifiers_and_later_has_full_block(
    tmp_path: Path,
) -> None:
    output = tmp_path / "cover.pdf"
    render_json(BAT_EXAMPLE, output)
    pages = _pages(output)
    cover = pages[0]
    later = "\n".join(pages[1:])
    assert "INMAR d.o.o." in cover
    assert "Gardinovec 24, 40319 Belica, Hrvatska" in cover
    assert "Kristijan Fažon — direktor i odgovorna osoba" in cover
    assert "Pripremljeno za:" in cover
    for forbidden in (
        "OIB",
        "MBS",
        "MB DZS",
        "@",
        "+385",
        "https://",
        "www.",
        "INMAR društvo s ograničenom odgovornošću",
    ):
        assert forbidden not in cover
    assert "OIB: 33281217245" in later
    assert "MBS: 070096926" in later
    assert "MB DZS: 02767392" in later
    assert "info@inmar.hr" in later
    assert "+385 91 45 46 013" in later
    assert "https://inmar.hr" in later
    assert "INMAR društvo s ograničenom odgovornošću" in later


def test_bat_v2_marks_pevex_primary_and_bauhaus_blocked(tmp_path: Path) -> None:
    output = tmp_path / "bat.pdf"
    render_json(BAT_EXAMPLE, output)
    text = "\n".join(_pages(output))
    assert 6 <= len(PdfReader(output).pages) <= 8
    assert "PEVEX Čakovec" in text
    assert "glavni lokalni konkurent" in text
    assert "BAUHAUS Varaždin" in text
    assert "sekundaran / blokiran" in text
    assert "Ovo je početno stanje" in text
    assert "detected change" not in text


def test_report_supports_croatian_unicode(tmp_path: Path) -> None:
    payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    payload["title"] = "Čakovec — tržišni izvještaj"
    output = tmp_path / "unicode.pdf"
    render_report(payload, output)
    assert output.exists()
    assert output.stat().st_size > 20_000


def test_report_render_is_byte_stable(tmp_path: Path) -> None:
    first = tmp_path / "first.pdf"
    second = tmp_path / "second.pdf"
    render_json(BAT_EXAMPLE, first)
    render_json(BAT_EXAMPLE, second)
    assert first.read_bytes() == second.read_bytes()


def test_module_cli_renders_pdf(tmp_path: Path) -> None:
    output = tmp_path / "cli.pdf"
    subprocess.run(
        [sys.executable, "-m", "reports.render", str(BAT_EXAMPLE), str(output)],
        check=True,
    )
    assert output.read_bytes().startswith(b"%PDF-")

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

from brochures.render import render_json

BROCHURE = Path("brochures/pulsewatch_client_brochure_hr.json")


def test_client_brochure_renders_six_page_pdf(tmp_path: Path) -> None:
    output = tmp_path / "pulsewatch-brochure.pdf"

    result = render_json(BROCHURE, output)

    assert result == output
    assert output.read_bytes().startswith(b"%PDF-")
    assert output.stat().st_size > 20_000

    reader = PdfReader(output)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 6
    assert reader.metadata.title == "PulseWatch — paketi upravljanog tržišnog nadzora"
    assert reader.metadata.author.startswith("INMAR društvo")
    assert "30-dnevni pilot" in text
    assert "1.500 €" in text
    assert "Managed Plus" in text
    assert "2.490 € / mj." in text
    assert "+ PDV" not in text
    assert "PDV nije obračunat sukladno članku 90. stavku 2." in text
    assert "Kristijan Fažon" in text
    assert "OIB: 33281217245" in text
    assert "Gardinovec 24" in text

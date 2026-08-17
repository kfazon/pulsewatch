"""Deterministic v2 PulseWatch client-report PDF renderer."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 17 * mm
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN
NAVY, BLUE, TEAL = (
    colors.HexColor("#10243E"),
    colors.HexColor("#176B87"),
    colors.HexColor("#21A0A0"),
)
INK, MUTED, LINE = (
    colors.HexColor("#152936"),
    colors.HexColor("#60717B"),
    colors.HexColor("#D9E2E7"),
)
SURFACE, PALE_TEAL, WHITE = (
    colors.HexColor("#F4F7F9"),
    colors.HexColor("#EAF6F5"),
    colors.white,
)
PRIORITY = {
    "P0": colors.HexColor("#A72525"),
    "P1": colors.HexColor("#B35F00"),
    "P2": BLUE,
}


def _register_fonts() -> None:
    for directory in [
        Path(__import__("reportlab").__file__).parent / "fonts",
        Path(rl_config.TTFSearchPath[0]),
    ]:
        regular, bold, italic = (
            directory / "Vera.ttf",
            directory / "VeraBd.ttf",
            directory / "VeraIt.ttf",
        )
        if regular.exists() and bold.exists() and italic.exists():
            pdfmetrics.registerFont(TTFont("PW-Regular", regular))
            pdfmetrics.registerFont(TTFont("PW-Bold", bold))
            pdfmetrics.registerFont(TTFont("PW-Italic", italic))
            pdfmetrics.registerFontFamily(
                "PW", normal="PW-Regular", bold="PW-Bold", italic="PW-Italic"
            )
            return
    raise RuntimeError("ReportLab Vera fonts were not found")


def _safe(value: Any) -> str:
    return html.escape(str(value), quote=False).replace("\n", "<br/>")


def _styles() -> dict[str, ParagraphStyle]:
    return {
        "body": ParagraphStyle(
            "body",
            fontName="PW-Regular",
            fontSize=9.2,
            leading=13.2,
            textColor=INK,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "small", fontName="PW-Regular", fontSize=8, leading=9.6, textColor=INK
        ),
        "label": ParagraphStyle(
            "label", fontName="PW-Bold", fontSize=8.1, leading=10, textColor=MUTED
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName="PW-Bold",
            fontSize=22,
            leading=27,
            textColor=NAVY,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName="PW-Bold",
            fontSize=15,
            leading=19,
            textColor=BLUE,
            spaceAfter=7,
        ),
        "h3": ParagraphStyle(
            "h3",
            fontName="PW-Bold",
            fontSize=10.4,
            leading=13,
            textColor=NAVY,
            spaceAfter=3,
        ),
        "cover_brand": ParagraphStyle(
            "cover_brand",
            fontName="PW-Bold",
            fontSize=12,
            leading=15,
            textColor=TEAL,
            alignment=TA_CENTER,
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName="PW-Bold",
            fontSize=29,
            leading=34,
            textColor=WHITE,
            alignment=TA_CENTER,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            fontName="PW-Regular",
            fontSize=11.5,
            leading=16,
            textColor=WHITE,
            alignment=TA_CENTER,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            fontName="PW-Regular",
            fontSize=9,
            leading=13,
            textColor=INK,
            alignment=TA_CENTER,
        ),
        "source": ParagraphStyle(
            "source",
            fontName="PW-Regular",
            fontSize=8.1,
            leading=10.5,
            textColor=MUTED,
            spaceAfter=3,
        ),
        "chip": ParagraphStyle(
            "chip", fontName="PW-Bold", fontSize=8.1, leading=10, alignment=TA_CENTER
        ),
    }


def _page_header_footer(canvas, doc) -> None:
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(TEAL)
        canvas.setLineWidth(1.2)
        canvas.line(
            MARGIN, PAGE_HEIGHT - 13 * mm, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 13 * mm
        )
        canvas.setFont("PW-Bold", 8)
        canvas.setFillColor(NAVY)
        canvas.drawString(MARGIN, PAGE_HEIGHT - 10 * mm, "PULSEWATCH")
        canvas.setFont("PW-Regular", 8)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(
            PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 10 * mm, str(doc.report_label)
        )
        canvas.setStrokeColor(LINE)
        canvas.line(MARGIN, 12 * mm, PAGE_WIDTH - MARGIN, 12 * mm)
        canvas.setFont("PW-Regular", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN, 8 * mm, str(doc.footer_text))
        canvas.drawRightString(PAGE_WIDTH - MARGIN, 8 * mm, str(doc.page))
    canvas.restoreState()


def _section(title: str, styles: dict[str, ParagraphStyle]) -> list[Any]:
    return [
        Paragraph(_safe(title), styles["h2"]),
        HRFlowable(width="100%", thickness=1.2, color=TEAL),
        Spacer(1, 6),
    ]


def _cover(data: dict[str, Any], styles: dict[str, ParagraphStyle]) -> list[Any]:
    box = Table(
        [
            [Paragraph("PULSEWATCH", styles["cover_brand"])],
            [Spacer(1, 6)],
            [Paragraph(_safe(data["title"]), styles["cover_title"])],
            [Spacer(1, 5)],
            [Paragraph(_safe(data["subtitle"]), styles["cover_subtitle"])],
        ],
        colWidths=[CONTENT_WIDTH],
        rowHeights=[14 * mm, 5 * mm, 35 * mm, 4 * mm, 23 * mm],
    )
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ]
        )
    )
    meta, publisher = data["meta"], data["publisher"]
    # Cover must contain exactly the three permitted publisher identifiers.
    publisher_text = "<br/>".join(
        [
            "<b>INMAR d.o.o.</b>",
            _safe(publisher["address"]),
            "Kristijan Fažon — direktor i odgovorna osoba",
        ]
    )
    identity = Table(
        [
            [Paragraph("IZRADIO I IZDAJE", styles["label"])],
            [Paragraph(publisher_text, styles["cover_meta"])],
        ],
        colWidths=[CONTENT_WIDTH * 0.72],
        hAlign="CENTER",
    )
    identity.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return [
        Spacer(1, 20 * mm),
        box,
        Spacer(1, 11 * mm),
        Paragraph(
            f"<b>Pripremljeno za:</b> {_safe(meta['prepared_for'])}",
            styles["cover_meta"],
        ),
        Paragraph(f"<b>Datum:</b> {_safe(meta['date'])}", styles["cover_meta"]),
        Paragraph(f"<b>Status:</b> {_safe(meta['status'])}", styles["cover_meta"]),
        Spacer(1, 8 * mm),
        identity,
        Spacer(1, 8 * mm),
        HRFlowable(width="32%", thickness=3, color=TEAL, hAlign="CENTER"),
        Spacer(1, 6 * mm),
        Paragraph(_safe(data["tagline"]), styles["cover_meta"]),
        PageBreak(),
    ]


def _card(
    title: str,
    blocks: list[tuple[str, str]],
    styles: dict[str, ParagraphStyle],
    priority: str = "P2",
) -> KeepTogether:
    accent = PRIORITY.get(priority, TEAL)
    content: list[Any] = [Paragraph(_safe(title), styles["h3"])]
    for label, text in blocks:
        content.extend(
            [
                Paragraph(_safe(label).upper(), styles["label"]),
                Paragraph(_safe(text), styles["small"]),
                Spacer(1, 3),
            ]
        )
    table = Table(
        [
            [
                Paragraph(
                    priority,
                    ParagraphStyle(
                        f"priority-{priority}", parent=styles["chip"], textColor=accent
                    ),
                ),
                content,
            ]
        ],
        colWidths=[17 * mm, CONTENT_WIDTH - 17 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), SURFACE),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("LINEBEFORE", (0, 0), (0, 0), 3, accent),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return KeepTogether([table, Spacer(1, 7)])


def _decision_card(
    item: dict[str, Any], styles: dict[str, ParagraphStyle]
) -> KeepTogether:
    return _card(
        item["title"],
        [
            ("Što smo vidjeli", item["fact_observation"]),
            ("Dokaz", f"{item['evidence']} · {item['confidence']}"),
            ("Zašto je važno — naša procjena", item["business_hypothesis"]),
            ("Što treba napraviti", item["recommendation"]),
            ("Tko · do kada", f"{item['owner']} · {item['due_date']}"),
            (
                "Kako mjeriti",
                f"sada: {item['kpi_baseline']} | cilj: {item['kpi_target']}",
            ),
            (
                "Što još ne znamo",
                f"{item['limitation']} Usporedba: {item['entity_sku_match']}",
            ),
        ],
        styles,
        item.get("priority", "P2"),
    )


def _action_register(
    items: list[dict[str, Any]], styles: dict[str, ParagraphStyle]
) -> Table:
    header = ["Važnost / stanje", "Što treba napraviti", "Kako znamo da je gotovo"]
    rows: list[list[Any]] = [[Paragraph(x, styles["label"]) for x in header]]
    for item in items:
        rows.append(
            [
                Paragraph(
                    f"<b>{_safe(item['priority'])}</b><br/>{_safe(item['status'])}",
                    styles["small"],
                ),
                Paragraph(
                    f"<b>{_safe(item['action'])}</b><br/>"
                    f"{_safe(item['owner'])} · {_safe(item['due_date'])}",
                    styles["small"],
                ),
                Paragraph(
                    f"<b>Sada:</b> {_safe(item['kpi_baseline'])}<br/>"
                    f"<b>Cilj:</b> {_safe(item['kpi_target'])}<br/>"
                    f"<b>Dokaz:</b> {_safe(item['evidence'])}",
                    styles["small"],
                ),
            ]
        )
    table = Table(rows, colWidths=[25 * mm, 78 * mm, 67 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, -1), WHITE),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def _scorecard(items: list[dict[str, Any]], styles: dict[str, ParagraphStyle]) -> Table:
    rows = [
        [
            Paragraph(x, styles["label"])
            for x in ["Što mjerimo", "Sada", "Cilj pilota", "Kako dokazujemo"]
        ]
    ]
    for item in items:
        rows.append(
            [
                Paragraph(_safe(item["metric"]), styles["small"]),
                Paragraph(_safe(item["baseline"]), styles["small"]),
                Paragraph(_safe(item["target"]), styles["small"]),
                Paragraph(_safe(item["evidence"]), styles["small"]),
            ]
        )
    table = Table(rows, colWidths=[39 * mm, 38 * mm, 47 * mm, 46 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PALE_TEAL),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _publisher_detail(
    publisher: dict[str, Any], styles: dict[str, ParagraphStyle]
) -> Table:
    text = "<br/>".join(
        [
            f"<b>{_safe(publisher['legal_name'])}</b>",
            _safe(publisher["address"]),
            f"OIB: {_safe(publisher['oib'])} · MBS: {_safe(publisher['mbs'])} · MB DZS: {_safe(publisher['mb_dzs'])}",
            _safe(publisher["registry_court"]),
            f"Direktor i odgovorna osoba: {_safe(publisher['director'])}",
            f"{_safe(publisher['email'])} · {_safe(publisher['phone'])} · {_safe(publisher['website'])}",
        ]
    )
    table = Table(
        [
            [Paragraph("IZDAVATELJ", styles["label"])],
            [Paragraph(text, styles["small"])],
        ],
        colWidths=[CONTENT_WIDTH],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def render_report(data: dict[str, Any], output_path: str | Path) -> Path:
    """Render a v2 report payload deterministically and return its PDF path."""
    rl_config.invariant = 1
    _register_fonts()
    styles = _styles()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    story: list[Any] = _cover(data, styles)
    story.extend(_section("1. Najvažnije odluke", styles))
    story.append(Paragraph(_safe(data["executive_intro"]), styles["body"]))
    for item in data["decision_brief"][:3]:
        story.append(_decision_card(item, styles))
    story.append(
        KeepTogether(
            [
                *_section("2. Kako ćemo mjeriti korist pilota", styles),
                Paragraph(_safe(data["value_intro"]), styles["body"]),
                _scorecard(data["value_scorecard"], styles),
            ]
        )
    )
    story.append(Spacer(1, 8))
    story.append(Paragraph(_safe(data["baseline_notice"]), styles["body"]))
    story.extend(_section("3. Tko treba što napraviti", styles))
    story.append(Paragraph(_safe(data["actions_intro"]), styles["body"]))
    story.append(_action_register(data["actions"][:3], styles))
    first_monitoring, *remaining_monitoring = data["monitoring"]
    story.append(
        KeepTogether(
            [
                *_section("4. Što pratimo", styles),
                Paragraph(_safe(data["positioning_conclusion"]), styles["body"]),
            ]
        )
    )
    story.append(
        _card(
            first_monitoring["title"],
            [
                ("Sadašnje stanje", first_monitoring["baseline"]),
                ("Što provjeravamo", first_monitoring["monitor"]),
            ],
            styles,
        )
    )
    for item in remaining_monitoring:
        story.append(
            _card(
                item["title"],
                [
                    ("Sadašnje stanje", item["baseline"]),
                    ("Što provjeravamo", item["monitor"]),
                ],
                styles,
            )
        )
    story.append(PageBreak())
    story.extend(_section("5. Konkurenti — što je važno pratiti", styles))
    story.append(Paragraph(_safe(data["competitor_intro"]), styles["body"]))
    for item in data["competitors"]:
        story.append(
            _card(
                item["name"],
                [
                    ("Što smo javno potvrdili", item["signal"]),
                    ("Koliko je potvrđeno", item.get("status", "potvrđeno")),
                    ("Što predlažemo", item["response"]),
                ],
                styles,
            )
        )
    if data.get("confidential"):
        story.append(Spacer(1, 6))
        story.extend(_section("6. Povjerljivi digitalni signal", styles))
        confidential = data["confidential"]
        story.append(Paragraph(_safe(confidential["finding"]), styles["body"]))
        story.append(Paragraph("Potvrđeno / opaženo", styles["h3"]))
        for item in confidential["known"]:
            story.append(Paragraph(f"• {_safe(item)}", styles["small"]))
        story.append(Paragraph("Nije dokazano", styles["h3"]))
        for item in confidential["unknown"]:
            story.append(Paragraph(f"• {_safe(item)}", styles["small"]))
    story.append(PageBreak())
    number = 7 if data.get("confidential") else 6
    story.extend(_section(f"{number}. Prijedlog probnog rada — 30 dana", styles))
    offer = data["offer"]
    story.append(Paragraph(_safe(offer["intro"]), styles["body"]))
    story.append(
        _card(
            "30 dana · prijedlog",
            [
                ("Što je uključeno", offer["scope"]),
                ("Koliko često provjeravamo", offer["cadence"]),
                ("Kada je pilot uspješan", offer["acceptance_kpi"]),
                ("Cijena", offer["price"]),
                ("Što pilot ne može dokazati", offer["limitation"]),
            ],
            styles,
            "P1",
        )
    )
    story.append(PageBreak())
    story.extend(_section(f"{number + 1}. Metodologija, izvori i izdavatelj", styles))
    for item in data["methodology"]:
        story.append(Paragraph(f"• {_safe(item)}", styles["small"]))
    story.append(Spacer(1, 6))
    story.append(_publisher_detail(data["publisher"], styles))
    story.append(Spacer(1, 7))
    story.append(Paragraph("Glavni javni izvori", styles["h3"]))
    for index, source in enumerate(data["sources"], 1):
        story.append(
            Paragraph(
                f"{index}. {_safe(source['label'])}<br/><font color='#176B87'>{_safe(source['url'])}</font>",
                styles["source"],
            )
        )
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=17 * mm,
        bottomMargin=16 * mm,
        title=str(data["title"]),
        author="INMAR d.o.o.",
        subject=str(data["subtitle"]),
    )
    doc.report_label = data["meta"].get("label", "DEMO · PUBLIC SOURCES ONLY")
    doc.footer_text = data["meta"].get("footer", "PulseWatch · demonstracijski pilot")
    doc.build(story, onFirstPage=_page_header_footer, onLaterPages=_page_header_footer)
    return output


def render_json(input_path: str | Path, output_path: str | Path) -> Path:
    return render_report(
        json.loads(Path(input_path).read_text(encoding="utf-8")), output_path
    )


def main() -> None:
    """Render one JSON report payload from the command line."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON payload path")
    parser.add_argument("output", type=Path, help="PDF output path")
    args = parser.parse_args()
    render_json(args.input, args.output)


if __name__ == "__main__":
    main()

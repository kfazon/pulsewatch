"""Render a structured PulseWatch executive report as a branded PDF."""

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

NAVY = colors.HexColor("#10243E")
BLUE = colors.HexColor("#176B87")
TEAL = colors.HexColor("#21A0A0")
INK = colors.HexColor("#152936")
MUTED = colors.HexColor("#60717B")
LINE = colors.HexColor("#D9E2E7")
SURFACE = colors.HexColor("#F4F7F9")
PALE_TEAL = colors.HexColor("#EAF6F5")
WHITE = colors.white

SEVERITY = {
    "critical": ("KRITIČNO", colors.HexColor("#A72525"), colors.HexColor("#FCEBEC")),
    "high": ("VISOKO", colors.HexColor("#B35F00"), colors.HexColor("#FFF2DF")),
    "medium": ("SREDNJE", colors.HexColor("#48637A"), colors.HexColor("#EAF0F5")),
    "low": ("NISKO", colors.HexColor("#2D6A4F"), colors.HexColor("#E8F4ED")),
}


def _register_fonts() -> None:
    """Use ReportLab-bundled Unicode fonts for reproducible output."""
    font_dir = Path(rl_config.TTFSearchPath[0])
    candidates = [
        Path(__import__("reportlab").__file__).parent / "fonts",
        font_dir,
    ]
    for directory in candidates:
        regular = directory / "Vera.ttf"
        bold = directory / "VeraBd.ttf"
        italic = directory / "VeraIt.ttf"
        if regular.exists() and bold.exists() and italic.exists():
            pdfmetrics.registerFont(TTFont("PW-Regular", regular))
            pdfmetrics.registerFont(TTFont("PW-Bold", bold))
            pdfmetrics.registerFont(TTFont("PW-Italic", italic))
            pdfmetrics.registerFontFamily(
                "PW",
                normal="PW-Regular",
                bold="PW-Bold",
                italic="PW-Italic",
            )
            return
    raise RuntimeError("ReportLab Vera fonts were not found")


def _safe(value: Any) -> str:
    text = html.escape(str(value), quote=False)
    return text.replace("\n", "<br/>")


def _styles() -> dict[str, ParagraphStyle]:
    return {
        "body": ParagraphStyle(
            "PWBody",
            fontName="PW-Regular",
            fontSize=9.2,
            leading=13.8,
            textColor=INK,
            spaceAfter=7,
        ),
        "body_small": ParagraphStyle(
            "PWBodySmall",
            fontName="PW-Regular",
            fontSize=8.6,
            leading=12.2,
            textColor=INK,
        ),
        "label": ParagraphStyle(
            "PWLabel",
            fontName="PW-Bold",
            fontSize=7.3,
            leading=9,
            textColor=MUTED,
            spaceAfter=2,
        ),
        "h1": ParagraphStyle(
            "PWH1",
            fontName="PW-Bold",
            fontSize=22,
            leading=27,
            textColor=NAVY,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "PWH2",
            fontName="PW-Bold",
            fontSize=15,
            leading=19,
            textColor=BLUE,
            spaceAfter=7,
        ),
        "h3": ParagraphStyle(
            "PWH3",
            fontName="PW-Bold",
            fontSize=10.8,
            leading=14,
            textColor=NAVY,
            spaceAfter=4,
        ),
        "cover_brand": ParagraphStyle(
            "PWCoverBrand",
            fontName="PW-Bold",
            fontSize=12,
            leading=15,
            textColor=TEAL,
            alignment=TA_CENTER,
        ),
        "cover_title": ParagraphStyle(
            "PWCoverTitle",
            fontName="PW-Bold",
            fontSize=31,
            leading=35,
            textColor=WHITE,
            alignment=TA_CENTER,
        ),
        "cover_subtitle": ParagraphStyle(
            "PWCoverSubtitle",
            fontName="PW-Regular",
            fontSize=12,
            leading=17,
            textColor=WHITE,
            alignment=TA_CENTER,
        ),
        "cover_meta": ParagraphStyle(
            "PWCoverMeta",
            fontName="PW-Regular",
            fontSize=9,
            leading=14,
            textColor=INK,
            alignment=TA_CENTER,
        ),
        "publisher": ParagraphStyle(
            "PWPublisher",
            fontName="PW-Regular",
            fontSize=7.8,
            leading=10.6,
            textColor=INK,
            alignment=TA_CENTER,
        ),
        "source": ParagraphStyle(
            "PWSource",
            fontName="PW-Regular",
            fontSize=8,
            leading=11,
            textColor=MUTED,
            spaceAfter=4,
        ),
        "chip": ParagraphStyle(
            "PWChip",
            fontName="PW-Bold",
            fontSize=7.4,
            leading=8.8,
            alignment=TA_CENTER,
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
        canvas.setFont("PW-Bold", 7.5)
        canvas.setFillColor(NAVY)
        canvas.drawString(MARGIN, PAGE_HEIGHT - 10 * mm, "PULSEWATCH")
        canvas.setFont("PW-Regular", 6.7)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(
            PAGE_WIDTH - MARGIN,
            PAGE_HEIGHT - 10 * mm,
            str(doc.report_label),
        )
    canvas.setStrokeColor(LINE)
    canvas.line(MARGIN, 12 * mm, PAGE_WIDTH - MARGIN, 12 * mm)
    canvas.setFont("PW-Regular", 6.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 8 * mm, str(doc.footer_text))
    canvas.drawRightString(PAGE_WIDTH - MARGIN, 8 * mm, str(doc.page))
    canvas.restoreState()


def _section_title(title: str, styles: dict[str, ParagraphStyle]) -> list[Any]:
    return [
        Paragraph(_safe(title), styles["h2"]),
        HRFlowable(width="100%", thickness=1.2, color=TEAL),
        Spacer(1, 7),
    ]


def _cover(data: dict[str, Any], styles: dict[str, ParagraphStyle]) -> list[Any]:
    title_box = Table(
        [
            [Paragraph("PULSEWATCH", styles["cover_brand"])],
            [Spacer(1, 7)],
            [Paragraph(_safe(data["title"]), styles["cover_title"])],
            [Spacer(1, 5)],
            [Paragraph(_safe(data["subtitle"]), styles["cover_subtitle"])],
        ],
        colWidths=[CONTENT_WIDTH],
        rowHeights=[15 * mm, 5 * mm, 36 * mm, 4 * mm, 23 * mm],
    )
    title_box.setStyle(
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
    meta = data["meta"]
    cover: list[Any] = [
        Spacer(1, 20 * mm),
        title_box,
        Spacer(1, 12 * mm),
        Paragraph(f"<b>Klijent:</b> {_safe(meta['client'])}", styles["cover_meta"]),
        Paragraph(f"<b>Datum:</b> {_safe(meta['date'])}", styles["cover_meta"]),
        Paragraph(f"<b>Status:</b> {_safe(meta['status'])}", styles["cover_meta"]),
    ]

    publisher = data.get("publisher")
    if publisher:
        publisher_lines = [
            f"<b>{_safe(publisher['legal_name'])}</b>",
            _safe(publisher["address"]),
            f"OIB: {_safe(publisher['oib'])} · MBS: {_safe(publisher['mbs'])}",
            f"{_safe(publisher['registry_court'])} · MB DZS: {_safe(publisher['mb_dzs'])}",
            f"Direktor: {_safe(publisher['director'])}",
            f"{_safe(publisher['email'])} · {_safe(publisher['phone'])}",
            _safe(publisher["website"]),
        ]
        publisher_box = Table(
            [
                [Paragraph("IZRADIO I IZDAJE", styles["label"])],
                [Paragraph("<br/>".join(publisher_lines), styles["publisher"])],
            ],
            colWidths=[CONTENT_WIDTH * 0.72],
            hAlign="CENTER",
        )
        publisher_box.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
                    ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )
        cover.extend([Spacer(1, 8 * mm), publisher_box])

    cover.extend(
        [
            Spacer(1, 8 * mm),
            HRFlowable(width="32%", thickness=3, color=TEAL, hAlign="CENTER"),
            Spacer(1, 6 * mm),
            Paragraph(_safe(data["tagline"]), styles["cover_meta"]),
            PageBreak(),
        ]
    )
    return cover


def _severity_card(
    signal: dict[str, Any], styles: dict[str, ParagraphStyle]
) -> KeepTogether:
    key = str(signal.get("severity", "medium")).lower()
    label, accent, background = SEVERITY.get(key, SEVERITY["medium"])
    chip_style = ParagraphStyle(f"Chip-{key}", parent=styles["chip"], textColor=accent)
    title = Paragraph(_safe(signal["title"]), styles["h3"])
    details = Paragraph(
        f"<font color='#60717B'><b>NALAZ</b></font><br/>{_safe(signal['finding'])}"
        f"<br/><br/><font color='#60717B'><b>POSLOVNI UČINAK</b></font><br/>"
        f"{_safe(signal['impact'])}"
        f"<br/><br/><font color='#60717B'><b>PREPORUKA</b></font><br/>"
        f"{_safe(signal['action'])}",
        styles["body_small"],
    )
    card = Table(
        [[Paragraph(label, chip_style), [title, details]]],
        colWidths=[22 * mm, CONTENT_WIDTH - 22 * mm],
        hAlign="LEFT",
    )
    card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), background),
                ("BACKGROUND", (1, 0), (1, 0), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("LINEBEFORE", (0, 0), (0, 0), 3, accent),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return KeepTogether([card, Spacer(1, 8)])


def _two_column_lists(
    left: dict[str, Any],
    right: dict[str, Any],
    styles: dict[str, ParagraphStyle],
) -> Table:
    def content(block: dict[str, Any]) -> list[Any]:
        items: list[Any] = [Paragraph(_safe(block["title"]), styles["h3"])]
        for item in block["items"]:
            items.append(Paragraph(f"• {_safe(item)}", styles["body_small"]))
            items.append(Spacer(1, 3))
        return items

    table = Table(
        [[content(left), content(right)]],
        colWidths=[CONTENT_WIDTH / 2 - 4, CONTENT_WIDTH / 2 - 4],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LINEBEFORE", (1, 0), (1, 0), 0.6, LINE),
            ]
        )
    )
    return table


def _competitor_card(
    item: dict[str, Any], styles: dict[str, ParagraphStyle]
) -> KeepTogether:
    name = Paragraph(_safe(item["name"]), styles["h3"])
    signal = Paragraph(
        f"<font color='#60717B'><b>JAVNI SIGNAL</b></font><br/>{_safe(item['signal'])}",
        styles["body_small"],
    )
    response = Paragraph(
        f"<font color='#60717B'><b>PREPORUČENI ODGOVOR</b></font><br/>"
        f"{_safe(item['response'])}",
        styles["body_small"],
    )
    card = Table(
        [[name], [Table([[signal, response]], colWidths=[CONTENT_WIDTH / 2 - 12] * 2)]],
        colWidths=[CONTENT_WIDTH],
        hAlign="LEFT",
    )
    card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PALE_TEAL),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return KeepTogether([card, Spacer(1, 8)])


def _action_card(
    item: dict[str, Any], styles: dict[str, ParagraphStyle]
) -> KeepTogether:
    key = str(item.get("priority", "P2"))
    accent = {"P0": colors.HexColor("#A72525"), "P1": BLUE}.get(key, TEAL)
    priority_style = ParagraphStyle(
        f"Priority-{key}", parent=styles["chip"], textColor=accent
    )
    text = Paragraph(
        f"<b>{_safe(item['action'])}</b><br/>"
        f"<font color='#60717B'>VLASNIK</font>  {_safe(item['owner'])}<br/>"
        f"<font color='#60717B'>DOKAZ ZAVRŠETKA</font>  {_safe(item['evidence'])}",
        styles["body_small"],
    )
    card = Table(
        [[Paragraph(key, priority_style), text]],
        colWidths=[18 * mm, CONTENT_WIDTH - 18 * mm],
    )
    card.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("BACKGROUND", (0, 0), (0, 0), SURFACE),
                ("LINEBEFORE", (0, 0), (0, 0), 3, accent),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return KeepTogether([card, Spacer(1, 7)])


def _monitor_grid(
    items: list[dict[str, Any]], styles: dict[str, ParagraphStyle]
) -> Table:
    cells: list[list[Any]] = []
    for item in items:
        cells.append(
            [
                Paragraph(_safe(item["title"]), styles["h3"]),
                Paragraph(
                    f"<font color='#60717B'><b>POČETNO STANJE</b></font><br/>"
                    f"{_safe(item['baseline'])}",
                    styles["body_small"],
                ),
                Spacer(1, 5),
                Paragraph(
                    f"<font color='#176B87'><b>PULSEWATCH PRATI</b></font><br/>"
                    f"{_safe(item['monitor'])}",
                    styles["body_small"],
                ),
            ]
        )

    rows: list[list[Any]] = []
    for index in range(0, len(cells), 2):
        row = [cells[index]]
        row.append(cells[index + 1] if index + 1 < len(cells) else [])
        rows.append(row)

    table = Table(rows, colWidths=[CONTENT_WIDTH / 2 - 4] * 2, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL),
                ("GRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def _offer_columns(data: dict[str, Any], styles: dict[str, ParagraphStyle]) -> Table:
    cells: list[list[Any]] = []
    for item in data["deliverables"]:
        cells.append(
            [
                Paragraph(_safe(item["title"]), styles["h3"]),
                Paragraph(_safe(item["description"]), styles["body_small"]),
            ]
        )
    rows: list[list[Any]] = []
    for index in range(0, len(cells), 2):
        row = [cells[index]]
        row.append(cells[index + 1] if index + 1 < len(cells) else [])
        rows.append(row)
    table = Table(rows, colWidths=[CONTENT_WIDTH / 2 - 4] * 2, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
                ("GRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return table


def render_report(data: dict[str, Any], output_path: str | Path) -> Path:
    """Render a report payload and return the created PDF path."""
    rl_config.invariant = 1
    _register_fonts()
    styles = _styles()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    story: list[Any] = []
    story.extend(_cover(data, styles))

    story.extend(_section_title("1. Izvršni sažetak", styles))
    story.append(Paragraph(_safe(data["executive_intro"]), styles["body"]))
    story.append(Spacer(1, 2))
    for signal in data["signals"]:
        story.append(_severity_card(signal, styles))

    story.append(PageBreak())
    story.extend(_section_title("2. Tržišna pozicija", styles))
    story.append(_two_column_lists(data["strengths"], data["gaps"], styles))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Zaključak", styles["h3"]))
    story.append(Paragraph(_safe(data["positioning_conclusion"]), styles["body"]))

    story.extend(_section_title("3. Konkurentski radar", styles))
    story.append(Paragraph(_safe(data["competitor_intro"]), styles["body"]))
    for item in data["competitors"]:
        story.append(_competitor_card(item, styles))

    story.append(PageBreak())
    story.extend(_section_title("4. Signali za kontinuirano praćenje", styles))
    story.append(_monitor_grid(data["monitoring"], styles))
    story.append(Spacer(1, 12))

    story.extend(_section_title("5. Preporučeni potezi", styles))
    story.append(Paragraph(_safe(data["actions_intro"]), styles["body"]))
    for item in data["actions"]:
        story.append(_action_card(item, styles))

    story.append(PageBreak())
    story.extend(_section_title("6. Predloženi PulseWatch pilot", styles))
    story.append(Paragraph(_safe(data["offer"]["intro"]), styles["body"]))
    story.append(_offer_columns(data["offer"], styles))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Kriterij uspjeha", styles["h3"]))
    story.append(Paragraph(_safe(data["offer"]["success"]), styles["body"]))

    confidential = data.get("confidential")
    if confidential:
        story.append(Spacer(1, 14))
        story.extend(_section_title("7. Povjerljivi digitalni signal", styles))
        story.append(
            Table(
                [[Paragraph("POVJERLJIVO", styles["chip"])]],
                colWidths=[30 * mm],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FCEBEC")),
                        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#A72525")),
                        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#A72525")),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                ),
            )
        )
        story.append(Spacer(1, 9))
        story.append(Paragraph(_safe(confidential["finding"]), styles["body"]))
        story.append(Paragraph("Što se smije zaključiti", styles["h3"]))
        for item in confidential["known"]:
            story.append(Paragraph(f"• {_safe(item)}", styles["body_small"]))
            story.append(Spacer(1, 3))
        story.append(Spacer(1, 6))
        story.append(Paragraph("Što nije dokazano", styles["h3"]))
        for item in confidential["unknown"]:
            story.append(Paragraph(f"• {_safe(item)}", styles["body_small"]))
            story.append(Spacer(1, 3))
        story.append(Spacer(1, 6))
        story.append(Paragraph("Siguran prvi odgovor", styles["h3"]))
        for index, item in enumerate(confidential["response"], start=1):
            story.append(Paragraph(f"{index}. {_safe(item)}", styles["body_small"]))
            story.append(Spacer(1, 3))

    story.append(PageBreak())
    section_number = 8 if confidential else 7
    story.extend(_section_title(f"{section_number}. Metodologija i izvori", styles))
    for item in data["methodology"]:
        story.append(Paragraph(f"• {_safe(item)}", styles["body_small"]))
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 9))
    story.append(Paragraph("Glavni javni izvori", styles["h3"]))
    for index, source in enumerate(data["sources"], start=1):
        story.append(
            Paragraph(
                f"{index}. {_safe(source['label'])}<br/>"
                f"<font color='#176B87'>{_safe(source['url'])}</font>",
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
        author=str(data.get("publisher", {}).get("legal_name", "PulseWatch")),
        subject=str(data["subtitle"]),
    )
    doc_any: Any = doc
    doc_any.report_label = data["meta"].get("label", "EXECUTIVE REPORT")
    publisher = data.get("publisher", {})
    doc_any.footer_text = data["meta"].get(
        "footer", f"PulseWatch · {publisher.get('legal_name', 'PulseWatch')}"
    )
    doc.build(
        story,
        onFirstPage=_page_header_footer,
        onLaterPages=_page_header_footer,
    )
    return output


def render_json(input_path: str | Path, output_path: str | Path) -> Path:
    """Load a JSON payload and render it as PDF."""
    payload = json.loads(Path(input_path).read_text(encoding="utf-8"))
    return render_report(payload, output_path)

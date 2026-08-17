"""Render the client-facing PulseWatch service brochure as PDF."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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

NAVY = colors.HexColor("#0C2038")
NAVY_2 = colors.HexColor("#173A57")
BLUE = colors.HexColor("#176B87")
TEAL = colors.HexColor("#21A0A0")
TEAL_DARK = colors.HexColor("#147A7A")
INK = colors.HexColor("#142936")
MUTED = colors.HexColor("#61727C")
LINE = colors.HexColor("#D8E3E8")
SURFACE = colors.HexColor("#F3F7F8")
PALE_TEAL = colors.HexColor("#E7F5F4")
PALE_BLUE = colors.HexColor("#EAF1F6")
WHITE = colors.white


def _register_fonts() -> None:
    candidates = [
        Path(__import__("reportlab").__file__).parent / "fonts",
        Path(rl_config.TTFSearchPath[0]),
    ]
    for directory in candidates:
        regular = directory / "Vera.ttf"
        bold = directory / "VeraBd.ttf"
        italic = directory / "VeraIt.ttf"
        if regular.exists() and bold.exists() and italic.exists():
            pdfmetrics.registerFont(TTFont("PWB-Regular", regular))
            pdfmetrics.registerFont(TTFont("PWB-Bold", bold))
            pdfmetrics.registerFont(TTFont("PWB-Italic", italic))
            pdfmetrics.registerFontFamily(
                "PWB",
                normal="PWB-Regular",
                bold="PWB-Bold",
                italic="PWB-Italic",
            )
            return
    raise RuntimeError("ReportLab Vera fonts were not found")


def _safe(value: Any) -> str:
    return html.escape(str(value), quote=False).replace("\n", "<br/>")


def _styles() -> dict[str, ParagraphStyle]:
    return {
        "eyebrow": ParagraphStyle(
            "BrochureEyebrow",
            fontName="PWB-Bold",
            fontSize=7.8,
            leading=10,
            textColor=TEAL_DARK,
            spaceAfter=4,
        ),
        "h1": ParagraphStyle(
            "BrochureH1",
            fontName="PWB-Bold",
            fontSize=25,
            leading=30,
            textColor=NAVY,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "BrochureH2",
            fontName="PWB-Bold",
            fontSize=16,
            leading=20,
            textColor=NAVY,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "BrochureH3",
            fontName="PWB-Bold",
            fontSize=11,
            leading=14,
            textColor=NAVY,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "BrochureBody",
            fontName="PWB-Regular",
            fontSize=9.3,
            leading=14,
            textColor=INK,
            spaceAfter=7,
        ),
        "body_small": ParagraphStyle(
            "BrochureBodySmall",
            fontName="PWB-Regular",
            fontSize=8.4,
            leading=12,
            textColor=INK,
        ),
        "muted": ParagraphStyle(
            "BrochureMuted",
            fontName="PWB-Regular",
            fontSize=8.2,
            leading=11.5,
            textColor=MUTED,
        ),
        "quote": ParagraphStyle(
            "BrochureQuote",
            fontName="PWB-Bold",
            fontSize=13.2,
            leading=18,
            textColor=NAVY,
            alignment=TA_LEFT,
        ),
        "cover_brand": ParagraphStyle(
            "BrochureCoverBrand",
            fontName="PWB-Bold",
            fontSize=14,
            leading=18,
            textColor=TEAL,
            alignment=TA_CENTER,
        ),
        "cover_title": ParagraphStyle(
            "BrochureCoverTitle",
            fontName="PWB-Bold",
            fontSize=30,
            leading=35,
            textColor=WHITE,
            alignment=TA_CENTER,
        ),
        "cover_subtitle": ParagraphStyle(
            "BrochureCoverSubtitle",
            fontName="PWB-Regular",
            fontSize=12,
            leading=18,
            textColor=WHITE,
            alignment=TA_CENTER,
        ),
        "cover_meta": ParagraphStyle(
            "BrochureCoverMeta",
            fontName="PWB-Regular",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#D9E6ED"),
            alignment=TA_CENTER,
        ),
        "price": ParagraphStyle(
            "BrochurePrice",
            fontName="PWB-Bold",
            fontSize=15,
            leading=18,
            textColor=TEAL_DARK,
        ),
        "chip": ParagraphStyle(
            "BrochureChip",
            fontName="PWB-Bold",
            fontSize=7.5,
            leading=9,
            textColor=TEAL_DARK,
            alignment=TA_CENTER,
        ),
        "cta": ParagraphStyle(
            "BrochureCta",
            fontName="PWB-Bold",
            fontSize=14,
            leading=19,
            textColor=WHITE,
            alignment=TA_CENTER,
        ),
    }


def _page_decoration(canvas, doc) -> None:
    canvas.saveState()
    if doc.page == 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
        canvas.setStrokeColor(colors.HexColor("#174B67"))
        canvas.setLineWidth(1)
        for offset in (0, 18 * mm, 36 * mm):
            canvas.circle(
                PAGE_WIDTH - 5 * mm,
                PAGE_HEIGHT - 33 * mm,
                33 * mm + offset,
                stroke=1,
                fill=0,
            )
        canvas.setFillColor(TEAL)
        canvas.circle(25 * mm, 30 * mm, 3 * mm, stroke=0, fill=1)
        canvas.setStrokeColor(TEAL)
        canvas.setLineWidth(2)
        canvas.line(32 * mm, 30 * mm, PAGE_WIDTH - 25 * mm, 30 * mm)
    else:
        canvas.setStrokeColor(TEAL)
        canvas.setLineWidth(1.3)
        canvas.line(
            MARGIN, PAGE_HEIGHT - 13 * mm, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 13 * mm
        )
        canvas.setFont("PWB-Bold", 7.5)
        canvas.setFillColor(NAVY)
        canvas.drawString(MARGIN, PAGE_HEIGHT - 10 * mm, "PULSEWATCH")
        canvas.setFont("PWB-Regular", 6.8)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(
            PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 10 * mm, "Upravljani tržišni nadzor"
        )

    if doc.page > 1:
        canvas.setStrokeColor(LINE)
        canvas.line(MARGIN, 12 * mm, PAGE_WIDTH - MARGIN, 12 * mm)
        canvas.setFont("PWB-Regular", 6.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN, 8 * mm, "PulseWatch · INMAR d.o.o. · OIB 33281217245")
        canvas.drawRightString(PAGE_WIDTH - MARGIN, 8 * mm, str(doc.page))
    canvas.restoreState()


def _page_title(
    eyebrow: str, title: str, intro: str, styles: dict[str, ParagraphStyle]
) -> list[Any]:
    return [
        Paragraph(_safe(eyebrow.upper()), styles["eyebrow"]),
        Paragraph(_safe(title), styles["h1"]),
        Paragraph(_safe(intro), styles["body"]),
        HRFlowable(width="100%", thickness=1.1, color=LINE),
        Spacer(1, 7 * mm),
    ]


def _bullet(text: str, styles: dict[str, ParagraphStyle]) -> Paragraph:
    return Paragraph(
        f"<font color='#21A0A0'><b>●</b></font>&nbsp;&nbsp;{_safe(text)}",
        styles["body_small"],
    )


def _info_card(
    title: str, body: str, styles: dict[str, ParagraphStyle], accent=TEAL
) -> KeepTogether:
    table = Table(
        [
            [Paragraph(_safe(title), styles["h3"])],
            [Paragraph(_safe(body), styles["body_small"])],
        ],
        colWidths=[CONTENT_WIDTH],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return KeepTogether([table, Spacer(1, 8)])


def _two_cards(
    cards: list[tuple[str, str]], styles: dict[str, ParagraphStyle]
) -> Table:
    cells: list[list[Any]] = []
    for title, text in cards:
        cells.append(
            [
                Paragraph(_safe(title), styles["h3"]),
                Paragraph(_safe(text), styles["body_small"]),
            ]
        )
    table = Table(
        [cells], colWidths=[CONTENT_WIDTH / len(cells) - 4] * len(cells), hAlign="LEFT"
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.6, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return table


def _cover(data: dict[str, Any], styles: dict[str, ParagraphStyle]) -> list[Any]:
    publisher = data["publisher"]
    return [
        Spacer(1, 23 * mm),
        Paragraph("PULSEWATCH", styles["cover_brand"]),
        Spacer(1, 13 * mm),
        Paragraph(_safe(data["cover"]["title"]), styles["cover_title"]),
        Spacer(1, 6 * mm),
        Paragraph(_safe(data["cover"]["subtitle"]), styles["cover_subtitle"]),
        Spacer(1, 17 * mm),
        Table(
            [[Paragraph(_safe(data["cover"]["promise"]), styles["quote"])]],
            colWidths=[CONTENT_WIDTH * 0.78],
            hAlign="CENTER",
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EAF6F5")),
                    ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
                    ("LEFTPADDING", (0, 0), (-1, -1), 14),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                    ("TOPPADDING", (0, 0), (-1, -1), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ]
            ),
        ),
        Spacer(1, 20 * mm),
        Paragraph("INFORMATIVNA BROŠURA USLUGE", styles["cover_meta"]),
        Spacer(1, 2 * mm),
        Paragraph(_safe(data["cover"]["validity"]), styles["cover_meta"]),
        Spacer(1, 22 * mm),
        Paragraph(
            f"Uslugu pruža <b>{_safe(publisher['short_name'])}</b><br/>"
            f"Direktor: {_safe(publisher['director'])}<br/>"
            f"{_safe(publisher['email'])} · {_safe(publisher['phone'])}",
            styles["cover_meta"],
        ),
        PageBreak(),
    ]


def _problem_page(data: dict[str, Any], styles: dict[str, ParagraphStyle]) -> list[Any]:
    flow: list[Any] = _page_title(
        "Poslovni problem",
        "Promjena je korisna tek kada vodi odluci",
        data["problem"]["intro"],
        styles,
    )
    left = [Paragraph("Što se događa bez sustava", styles["h3"])]
    left.extend([_bullet(item, styles) for item in data["problem"]["without"]])
    right = [Paragraph("Što PulseWatch preuzima", styles["h3"])]
    right.extend([_bullet(item, styles) for item in data["problem"]["with"]])
    grid = Table([[left, right]], colWidths=[CONTENT_WIDTH / 2 - 4] * 2)
    grid.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), SURFACE),
                ("BACKGROUND", (1, 0), (1, 0), PALE_TEAL),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.6, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, -1), 11),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
            ]
        )
    )
    flow.extend([grid, Spacer(1, 8 * mm)])
    flow.append(
        Table(
            [[Paragraph(_safe(data["problem"]["statement"]), styles["quote"])]],
            colWidths=[CONTENT_WIDTH],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
                    ("LINEBEFORE", (0, 0), (0, 0), 4, BLUE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 14),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                    ("TOPPADDING", (0, 0), (-1, -1), 13),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
                ]
            ),
        )
    )
    flow.extend([Spacer(1, 8 * mm), Paragraph("Najčešće pratimo", styles["h2"])])
    flow.append(
        _two_cards([(x["title"], x["text"]) for x in data["problem"]["themes"]], styles)
    )
    flow.append(PageBreak())
    return flow


def _workflow_page(
    data: dict[str, Any], styles: dict[str, ParagraphStyle]
) -> list[Any]:
    flow: list[Any] = _page_title(
        "Kako radi",
        "Od javnog izvora do sljedeće akcije",
        data["workflow"]["intro"],
        styles,
    )
    rows: list[list[Any]] = []
    for index, item in enumerate(data["workflow"]["steps"], start=1):
        num = Paragraph(
            f"{index:02d}",
            ParagraphStyle(f"Step{index}", parent=styles["price"], alignment=TA_CENTER),
        )
        content = [
            Paragraph(_safe(item["title"]), styles["h3"]),
            Paragraph(_safe(item["text"]), styles["body_small"]),
        ]
        rows.append([num, content])
    table = Table(rows, colWidths=[18 * mm, CONTENT_WIDTH - 18 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), PALE_TEAL),
                ("GRID", (0, 0), (-1, -1), 0.6, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    flow.extend(
        [table, Spacer(1, 8 * mm), Paragraph("Svaki važan signal sadrži", styles["h2"])]
    )
    signal_cells = []
    for item in data["workflow"]["signal"]:
        signal_cells.append(
            [
                Paragraph(_safe(item["label"]), styles["eyebrow"]),
                Paragraph(_safe(item["text"]), styles["body_small"]),
            ]
        )
    signal_table = Table([signal_cells], colWidths=[CONTENT_WIDTH / 3 - 3] * 3)
    signal_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.6, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    flow.extend([signal_table, PageBreak()])
    return flow


def _package_card(
    item: dict[str, Any], styles: dict[str, ParagraphStyle]
) -> KeepTogether:
    badge_style = ParagraphStyle(
        f"Badge{item['name']}",
        parent=styles["chip"],
        textColor=WHITE if item.get("featured") else TEAL_DARK,
    )
    accent = TEAL if item.get("featured") else BLUE
    header_bg = NAVY if item.get("featured") else PALE_BLUE
    title_color = WHITE if item.get("featured") else NAVY
    title_style = ParagraphStyle(
        f"Title{item['name']}", parent=styles["h3"], textColor=title_color
    )
    price_style = ParagraphStyle(
        f"Price{item['name']}",
        parent=styles["price"],
        textColor=WHITE if item.get("featured") else TEAL_DARK,
    )
    header = Table(
        [
            [
                Paragraph(_safe(item["name"]), title_style),
                Paragraph(_safe(item["badge"]), badge_style),
                Paragraph(_safe(item["price"]), price_style),
            ]
        ],
        colWidths=[46 * mm, 42 * mm, CONTENT_WIDTH - 88 * mm],
    )
    bullets = [_bullet(text, styles) for text in item["highlights"]]
    body = Table(
        [[Paragraph(_safe(item["fit"]), styles["body_small"]), bullets]],
        colWidths=[55 * mm, CONTENT_WIDTH - 55 * mm],
    )
    card = Table([[header], [body]], colWidths=[CONTENT_WIDTH])
    card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), header_bg),
                ("BACKGROUND", (0, 1), (0, 1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.7, LINE),
                ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return KeepTogether([card, Spacer(1, 7)])


def _packages_page(
    data: dict[str, Any], styles: dict[str, ParagraphStyle]
) -> list[Any]:
    flow: list[Any] = _page_title(
        "Paketi i cijene",
        "Jasan opseg. Bez skrivenog operativnog tereta.",
        data["packages"]["intro"],
        styles,
    )
    for item in data["packages"]["items"]:
        flow.append(_package_card(item, styles))
    flow.extend(
        [
            Spacer(1, 2 * mm),
            Paragraph(_safe(data["packages"]["note"]), styles["muted"]),
            PageBreak(),
        ]
    )
    return flow


def _comparison_page(
    data: dict[str, Any], styles: dict[str, ParagraphStyle]
) -> list[Any]:
    flow: list[Any] = _page_title(
        "Managed ili Lite",
        "Razlika nije samo u broju izvora",
        data["comparison"]["intro"],
        styles,
    )
    rows = [
        [
            Paragraph("ELEMENT", styles["eyebrow"]),
            Paragraph("MANAGED", styles["eyebrow"]),
            Paragraph("LITE", styles["eyebrow"]),
        ],
    ]
    for row in data["comparison"]["rows"]:
        rows.append(
            [
                Paragraph(_safe(row["label"]), styles["body_small"]),
                Paragraph(_safe(row["managed"]), styles["body_small"]),
                Paragraph(_safe(row["lite"]), styles["body_small"]),
            ]
        )
    table = Table(
        rows, colWidths=[42 * mm, 67 * mm, CONTENT_WIDTH - 109 * mm], repeatRows=1
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("BACKGROUND", (1, 1), (1, -1), PALE_TEAL),
                ("GRID", (0, 0), (-1, -1), 0.55, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    flow.extend([table, Spacer(1, 7 * mm)])
    flow.append(
        _two_cards(
            [(x["title"], x["text"]) for x in data["comparison"]["boundaries"]], styles
        )
    )
    flow.extend(
        [
            Spacer(1, 7 * mm),
            _info_card("Važno", data["comparison"]["important"], styles, BLUE),
            PageBreak(),
        ]
    )
    return flow


def _closing_page(data: dict[str, Any], styles: dict[str, ParagraphStyle]) -> list[Any]:
    publisher = data["publisher"]
    flow: list[Any] = _page_title(
        "Sljedeći korak",
        "Počinjemo jednom odlukom, ne cijelim internetom",
        data["closing"]["intro"],
        styles,
    )
    rows = []
    for index, item in enumerate(data["closing"]["steps"], start=1):
        rows.append(
            [
                Paragraph(
                    str(index),
                    ParagraphStyle(
                        f"Close{index}", parent=styles["price"], alignment=TA_CENTER
                    ),
                ),
                [
                    Paragraph(_safe(item["title"]), styles["h3"]),
                    Paragraph(_safe(item["text"]), styles["body_small"]),
                ],
            ]
        )
    table = Table(rows, colWidths=[18 * mm, CONTENT_WIDTH - 18 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), PALE_TEAL),
                ("GRID", (0, 0), (-1, -1), 0.6, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    flow.extend([table, Spacer(1, 9 * mm)])
    cta = Table(
        [
            [Paragraph(_safe(data["closing"]["cta"]), styles["cta"])],
            [Paragraph(_safe(data["closing"]["contact"]), styles["cover_meta"])],
        ],
        colWidths=[CONTENT_WIDTH],
    )
    cta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
                ("TOPPADDING", (0, 0), (-1, -1), 11),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    flow.extend([cta, Spacer(1, 8 * mm), Paragraph("Pružatelj usluge", styles["h2"])])
    legal = (
        f"<b>{_safe(publisher['legal_name'])}</b><br/>"
        f"{_safe(publisher['address'])}<br/>"
        f"OIB: {_safe(publisher['oib'])} · MBS: {_safe(publisher['mbs'])} · MB DZS: {_safe(publisher['mb_dzs'])}<br/>"
        f"{_safe(publisher['registry_court'])}<br/>"
        f"Direktor: {_safe(publisher['director'])}<br/>"
        f"{_safe(publisher['email'])} · {_safe(publisher['phone'])} · {_safe(publisher['website'])}"
    )
    flow.append(
        Table(
            [[Paragraph(legal, styles["body_small"])]],
            colWidths=[CONTENT_WIDTH],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
                    ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 11),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            ),
        )
    )
    return flow


def render_brochure(data: dict[str, Any], output: str | Path) -> Path:
    _register_fonts()
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    styles = _styles()
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=19 * mm,
        bottomMargin=17 * mm,
        title=data["metadata"]["title"],
        author=data["publisher"]["legal_name"],
        subject=data["metadata"]["subject"],
    )
    story: list[Any] = []
    story.extend(_cover(data, styles))
    story.extend(_problem_page(data, styles))
    story.extend(_workflow_page(data, styles))
    story.extend(_packages_page(data, styles))
    story.extend(_comparison_page(data, styles))
    story.extend(_closing_page(data, styles))
    doc.build(story, onFirstPage=_page_decoration, onLaterPages=_page_decoration)
    return output_path


def render_json(input_path: str | Path, output: str | Path) -> Path:
    payload = json.loads(Path(input_path).read_text(encoding="utf-8"))
    return render_brochure(payload, output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    render_json(args.input, args.output)

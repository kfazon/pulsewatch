# PulseWatch report design system

## Purpose

PulseWatch reports are decision documents, not raw monitoring dumps. Each report must let an executive answer three questions quickly:

1. What changed or was discovered?
2. Why does it matter?
3. Who should do what next?

## Visual rules

| Token | Rule |
|---|---|
| Page | A4 portrait, 17 mm content margins |
| Body | 9.2 pt, 13.8 pt leading |
| Table/card text | Never below 8 pt |
| Source text | 8 pt minimum |
| Headings | 22 / 15 / 10.8 pt |
| Spacing | 4, 8, 12, 16, 24 pt rhythm |
| Prose columns | Maximum three; prefer one or two |
| Alignment | Long text left aligned; never centered |
| Color | Navy + teal brand; severity always includes a text label |
| Density | Do not shrink text to make content fit; restructure the content |

## Information hierarchy

1. Cover, report status and legal publisher identity.
2. Executive signal cards ordered by severity.
3. Market position and confirmed gaps.
4. Competitor cards: public signal + recommended response.
5. Monitoring scope.
6. Prioritized action cards with owner and completion evidence.
7. Proposed pilot.
8. Confidential findings, if present.
9. Method and sources.

## Table policy

Tables are reserved for concise lookup data and precise values. Long narrative content must use cards or stacked sections.

- Use short column headers.
- Use consistent row/header density.
- Prefer no more than three columns when cells contain prose.
- Use one visual hierarchy inside a table: header + body.
- Do not use a 6 pt font to rescue an overloaded table.
- Numeric columns should be right aligned when introduced.
- Every severity value must include a text label; color alone is insufficient.

## Evidence contract

Every reported signal must contain:

- severity;
- finding;
- business impact;
- recommended action;
- source or evidence reference;
- detection/baseline date;
- known limitations.

A first report is explicitly labeled as a baseline. It must not imply that a historical change was automatically detected before monitoring was activated.

## Publisher identity

Every externally delivered report must identify the legal issuer on the cover and in the PDF metadata. The structured payload should include the full legal name, registered address, OIB, MBS, MB DZS, registry court, director, email, phone and website. The footer should use the concise form `PulseWatch · INMAR d.o.o. · OIB 33281217245`; the cover carries the full legal block.

## Sources used for the design rules

- IBM Carbon data table usage: https://carbondesignsystem.com/components/data-table/usage/
- Datawrapper table design: https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables
- Datawrapper text readability: https://www.datawrapper.de/blog/text-in-data-visualizations
- Datawrapper fonts: https://www.datawrapper.de/blog/fonts-for-data-visualization
- Nielsen Norman Group visual hierarchy: https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
- Adobe PDF accessibility checks: https://helpx.adobe.com/acrobat/using/create-verify-pdf-accessibility.html

## Known limitation

The initial ReportLab renderer creates searchable, extractable text and embedded Unicode fonts, but it does not yet create a fully tagged PDF/UA document. Tagged reading order and formal accessibility conformance remain a separate implementation gate.

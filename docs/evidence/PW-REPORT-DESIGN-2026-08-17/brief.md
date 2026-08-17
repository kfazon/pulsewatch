# Brief — PulseWatch report design system

**Date:** 2026-08-17

## Request

Create a reusable, better-designed PulseWatch PDF report system after the first Grama report showed inconsistent font sizes, spacing, and overly dense tables.

## Scope

- Research credible report/table design guidance.
- Add a structured JSON-to-PDF renderer.
- Preserve Croatian Unicode text.
- Add a representative Grama/TSH example.
- Add automated render tests.
- Produce and visually inspect the generated report.

## Acceptance gates

- No prose table text below 8 pt.
- No four-column table containing long narrative paragraphs.
- Searchable text and embedded Unicode font.
- PDF generation succeeds from the CLI and tests.
- Representative pages are visually reviewed for clipping, overlap, hierarchy, and spacing.

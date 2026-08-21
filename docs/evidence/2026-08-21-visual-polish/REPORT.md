# PulseWatch visual polish and SEO readiness — 2026-08-21

## Verdict

- **Visual candidate:** PASS. The user-reported footer brand defect and shared alignment inconsistencies are corrected.
- **Technical SEO:** PASS for crawlability/on-page mechanics.
- **Ranking proof:** NOT YET. Google Search Console currently shows only the homepage indexed and no 28-day search-performance rows. No honest process can promise strong rankings from technical setup alone.

## Visual defects confirmed and corrected

1. Footer's generic link rule forced the brand link to `display:block`, placing the wordmark below its mark. The footer brand now has an explicit `inline-flex`, centered horizontal lockup on desktop and mobile.
2. Hero and CTA buttons could wrap or use inconsistent mobile widths. Button text is now non-wrapping; mobile hero and CTA actions use aligned full-width controls.
3. Pricing descriptor text visually collided with the `€1,500` amount. It now occupies a separate line with controlled spacing and line height.
4. Shared card grids now explicitly stretch direct card children to equal track height.
5. Footer columns, headings, body copy and links now share explicit top alignment, margins and line height.
6. Report toolbar and report rows now use explicit cross-axis and text alignment.
7. Mobile footer spacing and final legal row were tightened and made consistent.
8. Lighthouse found an eyebrow contrast issue, skipped heading level in the example signal and a missing favicon request. Contrast, semantics and favicon are corrected.

## Verification

- Generator: 11 canonical pages rebuilt.
- Tests: `14 passed`.
- Ruff: PASS.
- PHP syntax: PASS.
- Secret scan: PASS.
- `git diff --check`: PASS.
- Browser matrix: 11 routes × 2 viewports = 22 checks; no horizontal overflow or console errors.
- Footer geometry: `inline-flex`, `align-items:center`, `flex-direction:row` on desktop and mobile.
- Candidate Lighthouse: Performance 100, Accessibility 100, Best Practices 100, SEO 100.
- Reviewed screenshots: homepage desktop/mobile, sample report desktop and pricing mobile.

## SEO reality

The site has the right technical basics: canonical URLs, unique title/description pairs, one H1 per canonical page, index/follow directives, structured JSON-LD, robots.txt, XML sitemap, internal links, semantic content and fast static delivery. The sitemap was resubmitted through Google Search Console.

That does **not** establish a strong ranking position. Current GSC evidence:

- 1 of 11 canonical routes is indexed.
- 10 routes are not yet known to Google.
- 0 clicks, 0 impressions and no query rows in the inspected 28-day window.
- The competitor-monitoring SERPs contain established monitoring and pricing-intelligence vendors, so authority, links, useful original content and time remain necessary.

Independent current-SERP review found that broad results are dominated by established, tool-led competitors such as [MonitoringMonkey](https://monitoringmonkey.com/) and [Visualping](https://visualping.io/competitive-monitoring). PulseWatch is intentionally a managed service, so generic software-intent terms are both difficult and poorly matched. The defensible future cluster is service-qualified: managed competitive intelligence for CRO agencies, material competitor-move analysis, a pricing-change response checklist and a reusable client intelligence brief template. Those pages must be original and evidence-led, not filler.

The next ranking gate is evidence, not another perfect audit score: all canonical routes discovered/indexed, first non-brand impressions, query-to-page relevance, then qualified clicks and pilot enquiries. Thin pages or invented case studies are explicitly excluded.

## Evidence

- `geometry.json`
- `lighthouse-summary.json`
- `gsc-summary.json`
- `screenshots/desktop-home.png`
- `screenshots/mobile-home.png`
- `screenshots/desktop-sample-report.png`
- `screenshots/mobile-pricing.png`

Full pre/post screenshot corpus is backed up outside the repository at:
`/Users/kfazon/.hermes/artifacts/pulsewatch-visual-polish-20260821/full-audit-evidence.tgz`

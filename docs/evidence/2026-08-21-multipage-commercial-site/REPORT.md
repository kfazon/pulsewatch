# PulseWatch multipage commercial site — verification report

**Date:** 2026-08-21  
**Scope:** Replace the one-page pilot landing with a truthful, production-ready multipage commercial foundation for the 30-day managed pilot.

## Delivered

- 11 canonical routes: home, paid pilot, method, sample report, pricing, CRO-agency use case, about, contact, security, privacy and terms.
- Shared responsive design system with local CSS/JS and no third-party runtime assets.
- Fixed pilot price shown as **€1,500 final total, paid upfront**; no unproven recurring or SaaS claim.
- Sample report explicitly identified as a demonstration based on PulseWatch's own public site change, not customer social proof.
- Public-source, human-review, evidence/interpretation, owner/checkpoint and limits methodology.
- Clean canonical routes, unique metadata, truthful Organization/WebSite/Service JSON-LD, sitemap and internal navigation.
- Existing private email capture endpoint retained.

## Automated verification

| Gate | Result |
|---|---|
| Full Python suite | PASS — `12 passed` |
| Ruff targeted check | PASS |
| Tracked secret scan | PASS |
| PHP syntax | PASS |
| `git diff --check` | PASS |
| Internal-link/canonical/schema test | PASS across all 11 routes |
| Page truthfulness/price/privacy/security tests | PASS |
| Deterministic rebuild | PASS — site tree SHA-256 `d1f7f4a63c4b65fb4ad15ffeae89c6da7fd1fc0543004086b1e5907ab348af65` |
| Local route HTTP probe | PASS — 11 pages plus CSS, JS and sitemap returned HTTP 200 |
| Local lead-capture E2E | PASS — HTTP 200, success true, one row, file mode `0600`; fixture removed |
| Playwright desktop/mobile gate | PASS — 11 routes × 2 viewports; zero overflow, missing main/H1, console errors or failed requests |

## Visual evidence

- `screenshots/desktop-home.png`
- `screenshots/mobile-home.png`
- `screenshots/desktop-sample-report.png`

The managed browser correctly blocked localhost by SSRF policy. The documented isolated Playwright fallback was used against the local PHP server.

## Truthfulness boundary

This release does **not** claim paid customers, proven conversion lift, recurring revenue, automated daily monitoring, a self-service platform or universal web coverage. The commercial proof gate remains the first unrelated prepaid pilot and a measured downstream decision/action.

## Release status

Local implementation and QA are complete. GitHub review, CI, merge, rollbackable production deploy and outside-in public verification are recorded separately after cutover.

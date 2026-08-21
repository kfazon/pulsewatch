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
| Full Python suite | PASS — `25 passed` |
| Focused public-landing suite | PASS — `12 passed` |
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
- `screenshots/production-desktop-home.png`
- `screenshots/production-mobile-home.png`

The managed browser correctly blocked localhost by SSRF policy. The documented isolated Playwright fallback was used for both local and production verification.

## Truthfulness boundary

This release does **not** claim paid customers, proven conversion lift, recurring revenue, automated daily monitoring, a self-service platform or universal web coverage. The commercial proof gate remains the first unrelated prepaid pilot and a measured downstream decision/action.

## Release status

**VERIFIED ONLINE.** PR #34 was independently reviewed after the JSON-LD correction, passed CI and merged as `1a546ce65aae773e022ff5c971a2b7ef99afc731`.

The exact hashed artifact (`052824baf0bcfafb80c5854a203d8e848c4fe307b8a5582c6ed61509b0f4ecda`) was deployed as release `pulsewatch-1a546ce65aae773e-20260821T114859Z` through a same-filesystem rename cutover. The retained rollback tree is `/home/pulsewatch/backups/public_html-20260821T120024Z-84339c0348fc`.

Outside-in production verification passed:

- 11 canonical routes returned HTTP 200 with one H1/main, matching canonical and parseable JSON-LD;
- desktop/mobile Playwright gate covered 22 route/view combinations with zero overflow, broken images, console errors or failed requests;
- the public signup returned HTTP 200 / `success: true`; the disposable lead was removed and private storage remained mode `0600`;
- `/subscribers.json`, `/.env` and `/.env.production` remained inaccessible (`403`);
- `www` redirected canonically to `https://pulsewatch.top/`;
- live `index.html` SHA-256 matched the canonical artifact (`5ce5187ae6f275f5eaae9a29972346d919814d1e2b80fadf965319210b4c736f`);
- Apache configuration returned `Syntax OK` and the rollback directory was confirmed readable.

The production SEO audit completed with four clean probes out of five. Its only finding was a P2 preload heuristic even though the page contains no images; no P0/P1 production finding remained.

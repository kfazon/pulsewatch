# PulseWatch GA4 and consent report

## Status before production deployment

| Gate | Result |
|---|---|
| Authorized Google identity | PASS — `kfazon@gmail.com` verified through OAuth user info |
| Dedicated GA4 property | PASS — `PulseWatch - GA4` |
| Web stream | PASS — `https://pulsewatch.top` |
| Retention | PASS — event data set to 2 months |
| Default consent | PASS — analytics/ad storage denied |
| Pre-consent Google requests | PASS — zero observed |
| Pre-consent GA cookies | PASS — zero observed |
| Reject and persistence | PASS |
| Reopen settings | PASS |
| Withdrawal cleanup | PASS — GA cookies expired; reload returns in denied mode |
| Focus restoration | PASS — main content or footer settings regains focus |
| Accept and returning visitor | PASS |
| GA loader after consent | PASS |
| Correct Measurement ID | PASS |
| GA collection request after consent | PASS — one request emitted in the local browser gate |
| Mobile overflow | PASS — 0 px |
| All-route browser gate | PASS — 11 routes × 2 viewports, 22/22; zero pre-consent analytics requests |
| Focused tests | PASS — 15 tests |

## Implementation

- The inline bootstrap defines Google Consent Mode v2 with analytics and all advertising consent denied.
- `gtag.js` is not downloaded until the visitor chooses **Accept analytics**.
- **Reject analytics** is equally available; the decision persists in local storage.
- Footer **Cookie settings** reopens the choice. Withdrawing a previous grant expires GA cookies and reloads the page in denied mode so the Google script is no longer present.
- GA4 config disables Google Signals and ad personalization signals.
- Successful forms emit `generate_lead` only after consent. The email value is never included.
- Privacy disclosure now names the categories, purpose, legal basis, withdrawal path, Google processor/privacy links, and 2-month retention.

## Evidence

- `ga4-resource.json` — Admin API resource identities and settings.
- `browser-gate.json` — consent/network/cookie/runtime assertions.
- `route-gate.json` — all 11 routes at desktop/mobile, including zero pre-consent analytics requests.
- `desktop-consent.png`, `mobile-consent.png` — visual evidence.
- `browser_gate.py`, `route_gate.py` — reproducible local browser gates.

Independent review initially found material gaps in post-accept cookie cleanup,
equal button prominence, and focus restoration. Those gaps were corrected before
release, and the expanded browser gate verifies each repaired path.

## Limits

- This implementation does not claim legal certification.
- Google Analytics Data API readback could not be used because that API is disabled on the OAuth client project. This does not block collection; runtime evidence verifies the expected GA loader and collection request after consent. Public production verification remains required after deployment.

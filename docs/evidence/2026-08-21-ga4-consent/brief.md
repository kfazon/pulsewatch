# GA4 + consent implementation brief

- Canonical site: `https://pulsewatch.top/`
- Analytics owner login requested: authorized Google account `kfazon@gmail.com`
- Business controller: INMAR d.o.o.
- Scope: create a dedicated GA4 property and web stream, add privacy-first consent, update disclosure, test locally, ship by PR, deploy atomically, and verify publicly.
- Collection rule: no Google Analytics network request or GA cookie before affirmative consent.
- Minimum analytics: page views plus a successful lead event; never send the submitted email address to GA4.
- Out of scope: advertising tags, Google Signals, remarketing, fabricated historical data, or ranking claims.

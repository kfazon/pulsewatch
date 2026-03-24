# PulseWatch v0.1 — ARCHITECTURE.md

**Product wedge (v0.1):** Pricing + packaging radar for SaaS + agencies. Continuously tracks competitor pages, detects meaningful changes (price, plan tiers, limits, add-ons, promos), and posts scored alerts to Discord.

**Primary design constraints:**
- High signal / low noise (pricing pages are dynamic and full of A/B tests, tracking, and localized content).
- Auditable evidence (DOM snapshot + visual proof).
- Security-first (least-privilege, encrypted secrets, controlled scraping).
- Simple v0.1 ops (single service + worker, minimal moving parts).

---

## 1) Scope

### P0 (must ship in v0.1)
1. **Watch targets**
   - CRUD: competitors, products, pages (URLs), and watch rules.
   - Scheduling (per page cadence + jitter) and manual re-capture.
2. **Capture pipeline** (Playwright)
   - Hybrid capture: **DOM extraction** + **masked screenshot** (for evidence and fallback).
   - Persist artifacts (HTML/DOM JSON, screenshot, extracted structured facts).
3. **Diff + noise control**
   - Deterministic normalization of HTML + extracted facts.
   - Rules to reduce false positives (ignore regions, dynamic tokens, ads, cookie banners).
   - Generate change events with severity score.
4. **Alerting**
   - Post alerts to a configured **Discord webhook**.
   - Alert taxonomy (price increase/decrease, plan rename, new plan, removed plan, limit changed, promo, billing period change).
   - Include evidence links (artifact URLs) + human-readable summary.
5. **Admin UI / minimal API**
   - Basic dashboard: list pages, last capture time, last change, current extracted prices.
   - API endpoints for core CRUD + capture trigger.
6. **Observability**
   - Job status, retries, dead-letter, metrics (captures/day, diff hit rate, false-positive flags).

### P1 (next after v0.1)
- Multi-tenant organizations + role-based access (viewer/editor/admin).
- Slack/MS Teams alerts.
- Semantic classification (LLM-assisted) *after* deterministic pipeline.
- Localized/country variants tracking with explicit locale matrix.
- PDF/checkout flow capture for gated pricing.
- “Competitor timeline” views and trend charts.
- Automatic selector discovery + self-healing masks.
- Browser fingerprint tuning, residential proxy support (opt-in), CAPTCHA workflows.

### Out of scope (explicitly not v0.1)
- Automated purchasing/checkout or bypassing paywalls.
- Aggressive evasion (anti-bot circumvention beyond normal browser automation).
- Large-scale crawling beyond defined watch list.
- Repackaging/selling captured content; we only store artifacts for monitoring and evidence.

---

## 2) High-level System Overview

**Core components (v0.1):**
1. **API Service** (control plane)
   - CRUD, auth, webhook config, exposes artifacts via signed URLs.
2. **Worker** (data plane)
   - Scheduler + Playwright capture + extraction + diff + alert emitter.
3. **PostgreSQL**
   - System-of-record: pages, captures, extracted facts, change events, alert deliveries.
4. **Object Storage** (S3-compatible)
   - Artifact store: HTML, normalized DOM JSON, screenshots, diff images (optional).
5. **Discord Webhook**
   - Outbound notifications.

**Primary flow:**
`Scheduler → Capture (DOM + screenshot) → Normalize → Extract facts → Diff vs previous → Score → Persist event → Alert → Deliver Discord message`

---

## 3) Data Model (PostgreSQL)

> Goal: support repeatable capture lineage, auditable diffs, and alert delivery tracking.

### Entities

#### organizations (P1; optional stub in v0.1)
- `id (uuid)`
- `name (text)`
- `created_at`

#### users (P1; optional stub in v0.1)
- `id (uuid)`
- `email (citext)`
- `password_hash`
- `org_id (uuid)`
- `role (text)`

#### competitors
- `id (uuid)`
- `org_id (uuid, nullable in v0.1)`
- `name (text)`
- `domain (text)`
- `tags (text[])`
- `created_at`

#### products
- `id (uuid)`
- `competitor_id (uuid)`
- `name (text)`
- `category (text)`
- `created_at`

#### pages
- `id (uuid)`
- `product_id (uuid)`
- `url (text)`
- `type (enum: pricing, plans, enterprise, addons, faq, other)`
- `active (bool)`
- `schedule_cron (text, nullable)` or `interval_minutes (int)`
- `timezone (text)`
- `locale (text, e.g. en-US)`
- `geo (text, e.g. US)`
- `headers_json (jsonb)` (custom headers)
- `cookies_json (jsonb)` (optional; avoid if possible)
- `capture_profile (jsonb)` (viewport, user-agent profile)
- `noise_rules (jsonb)` (mask selectors, ignore selectors, regex ignore, thresholds)
- `created_at`, `updated_at`

#### captures
- `id (uuid)`
- `page_id (uuid)`
- `status (enum: queued, running, succeeded, failed)`
- `started_at`, `finished_at`
- `http_status (int, nullable)`
- `final_url (text)`
- `content_hash_raw (text)` (hash of raw HTML)
- `content_hash_normalized (text)` (hash of normalized DOM)
- `screenshot_hash (text)`
- `artifacts (jsonb)` (pointers to object storage keys)
- `extraction (jsonb)` (structured facts extracted)
- `error (text)`
- `attempt (int)`
- `created_at`

#### extracted_offers (optional normalized table; v0.1 can keep in `captures.extraction`)
- `id (uuid)`
- `capture_id (uuid)`
- `plan_name (text)`
- `price_amount (numeric)`
- `price_currency (text)`
- `billing_period (enum: month, year, one_time, unknown)`
- `seat_min (int, nullable)`
- `seat_max (int, nullable)`
- `limits_json (jsonb)` (e.g., projects, users, storage)
- `features_json (jsonb)`

#### change_events
- `id (uuid)`
- `page_id (uuid)`
- `prev_capture_id (uuid)`
- `new_capture_id (uuid)`
- `event_type (enum: price_change, plan_added, plan_removed, plan_renamed, limit_change, feature_change, promo_change, billing_change, visual_change, content_change, error_recovery)`
- `summary (text)`
- `severity_score (int 0..100)`
- `confidence (int 0..100)`
- `diff (jsonb)` (structured diff, including numeric deltas)
- `visual_diff (jsonb)` (diff image key, changed regions)
- `created_at`

#### alert_endpoints
- `id (uuid)`
- `org_id (uuid, nullable in v0.1)`
- `type (enum: discord_webhook)`
- `name (text)`
- `config (jsonb)` (webhook url reference/key)
- `enabled (bool)`
- `created_at`

#### alert_deliveries
- `id (uuid)`
- `change_event_id (uuid)`
- `endpoint_id (uuid)`
- `status (enum: queued, sent, failed, suppressed)`
- `sent_at (timestamp, nullable)`
- `provider_message_id (text, nullable)`
- `error (text, nullable)`

### Indexing notes
- `pages(active, next_run_at)` if using computed scheduling.
- `captures(page_id, created_at desc)`.
- `change_events(page_id, created_at desc)`.
- Consider `citext` for emails/domains if P1.

---

## 4) Capture & Diff Pipeline (Hybrid DOM + Masked Screenshot)

### 4.1 Capture steps (Worker)
1. **Job acquisition**
   - Select due `pages` with jitter, lock row (SKIP LOCKED).
2. **Browser context**
   - Playwright Chromium, deterministic viewport, timezone, locale, geolocation.
   - Block heavy/irrelevant requests (ads, analytics) to reduce noise.
3. **Navigation**
   - `goto(url, wait_until="networkidle" | "domcontentloaded" based on profile)`
   - Handle cookie banners (best-effort): click known consent selectors configured per page.
4. **DOM snapshot**
   - Save:
     - raw HTML (`page.content()`)
     - simplified DOM JSON (see normalization)
     - extracted visible text of targeted nodes (pricing table)
5. **Masked screenshot**
   - Full-page screenshot or clipped to selected region.
   - Apply **mask selectors** prior to capture (blur/overlay) for elements known to change (chat widgets, rotating banners, timestamps).
6. **Extraction** (deterministic)
   - Use explicit selectors + regex for:
     - plan names
     - price amount + currency
     - billing period
     - key limits (seats, projects, storage) when reliably parseable
   - Store as `captures.extraction` with a stable schema version.
7. **Normalization + hashing**
   - Normalize HTML/DOM to reduce noise; compute normalized hash.
8. **Diff vs previous successful capture**
   - If normalized hash unchanged and extracted facts unchanged → no event.
   - Else compute:
     - structured extraction diff
     - DOM diff (tree/text)
     - visual diff (pixel diff on masked screenshots; optional for v0.1 but recommended)
9. **Scoring + alert decision**
   - Apply taxonomy + noise rules + thresholds.
   - Persist `change_event` + `alert_delivery` records.
10. **Discord notify**
   - Post message with summary, score, and evidence links.

### 4.2 Normalization rules (DOM)
Normalize before hashing/diffing:
- Remove script/style tags.
- Drop nodes matching ignore selectors (configured per page):
  - cookie banners, chat widgets, testimonials carousels, “recent signups”, dynamic counters.
- Strip attributes known to be unstable:
  - `data-*`, `aria-*` (unless used for extraction), randomized classnames.
- Normalize whitespace and numeric formatting:
  - collapse whitespace, normalize thousands separators.
- Canonicalize links:
  - strip UTM parameters, anchors.
- Locale-stable currency parsing:
  - parse to numeric amount + ISO currency when possible.

**Outputs:**
- `raw_html` (forensics)
- `normalized_dom_json` (deterministic)
- `normalized_text` (optional)
- `hash_normalized` (SHA-256)

### 4.3 Masking strategy (screenshots)
- Mask selectors list per page:
  - `[data-testid*="chat"]`, `iframe`, `#intercom-container`, `.drift-widget`, `.cookie-banner`, `.promo-rotator` etc.
- If no selectors are stable:
  - take screenshot of a **clipped region** (pricing table container) instead of full page.

### 4.4 Visual diff
- Compute pixel diff between masked screenshots.
- Ignore small pixel changes via threshold:
  - changed_pixels_ratio < `visual_threshold` → suppress.
- Store:
  - diff image (red overlay)
  - bounding boxes of changed regions.

---

## 5) Noise Control Rules (Anti-flap)

Noise control is the difference between a product and a toy. Implement these rules **deterministically**.

### 5.1 Suppression rules (hard)
- If only changes are within ignored selectors → suppress.
- If only changes are:
  - timestamps (“updated on”), rotating testimonials, “X customers”, blog feed widgets
  - tracking parameters in links
  - cookie consent state
  → suppress.

### 5.2 Threshold rules (soft)
- **Visual threshold:**
  - if `changed_pixels_ratio < 0.003` (0.3%) and extraction unchanged → suppress.
- **Text diff threshold:**
  - if Levenshtein ratio change < small threshold and no numeric deltas → suppress.

### 5.3 Stability windows
- Require **2 consecutive captures** confirming the same extraction change before sending a P0 alert for low-confidence pages.
- Add **cooldown** per page/event type (e.g., 6h) to prevent repeated alerts during experiments.

### 5.4 A/B detection heuristics
- If page alternates between two states within 24h:
  - classify as `flapping` and downgrade confidence.
  - alert only if change persists N times or exceeds severity threshold.

---

## 6) Alert Taxonomy & Scoring

### 6.1 Event taxonomy (v0.1)
1. **price_change**
   - price up/down for a plan or base product
2. **billing_change**
   - monthly↔annual, discounts, new billing cycles
3. **plan_added / plan_removed**
4. **plan_renamed**
5. **limit_change**
   - seats, usage caps, quotas
6. **feature_change**
   - major included feature toggled
7. **promo_change**
   - limited-time discount, banner, coupon
8. **visual_change**
   - visible change without structured extraction delta
9. **content_change**
   - meaningful text change (non-price) in key region
10. **error_recovery**
   - page was failing and recovered (useful ops alert)

### 6.2 Scoring model (0–100)
Compute:
- **Impact (0–60)**
  - Price delta magnitude (relative % and absolute): up to 40
  - Plan lifecycle (added/removed): 25
  - Billing cycle changes: 20
  - Limits/features change: 10–20 depending on key limit importance
- **Confidence (0–30)**
  - Extraction success (selectors hit): +10
  - Confirmed twice: +10
  - Visual diff agrees: +10
- **Novelty (0–10)**
  - Not seen in last 30 days for page: +10

**Severity score = clamp(Impact + Confidence + Novelty, 0..100)**

### 6.3 Alert routing rules
- Send to Discord if:
  - severity ≥ 40, OR
  - event_type in {price_change, plan_added, plan_removed, billing_change} with confidence ≥ 50
- Otherwise store event silently for timeline.

### 6.4 Discord message format
- Title: `🔎 PulseWatch: {Competitor} — {event_type} (score {score})`
- Fields:
  - URL
  - Summary
  - Key deltas (e.g., “Pro: $49 → $59 (+20%)”) 
  - Confidence
  - Evidence links: screenshot, diff image, normalized DOM JSON
  - Capture timestamps

---

## 7) Artifact Storage Layout (Object Storage)

Use an S3-compatible bucket with partitioned keys. All artifacts are immutable.

**Bucket:** `pulsewatch-artifacts` (env configurable)

**Key layout:**
```
/org={org_id}/competitor={competitor_id}/product={product_id}/page={page_id}/
  captures/{yyyy}/{mm}/{dd}/{capture_id}/
    raw.html
    normalized_dom.json
    extracted.json
    screenshot_masked.png
    screenshot_raw.png            # optional (avoid if privacy risk)
    console.log                   # optional
  diffs/{yyyy}/{mm}/{dd}/{event_id}/
    extraction_diff.json
    dom_diff.json
    visual_diff.png
    visual_diff_regions.json
```

**Retention (v0.1 recommendation):**
- Default: 90 days raw artifacts, 365 days structured diffs/events.
- Configurable per org/page.

**Access pattern:**
- API returns **time-limited signed URLs** for artifacts.
- Never expose bucket publicly.

---

## 8) Security, Privacy, Compliance Notes

### 8.1 Data handling
- Store only what is necessary:
  - pricing and packaging content is public, but pages may include personal data in widgets.
- Default to **masked screenshots**; avoid raw screenshots unless needed for debugging.
- Provide per-page masks and ignore selectors to prevent capturing user-specific tokens.

### 8.2 Secrets management
- Discord webhook URLs and any cookies/headers stored as secrets:
  - keep in a secrets store (or encrypted at rest in DB using KMS key).
- `.env` for local dev only; never commit.

### 8.3 Scraping ethics & legal
- Respect robots.txt where feasible; allow org-level override only with explicit user acknowledgement.
- Rate-limit per domain; exponential backoff on 429/403.
- Identify the crawler via UA string and contact email (configurable).

### 8.4 Platform hardening
- Worker runs in isolated container; no shell access from public network.
- Egress allowlist optional (P1).
- Use least-privilege IAM for object storage (write-only for worker, read-signed via API).

### 8.5 Auditability
- Every alert must link to immutable evidence artifacts.
- Keep capture and diff lineage (`prev_capture_id`, `new_capture_id`).

---

## 9) CI/CD, QA Gates, and Anti-noise Testing

### 9.1 CI pipeline (required gates)
1. **Lint + typecheck**
2. **Unit tests**
   - normalization functions
   - currency parsing
   - diff scoring
3. **Playwright smoke tests**
   - run against a curated set of stable test pages (or recorded fixtures)
   - verify:
     - capture succeeds
     - extraction produces expected schema
     - screenshot masking applied
4. **Anti-noise regression suite**
   - Fixtures: HTML snapshots for common noisy patterns
   - Ensure normalized hash stays stable when only noise changes.
5. **Security checks**
   - dependency scan
   - secret scan (gitleaks)

### 9.2 QA acceptance criteria (v0.1)
- For 20 known competitor pricing pages over 7 days:
  - false positive rate < 5% per day
  - missed major price changes = 0 (manual verification)
- Discord alert includes evidence and reproducible artifact references.

### 9.3 Performance targets
- Median capture time < 20s/page on standard worker.
- Max concurrency per domain: 1–2.

---

## 10) Rollout Plan with PR Milestones

### PR1 — Repo scaffold + core schema
- Project structure, env config
- Postgres migrations for `competitors/products/pages/captures/change_events/alert_*`
- Object storage client + artifact key conventions

### PR2 — Worker capture MVP
- Scheduler loop + job locking
- Playwright navigation + raw HTML + masked screenshot
- Artifact upload + capture record persistence

### PR3 — Deterministic normalization + hashing
- HTML/DOM normalizer
- Ignore selectors + attribute stripping
- Stable hash computation + baseline diff decision

### PR4 — Extraction engine (pricing/plans)
- Selector-driven extraction
- Currency/period parsing
- Schema versioning for extraction JSON

### PR5 — Diff + scoring + alerting (Discord)
- Structured diff (extraction deltas)
- Severity scoring
- Discord webhook sender + alert delivery tracking

### PR6 — Admin API + minimal dashboard
- CRUD endpoints
- Page status + last capture/event
- Signed URL endpoint for artifacts

### PR7 — CI gates + anti-noise suite
- Playwright smoke tests
- Fixture-based normalization regression
- Secret scan + dependency scan

### PR8 — Pilot rollout
- Seed 10–20 real competitors
- Monitor noise, refine masks/ignore rules
- Add flapping detection + cooldown

---

## 11) Operational Notes

### Scheduling
- Use `next_run_at` computed per page with jitter.
- Backoff on repeated failures; mark page as degraded and alert ops channel only.

### Retries
- Capture retries: 2–3 with exponential backoff.
- Alert retries: at-least-once with idempotency key (`change_event_id + endpoint_id`).

### Idempotency
- A change event is unique per `(page_id, prev_capture_id, new_capture_id)`.
- Suppress duplicate Discord posts via `alert_deliveries` unique constraint.

---

## 12) Output Contract (for implementation)

### 12.1 Capture output (stored in DB + artifacts)
- `captures.extraction` JSON schema (versioned):
```json
{
  "schema_version": "1.0",
  "detected_currency": "USD",
  "billing_default": "month",
  "plans": [
    {
      "name": "Pro",
      "price": {"amount": 59.0, "currency": "USD", "period": "month"},
      "limits": {"users": 10, "projects": 50},
      "features": ["SSO", "API access"]
    }
  ],
  "source": {
    "selectors_version": "2026-03-21",
    "confidence": 0.0
  }
}
```
- Artifact keys must be recorded in `captures.artifacts`:
```json
{
  "raw_html_key": ".../raw.html",
  "normalized_dom_key": ".../normalized_dom.json",
  "extracted_key": ".../extracted.json",
  "screenshot_masked_key": ".../screenshot_masked.png"
}
```

### 12.2 Change event output
- `change_events.diff` must include:
  - `extraction_delta` (plan-level numeric deltas)
  - `dom_delta_summary` (changed nodes count / key text)
  - `noise_flags` (e.g., `only_utm_changes`, `flapping_suspected`)
- `severity_score` (0..100) and `confidence` (0..100) must be set.

### 12.3 Discord alert payload
- Must include:
  - competitor + page URL
  - event type, score, confidence
  - human summary with numeric deltas when available
  - signed URLs to artifacts (masked screenshot + diff JSON)

### 12.4 Non-functional requirements
- Deterministic normalization: same input → same normalized hash.
- No secrets in logs.
- All artifacts immutable; access via signed URLs only.

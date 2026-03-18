# PulseWatch — Architecture

## MVP Scope and User Stories
- As an agency user: I can onboard my team and add target domains (up to 10 domains, 50+ pages each) so we can monitor competitor changes automatically.
- As a marketer: I want to view a unified feed of detected changes across all monitored sites with diffs and AI summaries, so I can act quickly.
- As an admin: I want to configure alert rules (Discord/email) and digest frequency (daily/weekly) to avoid noise.
- As a user: I want to see before/after screenshots and DOM/text diffs to understand exactly what changed.

## Data Model
Tables:
- tenants (id, name, slug, created_at)
- users (id, tenant_id, email, role)
- targets (id, tenant_id, url, domain, pages (JSON array), check_interval, last_checked, is_active)
- captures (id, target_id, captured_at, html_path, screenshot_paths (JSON), status)
- diffs (id, capture_id_old, capture_id_new, dom_diff (JSON/text), screenshot_diff_metric, changed_elements (JSON))
- summaries (id, diff_id, model_used, prompt_tokens, completion_tokens, content, importance_score (0-1), category)
- alert_rules (id, tenant_id, min_importance, channels (JSON: {discord_webhook, email}), digest_frequency, is_enabled, muted_until)
- alerts_sent (id, rule_id, summary_id, sent_at, channel)

## Capture Pipeline
- Scheduler: Redis queue + Celery beat; each target enqueues capture jobs based on check_interval.
- Worker: Python Playwright; concurrency per worker 4; rotate user-agents and proxy pool (optional rotation for high volume).
- Steps per job:
  1) Load target pages list (seed with homepage + sitemap discovery; allow manual page entry).
  2) For each page: navigate, wait for network idle, capture full-page screenshot (PNG), save DOM snapshot (pretty-printed HTML with inline resources stripped).
  3) Store artifacts: `screenshots/{target_id}/{date}/{page_hash}.png` and `html/{target_id}/{date}/{page_hash}.html`.
  4) Mark capture success; on error, retry 2x with backoff, then set target.is_active=false after 5 consecutive failures.
- Error handling: timeouts, 403s → rotate proxy/user-agent; log monitoring for failure rate >5% per tenant.

## Diff Strategy
- DOM diff: Use `html5lib` parse and `xml.etree` to compute tree diff; detect added/removed/modified nodes; ignore timestamp-specific attributes (data-timestamp, session tokens).
- Text diff: Extract visible text blocks (strip scripts/styles), run Myers diff; compute changed character ratio.
- Screenshot diff: perceptual hash (phash) or SSIM; if SSIM < 0.98, flag as visual change.
- Classification heuristics:
  - pricing change: keywords in diff (“price”, “$”, “€”, “discount”, “sale”)
  - product change: keywords (“new feature”, “version”, “release”)
  - content change: blog/news updates
  - careers change: “hiring”, “job”, “careers”
Assign one or more categories.

## AI Summarization
- Prompt: “Given the following change data for {domain} on {page}, summarize what changed in 1-2 sentences. Include importance from 1 (trivial) to 5 (critical).”
- Provide: changed text excerpts, category hints, before/after snippets.
- Model: OpenAI GPT-4o-mini or Anthropic Claude Haiku (cost control). Cache summaries for identical diffs (hash of diff text + category).
- Importance scoring: map model output to 0-1 float; fallback heuristics if model unavailable: changed text length ratio, pricing keywords present → boost.
- Cost control: max 500 tokens per summary; daily tenant quotas based on plan.

## Alerting & Delivery
- Each tenant has alert_rules.
- Digest modes: immediate (per change), daily (9am local), weekly (Mon 9am).
- Delivery channels:
  - Discord: webhook per rule; embed includes title, summary, importance, link to change in UI, thumbnail of screenshot diff.
  - Email: HTML email with same data; unsub link per tenant.
- Muting: admin can snooze alerts for a target or globally for N hours.
- Rate limiting: max 5 alerts/minute per tenant to avoid spam; queue and batch.

## Web UI Wireframe Notes
- Dashboard: tenant summary, active targets count, recent changes feed (last 24h), alert health.
- Targets page: list targets, add/remove pages, adjust interval, toggle active.
- Change feed: infinite scroll; each item shows: page URL, timestamp, categories, importance badge, summary, expand to view diffs (text and screenshots side-by-side).
- Settings: team members, alert rules, digest schedule, API token (for future integrations).
- Authentication: simple email+password; magic link optional.

## Deployment MVP (docker-compose)
Services:
- web (FastAPI + React served by Nginx)
- worker (Celery)
- beat (Celery beat)
- postgres
- redis
- storage (minio or local FS bind mount)
- Nginx reverse proxy + Let’s Encrypt (certbot)

One host: 4GB RAM, 2 vCPU.

docker-compose.yml defines networks, volumes, env vars.

## PoC Milestones
Week 1: Single-target capture + basic diff (Playwright, HTML+screenshot, simple DOM diff). CLI only.
Week 2: Persistent storage + FastAPI CRUD endpoints (targets, captures, diffs). Basic UI (React list).
Week 3: Integrate AI summarization + importance scoring. Add alerting (Discord webhook) per change.
Week 4: Multi-tenant scaffold + user management. Deploy docker-compose on VPS. Run full end-to-end test.

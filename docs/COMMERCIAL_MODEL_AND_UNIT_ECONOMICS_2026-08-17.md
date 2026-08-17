# PulseWatch commercial model and unit economics — 2026-08-17

> **Post-research commercial update:** competitor and managed-service research changed the recommended sell price. The current go-to-market source of truth is [`COMPETITIVE_POSITIONING_AND_90_DAY_BUSINESS_PLAN_2026-08-17.md`](COMPETITIVE_POSITIONING_AND_90_DAY_BUSINESS_PLAN_2026-08-17.md): EUR 1,500 paid pilot, EUR 1,490/month Managed, EUR 690/month tightly bounded Lite and a EUR 9,500–10,500 MRR operating target pending accountant confirmation. The EUR 590–890 figures below are preserved as the original cost-model hypothesis, not the current offer.

## Decision

PulseWatch should be sold first as a **managed intelligence service powered by PulseWatch software**. This is not a rejection of SaaS. It is the shortest path to paid proof, repeatable scope and the data needed to know which parts deserve self-service automation.

Recommended sequence:

1. **Managed pilot** — INMAR configures monitoring, reviews evidence and delivers actions.
2. **Managed platform** — client receives a portal for evidence and action tracking, while INMAR still controls setup and quality.
3. **SaaS tier** — self-service onboarding only for a narrow, standardized monitoring package after repeated renewals prove the workflow.

## Why not sell it as SaaS today?

A SaaS promise includes more than a dashboard. Customers reasonably expect self-onboarding, tenant isolation, access control, billing, usage limits, reliable scheduling, source health, backups, support and predictable results without analyst intervention.

The current repository has capture, screenshot, diff, AI summarization, Discord delivery, a dashboard skeleton and a deterministic PDF renderer. It still lacks a normalized signal model, deduplication, analyst review workflow, action lifecycle, measured capture quality, multi-tenant RBAC and billing. Calling this self-service SaaS now would transfer immature operations to the customer and create support load before the useful signal pattern is known.

Managed delivery is commercially stronger at this stage because the customer buys a reviewed result rather than unfinished software. It also lets INMAR learn:

- which monitored changes actually cause decisions;
- which sources fail or create noise;
- how much review time each client consumes;
- what can be standardized without weakening evidence quality;
- what clients renew and pay for.

## What is being sold

Do not lead with “AI monitoring” or “PDF reports.” Sell the outcome:

> PulseWatch turns public market and digital changes into reviewed signals, preserved evidence and prioritized actions for management.

The PDF is one delivery format. The recurring product is the monitored scope, evidence trail, analyst review, alert threshold and action follow-through.

## Cost model

### Important distinction

- **PDF generation alone:** effectively negligible incremental compute cost; the renderer runs locally and does not call an LLM.
- **Managed monthly report:** includes capture, storage, AI classification, human verification, report preparation and a decision meeting. Human review is the dominant cost.

PulseWatch does not yet record production time and token/storage usage per client, so there is **no measured actual cost per client yet**. The following is a planning model, not accounting fact.

### Base planning assumptions per client/month

| Assumption | Value |
|---|---:|
| Monitored URLs/product pages | 50 |
| Capture frequency | daily |
| Capture runs | 1,500/month |
| Average HTML + screenshot artifact | 0.75 MB |
| New storage before retention/compression | 1.099 GiB/month |
| Material-change rate sent to LLM | 10% |
| LLM calls | 150/month |
| Tokens per changed item | 8,000 input + 500 output |

### Variable machine cost

OpenRouter's public model catalogue was queried on 2026-08-17. It listed:

- Step 3.5 Flash: USD 0.10/M input and USD 0.30/M output tokens;
- GPT-5 mini: USD 0.25/M input and USD 2.00/M output tokens.

Under the base assumptions, estimated LLM cost is:

| Model | Estimated cost/client/month |
|---|---:|
| Step 3.5 Flash paid | USD 0.1425 |
| GPT-5 mini | USD 0.45 |

The repository currently defaults to a `:free` OpenRouter route, so nominal API cost can be zero, but a free route must not be the reliability basis of a paid service. Even with a paid model, LLM token cost is not the commercial bottleneck.

Allow **EUR 3–10/client/month** for allocated compute, storage, backups, email/alert delivery and paid AI at the first 5–10 clients. Replace this allowance with metered actuals after the first pilot.

### Human delivery cost

Current-state recurring delivery is expected to require **5–8 hours/client/month** until dedupe, review queue, evidence linking and report generation are integrated end-to-end.

| Loaded internal hour cost | 5 h/month | 8 h/month |
|---|---:|---:|
| EUR 30/h | EUR 150 | EUR 240 |
| EUR 40/h | EUR 200 | EUR 320 |

Adding the EUR 3–10 machine allowance gives a current planning cost of roughly **EUR 153–330 per recurring client/month**.

The first baseline/pilot is heavier. Budget **10–16 hours** for scope definition, source setup, evidence validation, baseline analysis and client presentation: approximately **EUR 303–650** including machine allowance at the same loaded hourly rates.

At the proposed commercial pricing:

| Offer | Price, excl. VAT | Planning delivery cost | Interpretation |
|---|---:|---:|---|
| 30-day pilot | EUR 1,250 | EUR 303–650 | Enough room for discovery and one-off setup if scope is controlled |
| Recurring managed service | EUR 590 | EUR 153–330 | Viable lower tier only with strict limits and low meeting/custom work |
| Recurring managed service | EUR 890 | EUR 153–330 | Healthier default for five competitors, reviewed alerts and monthly meeting |

These figures exclude sales time, tax, bad debt, legal/accounting overhead and major custom research. They are contribution-margin estimates, not net profit.

## Capacity without overload

Assume one operator reserves at most **80 productive hours/month** for client delivery. The rest must remain available for sales, product work, failures, administration and support.

- At 5 h/client: mathematical capacity is 16 clients.
- At 8 h/client: mathematical capacity is 10 clients.
- Mathematical capacity is not a safe operating limit because reports and meetings cluster around month-end.

Recommended caps:

| Operating maturity | Safe active clients | Why |
|---|---:|---|
| Current PoC/manual workflow | **3 pilots simultaneously** | Establish real time/noise/failure measurements before scaling |
| Current managed service after pilots | **6–8 recurring clients** | Leaves room for support, sales and month-end peaks |
| After signal schema, dedupe, review queue and automatic report assembly | **12–18 clients/operator** | Expected review time falls toward 2.5–4 h/client/month |
| Self-service SaaS | Not yet claimable | Capacity depends on verified tenant isolation, source reliability and support rate |

Infrastructure is unlikely to be the first bottleneck. Fifty daily pages equal 1,500 capture runs/client/month; even ten clients are only 15,000 scheduled captures/month. The bottleneck is analyst review, source breakage, custom requests and synchronized reporting deadlines.

## Anti-overload operating rules

1. Cap the first cohort at three concurrent pilots.
2. Stagger monthly reporting dates across four weekly cohorts; do not promise every report on the first day of the month.
3. Lock every package to a maximum number of monitored sources, competitors, products, alerts and meeting minutes.
4. Charge separately for custom research, new source types, security investigation and additional meetings.
5. Record per client: capture runs, failures, stored GB, LLM calls/tokens, accepted signals, false positives, analyst minutes, report minutes and meeting minutes.
6. Review gross margin and hours after 30 days; do not add the ninth recurring client until the six-to-eight-client cohort stays below the time budget for two cycles.

## Recommended packages

### PulseWatch Pilot — original hypothesis EUR 1,250 + VAT; current offer EUR 1,500

- 30 days;
- baseline and source setup;
- client + up to five competitors;
- up to 50 monitored public URLs, including up to 20 locked comparable product signals;
- reviewed high-priority alerts;
- one executive PDF;
- one 60-minute decision meeting.

### PulseWatch Managed — original hypothesis EUR 890 + VAT/month; current offer EUR 1,490/month

- same controlled scope;
- daily automated checks where sources permit;
- reviewed alerts, not raw diffs;
- weekly concise digest when relevant;
- monthly executive report;
- one 45-minute decision meeting;
- evidence archive and action status.

### PulseWatch Lite — original hypothesis EUR 590 + VAT/month; current offer EUR 690/month

Offer only after automation reduces review time. Suggested limit: up to three competitors, 25 URLs, no product basket, monthly report and no standing monthly meeting.

## SaaS promotion gates

Create a self-service SaaS tier only when all are true:

- at least two unrelated paying clients renew;
- one narrow package accounts for most delivered value;
- median analyst time is measured and stable;
- source failure and false-positive rates are measured;
- tenant isolation, RBAC, billing, backup/restore and retention are tested;
- a client can onboard and understand results without INMAR manually correcting the workflow.

Until then, market it honestly as **PulseWatch Managed Intelligence by INMAR d.o.o.**, supported by proprietary software and human verification.

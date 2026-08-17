# PulseWatch product direction — 2026-08-17

## Decision

PulseWatch should first be sold as a **managed market and digital intelligence service**, not as a self-service SaaS dashboard.

The customer buys:

- an important change discovered early;
- preserved evidence;
- a concise explanation of possible business impact;
- a prioritized action with an owner;
- a recurring executive report.

The current repository already contains useful technical building blocks, but it does not yet prove the reliability, evidence discipline, and multi-client operations needed for a standalone SaaS product.

## Current repository reality

| Capability | Status on `main` | Product interpretation |
|---|---|---|
| Web capture and screenshot | Present | Evidence acquisition exists |
| Filesystem capture storage | Present | Adequate for PoC, not multi-client operations |
| Text diff | Present | Raw change detection exists |
| LLM summary and importance score | Present | Useful analyst aid, not a source of truth |
| Discord alert and weekly digest | Present | Early delivery channel exists |
| React dashboard and Docker skeleton | Present | UI/deploy foundation exists |
| Normalized business signal model | Missing | Highest-priority product gap |
| Dedupe and signal lifecycle | Missing | Alerts can become noisy or repetitive |
| Action owner/status/closure | Missing | Findings are not yet managed to outcome |
| Deterministic executive PDF | Added in report-design PR | Repeatable client deliverable |
| Multi-tenant auth, billing and RBAC | Missing | Do not sell self-service SaaS yet |

## Product architecture

### 1. Evidence core

The system must preserve what was checked and what changed.

Required fields:

- client and monitored subject;
- canonical URL or data source;
- capture time and timezone;
- screenshot/HTML/PDF artifact path and hash;
- before/after evidence;
- parser/version metadata;
- capture success or failure reason.

A report claim must be traceable to evidence. LLM text is never evidence.

### 2. Signal engine

Raw diffs become normalized signals with a stable schema:

- `signal_id`;
- client, source and topic;
- first seen / last seen;
- finding;
- severity, confidence and category;
- business impact hypothesis;
- recommended action;
- evidence references;
- duplicate group;
- state: `new`, `reviewed`, `sent`, `actioned`, `closed`, `false_positive`;
- action owner, due date and completion evidence.

Deterministic rules should handle known changes such as broken links, catalogue expiry, price differences and missing pages. The LLM should explain and classify, not invent the underlying fact.

### 3. Analyst operations

Before a signal reaches a client, an analyst workflow should support:

- evidence preview;
- accept/reject/edit;
- duplicate merge;
- severity override with reason;
- false-positive feedback;
- action owner and status;
- audit history.

This is the quality-control layer that makes a managed service sellable before full SaaS automation.

### 4. Delivery

One signal model should produce three delivery forms:

1. **Immediate alert** — only for an agreed high-severity threshold.
2. **Weekly digest** — concise list of reviewed changes.
3. **Monthly executive PDF** — signal, evidence, implication, action, owner and status.

The client should not have to watch a dashboard. A portal can be added later for evidence drill-down and action tracking.

## First sellable package: Grama Market Pulse

### Scope

- Grama and TSH public domains;
- five agreed competitors;
- up to 20 locked, genuinely comparable products or product signals;
- catalogues, promotions, loyalty, local availability, pickup and unexpected website changes;
- weekly reviewed alerts;
- monthly executive PDF;
- one decision meeting.

### Explicit exclusions

- no ERP/CRM integration in the first pilot;
- no claim of exact local stock unless the source proves it;
- no security diagnosis without technical investigation;
- no automatic claim that the client is cheaper or more expensive without comparable EAN/package data;
- no credential collection in reports; all secrets are `[REDACTED]`.

### Commercial proposal

| Item | Proposal |
|---|---|
| Pilot | 30 days |
| Price | EUR 1,250 + VAT |
| After pilot | EUR 590–890 + VAT/month, based on sources and frequency |
| PASS | At least one timely signal leads to a documented business/protective action, evidence coverage is complete, and alert noise is accepted by the client |
| STOP/REDESIGN | Signals cannot be evidenced, false alarms dominate, or client actions cannot be assigned/closed |

## 90-day build order

### P0 — sellable managed service

1. Merge the deterministic report renderer and design system.
2. Define and validate the normalized signal/evidence schema.
3. Add client/monitor configuration with explicit frequency and thresholds.
4. Add evidence links/hashes to every alert and report item.
5. Add dedupe and signal lifecycle states.
6. Build a Grama pilot configuration and operating runbook.

### P1 — reliable repeated delivery

1. Add analyst review queue.
2. Add action owner/status/closure evidence.
3. Move operational records from loose filesystem indexing to a database while preserving immutable artifacts.
4. Add capture reliability metrics, alert-noise metrics and source health.
5. Generate weekly and monthly reports from the same stored signals.

### P2 — controlled productization

Only after two or more unrelated paying customers renew:

1. client portal with evidence drill-down;
2. tenant isolation and RBAC;
3. onboarding/config UI;
4. billing and usage limits;
5. integration connectors.

## Product gates before calling it SaaS

- two unrelated paying customers;
- at least one renewal;
- reproducible capture and report generation;
- complete evidence trace for every delivered claim;
- measured false-positive and missed-capture rates;
- tenant isolation and access control verified;
- backup/restore and incident runbook tested;
- clear data retention and licensing terms.

## Positioning

Do not sell “AI website monitoring” or “another dashboard.”

Sell:

> PulseWatch turns public market and digital changes into reviewed signals, preserved evidence and prioritized actions for management.

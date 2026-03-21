# PulseWatch — ARCHITECTURE (Scaffold)

> **Status:** Placeholder scaffold (pending CTO final architecture)
> **Owner:** CTO
> **Last updated:** 2026-03-21

---

## 1) Product Goals (MVP)

<!-- TODO(CTO): define concrete goals, non-goals, and launch criteria -->
- Goal 1: _TBD_
- Goal 2: _TBD_
- Goal 3: _TBD_

## 2) Scope

### In scope
- _TBD_

### Out of scope
- _TBD_

## 3) High-Level System Design

<!-- TODO(CTO): include architecture diagram / component map -->

### Core Components
- Capture service: _TBD_
- Diff engine: _TBD_
- Summarization service: _TBD_
- Alerts/notifications: _TBD_
- API + Web app: _TBD_

## 4) Data Model

<!-- TODO(CTO): finalize entities and relationships -->
- tenants: _TBD_
- users: _TBD_
- targets: _TBD_
- captures: _TBD_
- diffs: _TBD_
- summaries: _TBD_
- alert_rules: _TBD_

## 5) Capture & Diff Pipeline

<!-- TODO(CTO): scheduling cadence, retries, artifact format -->
1. Schedule target checks: _TBD_
2. Capture artifacts (HTML/screenshots): _TBD_
3. Compute text/DOM/visual diffs: _TBD_
4. Persist changes and metadata: _TBD_

## 6) AI Summarization

<!-- TODO(CTO): model/provider, prompt strategy, token/cost controls -->
- Provider/model: _TBD_
- Prompt contract: _TBD_
- Fallback behavior: _TBD_

## 7) Alerting & Delivery

<!-- TODO(CTO): trigger thresholds, channels, digest policy -->
- Immediate alerts: _TBD_
- Daily/weekly digests: _TBD_
- Channel strategy (Discord/email): _TBD_

## 8) Security & Compliance

<!-- TODO(CTO): secret management, RBAC, audit logging -->
- Auth model: _TBD_
- Data retention policy: _TBD_
- PII handling: _TBD_

## 9) Deployment & Operations

<!-- TODO(CTO): environments, infra baseline, scaling assumptions -->
- Runtime architecture: _TBD_
- Dependencies (DB/queue/storage): _TBD_
- Monitoring/alerting: _TBD_

## 10) Milestones

<!-- TODO(CTO): timeline + acceptance criteria -->
- Milestone 1: _TBD_
- Milestone 2: _TBD_
- Milestone 3: _TBD_

---

## Changelog
- 2026-03-21: Added scaffold structure so implementation can proceed once CTO finalizes content.

# ENGINEERING_DOCS_MINIMUM.md — Minimal Project Documentation Standard

## Goal
A **minimum viable** documentation set that:
- prevents CEO/specialist misalignment (clear brief → evidence)
- makes delivery reproducible (commands, env, tests)
- makes handoff easy (how to run, where to look)
- avoids process bloat

This standard is designed to map directly to our **Task Brief** + **Delivery Report** gates.

---

## Required structure (per repo)

```
README.md
CHANGELOG.md
/docs
  ARCHITECTURE.md
  RUNBOOK.md
  evidence/
    <TASK_ID>/
      brief.md
      report.md
      artifacts/
```

Notes:
- `docs/evidence/<TASK_ID>/` is the canonical place to store proof without dumping logs into chat.
- Artifacts can be small logs, screenshots, JSON summaries, links, etc.

---

## 1) README.md (required)
Purpose: one-page orientation.

Required sections:
- What this repo does (1–3 sentences)
- Quickstart (exact commands)
- Config (.env keys list; never paste secrets)
- How to run tests
- Where deployments/live URLs are (if relevant)
- Links to RUNBOOK + ARCHITECTURE

Template:
```md
# <project>

## What it is

## Quickstart
```sh
# install
...
# run
...
```

## Config
- `.env` keys:
  - KEY_1=
  - KEY_2=

## Tests
```sh
...
```

## Docs
- Architecture: docs/ARCHITECTURE.md
- Runbook: docs/RUNBOOK.md

## Evidence
- docs/evidence/<TASK_ID>/
```

---

## 2) docs/ARCHITECTURE.md (required)
Purpose: stable mental model.

Required sections:
- High-level diagram (ASCII ok)
- Main components + responsibilities
- Data flows / APIs
- Key dependencies
- Failure modes + mitigations
- Tech decisions (link to Decision Log if exists)

Template:
```md
# Architecture

## Overview

## Components

## Data/API flows

## Dependencies

## Failure modes

## Decisions
```

---

## 3) docs/RUNBOOK.md (required)
Purpose: operators can reproduce runs and fix issues.

Required sections:
- Common commands (run/dev/test/lint)
- Deploy procedure (if any)
- Rollback procedure
- Monitoring/health checks
- Troubleshooting playbook

Template:
```md
# Runbook

## Run locally

## Tests

## Deploy

## Rollback

## Troubleshooting
```

---

## 4) CHANGELOG.md (required)
Purpose: concise release notes / what changed.

Rule: one entry per TASK_ID or PR.

Template:
```md
# Changelog

## Unreleased

## YYYY-MM-DD
- TASK_ID: ... — <1 line change>
  - Evidence: docs/evidence/<TASK_ID>/
```

---

## Evidence convention (maps to workflow)
For each task:
- `docs/evidence/<TASK_ID>/brief.md` = copied Task Brief
- `docs/evidence/<TASK_ID>/report.md` = copied Delivery Report
- `docs/evidence/<TASK_ID>/artifacts/` = files/outputs

Naming guidance:
- `test-output.txt`
- `migration-notes.md`
- `before-after.png`
- `run-summary.json`

---

## Delivery Report → Docs mapping
- Changed files → goes into report.md + references in CHANGELOG
- Commands run + results → report.md (and/or artifacts)
- Acceptance criteria met → report.md
- Evidence → artifacts + links in report.md

---

## Adoption checklist (for a repo)
- [ ] Add required files/dirs
- [ ] Update README quickstart + tests
- [ ] Add first TASK_ID evidence folder
- [ ] Enforce: no DONE without report + evidence

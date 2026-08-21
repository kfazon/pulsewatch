# Evidence report — PulseWatch commercial website foundation

**Date:** 2026-08-21
**Branch:** `feat/commercial-foundation`

## Scope

Repository and public-landing reality check performed before defining the active product, website, SEO, marketing and sales plan.

## Security finding and immediate containment

The production subscription handler stored runtime subscriber data inside the
public document root, and the JSON file was directly retrievable. The handler
also contained a committed Discord webhook credential and stored request IP
addresses although the pilot form only requires an email address.

Immediate containment completed on 2026-08-21:

- backed up the subscriber file to a root-protected server backup location;
- deployed an Apache deny rule for `subscribers.json` and `.env*` in the
  PulseWatch document root;
- verified the home page remains `200` while private paths return `403`;
- revoked the exposed Discord webhook and verified it returns `404`;
- removed external webhook delivery from the lead-capture handler;
- removed IP collection from new subscription records;
- moved lead storage to `/var/lib/pulsewatch/subscribers.json`, outside the
  document root, with `www-data` ownership and mode `0600`;
- added a visible privacy notice, 90-day retention purge, exclusive file
  locking and fail-closed storage configuration;
- removed the tracked production environment file, replaced it with a
  placeholder-only template and added a tracked-file secret scan to CI;
- rotated the server-side application secrets; the published database user did
  not exist on the current VPS database, so no database-role password rotation
  was applicable;
- added regression assertions for credential absence and Apache denial.

Historical removal is not treated as secret recovery: the webhook was rotated
because git history remains permanent evidence of exposure.

## Verified repository state

- Canonical repository: `https://github.com/kfazon/pulsewatch`
- Default branch: `main`
- Working branch created from current `origin/main`: `feat/commercial-foundation`
- GitHub authentication: valid
- Existing revenue milestones/issues found:
  - Managed Pilot v0.2
  - Revenue Validation 90D
  - issues #16–#19 for account universe, paid-pilot assets, economics and approval-gated outreach
- Existing stacked report/business work found in open PRs #21 and #22; it is not yet canonical `main`.

## Product reality

Verified in repository:

- capture, diff, evidence, scoring and Discord-oriented components exist;
- a frontend dashboard and report-generation work exist;
- the public surface remains one static landing page and a pilot-details form;
- the public site must not be presented as a completed self-service SaaS;
- the honest initial delivery mode is a managed paid pilot/service.

## Public claim defect reproduced

The previous public HTML contained:

- fallback claim `247 growth teams already on the list`;
- claim `Used by growth teams worldwide`;
- claim `From startups to enterprise`.

The live count endpoint returned:

```json
{"count":5}
```

This made the old static fallback and adoption claims unverified. A regression
test was added first and failed against the previous page. The landing HTML was
then changed to the managed-pilot offer with no adoption claim.

## Commands and observed results

| Command | Result |
|---|---|
| `git fetch origin --prune && git switch main && git pull --ff-only origin main` | synchronized with canonical main |
| `gh auth status` | authenticated |
| `gh issue list ...` | existing v0.1, Managed Pilot and Revenue Validation work confirmed |
| `gh pr list ...` | open PRs #10, #11, #21, #22 confirmed |
| full `pytest tests/ -q` gate | 10 passed |
| targeted new truthfulness test before fix | failed as expected |
| targeted new truthfulness test after fix | passed |
| PHP syntax and isolated subscription flow | passed; valid, duplicate and invalid paths exercised; one email/timestamp record, mode `0600`, no IP retained |
| headless Playwright desktop/mobile/privacy gate | HTTP 200, one H1/main, no overflow, no console errors, no failed requests |
| production private-path check | home 200; `subscribers.json` 403; `.env` 403 |
| revoked webhook verification | 404 |
| `npm ci && npm run build` in `frontend/` | build passed; 41 modules transformed |
| `npm audit --json` | 7 vulnerabilities: 1 low, 1 moderate, 5 high; no critical |
| independent P0/P1/P2 review | all four findings remediated in the follow-up diff |
| Ruff, formatting, tracked-secret scan and `git diff --check` | passed |

## Current blockers and boundaries

1. No independent paying PulseWatch customer is yet evidenced.
2. Pricing is a hypothesis until a buyer pays.
3. Existing business/report PR stack is green but not merged; canonical-source reconciliation is required.
4. The React frontend dependency tree has 5 high advisories and needs a bounded upgrade PR before treating it as a production customer portal.
5. No external outreach, payment or legal publication was performed. The only
   direct production change was the emergency Apache privacy block.
6. Search ranking and revenue uplift remain unproven until measured after publication and sales execution.

## Decision

Proceed with:

1. truthfulness correction;
2. active commercial/web/SEO plan in the repository;
3. GitHub execution queue;
4. revenue-ready static website before self-service SaaS;
5. paid-pilot validation before broad product build.

Do not proceed yet with:

- mass outreach;
- fake testimonials/social proof;
- production customer dashboard claims;
- broad paid acquisition;
- self-service billing/onboarding.

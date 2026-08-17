# PulseWatch — Week 1 PoC

Simple CLI proof-of-concept for:
- capturing a single URL (HTML + full-page screenshot)
- storing artifacts on local filesystem
- diffing two captures with a text diff

## Quick start (Docker Compose full stack)
```bash
cp .env.production .env && docker-compose up --build
```

Services:
- **frontend** → <http://localhost:3000>
- **backend** → <http://localhost:8000>
- **postgres** → localhost:5432
- **discord-scheduler** → runs daily digest job via cron

> Note: backend startup is controlled by environment variables:
> - `MIGRATION_CMD` for DB migration command (optional)
> - `BACKEND_START_CMD` for the backend server command (optional)
> If not set, backend falls back to `python -m http.server 8000`.

## Architecture overview
- **postgres**: persistent Postgres 16 database (`postgres_data` volume)
- **backend**: Python app container built from root `Dockerfile`, mounts `pulsewatch_data` for persistent capture artifacts
- **frontend**: React + Vite app built in multi-stage Docker image and served by Nginx on port 3000
- **discord-scheduler**: Python Alpine container using `crond` to trigger `alerts.scheduler.check_and_send_digest()` once daily

## Files
- `pulsewatch_cli.py` — CLI entry point (`capture`, `diff`)
- `capture.py` — Playwright capture helper
- `storage.py` — filesystem pathing + artifact persistence
- `diff.py` — basic unified text diff

## Install (local, non-Docker)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Usage
### Capture
```bash
python pulsewatch_cli.py capture https://example.com
```
Artifacts are stored under:
```text
data/{target_domain}/{date}/{page_hash}/
```
with files:
- `page.html`
- `screenshot.png`
- `metadata.json`

### Diff two captures
```bash
python pulsewatch_cli.py diff data/example.com/2026-03-18/abc123 data/example.com/2026-03-18/def456
```
Outputs:
- changed lines count
- `diff.txt` path (written to the new capture directory)

### Render an executive PDF report

```bash
python pulsewatch_cli.py report \
  reports/examples/grama_market_pulse.json \
  artifacts/report.pdf
```

The `report` command turns a structured JSON payload into a branded A4 executive PDF. The reusable visual and evidence rules are documented in [`docs/REPORT_DESIGN_SYSTEM.md`](docs/REPORT_DESIGN_SYSTEM.md).

Commercial packaging, estimated unit economics and safe client-capacity limits are documented in [`docs/COMMERCIAL_MODEL_AND_UNIT_ECONOMICS_2026-08-17.md`](docs/COMMERCIAL_MODEL_AND_UNIT_ECONOMICS_2026-08-17.md).

The evidence-grounded competitor matrix, current Managed/Lite packages, role split and 90-day path to paid validation are documented in [`docs/COMPETITIVE_POSITIONING_AND_90_DAY_BUSINESS_PLAN_2026-08-17.md`](docs/COMPETITIVE_POSITIONING_AND_90_DAY_BUSINESS_PLAN_2026-08-17.md).

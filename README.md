# PulseWatch — Week 1 PoC

Simple CLI proof-of-concept for:
- capturing a single URL (HTML + full-page screenshot)
- storing artifacts on local filesystem
- diffing two captures with a text diff

## Files
- `pulsewatch_cli.py` — CLI entry point (`capture`, `diff`)
- `capture.py` — Playwright capture helper
- `storage.py` — filesystem pathing + artifact persistence
- `diff.py` — basic unified text diff

## Install
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

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8767"
ROUTES = [
    "/",
    "/paid-pilot/",
    "/how-it-works/",
    "/sample-report/",
    "/pricing/",
    "/for-cro-agencies/",
    "/about/",
    "/contact/",
    "/security/",
    "/privacy/",
    "/terms/",
]
VIEWPORTS = [(1440, 1000), (390, 844)]
OUT = Path("docs/evidence/2026-08-21-ga4-consent/route-gate.json")
rows = []
console_errors = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width, height in VIEWPORTS:
        context = browser.new_context(viewport={"width": width, "height": height})
        page = context.new_page()
        requests = []
        errors = []
        page.on("request", lambda request, target=requests: target.append(request.url))
        page.on(
            "console",
            lambda message, target=errors: (
                target.append(message.text) if message.type == "error" else None
            ),
        )
        for route in ROUTES:
            before = len(requests)
            response = page.goto(BASE + route, wait_until="networkidle")
            external = [
                url
                for url in requests[before:]
                if "googletagmanager.com" in url or "google-analytics.com" in url
            ]
            row = page.evaluate(
                """() => ({
                    h1: document.querySelectorAll('h1').length,
                    main: Boolean(document.querySelector('main')),
                    banner: !document.querySelector('.consent-banner').hidden,
                    overflow: document.documentElement.scrollWidth-document.documentElement.clientWidth
                })"""
            )
            row.update(
                {
                    "route": route,
                    "viewport": f"{width}x{height}",
                    "status": response.status if response else 0,
                    "analytics_requests_before_consent": external,
                }
            )
            rows.append(row)
        console_errors.extend(
            {"viewport": f"{width}x{height}", "message": error} for error in errors
        )
        context.close()
    browser.close()

failures = [
    row
    for row in rows
    if row["status"] != 200
    or row["h1"] != 1
    or not row["main"]
    or not row["banner"]
    or row["overflow"] > 1
    or row["analytics_requests_before_consent"]
]
result = {
    "routes": len(ROUTES),
    "viewports": len(VIEWPORTS),
    "checks": len(rows),
    "failures": failures,
    "console_errors": console_errors,
}
OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "routes": len(ROUTES),
            "viewports": len(VIEWPORTS),
            "checks": len(rows),
            "failures": len(failures),
        }
    )
)
raise SystemExit(1 if failures or console_errors else 0)

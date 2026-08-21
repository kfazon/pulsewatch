import json
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8767"
OUT = Path("docs/evidence/2026-08-21-ga4-consent")
OUT.mkdir(parents=True, exist_ok=True)
result = {}


def is_google_analytics(url: str) -> bool:
    return (
        "googletagmanager.com/gtag/js" in url or "google-analytics.com/g/collect" in url
    )


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # Fresh visitor: banner shown, GA4 entirely absent before a decision.
    context = browser.new_context(viewport={"width": 1440, "height": 1000})
    page = context.new_page()
    requests = []
    page.on("request", lambda request: requests.append(request.url))
    page.goto(BASE + "/", wait_until="networkidle")
    banner = page.locator(".consent-banner")
    result["fresh_banner_visible"] = banner.is_visible()
    result["pre_consent_analytics_requests"] = [
        u for u in requests if is_google_analytics(u)
    ]
    result["pre_consent_ga_cookies"] = [
        c["name"] for c in context.cookies() if c["name"].startswith("_ga")
    ]
    page.screenshot(path=str(OUT / "desktop-consent.png"), full_page=False)

    page.evaluate(
        "document.cookie='_ga=qa; Path=/'; document.cookie='_ga_QA=qa; Path=/'"
    )
    page.get_by_role("button", name="Reject analytics").click()
    page.wait_for_timeout(500)
    result["reject_choice"] = page.evaluate(
        "localStorage.getItem('pulsewatch_analytics_consent_v1')"
    )
    result["reject_banner_hidden"] = not banner.is_visible()
    result["reject_clears_ga_cookies"] = not any(
        c["name"].startswith("_ga") for c in context.cookies()
    )
    result["initial_reject_focuses_main"] = page.evaluate(
        "document.activeElement === document.querySelector('main')"
    )
    result["post_reject_analytics_requests"] = [
        u for u in requests if is_google_analytics(u)
    ]
    page.reload(wait_until="networkidle")
    result["reject_persists_after_reload"] = not banner.is_visible()
    page.get_by_role("button", name="Cookie settings").click()
    result["settings_reopens_banner"] = banner.is_visible()
    result["settings_focuses_reject"] = page.evaluate(
        "document.activeElement.classList.contains('js-consent-reject')"
    )
    page.get_by_role("button", name="Reject analytics").click()
    page.wait_for_timeout(100)
    result["settings_focus_restored"] = page.evaluate(
        "document.activeElement.classList.contains('js-cookie-settings')"
    )
    context.close()

    # Accepting loads the exact GA4 stream and stores the choice.
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    requests = []
    responses = []
    page.on("request", lambda request: requests.append(request.url))
    page.on(
        "response",
        lambda response: responses.append(
            {"url": response.url, "status": response.status}
        ),
    )
    page.goto(BASE + "/", wait_until="networkidle")
    page.screenshot(path=str(OUT / "mobile-consent.png"), full_page=False)
    page.get_by_role("button", name="Accept analytics").click()
    page.wait_for_timeout(2500)
    result["accept_choice"] = page.evaluate(
        "localStorage.getItem('pulsewatch_analytics_consent_v1')"
    )
    result["accept_banner_hidden"] = not page.locator(".consent-banner").is_visible()
    result["post_accept_gtag_requests"] = [
        u for u in requests if "googletagmanager.com/gtag/js" in u
    ]
    result["post_accept_collect_count"] = len(
        [u for u in requests if "google-analytics.com/g/collect" in u]
    )
    result["post_accept_collect_statuses"] = [
        r["status"] for r in responses if "google-analytics.com/g/collect" in r["url"]
    ]
    result["measurement_id_in_request"] = any("G-8BCQQRSG45" in u for u in requests)
    result["mobile_document_overflow"] = page.evaluate(
        "document.documentElement.scrollWidth-document.documentElement.clientWidth"
    )
    result["accept_focuses_main"] = page.evaluate(
        "document.activeElement === document.querySelector('main')"
    )
    page.evaluate("document.cookie='_ga_WITHDRAW=qa; Path=/'")
    before_withdraw = len(requests)
    page.get_by_role("button", name="Cookie settings").click()
    with page.expect_navigation(wait_until="networkidle"):
        page.get_by_role("button", name="Reject analytics").click()
    result["withdrawal_choice"] = page.evaluate(
        "localStorage.getItem('pulsewatch_analytics_consent_v1')"
    )
    result["withdrawal_remaining_ga_cookies"] = [
        {"name": c["name"], "domain": c["domain"], "path": c["path"]}
        for c in context.cookies()
        if c["name"].startswith("_ga")
    ]
    result["withdrawal_clears_ga_cookies"] = not result[
        "withdrawal_remaining_ga_cookies"
    ]
    result["withdrawal_stops_new_analytics_requests"] = not any(
        is_google_analytics(url) for url in requests[before_withdraw:]
    )
    context.close()

    # Returning accepted visitor: no banner and analytics starts.
    context = browser.new_context(viewport={"width": 1440, "height": 1000})
    context.add_init_script(
        "localStorage.setItem('pulsewatch_analytics_consent_v1','granted')"
    )
    page = context.new_page()
    requests = []
    page.on("request", lambda request: requests.append(request.url))
    page.goto(BASE + "/pricing/", wait_until="networkidle")
    page.wait_for_timeout(1500)
    result["returning_accept_banner_hidden"] = not page.locator(
        ".consent-banner"
    ).is_visible()
    result["returning_accept_gtag_loaded"] = any(
        "googletagmanager.com/gtag/js" in u for u in requests
    )
    context.close()
    browser.close()

checks = {
    "fresh_banner_visible": result["fresh_banner_visible"] is True,
    "zero_pre_consent_requests": result["pre_consent_analytics_requests"] == [],
    "zero_pre_consent_ga_cookies": result["pre_consent_ga_cookies"] == [],
    "reject_saved": result["reject_choice"] == "denied",
    "reject_hides_and_persists": result["reject_banner_hidden"]
    and result["reject_persists_after_reload"],
    "reject_clears_cookies": result["reject_clears_ga_cookies"],
    "initial_reject_focuses_main": result["initial_reject_focuses_main"],
    "zero_post_reject_requests": result["post_reject_analytics_requests"] == [],
    "settings_reopens": result["settings_reopens_banner"],
    "settings_focus_path": result["settings_focuses_reject"]
    and result["settings_focus_restored"],
    "accept_saved": result["accept_choice"] == "granted",
    "accept_hides": result["accept_banner_hidden"],
    "accept_focuses_main": result["accept_focuses_main"],
    "gtag_loaded_after_accept": bool(result["post_accept_gtag_requests"]),
    "measurement_id_correct": result["measurement_id_in_request"],
    "no_mobile_overflow": result["mobile_document_overflow"] <= 1,
    "withdrawal_clears_and_stops": result["withdrawal_choice"] == "denied"
    and result["withdrawal_clears_ga_cookies"]
    and result["withdrawal_stops_new_analytics_requests"],
    "returning_accept_loads": result["returning_accept_banner_hidden"]
    and result["returning_accept_gtag_loaded"],
}
result["checks"] = checks
result["pass"] = all(checks.values())
(OUT / "browser-gate.json").write_text(json.dumps(result, indent=2) + "\n")
print(
    json.dumps(
        {
            "pass": result["pass"],
            "checks": checks,
            "post_accept_collect_count": result["post_accept_collect_count"],
        },
        indent=2,
    )
)
raise SystemExit(0 if result["pass"] else 1)

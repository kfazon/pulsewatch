import json
import re
from pathlib import Path
from xml.etree import ElementTree

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public-landing"
CANONICAL_ROUTES = [
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


def route_file(route: str) -> Path:
    return PUBLIC / ("index.html" if route == "/" else route.strip("/") + "/index.html")


def test_commercial_site_has_all_canonical_routes() -> None:
    for route in CANONICAL_ROUTES:
        assert route_file(route).is_file(), route


def test_every_page_has_unique_seo_and_semantic_basics() -> None:
    titles: set[str] = set()
    descriptions: set[str] = set()
    for route in CANONICAL_ROUTES:
        html = route_file(route).read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")
        canonical = f"https://pulsewatch.top{route}"
        assert soup.html.get("lang") == "en"
        assert len(soup.select("main")) == 1
        assert len(soup.select("h1")) == 1
        assert soup.select_one('meta[name="robots"]')["content"].startswith(
            "index, follow"
        )
        assert soup.select_one('link[rel="canonical"]')["href"] == canonical
        assert soup.select_one('meta[property="og:url"]')["content"] == canonical
        title = soup.title.get_text(strip=True)
        description = soup.select_one('meta[name="description"]')["content"]
        assert 20 <= len(title) <= 70
        assert 70 <= len(description) <= 180
        assert title not in titles
        assert description not in descriptions
        titles.add(title)
        descriptions.add(description)
        payloads = soup.select('script[type="application/ld+json"]')
        assert len(payloads) == 1
        schema = json.loads(payloads[0].string)
        assert schema["@context"] == "https://schema.org"
        assert isinstance(schema["@graph"], list)
        expected_page_type = {
            "/paid-pilot/": "Service",
            "/pricing/": "Service",
            "/about/": "AboutPage",
            "/contact/": "ContactPage",
        }.get(route, "WebPage")
        assert {node["@type"] for node in schema["@graph"]} >= {
            "Organization",
            expected_page_type,
        }


def test_site_uses_local_shared_assets_and_no_runtime_cdn() -> None:
    for route in CANONICAL_ROUTES:
        html = route_file(route).read_text(encoding="utf-8")
        assert 'href="/assets/site.css"' in html
        assert 'src="/assets/site.js"' in html
        assert "cdn.tailwindcss.com" not in html
        assert "unpkg.com" not in html
        assert "fonts.googleapis.com" not in html
    assert (PUBLIC / "assets/site.css").stat().st_size > 5_000
    assert (PUBLIC / "assets/site.js").stat().st_size > 500


def test_internal_links_resolve_to_public_files() -> None:
    for route in CANONICAL_ROUTES:
        soup = BeautifulSoup(
            route_file(route).read_text(encoding="utf-8"), "html.parser"
        )
        for link in soup.select("a[href]"):
            href = link["href"].split("#", 1)[0]
            if not href or href.startswith(("http://", "https://", "mailto:")):
                continue
            assert href.startswith("/")
            if href.endswith(".html"):
                target = PUBLIC / href.lstrip("/")
            elif href == "/":
                target = PUBLIC / "index.html"
            else:
                target = PUBLIC / href.strip("/") / "index.html"
            assert target.is_file(), f"{route}: broken link {href}"


def test_offer_is_specific_truthful_and_not_self_service() -> None:
    combined = "\n".join(
        route_file(route).read_text(encoding="utf-8") for route in CANONICAL_ROUTES
    )
    required = (
        "30-day",
        "€1,500",
        "one client account",
        "five competitors",
        "up to 30 agreed public URLs",
        "Human review",
        "client-ready",
        "INMAR d.o.o.",
    )
    for phrase in required:
        assert phrase.lower() in combined.lower()
    unsupported = (
        "247 growth teams",
        "Used by growth teams worldwide",
        "From startups to enterprise",
        "We scrape daily",
        "Add any competitor URL",
        "Zero Noise",
        "SOC 2 certified",
        "ISO 27001 certified",
    )
    for claim in unsupported:
        assert claim not in combined
    assert "No published paid-client case study yet" in combined
    assert "not a client case study" in combined


def test_pricing_states_final_total_without_vat_addition() -> None:
    pricing = route_file("/pricing/").read_text(encoding="utf-8")
    pilot = route_file("/paid-pilot/").read_text(encoding="utf-8")
    assert "€1,500" in pricing and "final · one time" in pricing
    assert "not in the Croatian VAT system" in pricing
    assert "no VAT is added" in pilot
    assert "+ VAT" not in pricing
    assert "+ PDV" not in pricing
    assert "commercial hypothesis" in pricing


def test_sample_report_is_explicitly_demonstration_not_social_proof() -> None:
    sample = route_file("/sample-report/").read_text(encoding="utf-8")
    for phrase in (
        "demonstration",
        "not a client case study",
        "No claim that the positioning change improved conversion",
        "not social proof",
        "Observed change",
        "Interpretation",
        "Recommended action",
        "Confidence / limits",
    ):
        assert phrase.lower() in sample.lower()


def test_lead_form_and_privacy_disclosure_match_handler() -> None:
    pilot = route_file("/paid-pilot/").read_text(encoding="utf-8")
    privacy = route_file("/privacy/").read_text(encoding="utf-8")
    handler = (PUBLIC / "subscribe.php").read_text(encoding="utf-8")
    apache = (ROOT / "ops/apache/private-landing-state.conf").read_text(
        encoding="utf-8"
    )
    assert 'class="card form js-lead-form"' in pilot
    assert 'name="email"' in pilot
    assert "not a newsletter subscription" in pilot
    assert "automatically removed from the lead file after 90 days" in privacy
    assert "getenv('PULSEWATCH_SUBSCRIBERS_FILE') ?: ''" in handler
    assert "__DIR__ . '/subscribers.json'" not in handler
    assert "flock($handle, LOCK_EX)" in handler
    assert "90 * 24 * 60 * 60" in handler
    assert "REMOTE_ADDR" not in handler
    assert "subscribers\\.json" in apache
    assert "Require all denied" in apache


def test_ga4_is_consent_gated_and_privacy_disclosed() -> None:
    site_js = (PUBLIC / "assets/site.js").read_text(encoding="utf-8")
    privacy = route_file("/privacy/").read_text(encoding="utf-8")

    for route in CANONICAL_ROUTES:
        html = route_file(route).read_text(encoding="utf-8")
        assert 'window.PULSEWATCH_GA4_ID="G-8BCQQRSG45"' in html
        assert 'analytics_storage:"denied"' in html
        assert 'ad_storage:"denied"' in html
        assert 'class="consent-banner"' in html
        assert 'aria-live="polite"' in html
        assert '<main id="main" tabindex="-1">' in html
        assert html.count("button consent-choice") == 2
        assert "Accept analytics" in html
        assert "Reject analytics" in html
        assert 'src="https://www.googletagmanager.com' not in html

    assert "pulsewatch_analytics_consent_v1" in site_js
    assert "readConsent() !== 'granted'" in site_js
    assert "googletagmanager.com/gtag/js" in site_js
    assert "allow_google_signals: false" in site_js
    assert "allow_ad_personalization_signals: false" in site_js
    assert "deleteAnalyticsCookies" in site_js
    assert "Max-Age=0; Path=/" in site_js
    assert "settingsInvoker || document.querySelector('main')" in site_js
    assert "generate_lead" in site_js
    assert 'id="analytics"' in privacy
    assert "disabled unless you select" in privacy
    assert "two months" in privacy


def test_robots_and_sitemap_publish_only_canonical_routes() -> None:
    robots = (PUBLIC / "robots.txt").read_text(encoding="utf-8")
    assert "User-agent: *" in robots
    assert "Disallow:" not in robots
    assert "Sitemap: https://pulsewatch.top/sitemap.xml" in robots
    root = ElementTree.parse(PUBLIC / "sitemap.xml").getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text for node in root.findall("sm:url/sm:loc", ns)]
    assert urls == [f"https://pulsewatch.top{route}" for route in CANONICAL_ROUTES]
    assert len(urls) == len(set(urls))


def test_generator_is_deterministic_and_covers_sitemap_routes(tmp_path: Path) -> None:
    before = {
        p.relative_to(PUBLIC): p.read_bytes() for p in PUBLIC.rglob("*") if p.is_file()
    }
    import subprocess

    subprocess.run(
        ["python3", "scripts/build_commercial_site.py"], cwd=ROOT, check=True
    )
    after = {
        p.relative_to(PUBLIC): p.read_bytes() for p in PUBLIC.rglob("*") if p.is_file()
    }
    assert before == after


def test_google_verification_file_matches_registered_token() -> None:
    verification = (PUBLIC / "googledaf5b7b73736b24c.html").read_text(encoding="utf-8")
    assert verification == "google-site-verification: googledaf5b7b73736b24c.html\n"


def test_no_blank_or_javascript_links() -> None:
    for route in CANONICAL_ROUTES:
        html = route_file(route).read_text(encoding="utf-8")
        assert not re.search(
            r'href=["\'](?:#["\']|javascript:)', html, flags=re.IGNORECASE
        )


def test_shared_css_preserves_brand_and_component_alignment() -> None:
    css = (PUBLIC / "assets/site.css").read_text(encoding="utf-8")
    assert ".site-footer .brand{display:inline-flex;align-items:center" in css
    assert ".site-footer a:not(.brand)" in css
    assert ".price small{display:block" in css
    assert ".cta-band>.button{flex:0 0 auto}" in css
    assert ".hero-actions .button{width:100%}" in css


def test_homepage_accessibility_contract() -> None:
    html = route_file("/").read_text(encoding="utf-8")
    assert '<link rel="icon" href="/favicon.svg" type="image/svg+xml">' in html
    assert '<p class="signal-heading">Core offer repositioned</p>' in html
    assert "<h3>Core offer repositioned</h3>" not in html

    css = (PUBLIC / "assets/site.css").read_text(encoding="utf-8")
    assert ".dark .eyebrow{color:#8aa6ff}" in css

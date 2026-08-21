from pathlib import Path
from xml.etree import ElementTree

LANDING = Path(__file__).resolve().parents[1] / "public-landing" / "index.html"
PUBLIC = LANDING.parent


def test_landing_uses_current_early_access_status() -> None:
    html = LANDING.read_text(encoding="utf-8")

    assert "Early Access" in html
    assert "Launching Q2 2026" not in html
    assert "Q2 2026" not in html


def test_landing_has_canonical_indexability_and_semantics() -> None:
    html = LANDING.read_text(encoding="utf-8")

    assert '<link rel="canonical" href="https://pulsewatch.top/">' in html
    assert (
        '<meta name="robots" content="index, follow, max-image-preview:large">' in html
    )
    assert html.count("<main>") == 1
    assert html.count("</main>") == 1
    assert html.count('type="application/ld+json"') == 1
    assert '"@type": "Organization"' in html
    assert '"@type": "WebSite"' in html


def test_robots_points_to_the_canonical_sitemap() -> None:
    robots = (PUBLIC / "robots.txt").read_text(encoding="utf-8")

    assert "User-agent: *" in robots
    assert "Disallow:" not in robots
    assert "Sitemap: https://pulsewatch.top/sitemap.xml" in robots


def test_sitemap_contains_only_canonical_public_urls() -> None:
    root = ElementTree.parse(PUBLIC / "sitemap.xml").getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text for node in root.findall("sm:url/sm:loc", namespace)]

    assert urls == ["https://pulsewatch.top/"]


def test_apache_rules_canonicalize_http_and_www_without_touching_other_hosts() -> None:
    rules = (
        Path(__file__).resolve().parents[1]
        / "ops"
        / "apache"
        / "canonical-host-rewrite.conf"
    ).read_text(encoding="utf-8")

    assert "^(?:www\\.)?pulsewatch\\.top$" in rules
    assert "^www\\.pulsewatch\\.top$" in rules
    assert "%{HTTPS} !=on [OR]" in rules
    assert "https://pulsewatch.top%{REQUEST_URI}" in rules
    assert "[R=301,L,NE]" in rules

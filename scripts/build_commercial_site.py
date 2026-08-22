#!/usr/bin/env python3
"""Build the static PulseWatch commercial site from reviewed page content."""

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "public-landing"
BASE = "https://pulsewatch.top"
GA4_MEASUREMENT_ID = "G-8BCQQRSG45"

NAV = [
    ("How it works", "/how-it-works/"),
    ("Sample report", "/sample-report/"),
    ("Pricing", "/pricing/"),
    ("About", "/about/"),
]


def logo() -> str:
    return '<span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="2"/><path d="M12 12 18 7M12 3v3M21 12h-3M12 21v-3M3 12h3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></span>'


def header(current: str) -> str:
    links = "".join(
        f'<a href="{url}"{(" aria-current=page" if current == url else "")}>{label}</a>'
        for label, url in NAV
    )
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap nav">
<a class="brand" href="/">{logo()}<span>PulseWatch</span></a>
<button class="mobile-toggle" type="button" aria-expanded="false" aria-label="Open navigation"><span></span><span></span><span></span></button>
<nav class="nav-links" aria-label="Primary">{links}<a href="/contact/">Contact</a></nav>
<a class="button small" href="/paid-pilot/">Request pilot assessment</a>
</div></header>"""


def footer() -> str:
    return f"""<footer class="site-footer"><div class="wrap">
<div class="footer-grid"><div><a class="brand" href="/">{logo()}<span style="color:#fff">PulseWatch</span></a><p>Human-reviewed competitor intelligence for teams that need evidence, meaning and a next action—not another alert feed.</p></div>
<div><h3>Offer</h3><a href="/paid-pilot/">30-day paid pilot</a><a href="/pricing/">Pricing</a><a href="/sample-report/">Sample report</a></div>
<div><h3>Method</h3><a href="/how-it-works/">How it works</a><a href="/for-cro-agencies/">For CRO agencies</a><a href="/security/">Security</a></div>
<div><h3>Company</h3><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a><a href="/terms/">Website terms</a><button class="cookie-settings js-cookie-settings" type="button">Cookie settings</button></div></div>
<div class="footer-bottom"><span>© 2026 INMAR d.o.o. · PulseWatch service · Website by <a class="footer-credit" href="https://webstarthub.com/">WebStartHub</a></span><span>Gardinovec 24, 40319 Belica, Croatia</span></div>
</div></footer><section class="consent-banner" role="dialog" aria-modal="false" aria-live="polite" aria-labelledby="consent-title" hidden><div><h2 id="consent-title">Optional analytics</h2><p>With your permission, Google Analytics helps us understand site usage. We do not load analytics before you accept. See our <a href="/privacy/#analytics">privacy notice</a>.</p></div><div class="consent-actions"><button class="button consent-choice js-consent-reject" type="button">Reject analytics</button><button class="button consent-choice js-consent-accept" type="button">Accept analytics</button></div></section>"""


def schema(
    name: str, description: str, canonical: str, page_type: str = "WebPage"
) -> str:
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{BASE}/#organization",
                "name": "PulseWatch",
                "legalName": "INMAR d.o.o.",
                "url": f"{BASE}/",
            },
            {
                "@type": page_type,
                "@id": f"{canonical}#webpage",
                "url": canonical,
                "name": name,
                "description": description,
                "isPartOf": {
                    "@type": "WebSite",
                    "@id": f"{BASE}/#website",
                    "url": f"{BASE}/",
                    "name": "PulseWatch",
                },
                "about": {"@id": f"{BASE}/#organization"},
                "inLanguage": "en",
            },
        ],
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def page(
    path: str,
    title: str,
    description: str,
    body: str,
    *,
    current: str = "",
    page_type: str = "WebPage",
) -> None:
    canonical = BASE + path
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | PulseWatch</title><meta name="description" content="{escape(description, quote=True)}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:site_name" content="PulseWatch"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary"><meta name="theme-color" content="#0b1020">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"><script>window.PULSEWATCH_GA4_ID="{GA4_MEASUREMENT_ID}";window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("consent","default",{{analytics_storage:"denied",ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied",wait_for_update:500}});gtag("set","ads_data_redaction",true);</script><script type="application/ld+json">{schema(title, description, canonical, page_type)}</script></head><body>{header(current)}<main id="main" tabindex="-1">{body}</main>{footer()}<script src="/assets/site.js" defer></script></body></html>'''
    target = ROOT / ("index.html" if path == "/" else path.strip("/") + "/index.html")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")


def hero(kicker: str, title: str, lede: str) -> str:
    return f"""<section class="page-hero"><div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> / {escape(kicker)}</nav><span class="eyebrow">{escape(kicker)}</span><h1>{title}</h1><p class="lede">{lede}</p></div></section>"""


def cta(title: str = "See whether the pilot fits one client account") -> str:
    return f"""<section class="section"><div class="wrap"><div class="cta-band"><div><h2>{title}</h2><p>Tell us which decision your team needs to improve. We will reply with the scope and qualification steps.</p></div><a class="button secondary" href="/paid-pilot/#assessment">Request pilot assessment</a></div></div></section>"""


home = """<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">Operator-led competitive evidence</span><h1>Turn competitor moves<br>into client decisions.</h1><p class="lede">PulseWatch helps specialist CRO and performance agencies turn important competitor website, offer, pricing and messaging changes into reviewed evidence, decision hypotheses and client-ready next actions.</p><div class="hero-actions"><a class="button" href="/paid-pilot/">Explore the 30-day pilot</a><a class="button secondary" href="/sample-report/">Inspect the report format</a></div><p class="microcopy">Prepaid pilot · one client account · five competitors · up to 30 agreed public URLs</p></div>
<div class="signal-board" aria-label="Example reviewed signal"><div class="board-head"><div><strong>Reviewed signal</strong><div class="board-title">Illustrative report format</div></div><span class="badge reviewed">REVIEWED</span></div><div class="signal-change"><span class="badge high">HIGH RELEVANCE</span><p class="signal-heading">Core offer repositioned</p><p>The primary message moved from product automation to a managed outcome.</p><div class="comparison"><div class="snapshot"><strong>Before</strong><span>Tool-led monitoring</span></div><span>→</span><div class="snapshot"><strong>After</strong><span>Decision-ready service</span></div></div></div><div class="board-action"><small>Recommended action</small><strong>Review your own category promise and test an outcome-led hero.</strong></div></div></div></section>
<section class="trust-strip"><div class="wrap trust-grid"><div class="trust-item"><strong>Public sources only</strong><span>Agreed URLs within a bounded scope</span></div><div class="trust-item"><strong>Human reviewed</strong><span>Evidence checked before delivery</span></div><div class="trust-item"><strong>Client-ready output</strong><span>Meaning, action, owner and next step</span></div><div class="trust-item"><strong>Measured outcome</strong><span>We record whether a signal led to action</span></div></div></section>
<section class="section white"><div class="wrap split"><div><span class="eyebrow">Why PulseWatch exists</span><h2>Built from 15 years of competing for real customers.</h2><p class="lede">Founder Kristijan Fažon has spent roughly 15 years making sales, offer, pricing and positioning decisions inside his own physical print business—where a wrong assumption affects real margin, real work and real customer demand.</p><p>That experience shaped a practical rule: noticing a competitor is easy; deciding what the evidence means, what to ignore and what to test is the work that creates value. PulseWatch turns that operator discipline into a bounded evidence service for agency teams.</p><a class="text-link" href="/about/">Read the founder story and expertise boundary →</a></div><div class="card"><span class="kicker">The expertise we claim</span><h3>Commercial judgment grounded in practice</h3><ul class="checks"><li>Separating meaningful market signals from noise</li><li>Reading offers, pricing and positioning through a buyer lens</li><li>Connecting observations to a specific commercial decision</li><li>Stating uncertainty instead of presenting guesses as facts</li></ul><p class="microcopy">PulseWatch does not claim 15 years of CRO consulting. Your agency strategist retains the final client decision.</p></div></div></section>
<section class="section white"><div class="wrap"><div class="section-head"><span class="eyebrow">The gap after detection</span><h2>A page-change alert is not yet intelligence.</h2><p>Low-cost monitoring tools can detect raw differences. Your strategists still need to remove noise, prove what happened, interpret the business impact and turn the finding into something a client can approve.</p></div><div class="grid-3"><article class="card"><div class="icon">01</div><h3>Evidence before opinion</h3><p>Each material signal begins with the source URL, observed time and before/after evidence.</p></article><article class="card"><div class="icon">02</div><h3>Meaning with limits</h3><p>We explain why a change may matter and separate observable fact from interpretation.</p></article><article class="card"><div class="icon">03</div><h3>An operational next step</h3><p>The brief proposes a test or action, plus an owner and a decision checkpoint.</p></article></div></div></section>
<section class="section"><div class="wrap split"><div><span class="eyebrow">Designed for agency work</span><h2>One watchlist. One accountable decision loop.</h2><p class="lede">The first pilot is deliberately narrow so both sides can tell whether competitor intelligence changes real client work.</p><ul class="checks"><li>One ecommerce or SaaS client account</li><li>Five named competitors</li><li>Up to 30 pre-agreed public URLs</li><li>Offer, pricing, landing-page and messaging changes</li><li>Reviewed signals and a final decision session</li></ul><a class="button" href="/for-cro-agencies/">See the agency use case</a></div><div class="card"><span class="kicker">What this is not</span><ul class="checks crosses"><li>Not unlimited monitoring of the whole internet</li><li>Not a promise that every change will be detected</li><li>Not automated strategic truth generated by AI</li><li>Not a replacement for your client strategist</li><li>Not mass SKU repricing or legal intelligence</li></ul></div></div></section>
<section class="section dark"><div class="wrap"><div class="section-head center"><span class="eyebrow">Workflow</span><h2>From watchlist to client decision</h2><p>The operator remains responsible for reviewing the signal and its evidence.</p></div><div class="grid-4"><div class="card step"><span class="step-num">STEP 01</span><h3>Scope</h3><p>Agree competitors, URLs, materiality and decisions.</p></div><div class="card step"><span class="step-num">STEP 02</span><h3>Capture</h3><p>Observe source changes and preserve the evidence.</p></div><div class="card step"><span class="step-num">STEP 03</span><h3>Review</h3><p>Check relevance, confidence and likely impact.</p></div><div class="card step"><span class="step-num">STEP 04</span><h3>Act</h3><p>Assign a test or action and record the outcome.</p></div></div><p class="center" style="margin-top:30px"><a class="button secondary" href="/how-it-works/">Read the full method</a></p></div></section>
<section class="section white"><div class="wrap split"><div><span class="eyebrow">Commercial clarity</span><h2>A fixed, prepaid validation—not an open-ended consultancy.</h2><p class="lede">The 30-day Agency Design-Partner Pilot costs €1,500 as a final total price, paid upfront. The purpose is to prove whether at least one reviewed signal reaches a documented client decision or action.</p><a class="button" href="/pricing/">View scope and pricing</a></div><div class="card pricing"><span class="badge reviewed">AVAILABLE</span><h3>Agency Design-Partner Pilot</h3><div class="price">€1,500 <small>final · once</small></div><ul class="checks"><li>30 calendar days</li><li>Kickoff and watchlist definition</li><li>Reviewed material signals</li><li>Client-ready evidence brief</li><li>Final decision and value recap</li></ul></div></div></section>
<section class="section"><div class="wrap"><div class="section-head center"><span class="eyebrow">Questions before buying</span><h2>Clear scope, including the limits.</h2></div><div class="faq"><details><summary>Is PulseWatch a self-service SaaS platform?</summary><p>No. The current offer is an operator-led managed pilot. There is no claim of production-ready self-service onboarding, billing or dashboard access.</p></details><details><summary>Do you monitor any URL a client adds?</summary><p>No. Sources are agreed during kickoff. The pilot covers up to 30 public URLs across five named competitors.</p></details><details><summary>Does every detected change become an alert?</summary><p>No. Changes are reviewed against agreed materiality rules. Delivery cadence and channel are agreed for the pilot.</p></details><details><summary>What makes the pilot successful?</summary><p>At least one signal must contribute to a documented decision or action, and the buyer must see enough value to discuss continuation. If the workflow does not help, we do not recommend expanding it.</p></details></div></div></section>""" + cta()
page(
    "/",
    "Managed competitor monitoring for CRO agencies",
    "Human-reviewed competitor monitoring that turns website, pricing, offer and messaging changes into client-ready evidence and next actions.",
    home,
)

pilot = (
    hero(
        "Paid pilot",
        "Prove the decision value in 30 days.",
        "A fixed-scope, prepaid engagement for one agency client account. Operator-reviewed evidence supports the agency strategist; the goal is to test whether a competitor signal improves a real decision.",
    )
    + """<section class="section white"><div class="wrap split"><div><span class="eyebrow">Included</span><h2>A bounded operating scope.</h2><ul class="checks"><li>One client account and one named agency owner</li><li>Five competitors and up to 30 agreed public URLs</li><li>Monitoring of offers, pricing, landing pages and messaging</li><li>Human review against agreed materiality rules</li><li>Evidence briefs with fact, interpretation, recommendation and owner</li><li>Kickoff plus final decision/value recap</li></ul></div><div class="card pricing"><span class="badge reviewed">30 DAYS</span><h3>Agency Design-Partner Pilot</h3><div class="price">€1,500 <small>final · paid upfront</small></div><p>The price is the final total for this defined pilot. INMAR d.o.o. is not in the Croatian VAT system; no VAT is added.</p><a class="button" href="#assessment">Request assessment</a></div></div></section>
<section class="section"><div class="wrap"><div class="section-head"><span class="eyebrow">Pass / stop contract</span><h2>Success is an action—not an activity count.</h2></div><div class="grid-2"><article class="card"><span class="kicker">PASS</span><h3>A signal changes real work</h3><p>At least one reviewed signal is used in a documented client decision, test or action, and the buyer wants to discuss a continued workflow.</p></article><article class="card"><span class="kicker" style="color:var(--amber)">STOP</span><h3>The workflow does not earn continuation</h3><p>No useful decision emerges, there is no action owner, the sources cannot provide reliable evidence, or the buyer actually needs a low-cost self-service tool.</p></article></div></div></section>
<section class="section white"><div class="wrap"><div class="section-head"><span class="eyebrow">Timeline</span><h2>What happens during the month</h2></div><div class="grid-4"><div class="card"><span class="step-num">DAYS 1–3</span><h3>Kickoff</h3><p>Choose the client, sources, decision themes, owner and thresholds.</p></div><div class="card"><span class="step-num">WEEK 1</span><h3>Baseline</h3><p>Capture the initial source state and agree the brief format.</p></div><div class="card"><span class="step-num">WEEKS 2–4</span><h3>Review loop</h3><p>Review material signals and deliver evidence at the agreed cadence.</p></div><div class="card"><span class="step-num">DAY 30</span><h3>Decision recap</h3><p>Review actions, misses, false positives, human effort and next-step fit.</p></div></div></div></section>
<section class="section" id="assessment"><div class="wrap split"><div><span class="eyebrow">Qualification</span><h2>Request a pilot assessment.</h2><p class="lede">Submit a work email. We will send the scope questions and check whether one client account has a decision this pilot can realistically support.</p><p class="microcopy">This is a pilot enquiry, not a newsletter subscription. Unconverted enquiries are removed after 90 days.</p></div><form class="card form js-lead-form"><div class="field"><label for="pilot-email">Work email</label><input id="pilot-email" name="email" type="email" autocomplete="email" required placeholder="you@agency.com"></div><button class="button" type="submit">Request pilot assessment</button><div class="form-message" aria-live="polite"></div><p class="microcopy">By submitting, you acknowledge the <a href="/privacy/">privacy notice</a>.</p></form></div></section>"""
)
page(
    "/paid-pilot/",
    "30-day competitor monitoring pilot",
    "A €1,500 prepaid, fixed-scope competitor monitoring pilot for one CRO or performance agency client account.",
    pilot,
    current="/paid-pilot/",
    page_type="Service",
)

how = (
    hero(
        "How it works",
        "Evidence first. Interpretation second. Action third.",
        "PulseWatch applies an operator method shaped by 15 years of real sales and market decisions, while showing exactly where observation ends, judgment begins and the agency's responsibility remains.",
    )
    + """<section class="section white"><div class="wrap"><div class="grid-3"><article class="card"><div class="icon">1</div><h3>Define the decision</h3><p>We start with a named business decision, an agency owner and the competitor moves that could change the client plan.</p></article><article class="card"><div class="icon">2</div><h3>Bind the sources</h3><p>We agree named competitors and public URLs. This prevents an unbounded, noisy monitoring promise.</p></article><article class="card"><div class="icon">3</div><h3>Preserve the observation</h3><p>The brief records the URL, observation time, before/after state and what was directly visible.</p></article><article class="card"><div class="icon">4</div><h3>Review materiality</h3><p>An operator checks whether the change meets the agreed threshold and assigns confidence and relevance.</p></article><article class="card"><div class="icon">5</div><h3>Recommend an action</h3><p>The signal becomes a specific question, test or response with an owner—not a vague instruction to copy a competitor.</p></article><article class="card"><div class="icon">6</div><h3>Record the outcome</h3><p>We track whether the buyer dismissed, discussed, tested or acted on the signal and why.</p></article></div></div></section>
<section class="section"><div class="wrap split"><div><span class="eyebrow">Evidence model</span><h2>Every brief separates four layers.</h2></div><div class="table-wrap"><table><thead><tr><th>Layer</th><th>Question</th><th>Required output</th></tr></thead><tbody><tr><td><strong>Observation</strong></td><td>What visibly changed?</td><td>Source, time, before/after evidence</td></tr><tr><td><strong>Interpretation</strong></td><td>Why might it matter?</td><td>Reasoning, confidence and limits</td></tr><tr><td><strong>Recommendation</strong></td><td>What should the client consider?</td><td>Bounded test or action</td></tr><tr><td><strong>Outcome</strong></td><td>Did the signal affect work?</td><td>Status, owner, date and result note</td></tr></tbody></table></div></div></section>
<section class="section dark"><div class="wrap split"><div><span class="eyebrow">Human responsibility</span><h2>Automation may capture. It does not become the source of truth.</h2><p class="lede">Kristijan reviews material evidence through the practical lens developed in his own sales and print business. Recommendations remain hypotheses for the agency strategist to evaluate in the client's context.</p></div><div class="card"><h3>Known limits</h3><ul class="checks crosses"><li>Public sites can block or change access</li><li>Dynamic pages can create false differences</li><li>A source may change between observations</li><li>Competitor intent cannot be inferred as fact</li><li>No monitoring process guarantees complete detection</li></ul></div></div></section>"""
    + cta("See the evidence format before committing")
)
page(
    "/how-it-works/",
    "How PulseWatch competitor monitoring works",
    "The evidence, human review, recommendation and outcome method behind PulseWatch managed competitor monitoring.",
    how,
    current="/how-it-works/",
)

sample = (
    hero(
        "Sample report",
        "A transparent example of the deliverable.",
        "This demonstration uses a real change previously made to PulseWatch's own public homepage. It shows the report structure; it is not a client case study and makes no claim of customer results.",
    )
    + """<section class="section white"><div class="wrap"><article class="report"><div class="report-toolbar"><strong>Reviewed competitor signal · demonstration</strong><span>PW-DEMO-001</span></div><div class="report-body"><span class="badge reviewed">REVIEWED</span> <span class="badge high">HIGH RELEVANCE</span><h2>Homepage repositioned from tool-led automation to managed decision support</h2><dl><div class="report-row"><dt>Source</dt><dd>PulseWatch public homepage (used as a self-demonstration source)</dd></div><div class="report-row"><dt>Observed change</dt><dd>The headline and offer moved away from broad “AI-powered competitor monitoring” language toward a bounded managed service for CRO and performance agencies.</dd></div><div class="report-row"><dt>Before evidence</dt><dd>Tool-led positioning included unsupported self-service, daily-monitoring and adoption implications. Those claims were removed during the commercial foundation revision.</dd></div><div class="report-row"><dt>After evidence</dt><dd>The public offer now names one client account, five competitors, up to 30 agreed public URLs, human review and client-ready next actions.</dd></div><div class="report-row"><dt>Interpretation</dt><dd><strong>Fact:</strong> the visible offer and scope changed. <strong>Hypothesis:</strong> the new framing may reduce ambiguity for an agency buyer evaluating a managed pilot.</dd></div><div class="report-row"><dt>Recommended action</dt><dd>Compare your own hero promise against the buyer's operational outcome. Draft one outcome-led variant and test comprehension with qualified prospects before changing the live page.</dd></div><div class="report-row"><dt>Owner / checkpoint</dt><dd>Agency strategist · review at the next client planning session.</dd></div><div class="report-row"><dt>Confidence / limits</dt><dd>High confidence in the observed copy change. No claim that the positioning change improved conversion; revenue impact remains unproven.</dd></div></dl></div></article></div></section>
<section class="section"><div class="wrap"><div class="section-head"><span class="eyebrow">What the client receives</span><h2>Enough structure to audit the recommendation.</h2></div><div class="grid-4"><div class="card"><h3>Evidence</h3><p>Source URL, time and preserved before/after state.</p></div><div class="card"><h3>Materiality</h3><p>Relevance, severity and why the signal passed review.</p></div><div class="card"><h3>Action</h3><p>A bounded recommendation, owner and checkpoint.</p></div><div class="card"><h3>Limits</h3><p>Confidence plus what the evidence does not prove.</p></div></div></div></section>
<section class="section white"><div class="wrap"><div class="notice"><strong>Truthfulness note:</strong> This is an operating-format demonstration, not social proof. PulseWatch has not published a paid customer case study, conversion uplift or recurring-customer result.</div></div></section>"""
    + cta()
)
page(
    "/sample-report/",
    "Competitor monitoring sample report",
    "See an honest PulseWatch sample report with evidence, interpretation, recommendation, owner, confidence and explicit limits.",
    sample,
    current="/sample-report/",
)

pricing = (
    hero(
        "Pricing",
        "A fixed pilot price with a visible scope.",
        "Start with a 30-day proof of value. A continued managed service is discussed only after the pilot shows a repeatable decision workflow.",
    )
    + """<section class="section white"><div class="wrap"><div class="grid-2"><article class="card pricing"><span class="badge reviewed">START HERE</span><h2>Agency Design-Partner Pilot</h2><div class="price">€1,500 <small>final · one time</small></div><p>Paid upfront for a defined 30-day scope.</p><ul class="checks"><li>One client account</li><li>Five competitors</li><li>Up to 30 agreed public URLs</li><li>Kickoff, reviewed signals and final decision recap</li><li>Client-ready report format</li></ul><a class="button" href="/paid-pilot/#assessment">Request assessment</a></article><article class="card"><span class="badge">AFTER VALIDATION</span><h2>Managed Agency Desk</h2><div class="price">€1,490 <small>final / month hypothesis</small></div><p>A possible three-month managed continuation for one validated client watchlist, up to 50 URLs, reviewed delivery and a monthly decision session.</p><div class="notice" style="margin-top:20px">This recurring price and package are a commercial hypothesis, not proof of market acceptance. A specific proposal follows only after a successful pilot.</div></article></div></div></section>
<section class="section"><div class="wrap"><div class="section-head"><span class="eyebrow">Price context</span><h2>What the pilot price covers</h2><p>It pays for source scoping, monitored evidence handling, operator review, recommendation work, delivery and the final value decision—not merely software access.</p></div><div class="grid-3"><div class="card"><h3>Set-up</h3><p>Decision mapping, competitor selection, URL list and materiality rules.</p></div><div class="card"><h3>Operating work</h3><p>Capture review, evidence verification, interpretation and briefing.</p></div><div class="card"><h3>Learning</h3><p>Outcome tracking, false-positive review and continuation decision.</p></div></div></div></section>
<section class="section white"><div class="wrap split"><div><span class="eyebrow">Billing clarity</span><h2>No hidden VAT addition.</h2><p class="lede">INMAR d.o.o. is not in the Croatian VAT system. The prices shown here are final totals for the stated scope, without an additional VAT charge.</p></div><div class="card"><h3>Outside the stated scope</h3><ul class="checks crosses"><li>More competitors or URLs</li><li>Private/authenticated sources</li><li>Mass product-catalogue repricing</li><li>Custom software integrations</li><li>Legal, security or financial advice</li></ul><p>Any different work requires a separate written proposal.</p></div></div></section>"""
    + cta()
)
page(
    "/pricing/",
    "PulseWatch pricing",
    "Transparent pricing for the €1,500 PulseWatch agency design-partner pilot and the unvalidated managed-service hypothesis.",
    pricing,
    current="/pricing/",
    page_type="Service",
)

agency = (
    hero(
        "For CRO agencies",
        "Make competitor changes usable in client work.",
        "PulseWatch is designed for specialist CRO and performance teams that manage several ecommerce or SaaS clients but do not want strategists spending hours checking competitor pages and cleaning raw alerts.",
    )
    + """<section class="section white"><div class="wrap"><div class="section-head"><span class="eyebrow">Best fit</span><h2>The pilot works only when a signal can change a decision.</h2></div><div class="grid-3"><div class="card"><h3>Named strategist</h3><p>A client lead can judge relevance and own the next action.</p></div><div class="card"><h3>Active optimisation rhythm</h3><p>The client already maintains a test, campaign or landing-page backlog.</p></div><div class="card"><h3>Observable competitor set</h3><p>Five competitors expose useful public offers, pricing or messages.</p></div></div></div></section>
<section class="section"><div class="wrap split"><div><span class="eyebrow">Agency workflow</span><h2>Use the output without forwarding a raw diff.</h2><ul class="checks"><li>Add a reviewed signal to the weekly client agenda</li><li>Turn it into a research question or A/B test hypothesis</li><li>Assign an owner and decision date</li><li>Preserve evidence for later outcome review</li><li>Reject low-confidence signals without client noise</li></ul></div><div class="card"><h3>Example decision themes</h3><p><strong>Offer:</strong> Did a competitor change risk reversal, packaging or urgency?</p><p><strong>Pricing:</strong> Did plan structure, discount framing or trial language move?</p><p><strong>Landing page:</strong> Did the value proposition, proof or CTA hierarchy change?</p><p><strong>Messaging:</strong> Is a new segment, use case or objection being prioritised?</p></div></div></section>
<section class="section dark"><div class="wrap"><div class="section-head"><span class="eyebrow">Not a fit</span><h2>We will say no when the scope cannot prove value.</h2></div><div class="grid-3"><div class="card"><h3>No action owner</h3><p>Interesting observations alone cannot pass the pilot.</p></div><div class="card"><h3>Unlimited coverage request</h3><p>The pilot is bounded to named competitors and URLs.</p></div><div class="card"><h3>Commodity alert need</h3><p>If simple page alerts solve the job, a low-cost tool is more appropriate.</p></div></div></div></section>"""
    + cta()
)
page(
    "/for-cro-agencies/",
    "Competitor monitoring for CRO agencies",
    "Managed, human-reviewed competitor monitoring for specialist CRO and performance agencies working across ecommerce or SaaS clients.",
    agency,
)

about = (
    hero(
        "About",
        "Built by an operator, not invented around a dashboard.",
        "PulseWatch turns 15 years of hands-on sales, offer and competitor observation in a real production business into a disciplined evidence service for agency teams.",
    )
    + """<section class="section white"><div class="wrap split"><div><span class="eyebrow">The founder story</span><h2>Fifteen years learning what competitors can—and cannot—tell you.</h2><p class="lede">For roughly 15 years, Kristijan Fažon has done his own sales and commercial decision-making in the physical print business. He has watched competitors change prices, packages, messages and offers while customers changed what they asked for and what they bought.</p><p>This was not academic research or detached consulting. Decisions affected his own workload, margin and customer relationships. Over time, the useful skill became less about collecting more information and more about identifying which public signals deserve attention, which are noise and which justify a response.</p><p>PulseWatch packages that discipline for agencies: preserve the evidence, explain the commercial reading, expose uncertainty and hand the agency strategist a concrete question or next action.</p></div><div class="card"><span class="kicker">A precise claim</span><h3>Practical commercial expertise—not borrowed credentials.</h3><p>Kristijan is an experienced business operator who has spent roughly 15 years applying competitor, offer, pricing and customer observations in his own work.</p><p>PulseWatch does not present that as 15 years of formal CRO consulting, claim guaranteed growth outcomes or replace the agency's specialist judgment.</p></div></div></section>
<section class="section"><div class="wrap"><div class="section-head"><span class="eyebrow">The operator method</span><h2>What experience changes in the work</h2><p>The founder story matters only if it creates a better deliverable. These are the operating habits the pilot applies.</p></div><div class="grid-4"><div class="card"><div class="icon">01</div><h3>Start with the buyer</h3><p>Read the change through the customer's likely question, objection or decision—not through novelty alone.</p></div><div class="card"><div class="icon">02</div><h3>Protect the margin</h3><p>Do not recommend matching a competitor until the trade-off, positioning and commercial consequence are visible.</p></div><div class="card"><div class="icon">03</div><h3>Discard the noise</h3><p>A changed page is not automatically a meaningful market move. Low-value differences stay out of the client brief.</p></div><div class="card"><div class="icon">04</div><h3>Make one decision possible</h3><p>Every delivered signal should support a concrete test, discussion or action with a named owner.</p></div></div></div></section>
<section class="section white"><div class="wrap split"><div><span class="eyebrow">Accountability</span><h2>Named company. Named operating responsibility.</h2><p class="lede">PulseWatch is provided by INMAR d.o.o., Gardinovec 24, 40319 Belica, Croatia. During the design-partner phase, Kristijan controls critical signal review and final delivery.</p><p>That direct involvement is an operating fact for the current pilot, not a claim that the service has a large analyst team or enterprise coverage.</p></div><div class="card"><h3>Current stage</h3><ul class="checks"><li>Managed design-partner pilot available</li><li>Public, agreed sources only</li><li>Human review before delivery</li><li>No published paid-client case study yet</li><li>No production-ready self-service SaaS claim</li></ul></div></div></section>
<section class="section"><div class="wrap"><div class="section-head"><span class="eyebrow">Operating principles</span><h2>What we are building around</h2></div><div class="grid-3"><div class="card"><h3>Truth over theatre</h3><p>No invented customer logos, subscriber counts, urgency or unsupported automation claims.</p></div><div class="card"><h3>Evidence over alerts</h3><p>A signal should be inspectable and its uncertainty should remain visible.</p></div><div class="card"><h3>Paid value over feature volume</h3><p>New software follows a repeated, paid workflow—not the other way around.</p></div></div></div></section>"""
    + cta("Discuss a bounded design-partner pilot")
)
page(
    "/about/",
    "About PulseWatch and INMAR d.o.o.",
    "PulseWatch is an operator-led competitor-intelligence service built from 15 years of practical sales and market observation in a real business.",
    about,
    current="/about/",
    page_type="AboutPage",
)

contact = (
    hero(
        "Contact",
        "Start with the decision—not a feature list.",
        "Use the pilot assessment for a commercial enquiry, or contact INMAR directly for company, privacy or security matters.",
    )
    + """<section class="section white"><div class="wrap grid-2"><article class="card"><span class="kicker">Pilot enquiry</span><h2>Request the qualification questions</h2><p>Use the short assessment form. We will ask about the client account, five competitors, source URLs, decision owner and the action the pilot should support.</p><a class="button" href="/paid-pilot/#assessment">Request pilot assessment</a></article><article class="card"><span class="kicker">Company contact</span><h2>INMAR d.o.o.</h2><p>Gardinovec 24<br>40319 Belica<br>Croatia</p><p>For general, privacy or security enquiries, use the verified contact route on the INMAR corporate website.</p><a class="button secondary" href="https://inmar.hr/#contact" rel="noopener">Open INMAR contact form</a></article></div></section>
<section class="section"><div class="wrap"><div class="notice"><strong>Response expectation:</strong> We review fit manually and do not promise instant or 24/7 response. The first reply will clarify scope before any proposal or payment request.</div></div></section>"""
)
page(
    "/contact/",
    "Contact PulseWatch",
    "Contact PulseWatch for a managed competitor-monitoring pilot or reach INMAR d.o.o. for company, privacy and security matters.",
    contact,
    current="/contact/",
    page_type="ContactPage",
)

security = (
    hero(
        "Security",
        "Public sources in. Restricted lead data out.",
        "This page documents controls that are currently implemented for the public PulseWatch site and pilot-enquiry path. It does not claim certifications we do not hold.",
    )
    + """<section class="section white"><div class="wrap"><div class="grid-3"><div class="card"><h3>Restricted lead storage</h3><p>Pilot-enquiry emails are stored server-side outside the public document root with restricted file permissions.</p></div><div class="card"><h3>Minimal form data</h3><p>The enquiry handler stores the submitted work email and time. It does not intentionally record the sender's IP address.</p></div><div class="card"><h3>Retention control</h3><p>Unconverted enquiries are removed from the lead file after 90 days.</p></div><div class="card"><h3>Concurrent-write protection</h3><p>The lead file uses exclusive locking and duplicate-email handling.</p></div><div class="card"><h3>Secret scanning</h3><p>The repository CI checks tracked files for prohibited environment files and high-confidence secret patterns.</p></div><div class="card"><h3>Public source boundary</h3><p>The current pilot is limited to agreed public URLs; it does not request competitor credentials or private access.</p></div></div></div></section>
<section class="section"><div class="wrap split"><div><span class="eyebrow">No certification theatre</span><h2>Controls are described narrowly.</h2><p class="lede">PulseWatch does not claim SOC 2, ISO 27001, penetration-test certification, perfect detection or immunity from security incidents.</p></div><div class="card"><h3>Report a concern</h3><p>Use the INMAR company contact form and identify the message as a PulseWatch security report. Do not send passwords, access tokens or exploit data through the public pilot form.</p><a class="button secondary" href="https://inmar.hr/#contact" rel="noopener">Contact INMAR</a></div></div></section>"""
)
page(
    "/security/",
    "PulseWatch security controls",
    "Implemented security and privacy controls for the PulseWatch public site and managed-pilot enquiry process.",
    security,
)

privacy = (
    hero(
        "Privacy",
        "PulseWatch pilot enquiry privacy notice",
        "How INMAR d.o.o. processes pilot enquiries and optional website analytics. Last updated 21 August 2026.",
    )
    + """<section class="section white"><div class="wrap legal"><div class="notice"><strong>Controller:</strong> INMAR d.o.o., Gardinovec 24, 40319 Belica, Croatia. Use the <a href="https://inmar.hr/#contact">INMAR contact form</a> for privacy, access or deletion requests.</div><h2>Pilot enquiry data</h2><p>The managed-pilot enquiry form stores the work email address you submit and the submission time. The form does not intentionally store your IP address. We use the address only to review fit, send requested pilot information and answer related pre-contract questions. We do not sell submitted contact data.</p><h2 id="analytics">Optional Google Analytics</h2><p>Google Analytics 4 is disabled unless you select “Accept analytics”. If accepted, it may process page views, interactions, approximate location, device and browser information, referring pages and pseudonymous identifiers. We do not send your pilot-enquiry email address or form contents to Google Analytics.</p><p>Analytics is based on your consent. Rejecting it does not limit site access. Your choice is stored in your browser's local storage so the site can respect it. You can withdraw or change the choice at any time through “Cookie settings” in the footer; withdrawal stops future collection from that browser.</p><p>Google Ireland Limited provides Google Analytics for users in the EEA. Google may process data through systems outside the EEA under its applicable transfer safeguards. See <a href="https://policies.google.com/privacy" rel="noopener">Google's privacy policy</a> and <a href="https://support.google.com/analytics/answer/12017362" rel="noopener">Google Analytics privacy controls</a>.</p><h2>Retention</h2><p>Unconverted pilot enquiries are automatically removed from the lead file after 90 days. Google Analytics user-level event data is configured for the shortest available retention period of two months. Aggregated reports may remain available longer. If you become a client, information needed for the service, contract, accounting or legal obligations is handled under the relevant client documentation and retention rules.</p><h2>Service providers and access</h2><p>The lead file is stored in restricted server-side storage and is not intended to be publicly accessible. Access is limited to people and service providers needed to operate the site, hosting and enquiry process. Google receives analytics data only after consent; it does not receive the private lead file.</p><h2>Your choices and rights</h2><p>You may ask whether we hold your enquiry, request a copy or correction, object to processing, withdraw consent, or request deletion where applicable. Submit the request through the INMAR contact form linked above. You may also complain to the competent data-protection authority.</p><h2>No marketing subscription</h2><p>Submitting the pilot form is not consent to an unrelated marketing newsletter. Any future marketing subscription must use a separate, explicit choice.</p></div></section>"""
)
page(
    "/privacy/",
    "Privacy notice",
    "How INMAR d.o.o. processes managed-pilot enquiries and consent-based Google Analytics data on PulseWatch.",
    privacy,
)
# Keep the published legacy URL available, but canonicalise it to the clean route.
legacy = (
    (ROOT / "privacy" / "index.html")
    .read_text(encoding="utf-8")
    .replace(
        f'<link rel="canonical" href="{BASE}/privacy/">',
        f'<link rel="canonical" href="{BASE}/privacy/">',
    )
    .replace('href="/assets/site.css"', 'href="/assets/site.css"')
)
(ROOT / "privacy.html").write_text(legacy, encoding="utf-8")

terms = (
    hero(
        "Website terms",
        "Clear boundaries for this public site.",
        "These terms govern use of the public PulseWatch website. A paid pilot is governed by its separate written scope, proposal and applicable commercial documentation. Last updated 21 August 2026.",
    )
    + """<section class="section white"><div class="wrap legal"><h2>Provider</h2><p>This website and the PulseWatch service are operated by INMAR d.o.o., Gardinovec 24, 40319 Belica, Croatia.</p><h2>Informational website</h2><p>Website content explains the current managed-pilot offer. It is not a guarantee of availability, detection completeness, commercial results or fitness for a particular client decision.</p><h2>No contract from form submission</h2><p>Submitting an enquiry does not create a service contract, reserve capacity or require payment. A service begins only after both parties accept a separate written scope and the agreed upfront payment is received.</p><h2>Public-source boundary</h2><p>The described pilot concerns agreed publicly accessible competitor URLs. Buyers remain responsible for lawful use of the resulting information and for their own client, advertising, pricing and commercial decisions.</p><h2>Recommendations are hypotheses</h2><p>A PulseWatch recommendation is a decision-support hypothesis, not legal, financial, security or guaranteed growth advice. Competitor intent and business impact cannot be known from a public page change alone.</p><h2>Intellectual property and acceptable use</h2><p>You may read and link to public pages for normal business evaluation. Do not interfere with the site, attempt unauthorised access, submit malicious content or falsely represent PulseWatch material as a customer result.</p><h2>Changes and contact</h2><p>We may update this public website and these terms as the service evolves. Material pilot obligations belong in the signed commercial scope. Questions can be sent through the <a href="https://inmar.hr/#contact">INMAR contact form</a>.</p></div></section>"""
)
page(
    "/terms/",
    "Website terms",
    "Public website terms for PulseWatch, operated by INMAR d.o.o., including service, source and recommendation boundaries.",
    terms,
)

# Sitemap generated from canonical public routes.
routes = [
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
urlset = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
urlset.extend(f"  <url><loc>{BASE}{route}</loc></url>" for route in routes)
urlset.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(urlset) + "\n", encoding="utf-8")
print(f"built {len(routes)} canonical pages")

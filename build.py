#!/usr/bin/env python3
"""
Airlogical marketing site generator.

Emits a pure-static, multi-page site (no build step on the host — Vercel
just serves the files). Run `python3 build.py` to regenerate all HTML +
SEO assets (sitemap, robots, llms.txt, styles, icons).

Design language mirrors sealogical.com (Ubuntu + Ubuntu Mono, navy
#034566 / orange #F6881C, terminal/CLI motif). Every page ships:
title/description/canonical, Open Graph + Twitter, and JSON-LD
(Organization + WebSite site-wide; SoftwareApplication / FAQPage /
HowTo / BreadcrumbList / BlogPosting where relevant) — the SEO/AEO/GEO
foundation.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.airlogical.com"
APP = "https://app.airlogical.com"
ORG = "Airlogical"
TAGLINE = "Aircraft management software for private and business aviation"
UPDATED = "2026-07-11"

NAVY = "#034566"; ORANGE = "#F6881C"; TEAL = "#47D5C6"

# ── module data (rich per-module content) ───────────────────────────────────
from content_modules import MODULES  # noqa: E402

# ── site-wide FAQ (home + /faq) ──────────────────────────────────────────────
SITE_FAQS = [
    ("What is aircraft management software?",
     "Aircraft management software is a single platform that manages the operations, compliance, maintenance and finances of an aircraft — crew records, certificates, trips, maintenance, safety and owner reporting — replacing the spreadsheets and separate tools a flight department would otherwise juggle."),
    ("What does Airlogical do?",
     "Airlogical is aircraft management software for private and business aviation. It covers eight connected areas — aircraft, crew, certificates, operations, technical, safety, finance and compliance — as one shared source of truth."),
    ("Who is Airlogical for?",
     "Airlogical is built for flight departments and aircraft management companies operating private and business aircraft — from a single owner-flown aircraft to a managed fleet."),
    ("How is Airlogical different from FL3XX or Leon?",
     "FL3XX and Leon are charter-first operations platforms. Airlogical is a consolidated platform that combines operations, maintenance, safety, crew and owner-facing finance for private and business operators — with owner-transparent cost reporting built in."),
    ("Does Airlogical support Part 91 and Part 135 (and EASA) operations?",
     "Yes. Airlogical is designed around private and business aviation compliance, including operational categories such as NCO, NCC, SPO and commercial, and evaluates crew and flight-time limitations accordingly."),
    ("How does Airlogical track flight-time limitations (FTL)?",
     "Airlogical records crew duty periods and flight time and evaluates them against the applicable FTL rules, flagging crew approaching or exceeding limits at the point of assignment and across the fleet schedule."),
    ("Can aircraft owners see their costs?",
     "Yes. Airlogical provides owner-grade statements, a secure owner portal, and pre-trip cost estimates so owners can see what a trip will cost before it flies."),
    ("Is Airlogical suitable for a single-aircraft operator?",
     "Yes. Airlogical scales from a single aircraft to a managed fleet, with unlimited users on every account."),
    ("How much does Airlogical cost?",
     "Airlogical is priced per aircraft and includes unlimited users. Request a quote for pricing tailored to your operation."),
    ("Who makes Airlogical?",
     "Airlogical is built by the team behind Sealogical, the yacht-management platform trusted in fleet management since 2003."),
]

# ── blog posts ───────────────────────────────────────────────────────────────
BLOG = [
    dict(slug="what-is-aircraft-management-software",
         title="What is aircraft management software?",
         desc="A plain-English guide to what aircraft management software does, who needs it, and what to look for — for private and business aviation.",
         date="2026-07-11",
         body="""
<p class="lead">Aircraft management software is a single platform that manages the operations, compliance, maintenance and finances of an aircraft in one place — replacing the spreadsheets, inboxes and separate tools a flight department would otherwise juggle.</p>
<p>For a private or business aircraft, an enormous amount has to be tracked: crew licences and medicals, certificates and checks, maintenance and airworthiness, every trip, and the costs that follow. When that lives across disconnected tools, things slip — and in aviation the things that slip are the things that ground you.</p>
<h2>What it covers</h2>
<p>Good aircraft management software brings these threads together:</p>
<ul>
<li><strong>Crew</strong> — profiles, licences and ratings, medicals, recency and currency, and flight-time limitations (FTL).</li>
<li><strong>Certificates</strong> — aircraft, crew and company certificates in one register with expiry tracking.</li>
<li><strong>Operations</strong> — trips, dispatch, handling, permits and crew assignment.</li>
<li><strong>Technical</strong> — the maintenance log, life-limited components and Airworthiness Directive (AD) compliance.</li>
<li><strong>Safety</strong> — a safety management system (SMS): reports, hazards, risk assessments and corrective actions.</li>
<li><strong>Finance</strong> — standing and per-leg costs, budgets and owner statements.</li>
<li><strong>Compliance</strong> — a live forecast of everything coming due across the fleet.</li>
</ul>
<h2>Who needs it</h2>
<p>Flight departments, aircraft management companies and owner-operators of private and business aircraft. It scales from a single owner-flown aircraft to a managed fleet.</p>
<h2>What to look for</h2>
<p>Choose a platform that is purpose-built for aviation (not a generic tool bent into shape), keeps one source of truth across crew, aircraft and finance, and lets you prove compliance with an exportable history. Owner-facing cost transparency is a strong differentiator for managed aircraft.</p>
<p>Airlogical is aircraft management software for private and business aviation that does exactly this — eight connected modules, one shared source of truth. <a href="/">See how it works</a>.</p>
""",
         faqs=[("Is aircraft management software only for large fleets?",
                "No. It scales from a single owner-flown aircraft to a managed fleet; the value is in consolidating crew, compliance, maintenance and finance regardless of size."),
               ("Does aircraft management software replace maintenance tracking?",
                "It can. Airlogical includes maintenance logging, life-limited components and AD compliance, so a separate maintenance tracker may not be needed for many private and business operators.")]),
    dict(slug="flight-time-limitations-ftl-explained",
         title="Flight-time limitations (FTL) explained",
         desc="What flight-time limitations are, why they matter, and how software helps operators keep crew legal — a plain-English guide for private and business aviation.",
         date="2026-07-11",
         body="""
<p class="lead">Flight-time limitations (FTL) are the rules that cap how long crew may be on duty and flying within given windows, to manage fatigue. They limit flight duty period (FDP), total flight time and duty, and require minimum rest.</p>
<h2>Why FTL matters</h2>
<p>Fatigue is a flight-safety risk, so regulators limit duty and flight time and mandate rest. Operators must not roster or dispatch a crew member beyond their limits — doing so is both a safety and a compliance failure.</p>
<h2>The core limits</h2>
<ul>
<li><strong>Flight duty period (FDP)</strong> — the maximum duty window that includes flying, varying with report time and number of sectors.</li>
<li><strong>Cumulative flight time and duty</strong> — rolling limits over 7 days, 28 days and 12 months.</li>
<li><strong>Minimum rest</strong> — the rest required before the next duty, extended after long or disruptive duties.</li>
</ul>
<h2>How software helps</h2>
<p>Tracking FTL by hand is error-prone. Software records each duty period and flight, computes the rolling windows, and — crucially — checks limits <em>at the moment of assignment</em>, so a dispatcher sees before they commit whether a crew member would breach FDP, cumulative limits or rest.</p>
<p>Airlogical evaluates FTL across the fleet schedule and flags crew approaching or exceeding their limits, alongside licence, medical and recency checks. <a href="/modules/crew">See the Crew module</a>.</p>
""",
         faqs=[("What does FTL stand for?",
                "FTL stands for flight-time limitations — the regulatory limits on crew flight time, duty period and rest that manage fatigue."),
               ("How is FDP different from flight time?",
                "Flight time is time in the air; the flight duty period (FDP) is the whole duty window that includes the flying plus pre- and post-flight duty. FTL limits both.")]),
]


# ── helpers ──────────────────────────────────────────────────────────────────
def esc(s): return html.escape(s, quote=True)


def jsonld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, separators=(",", ":"))}</script>'


ORG_LD = {
    "@context": "https://schema.org", "@type": "Organization", "name": ORG,
    "url": BASE + "/", "logo": BASE + "/logo.svg",
    "description": TAGLINE + ".",
    "sameAs": ["https://www.sealogical.com"],
}
WEBSITE_LD = {
    "@context": "https://schema.org", "@type": "WebSite", "name": ORG,
    "url": BASE + "/",
}


def software_ld():
    return {
        "@context": "https://schema.org", "@type": "SoftwareApplication",
        "name": ORG, "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web", "url": BASE + "/",
        "description": TAGLINE + ", covering crew, certificates, operations, technical, safety, finance and compliance.",
        "offers": {"@type": "Offer", "priceCurrency": "GBP", "price": "0",
                   "description": "Priced per aircraft; unlimited users. Request a quote."},
        "publisher": {"@type": "Organization", "name": ORG},
    }


def faq_ld(faqs):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }


def breadcrumb_ld(trail):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u}
            for i, (n, u) in enumerate(trail)],
    }


NAV = [("Modules", "/modules"), ("Pricing", "/pricing"), ("About", "/about"), ("Blog", "/blog")]


def header():
    links = "".join(f'<a href="{u}">{esc(n)}</a>' for n, u in NAV)
    return f'''<div class="termbar"><div class="wrap"><span class="dots"><i class="r"></i><i class="y"></i><i class="g"></i></span><span>guest@airlogical:~</span></div></div>
<header class="nav"><div class="wrap">
  <a href="/" class="brand"><img class="logo" src="/logo.svg" width="150" height="34" alt="Airlogical" /></a>
  <nav class="main">{links}</nav>
  <div class="navbtns">
    <a class="btn btn-outline" href="{APP}/signup">Sign up</a>
    <a class="btn btn-orange" href="{APP}/login">Login</a>
  </div>
</div></header>'''


def footer():
    mods = "".join(f'<a href="/modules/{m["slug"]}">{esc(m["name"])}</a>' for m in MODULES)
    return f'''<footer>
  <div class="footcta wrap">
    <h2>Ready to see Airlogical?</h2>
    <p>Start free, or ask us for a walkthrough.</p>
    <a class="btn btn-orange" href="{APP}/signup">Get started</a>
  </div>
  <div class="wrap footcols">
    <div><strong class="fw">Airlogical</strong><p>{esc(TAGLINE)}.</p></div>
    <div><h4>Modules</h4><div class="fmods">{mods}</div></div>
    <div><h4>Company</h4><a href="/about">About</a><a href="/pricing">Pricing</a><a href="/blog">Blog</a><a href="{APP}/login">Login</a></div>
  </div>
  <div class="wrap foot-note">&gt; a sister platform to Sealogical — trusted in fleet management since 2003 · <span class="mono">updated {UPDATED}</span></div>
</footer>'''


def page(path, title, desc, body, *, canonical, extra_ld=None, og_type="website"):
    ld = [ORG_LD, WEBSITE_LD] + (extra_ld or [])
    ldblocks = "".join(jsonld(o) for o in ld)
    full_title = title if title.endswith("Airlogical") else f"{title} | Airlogical"
    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="{canonical}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<meta property="og:type" content="{og_type}" />
<meta property="og:site_name" content="Airlogical" />
<meta property="og:title" content="{esc(full_title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{BASE}/og.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{esc(full_title)}" />
<meta name="twitter:description" content="{esc(desc)}" />
<meta name="twitter:image" content="{BASE}/og.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Ubuntu:wght@400;500;700&family=Ubuntu+Mono:wght@400;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/styles.css" />
{ldblocks}
</head>
<body>
{header()}
{body}
{footer()}
<script defer src="https://cdn.vercel-insights.com/v1/script.js"></script>
</body>
</html>
'''
    fp = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(fp) or ROOT, exist_ok=True)
    with open(fp, "w") as f:
        f.write(out)
    return path


def faq_html(faqs, heading="Frequently asked questions"):
    items = "".join(
        f'<div class="faq"><h3>{esc(q)}</h3><p>{a}</p></div>' for q, a in faqs)
    return f'<section class="band-soft"><div class="wrap narrow"><div class="eyebrow">~ questions</div><h2 class="sec">{esc(heading)}</h2><div class="faqs">{items}</div></div></section>'


def cta_band():
    return f'''<section class="band-navy"><div class="wrap center narrow">
    <h2 class="sec" style="color:#fff">See the whole picture</h2>
    <p class="sub" style="color:#b9cdd8;margin:0 auto 20px">One platform for crew, compliance, maintenance, operations and owner reporting.</p>
    <a class="btn btn-orange" href="{APP}/signup">Try Now</a>
    <a class="btn btn-ghost" href="/modules">Explore the modules</a>
</div></section>'''


# ═══ PAGES ═══════════════════════════════════════════════════════════════════
def build_home():
    cards = ""
    for m in MODULES:
        cards += f'''<a class="module" href="/modules/{m["slug"]}"><div class="cap" style="background:{m["color"]}"></div><div class="body"><h3><span class="dot" style="background:{m["color"]}"></span>{esc(m["name"])}</h3><p>{esc(m["lead"].split(" — ")[0] if " — " in m["lead"] else m["lead"][:120])}</p></div></a>'''
    body = f'''
<section class="hero"><div class="wrap"><div class="grid">
  <div>
    <div class="tilde">~</div>
    <h1>Aircraft Management <span class="accent">Software</span></h1>
    <p class="lede"><strong>Airlogical is aircraft management software for private and business aviation.</strong> Operations, compliance, maintenance and owner reporting in one platform — built for flight departments, not adapted from spreadsheets.</p>
    <div class="cta">
      <a class="btn btn-navy" href="{APP}/signup">Try Now</a>
      <a class="btn btn-outline" href="{APP}/login">Login</a>
    </div>
    <div class="trust">&gt; <b>from the team behind Sealogical</b> — 20+ years in fleet management</div>
  </div>
  <div style="position:relative">
    <div class="mock">
      <div class="bar"><span class="dots"><i class="r"></i><i class="y"></i><i class="g"></i></span><span class="url">app.airlogical.com</span></div>
      <div class="app">
        <div class="apphead"><span class="brand2">airlogical</span><span class="tabs">Crew · Safety · Certificates · Technical · Operations · Finance</span></div>
        <div class="mgrid">
          <div class="mcard" style="background:#E2453C"><div class="h">Safety <span>&rarr;</span></div><div class="row"><span>Occurrences</span><span>2 open</span></div></div>
          <div class="mcard" style="background:#2FB37E"><div class="h">Technical <span>&rarr;</span></div><div class="row"><span>Maintenance due</span><span>320h</span></div></div>
          <div class="mcard" style="background:#E7C948;color:#4a3f00"><div class="h">Certificates <span>&rarr;</span></div><div class="row"><span>Expiring 30d</span><span>4</span></div></div>
          <div class="mcard" style="background:#12A5CE"><div class="h">Compliance <span>&rarr;</span></div><div class="row"><span>Due soon</span><span>7</span></div></div>
        </div>
      </div>
    </div>
    <div class="badge2003">[*] By the<b>Sealogical</b>team</div>
  </div>
</div></div></section>

<section id="modules"><div class="wrap">
  <div class="center narrow"><div class="eyebrow">~ what's inside</div><h2 class="sec">Complete aircraft management</h2><p class="sub center">Eight connected modules, one shared source of truth — so the office and the cockpit always see the same picture.</p></div>
  <div class="modules">{cards}</div>
</div></section>

<section class="band-soft"><div class="wrap"><div class="reports">
  <div>
    <div class="eyebrow">~ audit-ready</div>
    <h2 class="sec">Reports built for compliance and audit</h2>
    <p class="sub">Every expiry, check, approval and acknowledgement in one place — with the history to show an inspector exactly what happened and when.</p>
    <ul class="ticks">
      <li><span class="tick">&#10003;</span> Crew currency, recency and duty (FTL) at a glance</li>
      <li><span class="tick">&#10003;</span> Airworthiness &amp; AD compliance register</li>
      <li><span class="tick">&#10003;</span> Exportable read-and-acknowledge trail for manuals &amp; notices</li>
      <li><span class="tick">&#10003;</span> Owner-grade statements and pre-trip cost estimates</li>
    </ul>
  </div>
  <div class="rcard mono">
<span class="c3">~</span> airlogical status --fleet<br/>
<span class="c1">&#10003;</span> aircraft <span class="c2">airworthy</span> &nbsp; 4/4<br/>
<span class="c1">&#10003;</span> crew currency <span class="c2">valid</span><br/>
<span class="c3">!</span> certificates <span class="c2">expiring&lt;30d</span> &nbsp; 4<br/>
<span class="c1">&#10003;</span> ftl <span class="c2">within limits</span><br/>
<span class="c1">&#10003;</span> acknowledgements <span class="c2">100%</span>
  </div>
</div></div></section>

<section class="band-navy"><div class="wrap">
  <div class="center narrow"><div class="eyebrow">~ getting started</div><h2 class="sec" style="color:#fff">Up and running in four steps</h2></div>
  <div class="steps">
    <div class="step"><div class="n">01</div><h3><span class="tw">~</span> Sign in</h3><p>Use the login we set up for you, then set your own password.</p></div>
    <div class="step"><div class="n">02</div><h3><span class="tw">~</span> Add aircraft &amp; crew</h3><p>Start with your aircraft record and crew profiles — or let us import them.</p></div>
    <div class="step"><div class="n">03</div><h3><span class="tw">~</span> Load certificates</h3><p>Bring your certificates in so expiry tracking switches on.</p></div>
    <div class="step"><div class="n">04</div><h3><span class="tw">~</span> Work the dashboard</h3><p>Open it each day — it surfaces what's due, expiring and needs sign-off.</p></div>
  </div>
</div></section>

{faq_html(SITE_FAQS[:6])}
'''
    howto = {"@context": "https://schema.org", "@type": "HowTo",
             "name": "How to get started with Airlogical",
             "step": [{"@type": "HowToStep", "name": n, "text": t} for n, t in [
                 ("Sign in", "Use the login we set up for you, then set your own password."),
                 ("Add aircraft & crew", "Add your aircraft record and crew profiles, or import them."),
                 ("Load certificates", "Bring your certificates in so expiry tracking switches on."),
                 ("Work the dashboard", "Open the dashboard each day to see what's due, expiring and needs sign-off.")]]}
    page("index.html",
         "Aircraft Management Software",
         "Airlogical is aircraft management software for private and business aviation — crew, certificates, operations, maintenance, safety, finance and compliance in one platform.",
         body, canonical=BASE + "/",
         extra_ld=[software_ld(), howto, faq_ld(SITE_FAQS[:6])])


def build_modules_index():
    cards = "".join(
        f'<a class="module" href="/modules/{m["slug"]}"><div class="cap" style="background:{m["color"]}"></div><div class="body"><h3><span class="dot" style="background:{m["color"]}"></span>{esc(m["name"])}</h3><p>{esc(m["lead"])}</p></div></a>'
        for m in MODULES)
    body = f'''<section class="page-hero"><div class="wrap narrow center">
  <div class="eyebrow">~ modules</div>
  <h1>The complete aircraft management platform</h1>
  <p class="sub center">Airlogical is made of eight connected modules that share one source of truth. Explore each below.</p>
</div></section>
<section><div class="wrap"><div class="modules">{cards}</div></div></section>
{cta_band()}'''
    page("modules/index.html", "Modules — the complete aircraft management platform",
         "Explore Airlogical's eight modules: aircraft, crew, certificates, operations, technical, safety, finance and compliance — one platform for private and business aviation.",
         body, canonical=BASE + "/modules",
         extra_ld=[breadcrumb_ld([("Home", "/"), ("Modules", "/modules")])])


def clip(text, n=155):
    """Trim to a word boundary for meta descriptions."""
    t = " ".join(text.split())
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


def build_module(m):
    intro = "".join(f"<p>{esc(x)}</p>" for x in m["intro"])
    caps = "".join(
        f'<div class="cap-card"><h3><span class="dot" style="background:{m["color"]}"></span>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for t, d in m["capabilities"])
    steps = "".join(
        f'<div class="step"><div class="n">{i + 1:02d}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for i, (t, d) in enumerate(m["how"]))
    name_of = {o["slug"]: o["name"] for o in MODULES}
    rel = "".join(
        f'<a href="/modules/{s}" class="pill-link">{esc(name_of[s])}</a>'
        for s in m.get("related", []) if s in name_of)
    others = "".join(
        f'<a href="/modules/{o["slug"]}" class="pill-link">{esc(o["name"])}</a>'
        for o in MODULES if o["slug"] != m["slug"])

    body = f'''<section class="page-hero"><div class="wrap narrow">
  <nav class="crumbs mono"><a href="/">home</a> / <a href="/modules">modules</a> / {esc(m["name"].lower())}</nav>
  <div class="eyebrow" style="color:{m["color"]}">~ {esc(m["name"].lower())}</div>
  <h1>{esc(m["title"])}</h1>
  <p class="lead">{esc(m["lead"])}</p>
  <div class="cta"><a class="btn btn-navy" href="{APP}/signup">Try Now</a><a class="btn btn-outline" href="/pricing">Pricing</a></div>
</div></section>

<section><div class="wrap narrow prose">{intro}</div></section>

<section class="band-soft"><div class="wrap">
  <div class="center narrow"><div class="eyebrow">~ capabilities</div><h2 class="sec">What the {esc(m["name"])} module covers</h2></div>
  <div class="capgrid">{caps}</div>
</div></section>

<section class="band-navy"><div class="wrap">
  <div class="center narrow"><div class="eyebrow">~ how it works</div><h2 class="sec" style="color:#fff">How {esc(m["name"])} works</h2></div>
  <div class="steps">{steps}</div>
</div></section>

<section><div class="wrap narrow prose">
  <h2 class="sec">Who it&#39;s for</h2>
  <p>{esc(m["who"])}</p>
</div></section>

{faq_html(m["faqs"], "Questions about " + m["name"])}

<section><div class="wrap narrow center">
  <div class="eyebrow">~ works with</div><h2 class="sec">Related modules</h2>
  <div class="pill-links">{rel}</div>
  <p class="sub center" style="margin:26px auto 0">Every module</p>
  <div class="pill-links">{others}</div>
</div></section>
{cta_band()}'''

    page(f"modules/{m['slug']}.html", m["title"], clip(m["lead"]),
         body, canonical=f"{BASE}/modules/{m['slug']}",
         extra_ld=[software_ld(),
                   faq_ld(m["faqs"]),
                   breadcrumb_ld([("Home", "/"), ("Modules", "/modules"),
                                  (m["name"], f"/modules/{m['slug']}")])])


def build_pricing():
    body = f'''<section class="page-hero"><div class="wrap narrow center">
  <div class="eyebrow">~ pricing</div>
  <h1>Simple pricing, per aircraft</h1>
  <p class="sub center">Airlogical is priced per aircraft and includes <strong>unlimited users</strong> — the whole flight department, the crew and the owner, at no extra per-seat cost.</p>
</div></section>
<section><div class="wrap narrow">
  <div class="pricegrid">
    <div class="pricecard"><h3>Owner / single aircraft</h3><p>For an owner-operated or single managed aircraft.</p><ul class="ticks"><li><span class="tick">&#10003;</span> All modules</li><li><span class="tick">&#10003;</span> Unlimited users</li><li><span class="tick">&#10003;</span> Owner portal &amp; statements</li></ul><a class="btn btn-navy" href="{APP}/signup">Get started</a></div>
    <div class="pricecard feature"><h3>Fleet / management company</h3><p>For flight departments and management companies operating multiple aircraft.</p><ul class="ticks"><li><span class="tick">&#10003;</span> Everything in single-aircraft</li><li><span class="tick">&#10003;</span> Fleet-wide compliance forecast &amp; schedule</li><li><span class="tick">&#10003;</span> Multi-aircraft owner reporting</li></ul><a class="btn btn-orange" href="{APP}/signup">Get started</a></div>
    <div class="pricecard"><h3>Tailored</h3><p>Need onboarding help, data import or a walkthrough?</p><ul class="ticks"><li><span class="tick">&#10003;</span> Guided onboarding &amp; import</li><li><span class="tick">&#10003;</span> Priority support</li><li><span class="tick">&#10003;</span> A quote for your operation</li></ul><a class="btn btn-outline" href="mailto:hello@airlogical.com">Request a quote</a></div>
  </div>
  <p class="fineprint">Pricing scales with the number of aircraft. Every plan includes unlimited users and all modules. <a href="mailto:hello@airlogical.com">Contact us</a> for a quote tailored to your fleet.</p>
</div></section>
{faq_html([f for f in SITE_FAQS if "cost" in f[0].lower() or "single-aircraft" in f[0].lower() or "who is" in f[0].lower()], "Pricing questions")}'''
    page("pricing.html", "Pricing",
         "Airlogical is priced per aircraft with unlimited users and all modules included. Request a quote tailored to your private or business aviation operation.",
         body, canonical=BASE + "/pricing",
         extra_ld=[breadcrumb_ld([("Home", "/"), ("Pricing", "/pricing")])])


def build_about():
    body = f'''<section class="page-hero"><div class="wrap narrow">
  <div class="eyebrow">~ about</div>
  <h1>About Airlogical</h1>
  <p class="lead"><strong>Airlogical is aircraft management software for private and business aviation</strong>, built by the team behind Sealogical — the yacht-management platform trusted in fleet management since 2003.</p>
</div></section>
<section><div class="wrap narrow prose">
  <h2>Why we built it</h2>
  <p>Running an aircraft means tracking an enormous amount — crew licences and medicals, certificates and checks, maintenance and airworthiness, every trip, and the costs that follow. Too often that lives across spreadsheets, inboxes and separate tools, and things slip.</p>
  <p>We had already solved this problem at scale in another safety-critical, asset-heavy industry. Sealogical has managed fleets since 2003 across hundreds of vessels and thousands of users. Airlogical applies that same thesis to aviation: one consolidated, owner-transparent platform, purpose-built rather than adapted.</p>
  <h2>What we believe</h2>
  <ul class="ticks">
    <li><span class="tick">&#10003;</span> <strong>Purpose-built for aviation</strong> — designed around how flight departments actually work.</li>
    <li><span class="tick">&#10003;</span> <strong>Compliance you can prove</strong> — with the history an auditor needs.</li>
    <li><span class="tick">&#10003;</span> <strong>One source of truth</strong> — crew, aircraft, maintenance, trips and finance in one place.</li>
    <li><span class="tick">&#10003;</span> <strong>Owner transparency</strong> — clear, forward-looking cost reporting.</li>
  </ul>
  <h2>Get in touch</h2>
  <p>Email <a href="mailto:hello@airlogical.com">hello@airlogical.com</a> for a walkthrough, or <a href="{APP}/signup">start free</a>.</p>
</div></section>
{cta_band()}'''
    page("about.html", "About Airlogical — aircraft management software",
         "Airlogical is aircraft management software for private and business aviation, built by the team behind Sealogical — trusted in fleet management since 2003.",
         body, canonical=BASE + "/about",
         extra_ld=[breadcrumb_ld([("Home", "/"), ("About", "/about")])])


def build_faq():
    body = f'''<section class="page-hero"><div class="wrap narrow center">
  <div class="eyebrow">~ faq</div>
  <h1>Aircraft management software: FAQ</h1>
  <p class="sub center">Answers to the questions operators ask most about Airlogical.</p>
</div></section>
{faq_html(SITE_FAQS, "Frequently asked questions")}
{cta_band()}'''
    page("faq.html", "Aircraft management software FAQ",
         "Common questions about Airlogical and aircraft management software — FTL tracking, Part 91/135, owner cost reporting, pricing and more.",
         body, canonical=BASE + "/faq",
         extra_ld=[faq_ld(SITE_FAQS), breadcrumb_ld([("Home", "/"), ("FAQ", "/faq")])])


def build_blog_index():
    items = "".join(
        f'<a class="postcard" href="/blog/{p["slug"]}"><h3>{esc(p["title"])}</h3><p>{esc(p["desc"])}</p><span class="mono readmore">read &rarr;</span></a>'
        for p in BLOG)
    body = f'''<section class="page-hero"><div class="wrap narrow center">
  <div class="eyebrow">~ resources</div>
  <h1>Guides &amp; resources</h1>
  <p class="sub center">Plain-English guides to aircraft management, compliance and operations.</p>
</div></section>
<section><div class="wrap"><div class="postgrid">{items}</div></div></section>
{cta_band()}'''
    page("blog/index.html", "Guides & resources",
         "Plain-English guides to aircraft management software, flight-time limitations, compliance and operations for private and business aviation.",
         body, canonical=BASE + "/blog",
         extra_ld=[breadcrumb_ld([("Home", "/"), ("Blog", "/blog")])])


def build_post(p):
    faqs = faq_html(p["faqs"], "Related questions") if p.get("faqs") else ""
    body = f'''<article><section class="page-hero"><div class="wrap narrow">
  <nav class="crumbs mono"><a href="/">home</a> / <a href="/blog">blog</a></nav>
  <h1>{esc(p["title"])}</h1>
  <p class="mono postmeta">Published {p["date"]} · Airlogical</p>
</div></section>
<section><div class="wrap narrow prose">{p["body"]}</div></section>
{faqs}</article>
{cta_band()}'''
    post_ld = {"@context": "https://schema.org", "@type": "BlogPosting",
               "headline": p["title"], "description": p["desc"],
               "datePublished": p["date"], "dateModified": p["date"],
               "author": {"@type": "Organization", "name": ORG},
               "publisher": {"@type": "Organization", "name": ORG, "logo": {"@type": "ImageObject", "url": BASE + "/logo.svg"}},
               "mainEntityOfPage": f"{BASE}/blog/{p['slug']}"}
    extra = [post_ld, breadcrumb_ld([("Home", "/"), ("Blog", "/blog"), (p["title"], f"/blog/{p['slug']}")])]
    if p.get("faqs"):
        extra.append(faq_ld(p["faqs"]))
    page(f"blog/{p['slug']}.html", p["title"], p["desc"], body,
         canonical=f"{BASE}/blog/{p['slug']}", extra_ld=extra, og_type="article")


# ── static assets ────────────────────────────────────────────────────────────
def write(path, content):
    with open(os.path.join(ROOT, path), "w") as f:
        f.write(content)


def build_assets():
    urls = ["/", "/modules", "/pricing", "/about", "/faq", "/blog"] \
        + [f"/modules/{m['slug']}" for m in MODULES] \
        + [f"/blog/{p['slug']}" for p in BLOG]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        pr = "1.0" if u == "/" else ("0.8" if u.startswith("/modules") else "0.6")
        sm += f"  <url><loc>{BASE}{u}</loc><lastmod>{UPDATED}</lastmod><priority>{pr}</priority></url>\n"
    sm += "</urlset>\n"
    write("sitemap.xml", sm)

    write("robots.txt",
          "# Airlogical — allow all crawlers, including AI answer engines (GEO)\n"
          "User-agent: *\nAllow: /\n\n"
          "# AI crawlers explicitly welcomed\n"
          "User-agent: GPTBot\nAllow: /\n"
          "User-agent: OAI-SearchBot\nAllow: /\n"
          "User-agent: ChatGPT-User\nAllow: /\n"
          "User-agent: PerplexityBot\nAllow: /\n"
          "User-agent: Google-Extended\nAllow: /\n"
          "User-agent: ClaudeBot\nAllow: /\n"
          "User-agent: Applebot-Extended\nAllow: /\n\n"
          f"Sitemap: {BASE}/sitemap.xml\n")

    llms = f"""# Airlogical

> {TAGLINE}. One platform covering crew, certificates, operations, technical, safety, finance and compliance for private and business aviation. Built by the team behind Sealogical (fleet management since 2003).

## Pages
- [Home]({BASE}/): What Airlogical is and the eight modules.
- [Modules]({BASE}/modules): The complete platform.
"""
    for m in MODULES:
        llms += f"- [{m['name']}]({BASE}/modules/{m['slug']}): {m['title']}.\n"
    llms += f"- [Pricing]({BASE}/pricing): Per-aircraft pricing, unlimited users.\n"
    llms += f"- [About]({BASE}/about): Company and heritage.\n"
    llms += f"- [FAQ]({BASE}/faq): Common questions.\n"
    for p in BLOG:
        llms += f"- [{p['title']}]({BASE}/blog/{p['slug']}): {p['desc']}\n"
    write("llms.txt", llms)

    write("vercel.json", json.dumps({"cleanUrls": True, "trailingSlash": False}, indent=2) + "\n")

    # favicon (monogram tile)
    write("favicon.svg", '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#08325a"/><path fill="#00B5E2" d="M12 40 L22 40 L38 18 L46 18 L46 34 C46 37 47 38 50 38 L54 38 L54 46 L50 46 C43 46 38 41 38 34 L38 30 L26 46 L12 46 Z"/></svg>''')

    # og image (1200x630) — SVG source; a PNG is rendered separately for max compatibility
    og = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<rect width="1200" height="630" fill="#034566"/>
<rect y="0" width="1200" height="8" fill="#F6881C"/>
<g transform="translate(90,150)"><rect x="-30" y="-70" width="70" height="60" rx="10" fill="#fff"/></g>
<text x="90" y="250" font-family="Ubuntu, Arial, sans-serif" font-size="78" font-weight="700" fill="#ffffff">Aircraft Management</text>
<text x="90" y="340" font-family="Ubuntu, Arial, sans-serif" font-size="78" font-weight="700" fill="#F6881C">Software</text>
<text x="90" y="420" font-family="Ubuntu Mono, monospace" font-size="30" fill="#9fc0d2">Operations · Compliance · Maintenance · Owner reporting</text>
<text x="90" y="560" font-family="Ubuntu, Arial, sans-serif" font-size="34" font-weight="700" fill="#ffffff">airlogical<tspan fill="#00B5E2">.com</tspan></text>
</svg>'''
    write("og.svg", og)

    # 404
    page("404.html", "Page not found",
         "That page could not be found. Explore Airlogical's aircraft management modules.",
         '''<section class="page-hero"><div class="wrap narrow center" style="padding:80px 0">
  <div class="eyebrow">~ 404</div><h1>Page not found</h1>
  <p class="sub center">That page has moved or never existed.</p>
  <div class="cta" style="justify-content:center"><a class="btn btn-navy" href="/">Home</a><a class="btn btn-outline" href="/modules">Modules</a></div>
</div></section>''', canonical=BASE + "/404")


def build_styles():
    write("styles.css", CSS)


CSS = """
:root{--navy:#034566;--navy2:#055580;--orange:#F6881C;--teal:#47D5C6;--ink:#1A1A1A;--mute:#5b6b78;--line:#e3ebf1;--soft:#f7fafc}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:Ubuntu,system-ui,sans-serif;color:var(--ink);background:#fff;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.mono{font-family:"Ubuntu Mono",monospace}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.narrow{max-width:820px}
.center{text-align:center;margin-left:auto;margin-right:auto}
h1,h2,h3{color:var(--navy);font-weight:700;line-height:1.15}
.accent{color:var(--orange)}
.termbar{background:var(--navy);color:#cfe0ea;font-family:"Ubuntu Mono",monospace;font-size:13px}
.termbar .wrap{display:flex;align-items:center;gap:12px;height:34px}
.dots{display:flex;gap:7px}.dots i{width:11px;height:11px;border-radius:50%;display:inline-block}
.dots .r{background:#FF5F57}.dots .y{background:#FEBC2E}.dots .g{background:#28C840}
header.nav{position:sticky;top:0;z-index:20;background:#fff;border-bottom:1px solid var(--line)}
header.nav .wrap{display:flex;align-items:center;gap:20px;height:74px}
.logo{height:34px;width:auto;display:block}
nav.main{display:flex;align-items:center;gap:22px;margin-left:18px;flex:1}
nav.main a{font-size:15px;color:#31424d}
nav.main a:hover{color:var(--navy)}
.navbtns{display:flex;align-items:center;gap:10px}
.btn{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:15px;border-radius:10px;padding:11px 20px;border:2px solid transparent;cursor:pointer;transition:.15s}
.btn+.btn{margin-left:8px}
.btn-navy{background:var(--navy);color:#fff}.btn-navy:hover{background:#03395a}
.btn-outline{background:#fff;color:var(--navy);border-color:var(--navy)}.btn-outline:hover{background:#f2f7fa}
.btn-orange{background:var(--orange);color:#fff}.btn-orange:hover{filter:brightness(.96)}
.btn-ghost{background:transparent;color:#fff;border-color:rgba(255,255,255,.5)}.btn-ghost:hover{background:rgba(255,255,255,.1)}
.hero{padding:64px 0 44px}
.hero .grid{display:grid;grid-template-columns:1.05fr 1fr;gap:48px;align-items:center}
.tilde{color:var(--orange);font-family:"Ubuntu Mono",monospace;font-size:22px}
.hero h1{font-size:56px;letter-spacing:-1px;margin:6px 0 18px}
.lede{font-size:19px;color:#33454f;max-width:520px;margin-bottom:26px}
.cta{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.trust{margin-top:22px;font-family:"Ubuntu Mono",monospace;font-size:13px;color:var(--mute)}.trust b{color:var(--navy)}
.mock{border:1px solid var(--line);border-radius:14px;box-shadow:0 24px 60px -30px rgba(3,69,102,.45);overflow:hidden;background:#fff;position:relative}
.mock .bar{background:var(--navy);height:34px;display:flex;align-items:center;gap:8px;padding:0 12px}
.mock .bar .url{font-family:"Ubuntu Mono",monospace;color:#bcd3e0;font-size:12px;margin-left:8px}
.mock .app{padding:14px}
.mock .apphead{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:12px}
.mock .brand2{font-weight:700;color:var(--navy);font-size:15px}
.mock .tabs{display:flex;gap:8px;flex-wrap:wrap;font-size:11px;color:var(--mute)}
.mgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.mcard{border-radius:9px;padding:10px 12px;color:#fff;min-height:56px}
.mcard .h{display:flex;align-items:center;justify-content:space-between;font-weight:700;font-size:13px}
.mcard .row{font-size:10.5px;opacity:.92;margin-top:6px;display:flex;justify-content:space-between}
.badge2003{position:absolute;top:-14px;right:-14px;background:#fff;border:2px solid var(--orange);border-radius:12px;padding:8px 12px;font-family:"Ubuntu Mono",monospace;font-size:12px;color:var(--navy);box-shadow:0 8px 24px -12px rgba(3,69,102,.5)}
.badge2003 b{display:block;font-size:20px}
section{padding:62px 0}
.page-hero{padding:56px 0 26px}
.eyebrow{font-family:"Ubuntu Mono",monospace;color:var(--orange);font-size:13px;letter-spacing:1px;text-transform:lowercase}
h1{font-size:44px;letter-spacing:-.5px;margin:6px 0 14px}
h2.sec{font-size:32px;margin:6px 0 10px}
.sub{color:var(--mute);font-size:17px;max-width:640px}
.lead{font-size:20px;color:#33454f;margin:6px 0 22px;max-width:680px}
.crumbs{color:var(--mute);font-size:13px;margin-bottom:10px}.crumbs a{color:var(--mute)}.crumbs a:hover{color:var(--navy)}
.modules{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:34px}
.module{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff;transition:.15s;display:block}
.module:hover{transform:translateY(-3px);box-shadow:0 18px 40px -26px rgba(3,69,102,.45)}
.module .cap{height:8px}.module .body{padding:16px}
.module h3{font-size:17px;display:flex;align-items:center;gap:8px}
.module .dot{width:9px;height:9px;border-radius:50%}
.module p{font-size:13.5px;color:#3a4853;margin-top:8px}
.capgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:30px}
.cap-card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px}
.cap-card h3{font-size:16px;display:flex;align-items:center;gap:8px;margin-bottom:6px}
.cap-card .dot{width:9px;height:9px;border-radius:50%;flex:0 0 auto}
.cap-card p{font-size:14px;color:#3a4853}
.band-soft{background:var(--soft)}
.reports{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}
.ticks{list-style:none;display:grid;gap:10px;margin-top:16px}
.ticks li{display:flex;gap:10px;font-size:15px;color:#33454f}
.ticks.big li{font-size:16.5px}
.tick{color:var(--orange);font-family:"Ubuntu Mono",monospace;font-weight:700}
.rcard{background:var(--navy);border-radius:14px;padding:18px;color:#cfe0ea;font-family:"Ubuntu Mono",monospace;font-size:13px;line-height:1.9}
.rcard .c1{color:var(--teal)}.rcard .c2{color:#fff}.rcard .c3{color:var(--orange)}
.band-navy{background:var(--navy);color:#dce9f0}
.band-navy .eyebrow{color:var(--teal)}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:34px}
.step{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:10px;padding:18px}
.step .n{width:38px;height:38px;border-radius:50%;background:var(--teal);color:var(--navy);font-weight:700;display:flex;align-items:center;justify-content:center;font-family:"Ubuntu Mono",monospace}
.step h3{color:#fff;font-size:16px;margin:12px 0 6px}.step h3 .tw{color:var(--teal)}
.step p{font-size:13.5px;color:#b9cdd8}
.faqs{display:grid;gap:14px;margin-top:26px}
.faq{background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px 20px}
.faq h3{font-size:17px;margin-bottom:6px}
.faq p{font-size:15px;color:#3a4853}
.prose h2{font-size:26px;margin:26px 0 10px}
.prose p{margin:12px 0;font-size:16.5px;color:#2f3e48}
.prose ul{margin:12px 0 12px 2px;list-style:none;display:grid;gap:8px}
.prose ul li{padding-left:6px}
.prose .lead{font-size:20px}
.prose a{color:var(--navy);text-decoration:underline;text-underline-offset:3px}
.pricegrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:20px}
.pricecard{border:1px solid var(--line);border-radius:14px;padding:24px;display:flex;flex-direction:column}
.pricecard.feature{border-color:var(--orange);box-shadow:0 18px 40px -26px rgba(246,136,28,.5)}
.pricecard h3{font-size:20px}.pricecard p{color:var(--mute);font-size:14.5px;margin:8px 0}
.pricecard .ticks{flex:1;margin:10px 0 18px}
.fineprint{color:var(--mute);font-size:14px;margin-top:22px;text-align:center}
.postgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:20px}
.postcard{border:1px solid var(--line);border-radius:12px;padding:22px;display:block;transition:.15s}
.postcard:hover{transform:translateY(-3px);box-shadow:0 18px 40px -26px rgba(3,69,102,.4)}
.postcard h3{font-size:19px}.postcard p{color:#3a4853;font-size:14.5px;margin:8px 0}
.readmore{color:var(--orange)}
.postmeta{color:var(--mute);font-size:13px}
.pill-links{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:20px}
.pill-link{border:1px solid var(--line);border-radius:20px;padding:8px 16px;font-size:14px;color:var(--navy)}
.pill-link:hover{background:var(--soft)}
footer{background:var(--navy);color:#cfe0ea}
.footcta{text-align:center;padding:60px 0 40px;border-bottom:1px solid rgba(255,255,255,.12)}
.footcta h2{color:#fff;font-size:30px;margin-bottom:8px}.footcta p{color:#a9c4d3;margin-bottom:22px}
.footcols{display:grid;grid-template-columns:2fr 1fr 1fr;gap:30px;padding:36px 0}
.footcols h4{color:#fff;font-size:14px;margin-bottom:10px}
.footcols a{color:#a9c4d3;font-size:14px;display:block;margin-bottom:6px}.footcols a:hover{color:#fff}
.footcols p{color:#8fb0c2;font-size:14px}
.fw{color:#fff;font-size:16px}
.fmods{display:flex;flex-direction:column}
.foot-note{padding:0 0 28px;font-family:"Ubuntu Mono",monospace;font-size:12px;color:#7fa0b2}
@media(max-width:900px){
 .hero .grid,.reports,.footcols{grid-template-columns:1fr}
 .modules,.steps,.pricegrid,.postgrid,.capgrid{grid-template-columns:1fr 1fr}
 nav.main{display:none}
 .hero h1{font-size:40px}h1{font-size:34px}h2.sec{font-size:26px}
}
@media(max-width:560px){.modules,.steps,.pricegrid,.postgrid,.mgrid,.capgrid{grid-template-columns:1fr}}
"""


def main():
    build_styles()
    build_assets()
    build_home()
    build_modules_index()
    for m in MODULES:
        build_module(m)
    build_pricing()
    build_about()
    build_faq()
    build_blog_index()
    for p in BLOG:
        build_post(p)
    # count
    n = sum(len(files) for _, _, files in os.walk(ROOT))
    print("Generated site. HTML pages:",
          1 + 1 + len(MODULES) + 3 + 1 + len(BLOG))


if __name__ == "__main__":
    main()

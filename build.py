#!/usr/bin/env python3
"""Builds the CAPTCHA Accessibility Scorecard into _site/.

GitHub Actions runs this on every push to main and publishes _site/ to GitHub Pages.

Preview locally:
    python3 build.py
    python3 -m http.server -d _site 8000   # then open http://localhost:8000

Standard library only. Works on Python 3.8+.
"""
import datetime
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
SITE_NAME = "CAPTCHA Accessibility Scorecard"
REPO_URL = "https://github.com/aaliyahali/is308-final-project-captcha-scorecard"
UPDATED = datetime.date.today().strftime("%B %-d, %Y")

crit_data = json.loads((ROOT / "data/criteria.json").read_text(encoding="utf-8"))
CRITERIA = crit_data["criteria"]
GROUPS = crit_data["groups"]
RATINGS = crit_data["ratings"]
CAPTCHAS = json.loads((ROOT / "data/captchas.json").read_text(encoding="utf-8"))["captchas"]
ORDER = [c for g in GROUPS for c in g["criteria"]]

# Part 2 pages appear automatically once their content file exists in content/.
HAS_CHECKLIST = (ROOT / "content/checklist.html").exists()
HAS_METHODS = (ROOT / "content/methods.html").exists()

NAV = [("index.html", "Home"), ("scorecard.html", "Scorecard")]
if HAS_CHECKLIST:
    NAV.append(("checklist.html", "Developer checklist"))
if HAS_METHODS:
    NAV.append(("methods.html", "Methods &amp; sources"))

e = html.escape


def content(name):
    text = (ROOT / "content" / name).read_text(encoding="utf-8")
    return re.sub(r"<!--.*?-->\s*", "", text, count=1, flags=re.S)  # drop the owner comment


def anchor(cid):
    return "c-" + cid.replace(".", "-")


def rating_of(c, cid):
    return c["results"].get(cid, {}).get("rating", "untested")


def label(r):
    info = RATINGS[r]
    return '<span class="mark" aria-hidden="true">{}</span> {}'.format(info["icon"], info["label"])


def counts(c):
    n = {k: 0 for k in RATINGS}
    for cid in ORDER:
        n[rating_of(c, cid)] += 1
    return n


def counts_text(n):
    parts = ["{} {}".format(n[k], RATINGS[k]["label"].lower()) for k in ("pass", "partial", "fail")]
    if n["untested"]:
        parts.append("{} not yet rated".format(n["untested"]))
    return ", ".join(parts)


def bar(c):
    """A stacked bar of pass/partial/fail. Decorative: the same numbers are always given in text next to it."""
    n = counts(c)
    segs = "".join(
        '<span class="seg seg-{}" style="flex-grow:{}"></span>'.format(k, n[k])
        for k in ("pass", "partial", "fail", "untested") if n[k]
    )
    return '<span class="bar" aria-hidden="true">{}</span>'.format(segs)


def page(filename, title, body, current=None, lede=None, kicker=None):
    cur = current or filename
    nav = "".join(
        '<li><a href="{}"{}>{}</a></li>'.format(href, ' aria-current="page"' if href == cur else "", text)
        for href, text in NAV
    )
    full_title = SITE_NAME if filename == "index.html" else "{} | {}".format(re.sub("<[^>]+>", "", title), SITE_NAME)
    kicker_html = '<p class="kicker">{}</p>'.format(kicker) if kicker else ""
    lede_html = '<p class="lede">{}</p>'.format(lede) if lede else ""
    doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="We tested four popular CAPTCHAs with VoiceOver and keyboard only, against WCAG 2.2.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=JetBrains+Mono:wght@500&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap header-row">
    <a class="logo" href="index.html"><span class="logo-box" aria-hidden="true"></span>CAPTCHA Accessibility Scorecard</a>
    <nav aria-label="Main"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main" tabindex="-1">
  <div class="page-head">
    <div class="wrap">
      {kicker}
      <h1>{title}</h1>
      {lede}
    </div>
  </div>
  <div class="wrap page-body">
{body}
  </div>
</main>
<footer class="site-footer">
  <div class="wrap footer-row">
    <div>
      <p><strong>About this project.</strong> Made by Aaliyah Ali and Anya Acharya for Designing Inclusive Information Technologies at the University of Illinois Urbana-Champaign, fall 2026.</p>
      <p>Last updated {updated}.</p>
    </div>
    <p>Think we got a rating wrong? <a href="{repo}/issues/new/choose">Tell us on GitHub</a>.</p>
  </div>
</footer>
</body>
</html>
""".format(full_title=full_title, nav=nav, kicker=kicker_html, title=title, lede=lede_html,
           body=body, updated=UPDATED, repo=REPO_URL)
    (OUT / filename).write_text(doc, encoding="utf-8")


def build_home():
    rows = []
    for c in CAPTCHAS:
        n = counts(c)
        rows.append("""<tr>
  <th scope="row"><a href="{id}.html">{name}</a></th>
  <td>{style}</td>
  <td><span class="tally">{bar}<span class="tally-text">{counts}</span></span></td>
</tr>""".format(id=c["id"], name=e(c["name"]), style=e(c["style"]), bar=bar(c), counts=counts_text(n)))
    links = ['<a class="button" href="scorecard.html">Compare all four, criterion by criterion</a>']
    if HAS_CHECKLIST:
        links.append('<a class="button button-ghost" href="checklist.html">Picking a CAPTCHA? Start with the checklist</a>')
    body = """{intro}
<section aria-labelledby="compare-heading" class="section">
  <h2 id="compare-heading">How the four compare</h2>
  <p>Each one was checked against the same 10 WCAG 2.2 criteria.</p>
  <div class="table-scroll" role="region" aria-labelledby="home-caption" tabindex="0">
  <table class="summary-table">
    <caption id="home-caption" class="visually-hidden">Number of criteria each CAPTCHA passed, partly passed and failed</caption>
    <thead><tr><th scope="col">CAPTCHA</th><th scope="col">What it asks you to do</th><th scope="col">Out of 10 criteria</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  </div>
  {legend}
</section>
<div class="cta">{links}</div>""".format(intro=content("home-intro.html"), rows="".join(rows), legend=legend(), links="".join(links))
    page("index.html", "How accessible are the CAPTCHAs everyone clicks through?", body,
         kicker="A WCAG 2.2 audit of four popular bot checks",
         lede="If you can't get past a CAPTCHA, you don't just miss one feature. You're locked out of signing up, logging in, buying the ticket or sending the message.")


def legend():
    items = "".join(
        '<li><span class="key key-{k}">{lab}</span> {meaning}</li>'.format(k=k, lab=label(k), meaning=e(RATINGS[k]["meaning"]))
        for k in ("pass", "partial", "fail")
    )
    return '<details class="legend"><summary>What Pass, Partial and Fail mean</summary><ul>{}</ul></details>'.format(items)


def build_comparison():
    head = "".join('<th scope="col"><a href="{}.html">{}</a></th>'.format(c["id"], e(c["name"])) for c in CAPTCHAS)
    groups = []
    for g in GROUPS:
        rows = ['<tr class="group-row"><th scope="rowgroup" colspan="{}">{}</th></tr>'.format(len(CAPTCHAS) + 1, e(g["label"]))]
        for cid in g["criteria"]:
            cr = CRITERIA[cid]
            cells = "".join(
                '<td class="cell cell-{r}"><a href="{id}.html#{a}">{lab}</a></td>'.format(
                    r=rating_of(c, cid), id=c["id"], a=anchor(cid), lab=label(rating_of(c, cid)))
                for c in CAPTCHAS
            )
            rows.append('<tr><th scope="row"><span class="crit-id">{}</span> {} <span class="level">Level {}</span></th>{}</tr>'.format(
                cid, e(cr["name"]), cr["level"], cells))
        groups.append("<tbody>{}</tbody>".format("".join(rows)))
    totals = "".join("<td>{}<span class=\"tally-text\">{}</span></td>".format(bar(c), counts_text(counts(c))) for c in CAPTCHAS)
    body = """{legend}
<div class="table-scroll" role="region" aria-labelledby="cmp-caption" tabindex="0">
<table class="compare">
  <caption id="cmp-caption" class="visually-hidden">Ratings for each CAPTCHA on each WCAG 2.2 criterion, grouped by who the criterion affects most</caption>
  <thead><tr><th scope="col">Criterion</th>{head}</tr></thead>
  {groups}
  <tfoot><tr><th scope="row">Totals</th>{totals}</tr></tfoot>
</table>
</div>""".format(legend=legend(), head=head, groups="".join(groups), totals=totals)
    page("scorecard.html", "The scorecard", body,
         lede="All four CAPTCHAs, side by side. Rows are grouped by who each criterion matters most to. Select any rating to see why we gave it.")


def build_captcha(c):
    rows = []
    for cid in ORDER:
        cr = CRITERIA[cid]
        r = c["results"].get(cid, {"rating": "untested", "note": ""})
        rk = r.get("rating", "untested")
        rows.append("""<tr id="{a}">
  <th scope="row"><a href="{url}"><span class="crit-id">{cid}</span> {name}</a> <span class="level">Level {level}</span></th>
  <td class="cell cell-{rk}">{lab}</td>
  <td>{note}</td>
</tr>""".format(a=anchor(cid), url=cr["url"], cid=cid, name=e(cr["name"]), level=cr["level"], rk=rk, lab=label(rk), note=e(r.get("note", ""))))
    n = counts(c)
    exp = c["experience"]
    cv = c["claims_vs_found"]
    tested = "Tested {} by {}".format(e(c["test_date"]), e(c["tester"])) if c.get("test_date") else "Not tested yet"
    body = """<div class="verdict">
  <div class="verdict-score">
    <p class="verdict-label">Out of 10 criteria</p>
    {bar}
    <p class="tally-text">{counts}</p>
  </div>
  <div>
    <h2 id="how">How it did</h2>
    <p>{overall}</p>
  </div>
</div>

<div class="split">
  <section aria-labelledby="best" class="note-box note-good"><h2 id="best">Best for</h2><p>{best}</p></section>
  <section aria-labelledby="watch" class="note-box note-warn"><h2 id="watch">Watch out for</h2><p>{watch}</p></section>
</div>

<section aria-labelledby="experience" class="section">
  <h2 id="experience">What a user actually experiences</h2>
  <div class="split">
    <div><h3>Using a screen reader</h3><p>{sr}</p></div>
    <div><h3>Using only a keyboard</h3><p>{kb}</p></div>
  </div>
</section>

<section aria-labelledby="criteria-h" class="section">
  <h2 id="criteria-h">Criterion by criterion</h2>
  <div class="table-scroll" role="region" aria-labelledby="crit-caption" tabindex="0">
  <table class="results">
    <caption id="crit-caption" class="visually-hidden">{name}: rating and note for each WCAG 2.2 criterion</caption>
    <thead><tr><th scope="col">Criterion</th><th scope="col">Rating</th><th scope="col">Why</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  </div>
</section>

<section aria-labelledby="claims" class="section">
  <h2 id="claims">Vendor claims vs. what we found</h2>
  <div class="split">
    <div class="quote-box"><h3>What {vendor} says</h3><p>{claim}</p></div>
    <div class="quote-box quote-found"><h3>What we found</h3><p>{found}</p></div>
  </div>
</section>

<section aria-labelledby="details" class="section">
  <h2 id="details">Test details</h2>
  <dl class="details">
    <dt>Date tested</dt><dd>{date}</dd>
    <dt>Demo page</dt><dd><a href="{demo}">{demo}</a></dd>
    <dt>Tools</dt><dd>{tools}</dd>
    <dt>Tested by</dt><dd>{tester}; cross-checked by {checker}</dd>
  </dl>
</section>
<p class="back"><a href="scorecard.html">Back to the full scorecard</a></p>""".format(
        bar=bar(c), counts=counts_text(n), overall=e(c["overall"]), best=e(c["best_for"]), watch=e(c["watch_out_for"]),
        sr=e(exp["screen_reader"]), kb=e(exp["keyboard"]), name=e(c["name"]), rows="".join(rows),
        vendor=e(c["vendor"]), claim=e(cv["claim"]), found=e(cv["found"]),
        date=e(c["test_date"] or "Not tested yet"), demo=e(c["demo_url"]), tools=e(c["tools"]),
        tester=e(c["tester"]), checker=e(c["cross_checker"]))
    page("{}.html".format(c["id"]), e(c["name"]), body, current="scorecard.html",
         kicker="{} · {}".format(e(c["style"]), tested), lede=e(c["description"]))


def build_checklist():
    page("checklist.html", "Developer checklist", content("checklist.html"))


def build_methods():
    crit_rows = "".join(
        '<tr><th scope="row"><a href="{}">{} {}</a></th><td>{}</td><td>{}</td></tr>'.format(
            CRITERIA[cid]["url"], cid, e(CRITERIA[cid]["name"]), CRITERIA[cid]["level"], e(CRITERIA[cid]["check"]))
        for cid in ORDER
    )
    crit_table = """<div class="table-scroll" role="region" aria-labelledby="m-caption" tabindex="0"><table class="results">
<caption id="m-caption" class="visually-hidden">The 10 WCAG 2.2 criteria and what we checked</caption>
<thead><tr><th scope="col">Criterion</th><th scope="col">Level</th><th scope="col">What we check</th></tr></thead>
<tbody>{}</tbody></table></div>""".format(crit_rows)
    ratings = "".join(
        '<dt><span class="key key-{}">{}</span></dt><dd>{}</dd>'.format(k, label(k), e(v["meaning"]))
        for k, v in RATINGS.items() if k != "untested"
    )
    body = content("methods.html").replace("{{CRITERIA_TABLE}}", crit_table).replace(
        "{{RATINGS_LIST}}", '<dl class="rating-defs">{}</dl>'.format(ratings))
    page("methods.html", "Methods &amp; sources", body)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copy(ROOT / "static/style.css", OUT / "style.css")
    (OUT / ".nojekyll").write_text("")
    build_home()
    build_comparison()
    for c in CAPTCHAS:
        build_captcha(c)
    if HAS_CHECKLIST:
        build_checklist()
    if HAS_METHODS:
        build_methods()
    print("Built {} pages into {}/".format(len(list(OUT.glob("*.html"))), OUT))


if __name__ == "__main__":
    main()

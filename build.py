#!/usr/bin/env python3
"""Builds the CAPTCHA Accessibility Scorecard into _site/.

You normally don't need to run this yourself: GitHub Actions runs it on every
push to main and publishes _site/ to GitHub Pages.

To preview locally:
    python3 build.py
    python3 -m http.server -d _site 8000   # then open http://localhost:8000

Only uses the Python standard library.
"""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
SITE_NAME = "CAPTCHA Accessibility Scorecard"
REPO_URL = "https://aaliyahali.github.io/is308-final-project-captcha-scorecard/" 

crit_data = json.loads((ROOT / "data/criteria.json").read_text(encoding="utf-8"))
CRITERIA = crit_data["criteria"]
GROUPS = crit_data["groups"]
RATINGS = crit_data["ratings"]
CAPTCHAS = json.loads((ROOT / "data/captchas.json").read_text(encoding="utf-8"))["captchas"]
ORDER = [c for g in GROUPS for c in g["criteria"]]

e = html.escape


def content(name):
    text = (ROOT / "content" / name).read_text(encoding="utf-8")
    return re.sub(r"<!--.*?-->\s*", "", text, count=1, flags=re.S)  # drop the owner comment


def anchor(cid):
    return "c-" + cid.replace(".", "-")


def badge(result, link=None):
    r = result.get("rating", "untested")
    info = RATINGS[r]
    prelim = "" if result.get("verified") else ' <span class="badge badge-prelim">Preliminary</span>'
    inner = f'<span class="rating rating-{r}"><span aria-hidden="true" class="icon">{info["icon"]}</span> {info["label"]}</span>{prelim}'
    return f'<a href="{link}" class="rating-link">{inner}</a>' if link else inner


def counts(c):
    n = {k: 0 for k in RATINGS}
    for cid in ORDER:
        n[c["results"].get(cid, {}).get("rating", "untested")] += 1
    return n


def counts_text(n):
    parts = [f'{n[k]} {RATINGS[k]["label"].lower()}' for k in ("pass", "partial", "fail") ]
    if n["untested"]:
        parts.append(f'{n["untested"]} not yet rated')
    return ", ".join(parts)


def all_verified():
    return all(r.get("verified") for c in CAPTCHAS for r in c["results"].values())


NAV = [("index.html", "Home"), ("scorecard.html", "Scorecard"), ("checklist.html", "Developer checklist"), ("methods.html", "Methods &amp; sources")]


def page(filename, title, body, current=None):
    nav = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if href == (current or filename) else ""}>{label}</a></li>'
        for href, label in NAV
    )
    draft = "" if all_verified() else (
        '<div class="draft-banner" role="note"><p><strong>Draft:</strong> ratings marked Preliminary come from published reports '
        'and haven\'t been confirmed by hands-on testing yet.</p></div>'
    )
    full_title = SITE_NAME if filename == "index.html" else f"{title} | {SITE_NAME}"
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="An accessibility audit of four popular CAPTCHAs against WCAG 2.2, with a checklist for developers.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap">
    <a class="site-name" href="index.html">{SITE_NAME}</a>
    <nav aria-label="Main"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main" tabindex="-1">
  {draft}
  <div class="wrap">
    <h1>{title}</h1>
    {body}
  </div>
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>Built by Aaliyah Ali and Anya Acharya for Designing Inclusive Information Technologies, University of Illinois Urbana-Champaign.</p>
    <p>Spotted a problem with this site or a rating? <a href="{REPO_URL}/issues/new/choose">Send feedback on GitHub</a>.</p>
  </div>
</footer>
</body>
</html>
"""
    (OUT / filename).write_text(doc, encoding="utf-8")


def build_home():
    cards = []
    for c in CAPTCHAS:
        n = counts(c)
        cards.append(f"""<li class="card">
  <h3><a href="{c['id']}.html">{e(c['name'])}</a></h3>
  <p class="card-style">{e(c['style'])}</p>
  <ul class="tally" aria-label="Results across 10 criteria">
    <li class="rating-pass"><span aria-hidden="true" class="icon">{RATINGS['pass']['icon']}</span> {n['pass']} pass</li>
    <li class="rating-partial"><span aria-hidden="true" class="icon">{RATINGS['partial']['icon']}</span> {n['partial']} partial</li>
    <li class="rating-fail"><span aria-hidden="true" class="icon">{RATINGS['fail']['icon']}</span> {n['fail']} fail</li>
  </ul>
</li>""")
    body = f"""{content('home-intro.html')}
<section aria-labelledby="results-heading">
  <h2 id="results-heading">Results at a glance</h2>
  <ul class="cards">{''.join(cards)}</ul>
</section>
<div class="cta">
  <a class="button" href="scorecard.html">See the scorecard</a>
  <a class="button button-secondary" href="checklist.html">Read the developer checklist</a>
</div>"""
    page("index.html", "Why CAPTCHAs lock disabled users out", body)


def build_comparison():
    head = "".join(f'<th scope="col"><a href="{c["id"]}.html">{e(c["name"])}</a></th>' for c in CAPTCHAS)
    groups = []
    for g in GROUPS:
        rows = [f'<tr class="group-row"><th scope="rowgroup" colspan="{len(CAPTCHAS) + 1}">{e(g["label"])}</th></tr>']
        for cid in g["criteria"]:
            cr = CRITERIA[cid]
            cells = "".join(
                f'<td>{badge(c["results"].get(cid, {}), f"{c["id"]}.html#{anchor(cid)}")}</td>' for c in CAPTCHAS
            )
            rows.append(f'<tr><th scope="row"><span class="crit-id">{cid}</span> {e(cr["name"])} <span class="level">({cr["level"]})</span></th>{cells}</tr>')
        groups.append(f'<tbody>{"".join(rows)}</tbody>')
    totals = "".join(f"<td>{counts_text(counts(c))}</td>" for c in CAPTCHAS)
    body = f"""<p class="lede">All four CAPTCHAs across the 10 WCAG 2.2 criteria, grouped by who each criterion affects most. Select a rating to read the note behind it.</p>
<div class="table-scroll" role="region" aria-labelledby="cmp-caption" tabindex="0">
<table class="compare">
  <caption id="cmp-caption">Accessibility ratings by WCAG 2.2 criterion</caption>
  <thead><tr><th scope="col">Criterion</th>{head}</tr></thead>
  {''.join(groups)}
  <tfoot><tr><th scope="row">Totals</th>{totals}</tr></tfoot>
</table>
</div>
<p>What the ratings mean: see <a href="methods.html#ratings">rating definitions</a>.</p>"""
    page("scorecard.html", "Scorecard comparison", body)


def build_captcha(c):
    rows = []
    for cid in ORDER:
        cr = CRITERIA[cid]
        r = c["results"].get(cid, {"rating": "untested", "note": ""})
        rows.append(f"""<tr id="{anchor(cid)}">
  <th scope="row"><a href="{cr['url']}"><span class="crit-id">{cid}</span> {e(cr['name'])}</a> <span class="level">({cr['level']})</span></th>
  <td>{badge(r)}</td>
  <td>{e(r.get('note', ''))}</td>
</tr>""")
    n = counts(c)
    exp = c["experience"]
    cv = c["claims_vs_found"]
    body = f"""<p class="meta"><span>Vendor: {e(c['vendor'])}</span> <span>Challenge style: {e(c['style'])}</span></p>
<p class="lede">{e(c['description'])}</p>

<section aria-labelledby="overall" class="summary">
  <h2 id="overall">Overall result</h2>
  <p class="tally-line">{counts_text(n)}</p>
  <p>{e(c['overall'])}</p>
  <div class="two-col">
    <div><h3>Best for</h3><p>{e(c['best_for'])}</p></div>
    <div><h3>Watch out for</h3><p>{e(c['watch_out_for'])}</p></div>
  </div>
</section>

<section aria-labelledby="criteria-h">
  <h2 id="criteria-h">Criteria results</h2>
  <div class="table-scroll" role="region" aria-labelledby="crit-caption" tabindex="0">
  <table class="results">
    <caption id="crit-caption">{e(c['name'])}: results for each WCAG 2.2 criterion</caption>
    <thead><tr><th scope="col">Criterion</th><th scope="col">Rating</th><th scope="col">Note</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  </div>
</section>

<section aria-labelledby="experience">
  <h2 id="experience">What a user actually experiences</h2>
  <h3>Screen-reader users</h3>
  <p>{e(exp['screen_reader'])}</p>
  <h3>Keyboard-only users</h3>
  <p>{e(exp['keyboard'])}</p>
</section>

<section aria-labelledby="claims">
  <h2 id="claims">Vendor claims vs. what we found</h2>
  <h3>What the vendor says</h3>
  <p>{e(cv['claim'])}</p>
  <h3>What we found</h3>
  <p>{e(cv['found'])}</p>
</section>

<section aria-labelledby="details">
  <h2 id="details">Test details</h2>
  <dl class="details">
    <dt>Date tested</dt><dd>{e(c['test_date'] or 'Not yet tested')}</dd>
    <dt>Demo page</dt><dd><a href="{e(c['demo_url'])}">{e(c['demo_url'])}</a></dd>
    <dt>Tools</dt><dd>{e(c['tools'])}</dd>
    <dt>Tested by</dt><dd>{e(c['tester'])}; cross-checked by {e(c['cross_checker'])}</dd>
  </dl>
</section>
<p><a href="scorecard.html">Back to the comparison</a></p>"""
    page(f"{c['id']}.html", c["name"], body, current="scorecard.html")


def build_checklist():
    page("checklist.html", "Developer checklist", content("checklist.html"))


def build_methods():
    crit_rows = "".join(
        f'<tr><th scope="row"><a href="{CRITERIA[cid]["url"]}">{cid} {e(CRITERIA[cid]["name"])}</a></th><td>{CRITERIA[cid]["level"]}</td><td>{e(CRITERIA[cid]["check"])}</td></tr>'
        for cid in ORDER
    )
    crit_table = f"""<div class="table-scroll" role="region" aria-labelledby="m-caption" tabindex="0"><table class="results">
<caption id="m-caption">The 10 WCAG 2.2 criteria and what we checked</caption>
<thead><tr><th scope="col">Criterion</th><th scope="col">Level</th><th scope="col">What we check</th></tr></thead>
<tbody>{crit_rows}</tbody></table></div>"""
    ratings = "".join(
        f'<dt>{badge({"rating": k, "verified": True})}</dt><dd>{e(v["meaning"])}</dd>'
        for k, v in RATINGS.items() if k != "untested"
    )
    body = content("methods.html").replace("{{CRITERIA_TABLE}}", crit_table).replace(
        "{{RATINGS_LIST}}", f'<dl class="rating-defs">{ratings}</dl>'
    )
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
    build_checklist()
    build_methods()
    print(f"Built {len(list(OUT.glob('*.html')))} pages into {OUT}/")


if __name__ == "__main__":
    main()

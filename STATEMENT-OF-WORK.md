# Statement of Work

**Project:** CAPTCHA Accessibility Scorecard
**Course:** Designing Inclusive Information Technologies, UIUC, Fall 2026
**Team:** Aaliyah Ali and Anya Acharya
**Live site:** https://aaliyahali.github.io/is308-final-project-captcha-scorecard/
**Repo:** https://github.com/aaliyahali/is308-final-project-captcha-scorecard

## Deadlines (from the assignment)

| Deliverable | Due |
|---|---|
| Part 2: Released project + README, submitted to Canvas | December 1 |
| Part 3: 5–10 minute pitch presentation | December 1, 3 or 8 (our assigned slot) |

## The split at a glance

| Area | Owner | Reviewer |
|---|---|---|
| Home page | Aaliyah | Anya |
| Part 1: Scorecard comparison page | Aaliyah | Anya |
| Part 1: The four CAPTCHA pages | Aaliyah | Anya |
| Testing all four CAPTCHAs | Aaliyah | Anya (cross-check) |
| Part 2: Developer checklist page | Anya | Aaliyah |
| Methods & Sources page | Anya | Aaliyah |
| README | Both | Both |
| Shared design (`build.py`, `static/style.css`, `data/criteria.json`) | Change only by agreement | The other person |
| Presentation | Both | Both |

## Aaliyah's work

### 1. Run all four audits
For each of reCAPTCHA v2, hCaptcha, Cloudflare Turnstile and the slider CAPTCHA (GeeTest), follow `TESTING-WORKSHEET.md`:
- An automated first pass with axe DevTools or WAVE.
- A keyboard-only pass with the mouse off: 2.1.1, 2.4.7, 2.5.7, 2.5.8, 2.2.1.
- A VoiceOver pass: 4.1.2, 1.1.1, 1.3.1, 3.3.8.
- A zoom pass at 200%: 1.4.4.
- A screen recording of each session, for evidence and demo clips.

### 2. Put the results on the site
In `data/captchas.json`, for each CAPTCHA:
- Update every `rating` and `note` to match what testing showed.
- Write the two `experience` paragraphs: one for screen-reader users, one for keyboard-only users.
- Fill in `claims_vs_found.found`, `overall`, `best_for` and `watch_out_for`.
- Fill in `test_date`.

### 3. Home and Scorecard
- Edit the home page text in `content/home-intro.html` as needed.
- Check that the comparison table and totals match the final ratings.

### 4. Review Anya's pages
Review her pull requests for the checklist and Methods pages. Check that they match the scorecard findings and that they work with the keyboard and VoiceOver.

## Anya's work

### 1. Developer checklist (Part 2)
Create `content/checklist.html`. The page and its nav link appear on the site automatically once this file exists.

The plan from our pitch is a top-to-bottom guide in three stages:
1. **Do you need a CAPTCHA at all?** A short yes/no check.
2. **Try lower-barrier options first:** honeypot fields, rate limiting, email verification, passkeys.
3. **If a CAPTCHA stays, the must-haves:** a text label for its purpose, a working keyboard path, visible focus, no drag-only step, adequate or extendable time limits, targets at least 24×24 CSS px, a puzzle-free path on login (3.3.8), and testing with a screen reader before launch.

Where it fits, point to specific findings from the scorecard. For example, "the slider CAPTCHA failed 2.5.7" makes the no-drag rule concrete.

### 2. Methods & Sources page
Create `content/methods.html`. It should cover:
- What we tested and why: four CAPTCHAs, two user groups.
- The 10 criteria and what we checked for each.
- Rating definitions: Pass, Partial, Fail.
- Testing tools and process: VoiceOver, keyboard only, 200% zoom, axe/WAVE, and the cross-check.
- Limitations: we're not screen-reader users ourselves, we used one screen reader, CAPTCHAs change difficulty based on risk, demo pages may differ from real sites, and results reflect the test dates.
- References: the sources list from our pitch.

**Shortcut:** put `{{CRITERIA_TABLE}}` or `{{RATINGS_LIST}}` anywhere in the file, and the build replaces it with the criteria table or the rating definitions, generated from `data/criteria.json`.

### 3. Cross-check Aaliyah's ratings
For each CAPTCHA, re-test at least two criteria, picked by you, using `TESTING-WORKSHEET.md`. If you disagree with a rating, comment on it and we re-test together. This is what lets the Methods page say our ratings were cross-checked.

### 4. Review Aaliyah's pull requests
Look over the ratings and CAPTCHA page text before they're merged.

## How to write a page file

- Files in `content/` are **HTML fragments**: no `<html>`, `<head>` or `<body>` tags. `build.py` wraps them in the site's header, nav and footer.
- The page title is already the h1, so start your headings at `<h2>` and keep them in order.
- Link text should say where it goes. No "click here".
- Don't use color as the only way to show meaning.
- Ready-made styles you can use: `class="step"` (a boxed section), `class="step-num"` (a small label above a heading), `class="checklist"` (a list with checkbox markers), `class="callout"` (a highlighted note), `class="options"` (on a `<dl>`, for term and description pairs), `class="refs"` (a reference list).

## How we work in the repo

1. **Get set up once:** `git clone https://github.com/aaliyahali/is308-final-project-captcha-scorecard.git`
2. **Make a branch** for each piece of work, e.g. `git checkout -b anya-checklist`.
3. **Preview locally:** `python3 build.py` then `python3 -m http.server -d _site 8000`, and open http://localhost:8000.
4. **Push your branch** and open a pull request into `main`. The other person reviews it.
5. **Merge.** The live site updates in about a minute.

Before opening a pull request, Tab through your page with the mouse off and listen to it with VoiceOver (Cmd + F5).

## Proposed timeline (adjust together)

| Target date | Milestone |
|---|---|
| Nov 23 | Aaliyah finishes all four tests and updates `data/captchas.json` |
| Nov 25 | Anya's first drafts of the checklist and Methods pages are in a pull request |
| Nov 27 | Anya's cross-check done; disagreements settled |
| Nov 29 | Final read-through of the whole site together; README finalized |
| Nov 30 | Presentation slides drafted; agree who presents what |
| Dec 1 | Submit to Canvas (submitter: ______) |

## Presentation (Part 3)

| Section | Presenter |
|---|---|
| The problem and the research numbers | ______ |
| How we tested + live demo of a CAPTCHA with VoiceOver or keyboard | Aaliyah |
| Scorecard results | Aaliyah |
| Developer checklist and what it would take to implement | Anya |
| Limitations and next steps | ______ |

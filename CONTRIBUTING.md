# How we split the work

## Who owns what

Fill in names, then delete this line.

| Area | Files | Owner | Reviewer |
|---|---|---|---|
| Shared look and layout | `static/style.css`, `build.py`, `data/criteria.json` | Both (agree first) | the other person |
| **Part 1:** scorecard pages | `data/captchas.json` (comparison + 4 CAPTCHA pages are generated from it) | ______ | ______ |
| **Part 2:** developer checklist | `content/checklist.html` | ______ | ______ |
| Home, Methods & Sources | `content/home-intro.html`, `content/methods.html` | ______ | ______ |
| README | `README.md` | ______ | ______ |

**Testing split** (by CAPTCHA, so each person edits a different block of `data/captchas.json`):

| CAPTCHA | Tester | Cross-checker |
|---|---|---|
| reCAPTCHA v2 | ______ | ______ |
| hCaptcha | ______ | ______ |
| Cloudflare Turnstile | ______ | ______ |
| Slider (GeeTest) | ______ | ______ |

## Workflow

1. **Make a branch** for each piece of work, e.g. `part2-checklist` or `test-hcaptcha`. You can do this in GitHub's web editor: edit a file, then choose "Create a new branch for this commit".
2. **Open a pull request** into `main`. GitHub Actions builds the site to check it isn't broken.
3. **The other person reviews it.** For rating changes, this review is the cross-check. If you disagree with a rating, discuss it in the PR comments and re-test together.
4. **Merge.** The live site updates in about a minute.

## Updating a rating after testing

In `data/captchas.json`, find the CAPTCHA and criterion, then:

```json
"2.1.1": {"rating": "fail", "verified": true, "note": "Slider can't be moved with arrow keys; voice option not reachable with Tab."}
```

- `rating`: `pass`, `partial`, `fail` or `untested`
- `verified`: set to `true` only after hands-on testing **and** the cross-check. The "Preliminary" tag and draft banner disappear once every rating is verified.
- `note`: one line describing what a user actually runs into.

Also fill in `tester`, `cross_checker`, `test_date`, the two `experience` paragraphs, and `claims_vs_found.found`.

## Accessibility rules for our own site

- Use headings in order (the page title is the h1; sections start at h2).
- Every link says where it goes. No "click here".
- Never use color alone to show meaning.
- Before merging a page change, Tab through it with the mouse off and run it through VoiceOver.

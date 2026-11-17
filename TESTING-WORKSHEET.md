# Testing worksheet

Copy this once per CAPTCHA, or work straight into `data/captchas.json`. Allow about 30–45 minutes per CAPTCHA.

**CAPTCHA:** ________ **Tester:** ________ **Date:** ________
**Demo URL:** ________ **Browser + version:** ________ **macOS version:** ________

## Setup

- [ ] VoiceOver on/off: **Cmd + F5**. VO keys = **Control + Option**.
- [ ] Safari: turn on **Settings › Advanced › Press Tab to highlight each item on a webpage**. Also turn on Full Keyboard Access in System Settings › Keyboard if needed.
- [ ] Disconnect the mouse, or turn off the trackpad, for the keyboard-only pass.
- [ ] Run axe DevTools or WAVE once, and record any findings on the CAPTCHA widget. Many will be blocked by the iframe; note that too.
- [ ] Start a screen recording (Cmd + Shift + 5) with VoiceOver audio. It's useful as evidence and for the presentation demo.

## Pass 1: Keyboard only (mouse off, VoiceOver off)

| Criterion | What to do | Rating | Note |
|---|---|---|---|
| 2.1.1 Keyboard | Tab to the widget. Complete every step using only Tab / Shift+Tab / Enter / Space / arrows. Note any keyboard trap. | | |
| 2.4.7 Focus Visible | At every step, can you see where focus is? Screenshot any step where you can't. | | |
| 2.5.7 Dragging | Is any step drag-only? Is there a click or key alternative? | | |
| 2.5.8 Target Size | Inspect element › Computed. Record width and height of the checkbox and small icon buttons. ≥ 24×24? | | |
| 2.2.1 Timing | Time how long you have. Wait it out: what happens? Can you extend it? | | |

## Pass 2: VoiceOver

| Criterion | What to do | Rating | Note |
|---|---|---|---|
| 4.1.2 Name, Role, Value | Write down exactly what VoiceOver says for each control, e.g. "I'm not a robot, unchecked, checkbox". | | |
| 1.1.1 Non-text Content | Is the CAPTCHA's purpose announced? Can you find and use a non-visual alternative (audio, text challenge, voice)? | | |
| 1.3.1 Info and Relationships | Are the instructions read when you reach the input or tiles? Is the answer field labeled? | | |
| 3.3.8 Accessible Authentication | Could you get through without solving a puzzle (cookie, passive check, alternative)? | | |

Also record: **time to complete**, **number of attempts**, and whether the audio talked over VoiceOver.

## Pass 3: Zoom

| Criterion | What to do | Rating | Note |
|---|---|---|---|
| 1.4.4 Resize Text | Cmd + Plus to 200%. Is anything cut off or overlapping? Can you still finish? | | |

## Write-up (goes on the CAPTCHA's page)

- **Screen-reader experience** (2–4 sentences):
- **Keyboard-only experience** (2–4 sentences):
- **Vendor claim vs. what we found:**
- **Best for / Watch out for:**

## Cross-check

**Cross-checker:** ________ **Date:** ________
Any ratings you disagree with, and what you agreed after re-testing:

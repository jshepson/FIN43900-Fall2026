# Video 1 — Research evolution: exact recording guide

**Target length:** 2–3 minutes. **Read aloud:** only [video-1-research-evolution.md](video-1-research-evolution.md). This guide is for screen actions; do not read it aloud or submit it as the video transcript.

## Before pressing record

1. Open these four browser tabs, in this order:
   - `project-2-submission/README.md` on GitHub or in your editor.
   - `project-2-submission/mandate_reference.py`.
   - `project-2-submission/docs/decision-memo.md`.
   - The running app at `http://127.0.0.1:8000`.
2. Leave the app at: **59 monthly returns**, **Costs 0**, **Estimate haircut 0**, **Reserve minimum 3**.
3. Start recording with the README visible.

## Exact screen sequence while reading the transcript

| Spoken transcript section | What must be on screen | Action |
|---|---|---|
| AI disclosure | README top section | Point to the AI disclosure sentence. |
| “I began with the Meridian Foundation mandate” | `mandate_reference.py` | Scroll only enough to show `RESERVE_SIZE`, `QUARTERLY_DISTRIBUTION`, `QUARTERS_TO_COVER`, and `MINIMUM_LIQUID_SHARE`. |
| “3 percent reserve” / hard constraints | Same mandate file | Point to the reserve calculation inputs; do not claim the four-ticker universe meets them. |
| “supplied research universe is QQQ…” | Running app | Show the baseline/candidate table and red STOP message. Point to “No feasible allocation.” |
| “59-month… latest-36-month” | App | Change **Reserve minimum** from `3` to `0`; click **Run stress**. Keep costs/haircut at `0`. Then change **Return window** to **latest 36**; click **Run stress**. |
| “AI output I checked” through decision | Decision memo | Show the Recommendation heading and Conditions that would reverse the decision. |

## End

Stop recording after the last sentence. Do not include setup mistakes, browser searches, or an unedited long pause.

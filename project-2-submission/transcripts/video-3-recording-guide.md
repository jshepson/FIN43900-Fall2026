# Video 3 — Committee presentation: exact recording guide

**Target length:** 3–5 minutes. **Read aloud:** only [video-3-committee-presentation.md](video-3-committee-presentation.md). This guide is screen direction, not spoken transcript text.

## Before pressing record

1. Start the app in Terminal with `python3 app.py` from `project-2-submission`.
2. In the browser, open `http://127.0.0.1:8000`.
3. Set exactly: **Return window = 59 monthly returns**, **Costs = 0**, **Estimate haircut = 0**, **Reserve minimum = 3**. Click **Run stress**.
4. Scroll the browser so the red STOP box and the table’s constrained-grid-candidate row are both visible.
5. Start recording. The first frame must show the live running app—not Terminal, GitHub, or a title slide.

## Exact screen sequence while reading the transcript

| Spoken transcript section | What must be on screen | Action |
|---|---|---|
| AI disclosure and recommendation | Live app’s red STOP box/table | Point to STOP and “No feasible allocation.” |
| “reason is simple and decisive” | Same app view | Point to the 3% reserve control and candidate verdict. Do not change settings. |
| “material instability” | App stress controls | Change **Reserve minimum** to `0`; click **Run stress**. Point to 75% SPY / 25% VOO mechanics-only candidate. Then select **latest 36**; click **Run stress** and point to 100% SPY. |
| “Costs and estimate haircuts…” | App stress controls/table | Enter **Costs = 50**, click **Run stress**; then enter **Estimate haircut = 1**, click **Run stress**. Point to Net estimate. |
| “applying the real reserve…” | App | Restore **Reserve minimum = 3**; click **Run stress**. Point to “No feasible allocation.” |
| “I will monitor…” / reversal conditions | Decision memo | Switch to `docs/decision-memo.md`; show “Monitoring and reversal triggers.” |

## End

Return briefly to the live app for the final “no capital should be allocated” sentence. End while the red STOP box is visible.

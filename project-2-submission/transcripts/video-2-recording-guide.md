# Video 2 — Code and validation: exact recording guide

**Target length:** 3–5 minutes. **Read aloud:** only [video-2-code-walkthrough.md](video-2-code-walkthrough.md). This guide is screen direction, not spoken transcript text.

## Before pressing record

1. Open Terminal, a code editor with `project-2-submission/app.py`, and a browser.
2. In Terminal, type but do not run yet:

   ```sh
   cd /Users/josiahshepson/FIN43900-Fall2026/project-2-submission
   python3 app.py
   ```

3. Keep the browser on an unrelated blank tab. Start recording.

## Exact screen sequence while reading the transcript

| Spoken transcript section | What must be on screen | Exact action |
|---|---|---|
| “I am starting the application…” | Terminal | Press Return after the `cd` command, then press Return after `python3 app.py`. Show the “Serving Meridian app” line. |
| “The app is now running live…” | Browser address bar | Enter `http://127.0.0.1:8000` and press Return. |
| “standard library… frozen data…” | Code editor | Show top imports and `PRICE_FILE`; then briefly open `data/prices.csv` and show the date/ticker headers. |
| “price_data reads… Estimates converts…” | Code editor | Scroll to `price_data` and `estimates`. Point only; do not attempt to explain every line. |
| “Portfolio statistics…” | Code editor | Scroll to `portfolio_stats` and `optimize`; point to `if reserve_minimum > 0: return None`. |
| “table shows…” | Browser app | Set **Return window = 59 monthly returns**, **Costs = 0**, **Estimate haircut = 0**, **Reserve minimum = 3**. Click **Run stress**. Point to the red STOP box and candidate “No feasible allocation.” |
| “temporarily change…” | Browser app | Change **Reserve minimum** to `0`; click **Run stress**. Point to constrained grid candidate weights. |
| “change window…” | Browser app | Change **Return window** to **latest 36**; click **Run stress**. Point to changed candidate weights. |
| “enter 50…” | Browser app | Enter **Costs = 50**; click **Run stress**. Then enter **Estimate haircut = 1**; click **Run stress**. Point to Net estimate. |
| “return reserve…” | Browser app | Set **Reserve minimum = 3**; click **Run stress**. Point again to “No feasible allocation.” |

## End

Keep Terminal running until the video is finished. Stop the recording, then later use `Control + C` in Terminal to stop the app.

# Project 2 — Meridian Investment Management Application

**AI disclosure:** I used Codex to help organize the app, documentation, and reproducibility checks. The analysis and decision are mine. This is for education, not investment advice.

## Committee decision

**Reject the QQQ/SPY/NVDA/VOO model allocation for Meridian reserve capital; retain it only as a research pilot.** The supplied four-ticker universe has no cash or government-security reserve sleeve, so it cannot meet Meridian's 3.0% reserve requirement. The 59-month versus latest-36-month window check also changes the mechanics-only candidate by 25 percentage points, above the predeclared 20-point stability limit.

## Start the app

Requirements: Python 3.10+ only. No package installation, account, network call, or environment file is needed.

```sh
cd assignments/project-2-investment-management-app
python3 app.py
```

Open <http://127.0.0.1:8000>. Press `Ctrl+C` to stop. A reviewer can alter the estimation window, costs, estimate haircut, and reserve constraint in the web interface. The app shows two transparent baselines beside the constrained 5%-grid candidate, its mandate verdict, one point-in-time signal/data card, stresses, and the stop condition.

## Project files

- `app.py` — runnable standard-library Python web application.
- `data/prices.csv` — frozen monthly adjusted-close research input.
- `mandate_reference.py` — Lab 13's original checkable Meridian mandate, preserved as provenance.
- `docs/decision-memo.md` — committee recommendation, allocation range, triggers, and risks.
- `docs/validation-and-ai-use.md` — data/validation/AI-use ledger and changed-input procedure.
- `docs/locked-changed-input-record.md` — the student-authored, commit-before-run record that must be completed honestly.
- `transcripts/` — recording-ready verbatim scripts for the three required videos.
- `project-submission-manifest.csv` — final submission checklist and locations.

## Mandate and method

The decision user is the Meridian Foundation CIO managing a $100m reserve, with a seven-year horizon and annual rebalancing. The objective is CPI + 4% net of costs over rolling five-year periods. The comparison benchmark is 60% global equity / 40% U.S. investment-grade bonds. Hard constraints include long-only/no derivatives, four quarterly payouts held in cash or daily-liquid government securities (3.0% reserve minimum), at least 90% redeemable within five business days, 8% maximum non-exempt company exposure, and committee approval above 25% turnover. The calendar-year loss measure and breach response remain unspecified.

The four-ticker classroom research universe is QQQ, SPY, NVDA, and VOO. It is deliberately not a substitute for Meridian's full investable universe. The candidate enumerates long-only weights in five-percentage-point increments, seeks the lowest volatility subject to a 6.5% annual net historical-estimate floor, and never relaxes a positive reserve rule. Equal-weight and inverse-volatility allocations are the two transparent comparison baselines.

## Before submitting

1. Read every displayed number and every statement in the memo; edit only if it does not accurately reflect your work.
2. With AI off, choose one **fresh** app-control stress not already disclosed in this repository, then complete the human-authored prediction in `docs/locked-changed-input-record.md` **before** running it. Commit and push that prediction. Run only that setting without AI help, append the actual result, then commit and push again. Do not backdate or manufacture this record. The already-disclosed 59-versus-36-month comparison cannot be reused as the prediction.
3. Start the app from a fresh terminal, screen-record the three videos using the scripts in `transcripts/`, upload them to YouTube as unlisted/public, enable captions/transcripts, and replace the `VIDEO_URL_*` placeholders in the manifest.
4. Check each YouTube link while logged out and add its duration plus timestamp index in the manifest. If your spoken words differ from a supplied script, correct the matching transcript file so it matches the video.
5. Replace `COMMIT_AFTER_YOUR_LOCKED_RECORD` in the manifest with the actual commit SHA. Commit and push the folder. Attach `docs/decision-memo.md` and `docs/validation-and-ai-use.md` to Brightspace, and submit the repository and three YouTube links there.

The video files themselves must not be committed to GitHub. The placeholder items are intentionally not marked complete because only the student can make a truthful pre-run prediction, record a video, upload it, and verify a live external link.

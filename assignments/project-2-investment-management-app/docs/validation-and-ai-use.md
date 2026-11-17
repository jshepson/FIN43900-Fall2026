# Validation and AI Use — Project 2

**AI disclosure:** I used Codex to help organize the app, documentation, and reproducibility checks. The analysis and decision are mine. This is for education, not investment advice.

## Data card and conventions

| Field | Record |
|---|---|
| Decision / user | Meridian Foundation CIO; reject allocation, research pilot only |
| Source | Yahoo Finance monthly adjusted closes, obtained through `yfinance` on 2026-10-22 and frozen in `data/prices.csv` |
| Availability boundary | 2021-11-01 through 2026-10-01; no observation after the as-of date enters a calculation |
| Universe | QQQ, SPY, NVDA, VOO; no reserve-eligible sleeve is present |
| Transform | Simple monthly returns; arithmetic mean × 12; sample volatility × √12; same-return-sample correlations |
| Signal | Trailing 12-month simple price momentum at 2026-10-01; displayed only, not selected/optimized on |
| Costs | Stated bps subtract from gross historical estimate; no transaction-cost vendor model is available |
| Major data risk | Adjusted closes may be vendor-revised; historical arithmetic estimates are not forecasts |

## Validation register

| Check | Expected result | Actual / decision |
|---|---|---|
| Cold app launch | `python3 app.py` serves a local app with no third-party packages | Required before submission; record your check in the manifest |
| Weights / covariance | Candidate grid weights sum to 100%; volatility uses all covariance terms | Implemented in `app.py`; inspect in Video 2 |
| Baselines | Equal-weight and inverse-volatility rows appear beside candidate | Present; each receives a mandate verdict |
| Mandate reserve | 3.0% actual reserve minimum cannot be met by four-ticker universe | Fail / reject: 0.0% eligible reserve weight |
| Window stress | 59 vs latest 36 return windows should be compared | Mechanics-only candidate moves 75% SPY / 25% VOO to 100% SPY: 25-point shift; exceeds 20-point stop threshold |
| Cost stress | Higher bps should lower net estimate, not alter gross estimate | Available as an app control; use in Video 2 |
| Estimate stress | Larger haircut should lower net estimate and can eliminate feasibility | Available as an app control; use in Video 2 |
| Constraint stress | Positive reserve setting must produce no candidate, never an undisclosed relaxation | Implemented: any positive reserve minimum is infeasible |
| Decision | Hard-rule failure or >20-point stress shift stops allocation | Reject allocation / 0% current capital |

## Locked changed-input record

The required record is [locked-changed-input-record.md](locked-changed-input-record.md). Its current status is **open**, because a valid pre-run AI-off prediction must be authored, committed, and pushed by the student before the run. This package does not fabricate that evidence. Complete it using the procedure in the README, preserve both commits, and update the manifest before submission.

## AI-use register

| Tool | What it helped do | What I independently checked | Decision impact |
|---|---|---|---|
| Codex, 2026-11-17 | Organized the standard-library web app, documentation, and reproducibility structure from prior course inputs | I must read the code, run the app, inspect displayed outputs, and own the locked prediction | None; it cannot cure the reserve, cost, loss-rule, or stability failures |
| AI in prior portfolio exercises | Assisted with calculation structure and documentation | Earlier Lab 14/15 source checks and output comparison | No automatic adoption; the mandate still governs |

## Reproducibility boundary

Run `python3 app.py` in this folder and open the local address printed by the server. The app does not download current data; it operates only on the versioned frozen CSV. At every later cutoff, preserve a new source copy, document vendor revision risk, rerun the locked tests, and escalate any failed condition to the CIO.

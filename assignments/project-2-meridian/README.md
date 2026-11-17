# Project 2 — Meridian Historical-Window Allocation Review

**Lab 20:** Start with [SUBMIT-LAB-20.md](SUBMIT-LAB-20.md) for the complete one-folder submission index.

## Decision and intended user

For the Meridian Foundation CIO, **reject the QQQ/SPY/NVDA/VOO output as an adoptable allocation and retain it only as a pilot calculation.** The supplied universe lacks a reserve asset and has overlapping S&P 500 exposures; its lowest-risk answer changes materially when the estimation window changes. Reconsider only after the mandate defines a genuine reserve sleeve, net-of-costs objective, overlap treatment, loss rule, and breach response, and the result passes stability tests.

## One-command cold run

From the repository root, with Python 3.10+ and no third-party packages:

```sh
python3 assignments/project-2-meridian/analysis.py
```

The command prints the decision, inputs, as-of date, estimated returns, and both allocations. The same rounded decision facts are readable without execution in [visible_output.json](visible_output.json).

## Repository map

- `analysis.py` — Project 2 reproducibility entry point.
- `visible_output.json` — frozen executed output for GitHub review.
- `docs/decision-memo.md` — committee decision, conditions, and risks.
- `docs/validation-and-ai-use.md` — evidence ledger, validation, AI disclosure, and the truthful changed-input status.
- `Lab_20_Project2_Readiness.md` — individual checkout draft; items requiring the student/partner remain explicitly unresolved.
- `../week-09-portfolio-baselines/portfolio.py` — tested calculation engine.
- `../week-09-portfolio-baselines/prices.csv` — 60 monthly adjusted-close observations for QQQ, SPY, NVDA, and VOO.

## Data and conventions

The price source is Yahoo Finance, downloaded via `yfinance` on 2026-10-22. The file runs 2021-11-01 through 2026-10-01. The engine converts simple monthly adjusted-close returns to arithmetic mean × 12 and sample volatility × sqrt(12), calculates correlations from the same return observations, and enumerates long-only 5-percentage-point grid weights. These are historical estimates, not forecasts.

The 6.5% objective is a labelled classroom input. No cost or turnover model is present, so outputs are gross and pre-cost. The supplied universe contains no reserve-eligible asset; its documented reserve floor is therefore 0%, which is an adoption blocker rather than a satisfied Meridian mandate.

## Validation and reversal triggers

The base window and latest-36-month window produce different minimum-risk allocations. See the visible output and validation record. Do not adopt or allocate capital unless the reversal conditions in the decision memo are met.

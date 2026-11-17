# Lab 20 — Project 2 Readiness Checkout

**Lab date:** 2026-11-17  
**Project:** Meridian historical-window allocation review  
**Decision line:** **Reject** the QQQ/SPY/NVDA/VOO output as an adoptable allocation; retain it only as a pilot calculation. Reverse only after a complete mandate, genuine reserve sleeve, net-of-costs objective, overlap treatment, and stable predeclared validation results.

## What is ready

The 12-row status and locations are in [project-submission-manifest.csv](project-submission-manifest.csv). Currently ready in the repository: a one-command Python 3 run, visible output, a decision memo in Markdown, and a validation/AI-use record in Markdown. The command is:

```sh
python3 assignments/project-2-meridian/analysis.py
```

It was run locally on 2026-11-17 with Python 3; the result is also readable in `visible_output.json`. No third-party dependency is required. The first local attempt using `python` failed because that command is not installed; the README now specifies `python3`.

## Cold run — partner record required

**Status: not yet independently performed. Do not claim this is complete until a partner fills this in without coaching.**

| Partner name | Clone/folder | Exact command | First failure | Elapsed time | Result location | Rerun after fix |
|---|---|---|---|---|---|---|
|  |  | `python3 assignments/project-2-meridian/analysis.py` |  |  | `assignments/project-2-meridian/visible_output.json` |  |

## Changed input — required student action

**Status: open.** The historical all-59 versus latest-36-month comparison is preserved as validation evidence, but it is not a compliant Locked Changed-Input Record because no pre-run student prediction and immutable prediction commit are available. Before rerunning, the student must personally write the old/new window and units, expected number directions, and expected decision effect; commit and push that prediction; then run without AI assistance and complete the actual/reconciliation fields in `docs/validation-and-ai-use.md`.

## Explain-code prompt

Explain `analysis.py` top to bottom: it anchors the repository path, imports the existing tested portfolio engine, calls `estimate_from_prices` for each window, calls `find_lowest_risk_mix` with a 6.5% objective and 0% documented reserve floor, then prints the reviewable JSON decision/output. Partner question and answer: **not yet recorded.**

## Fix-one-thing status

The local `python` failure is repaired by using the explicit `python3` README command. A partner must rerun after pulling the pushed change before this can be recorded as the required partner-confirmed fix.

## Submission-only fields — complete personally in class

- Teammates/learning partners/contribution: **not supplied**
- Instructional-team access check: **not yet checked**
- Video/transcript/duration checks: **not ready; see manifest**
- Session token: **enter the token announced in the room; never invent it**
- In-person attendance declaration and truth attestation: **student must make personally**
- Brightspace receipt: **attach after submission**
- Unresolved blocker and attempted fix: missing Edition A/B PDF, locked prediction commit, partner cold run, three videos, transcripts, and final PDFs.

## Reflection / growth note

I can now trace a portfolio recommendation from price data through return estimates, covariance, constraints, grid search, and a visible decision output, and I can test whether the result is stable when the estimation window changes. What remains shaky is distinguishing a reproducible historical calculation from an allocation that actually satisfies a client's complete mandate. I will not touch the core calculation before the deadline without documenting a specific input, expected direction, test, and result.

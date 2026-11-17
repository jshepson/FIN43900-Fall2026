# Validation and AI Use

## Decision, version, and as-of boundary

Decision/user: Meridian Foundation CIO; reject the QQQ/SPY/NVDA/VOO result as an adoptable allocation and retain it only as a pilot calculation. Run `python3 assignments/project-2-meridian/analysis.py` from the repository root. Source cutoff: 2026-10-01 monthly adjusted-close observation; downloaded 2026-10-22. The Git commit for the final Project 2 package has **not yet been created**.

## Data and convention ledger

| Material input | Source | As-of/availability | Definition/units | Transformation/exclusion | Risk |
|---|---|---|---|---|---|
| QQQ, SPY, NVDA, VOO monthly adjusted close | Yahoo Finance via `yfinance`; `../week-09-portfolio-baselines/prices.csv` | Downloaded 2026-10-22; final observation 2026-10-01 | USD adjusted closes, oldest first | Simple monthly return; arithmetic mean × 12, sample volatility × sqrt(12) | Revised vendor data; backward-looking estimates |
| Return objective | Course-labelled Meridian input | Not a market observation | 6.5% annual gross expected return | Feasibility floor in 5% grid search | Not approved net-of-costs mandate |
| Reserve constraint | Supplied universe | No reserve asset present | 0% documented floor for this exercise | `reserve_minimum=0` | Does not meet Meridian's 3% reserve mandate |

## Validation register

| Claim/output | Failure mode | Test and expected direction | Actual result | Disposition | Evidence location |
|---|---|---|---|---|---|
| Calculation engine | Weights fail to sum or covariance is invalid | Engine validates correlation symmetry/bounds and grid sums to 100% | Pass in prior Lab 14/15 runs | Accepted for mechanics | `../week-09-portfolio-baselines/portfolio.py` |
| All-history calculation | Output not reproducible | Cold command should print 59-return mix | 0/75/0/25 QQQ/SPY/NVDA/VOO; 13.11% return; 15.56% volatility | Accepted as historical calculation only | `analysis.py`; `visible_output.json` |
| Window stability | Choice depends on sample window | Latest-36 test should be compared with all history | 0/100/0/0; 22.15%; 12.25%; allocation changes | Reject for adoption | `visible_output.json` |
| Mandate fit | Output is called adoptable despite missing reserve sleeve/cost model | Require reserve, net-of-costs, loss, liquidity, concentration, turnover checks | Cannot pass with supplied universe | Rejected for adoption | `decision-memo.md` |
| Cold reproducibility | README is insufficient for a stranger | Partner follows README unaided | **Not yet performed; requires a named partner's independent note** | Open | `Lab_20_Project2_Readiness.md` |

## Locked Changed-Input Record — status: not yet complete

The prior Lab 15 record documents a historical window comparison and expected direction, but it does **not** contain a pre-run human-authored prediction with an immutable commit. It cannot truthfully be presented as this project's locked record.

| Required pre-run field | Current truthful status |
|---|---|
| Human-authored prediction before AI assistance and execution | Not recorded in this Project 2 folder |
| Old → new input with units | Candidate: all 59 monthly returns → latest 36 monthly returns |
| Expected direction/decision effect | Must be written by the student before rerunning; do not backdate |
| Immutable prediction commit | Not yet created |
| Before/after preserved result | Available in `visible_output.json` and Lab 15 |

To close this item, the student must write their own prediction before running, commit and push it, run the command without AI assistance, preserve the output, then write the actual result and reconciliation. The expected and actual results must remain distinguishable.

## Named AI-use register

| Tool/model surface | Interaction date | Material task | Independent check | Disposition | Effect on decision |
|---|---|---|---|---|---|
| Codex | 2026-11-17 | Organized existing course calculations into a reproducible Project 2 package | Python rerun of the existing calculation engine and comparison to Lab 15 figures | Qualified; student must verify every number and own the locked prediction | No change: missing mandate/stability evidence still requires rejection |
| AI used in earlier portfolio labs | See source lab records | Grid search, CSV estimator, documentation | Known-answer and input-direction tests recorded in Lab 14/15 | Qualified | No automatic adoption allowed |

## Limitations, monitoring, and escalation

No adoption until the reversal conditions in the decision memo are met. Re-run at a new data cutoff only after preserving the source file and documenting vendor revision risk. Escalate to the CIO if the result changes materially under the predeclared window/cost/estimate tests or if the mandate remains incomplete.

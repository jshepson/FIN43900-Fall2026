# Validation and AI Use

## Decision, version, and boundary

Decision/user: buy-side investment committee; watch/defer NVIDIA common stock. Valuation date: September 24, 2026. Currency: USD. The analysis uses final evidence available through the Q2 FY2027 Form 10-Q filed August 26, 2026 and the market reference recorded in the course work. Run `python assignments/project-1-nvidia/analysis.py` from the repository root.

## Validation register

| Claim/output | Failure mode | Test and expected direction | Actual result | Disposition |
|---|---|---|---|---|
| Enterprise-to-equity bridge | Claims omitted or signs reversed | Known-answer bridge: 1,000 + 100 - 250 - 20 - 10 = 820; 820 / 100 = 8.20 | PASS | Accepted |
| Historical base | Opening balance sheet does not reconcile | FY2026 assets must equal liabilities plus equity at 206,803 | PASS | Accepted |
| Forecast statements | Model hides an imbalance | Every forecast-year balance gap must be below 0.05m | PASS; maximum 0.0m | Accepted |
| Cash linkage | Cash is typed rather than calculated | Cash must remain above the 10,000m floor after cash-flow calculation | PASS; minimum headroom 117,283.8m | Accepted with model limitation |
| DCF monotonicity | DCF signs are wrong | 9% WACC must produce a higher value than 11%; 4% terminal growth must exceed 2% | PASS; 226.98 > 167.82 and 219.31 > 173.52 | Accepted |
| Bridge arithmetic | EV and equity result conflict | Equity must equal EV + 62,556 - 8,468 | PASS | Accepted |
| Highest-risk failure | Terminal assumption dominates the decision | Record terminal-value share of EV and qualify outcome | 77.0% in base case | Qualified: terminal sensitivity is material |
| Peer consistency | P/E is treated as EV or over-relied on | Price and annual GAAP diluted EPS must share currency/basis; one peer cannot be a range | PASS; AMD P/E is equity-value reference only | Qualified/rejected as decision value |
| AI output | AI decides peer selection | Compare AI suggestion to predeclared peer policy and primary business disclosures | AMD transferability concern accepted; no AI price is used | Qualified |

## Locked Changed-Input Record

The prediction below was supplied by the student before this rerun. Only WACC will change; the FCFF forecast, cash/securities, debt, terminal growth, and share basis stay fixed.

| Precommit timestamp | Commit/snapshot | Material input | Old -> new value/units | Student's expected output direction | Expected decision effect |
|---|---|---|---|---|---|
| 2026-10-16 13:11:02 EDT | pending prediction commit | Base WACC | 10.0% -> 11.0% | “I think it will increase.” | If value increases, the watch/defer conclusion would weaken; if it falls, it would strengthen. |

| Before/after output | Actual decision effect | Prediction reconciliation | Failure diagnosis/no-change reason | Evidence path |
|---|---|---|---|---|
| 193.14/share at 10.0% WACC -> 167.82/share at 11.0% WACC (-25.33/share), run 2026-10-16 13:16:44 EDT | Watch/defer strengthens because the higher required return lowers the base value farther below the 221.70 market reference. | Incorrect: the prediction expected an increase, but value decreased. | A higher WACC increases the discount rate applied to the same FCFF and terminal value, reducing their present values. | `analysis.py` / `visible_output.txt` |

## Material AI-use register

| Tool | Material task | Independent check | Disposition |
|---|---|---|---|
| Codex | Organized existing NVIDIA research, model structure, documentation, and scripts | Student must inspect code, rerun it, verify filing values, and own the changed-input prediction | Assistive draft; human retains decision and validation ownership |

## Limitations and monitoring

The conclusion depends most on the durability of Data Center demand, gross-margin execution, reinvestment/capex, and a terminal value that is 77.0% of base EV. Monitor reported Data Center growth, gross margin, operating cash-flow conversion, capacity commitments, customer concentration, China restrictions, and evidence on share count/bridge classifications. Revisit on the next filing or if these facts materially depart from the model path.

# NVIDIA (NVDA) — Lab 11 Pro-Forma Sensitivity

**Model date:** September 29, 2026. Dollar amounts are USD millions except per-share data. The cash-flow measure is **FCFE** (free cash flow to equity), consistent with the existing equity valuation.

## Question

Which assumptions drive NVIDIA's forecast and value, and what explains their effects?

## Locked changed-input record

**Locked before runs — September 29, 2026 (America/Indiana/Indianapolis).**

| Driver | Base input, FY2027E–FY2031E | Tested input | Units / years changed | Prediction before run | Range reason |
|---|---|---|---|---|---|
| Revenue-growth path | 70%, 40%, 25%, 15%, 8% | Lower: 65%, 35%, 20%, 10%, 3%; Higher: 75%, 45%, 30%, 20%, 13% | Percentage of prior-year revenue; each forecast year | A higher path should increase each year's revenue, gross profit, operating income, FCFE, and value. I expected it to have the largest span because it compounds through all five years and drives working-capital balances as well. | **Labelled judgment:** a uniform ±5 percentage-point band tests uncertainty around the pace at which the Data Center ramp fades. It is not a probability interval. |
| Gross-margin path | 74.0%, 74.0%, 73.5%, 73.0%, 72.5% | Lower: 73.0%, 73.0%, 72.5%, 72.0%, 71.5%; Higher: 75.0%, 75.0%, 74.5%, 74.0%, 73.5% | Percentage of revenue; each forecast year | A higher margin should increase gross profit, operating income, FCFE, and value, but I expected a smaller effect than revenue growth over these ranges. | **Labelled judgment:** a uniform ±1 percentage-point band is wider than the FY2027 Q3 guidance's ±50 bp quarterly band, so it tests forecast/mix and component-cost uncertainty over a five-year path. It is not a probability interval. |

Only the named independent driver changes in a scenario. The other independent assumption resets to its base value before every run; all income-statement, balance-sheet, cash-flow, and valuation quantities then recalculate.

## Results

### Revenue-growth path sensitivity

| Case | Actual FY2027E–FY2031E input path | FY2031E operating income | FY2031E FCFE | Value per share | Change from base: operating income / FCFE / value per share | Accounting check |
|---|---|---:|---:|---:|---:|---|
| Lower | 65%, 35%, 20%, 10%, 3% | $403,256.1 | $322,369.5 | $160.38 | $(90,778.4) / $(68,527.2) / $(30.43) | Pass; maximum balance gap $0.0m |
| Base | 70%, 40%, 25%, 15%, 8% | $494,034.5 | $390,896.7 | $190.81 | $0.0 / $0.0 / $0.00 | Pass; maximum balance gap $0.0m |
| Higher | 75%, 45%, 30%, 20%, 13% | $600,029.8 | $470,153.4 | $225.76 | $105,995.4 / $79,256.8 / $34.96 | Pass; maximum balance gap $0.0m |
| **Span (maximum − minimum)** |  | **$196,773.8** | **$147,783.9** | **$65.38** |  |  |

Trace of the higher case: the FY2031E growth input is 13.0%, producing FY2031E revenue of $965,913.3m. The linked statements then produce operating income of $600,029.8m and FCFE of $470,153.4m; the balance-sheet gap is $0.0m.

### Gross-margin path sensitivity

| Case | Actual FY2027E–FY2031E input path | FY2031E operating income | FY2031E FCFE | Value per share | Change from base: operating income / FCFE / value per share | Accounting check |
|---|---|---:|---:|---:|---:|---|
| Lower | 73.0%, 73.0%, 72.5%, 72.0%, 71.5% | $486,311.0 | $384,453.3 | $187.60 | $(7,723.5) / $(6,443.4) / $(3.21) | Pass; maximum balance gap $0.0m |
| Base | 74.0%, 74.0%, 73.5%, 73.0%, 72.5% | $494,034.5 | $390,896.7 | $190.81 | $0.0 / $0.0 / $0.00 | Pass; maximum balance gap $0.0m |
| Higher | 75.0%, 75.0%, 74.5%, 74.0%, 73.5% | $501,757.9 | $397,340.0 | $194.01 | $7,723.5 / $6,443.4 / $3.21 | Pass; maximum balance gap $0.0m |
| **Span (maximum − minimum)** |  | **$15,447.0** | **$12,886.7** | **$6.41** |  |  |

## Checks and reconciliation

The base model was run before analysis and again after analysis. Both runs produce FY2031E operating income of **$494,034.5m**, FCFE of **$390,896.7m**, and value per share of **$190.81**. The restored-base check passes within $0.005m / $0.005 per share. Every usable sensitivity run has a maximum absolute balance-sheet gap of $0.0m and cash remains at or above the model's minimum.

The locked revenue-growth prediction was directionally correct. The higher path raises value per share by $34.96 and the lower path reduces it by $30.43. The slight asymmetry is expected: revenue growth compounds on the prior year's revenue, so the path is not a linear dollar change.

## Main driver and interpretation

**Over these ranges, the revenue-growth path is the larger driver** for FY2031E operating income ($196,773.8m span versus $15,447.0m), FCFE ($147,783.9m versus $12,886.7m), and value per share ($65.38 versus $6.41). Higher growth increases revenue and gross profit in each forecast year; it also raises receivables, inventory, prepaids, accounts payable, and accrued liabilities through the linked working-capital formulas. The operating-profit effect is still much larger than the incremental working-capital cash use, so FCFE and equity value rise.

This ranking does **not** establish that growth is inherently more important than margin. The revenue-growth path was tested over a ±5 percentage-point range in every year, whereas gross margin was tested over ±1 percentage point. A wider or differently supported margin range could change the ranking. The result does not change my valuation conclusion from the Lab 10 base case: the $190.81 base value remains below the September 24, 2026 market reference of $221.70, while the higher growth case reaches $225.76. My research priority is therefore evidence on the durability and fade rate of the Data Center ramp, including demand, supply capacity, customer concentration, product transitions, and China restrictions.

## Sensitivity reflection

One-at-a-time sensitivity changes one independent assumption while holding the other independent assumptions at their base values, then lets all linked calculations recalculate. It isolates the model response to that specified change; it is not a claim that real-world drivers move independently.

The selected input range directly affects the ranking because an output span is calculated as the maximum result minus the minimum result over the tested values. A larger range can create a larger span even when the underlying economics are not more important.

A sensitivity table is not a forecast probability because it does not assign probabilities to the cases, estimate their likelihood from data, or represent correlations among drivers. It shows conditional outcomes: *if* this input takes a particular value while the rest stay at base, the model produces this result.

The result that surprised me was the scale of the growth-path difference relative to the margin-path difference. The model's five-year compounding means that a 5-percentage-point change in every annual growth assumption produces a much larger FY2031 revenue base, so the impact is much larger than a 1-percentage-point margin change over the stated ranges.

## Partner exchange notes — complete with your actual exchange before submission

I did not fabricate a partner interaction. Fill in the brackets after the required live exchange.

| Exchange | Your note |
|---|---|
| Partner's question about my predicted input → statement → output link; my response | [Partner name and actual question/response] |
| Unit / one-change-at-a-time check my partner performed on my model | [Actual check and any correction] |
| Changed result and base difference my partner recomputed | [Actual values checked] |
| Check I performed on my partner's analysis | [Their driver, base/changed output, calculation, and finding] |
| Partner's question about whether the ranking reflects the chosen ranges; my response | [Actual question/response] |

## Run instructions

```bash
python3 assignments/week-05-pro-forma/nvidia_sensitivity.py
```

The script imports the existing root-level Lab 10 model, makes a fresh deep copy of the base inputs for every lower/base/higher run, prints the visible sensitivity output and checks, and reruns the restored base at the end.

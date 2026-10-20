# Lab 14 — Portfolio Baselines

## Decision and inputs

The decision user is the Meridian Foundation CIO. The action is to compare simple baseline portfolios for the $100 million reserve over Meridian's seven-year horizon with annual rebalancing. The comparison benchmark is S4: 40% investment-grade bond fund and 60% global equity index fund. The classroom universe is Treasury bills, Treasury 10-year notes, an investment-grade bond fund, and a global equity index fund.

The provisional classroom objective is CPI + 4%, using a labelled 2.5% CPI estimate, or **6.5% expected return**. This is a mechanics exercise, not an adoptable optimized recommendation: the five-year, net-of-costs mandate objective and the S9 calendar-year loss rule still require CIO clarification. Long-only, no derivatives, the 3.0% reserve minimum, at least 90% redeemable within five business days, the 8% single-company limit, and turnover approval above 25% remain hard constraints from Lab 13.

All inputs are annual course-authored training values, not market estimates. Returns and volatilities are decimals in `portfolio.py`; the displayed results are annual percentages. No sample or as-of date applies to these supplied classroom inputs. The engine does not impute missing values: a missing sleeve or correlation table label raises an error during validation.

## Baseline results

Run from this folder:

```sh
python portfolio.py
```

| Portfolio | Weights: bills / 10-year / IG / equity | Expected return | Volatility | Reserve-eligible | Meets 6.5%? |
|---|---:|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | no |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | no |

All three calculated weights sum to 100.0%. The code builds covariance entries as `correlation × volatility × volatility`, validates that each correlation is within -1 to 1, and rejects a non-symmetric table before calculating portfolios.

## Known-answer reconciliation and validation

For the benchmark, only IG and equity have nonzero weights. Its annual variance is:

`(0.40² × 0.06²) + (0.60² × 0.16²) + (2 × 0.40 × 0.60 × 0.25 × 0.06 × 0.16)`

`= 0.000576 + 0.009216 + 0.001152 = 0.010944`

Taking the square root yields `0.1046`, or **10.46%**, matching the engine and known answer. The cross term includes the 0.25 correlation; leaving it out produces the incorrect 9.90% result.

Changing the IG–equity correlation from 0.25 to 0.50 in both symmetric cells raises the benchmark volatility to **11.00%**. Restoring both cells to 0.25 returns it to 10.46%. Setting either correlation cell to 1.3 makes the program stop with a clear invalid-correlation error.

## Candidate and mandate report

Candidate E was added to Lab 13's `mandate.py` as Meridian's 40% IG / 60% equity benchmark. It has 0.0% reserve-eligible weight and fails the 3.0% reserve rule, even though it meets the provisional 6.5% expected-return classroom objective. It is therefore a benchmark and mechanics probe, not an adoptable mandate-compliant candidate.

The equal-weight and inverse-volatility portfolios are mechanics-only baselines. Equal weight has 50.0% reserve eligibility but misses the classroom objective. Inverse volatility gives the most weight to bills because 1 / 0.5% is much larger than 1 divided by the other volatilities; it has 90.3% reserve eligibility but also misses the objective.

## AI disclosure and reflection

AI was used to draft the reusable standard-library calculation structure. I accepted the suggestion to calculate covariance from the editable inputs and to validate both bounds and symmetry. I qualified any suggestion that a baseline meeting 6.5% is automatically adoptable: the unresolved loss rule and Lab 13 hard constraints still govern adoption.

I can now calculate a portfolio's return and risk from weights, volatilities, and correlations and test an input error instead of trusting a displayed number. I still need the CIO to define the calendar-year loss measurement and breach response before an optimized portfolio can be adopted.

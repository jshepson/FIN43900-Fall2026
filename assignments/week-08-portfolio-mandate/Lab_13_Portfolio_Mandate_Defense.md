# Lab 13 — Portfolio Mandate Defense

## Meridian Foundation Reserve

The user is the Meridian Foundation CIO. The action is to approve a $100 million reserve portfolio before any optimization. The horizon is seven years, with annual rebalancing. The permitted holdings are the eight holdings supplied in the case. The decision is made before building or optimizing the portfolio.

## Statement types: S1–S10

| Statement | Type | Reason |
|---|---|---|
| S1 | Hard constraint | A seven-year horizon and annual rebalancing set the mandate's timing. |
| S2 | Objective | CPI + 4% net of costs over rolling five-year periods states the desired investment result. |
| S3 | Hard constraint | It requires four quarterly payouts to be held in cash or daily-liquid government securities. |
| S4 | Preference | The 60/40 mix is a comparison benchmark, not a required holding mix. |
| S5 | Hard constraint | It expressly prohibits borrowing, short sales, and derivatives. |
| S6 | Hard constraint | It limits any one company, across all of its securities, to 8%. |
| S7 | Hard constraint | Turnover over 25% requires committee approval. |
| S8 | Hard constraint | At least 90% must be redeemable within five business days. |
| S9 | Unverifiable promise | The loss statement supplies neither a measurement method nor a breach rule, so it cannot be tested. |
| S10 | Missing | The CIO has not chosen the pilot's optimization target; no sector, ESG, tax, or home-bias preference is supplied. |

## Investment policy statement (IPS)

An IPS is the written agreement that translates a client's investment goals, limits, and decision process into a mandate that can be implemented and monitored. Its objective says what success means; its constraints say what an implementation may not violate.

| IPS element | Meridian statement(s) | Application |
|---|---|---|
| Client, purpose, horizon, and rebalancing | S1 | Meridian's $100 million reserve has a seven-year horizon and annual rebalancing. |
| Return objective | S2 | Seek CPI + 4% per year, net of costs, over rolling five-year periods. |
| Liquidity and spending | S3, S8 | Cover four $0.75 million quarterly payments and keep at least 90% redeemable within five business days. |
| Benchmark | S4 | Compare results with 60% global equities and 40% U.S. investment-grade bonds. |
| Investment restrictions | S5, S6, S7 | Long-only; no derivatives; company exposure no more than 8%; turnover no more than 25% without approval. |
| Risk tolerance | S9 | Calendar-year loss limit is intended, but is not operational until the CIO defines its measure and breach response. |
| Preferences and unresolved design choice | S10 | No sector, ESG, tax, or home-bias preference exists; the optimization target is still missing. |

## Checkable mandate and results

The checker is [mandate.py](mandate.py). Run it with:

```sh
python mandate.py
```

It calculates the reserve minimum rather than typing it in: 4 × $0.75m ÷ $100m = **3.0%**. It checks weight total, long-only status, reserve-eligible assets, five-business-day liquidity, and aggregated single-company exposure. Cash, U.S. Treasury securities, and diversified funds are exempt from the issuer limit. The calendar-year loss statement is deliberately printed as requiring CIO clarification and is never tested.

| Rule | A | B | C |
|---|---:|---:|---:|
| Weights sum to 100 | 100.0 pass | 100.0 pass | 100.0 pass |
| Long-only (lowest weight) | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve at least 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL |
| Redeemable in 5 days at least 90% | 100.0 pass | 85.0 FAIL | 100.0 pass |
| Largest single company at most 8% | 0.0 pass | 9.0 FAIL | 8.0 pass |
| Calendar-year loss | requires CIO clarification | requires CIO clarification | requires CIO clarification |
| Verdict | passes every checkable rule | fails 3 rule(s) | fails 1 rule(s) |

Acme is correctly aggregated: candidate B has 5% Acme bonds plus 4% Acme stock, or 9% in one company.

### Lab 14 benchmark check: candidate E

I added Meridian's S4 benchmark as candidate E: 40% Investment-grade bond fund and 60% Global equity index fund. Running `python mandate.py` reports a **0.0% reserve-eligible weight**, which fails the 3.0% reserve rule. The client's comparison benchmark therefore is not an adoptable mandate-compliant portfolio without a reserve allocation.

### Required probe

I temporarily changed candidate A's Cash weight to -2% and its Global equity index fund weight to 64%, then reran the program. The lowest weight was -2.0 and failed long-only; every other rule passed, including the 10.0% reserve-eligible amount. I then restored the original 2% Cash and 60% Global equity index fund inputs.

### Line check

The line I checked was `issuer_weights[issuer] = issuer_weights.get(issuer, 0) + weight`. My answer: it adds every security issued by the same non-exempt company before comparing that company total with the 8% limit. This is why Acme bonds and Acme stock become 9% in candidate B instead of being tested separately.

## Attack portfolio: candidate D

Candidate D holds 100% Cash and 0% in every other holding. It runs and passes every checkable rule: its weight total is 100.0%, its reserve-eligible and liquid weights are each 100.0%, and it has no non-exempt company exposure.

The objection holds because a 100% cash portfolio can comply with the mechanical limits while reasonably failing to pursue CPI + 4% net of costs over rolling five-year periods. S2 decides the objection, but the CIO must specify how the pilot should trade off that return objective with risk and benchmark performance. As a sceptical colleague reviewing this candidate, I would cite S2.

## Question for the CIO before optimization

**Question:** Should the pilot primarily maximize the probability of meeting the five-year CPI + 4% net-of-costs objective, minimize downside/shortfall risk, or minimize deviation from the 60/40 benchmark, after all hard constraints are met?

If the CIO chooses the return objective, the portfolio should generally accept more growth-asset exposure; if the CIO chooses downside or benchmark control, it should hold more liquid high-quality bonds/cash or stay nearer the 60/40 benchmark. That answer changes the portfolio design, so optimization must wait.

## Reflection

A portfolio can pass every checkable rule and still be wrong because compliance does not prove that it is likely to meet the return objective, fits the intended risk tolerance, or reflects the CIO's unresolved optimization choice. Candidate D demonstrates this gap: it passes the code but may be unsuitable under S2.

The type I was least sure of was S4. I classified it as a preference because it supplies a reference portfolio for evaluation rather than requiring Meridian to hold a 60/40 allocation; the CIO can clarify if it is meant to be a tracking constraint instead.

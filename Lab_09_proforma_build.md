# Lab 09 — Pro-Forma Build: The Engine and the Known Answer

## The question

What are five years of a company's statements worth, built from assumptions I can defend, and how do I know the statements are right?

This lab builds a five-year three-statement model for Asbury Automotive Group (ABG), from FY2025 actual opening balances through FY2030E. All dollar amounts are USD millions unless noted otherwise.

## Opening FY2025 balance sheet and operating base

| Line | Amount |
|---|---:|
| Revenue | 17,999.0 |
| Inventory | 2,135.8 |
| PP&E | 3,070.4 |
| Other assets | 6,371.6 |
| Cash | 40.4 |
| Floor plan | 2,027.0 |
| Term debt | 3,572.0 |
| Other liabilities | 2,127.5 |
| Equity | 3,891.7 |

The opening balance sheet balances: assets of 11,618.2 equal liabilities plus equity of 11,618.2.

## Assumption set

| Assumption | ABG value | Basis |
|---|---:|---|
| Organic revenue growth | 1.8% per year | Judgment |
| Gross margin | 17.05% | Judgment |
| SG&A ÷ gross profit, 2026–2030 | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% | Judgment |
| Depreciation ÷ opening PP&E | 82.4 ÷ 3,070.4 | FY2025 history |
| Impairment | 120.0 per year | Judgment; non-cash |
| Capital spending | 250.0 per year | Guidance |
| Tax rate | 25.5% | Judgment |
| Inventory days | 2,135.8 ÷ (17,999.0 − 3,071.7) × 365 | FY2025 history |
| Floor plan ÷ inventory | 2,027.0 ÷ 2,135.8 | FY2025 history |
| Other working capital | 0.8% of change in revenue | Judgment |
| Minimum cash / revolver limit / rate | 25.0 / 850.0 / 6.0% | History / judgment |
| Annual debt repayment / share buyback | 150.0 / 150.0 | Judgment |
| Interest: floor plan / term debt | 4.67% / 5.44% | History |
| Cost of equity / terminal growth | 10.0% / 2.5% | Judgment |
| Shares outstanding | 17.951349 million | 10-Q at 30 June 2026 |

## The three judgments that carry the ABG value

1. **Revenue growth (1.8%)** sets the size of the business. It drives gross profit, inventory, and therefore the amount of floor-plan financing needed.
2. **Operating margins** — the 17.05% gross margin and the declining SG&A-to-gross-profit ratio — drive operating income. The forecast assumes operating efficiency improves through 2028 and then holds steady.
3. **Cash allocation and valuation** — capex, debt repayment, buybacks, the 10% cost of equity, and 2.5% terminal growth — determine cash available to shareholders and what that cash is worth today. Terminal value is important here because it represents about 80% of equity value.

## Calculation order

For each forecast year, the engine uses beginning-of-year balances where the instruction requires them.

1. Revenue = prior-year revenue × (1 + growth).
2. Gross profit = revenue × gross margin; SG&A = gross profit × that year's SG&A ratio.
3. Depreciation = opening PP&E × historical depreciation ratio; impairment is 120.0.
4. Operating income = gross profit − SG&A − depreciation − impairment.
5. Interest = opening floor plan × 4.67% + opening term debt × 5.44% + opening revolver × 6.0%.
6. Tax = the greater of zero and pretax income, multiplied by 25.5%; net income follows.
7. The balance sheet excluding cash is projected: inventory from days, floor plan from inventory, PP&E from capex less depreciation, other assets from revenue change less impairment, debt from repayment, other liabilities flat, and equity from net income less buybacks.
8. FCFE = net income + depreciation + impairment − capex − change in inventory − change in other working capital + change in floor plan − debt repayment.
9. Cash is last: ending cash = opening cash + FCFE − buyback. The model draws on the revolver only when cash would be below 25.0 and repays existing revolver debt first when cash is above 25.0.

Cash must be the final calculated balance-sheet line because it is the residual result of operations, investment, working capital, financing, and distributions. Entering cash before those drivers would conceal an imbalance rather than expose it.

## Known-answer validation

The required checkpoints are reproduced to one decimal.

| Line | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| Free cash flow to equity | 211.4 | 342.3 |
| Cash, year end | 101.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 |

The valuation output is:

| Metric | Result |
|---|---:|
| Equity value | $5,237.34 million |
| Share of value after 2030 | 79.8% |
| Value per share | **$291.75** |

Equity value is the present value of the five annual FCFE amounts plus the present value of terminal value. Terminal value is calculated as `(2030 FCFE + 2030 debt repayment) × (1 + terminal growth) ÷ (cost of equity − terminal growth)`, then discounted five years.

## Proof that the model refuses a broken balance sheet

`assert_balanced` runs after every forecast year and raises an `AssertionError` if either the balance-sheet gap exceeds $0.05 million or cash is below the required minimum.

For the required break test, I temporarily replaced the calculated FY2026 cash balance with the opening $40.4 million. The program stopped immediately with:

```text
AssertionError: FY2026E does not balance: gap -61.4
```

The negative $61.4 million is the missing FY2026 increase in cash, with the sign flipped because the check is `assets − liabilities − equity`. This demonstrates that the check is meaningful: the model does not silently accept a manually overwritten cash line. The calculated-cash line was restored after the test.

## Floor-plan financing

Floor-plan financing is short-term inventory lending, typically supplied by vehicle manufacturers' finance arms and banks. It rises as inventory rises. The model charges interest on the opening floor-plan balance and includes the change in floor-plan debt in FCFE because it funds the operating inventory cycle. If the floor-plan line is removed, the company loses this operating funding source; cash must finance inventory instead, which is why the video shows cash falling to roughly negative $1.1 billion.

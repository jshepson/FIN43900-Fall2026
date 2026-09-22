# Lab 09 — Pro-Forma Build: ABG

## Question

What are five years of a company's statements worth, built from assumptions I can defend, and how do I know the statements are right?

## Three value-carrying judgments

1. Organic revenue growth of 1.8% determines the size of the business and its inventory financing need.
2. Gross margin of 17.05% and the declining SG&A-to-gross-profit ratio determine operating income.
3. Capital allocation and valuation assumptions — $250m annual capex, $150m debt repayment and buybacks, a 10% cost of equity, and 2.5% terminal growth — determine the cash distributed to equity and its present value.

Cash is calculated last because it is the residual outcome of operating performance, investment, working capital, financing, and distributions. Setting cash first would hide an imbalance instead of revealing it.

## Floor plan

Floor-plan financing is short-term inventory lending from manufacturers' finance arms and banks. It rises with inventory, its interest is calculated on the opening balance, and its change belongs inside FCFE because it finances the operating inventory cycle. Removing it removes a major operating funding source, so cash falls sharply (about negative $1.1bn in the video).

## Validation performed

`python3 proforma.py` reproduces the assigned FY2026E and FY2030E outputs and $291.75 per share. The program calls `assert_balanced` after every year and raises an error if the balance sheet has a material gap or cash is below the minimum.

For the required break test, temporarily replace the FY2026 computed cash with `40.4`. The balance check then raises `FY2026E does not balance: gap -61.4`. That gap is the omitted $61.4 increase in cash, shown with the sign flipped because the check is assets minus liabilities minus equity.

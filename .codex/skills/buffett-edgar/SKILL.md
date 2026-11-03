---
name: buffett-edgar
description: Analyze a public company using Warren Buffett-style operating checks computed solely from SEC EDGAR 10-K company facts. Use when asked for this repeatable, no-price business-quality review.
---

# Buffett EDGAR review

Use `scripts/analyze_company.py` for every numeric claim. It obtains a ticker's CIK
from SEC EDGAR and company facts from the SEC API; do not substitute market-data or
paid-data sources.

Run it with a truthful SEC-compliant User-Agent that identifies the user and their
contact email:

```sh
python scripts/analyze_company.py COST --user-agent "Full Name email@example.edu"
```

The script uses only annual 10-K facts, chooses the latest filing when an annual
period appears in multiple filings, and prints the latest five fiscal years. It
prints `not found` rather than estimating missing facts. Do not change tag priority,
period selection, or Buffett checks to improve a result.

For a memo, use only the displayed figures and checks. Make a short, price-free
business judgment: `own the business`, `watch it`, or `pass`. State uncertainty when
the script reports missing inputs or `not known`; do not infer a number. Save the
memo as Markdown next to the run artifacts. Before relying on a memo in the app,
use the app's memo-number audit and correct any flagged number.

The fixed checks are:

1. ROE is at least 15% in every reported year.
2. Owner earnings are positive in every reported year.
3. Owner earnings increased from the first reported year to the last.

`not known` is the result for a check with a missing input; it is not a pass or a
failure. This is an educational review of business operations, not investment advice.

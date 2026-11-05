---
name: burry-edgar
description: Screen a public company with Michael Burry-style cash-flow and leverage checks computed from the shared SEC EDGAR 10-K fact panel. Use for the Lab 19 investor panel, not price or short-sale analysis.
---

# Burry EDGAR review

Use the shared `buffett-edgar` analyzer to retrieve the five-year SEC EDGAR 10-K
fact panel. Apply only the deterministic checks in `scripts/burry_checks.py`:

1. Operating cash flow is at least net income every year.
2. Latest-year liabilities are no more than twice equity.

If an input is missing, or equity is zero or below, return `not known` rather
than estimating. Write a short price-free memo using only printed panel values
and state `own the business`, `watch it`, or `pass`.

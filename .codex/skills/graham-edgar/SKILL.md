---
name: graham-edgar
description: Screen a public company with Benjamin Graham-style financial-strength checks computed from the shared SEC EDGAR 10-K fact panel. Use for the Lab 19 investor panel, not price or intrinsic-value analysis.
---

# Graham EDGAR review

Use the shared `buffett-edgar` analyzer to retrieve the five-year SEC EDGAR 10-K
fact panel. Apply only the deterministic checks in `scripts/graham_checks.py`:

1. Latest-year current ratio is at least 2.0.
2. Net income is positive every year.
3. Net income grew from the first reported year to the last.

Keep the 2.0 current-ratio threshold after the required 1.0 probe; label a
missing input or zero denominator `not known`, never estimated. Write a short
price-free memo using only the printed panel values and state `own the business`,
`watch it`, or `pass`.

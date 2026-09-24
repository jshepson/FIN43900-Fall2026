# NVIDIA (NVDA) — Lab 10 Pro-Forma

**Model date:** September 24, 2026. All dollar amounts are USD millions except per-share values.

## The question

What are five years of NVIDIA's statements worth, built from assumptions I can defend?

## NVIDIA's company-specific line

NVIDIA is different because the speed and profitability of its Data Center ramp depend on AI-system demand and supply capacity, rather than on a store base or same-store sales. The model therefore uses a front-loaded revenue-growth path that fades as the current Blackwell/data-center ramp matures, and it retains elevated capital spending to support that ramp.

## Three-year history — GAAP

Each history value below is from the linked Form 10-K financial statements, not a data provider. Before submitting, independently open the FY2026 10-K and confirm at least two items (for example, revenue and inventory).

| Item | FY2024 | FY2025 | FY2026 | Filing source |
|---|---:|---:|---:|---|
| Revenue | 60,922 | 130,497 | 215,938 | [FY2026 10-K, Consolidated Statements of Income](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) (comparative table) |
| Gross profit | 44,301 | 97,858 | 153,463 | [FY2026 10-K, Consolidated Statements of Income](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) |
| SG&A | 2,654 | 3,491 | 4,579 | [FY2026 10-K, Consolidated Statements of Income](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) |
| Net income | 29,760 | 72,880 | 120,067 | [FY2026 10-K, Consolidated Statements of Income](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) |
| Inventory | 5,282 | 10,080 | 21,403 | [FY2025 10-K, Consolidated Balance Sheets](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm); [FY2026 10-K, Consolidated Balance Sheets](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) |
| PP&E, net | 3,914 | 6,283 | 10,383 | [FY2025 10-K, Consolidated Balance Sheets](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm); [FY2026 10-K, Consolidated Balance Sheets](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) |
| Shareholders' equity | 42,978 | 79,327 | 157,293 | [FY2025 10-K, Consolidated Balance Sheets](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm); [FY2026 10-K, Consolidated Balance Sheets](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) |

## FY2026 opening balance sheet used in the model

| Item | January 25, 2026 |
|---|---:|
| Cash and cash equivalents | 10,605 |
| Marketable securities | 51,951 |
| Accounts receivable, net | 38,466 |
| Inventory | 21,403 |
| Prepaids and other current assets | 3,180 |
| PP&E, net | 10,383 |
| Other non-cash assets | 70,815 |
| **Total assets** | **206,803** |
| Accounts payable | 9,812 |
| Accrued and other current liabilities | 21,352 |
| Debt, short- and long-term | 8,468 |
| Other liabilities | 9,878 |
| **Shareholders' equity** | **157,293** |
| **Total liabilities and equity** | **206,803** |

Source: [NVIDIA FY2026 10-K, Consolidated Balance Sheets](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm). “Other non-cash assets” groups operating-lease assets, goodwill, intangibles, deferred-tax assets, non-marketable equity securities, and other assets. “Other liabilities” groups long-term operating-lease and other long-term liabilities.

## Historical ratios and operating evidence

| Measure | FY2024 | FY2025 | FY2026 | Calculation / source |
|---|---:|---:|---:|---|
| Revenue growth | 126.5% | 114.2% | 65.5% | Year-over-year revenue growth from history above |
| Gross margin | 72.7% | 75.0% | 71.1% | Gross profit ÷ revenue |
| SG&A ÷ gross profit | 6.0% | 3.6% | 3.0% | SG&A ÷ gross profit |
| Inventory days | 116.0 | 112.7 | 125.0 | Inventory ÷ cost of revenue × 365 |
| D&A ÷ year-end PP&E | 38.5% | 29.7% | 27.4% | D&A of 1,508 / 1,864 / 2,843 from [FY2026 10-K cash-flow statement](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm), divided by year-end PP&E; proxy because D&A includes amortization |
| Capital spending, filing | 1,069 | 3,236 | 6,042 | “Purchases related to property and equipment and intangible assets” in [FY2026 10-K cash-flow statement](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) |
| Capital spending, provider field | unresolved | unresolved | unresolved | No data-provider field was used; the filing figure is the model input source. |
| Tax rate | 12.0% | 13.3% | 15.1% | Income tax expense ÷ income before income tax from the [FY2026 10-K income statement](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) |
| Organic / same-store / comparable growth | none disclosed | none disclosed | none disclosed | NVIDIA does not operate a comparable-store model. The filing reports total revenue growth; Data Center revenue grew 68% in FY2026. |

Organic growth means growth excluding acquisitions, divestitures, foreign-exchange effects, or other defined non-core changes. NVIDIA does not disclose same-store, comparable, or a directly labelled organic-growth metric because it is a platform and semiconductor company, not a store network. ABG's 1.8% was a conservative forecast assumption, while its 4.7% reported growth describes a past period; a forecast should not mechanically repeat reported growth.

## Assumption set

| Assumption | Value | Label | Reason |
|---|---:|---|---|
| Revenue growth: FY2027–FY2031 | 70%, 40%, 25%, 15%, 8% | Guidance + judgment | Management's August 2026 call indicated about 70% FY2028 growth; I use that high-growth evidence initially, then fade it as the revenue base grows and AI deployment/supply constraints matter more. |
| Gross margin: FY2027–FY2031 | 74.0%, 74.0%, 73.5%, 73.0%, 72.5% | Guidance + judgment | Q3 FY2027 GAAP gross-margin guidance was 74.0% ± 50 bp. I hold it initially, then allow modest mix and component-cost pressure rather than assuming the FY2025 peak repeats. |
| R&D ÷ revenue | 7.5% declining to 7.1% | Judgment | NVIDIA must keep funding platform and system development, but revenue can scale faster than R&D if the current platform ramps successfully. |
| SG&A ÷ gross profit | 3.0% to 3.2% | History + judgment | FY2026 was 3.0%. I retain approximately that efficient level and add a small increase later rather than assume permanent operating leverage. |
| Inventory days | 125 days | History | FY2026 inventory days were 125, reflecting complex systems and supply commitments; holding the latest year is conservative versus FY2024–FY2025. |
| Receivable / payable days | 65 / 57 days | History | Derived from FY2026 receivables and accounts payable relative to revenue/cost of revenue. |
| D&A ÷ opening PP&E | 27.4% | History | FY2026 D&A divided by FY2026 year-end PP&E; this is an explicit proxy because reported D&A includes amortization. |
| Capital spending | 9,000; 11,000; 12,000; 13,000; 14,000 | Judgment | Filed FY2026 capex was 6,042 and PP&E rose sharply. I assume continued investment to serve the Data Center ramp, without making capex grow as fast as revenue indefinitely. |
| Tax rate | 18.0% | Judgment | FY2024–FY2026 effective rates were 12.0%–15.1%; 18% allows for fewer favorable discrete tax items as earnings normalize. |
| Shareholder returns | 25% of net income | Judgment | FY2026 repurchases plus dividends were material. This retains most earnings for liquidity while continuing a visible capital-return policy. |
| Minimum cash | 10,000 | Judgment | This is near FY2026 cash and cash equivalents and avoids treating the $52.0bn marketable-securities portfolio as operating cash. |
| Revolver | $10,000 limit at 6% | Judgment | A conservative liquidity backstop; it is unused in the base run. |
| Cost of equity / terminal growth | 10.0% / 3.0% | Judgment | Consistent with the prior course DCF and a long-run nominal-growth assumption; terminal growth is not NVIDIA-specific hypergrowth. |
| **Company-specific driver: Data Center ramp** | Front-loaded growth and elevated capex | Guidance + judgment | Data Center revenue was NVIDIA's dominant engine and grew 68% in FY2026. The model explicitly fades growth and sustains investment because customer deployments, supply capacity, product transitions, China restrictions, and concentration can change this trajectory. |

## Model and checks

Run:

```bash
python nvidia_proforma.py
```

The model calculates cash from net income, D&A, capex, working-capital changes, and shareholder returns; it does not type cash. Its assertion function stops the run if a balance-sheet gap exceeds $0.05m or cash falls below the $10.0bn floor. The base run balances at zero in every forecast year and does not draw the revolver.

The model's value per share is **$190.81**, calculated using the same 24,304m shares outstanding reported in the FY2026 10-K. The check block prints **$0.0m** in FY2027E–FY2031E and cash remains above the $10.0bn floor; the base case does not draw the revolver.

The market price was **$221.70 per NVDA share on September 24, 2026** (during-market historical record; use the prior close if submitting before the close). The model says **$190.81** per share; the market says **$221.70** per share on September 24, 2026, with the model using the same 24,304m-share count. The question is whether the assumed Data Center growth fade and elevated reinvestment are too conservative or too optimistic.

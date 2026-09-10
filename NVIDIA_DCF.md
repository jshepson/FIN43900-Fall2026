# NVIDIA (NVDA) DCF — Lab 06

**Model date:** September 10, 2026. Dollar amounts are USD millions except per-share figures. This is a course exercise, not investment advice.

## Inputs and sources

| Input | Value used | Unit | As-of date | Source and locator |
|---|---:|---|---|---|
| Starting FCFF | 96,895.847 | $ millions | FY ended Jan. 25, 2026 | **Calculated:** cash from operations 102,718 + after-tax interest 219.847 − capex 6,042. NVIDIA FY2026 [Form 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm), Item 8, “Consolidated Statements of Cash Flows” / “Net cash provided by operating activities” and “Purchases related to property and equipment and intangible assets”; Item 7 / “Interest expense.” |
| Growth, years 1–5 | 70%, 40%, 25%, 15%, 8% | annual | Forecast made Sep. 10, 2026 | **Forecast, not a filing fact.** Item 7 reports FY2026 revenue growth of 65% after FY2025’s 114%; management’s Q2 FY2027 call gave a preliminary FY2028 revenue-growth expectation of about 70%. The path begins with that high-growth evidence and deliberately fades. [FY2026 10-K, Item 7](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm); [Q2 FY2027 call](https://investor.nvidia.com/files/content_files/TRANSCRIPT_-NVIDIA-Corp-NVDA-US-Q2-2027-Earnings-Call-26-August-2026-5_00-PM-ET.pdf). |
| WACC | 10.0% | annual | Sep. 10, 2026 | **Estimate:** cost of equity = 4.5% + 1.3 × 5.0% = 11.0%; after-tax debt cost = 6.0% × (1 − 25%) = 4.5%; 85% equity / 15% debt gives 10.0% (rounded). |
| Terminal growth | 3.0% | annual perpetual | Sep. 10, 2026 | Assumption representing long-run nominal economic growth, not NVIDIA-specific growth. |
| Cash and marketable securities | 62,556 | $ millions | Jan. 25, 2026 | [FY2026 10-K, Item 7 / Liquidity](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm), “Cash, cash equivalents, and marketable securities.” |
| Debt | 8,468 | $ millions | Jan. 25, 2026 | [FY2026 10-K, Item 7 / Debt](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm), “Net carrying amount”; 999 short-term plus 7,469 long-term. |
| Diluted shares | 24,514 | millions of shares | FY ended Jan. 25, 2026 | [FY2026 10-K, Item 8 / Consolidated Statements of Income](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm), “Weighted average shares used in per share computation — Diluted.” |
| Market price (reverse-DCF target) | 223.67 | $/share | Sep. 9, 2026 close; checked Sep. 10 before market close | [MarketMinute historical prices](https://www.marketminute.com/quote/NQ%3ANVDA/historical), Sep. 9 closing price. |

The FCFF tax rate is FY2026 tax expense ÷ pre-tax income: 21,383 ÷ 141,450 = **15.1170%**. Thus after-tax interest is 259 × (1 − 15.1170%) = 219.847.

## Reasonableness

`python dcf.py` produces a base-case value per diluted share of **$176.67** versus a $223.67 target price: **0.79×**, inside the lab’s 0.5×–2× band. I did not alter an input to force that comparison.

The input I distrust most is the five-year FCFF-growth path, particularly years 1–2. It is an analyst forecast inferred from extraordinary revenue growth and management commentary; FCFF can diverge from revenue as working capital, margins, and reinvestment change.

## Grid, reverse DCF, and call

Before running the grid, I predicted its highest corner would be 9% WACC / 4% terminal growth, because a lower discount rate and higher terminal growth both increase value. The 11% / 2% corner should be the lowest.

The reverse DCF holds starting FCFF, WACC, terminal growth, cash, debt, and diluted shares fixed, solving only for a uniform shift to all five explicit FCFF-growth rates. It is an implied expectation, **not proof of mispricing**.

**Watch/defer. Initiate if** the price falls below about **$176.67**, or sourced operating evidence supports a higher five-year FCFF-growth path without erosion in reinvestment or margins; **otherwise defer.** **Monitor:** Data Center revenue growth and operating-cash-flow conversion at the next quarterly report.

## Run and submit

1. Run `python dcf.py` from this folder.
2. Confirm the first twelve labelled lines are followed by the sensitivity grid and reverse-DCF block.
3. To do the training check, temporarily set the seven standard inputs to 100; `[8%, 6%, 5%, 4%, 3%]`; 10%; 3%; 50; 300; and 50, and set `TARGET_SHARE_PRICE` to 30.00. The grid should match the lab and the solved shift should be about +1.78 points. Restore NVIDIA’s inputs before submission.
4. Submit GitHub links to this file and `dcf.py` in the Lab 06 quiz.

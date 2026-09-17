# Lab 08 — Deal Evidence and Valuation Triangulation

## Decision question, date, and initial policy

**Target:** NVIDIA Corporation (NASDAQ: NVDA). **Comparison/Week 3 valuation date:** September 10, 2026. **Valuation object:** one NVIDIA common share in U.S. dollars. This is a course exercise, not investment advice.

NVIDIA earns money primarily by selling accelerated-computing and AI infrastructure products. Its FY2026 release reports $193.7 billion of Data Center revenue, driven by accelerated computing and AI, alongside Gaming, Professional Visualization, and Automotive businesses ([NVIDIA FY2026 results, “Data Center,” published February 25, 2026](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/)). NVIDIA reported positive FY2026 GAAP diluted EPS of **$4.90** ([same release, “Fiscal 2026 Summary—GAAP”](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/)).

**Initial peer policy (written before choosing candidates):** admit only a listed operating company with positive, annual **GAAP diluted EPS** publicly available by September 10, 2026; a material business selling data-center compute or AI accelerators; and semiconductor product economics rather than a primarily software, distribution, or services business. I will qualify companies with major PC, gaming, embedded, networking, or software businesses, and exclude them if those other economics dominate the company. All prices must be the September 10, 2026 close and all EPS inputs must be annual GAAP diluted EPS in USD on the post-split share basis. I did not revise this policy.

Focused research question: **Does AMD derive enough of its earnings from data-center CPUs and AI GPUs for its historical GAAP P/E to be a useful, explicitly qualified reference for NVIDIA, despite AMD's substantial Client and Gaming business?**

I would reject a candidate if its annual earnings were not positive or were only adjusted/non-GAAP, if its share basis/currency did not match the price, or if its filing showed that its principal earnings economics were software or a different semiconductor end market rather than data-center compute.

## Candidate investigation and decision log

I opened the linked company filing or investor-relations release before making each decision.

| Candidate | Evidence opened: business-model source and locator | Important difference from NVIDIA | Latest annual reported diluted EPS public by Sep. 10, 2026 | Decision and reason |
|---|---|---|---|---|
| Advanced Micro Devices (AMD) | [AMD 2025 Form 10-K, Item 7, “Data Center”](https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm) says Data Center revenue was $16.6bn and was driven by EPYC processors and Instinct GPU accelerators. | AMD also generated $14.6bn in Client and Gaming revenue in 2025; NVIDIA's FY2026 Data Center revenue was far more central to its business. | **$2.65**, FY ended Dec. 27, 2025; [AMD FY2025 annual-results release, “Annual Financial Results,” published Feb. 3, 2026](https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000014/0000002488-26-000014.pdf). GAAP, diluted, USD. | **Qualify / use.** It meets the compute-and-accelerator test and has compatible positive GAAP annual EPS, but its different revenue mix makes this one-peer output only a reference. |
| Broadcom (AVGO) | [Broadcom 2025 Form 10-K, Item 7, “Overview”](https://www.sec.gov/Archives/edgar/data/1730168/000173016825000121/avgo-20251102.htm) describes broad semiconductor solutions **and infrastructure software**. | It has material infrastructure-software subscriptions/services and diverse semiconductor products; this is not the same data-center GPU/platform earnings mix. | **$4.77**, FY ended Nov. 2, 2025; [Broadcom FY2025 Form 10-K, Item 8, “Consolidated Statements of Operations / Diluted income per share”](https://www.sec.gov/Archives/edgar/data/1730168/000173016825000121/avgo-20251102.htm), filed Dec. 18, 2025. GAAP, diluted, USD. | **Exclude.** Positive EPS is not enough: Broadcom fails the policy's sufficiently similar business-economics test. Its price and multiple were deliberately not entered in the calculator. |

## Inputs and source ledger

The date is a trading day. I used the **close**, not adjusted close or an intraday quote, for all companies. Nasdaq historical-data pages are the intended price-source pages: [NVDA](https://www.nasdaq.com/market-activity/stocks/nvda/historical), [AMD](https://www.nasdaq.com/market-activity/stocks/amd/historical), and [AVGO](https://www.nasdaq.com/market-activity/stocks/avgo/historical), each with the September 10, 2026 row. The recorded closes are also independently cross-checked in the historical tables for [NVDA](https://www.financecharts.com/stocks/NVDA/summary/price), [AMD](https://stockanalysis.com/stocks/amd/history/), and [AVGO](https://stockanalysis.com/stocks/avgo/history/).

| Company | Sep. 10, 2026 close | Annual GAAP diluted EPS used / fiscal year end | Results public date and earnings locator | Calculator status |
|---|---:|---|---|---|
| NVIDIA (target) | $218.36 | $4.90 / Jan. 25, 2026 | Feb. 25, 2026; [FY2026 release, “Fiscal 2026 Summary—GAAP”](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/) | Target |
| AMD | $503.60 | $2.65 / Dec. 27, 2025 | Feb. 3, 2026; [FY2025 release, “Annual Financial Results”](https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000014/0000002488-26-000014.pdf) | Use, qualified |
| Broadcom | $360.83 | $4.77 / Nov. 2, 2025 | Dec. 11, 2025 release / Dec. 18, 2025 10-K; [Item 8 EPS table](https://www.sec.gov/Archives/edgar/data/1730168/000173016825000121/avgo-20251102.htm) | Excluded |

Reported GAAP EPS is kept separate from adjusted/non-GAAP EPS. I used no quarterly EPS as a substitute for a year, and did not add cash or subtract debt because P/E is already an equity-value-per-share comparison.

## Calculator result and validation

I changed only the input block in `lab_07_pe_comps.py` to NVIDIA and the one admitted, qualified AMD peer, then ran:

```text
python3 lab_07_pe_comps.py
```

AMD's hand check is **$503.60 / $2.65 = 190.037736x**. Applying that multiple to NVIDIA's $4.90 annual GAAP diluted EPS gives **$931.18 per NVIDIA share**. The saved calculator returns the same one-peer reference estimate. It is not a range because one usable peer remains.

Before the changed-peer check, I predicted that removing AMD would leave no P/E estimate because AMD is the only admitted peer. The calculator confirms: removing AMD leaves **no usable peers** and therefore no estimate. Broadcom was not removed merely because of its price or result; it was excluded before the calculation under the documented business-policy test.

This result is mechanically correct but economically fragile. AMD's approximately 190.04x historical-GAAP P/E embeds much higher expected earnings relative to its 2025 GAAP EPS. NVIDIA's FY2026 earnings are also extraordinarily high and already reflect a very different data-center mix and growth path. The $931.18 figure is therefore a **qualified single-peer reference**, not a defensible stand-alone price target.

## DCF comparison and provisional call

| Method | NVIDIA result and date | Main assumption or limitation |
|---|---|---|
| Week 3 DCF | $140.30–$241.88 per share; base $176.67; model dated Sep. 10, 2026 | Five-year FCFF growth path, WACC, and terminal growth are forecasts; years 1–2 growth are the least certain inputs. See [NVIDIA DCF](NVIDIA_DCF.md). |
| Peer P/E | $931.18 one-peer reference; price/EPS inputs dated Sep. 10, 2026 | Only qualified AMD is admitted; the historical-GAAP P/E is highly sensitive to AMD's 2025 earnings base and different Client/Gaming mix. |

The methods should not be averaged. The DCF translates my NVIDIA cash-flow, discount-rate, and terminal-growth assumptions into value; the peer calculation applies AMD's market expectation to NVIDIA's backward-looking EPS. The peer reference is far above both the $218.36 comparison-date price and the DCF range, which is a signal to investigate rather than evidence that NVIDIA should trade at $931.18.

**Provisional call: watch/defer; do not initiate on this evidence alone.** The market price is above my DCF base case but within its sensitivity range, while the only peer reference is too dependent on a differently mixed company and a very high historical multiple to override the DCF. I would change my mind if I could support a materially higher NVIDIA FCFF-growth path with subsequent operating cash-flow conversion and margins, or if a second company meeting the original policy produced a consistent GAAP P/E reference. I would also reassess if NVIDIA's reported Data Center demand, earnings quality, or capital intensity weakens.

## Skeptical AI review and my judgment

**Codex skeptical review:** The weakest supported assumption is that AMD's 190.04x P/E is transferable to NVIDIA. The calculation matches USD, common-share price, annual GAAP diluted EPS, and a single comparison date, but it does not match fiscal year-end (AMD Dec. 2025; NVIDIA Jan. 2026), product/revenue mix, or the market's expected earnings-growth path. The larger mismatch is valuation object: a historical P/E reference is being compared with a DCF of forecast FCFF; neither establishes a common near-term earnings forecast. **Question that could change the decision:** What source-supported FY2027/FY2028 NVIDIA earnings or cash-flow evidence would justify applying even a fraction of AMD's historical P/E rather than relying on the DCF range?

**Judgment: accept.** The AMD filing confirms major Client/Gaming revenue in addition to Data Center, while NVIDIA's annual release shows Data Center is dominant. The sources support the factual mismatch and the question identifies evidence that would genuinely change the call. I reject any implication that the $931.18 reference should be averaged with the DCF: the two methods rely on different assumptions and the peer set has only one qualified company.

## Reflection

AMD adds a market-expectations comparison for a company that sells data-center processors and AI accelerators. Broadcom's exclusion demonstrates why sharing an “AI/semiconductor” label is insufficient. The comparison adds a useful warning that historical P/E can be dominated by expectations and by a peer's current earnings base; it does not replace the DCF. My conditional conclusion remains **watch/defer**, with a defendable DCF range of **$140.30–$241.88** and a clearly withheld peer range (only one qualified reference, $931.18). The answer to the skeptical question is: I would need filed or released evidence of NVIDIA's continuing revenue, operating-cash-flow conversion, margins, and reinvestment that supports a higher explicit FCFF path; then I would rerun the DCF, not mechanically adopt AMD's multiple.

## Submission files

- `Lab_08_deal_evidence_and_valuation_triangulation.md`
- `lab_07_pe_comps.py`
- `NVIDIA_DCF.md`

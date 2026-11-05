# Lab 19 — Legend Panel

## Purpose and fixed design

Three investor skills read the same five-year SEC EDGAR 10-K fact panel. Buffett uses ROE and owner earnings; Graham uses latest current ratio, net-income positivity, and net-income growth; Burry uses operating-cash-flow conversion and latest liabilities to equity. All numerical claims are computed in code. The memos make only a business-quality judgment and use no price data.

Graham's retained current-ratio threshold is **2.0**. The required **1.0** probe passes COST, but I retain 2.0 because the screen is deliberately a conservative liquidity test; lowering it after seeing the result would change the design.

## COST known-answer panel

| Investor | Check | Result |
|---|---|---|
| Buffett | ROE of 15% or more every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew, first year to last | pass |
| Graham | Current ratio of 2.0 or more, latest year | fail (1.06) |
| Graham | Net income positive every year | pass |
| Graham | Net income grew, first year to last | pass |
| Burry | Operating cash flow at least net income every year | pass |
| Burry | Liabilities no more than twice equity, latest year | pass (1.49) |

The live app run reproduced the expected COST panel: Buffett **3 of 3**, Graham **2 of 3**, and Burry **2 of 2**. The three verdicts were Buffett — own the business; Graham — watch it; Burry — own the business.

## Project 2 company: NVDA

I used NVDA as the Project 2 company, based on the prior Project 2 fund universe that included QQQ, SPY, NVDA, and VOO. The panel creates a real split rather than hiding it.

| Investor | Check | Result |
|---|---|---|
| Buffett | ROE of 15% or more every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew, first year to last | pass |
| Graham | Current ratio of 2.0 or more, latest year | pass (3.91) |
| Graham | Net income positive every year | pass |
| Graham | Net income grew, first year to last | pass |
| Burry | Operating cash flow at least net income every year | fail |
| Burry | Liabilities no more than twice equity, latest year | pass (0.31) |

NVDA's Buffett and Graham verdicts are **own the business**. Burry's is **watch it**: operating cash flow was below net income in two displayed years, including 9,108 versus 9,752 and 28,090 versus 29,760. The app retained that failure rather than averaging or explaining it away.

## Bull and bear from the same panel

**Bull:** Buffett's three operating-quality checks and Graham's three profitability/liquidity checks all pass for NVDA. Latest current ratio is 3.91 and latest liabilities to equity is 0.31, which are consistent with balance-sheet flexibility in this narrow screen.

**Bear:** Burry's cash-conversion check fails because operating cash flow did not reach net income in two years. That failure does not prove the business is weak, but it is a reason to investigate the cash-flow-to-income gap before using the panel result as a screen.

## Decision

**Only with a condition:** I would use the panel to prioritize Project 2 research only when every `not found`/`not known` remains visible and any failed check triggers a source-document review; it cannot choose a security or a price on its own.

## Runtime and audit evidence

On 5 November 2026, the updated Streamlit app was run live for COST and NVDA against SEC EDGAR using a runtime-only User-Agent. For both companies it rendered the chart, five-year fact table, panel table, verdicts, three side-by-side memos, and the combined memo-number audit. The audit reported: **Every number in all three memos appears in the scripts' computed panel.**

The audit was also checked by inserting `40.0%` into a memo; the app flagged it as unprinted.

## Artifacts

- [Shared SEC EDGAR analyzer](../../.codex/skills/buffett-edgar/scripts/analyze_company.py)
- [Graham skill](../../.codex/skills/graham-edgar/SKILL.md) and [check code](../../.codex/skills/graham-edgar/scripts/graham_checks.py)
- [Burry skill](../../.codex/skills/burry-edgar/SKILL.md) and [check code](../../.codex/skills/burry-edgar/scripts/burry_checks.py)
- [Lab 19 panel Streamlit app](Lab_19_Legend_Panel_App.py)
- [Lab 19 COST Buffett memo](Lab_19_COST_Buffett_Memo.md), [Graham memo](Lab_19_COST_Graham_Memo.md), and [Burry memo](Lab_19_COST_Burry_Memo.md)
- [Lab 19 NVDA Buffett memo](Lab_19_NVDA_Buffett_Memo.md), [Graham memo](Lab_19_NVDA_Graham_Memo.md), and [Burry memo](Lab_19_NVDA_Burry_Memo.md)

**Sources:** [SEC ticker-to-CIK file](https://www.sec.gov/files/company_tickers.json), SEC company facts for [COST](https://data.sec.gov/api/xbrl/companyfacts/CIK0000909832.json) and [NVDA](https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json), and the [FAskills repository](https://github.com/CinderZhang/FAskills).

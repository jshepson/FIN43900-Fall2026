# Meridian CIO Decision Memo — Project 2

## Recommendation and committee ask

**Reject the QQQ/SPY/NVDA/VOO result as an adoptable allocation; approve it only as a pilot calculation.** Do not allocate Meridian reserve capital from this output. The committee should require a complete, investable mandate and a rerun before considering allocation.

## Decision evidence — as of 2026-10-01

The source file contains monthly adjusted-close observations from 2021-11-01 to 2026-10-01, downloaded from Yahoo Finance on 2026-10-22. Using all 59 monthly returns, the least-volatility long-only 5% grid mix meeting the labelled 6.5% gross objective is 0% QQQ / 75% SPY / 0% NVDA / 25% VOO, with a 13.11% annualized arithmetic-return estimate and 15.56% annualized volatility. Using only the latest 36 returns, it becomes 0% / 100% / 0% / 0%, with a 22.15% estimate and 12.25% volatility.

This is not a stable investment recommendation: SPY increases 25 percentage points and VOO falls 25 percentage points solely because the estimation window changes. SPY and VOO also substantially overlap, so the apparent two-fund allocation is not meaningful diversification.

## Assumptions and limitations

The 6.5% objective is a labelled classroom input, not a client-approved or net-of-costs objective. Estimates are historical arithmetic means, not forecasts. Results are gross and pre-cost because no trading-cost or turnover model is supplied. The universe has no reserve-eligible sleeve, so the documented 0% reserve floor is a data limitation—not satisfaction of Meridian's 3% reserve requirement.

## Conditions that would reverse the decision

Reconsider a pilot or allocation only when the CIO supplies: a genuine reserve sleeve; a net-of-costs objective; explicit treatment of SPY/VOO overlap; a calendar-year loss rule with breach response; liquidity, concentration, and turnover checks; and a predeclared stability test that does not produce a materially different allocation. The portfolio owner must rerun the analysis at each new data cutoff and escalate any failed condition to the CIO.

The detailed source, validation, and AI-use record is in [validation-and-ai-use.md](validation-and-ai-use.md).

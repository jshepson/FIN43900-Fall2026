# Meridian CIO Decision Memo — Project 2

**AI disclosure:** I used Codex to help organize the app, documentation, and reproducibility checks. The analysis and decision are mine. This is for education, not investment advice.

## Recommendation

**Reject allocation to the QQQ/SPY/NVDA/VOO output and retain it only as a research pilot. Allocate 0% of Meridian reserve capital to this process today.** A future pilot allocation range is **0% to 5%**, only after every reversal condition below is met and the CIO approves it; no range is authorized for live investment before then.

## Evidence and comparison

As of 2026-10-01, the frozen data input has 59 monthly simple returns from Yahoo Finance adjusted closes (downloaded 2026-10-22). With the actual 3.0% reserve minimum, neither the two baselines nor the constrained candidate passes: the four-ticker universe has 0.0% reserve-eligible weight and no cash/daily-liquid government-security sleeve. The app makes that failure visible rather than silently substituting a 0% reserve rule.

For mechanics-only inspection under a 0% reserve relaxation and a 6.5% gross historical-estimate floor, the all-history candidate is 0% QQQ / 75% SPY / 0% NVDA / 25% VOO, with 13.11% annualized arithmetic estimated return and 15.56% annualized volatility. On the latest 36 returns it becomes 0% / 100% / 0% / 0%, with 22.15% and 12.25%, respectively. The 25-point allocation shift exceeds the predeclared 20-point materiality limit. SPY and VOO substantially overlap, so the apparent two-fund allocation does not demonstrate meaningful diversification.

## Stress and stop condition

The application permits a reviewer to stress the estimation window, explicit cost basis points, an estimate haircut, and the reserve constraint. Costs reduce each gross historical estimate; a haircut reduces it further. A positive reserve rule has no feasible candidate because the source universe contains no eligible sleeve. The process stops—and no allocation recommendation may be made—if any hard mandate condition fails or cannot be tested, if a positive reserve requirement has no eligible asset, or if a predeclared stress changes weights by more than 20 percentage points.

## Monitoring and reversal triggers

Monitor at every data cutoff: source-file/hash and vendor revisions; reserve-eligible weight; five-day liquidity; aggregated company exposure; turnover; costs; net-of-costs objective; overlap/exposure look-through; loss-rule breach status; and window/estimate/cost sensitivity. Escalate any failure to the CIO.

Reconsider only after the CIO supplies an investable universe with a genuine reserve sleeve; confirms a net-of-costs objective and a calendar-year-loss definition/breach response; provides liquidity, concentration, and turnover inputs; decides how to treat SPY/VOO overlap; and the locked validation plan passes without a material allocation change. That later reconsideration may authorize a 0%–5% pilot only; it is not an authorization to allocate now.

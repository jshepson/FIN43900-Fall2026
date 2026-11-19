# Video 2 transcript — Code and validation walkthrough (read verbatim when recording)

**AI disclosure:** I used Codex to help organize the app and documentation. The analysis and decision are mine. This is for education, not investment advice.

I am starting the application from its README command: python3 app.py. The app is now running live at the local address printed in the terminal.

The app uses only Python's standard library. The frozen data file contains monthly adjusted closes for QQQ, SPY, NVDA, and VOO through October 1, 2026. In app.py, price_data reads that local CSV. Estimates converts adjacent prices to simple monthly returns, annualizes their arithmetic mean and sample volatility, calculates correlations from the same return sample, and makes a trailing-12-month momentum signal. That point-in-time signal is displayed but not used by the optimizer.

Portfolio statistics calculates gross return, stated-cost and haircut net return, and volatility from every covariance term. Optimize enumerates long-only weights on a 5 percent grid. Crucially, it returns no candidate whenever reserve minimum is positive, because this universe has no reserve-eligible sleeve. It does not silently relax that mandate rule.

The table shows equal weight and inverse volatility as transparent baselines alongside the constrained candidate. Each row receives a mandate verdict. I begin with the actual mandate settings: 59 monthly returns, zero costs, zero estimate haircut, and a 3 percent reserve minimum. With Meridian's real 3 percent reserve rule, each row fails because reserve eligibility is zero.

For the mechanics-only validation, I temporarily change the reserve minimum from 3 percent to zero and click Run stress. This is not a recommendation; it only exposes the model calculation. I then change the window from 59 returns to the latest 36 and click Run stress. The documented comparison moves from 75 percent SPY and 25 percent VOO to 100 percent SPY, a 25-point shift. Next, I enter 50 basis points of costs and a 1 percentage-point estimate haircut, clicking Run stress after each change. These lower the net estimate. Finally, I return the reserve minimum to 3 percent and click Run stress. The app correctly shows no feasible candidate. These controls test window, estimates, costs, and constraints. My stop condition prohibits allocation if a hard rule fails or cannot be tested, or if a stress moves allocation more than 20 points.

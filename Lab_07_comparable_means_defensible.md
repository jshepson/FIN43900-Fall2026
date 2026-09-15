# Lab 07 — Comparable Means Defensible

## What I need to submit

Submit the GitHub links to this reflection and to `lab_07_pe_comps.py` in the Lab 07 Brightspace quiz when the instructor says to start it. The required evidence is the checked Asbury calculation, a justified peer decision, and an interpretation of the changed-peer result. This is an individual submission.

## Reopen and explain

My Week 3 DCF produces a base value of $176.67 per NVIDIA share, with a sensitivity range of $140.30 to $241.88. The major drivers are the five-year FCFF growth path, WACC, and terminal growth; the early growth assumptions are the input I distrust most. My initial question was: why can two companies in the same industry have different P/E multiples, and when would that difference make the comparison misleading?

Run the saved DCF from this folder with:

```bash
python dcf.py
```

Run the Lab 07 calculator with:

```bash
python lab_07_pe_comps.py
```

## What P/E means

P/E is price per share divided by annual diluted earnings per share (EPS). Price per share is the market value of one share; EPS is the annual earnings attributable to each diluted share. The resulting multiple shows how many dollars investors are paying for each dollar of annual earnings.

P/E puts differently sized companies on a per-share earnings basis, so a $400 share is not automatically more expensive than a $170 share. It complements the DCF: the DCF uses my assumptions about future cash flows, while P/E asks what the target would be worth if the market applied comparable companies' earnings multiples. A difference between the two methods is a reason to inspect the forecast, earnings definition, peers, and market conditions—not to average the values automatically.

A lower P/E is not automatically better. It may reflect lower expected growth, more risk, weak earnings quality, or different business economics. P/E is most useful when peers have comparable operations and positive earnings measured consistently. It is not meaningful for negative EPS. Unusual or temporarily high earnings can make P/E look artificially low; unusually depressed earnings can make it look high. Growth prospects, risk, geography, and financing activities can justify different multiples.

## Peer policy before the prices

Use publicly traded franchised vehicle retailers with new and used vehicle sales plus meaningful parts and service operations, positive annual GAAP diluted EPS, and the same earnings definition. Compare scale, geography, and financing activities before interpreting the number.

- **AutoNation (use):** It is a franchised vehicle retailer with comparable vehicle-sales and service activities. Its AutoNation Finance operations are a business difference to watch, but its core economics fit Asbury's.
- **Group 1 Automotive (use, qualified):** It has comparable dealer, vehicle-sales, and service economics. Its U.K. operations and the acquisition of 54 Inchcape dealerships in 2024 are material qualifications because they affect geography and the earnings being compared.

Neither is an exact copy of Asbury; that is why this output is a reference range rather than a proof of fair value.

## Asbury worked case

Inputs use December 31, 2024 closing prices and FY2024 total GAAP diluted EPS. This is a retrospective training comparison: annual earnings were reported after the year-end price, so it is not a point-in-time trade recommendation.

| Company | Price | FY2024 total GAAP diluted EPS | P/E |
|---|---:|---:|---:|
| Asbury (ABG), target | $243.03 | $21.50 | Target only; excluded from peer set |
| AutoNation (AN), peer | $169.84 | $16.92 | 10.037825x |
| Group 1 (GPI), qualified peer | $421.48 | $36.81 | 11.450149x |

AutoNation P/E is $169.84 / $16.92 = **10.037825x**. Group 1 P/E is $421.48 / $36.81 = **11.450149x**. The two-peer median P/E is **10.743987x**.

Applying the minimum, median, and maximum peer P/E multiples to Asbury's $21.50 EPS produces:

| Result | Implied price |
|---|---:|
| Minimum peer P/E | $215.81 |
| Median peer P/E | $231.00 |
| Maximum peer P/E | $246.18 |
| Peer-implied range | $215.81-$246.18 |

No cash or debt is added or subtracted: P/E already compares equity value per share with earnings per share.

## Change one peer

Before calculating, I predicted that removing Group 1 would lower the median-implied price because Group 1 has the higher P/E. The calculator confirms this: removing GPI leaves AutoNation's **$215.81** reference estimate, a **-$15.18** change from the full-peer median-implied price of $231.00.

With only AutoNation remaining, there is no peer range: one P/E produces one reference estimate. Removing Group 1 is not justified merely because it lowers the result; the original decision should remain unless the business evidence—not a preferred price—warrants exclusion.

## Reflection

The peer-implied band does not prove that Asbury is fairly valued. It depends on two selected peers, their reported GAAP earnings, and the assumption that their market multiples are relevant to Asbury despite differences in financing, geography, scale, and acquisitions. It is a useful comparison to investigate alongside a DCF, not investment advice or a conclusion by itself.

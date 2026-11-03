# Lab 18 — Legend Investor as Skill

This submission turns a fixed Buffett-style 10-K review into the repo-scoped
`buffett-edgar` Codex skill at [`../../.codex/skills/buffett-edgar`](../../.codex/skills/buffett-edgar/).
The script computes all figures from SEC EDGAR; the Markdown memo is a limited,
price-free business judgment based only on the printed results.

## Run

Use a truthful SEC User-Agent that identifies you and provides a contact email:

```sh
../../.venv/bin/python ../../.codex/skills/buffett-edgar/scripts/analyze_company.py COST \
  --user-agent "Your Name your.email@example.edu"
../../.venv/bin/streamlit run app.py
```

The app requests the same User-Agent in its sidebar. It plots owner earnings and
net income, shows every XBRL tag and fixed check, displays the COST memo, and
flags any numeric memo claim absent from the computed output.

## Known-answer validation

On 3 November 2026, the analyzer reproduced the supplied COST values for FY2022
through FY2026, including owner earnings of 3,501, 6,745, 6,629, 7,837, and
9,382. Its ROE, positive-owner-earnings, and owner-earnings-growth checks all
passed. The JPM probe returned `not found` for capital spending and `not known`
for both owner-earnings checks. An injected `40.0%` in the memo was flagged by
the app.

This is a learning demonstration, not investment advice.

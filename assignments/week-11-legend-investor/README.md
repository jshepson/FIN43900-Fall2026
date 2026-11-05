# Lab 18 — Legend Investor as Skill

This submission turns a fixed Buffett-style 10-K review into the repo-scoped
`buffett-edgar` Codex skill at [`../../.codex/skills/buffett-edgar`](../../.codex/skills/buffett-edgar/).
The script computes all figures from SEC EDGAR; the Markdown memo is a limited,
price-free business judgment based only on the printed results.

## Submission links

- [`SKILL.md`](../../.codex/skills/buffett-edgar/SKILL.md) — reusable Codex skill instructions.
- [`analyze_company.py`](../../.codex/skills/buffett-edgar/scripts/analyze_company.py) — EDGAR computation script.
- [`app.py`](app.py) — Streamlit application.
- [`COST_buffett_memo.md`](COST_buffett_memo.md) — short model judgment using only computed facts.
- [`COST_run_evidence.md`](COST_run_evidence.md) — rendered chart, computed table, checks, memo, and audit evidence.
- [`BRO_run_evidence.md`](BRO_run_evidence.md) — Brown & Brown run evidence, including its preserved missing-equity limitation.
- [`NVDA_run_evidence.md`](NVDA_run_evidence.md) — NVIDIA run evidence.
- [`Lab_19_Legend_Panel.md`](Lab_19_Legend_Panel.md) — COST known-answer panel, NVDA panel, threshold probe, bull/bear, decision, and live-run evidence.
- [`graham-edgar`](../../.codex/skills/graham-edgar/SKILL.md) and [`burry-edgar`](../../.codex/skills/burry-edgar/SKILL.md) — the new Lab 19 skills.
- [`lab-19/`](lab-19/README.md) — one-stop Lab 19 GitHub submission index.

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

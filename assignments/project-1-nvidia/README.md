# NVIDIA Project 1 - Corporate Finance Application

This is a FIN 43900 course project, not investment advice. The committee action is **watch/defer** as of September 24, 2026. The evidence cutoff is the NVIDIA Q2 FY2027 Form 10-Q filed August 26, 2026, plus the September 24 market-price reference recorded in the course work.

## Decision boundary

| Field | Final definition |
|---|---|
| User and action | Buy-side investment committee; initiate, watch/defer, or do not initiate NVIDIA common stock. |
| Target/security | NVIDIA Corporation (`NVDA`) common stock. |
| Valuation date/currency | September 24, 2026; USD. |
| Share basis | 24,304 million common shares outstanding, used consistently as a valuation-date share proxy; it is not the 24,514 million FY2026 weighted-average diluted EPS denominator. |
| Model architecture | Five-year three-statement pro-forma -> FCFF -> enterprise value -> equity bridge -> per-share value. |
| Exclusions | The AMD P/E reference is not averaged into the DCF range. No transaction value is used because a comparable control/synergy context was not established. |

## Run

From the repository root:

```sh
python assignments/project-1-nvidia/analysis.py
```

The executed result is saved in `visible_output.txt`. The program uses only the Python standard library and the existing NVIDIA pro-forma source file in `assignments/week-05-pro-forma/`.

## Folder guide

- `edition-a/`: unchanged Edition A source.
- `analysis.py`: final FCFF valuation wrapper and validation checks.
- `visible_output.txt`: executed, reviewable output.
- `evidence/`: source ledger, challenge record, and validation/AI-use record.
- `Decision_Memo.md`: final committee memo source.
- `videos/`: your recording scripts/transcripts. You must record and upload the three actual videos yourself.
- `project-submission-manifest.csv`: final access checklist; complete stable video URLs after recording.

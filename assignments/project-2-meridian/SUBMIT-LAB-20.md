# Submit Lab 20 From This Folder

Open this folder on GitHub and submit the links your instructor requests. The Lab 20 materials are all under `assignments/project-2-meridian`; you do not need to search the earlier weekly-lab folders.

## Submit these GitHub files

1. [Lab 20 checkout](Lab_20_Project2_Readiness.md) — your main individual checkout. Fill your partner details, session token, personal attestation, and receipt fields before submitting.
2. [README](README.md) — exact one-command reproduction instructions.
3. [Analysis code](analysis.py) — produces the decision output.
4. [Visible executed output](visible_output.json) — the decision numbers readable without running code.
5. [Decision memo](docs/decision-memo.md) — current committee decision and reversal conditions.
6. [Validation and AI-use record](docs/validation-and-ai-use.md) — validation, limits, and changed-input status.
7. [12-row manifest](project-submission-manifest.csv) — Project 2 readiness status, including honestly unresolved video/PDF rows.

## Do not submit as your own evidence

[Worked example](examples/Lab_20_worked_example.md) is only a formatting guide. It is not a partner cold run, a student-authored prediction, or an AI-closed run.

## Exact command

```sh
python3 assignments/project-2-meridian/analysis.py
```

The project uses the existing course calculation engine and source data in `assignments/week-09-portfolio-baselines/`; this Project 2 folder is the submission-facing package and links to that provenance in its README.

# Lab 20 Worked Example — Do Not Submit as Your Own Record

This illustrates format only. Replace every example statement with your own partner's actual observation and your own pre-run, AI-off prediction. It is not evidence that a partner performed a cold run or that a changed-input run was AI closed.

## Example partner cold-run note

| Field | Example only |
|---|---|
| Partner | Example Partner — replace with your actual partner |
| Folder | Fresh clone in a separate folder |
| Command entered | `python3 assignments/project-2-meridian/analysis.py` |
| First failure | `python assignments/project-2-meridian/analysis.py` failed because this computer did not provide a `python` command. |
| Elapsed time to first result | 0:12 |
| Where the result appeared | Terminal JSON; frozen copy at `assignments/project-2-meridian/visible_output.json` |
| Fix and rerun | README changed the command to `python3`; partner reruns after pulling the commit. |

Do not copy this note into your checkout. Ask your partner to use the README only and write what actually happened.

## Example changed-input sequence

1. With AI closed, write your own prediction in a new file before running anything. State the old/new values and units, expected direction of each decision number, and expected decision effect.
2. Commit and push that prediction by itself. Record that commit hash and time.
3. Still AI closed, run the command and save the output.
4. Add the before/after result, whether the decision changed, and why. Commit that result separately.

### Illustrative prediction — not student-authored evidence

| Input | Old → new | Illustrative expected output direction | Illustrative decision effect |
|---|---|---|---|
| Estimation window | all 59 monthly returns → latest 36 monthly returns | SPY weight increases; VOO weight decreases; return and volatility estimates change | Recommendation remains reject because the allocation is window-sensitive. |

### Illustrative actual result — not AI-closed evidence

| Before | After | Actual decision effect | Reconciliation |
|---|---|---|---|
| 0% QQQ / 75% SPY / 0% NVDA / 25% VOO; 13.11% return; 15.56% volatility | 0% / 100% / 0% / 0%; 22.15% return; 12.25% volatility | Still reject as adoptable; the window change remains material. | The direction matches the illustration: SPY rises 25 percentage points and VOO falls 25 points. |

Use `visible_output.json` as the preserved output reference. This example does not satisfy the Locked Changed-Input Record because it was written with AI assistance.

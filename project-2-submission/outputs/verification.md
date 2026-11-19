# Local verification record

Run on 2026-11-17 with Python 3.13:

```sh
python3 -m py_compile app.py
python3 -c "import app; print(app.optimize(*app.estimates(59)[1:4], 0, 0, 0)[0])"
```

Observed mechanics-only 0%-reserve allocation:

```text
{'QQQ': 0.0, 'SPY': 0.75, 'NVDA': 0.0, 'VOO': 0.25}
```

The local execution sandbox forbids binding a localhost TCP port, so it could not perform a browser HTTP check. `app.page({})` and the calculation functions were imported and evaluated successfully. A normal local machine should run the README command and complete the fresh-terminal/browser check before submission.

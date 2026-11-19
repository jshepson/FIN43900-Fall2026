"""Meridian Investment Management Application (standard-library web app).

Run from this directory: python3 app.py
Then open http://127.0.0.1:8000 in a browser.  No packages or network access
are required.  The app intentionally produces a *reject / pilot only* decision:
the supplied four-ticker research universe cannot satisfy Meridian's reserve rule.
"""
from __future__ import annotations

import csv
import html
import math
from itertools import product
from pathlib import Path
from statistics import correlation, mean, stdev
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

HERE = Path(__file__).resolve().parent
PRICE_FILE = HERE / "data" / "prices.csv"
NAMES = ("QQQ", "SPY", "NVDA", "VOO")
OBJECTIVE = 0.065
GRID_STEP = 0.05
MANDATE_RESERVE = 0.03


def price_data():
    with PRICE_FILE.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    dates = [row["Date"] for row in rows]
    prices = {name: [float(row[name]) for row in rows] for name in NAMES}
    return dates, prices


def estimates(window: int):
    dates, prices = price_data()
    returns = {
        name: [(b / a) - 1 for a, b in zip(values, values[1:])][-window:]
        for name, values in prices.items()
    }
    means = {name: mean(values) * 12 for name, values in returns.items()}
    vols = {name: stdev(values) * math.sqrt(12) for name, values in returns.items()}
    corr = {
        left: {right: 1.0 if left == right else correlation(returns[left], returns[right])
               for right in NAMES}
        for left in NAMES
    }
    momentum = {name: prices[name][-1] / prices[name][-13] - 1 for name in NAMES}
    return dates[-1], means, vols, corr, momentum


def portfolio_stats(weights, means, vols, corr, cost_bps, haircut_pct):
    gross = sum(weights[name] * means[name] for name in NAMES)
    net = gross - cost_bps / 10000 - haircut_pct / 100
    variance = sum(weights[a] * weights[b] * vols[a] * vols[b] * corr[a][b]
                   for a in NAMES for b in NAMES)
    return gross, net, math.sqrt(max(variance, 0))


def optimize(means, vols, corr, cost_bps, haircut_pct, reserve_minimum):
    # The research universe has no cash/T-bill sleeve. A positive reserve rule is
    # therefore infeasible by design; the app never silently relaxes it.
    if reserve_minimum > 0:
        return None
    units = round(1 / GRID_STEP)
    best = None
    for partial in product(range(units + 1), repeat=3):
        final = units - sum(partial)
        if final < 0:
            continue
        weights = dict(zip(NAMES, [x * GRID_STEP for x in (*partial, final)]))
        gross, net, volatility = portfolio_stats(weights, means, vols, corr, cost_bps, haircut_pct)
        if net + 1e-12 >= OBJECTIVE and (best is None or volatility < best[3]):
            best = weights, gross, net, volatility
    return best


def mandate_verdict(weights, reserve_minimum):
    if weights is None:
        return "FAIL — no feasible model portfolio: the requested reserve minimum is positive, but this universe has no reserve-eligible sleeve."
    if MANDATE_RESERVE > 0:
        return ("FAIL — 0.0% reserve-eligible weight versus Meridian's 3.0% minimum. "
                "Liquidity, issuer concentration, turnover, loss rule, and net-of-costs objective also remain unverified.")
    return "NOT ADOPTABLE — the scenario relaxed the actual 3.0% reserve mandate only to inspect model mechanics."


def pct(value):
    return f"{value * 100:.2f}%"


def weights_text(weights):
    if weights is None:
        return "No feasible allocation"
    return " · ".join(f"{name} {weights[name] * 100:.0f}%" for name in NAMES)


def result_row(label, weights, means, vols, corr, cost_bps, haircut, reserve):
    if weights is None:
        return f"<tr><th>{html.escape(label)}</th><td colspan='4'>No feasible allocation</td><td>{html.escape(mandate_verdict(None, reserve))}</td></tr>"
    gross, net, volatility = portfolio_stats(weights, means, vols, corr, cost_bps, haircut)
    return (f"<tr><th>{html.escape(label)}</th><td>{weights_text(weights)}</td><td>{pct(gross)}</td>"
            f"<td>{pct(net)}</td><td>{pct(volatility)}</td><td>{html.escape(mandate_verdict(weights, reserve))}</td></tr>")


def number(query, key, default, lower, upper):
    try:
        value = float(query.get(key, [str(default)])[0])
        return min(max(value, lower), upper)
    except ValueError:
        return default


def page(query):
    window = int(number(query, "window", 59, 36, 59))
    cost_bps = number(query, "cost", 0, 0, 500)
    haircut = number(query, "haircut", 0, 0, 20)
    reserve = number(query, "reserve", 3, 0, 20) / 100
    as_of, means, vols, corr, momentum = estimates(window)
    equal = {name: 0.25 for name in NAMES}
    inverse_raw = {name: 1 / vols[name] for name in NAMES}
    inverse = {name: value / sum(inverse_raw.values()) for name, value in inverse_raw.items()}
    candidate = optimize(means, vols, corr, cost_bps, haircut, reserve)
    candidate_weights = None if candidate is None else candidate[0]
    stop = ("STOP — reject allocation / retain calculation only as a pilot. The model universe cannot meet the 3.0% reserve requirement."
            if reserve >= MANDATE_RESERVE else
            "STOP — this what-if relaxes Meridian's real reserve rule and is not eligible for adoption.")
    stress_window = optimize(*estimates(36)[1:4], cost_bps, haircut, 0) if window == 59 else None
    change = "n/a"
    if candidate_weights and stress_window:
        shift = sum(abs(candidate_weights[n] - stress_window[0][n]) for n in NAMES) / 2
        change = pct(shift)
    rows = "".join([
        result_row("Equal weight baseline", equal, means, vols, corr, cost_bps, haircut, reserve),
        result_row("Inverse-volatility baseline", inverse, means, vols, corr, cost_bps, haircut, reserve),
        result_row("Constrained grid candidate", candidate_weights, means, vols, corr, cost_bps, haircut, reserve),
    ])
    signal = " · ".join(f"{name}: {pct(momentum[name])}" for name in NAMES)
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>Meridian Investment Management App</title>
<style>body{{font:16px system-ui,sans-serif;max-width:1200px;margin:2rem auto;padding:0 1rem;color:#172033}}h1{{margin-bottom:.1rem}}.warning{{background:#fff1f0;border-left:6px solid #b42318;padding:1rem;font-weight:600}}.card{{background:#f4f7fb;padding:1rem;margin:1rem 0;border-radius:8px}}table{{border-collapse:collapse;width:100%;font-size:.9rem}}th,td{{text-align:left;vertical-align:top;padding:.6rem;border:1px solid #cbd5e1}}input{{width:5rem}}footer{{color:#475569;font-size:.9rem;margin:2rem 0}}</style></head><body>
<h1>Meridian Investment Management Application</h1><p><strong>Decision:</strong> Reject for allocation; permit only a research pilot. As-of: {as_of}; source downloaded 2026-10-22.</p>
<div class='warning'>{stop}</div>
<form class='card' method='get'><strong>Stress controls</strong><br><label>Return window <select name='window'><option value='59' {'selected' if window == 59 else ''}>59 monthly returns</option><option value='36' {'selected' if window == 36 else ''}>latest 36</option></select></label> <label>Costs (bps) <input name='cost' value='{cost_bps:g}'></label> <label>Estimate haircut (percentage points) <input name='haircut' value='{haircut:g}'></label> <label>Reserve minimum (%) <input name='reserve' value='{reserve * 100:g}'></label> <button>Run stress</button><p>Candidate: long-only 5% grid, minimum 6.5% net estimated return. A positive reserve setting deliberately makes this universe infeasible.</p></form>
<h2>Baselines and constrained candidate</h2><table><tr><th>Portfolio</th><th>Weights</th><th>Gross estimate</th><th>Net estimate</th><th>Volatility</th><th>Mandate verdict</th></tr>{rows}</table>
<div class='card'><h2>Point-in-time signal card</h2><p><strong>Signal:</strong> trailing 12-month simple price momentum, measured only using prices available at {as_of}. It is displayed for review, not used by the optimizer or to select assets.</p><p>{signal}</p><p><strong>Data card:</strong> Yahoo Finance adjusted-close monthly prices, downloaded 2026-10-22; 2021-11-01 through 2026-10-01; USD; vendor revisions possible. Returns are simple monthly returns; arithmetic mean × 12 and sample volatility × √12. This is historical estimation, not a forecast.</p></div>
<div class='card'><h2>Predeclared stress and stop condition</h2><p>Window stress: all 59 returns versus latest 36. With no cost/haircut and the mechanics-only 0% reserve relaxation, the prior base candidate is SPY 75% / VOO 25%; latest-36 candidate is SPY 100%. Total weight shift: 25.00%, exceeding the 20% materiality threshold.</p><p>Estimate stress: haircut estimates; cost stress: subtract stated bps from each portfolio's gross estimate; constraint stress: apply the 3.0% reserve rule. <strong>Stop:</strong> do not recommend allocation if any hard mandate rule fails/is untestable, a positive reserve rule has no eligible sleeve, or the predeclared stress changes weights by more than 20 percentage points.</p></div>
<footer>AI disclosure: Codex helped organize and implement this app. The analysis and decision are the student's responsibility. Educational use only; not investment advice. See README, docs, and validation record.</footer></body></html>"""


def application(environ, start_response):
    query = parse_qs(environ.get("QUERY_STRING", ""))
    body = page(query).encode("utf-8")
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(body)))])
    return [body]


if __name__ == "__main__":
    print("Serving Meridian app at http://127.0.0.1:8000 — press Ctrl+C to stop.")
    with make_server("127.0.0.1", 8000, application) as server:
        server.serve_forever()

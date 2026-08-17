<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  <br />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Kaggle Environment](https://img.shields.io/badge/Kaggle-Environment-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/kaggriculture)
  [![Tests](https://img.shields.io/badge/tests-56%20passing-2ea44f?logo=pytest&logoColor=white)](#-verified-current-strategy)
  [![Submission status](https://img.shields.io/badge/V5%20submission-COMPLETE-2ea44f?logo=kaggle&logoColor=white)](#-submission)
  [![Policy](https://img.shields.io/badge/policy-V5%20recovery%20controller-7B61FF)](#-strategy)

  **A deterministic demand-routed farm agent for Kaggle's 720-state economic simulation.**
</div>

## 🌾 Overview

This repository contains a self-contained V5 agent for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
It shares one opening route, observes the public town shop sequence, and
freezes one of two production experts at step 168:

```text
shared opening through step 167
  ├─ low expert  → terminal 10 cows / 4 sheep
  └─ high expert → terminal 6 cows / 8 sheep
                     (12 sheep requested and placed cumulatively)
```

The policy uses gameplay observations only. It does not route on episode ID,
opponent or team identity, submission ID, or random seed. The Kaggle entrypoint
is [`main.py`](main.py); it has no runtime dependency on the rest of this
repository and returns only JSON-safe actions.

## 🧠 Strategy

V5 combines a deterministic two-expert production tape with failure-driven
execution and market repair:

- each seat keeps independent state, accumulates `unlocked_shops` through step
  168, then makes a sticky route decision;
- any observed `YARN_STORE` selects the high expert, except when the first two
  shops are exactly `ICE_CREAM_SHOP`, `YARN_STORE`, which selects the low
  expert because that early mix is milk-dominated;
- the low expert requests, places, and finishes with 10 cows and 4 sheep;
- the high expert requests and places 6 cows and 12 sheep over the full tape;
  four sheep leave or are replaced during the lifecycle, and verified terminal
  smokes finish at the stable 6-cow/8-sheep herd;
- visible weeds, displaced cow carriers, seed-prefix surplus, and partial cow
  purchases are repaired from observable state without changing the chosen
  route target;
- an active weed transaction is cleared at hour 0 because the engine resets
  workers to the shed at each day boundary; this prevents stale movement,
  watering, and care actions from yesterday's position;
- scheduled premium sales retain quantity-conserving one-turn and guarded
  seven-turn leads, with exact repayment at the original sale step;
- SELL slots are ranked using projected same-turn executable shed stock after
  PICKUP, DROP, and PLACE, and duplicate product orders are merged;
- terminal WHEAT seed purchases are removed once the route has no future WHEAT
  planting, avoiding malformed zero-quantity market orders;
- every nonzero-step observation is retry-safe through a per-seat state/action
  cache keyed by the gameplay observation;
- every action is hand-aligned, market orders remain capped at 10, and a
  malformed observation falls back to JSON-safe `PASS` actions.

The route tapes were reconstructed by component-wise majority from public
opponent behavior, then normalized, serialized, and compressed. Public
Notebooks were also used as mechanism references and hash-pinned evaluation
opponents; that does not establish that a replay participant ran a particular
Notebook artifact. Attribution and this boundary are recorded in
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). The detailed strategy and
evidence protocol are in [`docs/v5-strategy.md`](docs/v5-strategy.md).

## ✅ Verified current strategy

The current `main.py` SHA-256 is
`9390f7a9136f7c724376107fa3b2f464d871b0d725ac2039503c1cc312f6bc5b`.
It passed 56 automated tests. With `kaggle-environments==1.32.6`, starter and
random smoke matches each completed 720 states with `DONE/DONE` and no stderr;
the candidate won both local matches.

The current-hash opened regression panel used 16 seeds, four hash-pinned public
policies, and both candidate seats. Every game reached 720 states and
`DONE/DONE` without captured stderr:

| Frozen opponent artifact | Games | V5 W-L | Mean margin | Worst margin |
|:---|---:|---:|---:|---:|
| Kaito v27 | 32 | **32-0** | +14,526.500 | +1,697 |
| V17 | 32 | **32-0** | +6,294.219 | +906 |
| Public MoE | 32 | **32-0** | +2,837.188 | +777 |
| Tetsu adaptive | 32 | **32-0** | +1,626.594 | +181 |
| **Overall** | **128** | **128-0** | **+6,321.125** | **+181** |

The separately generated RC1 diagnostic panel reached 123/128, with mean
margin +6,417.453 and worst margin -2,549. It is retained as an honest
near-mirror diagnostic, not hidden by seed or opponent routing and not used to
claim universal performance. Exact hashes, seeds, aggregates, and claim
limits are recorded in
[`docs/evidence/v5-failure-analysis.json`](docs/evidence/v5-failure-analysis.json).

## 🚜 Quick start

Prerequisites: Git, CPython 3.12.13, and a POSIX-like shell. The exact Python
version is recorded in [`.python-version`](.python-version).

The committed `requirements.lock` reproduces the audited development package
snapshot for CPython 3.12.13 on macOS 26.5.1 arm64. It is intentionally
platform-specific and excludes `pip`, `setuptools`, and `wheel`.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python -m pip check
python -m pytest -q
```

On another operating system or architecture, resolve the portable top-level
inputs instead of using the macOS lock snapshot:

```bash
python -m pip install -r requirements-dev.txt
python -m pip check
```

Run full matches and write ignored replays:

```bash
python scripts/run_local_match.py --opponent starter --seed 20260805
python scripts/run_local_match.py --opponent random --seed 20260805 --player 1
```

Run a both-seat league against external public-agent files without committing
those files:

```bash
python scripts/run_league.py \
  --opponent kaito=/absolute/path/to/kaito.py \
  --opponent v17=/absolute/path/to/v17.py \
  --seed 20260811 --seed 20260829 \
  --output runs/eval/v4-panel.json
```

Build the minimal Kaggle archive and inspect its contents:

```bash
python scripts/package_submission.py
tar -tzf dist/submission.tar.gz
```

## 📦 Submission

V5 submission `55574866`, message `v5 recovery-aware executable-market
controller cd5e81b`, reached `COMPLETE`. The uploaded `main.py` maps to public
Git commit [`cd5e81b`](https://github.com/COK-ZhangZiliang/Kaggriculture/commit/cd5e81b1cc9d6ef38422aa5d47c7f76e64c866fc).
The reviewed three-file archive is 35,598 bytes with SHA-256
`9baa7fd9783bab1391fa7293497a174abf5772e0e0beae2b8259aabf9447f1b1`.

Kaggle reported an initial public score of **600.0** at
`2026-08-17T08:58:58Z`. Ratings are dynamic and this is a delivery snapshot,
not a final-rank or hidden-test estimate. The packaging script keeps the
executable self-contained and carries the applicable notice and license:

```text
submission.tar.gz
├── main.py
├── LICENSE-APACHE-2.0.txt
└── THIRD_PARTY_NOTICES.txt
```

Generated archives, replays, credentials, datasets, caches, and virtual
environments are ignored by Git.

## 🗂️ Project layout

```text
.
├── main.py                       # self-contained Kaggle agent
├── scripts/
│   ├── package_submission.py     # build and verify the archive
│   ├── analyze_failure_replays.py # summarize ignored public replay files
│   ├── run_local_match.py        # run a 720-state local episode
│   └── run_league.py             # both-seat file-agent league
├── docs/v5-strategy.md           # current strategy and evidence boundary
├── docs/evidence/v5-failure-analysis.json
├── tests/                        # unit and environment smoke tests
├── assets/logo.svg               # project wordmark
├── LICENSES/Apache-2.0.txt       # third-party license copy
├── THIRD_PARTY_NOTICES.md        # route provenance and modifications
├── AGENTS.md                     # strategy history and workflow rules
├── .python-version               # exact development interpreter
├── pyproject.toml
├── requirements*.txt             # portable top-level dependency inputs
└── requirements.lock             # macOS arm64 development snapshot
```

## 🧭 Development gates

Before changing the agent or submitting a new revision:

1. Run `python -m pytest -q`.
2. Complete at least one 720-state match against `starter` and `random`.
3. Rebuild the archive and confirm that it contains exactly `main.py`, the
   Apache-2.0 text, and the third-party notice.
4. Distinguish exact replay, open-loop counterfactual, closed-loop evaluation,
   remote validation, and leaderboard scoring.
5. Stage only explicit paths and keep secrets and generated artifacts out of
   every commit.

Repository-specific contribution rules live in [`AGENTS.md`](AGENTS.md). Its
Git constraints are pinned to
[`COK-ZhangZiliang/Git-Rules@ae0e80b`](https://github.com/COK-ZhangZiliang/Git-Rules/blob/ae0e80bb4a18a40c60ca514f0ce9d8f2a4c338af/README.md).

---

<div align="center">
  Route on public demand, then measure what actually holds. 🌱
</div>

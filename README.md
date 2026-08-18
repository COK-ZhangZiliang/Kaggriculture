<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  <br />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Kaggle Environment](https://img.shields.io/badge/Kaggle-Environment-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/kaggriculture)
  [![Tests](https://img.shields.io/badge/tests-59%20passing-2ea44f?logo=pytest&logoColor=white)](#-verified-current-strategy)
  [![Submission status](https://img.shields.io/badge/V6%20submission-COMPLETE-2ea44f?logo=kaggle&logoColor=white)](#-submission)
  [![Policy](https://img.shields.io/badge/policy-V6%20behavior%20router-7B61FF)](#-strategy)

  **A deterministic behavior-routed farm agent for Kaggle's 720-state economic simulation.**
</div>

## 🌾 Overview

This repository contains a self-contained V6 agent for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
It keeps V5 as the default two-expert policy and adds one conservative
step-72 behavior gate for a recurrent public failure cluster:

```text
shared opening through step 167
  ├─ exact public 2C/2S farm shape + BAKERY/PIZZA → counter expert
  └─ otherwise, public shops at step 168
       ├─ low expert  → terminal 10 cows / 4 sheep
       └─ high expert → terminal 6 cows / 8 sheep
```

The policy uses gameplay observations only. It does not route on episode ID,
opponent or team identity, submission ID, or random seed. The Kaggle entrypoint
is [`main.py`](main.py); it has no runtime dependency on the rest of this
repository and returns only JSON-safe actions.

## 🧠 Strategy

V6 combines three deterministic public-replay consensus routes with
failure-driven execution and market repair:

- each seat keeps independent state, accumulates `unlocked_shops` through step
  168, and makes sticky behavior and shop-route decisions;
- at step 72, the counter expert is enabled only when the opponent publicly
  shows exactly `$49`, no hands, 2 cows, 2 sheep, 12 melon plants, 7 wheat
  plants, and 5 pasture tiles, and the first shop is `BAKERY` or
  `PIZZA_SHOP`;
- a repeated first-two-shop prefix cancels the counter expert and falls back to
  the V5 route selector;
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

The three route tapes were reconstructed by component-wise majority from public
opponent behavior, then normalized, serialized, and compressed. Public
Notebooks were also used as mechanism references and hash-pinned evaluation
opponents; that does not establish that a replay participant ran a particular
Notebook artifact. Attribution and this boundary are recorded in
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). The detailed strategy and
evidence protocol are in [`docs/v6-strategy.md`](docs/v6-strategy.md).

## ✅ Verified current strategy

The current `main.py` SHA-256 is
`888115e1a4c48a52f28eeac60ce6fb8ede5dd67db360fee5df004ffa0613885e`.
It passed 59 automated tests. With `kaggle-environments==1.32.7`, starter and
random both-seat smoke matches each completed 720 states with `DONE/DONE` and
no stderr.

The captured 97-game public replay panel improved from 73 V5 wins to 78 V6
wins and raised mean margin from `+5252.247` to `+5834.186`, while retaining
all 73 historical win outcomes. The current candidate also completed 96/96
wins in the 16-seed both-seat panel against the three still-available
hash-pinned public artifacts:

| Frozen panel | Games | V6 W-L | Mean margin | Worst margin |
|:---|---:|---:|---:|---:|
| Existing three-opponent panel | 96 | **96-0** | +3,793.573 | +181 |
| Fresh three-opponent panel | 48 | **47-1** | +3,301.125 | -448 |

The fresh-panel loss was also V5's only loss on those rows; V6 improved mean
margin by `+763.063`. Kaito v27 was unavailable for the V6 rerun, so the
current claim is deliberately limited to the three hash-pinned artifacts.
Exact hashes, seeds, aggregates, and claim limits are recorded in
[`docs/evidence/v6-failure-analysis.json`](docs/evidence/v6-failure-analysis.json).

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

V6 submission `55596752`, message `v6 behavior-routed counter 2ba26b7`,
reached `COMPLETE`. The uploaded `main.py` maps to public Git commit
[`2ba26b7`](https://github.com/COK-ZhangZiliang/Kaggriculture/commit/2ba26b7ff3bc6df55000625df248c91f531c00d3).
The reviewed 44,336-byte archive has SHA-256
`e9dbd91bcd7b3ce1d98d29ed7e331d43432e9c3fef450797d5996d5fd063b64f`.

Kaggle reported an initial public score of **600.0** at
`2026-08-18T08:50:00.573Z`. Immediately before upload, the dynamic V5
submission score was **2730.6**. The latest observed V6 score was **909.1** at
`2026-08-18T09:06:26Z`. Simulation ratings change as episodes are played, so
these values are delivery snapshots rather than strength estimates or final
ranks.

The packaging script keeps the executable self-contained and carries the
applicable notice and license:

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
├── docs/v6-strategy.md           # current strategy and evidence boundary
├── docs/evidence/v6-failure-analysis.json
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

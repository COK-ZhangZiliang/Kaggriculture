<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  <br />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Kaggle Environment](https://img.shields.io/badge/Kaggle-Environment-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/kaggriculture)
  [![Tests](https://img.shields.io/badge/tests-61%20passing-2ea44f?logo=pytest&logoColor=white)](#-verified-current-strategy)
  [![Submission status](https://img.shields.io/badge/V7%20submission-COMPLETE-2ea44f?logo=kaggle&logoColor=white)](#-submission)
  [![Policy](https://img.shields.io/badge/policy-V7%20five--route-7B61FF)](#-strategy)

  **A deterministic public-demand-routed farm agent for Kaggle's 720-state economic simulation.**
</div>

## 🌾 Overview

This repository contains the self-contained V7 agent for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
V7 promotes five observable public-shop routes and retains the V6 recovery
controller. Route selection uses only the opponent's visible gameplay state;
it does not use identity, episode ID, submission ID, or random seed.

```text
public shop prefix
  ├─ first shop is YARN_STORE          → first-Yarn 6C/12S route
  ├─ first two shops end in YARN_STORE → second-Yarn 6C/12S route
  ├─ first three shops include Yarn    → 6C/8S route
  ├─ early milk-support signal         → 10C/4S route
  └─ otherwise                         → 8C/6S route
```

The Kaggle entrypoint is [`main.py`](main.py). It is self-contained, returns
JSON-safe actions, and has no runtime dependency on the rest of this repository.

## 🧠 Strategy

- A per-seat observable-state selector is re-evaluated as the public shop
  prefix unlocks. The exact first/second/third Yarn cases choose the
  corresponding majority route; an early milk-support signal can choose the
  low 10C/4S route; the default is 8C/6S. The legacy-opening decision is the
  sticky part of routing.
- A step-24–71 legacy-opening gate recognizes the older public opening shape
  and selects its matching legacy tape. This is a state-based compatibility
  path, not an opponent or episode identity rule.
- All five current and five legacy tapes are modified, normalized, compressed
  route data derived from the Apache-2.0 artifact documented in
  [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). The selector and runtime
  execution controller are independently maintained in this repository.
- V6 execution controls remain active: day-boundary weed recovery, observable
  cow-placement and purchase reconciliation, seed-prefix feasibility, bounded
  premium prepayment/repayment, executable same-turn SELL ranking, terminal
  seed pruning, retry-safe per-seat action caching, and malformed-observation
  protection.
- Every action is hand-aligned, market orders are capped at 10, and terminal
  liquidation is scheduled from the route tape.

## ✅ Verified current strategy

The frozen V7 `main.py` SHA-256 is
`7ce060d8551cf3e7a20a800c1eea2e18ece63d6d6eab8e21199b65f9b78e4794`.
The repository has 61 passing tests. With
`kaggle-environments==1.32.7`, starter and random both-seat smoke matches each
completed 720 states with `DONE/DONE` and no stderr.

The V7 analysis snapshot observed online V6 at score **2416.6** at
`2026-08-20T04:01:34Z`; V5 was **2665.5** at the same retrieval. The leaderboard
CSV captured at `2026-08-20T04:04:51Z` placed our team at rank
74/5446 with score 2665.5. These are dynamic simulation snapshots, not fixed
strength estimates. The CSV archive SHA-256 is
`dfc3e51ee9f924b89a6ab988768102e695ee5fc0e509a775dd56ef0c948cd61c`.

Against 126 captured V6 public games, V7 scored 99 wins and 27 losses, mean
margin `+7401.508`, median `+3409.5`, and worst margin `-25432`; it improved
72 rows and regressed 54. All games reached `DONE/DONE`. This is an open-loop
counterfactual diagnostic, not a closed-loop leaderboard result.

The frozen fresh closed-loop panel used engine 1.32.7, eight previously unused
seeds, both seats, and 16 games per opponent:

| Opponent artifact | Games | V7 W-L | Mean margin | Worst margin |
|:---|---:|---:|---:|---:|
| latest Tetsu adaptive | 16 | **16-0** | +3345.750 | +1584 |
| Tetsu town | 16 | **16-0** | +3262.125 | +1556 |
| V6 | 16 | 11-5 | +532.250 | -14727 |
| V17 | 16 | 13-3 | +291.438 | -25819 |
| **Total** | **64** | **56-8** | — | — |

Every fresh-panel match completed 720 states with `DONE/DONE` and no stderr.
An older 96-game panel was 65-31 for the pre-final V7 behavior candidate versus
96-0 for V6; it is retained as an explicit regression boundary and is not
misrepresented as a final-hash rerun. Exact hashes, seeds, raw artifact hashes,
and claim limits are recorded in
[`docs/evidence/v7-failure-analysis.json`](docs/evidence/v7-failure-analysis.json)
and [`docs/v7-strategy.md`](docs/v7-strategy.md).

## 🚜 Quick start

Prerequisites: Git, CPython 3.12.13, and a POSIX-like shell. The exact Python
version is recorded in [`.python-version`](.python-version).

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python -m pip check
python -m pytest -q
```

Run full matches and write ignored replays:

```bash
python scripts/run_local_match.py --opponent starter --seed 20260805
python scripts/run_local_match.py --opponent random --seed 20260805 --player 1
```

Build and inspect the minimal Kaggle archive:

```bash
python scripts/package_submission.py
tar -tzf dist/submission.tar.gz
```

## 📦 Submission

V7 submission `55638354`, message `v7 public-shop five-route 77c271f`, reached
`COMPLETE`. The uploaded `main.py` maps to public Git commit
[`77c271f`](https://github.com/COK-ZhangZiliang/Kaggriculture/commit/77c271f600b09b2dc070bc6b406240356bcb5616).

The reviewed archive is 99,523 bytes with SHA-256
`03c99a672bee741591d7224781865efd20cb3a26ea775193eadade4ac28f5c4a`.
Kaggle recorded the submission at `2026-08-20T04:56:38.653Z`; validation was
observed complete at `2026-08-20T05:02:19Z` with an initial public score of
**600.0**. At that observation V6 was **2417.7** and V5 was **2656.4**. All
scores are dynamic delivery snapshots, not final strength estimates. V7 was
later observed at **681.7** on `2026-08-20T05:05:16Z`.

The package contains only the self-contained entrypoint and the applicable
Apache attribution files:

```text
submission.tar.gz
├── main.py
├── LICENSE-APACHE-2.0.txt
└── THIRD_PARTY_NOTICES.txt
```

## 🗂️ Project layout

```text
.
├── main.py                       # self-contained V7 Kaggle agent
├── scripts/                      # local evaluation and packaging utilities
├── docs/v7-strategy.md           # current strategy and evidence boundary
├── docs/evidence/v7-failure-analysis.json
├── tests/                        # unit and environment smoke tests
├── THIRD_PARTY_NOTICES.md        # route provenance and modifications
├── AGENTS.md                     # strategy history and workflow rules
└── requirements*.txt             # portable dependency inputs and lockfile
```

## 🧭 Development gates

Before changing the agent or submitting a new revision:

1. Run `python -m pip check` and `python -m pytest -q`.
2. Complete 720-state starter and random matches.
3. Rebuild the archive and verify its exact contents and hash.
4. Distinguish replay reproduction, open-loop diagnostics, closed-loop local
   evaluation, remote validation, and leaderboard scoring.
5. Stage only explicit paths and keep secrets and generated artifacts out of
   every commit.

Repository-specific contribution and delivery rules live in
[`AGENTS.md`](AGENTS.md).

---

<div align="center">
  Route on public demand, then measure what actually holds. 🌱
</div>

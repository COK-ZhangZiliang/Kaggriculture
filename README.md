<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  <br />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Kaggle Environment](https://img.shields.io/badge/Kaggle-Environment-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/kaggriculture)
  [![Tests](https://img.shields.io/badge/tests-40%20passing-2ea44f?logo=pytest&logoColor=white)](#-verified-current-strategy)
  [![Submission status](https://img.shields.io/badge/V4%20submission-COMPLETE-2ea44f?logo=kaggle&logoColor=white)](#-submission)
  [![Policy](https://img.shields.io/badge/policy-10C%2F4S%20%7C%206C%2F8S-7B61FF)](#-strategy)

  **A deterministic demand-routed farm agent for Kaggle's 720-state economic simulation.**
</div>

## 🌾 Overview

This repository contains a self-contained agent for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
The current V4 policy shares one opening route, observes the public town
shop sequence, and freezes one of two production experts at step 168:

```text
shared opening through step 167
  ├─ low expert  → terminal 10 cows / 4 sheep
  └─ high expert → terminal 6 cows / 8 sheep
                     (12 sheep requested and placed cumulatively)
```

The policy uses public observations only. It does not route on episode ID,
opponent or team identity, submission ID, or random seed. The Kaggle entrypoint
is [`main.py`](main.py); it has no runtime dependency on the rest of this
repository and returns only JSON-safe actions.

## 🧠 Strategy

V4 combines a deterministic two-expert production tape with bounded execution
and market repair:

- each seat keeps independent state, accumulates `unlocked_shops` through step
  168, then makes a sticky route decision;
- any observed `YARN_STORE` selects the high expert, except when the first two
  shops are exactly `ICE_CREAM_SHOP`, `YARN_STORE`, which selects the low
  expert because that early mix is milk-dominated;
- the low expert requests, places, and finishes with 10 cows and 4 sheep;
- the high expert requests and places 6 cows and 12 sheep over the full tape;
  four sheep leave or are replaced during the lifecycle, and verified terminal
  smokes finish at the stable 6-cow/8-sheep herd;
- visible weeds, displaced cow carriers, first-day seed surplus, and partial
  cow purchases are repaired from observable state without changing the chosen
  route target;
- scheduled premium sales retain quantity-conserving one-turn and guarded
  seven-turn leads, with exact repayment at the original sale step;
- every action is hand-aligned, market orders remain capped at 10, and a
  malformed observation falls back to JSON-safe `PASS` actions.

The route tapes were reconstructed by component-wise majority from public
opponent behavior, then normalized, serialized, and compressed. Public
Notebooks were also used as mechanism references and hash-pinned evaluation
opponents; that does not establish that a replay participant ran a particular
Notebook artifact. Attribution and this boundary are recorded in
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). The detailed strategy and
evidence protocol are in [`docs/v4-strategy.md`](docs/v4-strategy.md).

## ✅ Verified current strategy

The current `main.py` SHA-256 is
`ff50c792a8e2dbe23c8b9855cfe63074885a22ea381883af463012513a956f70`.
It passed 40 automated tests. With `kaggle-environments==1.32.6`, the low-route
smoke completed 720 states and `DONE/DONE` at 157,958–3,453; both-seat
high-route smokes completed 720 states and `DONE/DONE` at 189,557–3,455 and
189,791–3,470. Those smokes also checked aligned hands and the 10-order market
cap.

The final-hash closed-loop paired panel used 16 seeds absent from the opened
development panel, four hash-pinned public policies, and both candidate seats.
Every game reached 720 states and `DONE/DONE` without captured stderr:

| Frozen opponent artifact | Games | V4 W-L | Mean margin | Worst margin |
|:---|---:|---:|---:|---:|
| Kaito v27 | 32 | **32-0** | +13,430.781 | +1,128 |
| V17 | 32 | **30-2** | +5,142.688 | -123 |
| Public MoE | 32 | **22-10** | +974.438 | -1,688 |
| Tetsu adaptive | 32 | **17-15** | -428.219 | -11,870 |
| **Overall** | **128** | **101-27** | **+4,779.922** | **-11,870** |

On the same 128 paired games, V3C went 45-83 with mean margin -3,982.281.
V4 gained 56 net wins and improved mean margin by 8,762.203, but regressed on
28 paired normalized margins. It therefore **failed** the strict all-wins and
positive-mean-versus-every-opponent gates; this result is evidence of a large
panel improvement, not a sweep or a leaderboard prediction. The evaluation
artifact does not record its engine version, so none is claimed for this panel.

Two additional diagnostics have narrower meanings:

- all 111 captured V3C public losses were first reproduced exactly under their
  recorded engine versions (`1.32.6`: 41; `1.32.7`: 70), with zero action,
  observation, reward, or status mismatches;
- final V4 won 97/111 fixed-loss tapes and improved 110/111 normalized margins,
  but the opponent actions were frozen, so this is open-loop counterfactual
  evidence rather than a policy rematch;
- a pre-frozen 32-game public-win control retained only 27 wins and lost five,
  so the preservation gate failed. This control also fixes opponent actions and
  must not be described as a closed-loop holdout.

The opened development panels evaluated pre-final candidate SHA-256
`38838d46bf435fed98c1892ca32982f1a3f59816ff5a1be985710a16b1324f96`
(51/64 on the paired panel and 76/80 on the legacy strong panel). They informed
development but are not evidence for the final hash. Exact hashes, seeds,
failure episode IDs, aggregates, and claim limits are recorded in
[`docs/evidence/v4-failure-analysis.json`](docs/evidence/v4-failure-analysis.json).

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

V4 submission `55569567`, message `v4 demand-routed mixed farm ea61ae0`,
reached `COMPLETE`. The uploaded `main.py` maps to public Git commit
[`ea61ae0`](https://github.com/COK-ZhangZiliang/Kaggriculture/commit/ea61ae044eb481b145ca9741df552e7dd1f0b422).
The reviewed three-file archive is 31,624 bytes with SHA-256
`796b1b29abf0b53186b3e3c56a6c19bbb5d47d06e6e98533c05531a11a634a8c`.

Kaggle reported an initial public score of **600.0** at
`2026-08-17T03:35:34Z`. New simulation agents commonly begin at this starting
snapshot before accumulating public episodes, so it is a delivery observation,
not a V4 strength estimate or final-rank claim. The packaging script keeps the
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
├── docs/v4-strategy.md           # current strategy and evidence boundary
├── docs/evidence/v4-failure-analysis.json
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

<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  <br />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Kaggle Environment](https://img.shields.io/badge/Kaggle-Environment-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/kaggriculture)
  [![Tests](https://img.shields.io/badge/tests-passing-2ea44f?logo=pytest&logoColor=white)](#-verified-current-strategy)
  [![Submission status](https://img.shields.io/badge/Kaggle%20submission-COMPLETE-20BEFF?logo=kaggle&logoColor=white)](#-submission)
  [![Policy](https://img.shields.io/badge/policy-adaptive%208C%2F4S-7B61FF)](#-strategy)

  **A deterministic mixed-farm agent for Kaggle's 720-state economic simulation.**
</div>

## 🌾 Overview

This repository contains a self-contained agent for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
The current local agent runs an 8-cow/4-sheep mixed-farm route with bounded
state repair and market timing selected from public observations. It combines
high-throughput production, quantity-conserving sale leads, both-seat
evaluation, and a reproducible archive.

```text
8 cow + 4 sheep + wheat / melon / strawberry route
  → repair visible weeds and displaced cow placement
  → move scheduled sales one turn early without changing total quantity
  → confirm H4 market opponents from public farm and inventory changes
  → counter confirmed premium preemption one additional turn early
```

The Kaggle entrypoint is [`main.py`](main.py). It has no runtime dependency on
the rest of this repository and returns only JSON-safe actions.

## 🧠 Strategy

The policy runs a diversified crop-and-livestock supply chain:

- hires five workers, expands to three quadrants, and reaches eight cows and
  four sheep while sustaining wheat, melon, and strawberry production;
- repairs visible weeds that block scheduled planting or pasture construction;
- realigns a cow carrier to an adjacent empty pasture during the expansion
  window, then resumes the frozen route;
- advances every scheduled product sale by one turn when stock is available
  and deterministic town demand does not erase the queue advantage;
- subtracts every advanced quantity from the original next-turn sale, so the
  two-turn planned quantity is conserved;
- detects near-mirror production from public farms and attributes premium
  market inventory changes after accounting for our sale and town demand;
- activates the second-order premium counter only after those observations
  confirm an opponent that is already preempting the public sale schedule.

The long-horizon route and premium reference schedule come from public Kaggle
Notebooks; the combined controller and repository verification were adapted
here. Attribution and changes
are recorded in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md), and the
full current evidence boundary is in
[`docs/v3b-strategy.md`](docs/v3b-strategy.md).

## ✅ Verified current strategy

The frozen strong-agent gate used Python 3.12,
`kaggle-environments==1.32.6`, deterministic unseen seeds, both candidate
seats, 720 recorded states, and required every individual game to be a win.

| Frozen opponent | Seeds | Games | Result | Mean margin |
|---|---:|---:|---:|---:|
| R5A 8C/4S | 16 | 32 | **32-0-0** | +1,524.781 |
| Kaito v27 | 8 | 16 | **16-0-0** | +19,665.688 |
| Breaking Tie | 8 | 16 | **16-0-0** | +1,077.000 |
| Adaptive | 8 | 16 | **16-0-0** | +6,642.625 |

All 80 games ended `DONE/DONE` without captured stderr. The narrowest winning
margin was +65, so the closest matchup remains sensitive. Exact opponent
hashes, seeds, per-game rows, and claim limits are recorded in
[`docs/evidence/v3b-strong-holdout.json`](docs/evidence/v3b-strong-holdout.json).
This proves a sweep only against these exact frozen artifacts on this panel; it
does not imply universal dominance or a public leaderboard score.

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

When dependency inputs change, refresh `requirements.lock` only from a clean
environment matching the platform scope in its header and rerun the verification
gates.

Run a full match and write an ignored replay:

```bash
python scripts/run_local_match.py --opponent starter --seed 20260805
python scripts/run_local_match.py --opponent random --seed 20260805 --player 1
```

Run a both-seat league against external public-agent files without committing
those files:

```bash
python scripts/run_league.py \
  --opponent kaito=/absolute/path/to/kaito.py \
  --opponent rayk=/absolute/path/to/rayk.py \
  --seed 20260811 --seed 20260829 \
  --require-all-wins \
  --output runs/eval/v3b-holdout.json
```

Build the minimal Kaggle archive and inspect its contents:

```bash
python scripts/package_submission.py
tar -tzf dist/submission.tar.gz
```

## 📦 Submission

Latest confirmed online delivery (V2):

| Delivery evidence | Value |
|:---|:---|
| Submission ID | `55292510` |
| Kaggle API timestamp | `2026-08-06T07:36:04.577000` |
| Message | `v2 market-aware mixed-farm route c587ec5` |
| Remote status | `COMPLETE` |
| Public score snapshot | **1,531.5** · verified `2026-08-13T13:26Z` |
| Matching code commit | [`c587ec5`](https://github.com/COK-ZhangZiliang/Kaggriculture/commit/c587ec54eb5e46e560f21797507b1e759ba7ccf6) |
| V2 online archive | 17,814 bytes · SHA256 `3967ea31aa2da69e0be8b5af0dc07b70d9f5f5384c3f8a1ae74ffa12173ca3ef` |
| V2 online `main.py` | 24,339 bytes · SHA256 `8d419acf65749692682698b1ac0091942b22f2b67c94a9a8cf90c3dbc3418c38` |
| Archive members | Three root-level files: `main.py`, Apache-2.0 text, notice |

The score above is a dynamic timestamped snapshot of the latest confirmed
online delivery, not a V3B result. The online archive and linked V2 commit have
the same `main.py` SHA256.

Current local V3B candidate:

| Local evidence | Value |
|:---|:---|
| Kaggle status | Not uploaded |
| Git status | Not committed or pushed |
| Strong-agent gate | 80/80 wins across four hash-pinned artifacts |
| Verification | 27 tests passed; starter/random gates passed |
| Performance | 719 calls · mean 0.097 ms · p99 0.288 ms · max 0.355 ms |
| `main.py` | 36,071 bytes · SHA256 `257d74f613f80607fba6fa68482e9db1eb07cb98618add47d45415b4f9079f54` |
| Archive | 20,223 bytes · SHA256 `b60f48ab876480c850821398ea52486ffc7e7da1a67faba657cbd665de1d67e0` |

The packaging script creates a deterministic archive whose executable remains
self-contained. The license and notice travel with the third-party route:

```text
submission.tar.gz
├── main.py
├── LICENSE-APACHE-2.0.txt
└── THIRD_PARTY_NOTICES.txt
```

Generated archives, replays, credentials, datasets, caches, and virtual
environments are ignored by Git. Configure Kaggle authentication outside the
repository, then submit the reviewed archive with the official CLI.

## 🗂️ Project layout

```text
.
├── main.py                       # self-contained Kaggle agent
├── scripts/
│   ├── package_submission.py     # build and verify the archive
│   ├── run_local_match.py        # run a 720-state local episode
│   └── run_league.py             # both-seat file-agent league
├── docs/v3b-strategy.md          # current strategy and evidence boundary
├── tests/                        # unit and environment smoke tests
├── assets/logo.svg               # project wordmark
├── LICENSES/Apache-2.0.txt       # third-party license copy
├── THIRD_PARTY_NOTICES.md        # route provenance and modifications
├── AGENTS.md                     # repository and Git workflow rules
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
4. Distinguish local completion, remote validation, and leaderboard scoring.
5. Stage only explicit paths and keep secrets and generated artifacts out of
   every commit.

Repository-specific contribution rules live in [`AGENTS.md`](AGENTS.md). Its
Git constraints are pinned to
[`COK-ZhangZiliang/Git-Rules@ae0e80b`](https://github.com/COK-ZhangZiliang/Git-Rules/blob/ae0e80bb4a18a40c60ca514f0ce9d8f2a4c338af/README.md).

---

<div align="center">
  Built to make the first valid move, then improve from evidence. 🌱
</div>

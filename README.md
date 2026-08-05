<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  <br />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Kaggle Environment](https://img.shields.io/badge/Kaggle-Environment-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/kaggriculture)
  [![Tests](https://img.shields.io/badge/tests-12%20passed-2ea44f?logo=pytest&logoColor=white)](#-verified-baseline)
  [![Policy](https://img.shields.io/badge/policy-deterministic-7B61FF)](#-strategy)

  **A small, reproducible first baseline for Kaggle's 720-state farming simulation.**
</div>

## 🌾 Overview

This repository contains a self-contained agent for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
The first milestone favors reliability over complexity: one deterministic
carrot-production policy, a repeatable local match runner, environment-level
tests, and a minimal submission archive.

```text
observe farm → assign one row per unit → water / harvest / dig / plant
             → sell produce and replenish seeds → liquidate on the final day
```

The Kaggle entrypoint is [`main.py`](main.py). It has no runtime dependency on
the rest of this repository and returns only JSON-safe actions.

## 🧠 Strategy

The baseline turns the north-west 5×5 unlocked area into a carrot field:

- hires four hands at the beginning of each day;
- assigns the farmer and hands to separate rows to avoid collisions;
- prioritizes peak-day watering, harvesting, weed removal, and replanting;
- reserves seeds locally so simultaneous `PLANT` actions remain valid;
- sells shed inventory throughout the season;
- stops planting before the end and returns carried produce to the shed for
  final liquidation.

This is intentionally a baseline, not a claim of leaderboard optimality. Its
purpose is to establish a valid, inspectable end-to-end path before search,
mixed-crop planning, opponent modeling, or learned policies are added.

## ✅ Verified baseline

Local verification used Python 3.12, `kaggle-environments==1.32.4`, 720 recorded
states, and fixed environment seeds.

| Side | Opponent | Seed | Example reward snapshot | Result |
|:---:|:---|---:|:---:|:---:|
| P0 | `starter` | 20260805 | **10,032** – 3,175 | Win |
| P1 | `starter` | 20260806 | 3,184 – **10,300** | Win |
| P0 | `random` | 20260805 | **9,924** – 50 | Win |
| P1 | `random` | 20260806 | 0 – **10,132** | Win |
| P0 | `pass` | 20260807 | **9,436** – 3,000 | Win |

The baseline is deterministic; the built-in `random` opponent is not, so those
two reward snapshots can vary between runs. The automated suite currently
contains twelve passing tests, including function-based and Kaggle file-loader
full-episode checks, terminal-inventory assertions, and reproducible archive
metadata checks. These results are local evidence only; they do not imply a
public leaderboard score.

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

Build the minimal Kaggle archive and inspect its contents:

```bash
python scripts/package_submission.py
tar -tzf dist/submission.tar.gz
```

## 📦 Submission

The packaging script creates `dist/submission.tar.gz` with exactly one member:

```text
submission.tar.gz
└── main.py
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
│   └── run_local_match.py        # run a 720-state local episode
├── tests/                        # unit and environment smoke tests
├── assets/logo.svg               # project wordmark
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
3. Rebuild the archive and confirm that it contains only `main.py`.
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

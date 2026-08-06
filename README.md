<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  <br />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Kaggle Environment](https://img.shields.io/badge/Kaggle-Environment-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/kaggriculture)
  [![Tests](https://img.shields.io/badge/tests-18%20passed-2ea44f?logo=pytest&logoColor=white)](#-verified-v2)
  [![Submission status](https://img.shields.io/badge/Kaggle%20submission-COMPLETE-20BEFF?logo=kaggle&logoColor=white)](#-submission)
  [![Policy](https://img.shields.io/badge/policy-market--aware-7B61FF)](#-strategy)

  **A deterministic mixed-farm agent for Kaggle's 720-state economic simulation.**
</div>

## 🌾 Overview

This repository contains a self-contained agent for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
V2 combines a complete mixed-farm economic route with visible-state repair,
shared-market timing, both-seat evaluation, and a reproducible submission
archive.

```text
mixed herd + wheat / melon / strawberry route
  → align workers and repair visible weeds
  → project same-turn shed stock
  → order fragile-product sales against public opponent exposure
  → drop and liquidate reachable stock on step 718
```

The Kaggle entrypoint is [`main.py`](main.py). It has no runtime dependency on
the rest of this repository and returns only JSON-safe actions.

## 🧠 Strategy

The policy runs a diversified supply chain instead of a single carrot field:

- scales labor and unlocks three quadrants for a mixed cow/sheep herd;
- uses wheat for feed and liquidity, bounded melons for capital events, and
  strawberries for town-supported recurring production;
- repairs visible weeds only for the affected actor, then replays a bounded
  local route suffix;
- clips sales to projected shed inventory after same-turn field actions;
- detects sustained near-mirror farms and moves the next complete premium sale
  one turn earlier;
- orders existing sale blocks by opponent exposure and glut sensitivity;
- uses the last executable step, 718, for same-turn `DROP` then `SELL`.

The long-horizon route is derived from an Apache-2.0 public Kaggle Notebook;
the state controller was written for this repository. Attribution and changes
are recorded in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md), and the
full research and evidence boundary is in
[`docs/v2-strategy.md`](docs/v2-strategy.md).

## ✅ Verified V2

Local verification used Python 3.12, `kaggle-environments==1.32.4`, 720 recorded
states, and fixed environment seeds.

| Gate | Games | Result | Mean margin |
|---|---:|---:|---:|
| Original V1 vs five public policy artifacts | 20 | 0 wins | Large negative |
| V2 development observation vs Kaito v21.1 | 12 | 12 wins | +2,697.5 |
| V2 unopened holdout vs five public policy artifacts | 40 | **38 wins** | Positive for every opponent |
| V2 P0 vs `starter`, seed 20260805 | 1 | **195,948 – 3,497** | +192,451 |
| V2 P0 vs `random`, seed 20260805 | 1 | **196,806 – 0** | +196,806 |

The 40-game holdout used four previously unopened seeds, both seats, and exact
temporary files for Kaito v21.1, Rayk c27, a Subin/Savko composite, a structured
economic policy, and Bruce Route 1. All 40 games ended `DONE/DONE`. The built-in
`random` opponent is not reproducible, so its reward is only a smoke snapshot.
The immutable per-match rows, opponent hashes, source URLs, and exact candidate
SHA are in [`docs/evidence/v2-holdout.json`](docs/evidence/v2-holdout.json).
The development-ablation row guided candidate selection, but its original
per-match artifact was not retained and is not counted as release evidence.
The automated suite contains eighteen passing tests, including both-seat
Kaggle file loading, self-play symmetry, terminal inventory, and reproducible
archive checks. Local results do not imply a public leaderboard score.

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
  --require-positive-mean \
  --output runs/eval/v2-dev.json
```

Build the minimal Kaggle archive and inspect its contents:

```bash
python scripts/package_submission.py
tar -tzf dist/submission.tar.gz
```

## 📦 Submission

Baseline V1 completed Kaggle's remote submission pipeline. V2 has passed its
local gates and the exact reviewed archive is ready for upload.

| Delivery evidence | Value |
|:---|:---|
| Submission ID | `55268182` |
| Kaggle API timestamp | `2026-08-05T11:19:05.207000` |
| Message | `baseline-v1 deterministic carrot planner` |
| Remote status | `COMPLETE` |
| Public score snapshot | **471.3** · verified `2026-08-05T11:25:21Z` |
| Archive | 2,211 bytes · SHA256 `d3781fb452c1ec3c85579c9c22f8dac860c307c3d4b57701eaef796c58d9f448` |
| Matching code commit | [`ec8bdba`](https://github.com/COK-ZhangZiliang/Kaggriculture/commit/ec8bdba50701653e4c3b884cce65897e6fc68f3e) |

V2 pre-upload artifact:

| Delivery evidence | Value |
|:---|:---|
| Local status | 18 tests passed; required starter/random gates passed |
| Archive | 17,814 bytes · SHA256 `3967ea31aa2da69e0be8b5af0dc07b70d9f5f5384c3f8a1ae74ffa12173ca3ef` |
| Packed `main.py` | 24,339 bytes · SHA256 `8d419acf65749692682698b1ac0091942b22f2b67c94a9a8cf90c3dbc3418c38` |
| Archive members | Three root-level files: `main.py`, Apache-2.0 text, notice |
| Kaggle status | Not uploaded yet |

The score above is a timestamped Kaggle API snapshot and may continue changing
as simulation episodes are processed; it is not a claim about final rank or
private leaderboard performance. The archived `main.py` and the file in the
linked commit have the same SHA256.

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
├── docs/v2-strategy.md           # research, ablations, and claim boundaries
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

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
The current local V3C agent runs an 8-cow/4-sheep mixed-farm route with
failure-driven execution repair and market timing selected from public
observations. It combines high-throughput production, quantity-conserving sale
leads, both-seat evaluation, and a reproducible archive.

```text
8 cow + 4 sheep + wheat / melon / strawberry route
  → repair visible weeds and displaced cow placement
  → preserve day-boundary cash and reconcile partial cow purchases
  → move scheduled sales one turn early without changing total quantity
  → confirm H4 market opponents from public farm and inventory changes
  → prepay confirmed premium sales at H7, then subtract the exact route quantity
```

The Kaggle entrypoint is [`main.py`](main.py). It has no runtime dependency on
the rest of this repository and returns only JSON-safe actions.

## 🧠 Strategy

The policy runs a diversified crop-and-livestock supply chain:

- requests up to five opening workers, expands to three quadrants, and reaches
  eight cows and four sheep while sustaining wheat, melon, and strawberry
  production;
- repairs visible weeds that block scheduled planting or pasture construction;
- realigns a cow carrier to an adjacent empty pasture during the expansion
  window, then resumes the frozen route;
- clips only a provable first-day seed surplus and enlarges an existing later
  cow order only when an earlier per-unit purchase was partially filled;
- buys a ninth cow only when an opponent has publicly placed at least nine,
  at least three active shop instances demand milk, milk is at least 225, cash
  is at least 800, and the market queue has room;
- advances every scheduled product sale by one turn when stock is available
  and deterministic town demand does not erase the queue advantage;
- subtracts every advanced quantity from the original next-turn sale, so the
  two-turn planned quantity is conserved;
- detects near-mirror production from public farms and attributes premium
  market inventory changes after accounting for our sale and town demand;
- activates the second-order premium counter only after those observations
  confirm an opponent that is already preempting the public sale schedule;
- moves that sale seven turns ahead, records the prepaid quantity, prevents H1
  from selling it again, and repays the original sale exactly.

The long-horizon route and premium reference schedule come from public Kaggle
Notebooks; the combined controller and repository verification were adapted
here. Attribution and changes
are recorded in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md), and the
full current evidence boundary is in
[`docs/v3c-strategy.md`](docs/v3c-strategy.md).

## ✅ Verified current strategy

The final-hash holdout used Python 3.12, `kaggle-environments==1.32.6`, eight
fresh deterministic seeds absent from the V3B panel, both candidate seats,
720 recorded states, and required every individual game to be a win.

| Frozen opponent | Seeds | Games | Result | Mean margin | Worst margin |
|---|---:|---:|---:|---:|---:|
| R5A 8C/4S | 8 | 16 | **16-0-0** | +1,641.063 | +116 |
| Kaito v27 | 8 | 16 | **16-0-0** | +15,451.375 | +6,062 |
| Breaking Tie | 8 | 16 | **16-0-0** | +1,342.938 | +729 |
| Adaptive | 8 | 16 | **16-0-0** | +5,260.438 | +621 |

All 64 games ended `DONE/DONE` without captured stderr. The aggregate mean
margin was +5,923.953 and the narrowest win was +116. Exact opponent hashes,
seed derivation, the 17-loss analysis, and claim limits are recorded in
[`docs/evidence/v3c-failure-analysis.json`](docs/evidence/v3c-failure-analysis.json).
On the 17 historical loss tapes, V3C improved 9, left 8 unchanged, regressed
none, and flipped 3; that diagnostic holds opponent actions fixed and is not a
closed-loop rematch. The 64-game result proves a sweep only against these exact
frozen artifacts on this panel, not universal dominance or a leaderboard score.

The verified local `main.py` SHA-256 is
`d9e26d7e45a944dd4e46adc28f66f7d9ae5c6974e71755debe6b291029aa79e0`.
Its deterministic three-file archive is 21,348 bytes with SHA-256
`90c800d2d51705a8662ed5d33d60f2953180f192f8091f2ab20d4886b29d13ef`.

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
  --output runs/eval/v3c-holdout.json
```

Build the minimal Kaggle archive and inspect its contents:

```bash
python scripts/package_submission.py
tar -tzf dist/submission.tar.gz
```

## 📦 Submission

Current confirmed online delivery (V3C):

| Delivery evidence | Value |
|:---|:---|
| Submission ID | `55500863` |
| Kaggle API timestamp | `2026-08-14T07:51:42.500000` |
| Message | `v3c failure-driven h7 recovery 6aadc96` |
| Remote status | `COMPLETE` |
| Initial public score snapshot | **600.0** · verified `2026-08-14T07:54:14Z` |
| Matching code commit | [`6aadc96`](https://github.com/COK-ZhangZiliang/Kaggriculture/commit/6aadc968f3cb0e81839532ff7f1ec0499b061f81) |
| Online archive | 21,348 bytes · SHA256 `90c800d2d51705a8662ed5d33d60f2953180f192f8091f2ab20d4886b29d13ef` |
| Online `main.py` | 40,408 bytes · SHA256 `d9e26d7e45a944dd4e46adc28f66f7d9ae5c6974e71755debe6b291029aa79e0` |
| Archive members | Three root-level files: `main.py`, Apache-2.0 text, notice |

The score above is a dynamic snapshot and can change as public simulation
episodes are processed. It is not a final-rank or private
leaderboard claim. The uploaded `main.py` is traceable to code commit
`6aadc96`; the delivery evidence update is recorded in a subsequent docs-only
commit. Its local evidence is 38 passing tests, starter/random smoke gates,
and the 64/64 fresh strong-agent holdout described above.

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
│   ├── analyze_failure_replays.py # summarize ignored public replay files
│   ├── run_local_match.py        # run a 720-state local episode
│   └── run_league.py             # both-seat file-agent league
├── docs/v3c-strategy.md          # current strategy and evidence boundary
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

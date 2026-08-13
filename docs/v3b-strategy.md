# V3B Strategy and Evidence Boundary

## Scope

V3B replaces the V3A production tape with an 8 `COW` / 4 `SHEEP` route
reconstructed by majority vote from public episodes `92165990`, `92185587`,
and `92223213` of public submission `55440039`. Its controller adds:

- bounded visible-`WEED` repair and cow-placement realignment;
- a one-turn, quantity-conserving lead for every scheduled sellable product;
- public-farm near-mirror detection and market-inventory flow accounting;
- an evidence-gated second-order counter for opponents observed preempting
  premium sales four steps early;
- per-seat state and a fail-safe action for malformed observations.

The one-turn lead never invents stock. It sells at most currently available
shed inventory and removes exactly that moved quantity from the following
scheduled sale. The second-order counter activates only after public state and
premium inventory deltas jointly support the anti-market inference.

## Frozen local candidate

| Artifact | SHA-256 |
|---|---|
| V3B `main.py` | `257d74f613f80607fba6fa68482e9db1eb07cb98618add47d45415b4f9079f54` |
| R5A public artifact | `7f87c941af3050d0f21376f2843b324d7a06a1a8c050fa554cf07a769e5c937c` |
| Kaito v27 public artifact | `f48c21166eac68d1b05a401f04f94a2eb6154e65415af64893672365ff33c7b8` |
| Breaking Tie public artifact | `df4e899ad535754cf2ddbd3c16e48085916b0cd2baa5182a1a2cfc6a856abae5` |
| Adaptive public artifact | `026bb0126b5ff9c4decb78ce5c3cd296515dadf462e79046ec081b9d80f9757a` |

The frozen strong-agent gate used `kaggle-environments==1.32.6`, both candidate
seats, 720 recorded states, and required every individual game to be a win.
All games ended `DONE/DONE` without captured stderr.

| Opponent | Seeds | Games | W-T-L | Mean margin | Minimum margin |
|---|---:|---:|---:|---:|---:|
| R5A | 16 | 32 | **32-0-0** | +1,524.781 | +65 |
| Kaito v27 | 8 | 16 | **16-0-0** | +19,665.688 | +14,396 |
| Breaking Tie | 8 | 16 | **16-0-0** | +1,077.000 | +344 |
| Adaptive | 8 | 16 | **16-0-0** | +6,642.625 | +1,183 |

The 16 R5A seeds were deterministically derived from
`SHA256("V3B-HOLDOUT-2026-08-13:<index>")` and were not used in the earlier
H1/H5 development screen. The other three opponents used the first eight of
the same frozen seed list. The exact seed list and per-match rows are stored in
`docs/evidence/v3b-strong-holdout.json`.

This establishes a complete sweep of these four exact, hash-pinned public
artifacts on this fixed local panel. It does not prove dominance over every
possible agent, future public revision, hidden Kaggle opponent, or leaderboard
distribution, and it is not a Kaggle score.

## Verification

- repository environment: CPython 3.12.13 and `kaggle-environments==1.32.4`;
- strong-agent gate: `kaggle-environments==1.32.6`;
- `python -m pip check`: no broken requirements;
- `python -m pytest -q`: 27 passed;
- starter seed `20260805`: 720 states, `DONE/DONE`, 187,654-3,491;
- random seed `20260805`: 720 states, `DONE/DONE`, 196,415-0; the built-in
  random opponent is nondeterministic, so this is only a smoke snapshot;
- performance over 719 calls in the starter smoke: mean 0.097 ms, p99 0.288
  ms, maximum 0.355 ms;
- deterministic archive: 20,223 bytes, SHA-256
  `b60f48ab876480c850821398ea52486ffc7e7da1a67faba657cbd665de1d67e0`;
- archive members: root-level `main.py`, `LICENSE-APACHE-2.0.txt`, and
  `THIRD_PARTY_NOTICES.txt`;
- V3B has not been submitted to Kaggle or committed to GitHub. The latest
  confirmed online delivery remains V2 submission `55292510`.

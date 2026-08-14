# V3C Strategy and Evidence Boundary

## Scope

V3C is a failure-driven revision of the V3B 8-cow/4-sheep policy. It keeps
the frozen production route and changes only decisions supported by public or
private observation state:

- clips a surplus first-day seed purchase before it can consume the cash
  needed by the next day's first hire;
- enlarges an already-scheduled cow order when an earlier per-unit purchase
  was only partially filled, without buying beyond the route's eight-cow
  target;
- permits a ninth cow only when the opponent has publicly placed at least nine
  cows, at least three active shop instances demand milk, milk is at least
  225, cash is at least 800, and the existing market queue has room;
- moves confirmed anti-market sales seven turns ahead, records the prepaid
  quantity, prevents the ordinary one-turn lead from moving it a second time,
  and subtracts the exact quantity from the original route sale.

The policy never reads an episode ID, opponent name, submission ID, or random
seed. The offline analysis tool reports those fields only for reproducibility
and is not imported by `main.py`.

## Seventeen-loss snapshot

The development panel contains the 17 public losses observed for Kaggle
submission `55484203` in the captured 99-episode snapshot. All replays report
environment module `1.32.6`. Fixed-action replay reproduced every one of the
17 episodes with:

- 720 recorded states and `DONE/DONE`;
- zero action, observation, reward, and status mismatches;
- zero final-reward error.

This exact reproduction establishes that the downloaded tapes and local
interpreter match the recorded episodes. It does not make later
counterfactuals closed-loop rematches: the opponent continues to execute its
recorded action tape after the candidate changes the game state.

### Root-cause clusters

| Cluster | Games | Evidence | Decision |
|---|---:|---|---|
| 10C/4S throughput routes | 5 | Opponents spent roughly 13.4k-15.7k more but gained much larger melon, wheat, and milk revenue; copying a complete 10C route improved all 17 historical cases but failed 10 of 80 frozen strong games. | Do not replace or splice the full route. |
| 8C/4S market mirrors | 6 | Production was close; the existing H4/H5 counter activated in all six. A seven-turn, quantity-conserving counter improved all six fixed tapes and flipped three. | Promote guarded H7 prepayment and exact repayment. |
| 9C/4S milk routes | 2 | The extra cow was publicly visible before the existing step-289 purchase opportunity. | Keep a narrow public-state ROI gate. |
| Sheep-heavy routes | 3 | The decisive deficits were wool and, in the 8C/6S case, melon. V3B has no compatible spare worker/tile lifecycle for another sheep. | Leave unchanged pending a complete production route. |
| Cash-starved partial execution | 1 | Episode `92821605` bought one surplus wheat seed, missed the next-day hire, and later bought only one of two scheduled cows, ending at 7C/4S. | Clip only the provable seed surplus and reconcile later scheduled cow orders. |

Several tempting explanations were rejected:

- eight opening fifth-hire failures were harmless `PASS` padding; moving those
  hires earlier spent extra cash without adding productive actions;
- all 17 episodes ended with no sellable shed or carried stock, so terminal
  liquidation was not the cause;
- disabling the existing one-turn/meta market controller made the six mirror
  cases worse overall;
- an early ninth-cow transaction displaced melon production and worker cycles,
  left its first milk unharvested, and moved one target case from -13,090 with
  the guarded step-289 candidate to -37,186, a 24,096 margin regression, so it
  was discarded;
- a V3B-step-0/10C-step-1 tape splice was state-incompatible and failed all 17
  cases catastrophically.

## Fixed-tape counterfactual

The final `main.py` SHA-256 is
`d9e26d7e45a944dd4e46adc28f66f7d9ae5c6974e71755debe6b291029aa79e0`.
The deterministic three-file archive is 21,348 bytes with SHA-256
`90c800d2d51705a8662ed5d33d60f2953180f192f8091f2ab20d4886b29d13ef`.
Against the 17 fixed opponent tapes:

| Metric | V3B online result | V3C counterfactual |
|---|---:|---:|
| Wins | 0/17 | 3/17 |
| Mean margin | -6,419.235 | -5,458.882 |
| Improved / unchanged / regressed | - | 9 / 8 / 0 |
| Mean margin delta | - | +960.353 |

The three flips were episodes `92676812`, `92768720`, and `92778156`.
The largest improvement was `92821605`, from -19,248 to -12,706. These are
open-loop diagnostics, not a claim that the same online opponents would keep
their original actions in a rematch.

## Closed-loop strong-agent gates

The H7 implementation was first checked against the original frozen V3B panel:
80/80 live-policy wins, all 720 states and `DONE/DONE`, with a minimum margin
of +65. A separate post-failure holdout then used eight deterministically
derived seeds absent from the V3B panel, both seats, and the same four
hash-pinned public artifacts. The exact final-hash result is recorded in
`docs/evidence/v3c-failure-analysis.json`.

These panels test closed-loop policies, but they still cover four fixed public
artifacts rather than the complete Kaggle population. They do not prove
universal dominance or predict a leaderboard score.

## Kaggle delivery

The three-file archive was submitted as Kaggle submission `55500863` with
message `v3c failure-driven h7 recovery 6aadc96` and reached `COMPLETE`. Its
`main.py` maps to Git commit
`6aadc968f3cb0e81839532ff7f1ec0499b061f81`; the archive SHA-256 is
`90c800d2d51705a8662ed5d33d60f2953180f192f8091f2ab20d4886b29d13ef`.
The initial public score snapshot was 600.0 at `2026-08-14T07:54:14Z`; ratings
remain dynamic and this is not a final leaderboard claim.

## Reproduction

Summarize downloaded public replays without committing them:

```bash
python scripts/analyze_failure_replays.py /path/to/episode-*-replay.json
```

Run the regular repository gates:

```bash
python -m pip check
python -m pytest -q
python scripts/run_local_match.py --opponent starter --seed 20260805
python scripts/run_local_match.py --opponent random --seed 20260805
python scripts/package_submission.py
```

Replay files and full local experiment outputs remain ignored. The committed
evidence file contains only aggregate results, public episode identifiers,
hashes, seeds, and the evidence boundary needed to audit the claims above.

# V4 Strategy and Evidence Boundary

## Scope

V4 replaces the single production tape with a public-demand-routed pair of
experts while retaining bounded observable-state execution and market repair.
The final local candidate is `main.py` SHA-256
`ff50c792a8e2dbe23c8b9855cfe63074885a22ea381883af463012513a956f70`.

The policy never reads an episode ID, team or opponent name, submission ID, or
random seed. Each seat owns independent route and controller state. A step-0
observation or decreasing step counter resets that seat so state cannot leak
across episodes.

## Route construction

The two 719-action production tapes were reconstructed from opponent actions
visible in the 111 captured V3C public-loss replays:

- the low route is the component-wise majority of 61 opponents whose terminal
  farm had 10 cows and 4 sheep;
- the high route uses the low route through step 167, then the component-wise
  majority of nine opponents whose terminal farm had 6 cows and 8 sheep;
- farmer, each hand slot, and the complete market list were voted separately,
  normalized to JSON-safe actions, serialized, and compressed;
- the low and high action-array SHA-256 values, after canonical JSON
  serialization, are respectively
  `93daf1e051d2f394c50c08b59d0fd56d55bf0a5e8770e08701dbcacb91458518`
  and
  `a548603cf9cae2bda0bc016d50d574e072287ea68315b790b7341c99ab63a31c`.

This is a behavioral reconstruction from public action traces. It is not a
claim that every participant used the same source code, that a replay can be
bound to a particular public Notebook, or that the current leaderboard binary
has been recovered. The public V17 and public MoE artifacts were separately
downloaded, hash-pinned, inspected as mechanism references, and used as local
opponents. Their attribution and license information are in
[`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).

### Herd semantics

The low tape cumulatively requests and places 10 cows and 4 sheep and ends at
10C/4S. The high tape cumulatively requests and places 6 cows and 12 sheep.
Four sheep leave or are replaced during the tape lifecycle; verified terminal
smokes end at the stable 6C/8S herd. Accordingly, “6C/8S” describes the high
expert's terminal state, while “12 sheep” describes its cumulative requests
and placements. They are not interchangeable counts.

## Public-demand selector

Steps 0–167 are shared. Through step 168, the selector records the public
`town.unlocked_shops` sequence for the current seat. At step 168 it freezes:

| Observable shop state | Expert |
|:---|:---|
| Contains `YARN_STORE`, except the exact dominated prefix below | High 6C/8S |
| First two shops exactly `ICE_CREAM_SHOP`, `YARN_STORE` | Low 10C/4S |
| No `YARN_STORE` observed | Low 10C/4S |

The decision is sticky after step 168. The special low-route exception is
deliberately narrow: it covers the observed early ice-cream/yarn mix in which
the milk-heavy 10C/4S route was stronger, without routing on non-public
identity metadata.

## Shared controller

After selecting a tape, V4 applies the same bounded controller to both routes:

1. clip only first-day seed quantity that exceeds remaining same-day planting
   capacity;
2. dig a visible weed blocking scheduled planting or pasture construction and
   replay the interrupted action;
3. move a cow carrier to an adjacent empty pasture when a scheduled placement
   is visibly displaced, then resume the tape;
4. enlarge an existing scheduled cow purchase only when observable ownership
   is below that route's cumulative target;
5. advance eligible premium sales while reserving actor pickups and conserving
   the original two-turn quantity;
6. activate the longer H7 lead only from public market/farm evidence, record
   prepaid quantities, and subtract them from the original sale;
7. align hand actions to the observed workforce, cap market orders at 10, and
   return safe `PASS` actions for malformed observations.

The prior ninth-cow branch is disabled in V4. No off-tape animal purchase is
added by the selector.

## Failure corpus and exact baseline

The analysis snapshot contains all 111 captured public losses of V3C submission
`55500863` from the downloaded episode set. Forty-one replays record engine
`1.32.6` and 70 record `1.32.7`; each was executed only with its recorded
version. Reproduction produced:

- 111/111 episodes with 720 states and `DONE/DONE`;
- zero action, observation, reward, and status mismatches;
- zero maximum reward error;
- mean recorded online margin -6,115.739, median -3,515, and worst -33,114.

This exact baseline validates the downloaded tapes and the V3C artifact
identity. It is not a V4 result. The manifest SHA-256 is
`9b253411ce4b166cd9c6a50db86c05515e1f71cfa81a496bbae3da7fa358c767`.

## Fixed-action counterfactuals

### All 111 recorded losses

The final V4 hash was substituted for V3C while each opponent continued its
recorded action sequence:

| Metric | Recorded V3C loss | V4 fixed-tape counterfactual |
|:---|---:|---:|
| Wins | 0/111 | 97/111 |
| Mean margin | -6,115.739 | +8,033.757 |
| Median margin | -3,515 | +3,931 |
| Worst margin | -33,114 | -7,733 |
| Mean raw margin delta | — | +14,149.495 |
| Raw improved / regressed | — | 108 / 3 |
| Normalized improved / regressed | — | 110 / 1 |

All games reached 720 states and `DONE/DONE` without captured stderr. The two
version-partitioned result hashes are recorded in the evidence JSON.

This is an **open-loop opponent-tape counterfactual**, not a closed-loop policy
rematch and not a holdout. Candidate actions alter observations from the first
turn onward, but the opponent cannot react to the changed game because its
actions remain frozen.

### Pre-frozen public-win controls

Thirty-two V3C public wins were frozen before candidate evaluation, stratified
by engine, candidate seat, and online-margin rank. V4 retained 27 wins and lost
five:

| Episode | Engine | Seat | V4 margin |
|---:|:---:|---:|---:|
| `92943447` | `1.32.6` | 1 | -1,570 |
| `92957413` | `1.32.6` | 0 | -782 |
| `93122737` | `1.32.6` | 0 | -538 |
| `93517046` | `1.32.7` | 1 | -1,364 |
| `93678333` | `1.32.7` | 1 | -199 |

The aggregate mean V4 margin was +11,560.875, but the strict 32/32
preservation gate **failed**. This negative control was blind to candidate
outcomes at selection time, yet it still fixes opponent actions. It therefore
cannot be promoted to a closed-loop holdout or described as a pass.

## Opened development evidence

Two panels guided route and selector choices before the final freeze:

- the opened paired panel contains 64 paired games per candidate. Pre-final V4
  SHA-256 `38838d46bf435fed98c1892ca32982f1a3f59816ff5a1be985710a16b1324f96`
  went 51-13 with mean margin +4,896.953; V3C went 24-40 with mean margin
  -1,194.172;
- the opened legacy strong panel evaluated the same pre-final V4 hash for 80
  games and produced 76 wins, four losses, mean margin +14,310.863, and worst
  margin -549.

These artifacts do not evaluate the final `ff50c792…` file. Their seeds and
opponents were visible during development, and their artifacts do not record
an engine version. They are diagnostic and regression context only.

## Final-hash fresh closed-loop panel

After the final candidate freeze, 16 seeds absent from the opened development
panel were used against four hash-pinned public policies, both seats. The
artifact contains 256 rows: 128 for V3C and 128 for V4.

| Opponent | V4 games | V4 W-L | Mean margin | Worst margin |
|:---|---:|---:|---:|---:|
| Kaito v27 | 32 | 32-0 | +13,430.781 | +1,128 |
| V17 | 32 | 30-2 | +5,142.688 | -123 |
| Public MoE | 32 | 22-10 | +974.438 | -1,688 |
| Tetsu adaptive | 32 | 17-15 | -428.219 | -11,870 |
| **V4 overall** | **128** | **101-27** | **+4,779.922** | **-11,870** |
| **V3C overall** | **128** | **45-83** | **-3,982.281** | **-33,751** |

The paired mean margin delta was +8,762.203 and the paired mean normalized
delta was +0.099971. V4 improved 100 paired normalized margins and regressed
28; transitions were 60 loss-to-win, 41 win-to-win, 23 loss-to-loss, and four
win-to-loss. All rows contain 720 states, `DONE/DONE`, and no captured stderr.

This is the strongest final-hash local evidence and shows a large improvement
over V3C on this panel. It nevertheless **failed** the original strict gate:
V4 did not win all 128 games, Tetsu adaptive retained a negative mean margin,
and some paired cases regressed. The artifact binds all seeds and policy
hashes but does not record its engine version or seed-generation timestamp;
neither is inferred here. Hash-pinned public opponents also do not represent
hidden or future Kaggle policies.

## Local correctness gates

The final hash passed 40 automated tests. Under
`kaggle-environments==1.32.6`:

- a low-route seat-0 smoke at seed `20260805` ended 157,958–3,453;
- high-route smokes at seed `1220298539` ended 189,557–3,455 from seat 0 and
  189,791–3,470 from seat 1;
- all three matches recorded 720 states, `DONE/DONE`, aligned hands, and no
  market list longer than 10.

These smoke results validate route execution, not generalization.

## Delivery boundary

V4 submission `55569567`, message `v4 demand-routed mixed farm ea61ae0`,
reached `COMPLETE` and maps to public Git commit
`ea61ae044eb481b145ca9741df552e7dd1f0b422`. The reviewed 31,624-byte
three-file archive has SHA-256
`796b1b29abf0b53186b3e3c56a6c19bbb5d47d06e6e98533c05531a11a634a8c`.
Kaggle reported the new submission at the 600.0 starting snapshot at
`2026-08-17T03:35:34Z`; that initial value is not a strength estimate.

The V3C analysis baseline was 2,444.7 at rank 371 of 4,818 in the full official
snapshot retrieved at `2026-08-17T02:36:22Z`; ratings and ranks are dynamic.

## Reproduction

Run repository correctness and packaging gates:

```bash
python -m pip check
python -m pytest -q
python scripts/run_local_match.py --opponent starter --seed 20260805
python scripts/run_local_match.py --opponent random --seed 20260805
python scripts/package_submission.py
```

Replay files, public-agent downloads, and full local experiment outputs remain
ignored. The committed evidence file stores aggregate results, public episode
identifiers needed for the failed control gate, hashes, seeds, and explicit
claim limits without committing those large artifacts.

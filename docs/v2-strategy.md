# V2 strategy and evidence ledger

This document records what was learned from public high-scoring
Kaggriculture work, what was independently changed for V2, and which claims
are supported only by local evaluation. Scores are simulation ratings and can
move while agents continue playing, so every online value below is a
timestamped snapshot.

## Public implementation audit

The audit was refreshed with the official Kaggle CLI on 2026-08-06. A public
Notebook title, a replay reward, and a leaderboard rating are different forms
of evidence; they are not interchangeable.

| Evidence | Verified score boundary | Mechanisms reviewed |
|---|---:|---|
| [Kaito Fukami, v21.1 Conditional Memory](https://www.kaggle.com/code/kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory) | Public artifact hash was followed about three minutes later by submission `55288553`, then rated **2843.1**; strongest implementation-to-submission linkage found. The title's `177/180` is a local replay holdout, not a Kaggle score. | Complete economic route, identity-free public-state memory, order-only SELL intervention, actor-local weed recovery, step-718 liquidation. |
| [Bruce, High-Score Pipeline](https://www.kaggle.com/code/bruceqdu/my-2026-08-04-high-score-pipeline) | Bruce's team had an official **2819.9** submission, but the API does not expose a file hash tying that exact binary to the Notebook. | Stable replay route, visible-weed repair, terminal cashout. |
| [Rayk Kretzschmar, Zero to Top Meta](https://www.kaggle.com/code/raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta) | Author team **2542.3**; Notebook separately reports a hash-checked c14 at 2182.2. Exact current binary linkage is unproven. | Repeated-route selection, field/market channel separation, both-seat gates, clone-aware premium front-running. |
| [Roman Tamrazov, Hamburger](https://www.kaggle.com/code/romantamrazov/kaggriculture-hamburger) | Author team had **2420.1**, but that submission predates the current Notebook. A post-Notebook submission was only 1468.6, so Hamburger must not be labeled a verified 2420.1 binary. | Staged mixed herd, SELL-slot ordering, clone checkpoints, terminal relay during steps 716–718. |
| [Sai Teja Bandaru, Mega-Ensemble](https://www.kaggle.com/code/saitejabandaruin/kaggriculture-ultimate-mega-ensemble-3000) | Author team **2448.3**. The page's `3000+` title was not supported by the official rating. | Routing among public policies; treated as a research lead, not score evidence. |
| [Subin An public episode 89945750](https://www.kaggle.com/competitions/kaggriculture/leaderboard?dialog=episodes-episode-89945750) | Public replay from a team later shown at **2996.0**. The replay proves one 720-turn action trace and bank result, not the source of the current rated binary. | Twelve-hand, three-quadrant farm with eight cows, six sheep, wheat, strawberry, melon, and fertilizer sales. |

The public code was downloaded only to a temporary directory for inspection
and local opponents. Those files are not committed. V2 includes one
Apache-2.0 public route with explicit attribution; its controller was not
copied. The Kaggle tar carries both the Apache-2.0 text and the attribution
notice alongside its root-level `main.py`; see
[`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).

## What the high-score meta converged on

The strongest public families agree on a complete supply chain rather than a
single crop:

1. Build parallel labor early, then operate roughly twelve hands when the
   workload supports it.
2. Unlock the north-east and south-west quadrants; the south-east quadrant is
   usually too expensive for its remaining-season return.
3. Run a mixed herd, commonly converging near eight cows and five or six
   sheep, instead of entering a pure-milk mirror.
4. Use wheat as feed and liquidity, melons as a bounded capital event, and
   strawberries as the more town-supported expansion crop.
5. Treat the field route and market route as separate channels. Mature farms
   are similar; SELL timing increasingly determines head-to-head results.
6. Test both seats. Atomic orders and ordered market slots make one-seat
   evaluation unsafe.
7. Finish the route at step 718. Unit actions execute before market orders,
   so a unit already at shed access can `DROP` and the market can `SELL` that
   stock in the same final executable turn.

Official-engine probes add two important constraints. Matching SELL orders in
the same market slot receive the same pre-commit price; the edge appears only
when a fragile product is moved into an earlier slot. Melon town demand is
small and its glut curve reaches the one-dollar floor quickly, so the route
must limit melon exposure instead of filling every new quadrant with it.
Fertilizer does not make melon harvestable before its fixed first-yield day;
it is more useful on tomato or strawberry, or as a saleable by-product.

## V2 controller

V2 replaces the carrot-only planner with six coordinated layers:

```text
public mixed-farm route
  -> align actions to the observed worker count
  -> repair visible weeds for only the affected actor
  -> clip SELL quantities to projected same-turn shed stock
  -> detect a sustained public-farm mirror
  -> front-run the mirror's next premium block and order collision risk first
  -> drop and liquidate reachable stock on step 718
```

The economic route provides the long-horizon labor, movement, herd, land,
crop, feed, and harvest schedule. The runtime controller remains observation
aware:

- **Actor-local repair:** if a planned plant or structure meets a visible
  weed, that unit digs, retries the delayed action, and replays a bounded
  eight-step local suffix. Other units stay on schedule.
- **Projected stock ledger:** same-turn `DROP` and product `PLACE` actions are
  accounted for before the market. SELL requests are clipped to stock that
  can actually be in the shed.
- **Clone gate:** a premium front-run is enabled only after twelve consecutive
  observations with equal worker count, equal unlocked quadrants, and a crop,
  animal, and structure count distance of at most two.
- **One-turn premium front-run:** when the next route turn sells melon,
  strawberry, milk, or wool, the complete scheduled block is moved one turn
  earlier if it is already available. This is conditional; unconditional
  early selling failed the public ablations.
- **Collision ordering:** existing SELL blocks are ordered by visible opponent
  exposure, product glut sensitivity, current price, and quantity. It does not
  inspect private opponent inventory or identity.
- **Terminal ledger:** on step 718, reachable carried products are dropped and
  all projected shed products are sold, ordered by exposure-weighted value.

## Offline promotion evidence

All opponents below were loaded from exact temporary Python files and run in
`kaggle-environments==1.32.4`. Every seed was played from both seats. These are
live local matches, but most public opponents contain fixed route components;
the results are therefore a strong falsification gate, not a forecast of the
online rating.

The original V1 carrot agent first played two seeds from both seats against
five public policy artifacts: **0 wins in 20 games**. V1 ended near
11,000–14,000 coins; the public policies ended near 157,000–196,000 coins.

### Development observations against Kaito v21.1

These contemporaneous results guided candidate selection, but their original
per-match manifest was not retained. They are recorded as exploratory
observations, not as a reproducible release gate; the archived 40-game holdout
below is the promotion evidence.

| Candidate | Wins / 12 | Mean margin |
|---|---:|---:|
| Route + safety only | 0 / 12 | -4,331.3 |
| Collision ordering only | 2 / 12 | -1,383.3 |
| Quarter-batch clone front-run only | 0 / 12 | -3,463.2 |
| Ordering + quarter-batch front-run | 6 / 12 | -25.3 |
| Ordering + half-batch front-run | 8 / 12 | +1,093.8 |
| **Ordering + complete scheduled front-run** | **12 / 12** | **+2,697.5** |
| Ordering + two-turn-early quarter batch | 4 / 12 | -1,025.5 |

The promoted amount was frozen before opening the four-seed holdout.

### Unopened holdout

| Opponent | Wins / 8 | Mean margin | Complete |
|---|---:|---:|:---:|
| Kaito v21.1 conditional memory | 6 / 8 | +1,694.5 | Yes |
| Rayk c27 | 8 / 8 | +12,104.9 | Yes |
| Soil / Subin-Savko composite | 8 / 8 | +10,093.9 | Yes |
| Structured economic policy | 8 / 8 | +22,952.3 | Yes |
| Bruce Route 1 | 8 / 8 | +9,625.3 | Yes |
| **Macro** | **38 / 40 (95%)** | **positive for every opponent** | **40 / 40** |

The holdout seeds were `314159`, `271828`, `161803`, and `141421`. They were
not used in the ablation. The checked-in league runner accepts external
file-based opponents and records their SHA-256 hashes so this protocol can be
repeated without committing third-party agents. The immutable per-match
manifest is checked in at [`docs/evidence/v2-holdout.json`](evidence/v2-holdout.json).

## Evidence boundary

- A local win is not a Kaggle rating.
- A successful upload is only `submitted` until the remote status becomes
  `COMPLETE`.
- The public simulation rating can continue moving after validation.
- A Notebook author's team score is not attributed to the Notebook binary
  unless hashes or chronology establish that link.
- V2's online row will be added only after the exact packaged `main.py` is
  uploaded and the submission ID is mapped to its Git commit.

# V7 strategy: public-shop five-route controller

V7 is the promoted `main.py` candidate with SHA-256
`7ce060d8551cf3e7a20a800c1eea2e18ece63d6d6eab8e21199b65f9b78e4794`.
It addresses the current V6 weakness: the 126-game public replay panel had
late market-cadence losses, especially when a low 10C/4S route met a public
6C/8S or 6C/9S opponent. V7 uses the opponent's observable shop prefix to
select a route whose production cadence is closer to the public behavior.

## Route selection

The selector is per-seat and re-evaluates the public prefix as shops unlock.
The legacy-opening decision is sticky. Both observe only gameplay fields that
are available to both agents during the episode.

| Observable signal | Current route | Route production profile |
|---|---|---:|
| first unlocked shop is `YARN_STORE` | first-Yarn | 6 cows / 12 sheep requested over the tape |
| second shop is `YARN_STORE` | second-Yarn | 6 cows / 12 sheep requested over the tape |
| Yarn appears by the third shop | 6C8S | 6 cows / 8 sheep |
| early first-three-shop milk-support pattern | 10C4S | 10 cows / 4 sheep |
| no earlier signal | 8C6S | 8 cows / 6 sheep |

The 6C/12S routes request and place twelve sheep over the full tape; the
verified route lifecycle can sell or replace animals and therefore has a
stable terminal herd different from its cumulative purchase target. The exact
route tapes are normalized JSON action sequences compressed into `main.py`.

For older public openings, a step-24–71 gate recognizes the observable legacy
farm shape and chooses the corresponding legacy tape. This is a compatibility
route based on public state, not an identity, episode, submission, or seed
lookup. If the gate is not satisfied, the current five-route selector remains
in control.

## Retained execution controller

V7 retains the independently maintained V6 execution layer around the route
tapes:

- day-boundary clearing of in-flight weed transactions and passive weed
  recovery;
- atomic crop planting and route-prefix seed-feasibility checks;
- observable cow placement and partial-purchase reconciliation;
- bounded premium prepayment with quantity-conserving repayment;
- executable same-turn shed projection for SELL ranking;
- terminal WHEAT seed pruning and market-order quantity caps;
- per-seat retry-safe action caching and malformed-observation `PASS` fallback.

The route data are modified derivative portions of the Apache-2.0 public
Notebook artifact described in [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).
That notice records the source hashes, the fact that the public replay identity
is not inferred from artifact identity, and the license files distributed with
the submission archive.

## Route data fingerprints

The normalized route JSON hashes used during development were:

| Route | Current hash | Legacy hash |
|---|---|---|
| 10C4S | `60cd665cbcafdc3186256f2aff7004968b127ecdccb1c16de1265885d422111c` | `25b683c5d82e120b7da51b50128ddd8c9966a933c38f53421b23f9c6785fd6de` |
| 8C6S | `2483809ada657c092e98e2b854ded9539a9b9a597723f1f4027a02ea97faa6aa` | `96f5164bece882a2b943e843f6208e8b16377a756df0d017ea3159fa167b7199` |
| 6C8S | `25f62869f42ce905b882b4acc66c1fb2061d89b6293ac42c24e030de60460942` | `3ccd016720dde7d921decf1caeebaac057390fca0f3c19906e4a94b4a20b6062` |
| first-Yarn 6C12S | `64e81ecf1788855ab65e58671042c0c241dbc63accc972eb73caed8b637da5d2` | `64e81ecf1788855ab65e58671042c0c241dbc63accc972eb73caed8b637da5d2` |
| second-Yarn 6C12S | `a072f831ccca5ba0e0ca4b6d38d1eec3994cc34627b8c748831f027c9e066d9d` | `a072f831ccca5ba0e0ca4b6d38d1eec3994cc34627b8c748831f027c9e066d9d` |

## Evidence boundary

The analysis snapshot observed V6 at score 2416.6 at
`2026-08-20T04:01:34Z`; V5 was 2665.5. The leaderboard CSV snapshot at
`2026-08-20T04:04:51Z` had 5,446 teams and the local team at rank 74 with
score 2665.5. These values are dynamic ratings, not immutable benchmark
results. The captured CSV ZIP SHA-256 is
`dfc3e51ee9f924b89a6ab988768102e695ee5fc0e509a775dd56ef0c948cd61c`.

The 126 public V6 replays were analyzed under engine 1.32.7. V6 had 75 wins
and 51 losses, all with terminal `DONE/DONE`; the largest loss clusters were
strawberry revenue deficits (23 rows, mean margin -3343.3), wool deficits (8,
-9174.6), wheat deficits (8, -1915.0), and late market cadence/liquidation
(10, -1756.9). V7's fixed-tape open-loop replay comparison was 99/126, mean
margin +7401.508, with 72 improved and 54 regressed rows. It is diagnostic
counterfactual evidence, not a closed-loop policy rematch.

The final frozen closed-loop panel used engine 1.32.7, both seats, and the
following eight seeds (none overlap the earlier development manifests):

```text
494168721, 1841303361, 1326838907, 635119006,
1232971796, 1228162192, 1754842454, 765588388
```

| Hash-pinned opponent | Main SHA-256 | Games | Wins | Losses | Mean margin | Worst margin |
|---|---|---:|---:|---:|---:|---:|
| latest Tetsu adaptive | `c26402b67a0d04a46348353069645b1a49c3cb3df6df69d7fa35d8adbbdbeae4` | 16 | 16 | 0 | +3345.750 | +1584 |
| Tetsu town | `399dd14bbe8d2040c475eaccf6489462132af0aa583f5e21cfba17ae1a6c5788` | 16 | 16 | 0 | +3262.125 | +1556 |
| V6 | `888115e1a4c48a52f28eeac60ce6fb8ede5dd67db360fee5df004ffa0613885e` | 16 | 11 | 5 | +532.250 | -14727 |
| V17 | `ccf2aefdadd600d3e6fcaad2879a310eb15bbd14183fc2deeff9bb2525697b9a` | 16 | 13 | 3 | +291.438 | -25819 |

All 64 fresh matches reached 720 states, `DONE/DONE`, and produced no stderr.
The per-opponent means are positive, but this panel does not establish
universal dominance. In particular, an older 96-game development panel gave
the pre-final behavior candidate (`575dcf5599c6cd4f899c96f5598fd8c7d11f6e7798ee815463faea0d6b09b21d`)
65/96 wins while V6 gave 96/96. That panel was not rerun after removal of
unused route constants, so it is intentionally retained as a pre-final
regression boundary rather than attributed to the final hash.

The Kaggle runner calls agents sequentially. V7's active route and sales
schedule use module-level mutable pointers and are verified for alternating
seat calls, but the policy is not designed for concurrent calls into one
Python module. The legacy compatibility gate also assumes a normal episode
starts before step 72. Both assumptions match the current competition runner.

Raw manifests and hashes are recorded in
[`docs/evidence/v7-failure-analysis.json`](evidence/v7-failure-analysis.json).
The reviewed 99,523-byte archive has SHA-256
`03c99a672bee741591d7224781865efd20cb3a26ea775193eadade4ac28f5c4a`.
It was delivered as Kaggle submission `55638354`, message
`v7 public-shop five-route 77c271f`, and reached `COMPLETE`. The uploaded
`main.py` maps to Git commit
`77c271f600b09b2dc070bc6b406240356bcb5616`. Kaggle recorded the submission at
`2026-08-20T04:56:38.653Z`; validation was observed at
`2026-08-20T05:02:19Z` with an initial dynamic public score of 600.0.

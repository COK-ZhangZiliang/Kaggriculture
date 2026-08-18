# V6 strategy and evidence

V6 keeps V5 as the default policy and adds one conservative behavior gate for
a repeated failure cluster found in public Kaggle replays.

## Failure diagnosis

The V5 public score immediately before V6 upload was `2730.6`. All 24
captured public losses reached 720 states with `DONE/DONE`; they were economic
losses rather than crashes, invalid-action termination, or timeout failures.
The largest repeatable opportunity was a public opening with an identical
observable farm shape at step 72 but a later production and market cadence
that V5 did not counter well.

On the 97 captured public games, V5 won 73 and lost 24, with mean margin
`+5252.247`. The V6 candidate won 78 and lost 19, with mean margin `+5834.186`.
It flipped five historical losses while retaining the win outcome in all 73
controls. This is fixed-action replay counterfactual evidence, not a live
rematch.

## Current policy

- Keep the V5 low/high public-shop selector, route-aware seed and cow purchase
  repair, bounded weed and placement recovery, executable SELL ranking,
  terminal pruning, and retry-safe per-seat action cache.
- At step 72, inspect only the opponent's public farm state and the public town
  shops. Select the counter route only when the opponent has exactly `$49`, no
  hired hands, 2 cows, 2 sheep, 12 melon plants, 7 wheat plants, and 5 pasture
  tiles, and the first unlocked shop is `BAKERY` or `PIZZA_SHOP`.
- If the first two unlocked shops later repeat, cancel the counter route and
  fall back to the V5 selector. This avoids applying a route reconstructed from
  six highly consistent public episodes to a nearby but unvalidated market
  prefix.
- Keep route state independent by seat and reset it on a new episode.

The controller never branches on opponent or team identity, submission ID,
episode ID, seed, or randomness.

## Verification boundary

The current repository `main.py` SHA-256 is
`888115e1a4c48a52f28eeac60ce6fb8ede5dd67db360fee5df004ffa0613885e`.
Its decompressed low, high, and counter route hashes are recorded in the
checked-in evidence JSON.

The 16-seed, both-seat regression panel against the three still-available
hash-pinned public artifacts completed 96/96 wins, mean margin `+3793.573`,
and worst margin `+181`; every game reached 720 states with `DONE/DONE` and no
captured stderr. Kaito v27 was unavailable for this rerun, so this is not
presented as the earlier four-opponent V5 panel.

A separate fresh 8-seed, both-seat panel completed 47/48 wins, mean margin
`+3301.125`, and worst margin `-448`. The same
Tetsu-adaptive/seed/seat row was also V5's only loss, while V6 improved mean
margin by `+763.063`. This supports non-regression but leaves the near-mirror
loss as an explicit boundary.

The evaluated frozen candidate and repository source differ only in the module
documentation string and compressed-route declaration order. Behavioral
equivalence is checked through all three decompressed route hashes and targeted
selector tests. Exact seeds, hashes, aggregates, and claim limits are in
[`evidence/v6-failure-analysis.json`](evidence/v6-failure-analysis.json).

These local and replay panels do not establish performance against hidden or
future policies. Kaggle validation and leaderboard scoring are separate
delivery gates.

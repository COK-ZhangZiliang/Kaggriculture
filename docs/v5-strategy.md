# V5 strategy and evidence

V5 keeps the public-shop two-expert route selector and hardens the execution
edges that caused the largest V4 failures.

## Current policy

- Select the low 10C/4S route or high 6C/8S terminal route from the first two
  public shops at step 168. The decision is sticky and per-seat.
- Clip seed purchases against the selected route's prefix planting demand,
  respecting the engine's atomic same-crop planting rule. Remove terminal wheat
  purchases after the last future wheat planting.
- Clear an in-flight weed replay at hour 0 because the engine resets workers to
  the shed at a day boundary. This prevents yesterday's movement/CARE/WATER
  transaction from being replayed from a new position.
- Keep the bounded visible-weed, cow-placement, partial-purchase, H1/H7, and
  retry-safe per-seat state controls from V4.
- Rank SELL slots using projected same-turn shed stock after farmer/hand
  PICKUP, DROP, and PLACE actions, then merge duplicate product orders without
  exceeding ten market slots.

All route choices and repairs use public/private gameplay observations only;
the controller does not branch on seed, episode, opponent/team name,
submission ID, or randomness.

## Verification boundary

The current `main.py` SHA-256 is
`9390f7a9136f7c724376107fa3b2f464d871b0d725ac2039503c1cc312f6bc5b`.
The repository has 56 passing tests. Starter and random local matches each
completed 720 states with `DONE/DONE` under the repository's Kaggle runtime.

The current-hash opened regression panel uses 16 seeds, four hash-pinned public
agents, both seats, and Kaggriculture engine 1.32.7. It completed 128/128 wins,
with mean margin `+6321.125` and worst margin `+181`; every row completed 720
states with no stderr. This is the promoted local strength gate represented by
the checked-in evidence JSON.

The separately generated RC1 diagnostic panel completed 123/128 wins, mean
margin `+6417.453`, and worst margin `-2549`. Its five remaining losses are
near-mirror stochastic market cases. They remain documented as an open
diagnostic rather than being hidden by identity or seed routing.

The day-boundary fix was causally checked on the prior worst seed: both seats
against four public agents completed 8/8 wins, all 720 states, and worst margin
`+255`. That predecessor artifact is included only as a debugging trace; the
promoted numbers are bound to the current hash above.

Raw result hashes and opponent artifact hashes are recorded in
[`evidence/v5-failure-analysis.json`](evidence/v5-failure-analysis.json).
The 128-game panel is closed-loop local evaluation; it is not a Kaggle
leaderboard score and does not establish performance against hidden policies.

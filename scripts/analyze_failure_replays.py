#!/usr/bin/env python3
"""Summarize Kaggriculture online replay failures without storing replay data.

The Kaggle replay at frame ``t + 1`` contains the action executed for
observation step ``t``.  This utility keeps that offset explicit and reports
only aggregate, non-private diagnostics suitable for regression design.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


SELLABLE = (
    "WHEAT",
    "CARROT",
    "TOMATO",
    "STRAWBERRY",
    "MELON",
    "EGG",
    "MILK",
    "WOOL",
    "FERTILIZER",
)
PREMIUM = ("MELON", "STRAWBERRY", "MILK", "WOOL")
CHECKPOINTS = (0, 24, 96, 160, 192, 288, 384, 480, 576, 672, 719)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("replays", nargs="+", type=Path)
    parser.add_argument("--team", default="ziliangCok")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def _quantity(order):
    try:
        return max(0, int(order[2])) if len(order) >= 3 else 1
    except (TypeError, ValueError):
        return 0


def _animal_counts(farm):
    counts = Counter()
    for row in farm.get("tiles", []) or []:
        for tile in row or []:
            if isinstance(tile, dict) and tile.get("animal"):
                counts[str(tile["animal"])] += 1
    return dict(sorted(counts.items()))


def _owned_animals(observation, seat):
    counts = Counter(_animal_counts(observation["farms"][seat]))
    private = observation.get("private", {}) or {}
    counts.update(
        {
            item: int(quantity or 0)
            for item, quantity in (private.get("shed", {}) or {}).items()
            if item in ("COW", "SHEEP", "GOOSE")
        }
    )
    for inventory in private.get("inventories", []) or []:
        counts.update(
            {
                item: int(quantity or 0)
                for item, quantity in (inventory or {}).items()
                if item in ("COW", "SHEEP", "GOOSE")
            }
        )
    return counts


def _crop_counts(farm):
    counts = Counter()
    for row in farm.get("tiles", []) or []:
        for tile in row or []:
            if isinstance(tile, dict) and tile.get("crop"):
                counts[str(tile["crop"])] += 1
    return dict(sorted(counts.items()))


def _stock(private):
    total = Counter(private.get("shed", {}) or {})
    for inventory in private.get("inventories", []) or []:
        total.update(inventory or {})
    return {item: max(0, int(total.get(item, 0) or 0)) for item in SELLABLE}


def _market_summary(replay, seat):
    requested_sales = Counter()
    sale_steps = defaultdict(list)
    buys = Counter()
    market_op_counts = Counter()
    positive_net_money_delta = 0
    negative_net_money_delta = 0
    mixed_cashflow_steps = 0
    unfilled_hire_orders = []
    unfilled_animal_orders = []

    for step in range(min(719, len(replay["steps"]) - 1)):
        before = replay["steps"][step][seat]["observation"]
        after = replay["steps"][step + 1][seat]["observation"]
        action = replay["steps"][step + 1][seat].get("action") or {}
        orders = action.get("market", []) or []
        ops = {order[0] for order in orders if isinstance(order, list) and order}
        if "SELL" in ops and len(ops) > 1:
            mixed_cashflow_steps += 1
        delta = int(after["farms"][seat]["money"]) - int(
            before["farms"][seat]["money"]
        )
        positive_net_money_delta += max(0, delta)
        negative_net_money_delta += max(0, -delta)
        for order in orders:
            if not isinstance(order, list) or not order:
                continue
            op = str(order[0])
            market_op_counts[op] += 1
            if op == "SELL" and len(order) >= 2:
                item = str(order[1])
                requested_sales[item] += _quantity(order)
                sale_steps[item].append(step)
            elif op.startswith("BUY_") and len(order) >= 2:
                buys[f"{op}:{order[1]}"] += _quantity(order)
            elif op in ("HIRE", "BUY_LAND"):
                buys[op] += 1
        requested_hires = sum(
            order == ["HIRE"] for order in orders if isinstance(order, list)
        )
        if requested_hires and step % 24 != 23:
            before_hands = len(before["farms"][seat].get("hands", []) or [])
            after_hands = len(after["farms"][seat].get("hands", []) or [])
            successful = max(0, after_hands - before_hands)
            if successful < requested_hires:
                unfilled_hire_orders.append(
                    {
                        "step": step,
                        "requested": requested_hires,
                        "successful": successful,
                        "money_before": int(before["farms"][seat]["money"]),
                        "causal_impact": "unknown_without_untruncated_route",
                    }
                )
        before_animals = _owned_animals(before, seat)
        after_animals = _owned_animals(after, seat)
        for item in ("COW", "SHEEP", "GOOSE"):
            requested = sum(
                _quantity(order)
                for order in orders
                if isinstance(order, list)
                and len(order) >= 2
                and order[:2] == ["BUY_ANIMAL", item]
            )
            if not requested:
                continue
            successful = max(0, after_animals[item] - before_animals[item])
            if successful < requested:
                unfilled_animal_orders.append(
                    {
                        "step": step,
                        "item": item,
                        "requested": requested,
                        "successful": successful,
                        "money_before": int(before["farms"][seat]["money"]),
                    }
                )
    return {
        "requested_sales": dict(sorted(requested_sales.items())),
        "sale_steps": {key: value for key, value in sorted(sale_steps.items())},
        "buys": dict(sorted(buys.items())),
        "market_order_counts": dict(sorted(market_op_counts.items())),
        "positive_net_money_delta": positive_net_money_delta,
        "negative_net_money_delta": negative_net_money_delta,
        "mixed_cashflow_steps": mixed_cashflow_steps,
        "unfilled_hire_orders": unfilled_hire_orders,
        "unfilled_animal_orders": unfilled_animal_orders,
    }


def _field_summary(replay, seat):
    counts = Counter()
    for frame in replay["steps"][1:]:
        action = frame[seat].get("action") or {}
        orders = [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]
        for order in orders:
            if isinstance(order, list) and order:
                counts[str(order[0])] += 1
    return dict(sorted(counts.items()))


def _sale_timing_relation(left, right):
    result = {}
    for item in PREMIUM:
        own = left.get("sale_steps", {}).get(item, [])
        opponent = right.get("sale_steps", {}).get(item, [])
        if not own or not opponent:
            result[item] = {"same": 0, "opponent_1_5_early": 0}
            continue
        result[item] = {
            "same": sum(step in opponent for step in own),
            "opponent_1_5_early": sum(
                any(step - 5 <= other < step for other in opponent)
                for step in own
            ),
        }
    return result


def analyze(path, team):
    replay = json.loads(path.read_text(encoding="utf-8"))
    teams = list(replay["info"]["TeamNames"])
    if teams.count(team) != 1:
        raise ValueError(f"{path}: team {team!r} is not present exactly once")
    seat = teams.index(team)
    opponent = 1 - seat
    own_market = _market_summary(replay, seat)
    opponent_market = _market_summary(replay, opponent)
    checkpoints = []
    for frame_index in CHECKPOINTS:
        if frame_index >= len(replay["steps"]):
            continue
        own_obs = replay["steps"][frame_index][seat]["observation"]
        opponent_obs = replay["steps"][frame_index][opponent]["observation"]
        own_farm = own_obs["farms"][seat]
        opponent_farm = own_obs["farms"][opponent]
        checkpoints.append(
            {
                "frame": frame_index,
                "money_margin": int(own_farm["money"]) - int(opponent_farm["money"]),
                "money": [int(own_farm["money"]), int(opponent_farm["money"])],
                "hands": [len(own_farm.get("hands", []) or []), len(opponent_farm.get("hands", []) or [])],
                "animals": [_animal_counts(own_farm), _animal_counts(opponent_farm)],
                "crops": [_crop_counts(own_farm), _crop_counts(opponent_farm)],
                "stock": [_stock(own_obs.get("private", {}) or {}), _stock(opponent_obs.get("private", {}) or {})],
            }
        )
    rewards = [int(value) for value in replay["rewards"]]
    return {
        "episode_id": int(replay["info"]["EpisodeId"]),
        "seed": int(replay["info"]["seed"]),
        "seat": seat,
        "opponent": teams[opponent],
        "rewards": rewards,
        "margin": rewards[seat] - rewards[opponent],
        "statuses": replay["statuses"],
        "checkpoints": checkpoints,
        "own_market": own_market,
        "opponent_market": opponent_market,
        "sale_timing_relation": _sale_timing_relation(own_market, opponent_market),
        "own_field": _field_summary(replay, seat),
        "opponent_field": _field_summary(replay, opponent),
    }


def main():
    args = parse_args()
    rows = [analyze(path, args.team) for path in args.replays]
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True))
        return
    header = (
        "episode\tseat\tmargin\topponent\t"
        "m192\tm384\tm576\tend\t"
        "own_positive_net_delta\topp_positive_net_delta\t"
        "own_cows\topp_cows\tstranded\tunfilled_hires\tunfilled_animals"
    )
    print(header)
    for row in rows:
        by_frame = {point["frame"]: point for point in row["checkpoints"]}
        final = by_frame[max(by_frame)]
        own_animals, opponent_animals = final["animals"]
        stranded = sum(final["stock"][0].values())
        print(
            row["episode_id"],
            row["seat"],
            row["margin"],
            row["opponent"],
            by_frame.get(192, {}).get("money_margin"),
            by_frame.get(384, {}).get("money_margin"),
            by_frame.get(576, {}).get("money_margin"),
            final["money_margin"],
            row["own_market"]["positive_net_money_delta"],
            row["opponent_market"]["positive_net_money_delta"],
            own_animals.get("COW", 0),
            opponent_animals.get("COW", 0),
            stranded,
            len(row["own_market"]["unfilled_hire_orders"]),
            len(row["own_market"]["unfilled_animal_orders"]),
            sep="\t",
        )


if __name__ == "__main__":
    main()

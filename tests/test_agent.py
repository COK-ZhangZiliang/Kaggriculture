from copy import deepcopy

import main as submission
from main import agent


PRODUCTS = (
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


def make_observation(
    *,
    step=0,
    player=0,
    shed=None,
    inventories=None,
    hands=None,
    identical_opponent=True,
):
    hands = deepcopy(hands or [])
    tiles = []
    for y in range(10):
        row = []
        for x in range(10):
            row.append(None if x < 5 and y < 5 else "LOCKED")
        tiles.append(row)
    farm = {
        "money": 3000,
        "tiles": tiles,
        "farmer": [4, 4],
        "hands": hands,
        "unlocked_quadrants": ["NW"],
        "hires_today": 0,
    }
    other = deepcopy(farm)
    if not identical_opponent:
        other["money"] = 2500
        other["unlocked_quadrants"] = ["NW", "NE"]
    unit_inventories = deepcopy(
        inventories or [{} for _ in range(len(hands) + 1)]
    )
    return {
        "step": step,
        "day": step // 24,
        "hour": step % 24,
        "player": player,
        "farms": [deepcopy(farm), other],
        "market": {
            "inventory": {product: 10000 for product in PRODUCTS},
            "prices": {product: 100 for product in PRODUCTS},
        },
        "town": {"unlocked_shops": []},
        "private": {
            "shed": deepcopy(shed or {}),
            "seeds": {},
            "inventories": unit_inventories,
        },
    }


def test_opening_builds_a_mixed_herd_and_crop_supply_chain():
    action = agent(make_observation())

    assert action["farmer"] == ["PASS"]
    assert action["hands"] == []
    assert action["market"].count(["HIRE"]) == 5
    assert ["BUY_ANIMAL", "SHEEP", 2] in action["market"]
    assert ["BUY_ANIMAL", "COW", 2] in action["market"]
    assert ["BUY_SEED", "WHEAT", 7] in action["market"]
    assert ["BUY_SEED", "MELON", 12] in action["market"]
    assert len(action["market"]) <= 10


def test_hand_actions_are_aligned_to_observed_workers():
    hands = [[4, 3], [4, 2], [4, 1]]
    action = agent(make_observation(step=2, hands=hands))

    assert len(action["hands"]) == len(hands)


def test_visible_weed_is_dug_then_the_delayed_build_is_retried():
    hands = [[4, 3], [4, 2], [4, 1], [4, 0], [3, 4]]
    obs = make_observation(step=2, hands=hands)
    obs["farms"][0]["tiles"][4][4] = {"kind": "WEED"}

    assert agent(obs)["farmer"] == ["DIG"]

    retry = make_observation(step=3, hands=hands)
    assert agent(retry)["farmer"] == ["BUILD_PASTURE"]


def test_sell_quantity_is_clipped_to_projected_shed_stock():
    action = agent(make_observation(step=39, shed={"FERTILIZER": 1}))

    assert ["SELL", "FERTILIZER", 1] in action["market"]
    assert ["SELL", "FERTILIZER", 2] not in action["market"]


def test_clone_front_run_moves_the_complete_next_premium_sale_forward():
    for step in range(202, 213):
        agent(make_observation(step=step))
    action = agent(make_observation(step=213, shed={"MILK": 6}))

    assert action["market"][0] == ["SELL", "MILK", 6]


def test_clone_front_run_does_not_evict_route_orders_from_a_full_market(monkeypatch):
    route_action = submission._action_at(648)
    assert len(route_action["market"]) == 10
    assert route_action["market"][-1] == ["BUY_SEED", "WHEAT", 8]

    original_action_at = submission._action_at

    def action_at(step):
        if step == 649:
            return {
                "farmer": ["PASS"],
                "hands": [],
                "market": [["SELL", "MELON", 5]],
            }
        return original_action_at(step)

    monkeypatch.setattr(submission, "_action_at", action_at)
    monkeypatch.setattr(submission, "_clone_like", lambda obs, step: True)
    action = agent(
        make_observation(
            step=648,
            shed={
                "WHEAT": 2,
                "STRAWBERRY": 9,
                "WOOL": 7,
                "MILK": 3,
                "MELON": 5,
            },
        )
    )

    assert len(action["market"]) == 10
    assert ["BUY_SEED", "WHEAT", 8] in action["market"]
    assert ["SELL", "MELON", 5] not in action["market"]


def test_last_executable_turn_drops_and_sells_all_reachable_products():
    obs = make_observation(
        step=718,
        shed={"MELON": 3},
        inventories=[{"MILK": 2}],
    )
    action = agent(obs)

    assert action["farmer"] == ["DROP"]
    assert ["SELL", "MELON", 3] in action["market"]
    assert ["SELL", "MILK", 2] in action["market"]


def test_actions_are_deterministic_after_game_reset():
    obs = make_observation(step=0)

    assert agent(deepcopy(obs)) == agent(deepcopy(obs))


def test_invalid_observation_fails_safe():
    assert agent({}) == {"farmer": ["PASS"], "hands": [], "market": []}

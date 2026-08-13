import hashlib
import json
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
    money=3000,
    shops=None,
):
    hands = deepcopy(hands or [])
    tiles = []
    for y in range(10):
        row = []
        for x in range(10):
            row.append(None if x < 5 and y < 5 else "LOCKED")
        tiles.append(row)
    farm = {
        "money": money,
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
        "town": {"unlocked_shops": list(shops or [])},
        "private": {
            "shed": deepcopy(shed or {}),
            "seeds": {},
            "inventories": unit_inventories,
        },
    }


def reset_controller():
    submission._FR_STATE.clear()
    submission._FR_STATE.update(
        {
            0: {"last_step": -1, "due_step": -1, "due": {}},
            1: {"last_step": -1, "due_step": -1, "due": {}},
        }
    )
    submission._WEED_STATE.clear()
    submission._WEED_STATE.update({0: {}, 1: {}})
    submission._COW_ALIGN_STATE.clear()
    submission._COW_ALIGN_STATE.update(
        {
            0: {"last_step": -1, "active": {}},
            1: {"last_step": -1, "active": {}},
        }
    )
    submission._META_STATE.clear()
    submission._META_STATE.update(
        {0: submission._new_meta_state(), 1: submission._new_meta_state()}
    )


def test_route_is_the_frozen_eight_cow_four_sheep_schedule():
    route_hash = hashlib.sha256(
        json.dumps(submission._ACTIONS, separators=(",", ":")).encode()
    ).hexdigest()
    cow_buys = sum(
        order[2]
        for action in submission._ACTIONS[:719]
        for order in action.get("market", [])
        if order[:2] == ["BUY_ANIMAL", "COW"]
    )
    sheep_buys = sum(
        order[2]
        for action in submission._ACTIONS[:719]
        for order in action.get("market", [])
        if order[:2] == ["BUY_ANIMAL", "SHEEP"]
    )

    assert len(submission._ACTIONS) == 720
    assert route_hash == (
        "7a338431c2080e929df6871f45f686d0fde09036070c7a85ee0143afc228cfeb"
    )
    assert (cow_buys, sheep_buys) == (8, 4)


def test_opening_builds_the_eight_cow_four_sheep_supply_chain():
    reset_controller()
    action = agent(make_observation())

    assert action["farmer"] == ["PASS"]
    assert action["hands"] == []
    assert action["market"].count(["HIRE"]) == 5
    assert ["BUY_ANIMAL", "SHEEP", 4] in action["market"]
    assert ["BUY_ANIMAL", "COW", 1] in action["market"]
    assert ["BUY_SEED", "MELON", 5] in action["market"]
    assert len(action["market"]) == 10


def test_hand_actions_are_aligned_to_observed_workers():
    reset_controller()
    hands = [[4, 3], [4, 2], [4, 1]]
    action = agent(make_observation(step=2, hands=hands))

    assert len(action["hands"]) == len(hands)


def test_visible_weed_is_dug_then_the_delayed_build_is_retried():
    reset_controller()
    hands = [[4, 3], [4, 2], [4, 1], [4, 0], [3, 4]]
    obs = make_observation(step=4, hands=hands)
    obs["farms"][0]["tiles"][4][4] = {"kind": "WEED"}

    assert agent(obs)["farmer"] == ["DIG"]
    retry = make_observation(step=5, hands=hands)
    assert agent(retry)["farmer"] == ["BUILD_PASTURE"]


def test_cow_alignment_moves_to_an_adjacent_empty_pasture_then_places():
    reset_controller()
    obs = make_observation(step=165, inventories=[{"COW": 1}])
    obs["farms"][0]["tiles"][4][4] = {"kind": "PASTURE", "animal": "COW"}
    obs["farms"][0]["tiles"][4][5] = {"kind": "PASTURE", "animal": None}
    action = {"farmer": ["PLACE", "COW", 1], "hands": [], "market": []}

    moved = submission._cow_place_alignment(obs, action, 165)
    assert moved["farmer"] == ["EAST"]

    next_obs = make_observation(step=166, inventories=[{"COW": 1}])
    next_obs["farms"][0]["farmer"] = [5, 4]
    next_obs["farms"][0]["tiles"][4][5] = {
        "kind": "PASTURE",
        "animal": None,
    }
    placed = submission._cow_place_alignment(
        next_obs,
        {"farmer": ["PASS"], "hands": [], "market": []},
        166,
    )
    assert placed["farmer"] == ["PLACE", "COW", 1]


def test_one_turn_lead_conserves_the_scheduled_quantity():
    reset_controller()
    obs = make_observation(step=159, shed={"WOOL": 9})
    state = submission._fr_state(obs, 159)
    action = submission._front_run(
        {"farmer": ["PASS"], "hands": [], "market": []},
        obs,
        state,
        159,
    )

    assert action["market"] == [["SELL", "WOOL", 9]]
    assert state == {
        "last_step": 159,
        "due_step": 160,
        "due": {"WOOL": 9},
    }
    repaid = submission._repay(
        deepcopy(submission._ACTIONS[160]), state, 160
    )
    assert ["SELL", "WOOL", 9] not in repaid["market"]


def test_one_turn_lead_also_covers_wheat_and_fertilizer_collisions():
    assert "WHEAT" in submission._FR_ITEMS
    assert "FERTILIZER" in submission._FR_ITEMS


def test_one_turn_lead_skips_a_town_demand_turn():
    reset_controller()
    obs = make_observation(
        step=232,
        shed={"MILK": 3},
        shops=["SMOOTHIE_SHOP"],
    )
    state = submission._fr_state(obs, 232)
    action = submission._front_run(
        {"farmer": ["PASS"], "hands": [], "market": []},
        obs,
        state,
        232,
    )

    assert action["market"] == []
    assert state["due"] == {}


def test_h4_observation_activates_only_from_clean_public_supply():
    reset_controller()
    obs = make_observation(step=157)
    state = submission._new_meta_state()
    state.update(
        {
            "clone_confidence": 3,
            "prev_market_inv": {product: 10000 for product in PRODUCTS},
            "prev_prices": {product: 100 for product in PRODUCTS},
            "prev_action": {
                "farmer": ["PASS"],
                "hands": [],
                "market": [["SELL", "WOOL", 9]],
            },
            "prev_shed": {"WOOL": 9},
            "prev_town_shops": (),
            "prev_step": 156,
        }
    )
    obs["market"]["inventory"]["WOOL"] += 18

    submission._meta_observe_h4(obs, 157, state)

    assert state["h4_active"] is True
    assert state["h4_evidence"] == 1


def test_h4_observation_ignores_the_one_dollar_price_floor():
    reset_controller()
    obs = make_observation(step=157)
    state = submission._new_meta_state()
    state.update(
        {
            "clone_confidence": 3,
            "prev_market_inv": {product: 10000 for product in PRODUCTS},
            "prev_prices": {**{product: 100 for product in PRODUCTS}, "WOOL": 1},
            "prev_action": {
                "farmer": ["PASS"],
                "hands": [],
                "market": [["SELL", "WOOL", 9]],
            },
            "prev_shed": {"WOOL": 9},
            "prev_town_shops": (),
            "prev_step": 156,
        }
    )
    obs["market"]["inventory"]["WOOL"] += 18

    submission._meta_observe_h4(obs, 157, state)

    assert state["h4_active"] is False


def test_confirmed_h4_counter_preempts_the_matching_sale_by_five_turns():
    reset_controller()
    obs = make_observation(step=155, shed={"WOOL": 9})
    state = submission._new_meta_state()
    state["h4_active"] = True
    action = {"farmer": ["PASS"], "hands": [], "market": []}

    assert submission._meta_h5_counter(action, obs, 155, state)
    assert action["market"] == [["SELL", "WOOL", 9]]


def test_h5_counter_does_not_evict_a_full_market_queue():
    reset_controller()
    market = [["BUY_SEED", "WHEAT", index + 1] for index in range(10)]
    action = {"farmer": ["PASS"], "hands": [], "market": deepcopy(market)}
    obs = make_observation(step=155, shed={"WOOL": 9})
    state = submission._new_meta_state()
    state["h4_active"] = True

    assert not submission._meta_h5_counter(action, obs, 155, state)
    assert action["market"] == market


def test_h5_counter_skips_when_current_town_demand_resets_the_edge():
    reset_controller()
    obs = make_observation(
        step=228,
        shed={"MILK": 3},
        shops=["SMOOTHIE_SHOP"],
    )
    state = submission._new_meta_state()
    state["h4_active"] = True
    action = {"farmer": ["PASS"], "hands": [], "market": []}

    assert not submission._meta_h5_counter(action, obs, 228, state)
    assert action["market"] == []


def test_meta_state_is_isolated_between_player_seats():
    reset_controller()
    submission._META_STATE[0]["h4_active"] = True

    second = submission._meta_state(make_observation(step=10, player=1), 10)

    assert submission._META_STATE[0]["h4_active"] is True
    assert second["h4_active"] is False


def test_step_zero_reset_is_deterministic():
    reset_controller()
    obs = make_observation(step=0)

    assert agent(deepcopy(obs)) == agent(deepcopy(obs))


def test_invalid_observation_fails_safe():
    reset_controller()
    assert agent({}) == {"farmer": ["PASS"], "hands": [], "market": []}

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


def make_cow9_observation(
    *,
    player=0,
    own_cows=8,
    opponent_cows=9,
    milk_price=225,
    money=800,
    shops=None,
):
    obs = make_observation(
        step=289,
        player=player,
        money=money,
        shops=shops
        or ["PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP"],
    )
    for farm_index, cow_count in (
        (player, own_cows),
        (1 - player, opponent_cows),
    ):
        for index in range(cow_count):
            x, y = index % 10, index // 10
            obs["farms"][farm_index]["tiles"][y][x] = {
                "kind": "PASTURE",
                "animal": "COW",
            }
    obs["market"]["prices"]["MILK"] = milk_price
    return obs


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


def test_opening_seed_buys_are_clipped_to_remaining_plant_demand():
    surplus = make_observation(step=1, money=2)
    surplus["private"]["seeds"] = {"MELON": 2, "WHEAT": 4}
    protected = submission._clip_opening_seed_surplus(
        deepcopy(submission._ACTIONS[1]), surplus, 1
    )
    assert ["BUY_SEED", "MELON", 3] in protected["market"]
    assert ["BUY_SEED", "WHEAT", 1] in protected["market"]

    exact = make_observation(step=1, money=3)
    exact["private"]["seeds"] = {"MELON": 2, "WHEAT": 3}
    unchanged = submission._clip_opening_seed_surplus(
        deepcopy(submission._ACTIONS[1]), exact, 1
    )
    assert ["BUY_SEED", "MELON", 3] in unchanged["market"]
    assert ["BUY_SEED", "WHEAT", 2] in unchanged["market"]


def test_opening_seed_clip_removes_zero_quantity_orders_from_agent_output():
    reset_controller()
    surplus = make_observation(step=1, money=2)
    surplus["private"]["seeds"] = {"MELON": 99, "WHEAT": 99}

    action = submission.agent(surplus)

    assert not [
        order
        for order in action["market"]
        if order[:2] in (
            ["BUY_SEED", "MELON"],
            ["BUY_SEED", "WHEAT"],
        )
    ]
    assert all(
        len(order) < 3 or int(order[2]) > 0
        for order in action["market"]
    )


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


def test_later_cow_order_repairs_an_observed_partial_purchase():
    obs = make_observation(step=168, money=2200)
    for x in range(3):
        obs["farms"][0]["tiles"][0][x] = {
            "kind": "PASTURE",
            "animal": "COW",
        }
    repaired = submission._reconcile_scheduled_cows(
        obs, deepcopy(submission._ACTIONS[168]), 168
    )
    cow_order = next(
        order
        for order in repaired["market"]
        if order[:2] == ["BUY_ANIMAL", "COW"]
    )
    assert cow_order == ["BUY_ANIMAL", "COW", 3]

    obs["farms"][0]["tiles"][0][3] = {
        "kind": "PASTURE",
        "animal": "COW",
    }
    unchanged = submission._reconcile_scheduled_cows(
        obs, deepcopy(submission._ACTIONS[168]), 168
    )
    assert next(
        order
        for order in unchanged["market"]
        if order[:2] == ["BUY_ANIMAL", "COW"]
    ) == ["BUY_ANIMAL", "COW", 2]


def test_ninth_cow_requires_public_roi_signals_and_is_seat_seed_agnostic():
    market = [["BUY_SEED", "WHEAT", index + 1] for index in range(9)]
    action = {"farmer": ["PASS"], "hands": [], "market": market}
    results = []

    for player, seed, opponent_name in (
        (0, 11, "opponent-a"),
        (1, 987654321, "opponent-b"),
    ):
        obs = make_cow9_observation(player=player)
        obs["seed"] = seed
        obs["opponent_name"] = opponent_name
        result = submission._guarded_demand_cow9(
            obs, deepcopy(action), 289
        )
        assert result["market"][-1] == ["BUY_ANIMAL", "COW", 1]
        assert len(result["market"]) == 10
        results.append(result)

    assert results[0] == results[1]


def test_ninth_cow_stays_off_at_each_roi_boundary():
    action = {"farmer": ["PASS"], "hands": [], "market": []}
    cases = [
        make_cow9_observation(own_cows=7),
        make_cow9_observation(opponent_cows=8),
        make_cow9_observation(milk_price=224),
        make_cow9_observation(
            shops=["PIZZA_SHOP", "ICE_CREAM_SHOP"]
        ),
        make_cow9_observation(money=799),
    ]

    for obs in cases:
        assert submission._guarded_demand_cow9(
            obs, deepcopy(action), 289
        ) == action

    wrong_step = make_cow9_observation()
    assert submission._guarded_demand_cow9(
        wrong_step, deepcopy(action), 288
    ) == action


def test_ninth_cow_rejects_non_finite_roi_values():
    action = {"farmer": ["PASS"], "hands": [], "market": []}
    cases = []
    for invalid in (float("nan"), float("inf"), float("-inf")):
        invalid_price = make_cow9_observation()
        invalid_price["market"]["prices"]["MILK"] = invalid
        cases.append(invalid_price)
        invalid_money = make_cow9_observation()
        invalid_money["farms"][0]["money"] = invalid
        cases.append(invalid_money)

    for obs in cases:
        assert submission._guarded_demand_cow9(
            obs, deepcopy(action), 289
        ) == action


def test_ninth_cow_never_overflows_or_duplicates_the_market_queue():
    obs = make_cow9_observation()
    full_market = [["BUY_SEED", "WHEAT", index + 1] for index in range(10)]
    full_action = {
        "farmer": ["PASS"],
        "hands": [],
        "market": deepcopy(full_market),
    }
    assert submission._guarded_demand_cow9(
        obs, full_action, 289
    )["market"] == full_market

    existing_cow = {
        "farmer": ["PASS"],
        "hands": [],
        "market": [["BUY_ANIMAL", "COW", 2]],
    }
    assert submission._guarded_demand_cow9(
        obs, deepcopy(existing_cow), 289
    ) == existing_cow


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


def test_confirmed_h4_counter_preempts_the_matching_sale_by_seven_turns():
    reset_controller()
    obs = make_observation(step=153, shed={"WOOL": 9})
    state = submission._new_meta_state()
    state["h4_active"] = True
    action = {"farmer": ["PASS"], "hands": [], "market": []}

    assert submission._meta_h5_counter(action, obs, 153, state)
    assert action["market"] == [["SELL", "WOOL", 9]]
    assert state["h5_due"] == {160: {"WOOL": 9}}


def test_h7_prepayment_is_not_sold_again_by_the_one_turn_lead():
    reset_controller()
    meta = submission._new_meta_state()
    meta["h4_active"] = True
    early = {"farmer": ["PASS"], "hands": [], "market": []}
    assert submission._meta_h5_counter(
        early,
        make_observation(step=153, shed={"WOOL": 9}),
        153,
        meta,
    )

    fr_state = submission._fr_state(
        make_observation(step=159, shed={"WOOL": 9}), 159
    )
    one_turn = submission._front_run(
        {"farmer": ["PASS"], "hands": [], "market": []},
        make_observation(step=159, shed={"WOOL": 9}),
        fr_state,
        159,
        prepaid=meta["h5_due"][160],
    )
    assert one_turn["market"] == []

    due = deepcopy(submission._ACTIONS[160])
    submission._meta_repay_h5(due, 160, meta)
    assert ["SELL", "WOOL", 9] not in due["market"]
    assert meta["h5_due"] == {}


def test_h5_counter_does_not_evict_a_full_market_queue():
    reset_controller()
    market = [["BUY_SEED", "WHEAT", index + 1] for index in range(10)]
    action = {"farmer": ["PASS"], "hands": [], "market": deepcopy(market)}
    obs = make_observation(step=153, shed={"WOOL": 9})
    state = submission._new_meta_state()
    state["h4_active"] = True

    assert not submission._meta_h5_counter(action, obs, 153, state)
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

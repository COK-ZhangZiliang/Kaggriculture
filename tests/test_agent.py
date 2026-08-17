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
    submission._ACTIONS = submission._LOW_ACTIONS
    submission._META_SALES = submission._LOW_META_SALES
    submission._ROUTE_STATE.clear()
    submission._ROUTE_STATE.update(
        {
            0: {"last_step": -1, "shops": (), "expert": None},
            1: {"last_step": -1, "shops": (), "expert": None},
        }
    )
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
    submission._ACTION_CACHE.clear()
    submission._ACTION_CACHE.update(
        {
            0: {"step": -1, "signature": None, "action": None},
            1: {"step": -1, "signature": None, "action": None},
        }
    )


def test_routes_are_frozen_and_share_the_public_opening():
    expected = {
        "low": (
            submission._LOW_ACTIONS,
            "93daf1e051d2f394c50c08b59d0fd56d55bf0a5e8770e08701dbcacb91458518",
            (10, 4),
        ),
        "high": (
            submission._HIGH_ACTIONS,
            "a548603cf9cae2bda0bc016d50d574e072287ea68315b790b7341c99ab63a31c",
            (6, 12),
        ),
    }
    for route, route_hash, animal_buys in expected.values():
        actual_hash = hashlib.sha256(
            json.dumps(route, separators=(",", ":")).encode()
        ).hexdigest()
        cow_buys = sum(
            order[2]
            for action in route
            for order in action.get("market", [])
            if order[:2] == ["BUY_ANIMAL", "COW"]
        )
        sheep_buys = sum(
            order[2]
            for action in route
            for order in action.get("market", [])
            if order[:2] == ["BUY_ANIMAL", "SHEEP"]
        )
        assert len(route) == 719
        assert actual_hash == route_hash
        assert (cow_buys, sheep_buys) == animal_buys

    assert submission._LOW_ACTIONS[:168] == submission._HIGH_ACTIONS[:168]
    assert submission._LOW_ACTIONS[168] != submission._HIGH_ACTIONS[168]


def test_opening_builds_the_shared_high_throughput_supply_chain():
    reset_controller()
    action = agent(make_observation())

    assert action["farmer"] == ["BUILD_PASTURE"]
    assert action["hands"] == []
    assert action["market"].count(["HIRE"]) == 5
    assert ["BUY_ANIMAL", "SHEEP", 2] in action["market"]
    assert ["BUY_ANIMAL", "COW", 2] in action["market"]
    assert ["BUY_SEED", "MELON", 12] in action["market"]
    assert ["BUY_SEED", "WHEAT", 7] in action["market"]
    assert len(action["market"]) == 10


def test_hand_actions_are_aligned_to_observed_workers():
    reset_controller()
    hands = [[4, 3], [4, 2], [4, 1]]
    action = agent(make_observation(step=2, hands=hands))

    assert len(action["hands"]) == len(hands)


def test_route_selector_uses_only_early_public_shop_demand():
    reset_controller()
    high, high_sales = submission._select_route(
        make_observation(step=168, shops=["BAKERY", "YARN_STORE"]),
        168,
    )
    assert high is submission._HIGH_ACTIONS
    assert high_sales is submission._HIGH_META_SALES

    reset_controller()
    low, low_sales = submission._select_route(
        make_observation(step=168, shops=["BAKERY", "PIZZA_SHOP"]),
        168,
    )
    assert low is submission._LOW_ACTIONS
    assert low_sales is submission._LOW_META_SALES

    reset_controller()
    dominated, _ = submission._select_route(
        make_observation(
            step=168,
            shops=["ICE_CREAM_SHOP", "YARN_STORE"],
        ),
        168,
    )
    assert dominated is submission._LOW_ACTIONS


def test_route_selection_is_sticky_isolated_and_resets_between_games():
    reset_controller()
    high_obs = make_observation(
        step=168,
        player=0,
        shops=["YARN_STORE", "BAKERY"],
    )
    assert submission._select_route(high_obs, 168)[0] is submission._HIGH_ACTIONS
    changed = make_observation(
        step=216,
        player=0,
        shops=["BAKERY", "PIZZA_SHOP", "BRUNCH_SPOT"],
    )
    assert submission._select_route(changed, 216)[0] is submission._HIGH_ACTIONS

    low_other = make_observation(
        step=168,
        player=1,
        shops=["BAKERY", "PIZZA_SHOP"],
    )
    assert submission._select_route(low_other, 168)[0] is submission._LOW_ACTIONS
    reset_obs = make_observation(step=0, player=0)
    assert submission._select_route(reset_obs, 0)[0] is submission._LOW_ACTIONS


def test_route_selection_ignores_identity_metadata():
    actions = []
    for seed, opponent_name in ((11, "alpha"), (987654321, "beta")):
        reset_controller()
        obs = make_observation(
            step=168,
            shops=["YARN_STORE", "BAKERY"],
        )
        obs["seed"] = seed
        obs["opponent_name"] = opponent_name
        obs["EpisodeId"] = seed + 100
        actions.append(submission._select_route(obs, 168)[0][168])
    assert actions[0] == actions[1]


def test_seed_surplus_guard_is_a_noop_without_seed_orders():
    obs = make_observation(step=1, money=2)
    obs["private"]["seeds"] = {"MELON": 99, "WHEAT": 99}
    route_action = deepcopy(submission._ACTIONS[1])

    assert submission._clip_seed_surplus(
        route_action, obs, 1
    ) == submission._ACTIONS[1]


def test_opening_seed_clip_removes_zero_quantity_orders_from_agent_output():
    reset_controller()
    surplus = make_observation(step=0, money=2)
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


def test_seed_clip_preserves_prefix_capacity_and_removes_later_surplus():
    reset_controller()
    submission._ACTIONS = submission._LOW_ACTIONS
    obs = make_observation(step=152, money=1235)
    obs["private"]["seeds"] = {
        "WHEAT": 2,
        "CARROT": 0,
        "STRAWBERRY": 3,
        "MELON": 8,
    }

    clipped = submission._clip_seed_surplus(
        deepcopy(submission._LOW_ACTIONS[152]), obs, 152
    )

    assert clipped["market"] == [["BUY_SEED", "CARROT", 2]]


def test_seed_clip_does_not_buy_for_an_atomic_plant_that_already_failed():
    reset_controller()
    submission._ACTIONS = submission._LOW_ACTIONS
    obs = make_observation(step=525)
    obs["private"]["seeds"] = {"CARROT": 0}

    clipped = submission._clip_seed_surplus(
        deepcopy(submission._LOW_ACTIONS[525]), obs, 525
    )

    assert ["BUY_SEED", "CARROT", 1] not in clipped["market"]


def test_visible_weed_is_dug_then_the_delayed_build_is_retried():
    reset_controller()
    obs = make_observation(step=0)
    obs["farms"][0]["tiles"][4][4] = {"kind": "WEED"}

    assert agent(obs)["farmer"] == ["DIG"]
    retry = make_observation(step=1)
    assert agent(retry)["farmer"] == ["BUILD_PASTURE"]


def test_pass_on_a_visible_weed_is_replaced_by_dig():
    reset_controller()
    obs = make_observation(step=10)
    obs["farms"][0]["tiles"][4][4] = {"kind": "WEED"}
    action = {"farmer": ["PASS"], "hands": [], "market": []}

    repaired = submission._clear_passive_weeds(obs, action)

    assert repaired["farmer"] == ["DIG"]


def test_weed_replay_rejoins_on_the_first_move_to_an_empty_tile(monkeypatch):
    reset_controller()
    route = deepcopy(submission._LOW_ACTIONS)
    route[11]["farmer"] = ["WEST"]
    monkeypatch.setattr(submission, "_ACTIONS", route)
    submission._WEED_STATE[0] = {
        "last_step": 11,
        "active": {
            "farmer": {
                "start": 10,
                "intended": ["BUILD_PASTURE"],
            }
        },
        "post_recovery_market_regime": False,
    }
    obs = make_observation(step=12)

    repaired = submission._weed_repair_action(
        obs,
        {"farmer": ["PASS"], "hands": [], "market": []},
        12,
    )

    assert repaired["farmer"] == ["WEST"]
    assert submission._WEED_STATE[0]["active"] == {}
    assert (
        submission._WEED_STATE[0]["post_recovery_market_regime"] is True
    )


def test_weed_replay_preserves_followup_work_on_an_occupied_tile(monkeypatch):
    reset_controller()
    route = deepcopy(submission._LOW_ACTIONS)
    route[11]["farmer"] = ["WEST"]
    route[12]["farmer"] = ["WATER"]
    monkeypatch.setattr(submission, "_ACTIONS", route)
    submission._WEED_STATE[0] = {
        "last_step": 11,
        "active": {
            "farmer": {
                "start": 10,
                "intended": ["PLANT", "STRAWBERRY"],
            }
        },
        "post_recovery_market_regime": False,
    }
    moved = make_observation(step=12)
    moved["farms"][0]["tiles"][4][3] = {
        "kind": "PLANT",
        "plant": "STRAWBERRY",
    }

    first = submission._weed_repair_action(
        moved,
        {"farmer": ["PASS"], "hands": [], "market": []},
        12,
    )
    followup = make_observation(step=13)
    followup["farms"][0]["farmer"] = [3, 4]
    followup["farms"][0]["tiles"][4][3] = {
        "kind": "PLANT",
        "plant": "STRAWBERRY",
    }
    second = submission._weed_repair_action(
        followup,
        {"farmer": ["PASS"], "hands": [], "market": []},
        13,
    )

    assert first["farmer"] == ["WEST"]
    assert second["farmer"] == ["WATER"]
    assert (
        submission._WEED_STATE[0]["post_recovery_market_regime"] is False
    )


def test_weed_replay_is_cleared_when_workers_reset_at_day_boundary():
    reset_controller()
    submission._WEED_STATE[0] = {
        "last_step": 23,
        "active": {
            "farmer": {
                "start": 21,
                "intended": ["PLANT", "STRAWBERRY"],
            }
        },
        "post_recovery_market_regime": False,
    }
    obs = make_observation(step=24)
    current = {"farmer": ["EAST"], "hands": [], "market": []}

    repaired = submission._weed_repair_action(obs, current, 24)

    assert repaired["farmer"] == ["EAST"]
    assert submission._WEED_STATE[0]["active"] == {}


def test_day_boundary_clears_every_active_worker_transaction():
    reset_controller()
    submission._WEED_STATE[0] = {
        "last_step": 23,
        "active": {
            "farmer": {
                "start": 21,
                "intended": ["PLANT", "STRAWBERRY"],
            },
            0: {
                "start": 22,
                "intended": ["BUILD_PASTURE"],
            },
        },
        "post_recovery_market_regime": False,
    }
    obs = make_observation(step=24, hands=[[4, 4]])
    current = {
        "farmer": ["EAST"],
        "hands": [["WEST"]],
        "market": [],
    }

    repaired = submission._weed_repair_action(obs, current, 24)

    assert repaired["farmer"] == ["EAST"]
    assert repaired["hands"] == [["WEST"]]
    assert submission._WEED_STATE[0]["active"] == {}


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
    reset_controller()
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


def test_retired_ninth_cow_extension_never_mutates_the_route():
    obs = make_cow9_observation()
    action = {
        "farmer": ["PASS"],
        "hands": [],
        "market": [["BUY_SEED", "WHEAT", index + 1] for index in range(9)],
    }
    assert submission._ENABLE_NINTH_COW is False
    assert submission._guarded_demand_cow9(
        obs, deepcopy(action), 289
    ) == action


def test_low_route_repairs_partial_cow_purchases_through_ten_cows():
    reset_controller()
    expected = {0: 2, 73: 3, 120: 4, 168: 6, 216: 8, 264: 10}
    assert {
        step: submission._cow_target_after_buy(step)
        for step in expected
    } == expected

    obs = make_observation(step=264, money=2200)
    for index in range(7):
        x, y = index % 5, index // 5
        obs["farms"][0]["tiles"][y][x] = {
            "kind": "PASTURE",
            "animal": "COW",
        }
    repaired = submission._reconcile_scheduled_cows(
        obs, deepcopy(submission._LOW_ACTIONS[264]), 264
    )
    assert next(
        order
        for order in repaired["market"]
        if order[:2] == ["BUY_ANIMAL", "COW"]
    ) == ["BUY_ANIMAL", "COW", 3]


def test_high_route_stops_its_cow_target_at_six():
    reset_controller()
    submission._ACTIONS = submission._HIGH_ACTIONS
    assert submission._cow_target_after_buy(168) == 6
    assert submission._cow_target_after_buy(216) is None
    assert submission._cow_target_after_buy(264) is None


def test_one_turn_lead_conserves_the_scheduled_quantity():
    reset_controller()
    obs = make_observation(step=147, shed={"WOOL": 6})
    state = submission._fr_state(obs, 147)
    action = submission._front_run(
        {"farmer": ["PASS"], "hands": [], "market": []},
        obs,
        state,
        147,
    )

    assert action["market"] == [["SELL", "WOOL", 6]]
    assert state == {
        "last_step": 147,
        "due_step": 148,
        "due": {"WOOL": 6},
    }
    repaid = submission._repay(
        deepcopy(submission._ACTIONS[148]), state, 148
    )
    assert ["SELL", "WOOL", 6] not in repaid["market"]


def test_one_turn_lead_precedes_existing_market_outflows():
    reset_controller()
    obs = make_observation(step=147, shed={"WOOL": 6})
    state = submission._fr_state(obs, 147)
    action = submission._front_run(
        {
            "farmer": ["PASS"],
            "hands": [],
            "market": [["BUY_SEED", "WHEAT", 1]],
        },
        obs,
        state,
        147,
    )

    assert action["market"][:2] == [
        ["SELL", "WOOL", 6],
        ["BUY_SEED", "WHEAT", 1],
    ]


def test_one_turn_lead_also_covers_wheat_and_fertilizer_collisions():
    assert "WHEAT" in submission._FR_ITEMS
    assert "FERTILIZER" in submission._FR_ITEMS


def test_one_turn_lead_skips_a_town_demand_turn():
    reset_controller()
    obs = make_observation(
        step=196,
        shed={"MILK": 12},
        shops=["SMOOTHIE_SHOP"],
    )
    state = submission._fr_state(obs, 196)
    action = submission._front_run(
        {"farmer": ["PASS"], "hands": [], "market": []},
        obs,
        state,
        196,
    )

    assert action["market"] == []
    assert state["due"] == {}


def test_h4_observation_activates_only_from_clean_public_supply():
    reset_controller()
    obs = make_observation(step=194)
    state = submission._new_meta_state()
    state.update(
        {
            "clone_confidence": 3,
            "prev_market_inv": {product: 10000 for product in PRODUCTS},
            "prev_prices": {product: 100 for product in PRODUCTS},
            "prev_action": {
                "farmer": ["PASS"],
                "hands": [],
                "market": [["SELL", "MILK", 12]],
            },
            "prev_shed": {"MILK": 12},
            "prev_town_shops": (),
            "prev_step": 193,
        }
    )
    obs["market"]["inventory"]["MILK"] += 24

    submission._meta_observe_h4(obs, 194, state)

    assert state["h4_active"] is True
    assert state["h4_evidence"] == 1


def test_h4_observation_ignores_the_one_dollar_price_floor():
    reset_controller()
    obs = make_observation(step=194)
    state = submission._new_meta_state()
    state.update(
        {
            "clone_confidence": 3,
            "prev_market_inv": {product: 10000 for product in PRODUCTS},
            "prev_prices": {**{product: 100 for product in PRODUCTS}, "MILK": 1},
            "prev_action": {
                "farmer": ["PASS"],
                "hands": [],
                "market": [["SELL", "MILK", 12]],
            },
            "prev_shed": {"MILK": 12},
            "prev_town_shops": (),
            "prev_step": 193,
        }
    )
    obs["market"]["inventory"]["MILK"] += 24

    submission._meta_observe_h4(obs, 194, state)

    assert state["h4_active"] is False


def test_confirmed_h4_counter_preempts_the_matching_sale_by_seven_turns():
    reset_controller()
    obs = make_observation(step=141, shed={"WOOL": 6})
    state = submission._new_meta_state()
    state["h4_active"] = True
    action = {"farmer": ["PASS"], "hands": [], "market": []}

    assert submission._meta_h5_counter(action, obs, 141, state)
    assert action["market"] == [["SELL", "WOOL", 6]]
    assert state["h5_due"] == {148: {"WOOL": 6}}


def test_h7_prepayment_is_not_sold_again_by_the_one_turn_lead():
    reset_controller()
    meta = submission._new_meta_state()
    meta["h4_active"] = True
    early = {"farmer": ["PASS"], "hands": [], "market": []}
    assert submission._meta_h5_counter(
        early,
        make_observation(step=141, shed={"WOOL": 6}),
        141,
        meta,
    )

    fr_state = submission._fr_state(
        make_observation(step=147, shed={"WOOL": 6}), 147
    )
    one_turn = submission._front_run(
        {"farmer": ["PASS"], "hands": [], "market": []},
        make_observation(step=147, shed={"WOOL": 6}),
        fr_state,
        147,
        prepaid=meta["h5_due"][148],
    )
    assert one_turn["market"] == []

    due = deepcopy(submission._ACTIONS[148])
    submission._meta_repay_h5(due, 148, meta)
    assert ["SELL", "WOOL", 6] not in due["market"]
    assert meta["h5_due"] == {}


def test_h5_counter_does_not_evict_a_full_market_queue():
    reset_controller()
    market = [["BUY_SEED", "WHEAT", index + 1] for index in range(10)]
    action = {"farmer": ["PASS"], "hands": [], "market": deepcopy(market)}
    obs = make_observation(step=141, shed={"WOOL": 6})
    state = submission._new_meta_state()
    state["h4_active"] = True

    assert not submission._meta_h5_counter(action, obs, 141, state)
    assert action["market"] == market


def test_h5_counter_skips_when_current_town_demand_resets_the_edge():
    reset_controller()
    obs = make_observation(
        step=144,
        shed={"WOOL": 6},
        shops=["YARN_STORE"],
    )
    state = submission._new_meta_state()
    state["h4_active"] = True
    action = {"farmer": ["PASS"], "hands": [], "market": []}

    assert not submission._meta_h5_counter(action, obs, 144, state)
    assert action["market"] == []


def test_post_weed_regime_extends_meta_horizon_without_identity_routing(
    monkeypatch,
):
    reset_controller()
    monkeypatch.setattr(submission, "_META_SALES", {10: {"WOOL": 6}})
    obs = make_observation(step=1, shed={"WOOL": 6})
    state = submission._new_meta_state()
    state["clone_confidence"] = 1
    baseline = {"farmer": ["PASS"], "hands": [], "market": []}

    submission._meta_front_run(baseline, obs, 1, state)
    assert baseline["market"] == []

    submission._WEED_STATE[0]["post_recovery_market_regime"] = True
    recovered = {"farmer": ["PASS"], "hands": [], "market": []}
    submission._meta_front_run(recovered, obs, 1, state)

    assert recovered["market"] == [["SELL", "WOOL", 6]]


def test_v5_market_finalize_prioritizes_premium_and_merges_duplicates():
    reset_controller()
    action = {
        "farmer": ["PASS"],
        "hands": [],
        "market": [
            ["BUY_SEED", "WHEAT", 1],
            ["SELL", "STRAWBERRY", 2],
            ["SELL", "WHEAT", 5],
            ["SELL", "STRAWBERRY", 3],
        ],
    }

    finalized = submission._v5_market_finalize(
        deepcopy(action), make_observation(step=100)
    )

    strawberry = [
        order
        for order in finalized["market"]
        if order[:2] == ["SELL", "STRAWBERRY"]
    ]
    assert finalized["market"][0][0] == "SELL"
    assert strawberry == [["SELL", "STRAWBERRY", 5]]
    assert len(finalized["market"]) <= 10


def test_projected_shed_applies_pickup_before_a_later_drop():
    reset_controller()
    obs = make_observation(
        step=100,
        shed={"WHEAT": 100},
        hands=[[4, 4]],
        inventories=[{}, {"MILK": 2}],
    )
    action = {
        "farmer": ["PICKUP", "WHEAT", 10],
        "hands": [["DROP"]],
        "market": [],
    }

    projected = submission._v5_projected_shed(obs, action)

    assert projected["WHEAT"] == 90
    assert projected["MILK"] == 2


def test_market_rank_uses_executable_stock_including_same_turn_place():
    reset_controller()
    obs = make_observation(
        step=100,
        shed={"STRAWBERRY": 2},
        inventories=[{"WOOL": 5}],
    )
    orders = [
        ["SELL", "WOOL", 74],
        ["SELL", "STRAWBERRY", 2],
    ]
    without_place = submission._v5_market_finalize(
        {"farmer": ["PASS"], "hands": [], "market": orders},
        obs,
    )
    with_place = submission._v5_market_finalize(
        {
            "farmer": ["PLACE", "WOOL", 5],
            "hands": [],
            "market": orders,
        },
        obs,
    )

    assert without_place["market"][0][:2] == ["SELL", "STRAWBERRY"]
    assert with_place["market"][0][:2] == ["SELL", "WOOL"]


def test_terminal_seed_prune_removes_the_order_instead_of_emitting_zero():
    reset_controller()
    submission._ACTIONS = submission._LOW_ACTIONS

    pruned = submission._v5_prune_terminal_wheat_seed(
        deepcopy(submission._LOW_ACTIONS[670]), 670
    )

    assert not [
        order
        for order in pruned["market"]
        if order[:2] == ["BUY_SEED", "WHEAT"]
    ]
    assert all(len(order) < 3 or int(order[2]) > 0 for order in pruned["market"])


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


def test_same_nonzero_observation_retry_is_idempotent_and_copy_safe():
    reset_controller()
    submission._META_STATE[0]["h4_active"] = True
    obs = make_observation(step=141, shed={"WOOL": 6})

    first = agent(deepcopy(obs))
    state_after_first = deepcopy(submission._META_STATE[0])
    first["market"].append(["SELL", "MILK", 999])
    retry = deepcopy(obs)
    retry["remainingOverageTime"] = 12.5
    second = agent(retry)

    assert ["SELL", "WOOL", 6] in second["market"]
    assert ["SELL", "MILK", 999] not in second["market"]
    assert submission._META_STATE[0] == state_after_first


def test_same_step_with_changed_game_state_is_recomputed():
    reset_controller()
    stocked = make_observation(step=147, shed={"WOOL": 6})
    empty = make_observation(step=147, shed={})

    first = agent(stocked)
    second = agent(empty)

    assert ["SELL", "WOOL", 6] in first["market"]
    assert ["SELL", "WOOL", 6] not in second["market"]


def test_action_cache_is_isolated_between_player_seats():
    reset_controller()
    first = agent(make_observation(step=147, player=0, shed={"WOOL": 6}))
    second = agent(make_observation(step=147, player=1, shed={}))

    assert ["SELL", "WOOL", 6] in first["market"]
    assert ["SELL", "WOOL", 6] not in second["market"]


def test_invalid_observation_fails_safe():
    reset_controller()
    assert agent({}) == {"farmer": ["PASS"], "hands": [], "market": []}

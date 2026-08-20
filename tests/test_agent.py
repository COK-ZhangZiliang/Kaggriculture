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


def make_legacy_observation(*, step=24, player=0, shops=None):
    obs = make_observation(
        step=step,
        player=player,
        shops=shops or ["BAKERY"],
    )
    opponent = obs["farms"][1 - player]
    opponent["money"] = 12
    opponent["hands"] = []
    opponent["tiles"] = [[None for _ in range(10)] for _ in range(10)]
    tiles = [
        {"kind": "PASTURE", "animal": "COW"},
        *[
            {"kind": "PASTURE", "animal": "SHEEP"}
            for _ in range(4)
        ],
        *[
            {"kind": "PLANT", "crop": "MELON"}
            for _ in range(5)
        ],
        *[
            {"kind": "PLANT", "crop": "WHEAT"}
            for _ in range(5)
        ],
    ]
    for index, tile in enumerate(tiles):
        opponent["tiles"][index // 10][index % 10] = tile
    return obs


def reset_controller():
    submission._ACTIONS = submission._ACTIONS_8C6S_3Q
    submission._META_SALES = submission._V7_CURRENT_SALES["8c6s_3q"]
    submission._ROUTE_STATE.clear()
    submission._ROUTE_STATE.update(
        {
            0: {"last_step": -1, "legacy": None, "label": None},
            1: {"last_step": -1, "legacy": None, "label": None},
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


def test_routes_are_frozen_with_route_specific_sale_schedules():
    current = {
        "10c4s_3q": (
            "60cd665cbcafdc3186256f2aff7004968b127ecdccb1c16de1265885d422111c",
            (10, 4),
        ),
        "8c6s_3q": (
            "2483809ada657c092e98e2b854ded9539a9b9a597723f1f4027a02ea97faa6aa",
            (8, 6),
        ),
        "6c8s_3q": (
            "25f62869f42ce905b882b4acc66c1fb2061d89b6293ac42c24e030de60460942",
            (6, 8),
        ),
        "6c12s_4q_first_yarn": (
            "64e81ecf1788855ab65e58671042c0c241dbc63accc972eb73caed8b637da5d2",
            (6, 12),
        ),
        "6c12s_4q_second_yarn": (
            "a072f831ccca5ba0e0ca4b6d38d1eec3994cc34627b8c748831f027c9e066d9d",
            (6, 12),
        ),
    }
    legacy_hashes = {
        "10c4s_3q": "25b683c5d82e120b7da51b50128ddd8c9966a933c38f53421b23f9c6785fd6de",
        "8c6s_3q": "96f5164bece882a2b943e843f6208e8b16377a756df0d017ea3159fa167b7199",
        "6c8s_3q": "3ccd016720dde7d921decf1caeebaac057390fca0f3c19906e4a94b4a20b6062",
        "6c12s_4q_first_yarn": current["6c12s_4q_first_yarn"][0],
        "6c12s_4q_second_yarn": current["6c12s_4q_second_yarn"][0],
    }
    for label, (route_hash, animal_buys) in current.items():
        route = submission._V7_CURRENT_ROUTES[label]
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
        assert (
            submission._V7_CURRENT_SALES[label]
            == submission._v7_sales_schedule(route)
        )

    for label, route in submission._V7_LEGACY_ROUTES.items():
        actual_hash = hashlib.sha256(
            json.dumps(route, separators=(",", ":")).encode()
        ).hexdigest()
        assert len(route) == 719
        assert actual_hash == legacy_hashes[label]
        assert (
            submission._V7_LEGACY_SALES[label]
            == submission._v7_sales_schedule(route)
        )

    routes = submission._V7_CURRENT_ROUTES
    assert routes["8c6s_3q"][:264] == routes["10c4s_3q"][:264]
    assert routes["8c6s_3q"][:216] == routes["6c8s_3q"][:216]
    assert (
        routes["8c6s_3q"][:120]
        == routes["6c12s_4q_first_yarn"][:120]
    )
    assert (
        routes["8c6s_3q"][:72]
        == routes["6c12s_4q_second_yarn"][:72]
    )


def test_legacy_route_uses_only_the_validated_public_layout():
    reset_controller()
    route, sales = submission._select_route(
        make_legacy_observation(),
        24,
    )
    assert route is submission._LEGACY_ACTIONS_8C6S_3Q
    assert sales is submission._V7_LEGACY_SALES["8c6s_3q"]

    reset_controller()
    mismatch = make_legacy_observation()
    mismatch["farms"][1]["money"] = 13
    assert (
        submission._select_route(mismatch, 24)[0]
        is submission._ACTIONS_8C6S_3Q
    )


def test_legacy_route_decision_is_sticky_after_the_opening_window():
    reset_controller()
    assert (
        submission._select_route(make_legacy_observation(), 24)[0]
        is submission._LEGACY_ACTIONS_8C6S_3Q
    )
    later = make_observation(
        step=80,
        shops=["PIZZA_SHOP"],
    )
    route, sales = submission._select_route(later, 80)
    assert route is submission._LEGACY_ACTIONS_10C4S_3Q
    assert sales is submission._V7_LEGACY_SALES["10c4s_3q"]


def test_legacy_route_state_is_isolated_by_seat():
    reset_controller()
    assert (
        submission._select_route(
            make_legacy_observation(player=0),
            24,
        )[0]
        is submission._LEGACY_ACTIONS_8C6S_3Q
    )
    assert (
        submission._select_route(
            make_observation(
                step=24,
                player=1,
                shops=["BAKERY"],
            ),
            24,
        )[0]
        is submission._ACTIONS_8C6S_3Q
    )


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


def test_route_selector_maps_public_shop_prefixes_to_five_routes():
    cases = [
        (["YARN_STORE"], "6c12s_4q_first_yarn"),
        (["BAKERY", "YARN_STORE"], "6c12s_4q_second_yarn"),
        (["BAKERY", "BRUNCH_SPOT", "YARN_STORE"], "6c8s_3q"),
        (["BAKERY", "PIZZA_SHOP"], "10c4s_3q"),
        (["BAKERY", "BRUNCH_SPOT", "PET_CAFE"], "8c6s_3q"),
    ]
    for shops, label in cases:
        reset_controller()
        route, sales = submission._select_route(
            make_observation(step=216, shops=shops), 216
        )
        assert route is submission._V7_CURRENT_ROUTES[label]
        assert sales is submission._V7_CURRENT_SALES[label]


def test_route_selection_is_staged_isolated_and_resets_between_games():
    reset_controller()
    first_yarn = make_observation(
        step=120,
        player=0,
        shops=["YARN_STORE"],
    )
    assert (
        submission._select_route(first_yarn, 120)[0]
        is submission._ACTIONS_6C12S_4Q_FIRST_YARN
    )
    later_yarn = make_observation(
        step=216,
        player=0,
        shops=["YARN_STORE", "PIZZA_SHOP", "BRUNCH_SPOT"],
    )
    assert (
        submission._select_route(later_yarn, 216)[0]
        is submission._ACTIONS_6C12S_4Q_FIRST_YARN
    )

    milk_other = make_observation(
        step=216,
        player=1,
        shops=["BAKERY", "PIZZA_SHOP"],
    )
    assert (
        submission._select_route(milk_other, 216)[0]
        is submission._ACTIONS_10C4S_3Q
    )
    reset_obs = make_observation(step=0, player=0)
    assert (
        submission._select_route(reset_obs, 0)[0]
        is submission._ACTIONS_8C6S_3Q
    )


def test_third_shop_can_refine_route_before_the_shared_prefix_diverges():
    reset_controller()
    before = make_observation(
        step=168,
        shops=["BAKERY", "BRUNCH_SPOT"],
    )
    assert (
        submission._select_route(before, 168)[0]
        is submission._ACTIONS_8C6S_3Q
    )
    after = make_observation(
        step=216,
        shops=["BAKERY", "BRUNCH_SPOT", "PIZZA_SHOP"],
    )
    assert (
        submission._select_route(after, 216)[0]
        is submission._ACTIONS_10C4S_3Q
    )
    assert (
        submission._ACTIONS_8C6S_3Q[:216]
        == submission._ACTIONS_10C4S_3Q[:216]
    )


def test_route_selection_ignores_identity_metadata():
    actions = []
    for seed, opponent_name in ((11, "alpha"), (987654321, "beta")):
        reset_controller()
        obs = make_observation(
            step=216,
            shops=["YARN_STORE", "BAKERY"],
        )
        obs["seed"] = seed
        obs["opponent_name"] = opponent_name
        obs["EpisodeId"] = seed + 100
        actions.append(submission._select_route(obs, 216)[0][216])
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
    submission._ACTIONS = submission._ACTIONS_10C4S_3Q
    obs = make_observation(step=149, money=1235)
    obs["private"]["seeds"] = {
        "WHEAT": 2,
        "CARROT": 0,
        "STRAWBERRY": 3,
        "MELON": 8,
    }

    clipped = submission._clip_seed_surplus(
        deepcopy(submission._ACTIONS_10C4S_3Q[149]), obs, 149
    )

    assert clipped["market"] == [
        ["BUY_PRODUCT", "WHEAT", 2],
        ["BUY_SEED", "CARROT", 1],
    ]


def test_seed_clip_does_not_buy_for_an_atomic_plant_that_already_failed():
    reset_controller()
    submission._ACTIONS = submission._ACTIONS_10C4S_3Q
    obs = make_observation(step=525)
    obs["private"]["seeds"] = {"CARROT": 0}

    clipped = submission._clip_seed_surplus(
        deepcopy(submission._ACTIONS_10C4S_3Q[525]), obs, 525
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
    route = deepcopy(submission._ACTIONS_10C4S_3Q)
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
    route = deepcopy(submission._ACTIONS_10C4S_3Q)
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
    submission._ACTIONS = submission._ACTIONS_10C4S_3Q
    expected = {0: 2, 72: 3, 120: 4, 168: 6, 216: 8, 264: 10}
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
        obs, deepcopy(submission._ACTIONS_10C4S_3Q[264]), 264
    )
    assert next(
        order
        for order in repaired["market"]
        if order[:2] == ["BUY_ANIMAL", "COW"]
    ) == ["BUY_ANIMAL", "COW", 3]


def test_high_route_stops_its_cow_target_at_six():
    reset_controller()
    submission._ACTIONS = submission._ACTIONS_6C8S_3Q
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
    submission._ACTIONS = submission._ACTIONS_10C4S_3Q

    pruned = submission._v5_prune_terminal_wheat_seed(
        deepcopy(submission._ACTIONS_10C4S_3Q[670]), 670
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


def test_alternating_seats_keep_route_schedule_and_cached_action_isolated():
    reset_controller()
    first_yarn = make_observation(
        step=216,
        player=0,
        shops=["YARN_STORE", "BAKERY", "PET_CAFE"],
    )
    milk_route = make_observation(
        step=216,
        player=1,
        shops=["BAKERY", "PIZZA_SHOP", "PET_CAFE"],
    )

    first = agent(deepcopy(first_yarn))
    agent(deepcopy(milk_route))
    retry = agent(deepcopy(first_yarn))

    assert retry == first
    assert submission._ROUTE_STATE[0]["label"] == "6c12s_4q_first_yarn"
    assert submission._ROUTE_STATE[1]["label"] == "10c4s_3q"

    next_obs = make_observation(
        step=217,
        player=0,
        shops=["YARN_STORE", "BAKERY", "PET_CAFE"],
    )
    agent(next_obs)
    assert submission._ACTIONS is submission._ACTIONS_6C12S_4Q_FIRST_YARN
    assert (
        submission._META_SALES
        is submission._V7_CURRENT_SALES["6c12s_4q_first_yarn"]
    )


def test_invalid_observation_fails_safe():
    reset_controller()
    assert agent({}) == {"farmer": ["PASS"], "hands": [], "market": []}

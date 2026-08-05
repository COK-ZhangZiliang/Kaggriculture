from copy import deepcopy

from main import CROP, agent


def make_observation(*, day=0, hour=0, player=0, seeds=0, shed=None, hands=None):
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
        "hands": deepcopy(hands or []),
        "unlocked_quadrants": ["NW"],
        "hires_today": 0,
    }
    other = deepcopy(farm)
    farms = [deepcopy(farm), deepcopy(other)]
    inventories = [{} for _ in range(1 + len(hands or []))]
    return {
        "player": player,
        "day": day,
        "hour": hour,
        "farms": farms,
        "market": {"inventory": {}, "prices": {}},
        "town": {"unlocked_shops": []},
        "private": {
            "shed": deepcopy(shed or {}),
            "seeds": {CROP: seeds},
            "inventories": inventories,
        },
    }


def carrot(*, planted_day=0, watered_today=False, yield_units=1):
    return {
        "kind": "PLANT",
        "crop": CROP,
        "planted_day": planted_day,
        "watered_today": watered_today,
        "consecutive_unwatered": 0,
        "yield_units": yield_units,
        "max_lifespan_step": 96,
        "fertilized_until_day": -1,
    }


def test_initial_turn_buys_seeds_and_hires_four_hands():
    action = agent(make_observation())

    assert action["farmer"] == ["PASS"]
    assert action["hands"] == []
    assert ["BUY_SEED", CROP, 25] in action["market"]
    assert action["market"].count(["HIRE"]) == 4
    assert len(action["market"]) <= 10


def test_agent_uses_current_player_farm_and_plants_available_seed():
    obs = make_observation(player=1, seeds=1, hour=1)
    obs["farms"][0]["tiles"][4][4] = {"kind": "WEED"}

    action = agent(obs)

    assert action["farmer"] == ["PLANT", CROP]


def test_new_carrot_is_watered_before_the_day_ends():
    obs = make_observation(seeds=0, hour=2)
    obs["farms"][0]["tiles"][4][4] = carrot(planted_day=0)

    assert agent(obs)["farmer"] == ["WATER"]


def test_peak_carrot_is_watered_then_harvested():
    obs = make_observation(day=3, hour=2)
    obs["farms"][0]["tiles"][4][4] = carrot(
        planted_day=0,
        watered_today=False,
        yield_units=2,
    )
    assert agent(obs)["farmer"] == ["WATER"]

    obs["farms"][0]["tiles"][4][4]["watered_today"] = True
    obs["farms"][0]["tiles"][4][4]["yield_units"] = 3
    assert agent(obs)["farmer"] == ["HARVEST"]


def test_parallel_planting_never_exceeds_seed_budget():
    hands = [[4, 3], [4, 2], [4, 1], [4, 0]]
    obs = make_observation(seeds=2, hour=1, hands=hands)

    action = agent(obs)
    unit_actions = [action["farmer"], *action["hands"]]

    plant_count = sum(
        unit_action[:2] == ["PLANT", CROP] for unit_action in unit_actions
    )
    assert plant_count == 2


def test_final_day_inventory_returns_to_shed_and_is_sold():
    obs = make_observation(day=29, hour=10, shed={CROP: 2})
    obs["farms"][0]["farmer"] = [4, 4]
    obs["private"]["inventories"][0] = {CROP: 3}

    action = agent(obs)

    assert action["farmer"] == ["DROP"]
    assert ["SELL", CROP, 100] in action["market"]


def test_last_turn_does_not_start_work_that_cannot_be_liquidated():
    obs = make_observation(day=29, hour=22, seeds=0)
    obs["farms"][0]["farmer"] = [0, 4]
    obs["farms"][0]["tiles"][4][0] = carrot(
        planted_day=20,
        watered_today=True,
        yield_units=3,
    )

    assert agent(obs)["farmer"] == ["PASS"]

    obs["private"]["inventories"][0] = {CROP: 3}
    assert agent(obs)["farmer"] == ["PASS"]


def test_final_day_harvest_requires_enough_time_to_drop():
    obs = make_observation(day=29, hour=21, seeds=0)
    obs["farms"][0]["tiles"][4][4] = carrot(
        planted_day=20,
        watered_today=True,
        yield_units=3,
    )

    assert agent(obs)["farmer"] == ["HARVEST"]


def test_invalid_observation_fails_safe():
    assert agent({}) == {"farmer": ["PASS"], "hands": [], "market": []}

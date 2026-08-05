"""Deterministic carrot-field baseline for the Kaggriculture competition.

Keep ``agent`` as the final top-level callable. Kaggle's local file loader uses
the last callable defined in a submission file as its entrypoint.
"""

CROP = "CARROT"
MAX_YIELD_DAY = 3
LAST_PLANT_DAY = 25
TARGET_SEED_STOCK = 25
ROW_BY_UNIT_INDEX = (4, 3, 2, 1, 0)
SHED_TILE = (4, 4)


def _pass_action(hand_count):
    return {
        "farmer": ["PASS"],
        "hands": [["PASS"] for _ in range(hand_count)],
        "market": [],
    }


def _move_towards(position, target):
    """Return one deterministic move, preferring vertical movement."""
    x, y = position
    target_x, target_y = target
    if y < target_y:
        return ["SOUTH"]
    if y > target_y:
        return ["NORTH"]
    if x < target_x:
        return ["EAST"]
    if x > target_x:
        return ["WEST"]
    return ["PASS"]


def _task_for_tile(tile, day, may_plant):
    """Return ``(priority, action)`` for one tile, or ``None``."""
    if isinstance(tile, dict) and tile.get("kind") == "PLANT":
        if tile.get("crop") != CROP:
            if not tile.get("watered_today", False):
                return (2, ["WATER"])
            if tile.get("yield_units", 0) > 0:
                return (3, ["HARVEST"])
            return None

        age = day - int(tile.get("planted_day", day))
        if age >= MAX_YIELD_DAY:
            # Water at peak age before harvesting to collect the final bonus.
            if not tile.get("watered_today", False):
                return (0, ["WATER"])
            if tile.get("yield_units", 0) > 0:
                return (1, ["HARVEST"])
        if not tile.get("watered_today", False):
            return (2, ["WATER"])
        return None

    if isinstance(tile, dict) and tile.get("kind") == "WEED":
        return (3, ["DIG"])
    if tile is None and may_plant:
        return (4, ["PLANT", CROP])
    return None


def _unit_position(farm, unit_index):
    if unit_index == 0:
        return tuple(farm.get("farmer", SHED_TILE))
    hands = farm.get("hands", [])
    hand_index = unit_index - 1
    if hand_index >= len(hands):
        return SHED_TILE
    return tuple(hands[hand_index])


def _inventory_for_unit(private, unit_index):
    inventories = private.get("inventories", [])
    if unit_index < len(inventories) and isinstance(
        inventories[unit_index],
        dict,
    ):
        return inventories[unit_index]
    return {}


def _plan_liquidation_unit(farm, private, unit_index, hour):
    """Harvest only when the produce can still be sold by hour 22."""
    position = _unit_position(farm, unit_index)
    inventory = _inventory_for_unit(private, unit_index)
    distance_to_shed = abs(position[0] - SHED_TILE[0]) + abs(
        position[1] - SHED_TILE[1]
    )

    if sum(inventory.values()) > 0:
        if position == SHED_TILE:
            return ["DROP"]
        if hour + distance_to_shed <= 22:
            return _move_towards(position, SHED_TILE)
        return ["PASS"]

    row_index = min(unit_index, len(ROW_BY_UNIT_INDEX) - 1)
    row = ROW_BY_UNIT_INDEX[row_index]
    tiles = farm.get("tiles", [])
    if row >= len(tiles):
        return ["PASS"]

    candidates = []
    for x in range(min(5, len(tiles[row]))):
        tile = tiles[row][x]
        if not (
            isinstance(tile, dict)
            and tile.get("kind") == "PLANT"
            and tile.get("crop") == CROP
            and int(tile.get("yield_units", 0)) > 0
        ):
            continue
        distance_to_crop = abs(position[0] - x) + abs(position[1] - row)
        crop_to_shed = abs(x - SHED_TILE[0]) + abs(row - SHED_TILE[1])
        final_drop_hour = hour + distance_to_crop + crop_to_shed + 1
        if final_drop_hour <= 22:
            candidates.append(
                (
                    distance_to_crop + crop_to_shed,
                    -int(tile.get("yield_units", 0)),
                    x,
                )
            )

    if not candidates:
        return ["PASS"]
    _, _, target_x = min(candidates)
    target = (target_x, row)
    if position == target:
        return ["HARVEST"]
    return _move_towards(position, target)


def _plan_unit(farm, private, unit_index, day, seed_budget):
    """Plan one unit and return ``(action, remaining_seed_budget)``."""
    position = _unit_position(farm, unit_index)

    row_index = min(unit_index, len(ROW_BY_UNIT_INDEX) - 1)
    row = ROW_BY_UNIT_INDEX[row_index]
    tiles = farm.get("tiles", [])
    if row >= len(tiles):
        return ["PASS"], seed_budget

    may_plant = day <= LAST_PLANT_DAY and seed_budget > 0
    candidates = []
    for x in range(min(5, len(tiles[row]))):
        task = _task_for_tile(tiles[row][x], day, may_plant)
        if task is None:
            continue
        priority, action = task
        distance = abs(position[0] - x) + abs(position[1] - row)
        candidates.append((priority, distance, x, action))

    if not candidates:
        return ["PASS"], seed_budget

    _, _, target_x, action = min(candidates)
    target = (target_x, row)
    if position != target:
        return _move_towards(position, target), seed_budget
    if action[:2] == ["PLANT", CROP]:
        return action, seed_budget - 1
    return action, seed_budget


def _market_plan(private, day, hour, planned_plants):
    shed = private.get("shed", {})
    seeds = private.get("seeds", {})
    market = []

    carrot_stock = int(shed.get(CROP, 0))
    if day >= 29:
        # Unit actions run before market orders. Requesting the shed limit sells
        # both existing stock and carrots DROPped earlier in this turn; the
        # interpreter stops the order cleanly when the shed becomes empty.
        market.append(["SELL", CROP, 100])
    elif carrot_stock > 0:
        market.append(["SELL", CROP, carrot_stock])

    seeds_after_actions = max(0, int(seeds.get(CROP, 0)) - planned_plants)
    if day <= LAST_PLANT_DAY and seeds_after_actions < 10:
        market.append(["BUY_SEED", CROP, TARGET_SEED_STOCK - seeds_after_actions])

    if hour == 0:
        market.extend([["HIRE"] for _ in range(4)])

    return market[:10]


def agent(obs):
    """Return one deterministic Kaggriculture action."""
    farms = obs.get("farms", [])
    player = int(obs.get("player", 0))
    private = obs.get("private", {}) or {}
    if not farms or not 0 <= player < len(farms):
        return _pass_action(0)

    farm = farms[player]
    day = int(obs.get("day", 0))
    hour = int(obs.get("hour", 0))
    hand_count = len(farm.get("hands", []))
    starting_seeds = int(private.get("seeds", {}).get(CROP, 0))
    seed_budget = starting_seeds
    unit_actions = []

    for unit_index in range(hand_count + 1):
        if day >= 29:
            unit_actions.append(
                _plan_liquidation_unit(farm, private, unit_index, hour)
            )
            continue
        action, seed_budget = _plan_unit(
            farm,
            private,
            unit_index,
            day,
            seed_budget,
        )
        unit_actions.append(action)

    planned_plants = starting_seeds - seed_budget
    return {
        "farmer": unit_actions[0],
        "hands": unit_actions[1:],
        "market": _market_plan(private, day, hour, planned_plants),
    }

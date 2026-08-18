from importlib.metadata import version

import pytest
from kaggle_environments import make

from main import agent


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


def assert_complete_episode(players, seed, candidate_seat):
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed},
        debug=False,
    )
    steps = env.run(players)
    final = steps[-1]

    assert version("kaggle-environments") == "1.32.7"
    assert len(steps) == 720
    assert [state.status for state in final] == ["DONE", "DONE"]
    assert all(state.reward is not None for state in final)
    assert all(state.reward >= 0 for state in final)
    assert not [
        (turn, player, log.get("stderr"))
        for turn, logs in enumerate(env.logs)
        for player, log in enumerate(logs)
        if log.get("stderr")
    ]
    candidate_private = final[candidate_seat].observation.private
    assert all(candidate_private.shed.get(product, 0) == 0 for product in SELLABLE)
    assert all(
        sum(
            quantity
            for product, quantity in inventory.items()
            if product in SELLABLE
        )
        == 0
        for inventory in candidate_private.inventories
    )
    return [state.reward for state in final]


def test_full_episode_against_starter():
    rewards = assert_complete_episode(
        [agent, "starter"],
        seed=20260805,
        candidate_seat=0,
    )
    assert rewards[0] > rewards[1]


@pytest.mark.parametrize(
    ("candidate_seat", "seed"),
    ((0, 20260806), (1, 20260807)),
)
def test_submission_file_loader_from_both_seats(candidate_seat, seed):
    players = ["main.py", "starter"]
    if candidate_seat == 1:
        players.reverse()
    rewards = assert_complete_episode(players, seed, candidate_seat)
    assert rewards[candidate_seat] > rewards[1 - candidate_seat]


def test_self_play_completes_without_runtime_errors():
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": 20260808},
        debug=False,
    )
    steps = env.run(["main.py", "main.py"])
    final = steps[-1]

    assert len(steps) == 720
    assert [state.status for state in final] == ["DONE", "DONE"]
    assert all(state.reward is not None and state.reward > 0 for state in final)
    assert not [
        (turn, player, log.get("stderr"))
        for turn, logs in enumerate(env.logs)
        for player, log in enumerate(logs)
        if log.get("stderr")
    ]

from importlib.metadata import version

from kaggle_environments import make

from main import CROP, agent


def assert_complete_episode(players, seed):
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed},
        debug=False,
    )
    steps = env.run(players)
    final = steps[-1]

    assert version("kaggle-environments") == "1.32.4"
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
    baseline_private = final[0].observation.private
    assert baseline_private.shed.get(CROP, 0) == 0
    assert all(
        sum(inventory.values()) == 0
        for inventory in baseline_private.inventories
    )


def test_full_episode_against_starter():
    assert_complete_episode([agent, "starter"], seed=20260805)


def test_submission_file_loader():
    assert_complete_episode(["main.py", "starter"], seed=20260806)

import json

from scripts.analyze_failure_replays import _market_summary, analyze


def _tiles():
    return [[None for _ in range(10)] for _ in range(10)]


def _observation(*, step, money=(100, 100), hands=(0, 0), private=None):
    farms = [
        {
            "money": money[seat],
            "tiles": _tiles(),
            "farmer": [4, 4],
            "hands": [[4, 4] for _ in range(hands[seat])],
            "unlocked_quadrants": ["NW"],
        }
        for seat in (0, 1)
    ]
    return {
        "step": step,
        "farms": farms,
        "private": private or {"shed": {}, "inventories": [{}]},
    }


def _state(observation, action=None):
    return {
        "observation": observation,
        "action": action,
    }


def test_analysis_uses_next_frame_action_and_each_seats_private_state(tmp_path):
    before = [
        _observation(step=0, private={"shed": {"MILK": 3}, "inventories": [{}]}),
        _observation(step=0, private={"shed": {"WOOL": 7}, "inventories": [{}]}),
    ]
    after = [
        _observation(step=1, money=(130, 100), private={"shed": {}, "inventories": [{}]}),
        _observation(step=1, money=(130, 100), private={"shed": {"WOOL": 7}, "inventories": [{}]}),
    ]
    replay = {
        "info": {"EpisodeId": 7, "seed": 11, "TeamNames": ["ours", "opp"]},
        "rewards": [130, 100],
        "statuses": ["DONE", "DONE"],
        "steps": [
            [_state(before[0]), _state(before[1])],
            [
                _state(
                    after[0],
                    {"farmer": ["PASS"], "hands": [], "market": [["SELL", "MILK", 3]]},
                ),
                _state(after[1], {"farmer": ["PASS"], "hands": [], "market": []}),
            ],
        ],
    }
    path = tmp_path / "replay.json"
    path.write_text(json.dumps(replay), encoding="utf-8")

    row = analyze(path, "ours")

    assert row["own_market"]["requested_sales"] == {"MILK": 3}
    assert row["opponent_market"]["requested_sales"] == {}
    assert row["checkpoints"][-1]["stock"][1]["WOOL"] == 7


def test_unfilled_hire_is_reported_without_claiming_causal_impact():
    before = _observation(step=0, hands=(4, 0))
    after = _observation(step=1, hands=(4, 0))
    replay = {
        "steps": [
            [_state(before), _state(_observation(step=0))],
            [
                _state(
                    after,
                    {"farmer": ["PASS"], "hands": [], "market": [["HIRE"]]},
                ),
                _state(_observation(step=1), {"farmer": ["PASS"], "hands": [], "market": []}),
            ],
        ]
    }

    summary = _market_summary(replay, 0)

    assert summary["unfilled_hire_orders"] == [
        {
            "step": 0,
            "requested": 1,
            "successful": 0,
            "money_before": 100,
            "causal_impact": "unknown_without_untruncated_route",
        }
    ]
    assert "failed_hires" not in summary


def test_day_end_partial_animal_purchase_is_not_skipped():
    frames = []
    for step in range(25):
        own_private = {
            "shed": {"COW": 1 if step == 24 else 0},
            "inventories": [{}],
        }
        frames.append(
            [
                _state(_observation(step=step, private=own_private)),
                _state(_observation(step=step)),
            ]
        )
    frames[24][0]["action"] = {
        "farmer": ["PASS"],
        "hands": [],
        "market": [["BUY_ANIMAL", "COW", 2]],
    }
    frames[24][1]["action"] = {
        "farmer": ["PASS"],
        "hands": [],
        "market": [],
    }

    summary = _market_summary({"steps": frames}, 0)

    assert summary["unfilled_animal_orders"] == [
        {
            "step": 23,
            "item": "COW",
            "requested": 2,
            "successful": 1,
            "money_before": 100,
        }
    ]
    assert "positive_cashflow" not in summary
    assert summary["positive_net_money_delta"] == 0

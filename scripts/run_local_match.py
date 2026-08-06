#!/usr/bin/env python3
"""Run a full local Kaggriculture match and save a replay."""

import argparse
import json
import sys
from importlib.metadata import version
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from kaggle_environments import make

from main import agent


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--opponent",
        choices=("pass", "random", "starter"),
        default="starter",
    )
    parser.add_argument("--seed", type=int, default=20260805)
    parser.add_argument("--player", type=int, choices=(0, 1), default=0)
    parser.add_argument("--replay", type=Path)
    return parser.parse_args()


def main():
    args = parse_args()
    replay_path = args.replay or Path(
        f"replays/v2-p{args.player}-vs-{args.opponent}-seed-{args.seed}.json"
    )
    replay_path.parent.mkdir(parents=True, exist_ok=True)

    players = [agent, args.opponent] if args.player == 0 else [args.opponent, agent]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": args.seed},
        debug=False,
    )
    steps = env.run(players)
    final = steps[-1]
    statuses = [state.status for state in final]
    rewards = [state.reward for state in final]

    if len(steps) != 720:
        raise RuntimeError(f"expected 720 recorded states, got {len(steps)}")
    if statuses != ["DONE", "DONE"]:
        raise RuntimeError(f"episode did not finish cleanly: {statuses}")

    replay_path.write_text(
        json.dumps(env.toJSON(), separators=(",", ":")),
        encoding="utf-8",
    )
    candidate_reward = rewards[args.player]
    opponent_reward = rewards[1 - args.player]
    summary = {
        "environment": "kaggriculture",
        "kaggle_environments_version": version("kaggle-environments"),
        "opponent": args.opponent,
        "player": args.player,
        "seed": args.seed,
        "steps": len(steps),
        "statuses": statuses,
        "rewards": rewards,
        "result": (
            "win"
            if candidate_reward > opponent_reward
            else "loss"
            if candidate_reward < opponent_reward
            else "tie"
        ),
        "replay": str(replay_path),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

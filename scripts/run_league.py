#!/usr/bin/env python3
"""Evaluate a candidate against file-based agents from both seats."""

import argparse
import hashlib
import json
import statistics
import sys
import time
from importlib.metadata import version
from pathlib import Path

from kaggle_environments import make


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SEEDS = (20260811, 20260829, 20260907, 20260919)


def existing_python_file(value):
    path = Path(value).expanduser().resolve()
    if not path.is_file() or path.suffix != ".py":
        raise argparse.ArgumentTypeError(f"expected a Python file: {value}")
    return path


def opponent_spec(value):
    if "=" not in value:
        raise argparse.ArgumentTypeError("use NAME=/path/to/opponent.py")
    name, raw_path = value.split("=", 1)
    if not name.strip():
        raise argparse.ArgumentTypeError("opponent name cannot be empty")
    return name.strip(), existing_python_file(raw_path)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--candidate",
        type=existing_python_file,
        default=REPOSITORY_ROOT / "main.py",
    )
    parser.add_argument(
        "--opponent",
        type=opponent_spec,
        action="append",
        required=True,
        metavar="NAME=PATH",
    )
    parser.add_argument("--seed", type=int, action="append")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--require-positive-mean",
        action="store_true",
        help=(
            "fail unless every opponent finishes cleanly and has a strictly "
            "positive candidate mean margin"
        ),
    )
    args = parser.parse_args()
    duplicate_names = find_duplicate_names(name for name, _ in args.opponent)
    if duplicate_names:
        parser.error(
            "opponent names must be unique; repeated: "
            + ", ".join(duplicate_names)
        )
    return args


def find_duplicate_names(names):
    seen = set()
    duplicates = set()
    for name in names:
        if name in seen:
            duplicates.add(name)
        seen.add(name)
    return sorted(duplicates)


def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_match(candidate, opponent, opponent_name, seed, seat):
    players = [str(candidate), str(opponent)]
    if seat == 1:
        players.reverse()
    started = time.perf_counter()
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed},
        debug=False,
    )
    steps = env.run(players)
    final = steps[-1]
    statuses = [str(state.status) for state in final]
    rewards = [float(state.reward or 0) for state in final]
    candidate_reward = rewards[seat]
    opponent_reward = rewards[1 - seat]
    total = candidate_reward + opponent_reward
    return {
        "opponent": opponent_name,
        "seed": seed,
        "seat": seat,
        "states": len(steps),
        "statuses": statuses,
        "candidate_reward": candidate_reward,
        "opponent_reward": opponent_reward,
        "margin": candidate_reward - opponent_reward,
        "normalized_margin": (
            0.0 if total == 0 else 2 * (candidate_reward - opponent_reward) / total
        ),
        "result": (
            "win"
            if candidate_reward > opponent_reward
            else "loss"
            if candidate_reward < opponent_reward
            else "tie"
        ),
        "seconds": round(time.perf_counter() - started, 3),
        "stderr": [
            {"turn": turn, "player": player, "text": log.get("stderr")}
            for turn, logs in enumerate(env.logs)
            for player, log in enumerate(logs)
            if log.get("stderr")
        ],
    }


def summarize(rows, opponent_name):
    group = [row for row in rows if row["opponent"] == opponent_name]
    return {
        "opponent": opponent_name,
        "games": len(group),
        "wins": sum(row["result"] == "win" for row in group),
        "ties": sum(row["result"] == "tie" for row in group),
        "losses": sum(row["result"] == "loss" for row in group),
        "win_rate": sum(row["result"] == "win" for row in group) / len(group),
        "mean_candidate_reward": statistics.fmean(
            row["candidate_reward"] for row in group
        ),
        "mean_margin": statistics.fmean(row["margin"] for row in group),
        "median_normalized_margin": statistics.median(
            row["normalized_margin"] for row in group
        ),
        "all_done": all(
            row["states"] == 720
            and row["statuses"] == ["DONE", "DONE"]
            and not row["stderr"]
            for row in group
        ),
    }


def passes_gate(summaries, require_positive_mean=False):
    if not all(summary["all_done"] for summary in summaries):
        return False
    if require_positive_mean:
        return all(summary["mean_margin"] > 0 for summary in summaries)
    return True


def main():
    args = parse_args()
    seeds = tuple(args.seed or DEFAULT_SEEDS)
    rows = []
    for opponent_name, opponent in args.opponent:
        for seed in seeds:
            for seat in (0, 1):
                row = run_match(
                    args.candidate,
                    opponent,
                    opponent_name,
                    seed,
                    seat,
                )
                rows.append(row)
                print(json.dumps({"type": "match", **row}, sort_keys=True))

    summaries = [summarize(rows, name) for name, _ in args.opponent]
    manifest = {
        "environment": "kaggriculture",
        "kaggle_environments_version": version("kaggle-environments"),
        "candidate": str(args.candidate),
        "candidate_sha256": file_sha256(args.candidate),
        "opponents": [
            {"name": name, "path": str(path), "sha256": file_sha256(path)}
            for name, path in args.opponent
        ],
        "seeds": list(seeds),
        "both_seats": True,
    }
    result = {"manifest": manifest, "matches": rows, "summaries": summaries}
    print(json.dumps({"type": "summary", **result}, sort_keys=True))

    if args.output:
        output = args.output if args.output.is_absolute() else Path.cwd() / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2), encoding="utf-8")

    if not passes_gate(summaries, args.require_positive_mean):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

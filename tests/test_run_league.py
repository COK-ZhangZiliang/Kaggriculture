from scripts.run_league import find_duplicate_names, passes_gate


def test_find_duplicate_names_is_sorted_and_unique():
    assert find_duplicate_names(["rayk", "kaito", "rayk", "kaito", "bruce"]) == [
        "kaito",
        "rayk",
    ]


def test_default_gate_only_requires_clean_completion():
    summaries = [{"all_done": True, "mean_margin": -1.0}]

    assert passes_gate(summaries)


def test_positive_mean_gate_requires_every_opponent_to_be_positive():
    summaries = [
        {"all_done": True, "mean_margin": 10.0},
        {"all_done": True, "mean_margin": 0.0},
    ]

    assert not passes_gate(summaries, require_positive_mean=True)


def test_gate_always_rejects_incomplete_matches():
    summaries = [{"all_done": False, "mean_margin": 10.0}]

    assert not passes_gate(summaries)
    assert not passes_gate(summaries, require_positive_mean=True)

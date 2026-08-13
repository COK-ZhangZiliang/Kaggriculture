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
    summaries = [
        {
            "all_done": False,
            "games": 1,
            "wins": 1,
            "mean_margin": 10.0,
        }
    ]

    assert not passes_gate(summaries)
    assert not passes_gate(summaries, require_positive_mean=True)


def test_all_wins_gate_rejects_even_one_clean_loss():
    summaries = [
        {
            "all_done": True,
            "games": 8,
            "wins": 7,
            "mean_margin": 100.0,
        }
    ]

    assert not passes_gate(summaries, require_all_wins=True)


def test_all_wins_gate_accepts_only_a_clean_sweep():
    summaries = [
        {
            "all_done": True,
            "games": 8,
            "wins": 8,
            "mean_margin": 1.0,
        }
    ]

    assert passes_gate(summaries, require_all_wins=True)

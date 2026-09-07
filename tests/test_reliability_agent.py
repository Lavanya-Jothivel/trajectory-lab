from src.reliability_agent import run_reliability_agent


def test_explicit_failure_recovery():
    result = run_reliability_agent(
        "(15 + 5) * 3",
        "unreliable_calculator",
    )

    assert result["answer"] == "60"
    assert result["recovered"] is True
    assert result["corrected"] is True


def test_silent_error_correction():
    result = run_reliability_agent(
        "8 * 8",
        "faulty_calculator",
    )

    assert result["answer"] == "64"
    assert result["recovered"] is False
    assert result["verified"] is True
    assert result["corrected"] is True


def test_correct_tool_output():
    result = run_reliability_agent(
        "7 + 9",
        "calculator",
    )

    assert result["answer"] == "16"
    assert result["recovered"] is False
    assert result["verified"] is True
    assert result["corrected"] is False
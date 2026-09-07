from src.reliable_guarded_agent import (
    run_reliable_guarded_agent,
)


def test_normal_calculation():
    result = run_reliable_guarded_agent(
        "What is 6 * 7?"
    )

    assert result["answer"] == "42"
    assert result["guard_triggered"] is True
    assert result["recovered"] is False
    assert result["verified"] is False
    assert result["corrected"] is False


def test_explicit_failure_recovery():
    result = run_reliable_guarded_agent(
        "What is (15 + 5) * 3?",
        simulate_failure=True,
    )

    assert result["answer"] == "60"
    assert result["recovered"] is True
    assert result["corrected"] is False


def test_silent_fault_verification():
    result = run_reliable_guarded_agent(
        "What is 8 * 8?",
        simulate_silent_fault=True,
    )

    assert result["answer"] == "64"
    assert result["verified"] is True
    assert result["corrected"] is True


def test_no_supported_route():
    result = run_reliable_guarded_agent(
        "Explain reinforcement learning."
    )

    assert result["answer"] is None
    assert result["guard_triggered"] is False
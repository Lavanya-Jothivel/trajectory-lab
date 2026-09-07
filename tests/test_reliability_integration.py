from src.reliable_guarded_agent import (
    run_reliable_guarded_agent,
)


def test_normal_guarded_execution():
    result = run_reliable_guarded_agent(
        "What is 6 * 7?"
    )

    assert result["answer"] == "42"
    assert result["guard_triggered"] is True
    assert result["recovered"] is False
    assert result["verified"] is False


def test_failure_recovery_pipeline():
    result = run_reliable_guarded_agent(
        "What is (15 + 5) * 3?",
        simulate_failure=True,
    )

    assert result["answer"] == "60"
    assert result["recovered"] is True

    event_types = [
        event["type"]
        for event in result["trajectory"]
    ]

    assert "guard" in event_types
    assert "action" in event_types
    assert "recovery" in event_types


def test_silent_fault_correction_pipeline():
    result = run_reliable_guarded_agent(
        "What is 8 * 8?",
        simulate_silent_fault=True,
    )

    assert result["answer"] == "64"
    assert result["verified"] is True
    assert result["corrected"] is True

    event_types = [
        event["type"]
        for event in result["trajectory"]
    ]

    assert "verification" in event_types
    assert "correction" in event_types


def test_unsupported_request_abstains():
    result = run_reliable_guarded_agent(
        "Explain reinforcement learning."
    )

    assert result["answer"] is None
    assert result["tool"] is None
    assert result["guard_triggered"] is False

    assert (
        result["trajectory"][0]["decision"]
        == "no_math_route"
    )
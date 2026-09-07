from src.reliable_guarded_router import (
    run_reliable_guarded_router,
)


def test_math_route():
    result = run_reliable_guarded_router(
        "What is 6 * 7?"
    )

    assert result["answer"] == "42"
    assert result["tool"] == "calculator"
    assert result["guard_triggered"] is True


def test_lookup_route():
    result = run_reliable_guarded_router(
        "What is the capital of Japan?"
    )

    assert result["answer"] == "Tokyo"
    assert result["tool"] == "lookup"
    assert result["guard_triggered"] is True


def test_explicit_failure_recovery():
    result = run_reliable_guarded_router(
        "What is (15 + 5) * 3?",
        simulate_failure=True,
    )

    assert result["answer"] == "60"
    assert result["recovered"] is True


def test_silent_fault_correction():
    result = run_reliable_guarded_router(
        "What is 8 * 8?",
        simulate_silent_fault=True,
    )

    assert result["answer"] == "64"
    assert result["verified"] is True
    assert result["corrected"] is True


def test_unsupported_abstention():
    result = run_reliable_guarded_router(
        "Explain reinforcement learning."
    )

    assert result["answer"] is None
    assert result["tool"] is None
    assert result["guard_triggered"] is False
    
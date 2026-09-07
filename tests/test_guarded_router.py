from src.guarded_router import run_guarded_router


def test_guarded_router_math():
    result = run_guarded_router(
        "What is (15 + 5) * 3?"
    )

    assert result["answer"] == "60"
    assert result["tool"] == "calculator"
    assert result["guard_triggered"] is True


def test_guarded_router_lookup_capital():
    result = run_guarded_router(
        "What is the capital of Japan?"
    )

    assert result["answer"] == "Tokyo"
    assert result["tool"] == "lookup"
    assert result["guard_triggered"] is True


def test_guarded_router_lookup_python():
    result = run_guarded_router(
        "Who is the creator of Python?"
    )

    assert result["answer"] == "Guido van Rossum"
    assert result["tool"] == "lookup"
    assert result["guard_triggered"] is True


def test_guarded_router_unknown():
    result = run_guarded_router(
        "Explain reinforcement learning."
    )

    assert result["answer"] is None
    assert result["tool"] is None
    assert result["guard_triggered"] is False
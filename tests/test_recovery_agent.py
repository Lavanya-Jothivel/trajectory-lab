from src.recovery_agent import run_recovery_demo


def test_recovery_after_tool_failure():
    result = run_recovery_demo("(15 + 5) * 3")

    assert result["answer"] == "60"
    assert result["recovered"] is True
    assert len(result["trajectory"]) == 2

    assert result["trajectory"][0]["tool"] == "unreliable_calculator"
    assert result["trajectory"][1]["tool"] == "calculator"
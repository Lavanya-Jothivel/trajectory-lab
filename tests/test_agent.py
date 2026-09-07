from src.agent import run_react_agent


def test_math_question():
    result = run_react_agent("What is 6 * 7?")

    assert result["answer"] == "42"
    assert result["steps"] == 2
    assert result["trajectory"][0]["tool"] == "calculator"


def test_lookup_question():
    result = run_react_agent("What is the capital of Japan?")

    assert result["answer"] == "Tokyo"
    assert result["steps"] == 2
    assert result["trajectory"][0]["tool"] == "lookup"
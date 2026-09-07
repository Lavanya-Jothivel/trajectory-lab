from src.tools import calculator, lookup, run_tool


def test_calculator():
    assert calculator("6 * 7") == "42"


def test_calculator_parentheses():
    assert calculator("(10 + 5) * 2") == "30"


def test_lookup():
    assert lookup("capital of japan") == "Tokyo"


def test_tool_registry():
    assert run_tool("calculator", "8 * 8") == "64"


def test_unknown_tool():
    assert run_tool("does_not_exist", "test") == "Unknown tool: does_not_exist"
from src.parser import AgentAction, AgentFinish, parse_agent_output


def test_parse_action():
    text = (
        "Thought: I should calculate this.\n"
        "Action: calculator\n"
        "Action Input: 12 * 9"
    )

    result = parse_agent_output(text)

    assert isinstance(result, AgentAction)
    assert result.tool == "calculator"
    assert result.tool_input == "12 * 9"


def test_parse_finish():
    text = (
        "Thought: I know the answer.\n"
        "Final Answer: 108"
    )

    result = parse_agent_output(text)

    assert isinstance(result, AgentFinish)
    assert result.answer == "108"
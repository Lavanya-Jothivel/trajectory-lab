import re


def mock_model(prompt: str) -> str:
    """
    Deterministic mock model for testing ReAct behavior
    without requiring an external LLM.
    """

    # Finish when an observation already exists
    observations = re.findall(r"Observation:\s*(.+)", prompt)

    if observations:
        latest_observation = observations[-1].strip()

        return (
            "Thought: I have the result.\n"
            f"Final Answer: {latest_observation}"
        )

    # Lookup question
    if "capital of japan" in prompt.lower():
        return (
        "Thought: I should look up this fact.\n"
        "Action: lookup\n"
        "Action Input: capital of japan"
    )

    if "creator of python" in prompt.lower():
        return (
        "Thought: I should look up this fact.\n"
        "Action: lookup\n"
        "Action Input: creator of python"
    )

    # Extract simple arithmetic expression from the question
    question_text = prompt.split("Question:", 1)[-1].split("\n", 1)[0]

    math_match = re.search(
       r"(\(?\d[\d\s\+\-\*\/\(\)]*\d|\d)",
       question_text,
)

    if math_match:
        expression = math_match.group(1).strip()

        return (
            "Thought: I should calculate this.\n"
            "Action: calculator\n"
            f"Action Input: {expression}"
        )

    return (
        "Thought: I cannot determine what tool to use.\n"
        "Final Answer: Unknown"
    )
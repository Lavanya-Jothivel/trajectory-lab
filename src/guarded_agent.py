import re

from src.tools import run_tool


def extract_math_expression(question: str):
    """
    Extract an arithmetic expression from a question.
    """

    matches = re.findall(
        r"\(?\d[\d\s\+\-\*\/\(\)]*\d\)?",
        question,
    )

    for match in matches:
        expression = match.strip()

        if any(
            symbol in expression
            for symbol in ["+", "-", "*", "/"]
        ):
            return expression

    return None


def run_guarded_agent(question: str):
    """
    Reliability-aware agent that requires calculator
    execution for arithmetic expressions.
    """

    trajectory = []

    expression = extract_math_expression(
        question
    )

    if expression is not None:
        trajectory.append(
            {
                "type": "guard",
                "decision": "calculator_required",
                "expression": expression,
            }
        )

        result = run_tool(
            "calculator",
            expression,
        )

        trajectory.append(
            {
                "type": "action",
                "tool": "calculator",
                "tool_input": expression,
                "observation": result,
            }
        )

        return {
            "answer": result,
            "tool": "calculator",
            "guard_triggered": True,
            "trajectory": trajectory,
        }

    trajectory.append(
        {
            "type": "guard",
            "decision": "no_math_expression",
        }
    )

    return {
        "answer": None,
        "tool": None,
        "guard_triggered": False,
        "trajectory": trajectory,
    }
from src.tools import run_tool


def run_recovery_demo(expression: str):
    """
    Demonstrates simple failure recovery:
    1. Try unreliable_calculator.
    2. Detect tool failure.
    3. Fall back to calculator.
    """

    trajectory = []

    first_result = run_tool(
        "unreliable_calculator",
        expression,
    )

    trajectory.append(
        {
            "tool": "unreliable_calculator",
            "input": expression,
            "observation": first_result,
        }
    )

    if first_result.startswith("ERROR:"):
        recovered_result = run_tool(
            "calculator",
            expression,
        )

        trajectory.append(
            {
                "tool": "calculator",
                "input": expression,
                "observation": recovered_result,
                "recovery": True,
            }
        )

        return {
            "answer": recovered_result,
            "recovered": True,
            "trajectory": trajectory,
        }

    return {
        "answer": first_result,
        "recovered": False,
        "trajectory": trajectory,
    }
from src.tools import run_tool


def run_verification_demo(expression: str):
    """
    Detect a silent tool error by verifying the result
    with a second trusted tool.
    """

    trajectory = []

    primary_result = run_tool(
        "faulty_calculator",
        expression,
    )

    trajectory.append(
        {
            "stage": "primary",
            "tool": "faulty_calculator",
            "input": expression,
            "observation": primary_result,
        }
    )

    verification_result = run_tool(
        "calculator",
        expression,
    )

    trajectory.append(
        {
            "stage": "verification",
            "tool": "calculator",
            "input": expression,
            "observation": verification_result,
        }
    )

    verified = primary_result == verification_result

    final_answer = (
        primary_result
        if verified
        else verification_result
    )

    return {
        "answer": final_answer,
        "verified": verified,
        "correction_made": not verified,
        "trajectory": trajectory,
    }
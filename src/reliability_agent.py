from src.tools import run_tool


def run_reliability_agent(
    expression: str,
    primary_tool: str,
):
    """
    Reliability-aware calculator agent.

    Handles:
    1. Explicit tool failures using fallback recovery.
    2. Silent incorrect outputs using verification.
    """

    trajectory = []

    primary_result = run_tool(
        primary_tool,
        expression,
    )

    trajectory.append(
        {
            "stage": "primary",
            "tool": primary_tool,
            "input": expression,
            "observation": primary_result,
        }
    )

    # Explicit failure recovery
    if primary_result.startswith("ERROR:"):
        fallback_result = run_tool(
            "calculator",
            expression,
        )

        trajectory.append(
            {
                "stage": "recovery",
                "tool": "calculator",
                "input": expression,
                "observation": fallback_result,
            }
        )

        return {
            "answer": fallback_result,
            "recovered": True,
            "verified": False,
            "corrected": True,
            "trajectory": trajectory,
        }

    # Silent-error verification
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

    if primary_result != verification_result:
        return {
            "answer": verification_result,
            "recovered": False,
            "verified": True,
            "corrected": True,
            "trajectory": trajectory,
        }

    return {
        "answer": primary_result,
        "recovered": False,
        "verified": True,
        "corrected": False,
        "trajectory": trajectory,
    }
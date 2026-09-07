from src.guarded_agent import extract_math_expression
from src.tools import run_tool


def run_reliable_guarded_agent(
    question: str,
    simulate_failure: bool = False,
    simulate_silent_fault: bool = False,
):
    """
    Guarded tool-routing agent with:

    1. Mandatory calculator routing for arithmetic.
    2. Explicit tool-failure recovery.
    3. Silent-error verification.
    """

    trajectory = []

    expression = extract_math_expression(question)

    if expression is None:
        return {
            "answer": None,
            "tool": None,
            "guard_triggered": False,
            "recovered": False,
            "verified": False,
            "corrected": False,
            "trajectory": [
                {
                    "type": "guard",
                    "decision": "no_math_route",
                }
            ],
        }

    trajectory.append(
        {
            "type": "guard",
            "decision": "calculator_required",
            "expression": expression,
        }
    )

    recovered = False
    verified = False
    corrected = False

    if simulate_failure:
        primary_tool = "unreliable_calculator"

    elif simulate_silent_fault:
        primary_tool = "faulty_calculator"

    else:
        primary_tool = "calculator"

    primary_result = run_tool(
        primary_tool,
        expression,
    )

    trajectory.append(
        {
            "type": "action",
            "tool": primary_tool,
            "tool_input": expression,
            "observation": primary_result,
        }
    )

    # Explicit failure recovery
    if primary_result.startswith("ERROR"):
        recovered = True

        fallback_result = run_tool(
            "calculator",
            expression,
        )

        trajectory.append(
            {
                "type": "recovery",
                "from_tool": primary_tool,
                "to_tool": "calculator",
                "observation": fallback_result,
            }
        )

        return {
            "answer": fallback_result,
            "tool": "calculator",
            "guard_triggered": True,
            "recovered": recovered,
            "verified": False,
            "corrected": False,
            "trajectory": trajectory,
        }

    # Silent error verification
    if simulate_silent_fault:
        verified = True

        trusted_result = run_tool(
            "calculator",
            expression,
        )

        trajectory.append(
            {
                "type": "verification",
                "primary_result": primary_result,
                "trusted_result": trusted_result,
            }
        )

        if primary_result != trusted_result:
            corrected = True

            trajectory.append(
                {
                    "type": "correction",
                    "incorrect_result": primary_result,
                    "correct_result": trusted_result,
                }
            )

            primary_result = trusted_result

    return {
        "answer": primary_result,
        "tool": primary_tool,
        "guard_triggered": True,
        "recovered": recovered,
        "verified": verified,
        "corrected": corrected,
        "trajectory": trajectory,
    }
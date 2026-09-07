from src.guarded_agent import extract_math_expression
from src.tools import run_tool


FACT_PATTERNS = {
    "capital of japan": "capital of japan",
    "capital of france": "capital of france",
    "creator of python": "creator of python",
}


def extract_lookup_query(question: str):
    """
    Detect supported factual lookup requests.
    """

    question_lower = question.lower()

    for pattern, query in FACT_PATTERNS.items():
        if pattern in question_lower:
            return query

    return None


def run_reliable_guarded_router(
    question: str,
    simulate_failure: bool = False,
    simulate_silent_fault: bool = False,
):
    """
    Unified reliability-aware guarded router.

    Supports:
    - arithmetic routing
    - factual lookup routing
    - explicit calculator failure recovery
    - silent calculator fault verification
    - abstention for unsupported requests
    """

    trajectory = []

    math_expression = extract_math_expression(
        question
    )

    if math_expression is not None:
        trajectory.append(
            {
                "type": "guard",
                "decision": "calculator",
                "expression": math_expression,
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
            math_expression,
        )

        trajectory.append(
            {
                "type": "action",
                "tool": primary_tool,
                "tool_input": math_expression,
                "observation": primary_result,
            }
        )

        if primary_result.startswith("ERROR"):
            recovered = True

            fallback_result = run_tool(
                "calculator",
                math_expression,
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
                "recovered": True,
                "verified": False,
                "corrected": False,
                "trajectory": trajectory,
            }

        if simulate_silent_fault:
            verified = True

            trusted_result = run_tool(
                "calculator",
                math_expression,
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

    lookup_query = extract_lookup_query(
        question
    )

    if lookup_query is not None:
        trajectory.append(
            {
                "type": "guard",
                "decision": "lookup",
                "query": lookup_query,
            }
        )

        result = run_tool(
            "lookup",
            lookup_query,
        )

        trajectory.append(
            {
                "type": "action",
                "tool": "lookup",
                "tool_input": lookup_query,
                "observation": result,
            }
        )

        return {
            "answer": result,
            "tool": "lookup",
            "guard_triggered": True,
            "recovered": False,
            "verified": False,
            "corrected": False,
            "trajectory": trajectory,
        }

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
                "decision": "no_route",
            }
        ],
    }
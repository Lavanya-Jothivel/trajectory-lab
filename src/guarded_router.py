from src.guarded_agent import extract_math_expression
from src.tools import run_tool


FACT_PATTERNS = [
    "capital of",
    "creator of python",
]


def run_guarded_router(question: str):
    trajectory = []

    math_expression = extract_math_expression(
        question
    )

    if math_expression is not None:
        result = run_tool(
            "calculator",
            math_expression,
        )

        trajectory.append(
            {
                "type": "guard",
                "decision": "calculator",
            }
        )

        trajectory.append(
            {
                "type": "action",
                "tool": "calculator",
                "tool_input": math_expression,
                "observation": result,
            }
        )

        return {
            "answer": result,
            "tool": "calculator",
            "guard_triggered": True,
            "trajectory": trajectory,
        }

    question_lower = question.lower()

    for pattern in FACT_PATTERNS:
        if pattern in question_lower:
            if "capital of japan" in question_lower:
                query = "capital of japan"

            elif "creator of python" in question_lower:
                query = "creator of python"

            else:
                query = question

            result = run_tool(
                "lookup",
                query,
            )

            trajectory.append(
                {
                    "type": "guard",
                    "decision": "lookup",
                }
            )

            trajectory.append(
                {
                    "type": "action",
                    "tool": "lookup",
                    "tool_input": query,
                    "observation": result,
                }
            )

            return {
                "answer": result,
                "tool": "lookup",
                "guard_triggered": True,
                "trajectory": trajectory,
            }

    return {
        "answer": None,
        "tool": None,
        "guard_triggered": False,
        "trajectory": [
            {
                "type": "guard",
                "decision": "no_route",
            }
        ],
    }
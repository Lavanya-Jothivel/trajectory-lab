import re

from src.tools import run_tool


def extract_math_expression(query: str) -> str:
    """
    Extract a mathematical expression from a natural-language query.

    Examples:
    'What is 25 * 18?' -> '25 * 18'
    'Calculate (15 + 5) * 3' -> '(15 + 5) * 3'
    """

    cleaned = query.strip()

    prefixes = [
        r"^what is\s+",
        r"^calculate\s+",
        r"^compute\s+",
        r"^evaluate\s+",
        r"^solve\s+",
        r"^find\s+",
    ]

    for pattern in prefixes:
        cleaned = re.sub(
            pattern,
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

    cleaned = cleaned.strip().rstrip("?")

    return cleaned.strip()


def is_math_query(query: str) -> bool:
    """
    Determine whether the query is primarily mathematical.
    """

    cleaned = extract_math_expression(query)

    # Must contain at least one digit
    if not any(char.isdigit() for char in cleaned):
        return False

    # Allowed characters for calculator expressions
    allowed_pattern = r"^[0-9\s\+\-\*\/\%\.\(\)]+$"

    return bool(
        re.fullmatch(
            allowed_pattern,
            cleaned,
        )
    )


def choose_tool(query: str) -> str:
    """
    Automatically choose the most appropriate tool.
    """

    if is_math_query(query):
        return "calculator"

    return "lookup"


def get_reliable_tool(selected_tool: str) -> str:
    """
    Return the trusted tool used for recovery
    and verification.
    """

    calculator_tools = {
        "calculator",
        "unreliable_calculator",
        "faulty_calculator",
    }

    if selected_tool in calculator_tools:
        return "calculator"

    return "lookup"


def prepare_tool_input(
    query: str,
    selected_tool: str,
) -> str:
    """
    Prepare input for the selected tool.

    Calculator receives only the mathematical expression.
    Lookup receives the original natural-language query.
    """

    calculator_tools = {
        "calculator",
        "unreliable_calculator",
        "faulty_calculator",
    }

    if selected_tool in calculator_tools:
        return extract_math_expression(query)

    return query


def run_multi_tool_reliability_agent(
    query: str,
    primary_tool: str = "auto",
):
    """
    Reliable multi-tool agent.

    Features:
    - Automatic calculator/lookup routing
    - Natural-language math queries
    - Explicit failure recovery
    - Independent verification
    - Silent-error correction
    - Full execution trajectory
    """

    trajectory = []

    # --------------------------------------------------
    # Tool selection
    # --------------------------------------------------

    if primary_tool == "auto":
        selected_tool = choose_tool(query)
    else:
        selected_tool = primary_tool

    tool_input = prepare_tool_input(
        query,
        selected_tool,
    )

    trajectory.append(
        {
            "stage": "tool_selection",
            "tool": selected_tool,
            "input": query,
            "observation": (
                f"Selected tool: {selected_tool}"
            ),
        }
    )

    # --------------------------------------------------
    # Primary execution
    # --------------------------------------------------

    primary_result = run_tool(
        selected_tool,
        tool_input,
    )

    trajectory.append(
        {
            "stage": "primary",
            "tool": selected_tool,
            "input": tool_input,
            "observation": primary_result,
        }
    )

    reliable_tool = get_reliable_tool(
        selected_tool
    )

    reliable_input = prepare_tool_input(
        query,
        reliable_tool,
    )

    # --------------------------------------------------
    # Explicit failure recovery
    # --------------------------------------------------

    if primary_result.startswith("ERROR:"):

        recovery_result = run_tool(
            reliable_tool,
            reliable_input,
        )

        trajectory.append(
            {
                "stage": "recovery",
                "tool": reliable_tool,
                "input": reliable_input,
                "observation": recovery_result,
            }
        )

        return {
            "query": query,
            "selected_tool": selected_tool,
            "answer": recovery_result,
            "recovered": True,
            "verified": False,
            "corrected": True,
            "trajectory": trajectory,
        }

    # --------------------------------------------------
    # Verification
    # --------------------------------------------------

    verification_result = run_tool(
        reliable_tool,
        reliable_input,
    )

    trajectory.append(
        {
            "stage": "verification",
            "tool": reliable_tool,
            "input": reliable_input,
            "observation": verification_result,
        }
    )

    # --------------------------------------------------
    # Silent-error correction
    # --------------------------------------------------

    if primary_result != verification_result:

        return {
            "query": query,
            "selected_tool": selected_tool,
            "answer": verification_result,
            "recovered": False,
            "verified": True,
            "corrected": True,
            "trajectory": trajectory,
        }

    # --------------------------------------------------
    # Verified success
    # --------------------------------------------------

    return {
        "query": query,
        "selected_tool": selected_tool,
        "answer": primary_result,
        "recovered": False,
        "verified": True,
        "corrected": False,
        "trajectory": trajectory,
    }
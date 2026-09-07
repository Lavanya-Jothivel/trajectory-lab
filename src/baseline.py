import re


def direct_answer(question: str) -> str:
    """
    Simple non-agent baseline.
    Produces an answer directly without tools or trajectories.
    """

    question_lower = question.lower()

    if "capital of japan" in question_lower:
        return "Tokyo"

    math_match = re.search(
        r"(\d+)\s*([\+\-\*\/])\s*(\d+)",
        question,
    )

    if math_match:
        left = int(math_match.group(1))
        operator = math_match.group(2)
        right = int(math_match.group(3))

        if operator == "+":
            return str(left + right)
        if operator == "-":
            return str(left - right)
        if operator == "*":
            return str(left * right)
        if operator == "/":
            return str(left / right)

    return "Unknown"
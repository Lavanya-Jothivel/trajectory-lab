import re

from src.parser import (
    AgentAction,
    AgentFinish,
    parse_agent_output,
)
from src.tools import run_tool
from src.model_interface import MockModel


RECOVERY_REACT_PROMPT = """
You are a tool-using reasoning agent.

Available tools:
calculator
lookup

Rules:

1. Use calculator for arithmetic questions.
2. Use lookup for factual questions.
3. Never invent observations.
4. Never simulate tool results.
5. Output only one action at a time.
6. After receiving an observation, either:
   - make one additional tool call if needed, or
   - return the final answer.
7. Do not use Markdown.
8. Do not use code fences.
"""


def extract_math_expression(question: str):
    """
    Extract an arithmetic expression from the question.
    """

    match = re.search(
        r"[\d\s\+\-\*\/\(\)]+",
        question,
    )

    if match:
        expression = match.group(0).strip()

        if any(
            operator in expression
            for operator in ["+", "-", "*", "/"]
        ):
            return expression

    return None


def validate_tool_call(
    question: str,
    tool_name: str,
    tool_input: str,
):
    """
    Reliability guard.

    Correct obvious tool-selection and tool-input errors
    before executing the tool.
    """

    math_expression = extract_math_expression(
        question
    )

    corrected = False
    correction_reason = None

    if math_expression is not None:
        if tool_name != "calculator":
            tool_name = "calculator"
            corrected = True
            correction_reason = (
                "Wrong tool corrected to calculator"
            )

        cleaned_input = (
            tool_input
            .replace('"', "")
            .replace("'", "")
            .strip()
        )

        if cleaned_input != math_expression:
            tool_input = math_expression
            corrected = True

            if correction_reason:
                correction_reason += (
                    "; incomplete tool input corrected"
                )
            else:
                correction_reason = (
                    "Incomplete tool input corrected"
                )

    return (
        tool_name,
        tool_input,
        corrected,
        correction_reason,
    )


def run_react_recovery_agent(
    question: str,
    max_steps: int = 5,
    model=None,
):
    if model is None:
        model = MockModel()

    prompt = (
        RECOVERY_REACT_PROMPT
        + "\nQuestion: "
        + question
        + "\n"
    )

    trajectory = []
    recovery_count = 0
    correction_count = 0

    for step in range(max_steps):
        model_output = model.generate(
            prompt
        )

        try:
            parsed = parse_agent_output(
                model_output
            )

        except ValueError:
            return {
                "answer": None,
                "steps": step + 1,
                "trajectory": trajectory,
                "recoveries": recovery_count,
                "corrections": correction_count,
                "error": "Could not parse model output",
                "raw_model_output": model_output,
            }

        if isinstance(
            parsed,
            AgentFinish,
        ):
            trajectory.append(
                {
                    "step": step + 1,
                    "type": "finish",
                    "answer": parsed.answer,
                    "model_output": model_output,
                }
            )

            return {
                "answer": parsed.answer,
                "steps": step + 1,
                "trajectory": trajectory,
                "recoveries": recovery_count,
                "corrections": correction_count,
            }

        if not isinstance(
            parsed,
            AgentAction,
        ):
            return {
                "answer": None,
                "steps": step + 1,
                "trajectory": trajectory,
                "recoveries": recovery_count,
                "corrections": correction_count,
                "error": "Unexpected parser result",
            }

        original_tool = (
            parsed.tool.strip().lower()
        )

        original_input = (
            parsed.tool_input.strip()
        )

        (
            tool_name,
            tool_input,
            corrected,
            correction_reason,
        ) = validate_tool_call(
            question,
            original_tool,
            original_input,
        )

        if corrected:
            correction_count += 1

            trajectory.append(
                {
                    "step": step + 1,
                    "type": "correction",
                    "original_tool": original_tool,
                    "original_input": original_input,
                    "corrected_tool": tool_name,
                    "corrected_input": tool_input,
                    "reason": correction_reason,
                }
            )

        if (
            tool_name == "calculator"
            and "15" in tool_input
        ):
            observation = run_tool(
                "unreliable_calculator",
                tool_input,
            )

            trajectory.append(
                {
                    "step": step + 1,
                    "type": "action",
                    "tool": "unreliable_calculator",
                    "tool_input": tool_input,
                    "observation": observation,
                    "model_output": model_output,
                }
            )

            if observation.startswith(
                "ERROR:"
            ):
                recovery_count += 1

                observation = run_tool(
                    "calculator",
                    tool_input,
                )

                trajectory.append(
                    {
                        "step": step + 1,
                        "type": "recovery",
                        "tool": "calculator",
                        "tool_input": tool_input,
                        "observation": observation,
                    }
                )

        else:
            observation = run_tool(
                tool_name,
                tool_input,
            )

            trajectory.append(
                {
                    "step": step + 1,
                    "type": "action",
                    "tool": tool_name,
                    "tool_input": tool_input,
                    "observation": observation,
                    "model_output": model_output,
                }
            )

        prompt += (
            f"\nObservation: {observation}\n"
            "This observation is authoritative.\n"
            "Return the final answer using this result.\n"
        )

    return {
        "answer": None,
        "steps": max_steps,
        "trajectory": trajectory,
        "recoveries": recovery_count,
        "corrections": correction_count,
        "error": "Maximum steps reached",
    }
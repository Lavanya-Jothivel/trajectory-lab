
from src.parser import AgentAction, AgentFinish, parse_agent_output
from src.tools import run_tool
from src.model_interface import MockModel
from src.prompts import REACT_PROMPT


def execute_agent_step(model_output: str):
    """
    Parse one ReAct model output and either:
    - execute a tool action, or
    - return the final answer.
    """

    parsed = parse_agent_output(model_output)

    if isinstance(parsed, AgentFinish):
        return {
            "type": "finish",
            "answer": parsed.answer,
        }

    if isinstance(parsed, AgentAction):
        observation = run_tool(
            parsed.tool,
            parsed.tool_input,
        )

        return {
            "type": "action",
            "tool": parsed.tool,
            "tool_input": parsed.tool_input,
            "observation": observation,
        }

    raise ValueError("Unexpected parser result")


def run_react_agent(
    question: str,
    max_steps: int = 5,
    model=None,
):
    """
    Run a complete ReAct loop using the model interface
    and record the full agent trajectory.
    """

    if model is None:
        model = MockModel()

    prompt = (
    REACT_PROMPT
    + "\n"
    + f"Question: {question}\n"
)
    trajectory = []

    for step in range(max_steps):
        model_output = model.generate(prompt)

        try:
         parsed = execute_agent_step(
         model_output
    )
        except ValueError:
             return {
        "answer": None,
        "steps": step + 1,
        "trajectory": trajectory,
        "error": "Could not parse model output",
        "raw_model_output": model_output,
    }

        if parsed["type"] == "finish":
            trajectory.append(
                {
                    "step": step + 1,
                    "type": "finish",
                    "model_output": model_output,
                    "answer": parsed["answer"],
                }
            )

            return {
                "answer": parsed["answer"],
                "steps": step + 1,
                "trajectory": trajectory,
            }

        observation = parsed["observation"]

        trajectory.append(
            {
                "step": step + 1,
                "type": "action",
                "tool": parsed["tool"],
                "tool_input": parsed["tool_input"],
                "observation": observation,
            }
        )

        
        prompt += (
    f"\n{model_output}\n"
    f"Observation: {observation}\n\n"
    "The tool has returned a result.\n"
    "Now respond using EXACTLY these two lines:\n"
    "Thought: I have the result.\n"
    "Final Answer: <answer from the observation>\n"
    "Do not call another tool unless the observation is an error.\n"
)



    return {
        "answer": None,
        "steps": max_steps,
        "trajectory": trajectory,
        "error": "Maximum steps reached",
    }


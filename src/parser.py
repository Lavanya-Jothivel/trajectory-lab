
import re
from dataclasses import dataclass


@dataclass
class AgentAction:
    tool: str
    tool_input: str


@dataclass
class AgentFinish:
    answer: str


def parse_agent_output(text: str):
    """
    Parse ReAct model output robustly.

    Rules:
    - Prefer a tool Action if both Action and Final Answer appear.
    - Accept both 'Action Input:' and 'Input:'.
    - Capture only the first Final Answer line.
    """

    action_match = re.search(
        r"Action:\s*([^\n]+)\s*\n"
        r"(?:Action Input|Input):\s*([^\n]+)",
        text,
        re.IGNORECASE,
    )

    if action_match:
        return AgentAction(
            tool=action_match.group(1).strip(),
            tool_input=action_match.group(2).strip(),
        )

    final_match = re.search(
    r"(?:\d+\.\s*)?"
    r"\*{0,2}Final Answer\*{0,2}\s*:\s*"
    r"([^\n]+)",
    text,
    re.IGNORECASE,
)

    if final_match:
     return AgentFinish(
        answer=final_match.group(1).strip()
    )

    raise ValueError("Could not parse agent output")


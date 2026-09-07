
import json

from src.agent import run_react_agent
from src.model_interface import HuggingFaceModel


TASKS = [
    "What is 6 * 7?",
    "What is 8 * 8?",
    "What is 12 + 9?",
    "What is 15 - 7?",
    "What is 9 * 5?",
    "What is the capital of Japan?",
    "Who is the creator of Python?",
]


model = HuggingFaceModel(
    model_name="Qwen/Qwen2.5-0.5B-Instruct",
    max_new_tokens=100,
)


records = []

for question in TASKS:
    result = run_react_agent(
        question,
        model=model,
    )

    records.append(
    {
        "question": question,
        "answer": result.get("answer"),
        "steps": result.get("steps"),
        "error": result.get("error"),
        "raw_model_output": result.get(
            "raw_model_output"
        ),
        "trajectory": result.get(
            "trajectory",
            [],
        ),
    }
)


with open(
    "results/real_model_trajectories.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        records,
        file,
        indent=2,
    )


print(
    "Saved: results/real_model_trajectories.json"
)


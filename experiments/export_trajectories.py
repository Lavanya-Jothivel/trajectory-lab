import json

from src.reliability_agent import run_reliability_agent


CASES = [
    {
        "id": "normal_01",
        "expression": "7 + 9",
        "primary_tool": "calculator",
    },
    {
        "id": "failure_01",
        "expression": "(15 + 5) * 3",
        "primary_tool": "unreliable_calculator",
    },
    {
        "id": "silent_01",
        "expression": "8 * 8",
        "primary_tool": "faulty_calculator",
    },
]


trajectories = []

for case in CASES:
    result = run_reliability_agent(
        case["expression"],
        case["primary_tool"],
    )

    trajectories.append(
        {
            "id": case["id"],
            "expression": case["expression"],
            "primary_tool": case["primary_tool"],
            "answer": result["answer"],
            "recovered": result["recovered"],
            "verified": result["verified"],
            "corrected": result["corrected"],
            "trajectory": result["trajectory"],
        }
    )


with open(
    "results/trajectories.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        trajectories,
        file,
        indent=2,
    )


print("Saved: results/trajectories.json")
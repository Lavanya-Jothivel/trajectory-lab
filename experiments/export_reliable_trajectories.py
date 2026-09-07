import json

from src.reliable_guarded_agent import (
    run_reliable_guarded_agent,
)


TASKS = [
    {
        "name": "normal_01",
        "question": "What is 6 * 7?",
        "simulate_failure": False,
        "simulate_silent_fault": False,
    },
    {
        "name": "normal_02",
        "question": "What is 12 + 9?",
        "simulate_failure": False,
        "simulate_silent_fault": False,
    },
    {
        "name": "explicit_failure",
        "question": "What is (15 + 5) * 3?",
        "simulate_failure": True,
        "simulate_silent_fault": False,
    },
    {
        "name": "silent_fault",
        "question": "What is 8 * 8?",
        "simulate_failure": False,
        "simulate_silent_fault": True,
    },
    {
        "name": "unsupported",
        "question": "Explain reinforcement learning.",
        "simulate_failure": False,
        "simulate_silent_fault": False,
    },
]


records = []

for task in TASKS:
    result = run_reliable_guarded_agent(
        question=task["question"],
        simulate_failure=task["simulate_failure"],
        simulate_silent_fault=task["simulate_silent_fault"],
    )

    records.append(
        {
            "name": task["name"],
            "question": task["question"],
            "answer": result["answer"],
            "guard_triggered": result["guard_triggered"],
            "recovered": result["recovered"],
            "verified": result["verified"],
            "corrected": result["corrected"],
            "trajectory": result["trajectory"],
        }
    )


with open(
    "results/reliable_guarded_trajectories.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        records,
        file,
        indent=2,
    )


print(
    "Saved: results/reliable_guarded_trajectories.json"
)

for record in records:
    print(
        f"{record['name']}: "
        f"{len(record['trajectory'])} trajectory events"
    )
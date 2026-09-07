import pandas as pd

from src.reliable_guarded_agent import (
    run_reliable_guarded_agent,
)


TASKS = [
    {
        "name": "normal_01",
        "question": "What is 6 * 7?",
        "expected": "42",
        "simulate_failure": False,
        "simulate_silent_fault": False,
    },
    {
        "name": "normal_02",
        "question": "What is 12 + 9?",
        "expected": "21",
        "simulate_failure": False,
        "simulate_silent_fault": False,
    },
    {
        "name": "explicit_failure",
        "question": "What is (15 + 5) * 3?",
        "expected": "60",
        "simulate_failure": True,
        "simulate_silent_fault": False,
    },
    {
        "name": "silent_fault",
        "question": "What is 8 * 8?",
        "expected": "64",
        "simulate_failure": False,
        "simulate_silent_fault": True,
    },
    {
        "name": "unsupported",
        "question": "Explain reinforcement learning.",
        "expected": None,
        "simulate_failure": False,
        "simulate_silent_fault": False,
    },
]


rows = []

for task in TASKS:
    result = run_reliable_guarded_agent(
        question=task["question"],
        simulate_failure=task["simulate_failure"],
        simulate_silent_fault=task["simulate_silent_fault"],
    )

    if task["expected"] is None:
        correct = result["answer"] is None
    else:
        correct = (
            str(result["answer"])
            == str(task["expected"])
        )

    rows.append(
        {
            "name": task["name"],
            "question": task["question"],
            "expected": task["expected"],
            "answer": result["answer"],
            "correct": correct,
            "guard_triggered": result["guard_triggered"],
            "recovered": result["recovered"],
            "verified": result["verified"],
            "corrected": result["corrected"],
        }
    )


df = pd.DataFrame(rows)

df.to_csv(
    "results/reliable_guarded_benchmark.csv",
    index=False,
)

print(df.to_string(index=False))

print("\n--- Reliable Guarded Benchmark ---")
print(f"Tasks: {len(df)}")
print(
    f"Accuracy: "
    f"{df['correct'].mean():.2%}"
)
print(
    f"Guard Trigger Rate: "
    f"{df['guard_triggered'].mean():.2%}"
)
print(
    f"Recovery Events: "
    f"{df['recovered'].sum()}"
)
print(
    f"Verification Events: "
    f"{df['verified'].sum()}"
)
print(
    f"Correction Events: "
    f"{df['corrected'].sum()}"
)
import pandas as pd

from src.reliable_guarded_router import (
    run_reliable_guarded_router,
)


TASKS = [
    {
        "name": "math_normal",
        "question": "What is 6 * 7?",
        "expected": "42",
        "simulate_failure": False,
        "simulate_silent_fault": False,
    },
    {
        "name": "math_failure",
        "question": "What is (15 + 5) * 3?",
        "expected": "60",
        "simulate_failure": True,
        "simulate_silent_fault": False,
    },
    {
        "name": "math_silent_fault",
        "question": "What is 8 * 8?",
        "expected": "64",
        "simulate_failure": False,
        "simulate_silent_fault": True,
    },
    {
        "name": "lookup_japan",
        "question": "What is the capital of Japan?",
        "expected": "Tokyo",
        "simulate_failure": False,
        "simulate_silent_fault": False,
    },
    {
        "name": "lookup_france",
        "question": "What is the capital of France?",
        "expected": "Paris",
        "simulate_failure": False,
        "simulate_silent_fault": False,
    },
    {
        "name": "lookup_python",
        "question": "Who is the creator of Python?",
        "expected": "Guido van Rossum",
        "simulate_failure": False,
        "simulate_silent_fault": False,
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
    result = run_reliable_guarded_router(
        question=task["question"],
        simulate_failure=task["simulate_failure"],
        simulate_silent_fault=task["simulate_silent_fault"],
    )

    if task["expected"] is None:
        correct = (
            result["answer"] is None
            and result["guard_triggered"] is False
        )
    else:
        correct = (
            str(result["answer"])
            == str(task["expected"])
        )

    rows.append(
        {
            "name": task["name"],
            "expected": task["expected"],
            "answer": result["answer"],
            "tool": result["tool"],
            "correct": correct,
            "guard_triggered": result["guard_triggered"],
            "recovered": result["recovered"],
            "verified": result["verified"],
            "corrected": result["corrected"],
            "trajectory_events": len(
                result["trajectory"]
            ),
        }
    )


df = pd.DataFrame(rows)

df.to_csv(
    "results/unified_router_benchmark.csv",
    index=False,
)

print(df.to_string(index=False))

print("\n--- Unified Reliable Router Benchmark ---")

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
    f"Abstention Rate: "
    f"{(~df['guard_triggered']).mean():.2%}"
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

print(
    f"Average Trajectory Events: "
    f"{df['trajectory_events'].mean():.2f}"
)
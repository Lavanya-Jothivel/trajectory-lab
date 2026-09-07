import json
import pandas as pd


summary = {
    "tests_passed": 32,
    "direct_baseline_accuracy": 60.00,
    "mock_react_accuracy": 100.00,
    "qwen_react_answer_accuracy": 100.00,
    "qwen_react_tool_selection_accuracy": 57.14,
    "raw_qwen_controlled_accuracy": 87.50,
    "guarded_router_accuracy": 100.00,
    "reliable_guarded_benchmark_accuracy": 100.00,
    "unified_router_accuracy": 100.00,
    "unified_router_guard_trigger_rate": 85.71,
    "unified_router_abstention_rate": 14.29,
    "recovery_events": 1,
    "verification_events": 1,
    "correction_events": 1,
    "average_unified_trajectory_events": 2.29,
}


notes = [
    "Results come from multiple small controlled task sets.",
    "Percentages across different task sets should not be treated as directly comparable benchmark scores.",
    "Qwen2.5-0.5B-Instruct is used for the real-model experiments.",
    "Explicit failures and silent faults are deliberately injected for reliability evaluation.",
    "The guarded router uses deterministic routing rules for supported arithmetic and factual lookup tasks.",
    "Unsupported requests can abstain instead of forcing an incorrect tool route.",
]


with open(
    "results/final_results_summary.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        {
            "metrics": summary,
            "notes": notes,
        },
        file,
        indent=2,
    )


df = pd.DataFrame(
    [
        {
            "metric": metric,
            "value": value,
        }
        for metric, value in summary.items()
    ]
)

df.to_csv(
    "results/final_results_summary.csv",
    index=False,
)


print("--- Final TrajectoryLab Results ---")

for metric, value in summary.items():
    print(f"{metric}: {value}")

print(
    "\nSaved: results/final_results_summary.json"
)

print(
    "Saved: results/final_results_summary.csv"
)
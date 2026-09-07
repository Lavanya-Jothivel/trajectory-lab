import json
import pandas as pd


summary = {
    "tests_passed": 19,
    "direct_baseline_accuracy": 60.0,
    "mock_react_accuracy": 100.0,
    "qwen_react_answer_accuracy": 100.0,
    "qwen_react_tool_selection_accuracy": 57.14,
    "raw_qwen_controlled_accuracy": 87.5,
    "guarded_router_accuracy": 100.0,
    "recovery_agent_accuracy": 100.0,
    "verification_agent_accuracy": 100.0,
    "notes": [
        "Results come from different controlled task sets.",
        "Percentages should not be treated as a single unified benchmark.",
        "Real-model Qwen evaluation uses a small sanity-check task set.",
        "Failure and silent-error experiments use deliberately injected faults.",
    ],
}


with open(
    "results/project_summary.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        summary,
        file,
        indent=2,
    )


df = pd.DataFrame(
    [
        {
            "metric": key,
            "value": value,
        }
        for key, value in summary.items()
        if key != "notes"
    ]
)

df.to_csv(
    "results/project_summary.csv",
    index=False,
)

print(
    "Saved: results/project_summary.json"
)

print(
    "Saved: results/project_summary.csv"
)
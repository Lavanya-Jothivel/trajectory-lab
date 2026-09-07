import pandas as pd


rows = [
    {
        "method": "Direct Baseline",
        "task_set": "Synthetic 5-task",
        "accuracy": 60.00,
        "tool_selection_accuracy": None,
        "recovery": False,
        "verification": False,
    },
    {
        "method": "ReAct (Mock Model)",
        "task_set": "Synthetic 5-task",
        "accuracy": 100.00,
        "tool_selection_accuracy": None,
        "recovery": False,
        "verification": False,
    },
    {
        "method": "Qwen ReAct",
        "task_set": "Real-model 7-task",
        "accuracy": 100.00,
        "tool_selection_accuracy": 57.14,
        "recovery": False,
        "verification": False,
    },
    {
        "method": "Raw Qwen",
        "task_set": "Controlled 8-task",
        "accuracy": 87.50,
        "tool_selection_accuracy": None,
        "recovery": False,
        "verification": False,
    },
    {
        "method": "Guarded Router",
        "task_set": "Controlled 8-task",
        "accuracy": 100.00,
        "tool_selection_accuracy": 100.00,
        "recovery": False,
        "verification": False,
    },
    {
        "method": "Recovery Agent",
        "task_set": "Failure stress test",
        "accuracy": 100.00,
        "tool_selection_accuracy": None,
        "recovery": True,
        "verification": False,
    },
    {
        "method": "Verification Agent",
        "task_set": "Silent-error stress test",
        "accuracy": 100.00,
        "tool_selection_accuracy": None,
        "recovery": False,
        "verification": True,
    },
]


df = pd.DataFrame(rows)

df.to_csv(
    "results/ablation_summary.csv",
    index=False,
)

print(df.to_string(index=False))

print(
    "\nSaved: results/ablation_summary.csv"
)
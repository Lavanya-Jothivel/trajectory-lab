import json
import pandas as pd


EXPECTED_TOOLS = {
    "What is 6 * 7?": "calculator",
    "What is 8 * 8?": "calculator",
    "What is 12 + 9?": "calculator",
    "What is 15 - 7?": "calculator",
    "What is 9 * 5?": "calculator",
    "What is the capital of Japan?": "lookup",
    "Who is the creator of Python?": "lookup",
}


with open(
    "results/real_model_trajectories.json",
    "r",
    encoding="utf-8",
) as file:
    records = json.load(file)


rows = []

for record in records:
    question = record["question"]
    trajectory = record["trajectory"]

    action_steps = [
        step
        for step in trajectory
        if step.get("type") == "action"
    ]

    actual_tool = (
    action_steps[0]["tool"].strip().lower()
    if action_steps
    else "none"
)

    expected_tool = EXPECTED_TOOLS[question]

    correct_tool = actual_tool == expected_tool

    rows.append(
        {
            "question": question,
            "expected_tool": expected_tool,
            "actual_tool": actual_tool,
            "tool_selected": actual_tool != "none",
            "correct_tool": correct_tool,
        }
    )


df = pd.DataFrame(rows)

df.to_csv(
    "results/tool_selection_eval.csv",
    index=False,
)

print(df)

print("\n--- Tool Selection Evaluation ---")
print(f"Tasks: {len(df)}")
print(
    f"Tool Usage Rate: "
    f"{df['tool_selected'].mean():.2%}"
)
print(
    f"Correct Tool Selection Rate: "
    f"{df['correct_tool'].mean():.2%}"
)
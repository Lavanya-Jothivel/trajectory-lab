
import json
import pandas as pd


with open(
    "results/real_model_trajectories.json",
    "r",
    encoding="utf-8",
) as file:
    records = json.load(file)


rows = []

for record in records:
    trajectory = record["trajectory"]

    tool_calls = sum(
        1
        for step in trajectory
        if step.get("type") == "action"
    )

    finish_steps = sum(
        1
        for step in trajectory
        if step.get("type") == "finish"
    )

    rows.append(
        {
            "question": record["question"],
            "steps": record["steps"],
            "tool_calls": tool_calls,
            "finish_steps": finish_steps,
            "had_error": record["error"] is not None,
        }
    )


df = pd.DataFrame(rows)

df.to_csv(
    "results/real_trajectory_metrics.csv",
    index=False,
)

print(df)

print("\n--- Real Trajectory Metrics ---")
print(f"Runs: {len(df)}")
print(f"Average Steps: {df['steps'].mean():.2f}")
print(f"Average Tool Calls: {df['tool_calls'].mean():.2f}")
print(f"Error Rate: {df['had_error'].mean():.2%}")


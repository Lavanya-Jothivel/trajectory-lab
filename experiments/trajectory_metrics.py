import json
import pandas as pd


with open(
    "results/trajectories.json",
    "r",
    encoding="utf-8",
) as file:
    trajectories = json.load(file)


rows = []

for item in trajectories:
    steps = item["trajectory"]

    rows.append(
        {
            "id": item["id"],
            "steps": len(steps),
            "recovered": item["recovered"],
            "verified": item["verified"],
            "corrected": item["corrected"],
        }
    )


df = pd.DataFrame(rows)

df.to_csv(
    "results/trajectory_metrics.csv",
    index=False,
)

print(df)

print("\n--- Trajectory Metrics ---")
print(f"Runs: {len(df)}")
print(f"Average Steps: {df['steps'].mean():.2f}")
print(f"Recovery Rate: {df['recovered'].mean():.2%}")
print(f"Verification Rate: {df['verified'].mean():.2%}")
print(f"Correction Rate: {df['corrected'].mean():.2%}")
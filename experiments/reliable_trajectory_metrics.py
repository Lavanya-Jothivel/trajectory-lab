import json

import pandas as pd


with open(
    "results/reliable_guarded_trajectories.json",
    "r",
    encoding="utf-8",
) as file:
    records = json.load(file)


rows = []

for record in records:
    trajectory = record["trajectory"]

    event_types = [
        event["type"]
        for event in trajectory
    ]

    rows.append(
        {
            "name": record["name"],
            "trajectory_events": len(trajectory),
            "guard_events": event_types.count("guard"),
            "action_events": event_types.count("action"),
            "recovery_events": event_types.count("recovery"),
            "verification_events": event_types.count("verification"),
            "correction_events": event_types.count("correction"),
        }
    )


df = pd.DataFrame(rows)

df.to_csv(
    "results/reliable_trajectory_metrics.csv",
    index=False,
)

print(df.to_string(index=False))

print("\n--- Reliable Trajectory Metrics ---")

print(
    f"Runs: {len(df)}"
)

print(
    f"Average Trajectory Events: "
    f"{df['trajectory_events'].mean():.2f}"
)

print(
    f"Total Guard Events: "
    f"{df['guard_events'].sum()}"
)

print(
    f"Total Tool Actions: "
    f"{df['action_events'].sum()}"
)

print(
    f"Total Recovery Events: "
    f"{df['recovery_events'].sum()}"
)

print(
    f"Total Verification Events: "
    f"{df['verification_events'].sum()}"
)

print(
    f"Total Correction Events: "
    f"{df['correction_events'].sum()}"
)

print(
    f"Recovery Rate: "
    f"{df['recovery_events'].gt(0).mean():.2%}"
)

print(
    f"Verification Rate: "
    f"{df['verification_events'].gt(0).mean():.2%}"
)

print(
    f"Correction Rate: "
    f"{df['correction_events'].gt(0).mean():.2%}"
)

print(
    "\nSaved: results/reliable_trajectory_metrics.csv"
)
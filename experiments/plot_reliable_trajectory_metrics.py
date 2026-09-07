import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "results/reliable_trajectory_metrics.csv"
)


metrics = {
    "Guard": df["guard_events"].sum(),
    "Tool Action": df["action_events"].sum(),
    "Recovery": df["recovery_events"].sum(),
    "Verification": df["verification_events"].sum(),
    "Correction": df["correction_events"].sum(),
}


labels = list(metrics.keys())
values = list(metrics.values())


plt.figure(
    figsize=(8, 5)
)

bars = plt.bar(
    labels,
    values,
)

plt.title(
    "Reliable Agent Trajectory Events"
)

plt.ylabel(
    "Number of Events"
)

plt.ylim(
    0,
    max(values) + 1.5,
)


for bar, value in zip(
    bars,
    values,
):
    plt.text(
        bar.get_x()
        + bar.get_width() / 2,
        value + 0.1,
        str(value),
        ha="center",
    )


plt.tight_layout()

plt.savefig(
    "results/reliable_trajectory_metrics.png",
    dpi=200,
)

plt.close()


print(
    "Saved: results/reliable_trajectory_metrics.png"
)
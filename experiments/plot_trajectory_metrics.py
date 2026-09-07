import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "results/trajectory_metrics.csv"
)

metrics = [
    "Recovery Rate",
    "Verification Rate",
    "Correction Rate",
]

values = [
    df["recovered"].mean() * 100,
    df["verified"].mean() * 100,
    df["corrected"].mean() * 100,
]

plt.figure(figsize=(7, 4))

bars = plt.bar(
    metrics,
    values,
)

plt.ylabel("Rate (%)")
plt.ylim(0, 110)
plt.title("Trajectory-Level Reliability Behavior")

for bar, value in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.1f}%",
        ha="center",
    )

plt.tight_layout()

plt.savefig(
    "results/trajectory_metrics.png",
    dpi=200,
)

plt.close()

print(
    "Saved: results/trajectory_metrics.png"
)
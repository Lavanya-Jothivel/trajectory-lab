import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "results/ablation_summary.csv"
)

labels = df["method"]
values = df["accuracy"]

plt.figure(
    figsize=(10, 5)
)

bars = plt.bar(
    labels,
    values,
)

plt.title(
    "TrajectoryLab Controlled Evaluation Summary"
)

plt.ylabel(
    "Accuracy (%)"
)

plt.ylim(
    0,
    110,
)

plt.xticks(
    rotation=25,
    ha="right",
)

for bar, value in zip(
    bars,
    values,
):
    plt.text(
        bar.get_x()
        + bar.get_width() / 2,
        value + 1.5,
        f"{value:.1f}%",
        ha="center",
        fontsize=8,
    )

plt.tight_layout()

plt.savefig(
    "results/ablation_summary.png",
    dpi=200,
)

plt.close()

print(
    "Saved: results/ablation_summary.png"
)
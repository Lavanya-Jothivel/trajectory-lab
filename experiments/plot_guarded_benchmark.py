import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "results/guarded_benchmark.csv"
)

raw_accuracy = (
    df["raw_correct"].mean() * 100
)

guarded_accuracy = (
    df["guarded_correct"].mean() * 100
)

labels = [
    "Raw Qwen",
    "Guarded Agent",
]

values = [
    raw_accuracy,
    guarded_accuracy,
]

plt.figure(
    figsize=(6, 4)
)

bars = plt.bar(
    labels,
    values,
)

plt.title(
    "Raw Model vs Guarded Agent Accuracy"
)

plt.ylabel(
    "Accuracy (%)"
)

plt.ylim(
    0,
    110,
)

for bar, value in zip(
    bars,
    values,
):
    plt.text(
        bar.get_x()
        + bar.get_width() / 2,
        value + 2,
        f"{value:.2f}%",
        ha="center",
    )

plt.tight_layout()

plt.savefig(
    "results/guarded_benchmark.png",
    dpi=200,
)

plt.close()

print(
    "Saved: results/guarded_benchmark.png"
)
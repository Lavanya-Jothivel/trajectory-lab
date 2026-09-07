import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "results/reliability_summary.csv"
)

baseline = (
    df["baseline_success"].mean() * 100
)

reliability_aware = (
    df["improved_success"].mean() * 100
)

methods = [
    "Baseline",
    "Reliability-Aware Agent",
]

scores = [
    baseline,
    reliability_aware,
]

plt.figure(figsize=(7, 4))

bars = plt.bar(
    methods,
    scores,
)

plt.ylabel("Success Rate (%)")
plt.ylim(0, 110)
plt.title("Reliability Stress-Test Results")

for bar, value in zip(bars, scores):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.1f}%",
        ha="center",
    )

plt.tight_layout()

plt.savefig(
    "results/reliability_summary.png",
    dpi=200,
)

plt.close()

print(
    "Saved: results/reliability_summary.png"
)
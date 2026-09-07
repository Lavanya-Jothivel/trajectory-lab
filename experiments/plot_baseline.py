import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("results/baseline_results.csv")

metrics = {
    "Answer Accuracy": df["answer_correct"].mean() * 100,
    "Tool Accuracy": df["tool_correct"].mean() * 100,
}

plt.figure(figsize=(6, 4))
plt.bar(metrics.keys(), metrics.values())
plt.ylim(0, 110)
plt.ylabel("Accuracy (%)")
plt.title("TrajectoryLab Baseline Performance")

for index, value in enumerate(metrics.values()):
    plt.text(index, value + 2, f"{value:.0f}%", ha="center")

plt.tight_layout()
plt.savefig("results/baseline_accuracy.png", dpi=200)
plt.close()

print("Saved: results/baseline_accuracy.png")
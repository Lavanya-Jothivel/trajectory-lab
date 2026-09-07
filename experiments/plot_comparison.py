import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("results/baseline_comparison.csv")

direct_accuracy = df["direct_correct"].mean() * 100
react_accuracy = df["react_correct"].mean() * 100

methods = ["Direct", "ReAct"]
accuracies = [direct_accuracy, react_accuracy]

plt.figure(figsize=(6, 4))

bars = plt.bar(methods, accuracies)

plt.ylabel("Accuracy (%)")
plt.ylim(0, 110)
plt.title("Direct Answering vs ReAct")

for bar, value in zip(bars, accuracies):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.0f}%",
        ha="center",
    )

plt.tight_layout()

plt.savefig(
    "results/direct_vs_react.png",
    dpi=200,
)

plt.close()

print("Saved: results/direct_vs_react.png")
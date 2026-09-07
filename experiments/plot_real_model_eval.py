import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "results/real_model_eval.csv"
)

accuracy = df["correct"].mean() * 100
average_steps = df["steps"].mean()

labels = [
    "Accuracy (%)",
    "Average Steps",
]

values = [
    accuracy,
    average_steps,
]

plt.figure(figsize=(6, 4))

bars = plt.bar(
    labels,
    values,
)

plt.title("Real-Model ReAct Evaluation")
plt.ylabel("Value")

for bar, value in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.5,
        f"{value:.2f}",
        ha="center",
    )

plt.tight_layout()

plt.savefig(
    "results/real_model_eval.png",
    dpi=200,
)

plt.close()

print(
    "Saved: results/real_model_eval.png"
)
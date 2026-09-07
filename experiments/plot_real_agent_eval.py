import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "results/real_agent_eval.csv"
)

answer_accuracy = (
    df["answer_correct"].mean() * 100
)

tool_accuracy = (
    df["correct_tool"].mean() * 100
)

labels = [
    "Answer Accuracy",
    "Tool Selection Accuracy",
]

values = [
    answer_accuracy,
    tool_accuracy,
]

plt.figure(
    figsize=(7, 4)
)

bars = plt.bar(
    labels,
    values,
)

plt.title(
    "Real-Model Answer vs Tool-Selection Accuracy"
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
    "results/real_agent_accuracy.png",
    dpi=200,
)

plt.close()

print(
    "Saved: results/real_agent_accuracy.png"
)
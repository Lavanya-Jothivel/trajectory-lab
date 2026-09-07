import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "results/verification_comparison.csv"
)

faulty_accuracy = (
    df["faulty_correct"].mean() * 100
)

verification_accuracy = (
    df["verified_correct"].mean() * 100
)

methods = [
    "Faulty Tool",
    "Verification Agent",
]

accuracies = [
    faulty_accuracy,
    verification_accuracy,
]

plt.figure(figsize=(6, 4))

bars = plt.bar(
    methods,
    accuracies,
)

plt.ylabel("Accuracy (%)")
plt.ylim(0, 110)
plt.title("Silent Tool Error Verification")

for bar, value in zip(bars, accuracies):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.1f}%",
        ha="center",
    )

plt.tight_layout()

plt.savefig(
    "results/verification_accuracy.png",
    dpi=200,
)

plt.close()

print(
    "Saved: results/verification_accuracy.png"
)
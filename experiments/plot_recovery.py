import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("results/recovery_comparison.csv")

standard_success = df["standard_success"].mean() * 100
recovery_success = df["recovery_success"].mean() * 100

methods = [
    "Standard",
    "Recovery Agent",
]

success_rates = [
    standard_success,
    recovery_success,
]

plt.figure(figsize=(6, 4))

bars = plt.bar(
    methods,
    success_rates,
)

plt.ylabel("Success Rate (%)")
plt.ylim(0, 110)
plt.title("Tool Failure Recovery Experiment")

for bar, value in zip(bars, success_rates):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.1f}%",
        ha="center",
    )

plt.tight_layout()

plt.savefig(
    "results/recovery_success.png",
    dpi=200,
)

plt.close()

print("Saved: results/recovery_success.png")
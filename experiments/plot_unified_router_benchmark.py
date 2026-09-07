import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "results/unified_router_benchmark.csv"
)


accuracy = df["correct"].mean() * 100
guard_rate = df["guard_triggered"].mean() * 100
abstention_rate = (~df["guard_triggered"]).mean() * 100


labels = [
    "Accuracy",
    "Guard Trigger",
    "Abstention",
]

values = [
    accuracy,
    guard_rate,
    abstention_rate,
]


plt.figure(
    figsize=(7, 5)
)

bars = plt.bar(
    labels,
    values,
)

plt.title(
    "Unified Reliable Router Evaluation"
)

plt.ylabel(
    "Rate (%)"
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
    "results/unified_router_benchmark.png",
    dpi=200,
)

plt.close()


print(
    "Saved: results/unified_router_benchmark.png"
)
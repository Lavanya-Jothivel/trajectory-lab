import pandas as pd

from src.tools import run_tool
from src.recovery_agent import run_recovery_demo


EXPRESSIONS = [
    "8 * 8",
    "(15 + 5) * 3",
    "7 + 9",
]


rows = []

for expression in EXPRESSIONS:
    standard_result = run_tool(
        "unreliable_calculator",
        expression,
    )

    recovery_result = run_recovery_demo(expression)

    standard_success = not standard_result.startswith("ERROR:")

    rows.append(
        {
            "expression": expression,
            "standard_result": standard_result,
            "standard_success": standard_success,
            "recovery_result": recovery_result["answer"],
            "recovery_success": not str(
                recovery_result["answer"]
            ).startswith("ERROR:"),
            "recovered": recovery_result["recovered"],
        }
    )


df = pd.DataFrame(rows)

df.to_csv(
    "results/recovery_comparison.csv",
    index=False,
)

print(df)

print("\n--- Recovery Summary ---")
print(
    f"Standard Success Rate: "
    f"{df['standard_success'].mean():.2%}"
)
print(
    f"Recovery Agent Success Rate: "
    f"{df['recovery_success'].mean():.2%}"
)
print(
    f"Recovery Events: "
    f"{df['recovered'].sum()}"
)
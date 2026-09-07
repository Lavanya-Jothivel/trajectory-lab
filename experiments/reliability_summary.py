import pandas as pd

from src.tools import run_tool
from src.recovery_agent import run_recovery_demo
from src.verification_agent import run_verification_demo


rows = []


# Explicit failure case
expression = "(15 + 5) * 3"

standard_result = run_tool(
    "unreliable_calculator",
    expression,
)

recovery_result = run_recovery_demo(
    expression,
)

rows.append(
    {
        "scenario": "Explicit Tool Failure",
        "baseline_success": not standard_result.startswith("ERROR:"),
        "improved_success": recovery_result["answer"] == "60",
        "mechanism": "Recovery",
    }
)


# Silent error case
expression = "8 * 8"

faulty_result = run_tool(
    "faulty_calculator",
    expression,
)

verification_result = run_verification_demo(
    expression,
)

rows.append(
    {
        "scenario": "Silent Tool Error",
        "baseline_success": faulty_result == "64",
        "improved_success": verification_result["answer"] == "64",
        "mechanism": "Verification",
    }
)


df = pd.DataFrame(rows)

df.to_csv(
    "results/reliability_summary.csv",
    index=False,
)

print(df)

print("\n--- Reliability Summary ---")
print(
    f"Baseline Success: "
    f"{df['baseline_success'].mean():.2%}"
)
print(
    f"Reliability-Aware Success: "
    f"{df['improved_success'].mean():.2%}"
)
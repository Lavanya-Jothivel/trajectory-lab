import pandas as pd

from src.tools import run_tool
from src.verification_agent import run_verification_demo


EXPRESSIONS = [
    ("8 * 8", "64"),
    ("7 + 9", "16"),
    ("6 * 7", "42"),
]


rows = []

for expression, expected_answer in EXPRESSIONS:
    faulty_result = run_tool(
        "faulty_calculator",
        expression,
    )

    verified_result = run_verification_demo(expression)

    rows.append(
        {
            "expression": expression,
            "expected_answer": expected_answer,
            "faulty_result": faulty_result,
            "faulty_correct": faulty_result == expected_answer,
            "verified_result": verified_result["answer"],
            "verified_correct": verified_result["answer"] == expected_answer,
            "correction_made": verified_result["correction_made"],
        }
    )


df = pd.DataFrame(rows)

df.to_csv(
    "results/verification_comparison.csv",
    index=False,
)

print(df)

print("\n--- Verification Summary ---")
print(
    f"Faulty Tool Accuracy: "
    f"{df['faulty_correct'].mean():.2%}"
)
print(
    f"Verification Agent Accuracy: "
    f"{df['verified_correct'].mean():.2%}"
)
print(
    f"Corrections Made: "
    f"{df['correction_made'].sum()}"
)
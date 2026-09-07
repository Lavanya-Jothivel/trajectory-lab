import pandas as pd

from src.reliability_agent import run_reliability_agent


CASES = [
    {
        "id": "normal_01",
        "expression": "7 + 9",
        "primary_tool": "calculator",
        "expected_answer": "16",
        "scenario": "normal",
    },
    {
        "id": "normal_02",
        "expression": "6 * 7",
        "primary_tool": "calculator",
        "expected_answer": "42",
        "scenario": "normal",
    },
    {
        "id": "failure_01",
        "expression": "(15 + 5) * 3",
        "primary_tool": "unreliable_calculator",
        "expected_answer": "60",
        "scenario": "explicit_failure",
    },
    {
        "id": "silent_01",
        "expression": "8 * 8",
        "primary_tool": "faulty_calculator",
        "expected_answer": "64",
        "scenario": "silent_error",
    },
]


rows = []

for case in CASES:
    result = run_reliability_agent(
        case["expression"],
        case["primary_tool"],
    )

    rows.append(
        {
            "id": case["id"],
            "scenario": case["scenario"],
            "expression": case["expression"],
            "primary_tool": case["primary_tool"],
            "expected_answer": case["expected_answer"],
            "predicted_answer": result["answer"],
            "correct": result["answer"]
            == case["expected_answer"],
            "recovered": result["recovered"],
            "verified": result["verified"],
            "corrected": result["corrected"],
            "steps": len(result["trajectory"]),
        }
    )


df = pd.DataFrame(rows)

df.to_csv(
    "results/unified_benchmark.csv",
    index=False,
)

print(df)

print("\n--- Unified Benchmark Summary ---")
print(f"Cases: {len(df)}")
print(f"Accuracy: {df['correct'].mean():.2%}")
print(f"Recoveries: {df['recovered'].sum()}")
print(f"Corrections: {df['corrected'].sum()}")
print(f"Average Steps: {df['steps'].mean():.2f}")
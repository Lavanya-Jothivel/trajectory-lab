import pandas as pd

from experiments.baseline_tasks import TASKS
from src.agent import run_react_agent
from src.baseline import direct_answer


rows = []

for task in TASKS:
    direct = direct_answer(task["question"])
    react = run_react_agent(task["question"])

    rows.append(
        {
            "id": task["id"],
            "question": task["question"],
            "expected_answer": task["expected_answer"],
            "direct_answer": direct,
            "direct_correct": str(direct).lower()
            == str(task["expected_answer"]).lower(),
            "react_answer": react["answer"],
            "react_correct": str(react["answer"]).lower()
            == str(task["expected_answer"]).lower(),
            "react_steps": react["steps"],
        }
    )

df = pd.DataFrame(rows)

df.to_csv(
    "results/baseline_comparison.csv",
    index=False,
)

print(df)

print("\n--- Comparison Summary ---")
print(f"Direct Accuracy: {df['direct_correct'].mean():.2%}")
print(f"ReAct Accuracy: {df['react_correct'].mean():.2%}")
print(f"Average ReAct Steps: {df['react_steps'].mean():.2f}")
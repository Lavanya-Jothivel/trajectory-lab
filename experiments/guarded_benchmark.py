import re
import pandas as pd

from src.model_interface import HuggingFaceModel
from src.guarded_agent import run_guarded_agent


TASKS = [
    {
        "question": "What is 6 * 7?",
        "expected": "42",
    },
    {
        "question": "What is 8 * 8?",
        "expected": "64",
    },
    {
        "question": "What is 12 + 9?",
        "expected": "21",
    },
    {
        "question": "What is 15 - 7?",
        "expected": "8",
    },
    {
        "question": "What is 9 * 5?",
        "expected": "45",
    },
    {
        "question": "What is (15 + 5) * 3?",
        "expected": "60",
    },
]


def extract_number(text):
    if text is None:
        return None

    numbers = re.findall(
        r"-?\d+(?:\.\d+)?",
        str(text),
    )

    if not numbers:
        return None

    return numbers[-1]


model = HuggingFaceModel(
    model_name="Qwen/Qwen2.5-0.5B-Instruct",
    max_new_tokens=80,
)


rows = []

for task in TASKS:
    question = task["question"]
    expected = task["expected"]

    raw_output = model.generate(
        question
    )

    raw_prediction = extract_number(
        raw_output
    )

    guarded_result = run_guarded_agent(
        question
    )

    guarded_prediction = (
        guarded_result["answer"]
    )

    rows.append(
        {
            "question": question,
            "expected": expected,
            "raw_prediction": raw_prediction,
            "raw_correct":
                raw_prediction == expected,
            "guarded_prediction":
                guarded_prediction,
            "guarded_correct":
                guarded_prediction == expected,
            "guard_triggered":
                guarded_result["guard_triggered"],
        }
    )


df = pd.DataFrame(rows)

df.to_csv(
    "results/guarded_benchmark.csv",
    index=False,
)

print(df)

print("\n--- Guarded Agent Benchmark ---")
print(f"Tasks: {len(df)}")

print(
    f"Raw Qwen Accuracy: "
    f"{df['raw_correct'].mean():.2%}"
)

print(
    f"Guarded Agent Accuracy: "
    f"{df['guarded_correct'].mean():.2%}"
)

print(
    f"Guard Trigger Rate: "
    f"{df['guard_triggered'].mean():.2%}"
)
import re
import pandas as pd

from src.model_interface import HuggingFaceModel
from src.guarded_router import run_guarded_router


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
    {
        "question": "What is the capital of Japan?",
        "expected": "Tokyo",
    },
    {
        "question": "Who is the creator of Python?",
        "expected": "Guido van Rossum",
    },
]


def normalize(text):
    if text is None:
        return ""

    return re.sub(
        r"[^a-z0-9]+",
        " ",
        str(text).lower(),
    ).strip()


model = HuggingFaceModel(
    model_name="Qwen/Qwen2.5-0.5B-Instruct",
    max_new_tokens=80,
)


rows = []

for task in TASKS:
    question = task["question"]
    expected = task["expected"]

    raw_answer = model.generate(
        question
    )

    raw_correct = (
        normalize(expected)
        in normalize(raw_answer)
    )

    guarded = run_guarded_router(
        question
    )

    guarded_answer = guarded["answer"]

    guarded_correct = (
        normalize(expected)
        in normalize(guarded_answer)
    )

    rows.append(
        {
            "question": question,
            "expected": expected,
            "raw_answer": raw_answer,
            "raw_correct": raw_correct,
            "guarded_answer": guarded_answer,
            "guarded_correct": guarded_correct,
            "tool": guarded["tool"],
            "guard_triggered":
                guarded["guard_triggered"],
        }
    )


df = pd.DataFrame(rows)

df.to_csv(
    "results/guarded_router_benchmark.csv",
    index=False,
)

print(df)

print("\n--- Guarded Router Benchmark ---")
print(f"Tasks: {len(df)}")

print(
    f"Raw Qwen Accuracy: "
    f"{df['raw_correct'].mean():.2%}"
)

print(
    f"Guarded Router Accuracy: "
    f"{df['guarded_correct'].mean():.2%}"
)

print(
    f"Guard Trigger Rate: "
    f"{df['guard_triggered'].mean():.2%}"
)
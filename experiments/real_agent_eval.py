import json
import re
import pandas as pd


EXPECTED = {
    "What is 6 * 7?": {
        "answer": "42",
        "tool": "calculator",
    },
    "What is 8 * 8?": {
        "answer": "64",
        "tool": "calculator",
    },
    "What is 12 + 9?": {
        "answer": "21",
        "tool": "calculator",
    },
    "What is 15 - 7?": {
        "answer": "8",
        "tool": "calculator",
    },
    "What is 9 * 5?": {
        "answer": "45",
        "tool": "calculator",
    },
    "What is the capital of Japan?": {
        "answer": "Tokyo",
        "tool": "lookup",
    },
    "Who is the creator of Python?": {
        "answer": "Guido van Rossum",
        "tool": "lookup",
    },
}


def normalize_answer(text):
    if text is None:
        return ""

    return re.sub(
        r"[^a-z0-9]+",
        " ",
        str(text).lower(),
    ).strip()


with open(
    "results/real_model_trajectories.json",
    "r",
    encoding="utf-8",
) as file:
    records = json.load(file)


rows = []

for record in records:
    question = record["question"]
    expected = EXPECTED[question]

    answer = record.get("answer")

    normalized_answer = normalize_answer(answer)
    normalized_expected = normalize_answer(
        expected["answer"]
    )

    answer_correct = (
        normalized_expected in normalized_answer
    )

    actions = [
        step
        for step in record["trajectory"]
        if step.get("type") == "action"
    ]

    actual_tool = (
        actions[0]["tool"].strip().lower()
        if actions
        else "none"
    )

    correct_tool = (
        actual_tool == expected["tool"]
    )

    rows.append(
        {
            "question": question,
            "answer": answer,
            "expected_answer": expected["answer"],
            "answer_correct": answer_correct,
            "expected_tool": expected["tool"],
            "actual_tool": actual_tool,
            "correct_tool": correct_tool,
        }
    )


df = pd.DataFrame(rows)

df.to_csv(
    "results/real_agent_eval.csv",
    index=False,
)

print(df)

print("\n--- Real Agent Evaluation ---")
print(f"Tasks: {len(df)}")
print(
    f"Answer Accuracy: "
    f"{df['answer_correct'].mean():.2%}"
)
print(
    f"Correct Tool Selection Rate: "
    f"{df['correct_tool'].mean():.2%}"
)
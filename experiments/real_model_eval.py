import re
import pandas as pd
from src.agent import run_react_agent
from src.model_interface import HuggingFaceModel


TASKS = [
    {
        "question": "What is 6 * 7?",
        "expected": "42",
    },
    {
        "question": "What is 8 * 8?",
        "expected": "64",
    },
]


def extract_number(text):
    """
    Extract the final numeric value from a model answer.
    """

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
    max_new_tokens=100,
)

rows = []
correct = 0

for task in TASKS:
    result = run_react_agent(
        task["question"],
        model=model,
    )

    answer = result.get("answer")

    predicted = extract_number(answer)
    expected = task["expected"]

    is_correct = predicted == expected

    correct += int(is_correct)
    rows.append(
    {
        "question": task["question"],
        "raw_answer": answer,
        "normalized_prediction": predicted,
        "expected": expected,
        "correct": is_correct,
        "steps": result["steps"],
        "error": result.get("error"),
    }
)
    print("\nQuestion:", task["question"])
    print("Raw Answer:", answer)
    print("Normalized Prediction:", predicted)
    print("Expected:", expected)
    print("Correct:", is_correct)
    print("Steps:", result["steps"])

    if result.get("trajectory"):
        print("Trajectory:")

        for item in result["trajectory"]:
            print(item)

    if result.get("error"):
        print("Error:", result["error"])

    if result.get("raw_model_output"):
        print(
            "Raw Model Output:",
            result["raw_model_output"],
        )


accuracy = correct / len(TASKS)
df = pd.DataFrame(rows)

df.to_csv(
    "results/real_model_eval.csv",
    index=False,
)

print("\nSaved: results/real_model_eval.csv")
print("\n--- Real Model Evaluation ---")
print(f"Tasks: {len(TASKS)}")
print(f"Accuracy: {accuracy:.2%}")


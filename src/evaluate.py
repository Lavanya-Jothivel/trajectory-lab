from experiments.baseline_tasks import TASKS
from src.agent import run_react_agent
import pandas as pd


def evaluate():
    results = []

    for task in TASKS:
        output = run_react_agent(task["question"])

        predicted_answer = output["answer"]

        first_step = output["trajectory"][0]
        predicted_tool = first_step.get("tool")

        answer_correct = (
            str(predicted_answer).strip().lower()
            == str(task["expected_answer"]).strip().lower()
        )

        tool_correct = predicted_tool == task["expected_tool"]

        results.append(
            {
                "id": task["id"],
                "question": task["question"],
                "predicted_answer": predicted_answer,
                "expected_answer": task["expected_answer"],
                "predicted_tool": predicted_tool,
                "expected_tool": task["expected_tool"],
                "answer_correct": answer_correct,
                "tool_correct": tool_correct,
                "steps": output["steps"],
            }
        )

    return results


if __name__ == "__main__":
    
    results = evaluate()
    df = pd.DataFrame(results)
    df.to_csv("results/baseline_results.csv", index=False)

    for result in results:
        print(result)

    total = len(results)

    answer_accuracy = sum(
        result["answer_correct"] for result in results
    ) / total

    tool_accuracy = sum(
        result["tool_correct"] for result in results
    ) / total

    average_steps = sum(
        result["steps"] for result in results
    ) / total

    print("\n--- Evaluation Summary ---")
    print(f"Tasks: {total}")
    print(f"Answer Accuracy: {answer_accuracy:.2%}")
    print(f"Tool Accuracy: {tool_accuracy:.2%}")
    print(f"Average Steps: {average_steps:.2f}")
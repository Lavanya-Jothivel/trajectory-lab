from src.model_interface import HuggingFaceModel
from src.react_recovery_agent import (
    run_react_recovery_agent,
)


model = HuggingFaceModel(
    model_name="Qwen/Qwen2.5-0.5B-Instruct",
    max_new_tokens=100,
)


question = "What is (15 + 5) * 3?"

result = run_react_recovery_agent(
    question,
    model=model,
)


print("\n--- Real ReAct Recovery Test ---")
print("Question:", question)
print("Answer:", result.get("answer"))
print("Steps:", result.get("steps"))
print("Recoveries:", result.get("recoveries"))
print("Error:", result.get("error"))

print("\nTrajectory:")

for item in result.get("trajectory", []):
    print(item)

if result.get("raw_model_output"):
    print(
        "\nRaw Model Output:",
        result["raw_model_output"],
    )
from src.model_interface import HuggingFaceModel
from src.guarded_agent import run_guarded_agent


model = HuggingFaceModel(
    model_name="Qwen/Qwen2.5-0.5B-Instruct",
    max_new_tokens=80,
)

question = "What is (15 + 5) * 3?"
expected = "60"


raw_answer = model.generate(question)

guarded_result = run_guarded_agent(
    question
)

guarded_answer = guarded_result["answer"]


print("\n--- Guarded Agent Comparison ---")

print("Question:", question)
print("Expected:", expected)

print("\nRaw Qwen Answer:")
print(raw_answer)

print("\nGuarded Agent Answer:")
print(guarded_answer)

print(
    "\nGuard Triggered:",
    guarded_result["guard_triggered"],
)

print(
    "Guarded Correct:",
    guarded_answer == expected,
)
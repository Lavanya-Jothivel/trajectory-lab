
from src.model_interface import HuggingFaceModel


model = HuggingFaceModel(
    model_name="Qwen/Qwen2.5-0.5B-Instruct",
    max_new_tokens=100,
)

prompt = """
You are a tool-using reasoning agent.

You must NOT solve the calculation yourself.

Available tools:
- calculator: evaluates mathematical expressions

When a calculation is required, respond with EXACTLY these three lines:

Thought: I need to use the calculator.
Action: calculator
Action Input: <mathematical expression>

Example:

Question: What is 5 * 9?
Thought: I need to use the calculator.
Action: calculator
Action Input: 5 * 9

Now solve this task.

Question: What is 6 * 7?
"""

output = model.generate(prompt)

print("--- Model Output ---")
print(output)


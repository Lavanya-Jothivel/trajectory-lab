from src.recovery_agent import run_recovery_demo


expression = "(15 + 5) * 3"

result = run_recovery_demo(
    expression
)

print("\n--- Recovery Test ---")
print("Expression:", expression)
print("Answer:", result["answer"])
print("Recovered:", result["recovered"])

print("\nTrajectory:")
for step in result["trajectory"]:
    print(step)
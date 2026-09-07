
from pprint import pprint

from src.agent import run_react_agent
from src.model_interface import HuggingFaceModel


model = HuggingFaceModel(
    model_name="Qwen/Qwen2.5-0.5B-Instruct",
    max_new_tokens=100,
)

result = run_react_agent(
    "What is 6 * 7?",
    model=model,
)

pprint(result)


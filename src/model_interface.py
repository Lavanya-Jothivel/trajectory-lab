from abc import ABC, abstractmethod

from src.environment import mock_model


class BaseModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate model output for a prompt."""
        pass


class MockModel(BaseModel):
    def generate(self, prompt: str) -> str:
        return mock_model(prompt)


class HuggingFaceModel(BaseModel):
    def __init__(
        self,
        model_name: str,
        max_new_tokens: int = 128,
    ):
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
        )

        self.max_new_tokens = max_new_tokens

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name
        )

        self.model.eval()

    def generate(self, prompt: str) -> str:
        messages = [
            {
                "role": "system",
                "content": (
                    "Follow the requested output format exactly. "
                    "Do not invent tool observations."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        formatted_prompt = (
            self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        )

        inputs = self.tokenizer(
            formatted_prompt,
            return_tensors="pt",
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_new_tokens,
            do_sample=False,
        )

        generated_tokens = outputs[
            0,
            inputs["input_ids"].shape[1]:,
        ]

        text = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True,
        )

        return text.strip()
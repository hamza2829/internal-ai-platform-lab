"""Offline-first adapter. An optional tiny open model is attempted in Actions."""
import os


class MockAdapter:
    name = "deterministic-mock"

    def generate(self, prompt: str, user_input: str) -> str:
        excerpt = " ".join(user_input.split())[:280]
        return f"Demo response (mock): {excerpt}\n\nUse the supplied facts only; verify before taking action."


class TinyModelAdapter:
    name = "sshleifer/tiny-gpt2"

    def __init__(self) -> None:
        from transformers import pipeline
        self.generator = pipeline("text-generation", model=os.getenv("AI_MODEL", self.name), device=-1)

    def generate(self, prompt: str, user_input: str) -> str:
        result = self.generator(f"{prompt}\n", max_new_tokens=80, do_sample=False, pad_token_id=50256)
        return result[0]["generated_text"].split("\n", 1)[-1].strip() or "The model returned no text. Please use the supplied facts and review manually."


def create_adapter():
    if os.getenv("AI_ADAPTER", "mock").lower() == "model":
        try:
            return TinyModelAdapter()
        except Exception:
            pass
    return MockAdapter()

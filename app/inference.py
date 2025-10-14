from llama_cpp import Llama

class LLMEngine:
    def __init__(self, model_path: str, n_ctx: int = 2048):
        self.llm = Llama(model_path=model_path, n_ctx=n_ctx)

    def generate(self, prompt: str) -> str:
        output = self.llm(prompt, max_tokens=256, stop=["</s>"])
        return output["choices"][0]["text"].strip()

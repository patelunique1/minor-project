import traceback
import google.generativeai as genai
from adapters.base import LLMAdapter


class GeminiAdapter(LLMAdapter):
    def __init__(self, api_key: str, model="gemini-1.5-pro"):
        self.api_key = api_key
        self.model_name = model
        self.configured = False

        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.configured = True
        except Exception as e:
            traceback.print_exc()
            self.configured = False

    def generate(self, prompt: str, n: int = 1, temperature: float = 0.8):
        if not self.configured:
            raise RuntimeError("GeminiAdapter not configured properly.")

        completions = []
        try:
            for _ in range(n):
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": temperature,
                        "top_p": 1,
                        "max_output_tokens": 512,
                    }
                )
                completions.append({
                    "text": response.text.strip(),
                    "logprobs": [-1.0]  # Gemini API does not return token logprobs
                })
        except Exception as e:
            print("[GeminiAdapter] Generation failed:")
            traceback.print_exc()
            raise RuntimeError(f"Gemini generation failed: {e}")

        return completions

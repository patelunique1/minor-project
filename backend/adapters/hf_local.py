import together
from adapters.base import LLMAdapter
from evaluation.entropy import pseudo_entropy_from_tokens  # Import actual entropy approximation


class TogetherAIAdapter(LLMAdapter):
    def __init__(self, api_key="tgp_v1_0kGI-hRIIlsBaxm5jPfpb9ayCuPfyJB0Mfppfp6dVP4",                                                     model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"):
        import os
        self.api_key = api_key
        self.model_name = model
        together.api_key = self.api_key

    def build_prompt(self, code: str) -> str:
        return (
            "### Task: Fix the bug in the following function.\n"
            "### Return only the corrected code.\n\n"
            f"{code.strip()}\n"
        )

    def generate(self, prompt: str, n: int = 1, temperature: float = 0.6):
        completions = []

        # Since TogetherAI does not support multiple completions in one call,
        # manually loop to simulate `n` completions.
        for _ in range(n):
            response = together.Complete.create(
                model=self.model_name,
                prompt=prompt,
                max_tokens=256,
                temperature=temperature,
                top_p=0.9,
                stop=["###"]
            )

            text = response.get("choices", [{}])[0].get("text", "").strip()
            completions.append({
                "text": text,
                "logprobs": []  # No logprobs returned by Together
            })

        return completions

    def compute_entropy(self, text: str):
        # Approximate entropy using token diversity
        tokens = text.split()
        norm_entropy, _ = pseudo_entropy_from_tokens(tokens)
        return [norm_entropy] * len(tokens)  # Return pseudo list of same size for compatibility

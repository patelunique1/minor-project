"""
Chain-of-Thought (CoT) style prompt:
We ask the model to reason step by step about potential issues, 
then produce the final refined code.
"""

class CoTPrompt:
    def make_prompt(self, code_snippet: str, language: str = "python") -> str:
        prompt_text = (
            f"Analyze and refine the following {language} code. "
            "Explain reasoning step-by-step, then give final code.\n\n"
            "Code:\n"
            f"{code_snippet}\n\n"
            "Think aloud:\n"
            "# 1) Check syntax\n"
            "# 2) Check correctness\n"
            "# 3) Suggest improvements\n\n"
            "# Final Answer:\n"
        )
        return prompt_text

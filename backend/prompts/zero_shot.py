"""
Simple zero-shot prompt: "Refine the following code for correctness and style."
"""

class ZeroShotPrompt:
    def make_prompt(self, code_snippet: str, language: str = "python") -> str:
        # Minimal zero-shot instruction
        # You can expand this text to ask for style improvements, bug fixes, etc.
        prompt_text = (
            f"Refine the following {language} code. "
            "Fix any bugs, improve readability, but do not change behavior.\n"
            "Code:\n"
            f"{code_snippet}\n\n"
            "Refined code:"
        )
        return prompt_text

"""
Few-shot prompt strategy: Provide 1-2 examples of "buggy code -> refined code"
before the target code snippet.
"""

class FewShotPrompt:
    def __init__(self):
        # Example pairs
        self.example_in = "def add(x, y):\n    return x - y  # bug"
        self.example_out = (
            "def add(x, y):\n"
            "    # Corrected the operation, maintain style\n"
            "    return x + y"
        )

    def make_prompt(self, code_snippet: str, language: str = "python") -> str:
        prompt_text = (
            f"Below are example refinements in {language}.\n\n"
            "Example input:\n"
            f"{self.example_in}\n"
            "Example refined code:\n"
            f"{self.example_out}\n\n"
            "Now refine the following code:\n"
            f"{code_snippet}\n\n"
            "Refined code:"
        )
        return prompt_text

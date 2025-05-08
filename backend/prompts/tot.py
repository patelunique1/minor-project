"""
Tree-of-Thought (ToT) style prompt:
We ask the model to generate multiple branches of reasoning 
and pick the best solution. This is conceptual; 
practical usage requires more advanced orchestration.
"""

class ToTPrompt:
    def make_prompt(self, code_snippet: str, language: str = "python") -> str:
        prompt_text = (
            f"We have code in {language} that may have bugs or style issues. "
            "Use a tree-of-thought approach. Generate possible solutions, "
            "evaluate them, and finalize the best code.\n\n"
            "Code:\n"
            f"{code_snippet}\n\n"
            "Plan multiple solution branches, then converge on best fix.\n"
            "Final refined code:"
        )
        return prompt_text

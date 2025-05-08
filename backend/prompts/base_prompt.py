"""
A base prompt engine that can handle multiple "prompt styles":
zero_shot, few_shot, chain_of_thought, tree_of_thought, etc.
Each style is implemented in a separate file, but
BasePromptEngine coordinates them.
"""

from prompts.zero_shot import ZeroShotPrompt
from prompts.few_shot import FewShotPrompt
from prompts.cot import CoTPrompt
from prompts.tot import ToTPrompt

class PromptEngine:
    """
    Orchestrates different prompt styles. 
    """

    def __init__(self):
        self.strategies = {
            "zero_shot": ZeroShotPrompt(),
            "few_shot": FewShotPrompt(),
            "cot": CoTPrompt(),
            "tot": ToTPrompt()
        }

    def build_prompt(
        self, 
        code_snippet: str, 
        language: str = "python", 
        style: str = "zero_shot"
    ) -> str:
        """
        Delegates to the requested prompt strategy to build the final prompt text.
        """
        if style not in self.strategies:
            style = "zero_shot"
        strategy = self.strategies[style]
        return strategy.make_prompt(code_snippet, language=language)

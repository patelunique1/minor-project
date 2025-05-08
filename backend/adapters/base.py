"""
Base classes / interfaces for LLM model adapters.
All new LLM wrappers should inherit from LLMAdapter.
"""

from abc import ABC, abstractmethod

class LLMAdapter(ABC):
    """
    Abstract base for any Large Language Model adapter.
    Must implement `generate` method returning a list of { "text": ..., "logprobs": [...] }
    """

    @abstractmethod
    def generate(self, prompt: str, n: int = 1, temperature: float = 0.8):
        """
        Generates `n` completions for the given prompt with the specified temperature.
        Returns a list of dict, each dict containing:
          - "text": the generated string
          - "logprobs": a list of token-level log probabilities
        """
        pass

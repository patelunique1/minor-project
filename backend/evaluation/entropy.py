import math
from collections import Counter
from typing import List, Tuple

def mean_entropy(logprobs: List[float]) -> float:
    """
    Computes the mean entropy using actual log probabilities from an API
    (only available for models like OpenAI).
    
    Returns:
        Float value: average entropy per token
    """
    if not logprobs:
        return 0.0
    return -sum(logprobs) / len(logprobs)


def sum_entropy(logprobs: List[float]) -> float:
    """
    Computes the total entropy using actual log probabilities.
    
    Returns:
        Float value: total entropy
    """
    if not logprobs:
        return 0.0
    return -sum(logprobs)


def pseudo_entropy_from_tokens(tokens: List[str]) -> Tuple[float, float]:
    """
    Approximates entropy based on token diversity.
    Useful when logprobs are not available (e.g. Gemini or Meta LLaMA).
    
    Returns:
        Tuple (normalized_entropy [0–1], raw_entropy)
    """
    if not tokens or len(tokens) == 0:
        return 0.0, 0.0

    token_counts = Counter(tokens)
    total_tokens = len(tokens)
    probabilities = [count / total_tokens for count in token_counts.values()]

    # Shannon entropy
    raw_entropy = -sum(p * math.log2(p) for p in probabilities)

    # Normalize by max entropy possible (log2 of number of unique tokens)
    max_entropy = math.log2(len(token_counts)) if len(token_counts) > 1 else 1
    normalized_entropy = raw_entropy / max_entropy if max_entropy else 0.0

    # Clamp to [0.0, 1.0]
    normalized_entropy = max(0.0, min(1.0, normalized_entropy))

    return round(normalized_entropy, 4), round(raw_entropy, 4)

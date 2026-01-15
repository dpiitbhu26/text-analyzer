"""
Word tokenization and frequency counting.
"""

from collections import Counter
from typing import Dict, List, Optional, Tuple


# words we skip - they're too common to be interesting
STOP_WORDS = [
    "the", "and", "is", "at", "which", "on", "a", "an", "as", "are",
    "was", "were", "been", "be", "have", "has", "had", "do", "does",
    "did", "will", "would", "could", "should", "may"
]


class WordCounter:
    """Splits text into words and counts how often each appears."""

    def __init__(self, stop_words: Optional[List[str]] = None) -> None:
        if stop_words is None:
            self._ignored = set(STOP_WORDS)
        else:
            self._ignored = set(w.lower() for w in stop_words)
        self._counts: Dict[str, int] = {}

    def tokenize(self, text: str) -> List[str]:
        """Split into words, drop anything under 3 chars."""
        if not text:
            return []
        return [w for w in text.split() if len(w) >= 3]

    def count_frequencies(self, words: List[str]) -> Dict[str, int]:
        """Count each word, ignoring stop words."""
        if not words:
            self._counts = {}
            return {}

        # skip the boring common words
        filtered = [w for w in words if w.lower() not in self._ignored]
        self._counts = dict(Counter(filtered))
        return self._counts.copy()

    def get_top_n_words(self, n: int) -> List[Tuple[str, int]]:
        """Get the n most common words, sorted by count (desc) then alphabetically."""
        if n < 0:
            raise ValueError("n must be non-negative")
        if n == 0:
            return []

        sorted_words = sorted(self._counts.items(), key=lambda x: (-x[1], x[0]))
        return sorted_words[:n]

    def get_words_starting_with(self, prefix: str) -> List[str]:
        """Find words that start with prefix, sorted alphabetically."""
        if not prefix:
            return sorted(self._counts.keys())

        p = prefix.lower()
        matches = [w for w in self._counts if w.lower().startswith(p)]
        return sorted(matches)

    @property
    def word_frequencies(self) -> Dict[str, int]:
        """Get a copy of the word counts."""
        return self._counts.copy()

"""
Statistics calculation and report generation.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class StatisticsReport:
    """Calculates stats from word frequencies and can export a nice report."""

    def __init__(self, frequencies: Dict[str, int], text: str,
                 source_file: Optional[str] = None) -> None:
        self.word_frequencies = frequencies.copy()
        self.original_text = text
        self.source_file = source_file or "Unknown"
        self._stats: Optional[Dict[str, Any]] = None

    def calculate_statistics(self) -> Dict[str, Any]:
        """
        Figure out total words, unique count, avg length, 
        longest word, and most frequent word.
        """
        if not self.word_frequencies:
            self._stats = {
                "total_word_count": 0,
                "unique_word_count": 0,
                "average_word_length": 0.0,
                "longest_word": "",
                "most_frequent_word": ""
            }
            return self._stats.copy()

        total = sum(self.word_frequencies.values())
        unique = len(self.word_frequencies)

        # avg length weighted by how often each word appears
        char_total = sum(len(w) * cnt for w, cnt in self.word_frequencies.items())
        avg_len = round(char_total / total, 2)

        self._stats = {
            "total_word_count": total,
            "unique_word_count": unique,
            "average_word_length": avg_len,
            "longest_word": self._longest_word(),
            "most_frequent_word": self._most_frequent()
        }
        return self._stats.copy()

    def _longest_word(self) -> str:
        if not self.word_frequencies:
            return ""
        max_len = max(len(w) for w in self.word_frequencies)
        # if there's a tie, pick alphabetically first
        candidates = [w for w in self.word_frequencies if len(w) == max_len]
        return sorted(candidates)[0]

    def _most_frequent(self) -> str:
        if not self.word_frequencies:
            return ""
        max_cnt = max(self.word_frequencies.values())
        candidates = [w for w, c in self.word_frequencies.items() if c == max_cnt]
        return sorted(candidates)[0]

    def _top_words(self, n: int) -> List[Tuple[str, int]]:
        ranked = sorted(self.word_frequencies.items(), key=lambda x: (-x[1], x[0]))
        return ranked[:n]

    def _words_with_prefix(self, prefix: str) -> List[str]:
        p = prefix.lower()
        return sorted(w for w in self.word_frequencies if w.lower().startswith(p))

    def export_report(self, output_path: str) -> None:
        """Write everything to a formatted text file."""
        if self._stats is None:
            self.calculate_statistics()

        stats = self._stats
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        top10 = self._top_words(10)
        a_words = self._words_with_prefix("a")

        lines = [
            "TEXT ANALYSIS REPORT",
            "====================",
            f"File: {self.source_file}",
            f"Generated: {now}",
            "",
            "STATISTICS",
            "----------",
            f"Total Words: {stats['total_word_count']}",
            f"Unique Words: {stats['unique_word_count']}",
            f"Average Word Length: {stats['average_word_length']}",
            f"Longest Word: {stats['longest_word']}",
            f"Most Frequent Word: {stats['most_frequent_word']} ({self.word_frequencies.get(stats['most_frequent_word'], 0)} occurrences)",
            "",
            "TOP 10 MOST FREQUENT WORDS",
            "---------------------------",
        ]

        for i, (word, count) in enumerate(top10, 1):
            lines.append(f"{i}. {word} - {count} occurrences")

        lines.append("")
        lines.append("WORDS STARTING WITH 'A'")
        lines.append("------------------------")
        lines.append(", ".join(a_words) if a_words else "No words starting with 'A' found.")

        # make sure parent dirs exist
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with open(out, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

"""Text Analyzer - reads, analyzes, and reports on text documents."""

from .text_reader import TextReader
from .word_counter import WordCounter
from .statistics_report import StatisticsReport

__version__ = "1.0.0"
__all__ = ["TextReader", "WordCounter", "StatisticsReport"]

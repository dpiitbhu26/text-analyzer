"""
Handles reading and normalizing text files.
"""

import re
from pathlib import Path


class TextReaderError(Exception):
    """Base error for file reading problems."""
    pass

class FileNotFoundError(TextReaderError):
    pass

class FilePermissionError(TextReaderError):
    pass

class EncodingError(TextReaderError):
    pass


class TextReader:
    """Reads text files and cleans them up for analysis."""

    def __init__(self, filepath: str) -> None:
        if not filepath:
            raise ValueError("File path cannot be empty or None")
        self.file_path = Path(filepath)

    def read_file(self) -> str:
        """
        Reads the whole file and returns its content.
        Tries UTF-8 first, falls back to latin-1 if needed.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        if not self.file_path.is_file():
            raise FileNotFoundError(f"Path is not a file: {self.file_path}")

        try:
            return self._read_with_encoding("utf-8")
        except UnicodeDecodeError:
            # latin-1 can read anything, good fallback
            try:
                return self._read_with_encoding("latin-1")
            except Exception as e:
                raise EncodingError(f"Couldn't decode file: {e}")

    def _read_with_encoding(self, encoding: str) -> str:
        try:
            with open(self.file_path, "r", encoding=encoding) as f:
                return f.read()
        except PermissionError:
            raise FilePermissionError(f"Can't access: {self.file_path}")

    def normalize_text(self, text: str) -> str:
        """
        Cleans up text - makes it lowercase, removes punctuation,
        and collapses whitespace. Only letters, numbers and spaces remain.
        """
        if not text:
            return ""

        result = text.lower()
        result = re.sub(r"[\n\t\r]", " ", result)
        result = re.sub(r"[^a-z0-9\s]", "", result)
        result = re.sub(r"\s+", " ", result)
        return result.strip()

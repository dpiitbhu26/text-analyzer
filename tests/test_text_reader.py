"""TextReader tests"""

from pathlib import Path
import pytest
from src.text_reader import TextReader, FileNotFoundError


class TestInit:
    def test_valid_path(self):
        r = TextReader("test.txt")
        assert r.file_path == Path("test.txt")

    def test_empty_path(self):
        with pytest.raises(ValueError):
            TextReader("")

    def test_none_path(self):
        with pytest.raises(ValueError):
            TextReader(None)


class TestReadFile:
    def test_basic_read(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("Hello World", encoding="utf-8")
        assert TextReader(str(f)).read_file() == "Hello World"

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("", encoding="utf-8")
        assert TextReader(str(f)).read_file() == ""

    def test_missing_file(self):
        with pytest.raises(FileNotFoundError):
            TextReader("nope.txt").read_file()

    def test_directory(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            TextReader(str(tmp_path)).read_file()

    def test_unicode(self, tmp_path):
        f = tmp_path / "uni.txt"
        f.write_text("Hello 世界 🌍", encoding="utf-8")
        assert "世界" in TextReader(str(f)).read_file()

    def test_latin1_fallback(self, tmp_path):
        f = tmp_path / "latin.txt"
        f.write_bytes(b"Caf\xe9")  # invalid utf-8
        assert "Caf" in TextReader(str(f)).read_file()

    def test_multiline(self, tmp_path):
        f = tmp_path / "multi.txt"
        f.write_text("line1\nline2\nline3", encoding="utf-8")
        content = TextReader(str(f)).read_file()
        assert "line1" in content and "line3" in content


class TestNormalize:
    @pytest.fixture
    def reader(self, tmp_path):
        f = tmp_path / "x.txt"
        f.write_text("x", encoding="utf-8")
        return TextReader(str(f))

    def test_empty(self, reader):
        assert reader.normalize_text("") == ""

    def test_none(self, reader):
        assert reader.normalize_text(None) == ""

    def test_lowercase(self, reader):
        assert reader.normalize_text("HELLO") == "hello"

    def test_punctuation(self, reader):
        assert reader.normalize_text("hi, there!") == "hi there"

    def test_numbers(self, reader):
        assert reader.normalize_text("test 123") == "test 123"

    def test_special_chars(self, reader):
        assert reader.normalize_text("@#$%") == ""

    def test_whitespace(self, reader):
        assert reader.normalize_text("too   many") == "too many"

    def test_newlines(self, reader):
        assert reader.normalize_text("a\nb") == "a b"

    def test_tabs(self, reader):
        assert reader.normalize_text("a\tb") == "a b"

    def test_mixed(self, reader):
        result = reader.normalize_text("Hello, World! Test 123.")
        assert result == "hello world test 123"


class TestIntegration:
    def test_read_and_normalize(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("Hello, World!\nTest 123", encoding="utf-8")
        r = TextReader(str(f))
        assert r.normalize_text(r.read_file()) == "hello world test 123"

    def test_big_file(self, tmp_path):
        f = tmp_path / "big.txt"
        f.write_text("word " * 5000, encoding="utf-8")
        r = TextReader(str(f))
        result = r.normalize_text(r.read_file())
        assert result.count("word") == 5000

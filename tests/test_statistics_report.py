"""StatisticsReport tests"""

from pathlib import Path
import pytest
from src.statistics_report import StatisticsReport


class TestInit:
    def test_basic(self):
        r = StatisticsReport({"hello": 5}, "text")
        assert r.word_frequencies["hello"] == 5

    def test_copies_data(self):
        freqs = {"hello": 5}
        r = StatisticsReport(freqs, "text")
        freqs["hello"] = 999
        assert r.word_frequencies["hello"] == 5  # shouldn't change

    def test_source_file(self):
        r = StatisticsReport({}, "", source_file="test.txt")
        assert r.source_file == "test.txt"

    def test_default_source(self):
        r = StatisticsReport({}, "")
        assert r.source_file == "Unknown"


class TestStats:
    def test_basic(self):
        r = StatisticsReport({"hello": 3, "world": 2}, "")
        stats = r.calculate_statistics()
        assert stats["total_word_count"] == 5
        assert stats["unique_word_count"] == 2

    def test_empty(self):
        r = StatisticsReport({}, "")
        stats = r.calculate_statistics()
        assert stats["total_word_count"] == 0
        assert stats["longest_word"] == ""

    def test_avg_length(self):
        # cat(3)*2 + dog(3)*2 = 12 / 4 = 3.0
        r = StatisticsReport({"cat": 2, "dog": 2}, "")
        assert r.calculate_statistics()["average_word_length"] == 3.0

    def test_longest(self):
        r = StatisticsReport({"hi": 1, "hello": 1, "superlongword": 1}, "")
        assert r.calculate_statistics()["longest_word"] == "superlongword"

    def test_longest_tie(self):
        # same length, should pick alphabetically first
        r = StatisticsReport({"zebra": 1, "apple": 1}, "")
        assert r.calculate_statistics()["longest_word"] == "apple"

    def test_most_frequent(self):
        r = StatisticsReport({"rare": 1, "common": 10}, "")
        assert r.calculate_statistics()["most_frequent_word"] == "common"

    def test_most_frequent_tie(self):
        r = StatisticsReport({"zebra": 5, "apple": 5}, "")
        assert r.calculate_statistics()["most_frequent_word"] == "apple"


class TestExport:
    @pytest.fixture
    def report(self):
        freqs = {
            "python": 10, "code": 8, "development": 6,
            "testing": 4, "analysis": 3, "algorithm": 2
        }
        return StatisticsReport(freqs, "", source_file="test.txt")

    def test_creates_file(self, report, tmp_path):
        out = tmp_path / "report.txt"
        report.export_report(str(out))
        assert out.exists()

    def test_format(self, report, tmp_path):
        out = tmp_path / "report.txt"
        report.export_report(str(out))
        content = out.read_text()
        assert "TEXT ANALYSIS REPORT" in content
        assert "STATISTICS" in content
        assert "Total Words:" in content

    def test_filename_in_report(self, report, tmp_path):
        out = tmp_path / "report.txt"
        report.export_report(str(out))
        assert "File: test.txt" in out.read_text()

    def test_top_words(self, report, tmp_path):
        out = tmp_path / "report.txt"
        report.export_report(str(out))
        assert "1. python - 10 occurrences" in out.read_text()

    def test_a_words(self, report, tmp_path):
        out = tmp_path / "report.txt"
        report.export_report(str(out))
        content = out.read_text()
        assert "algorithm" in content
        assert "analysis" in content

    def test_creates_dirs(self, report, tmp_path):
        out = tmp_path / "some" / "nested" / "dir" / "report.txt"
        report.export_report(str(out))
        assert out.exists()

    def test_empty_data(self, tmp_path):
        r = StatisticsReport({}, "")
        out = tmp_path / "empty.txt"
        r.export_report(str(out))
        assert "Total Words: 0" in out.read_text()

    def test_no_a_words(self, tmp_path):
        r = StatisticsReport({"python": 1, "code": 1}, "")
        out = tmp_path / "no_a.txt"
        r.export_report(str(out))
        assert "No words starting with 'A'" in out.read_text()


class TestIntegration:
    def test_full_workflow(self, tmp_path):
        freqs = {"python": 15, "code": 8, "amazing": 5}
        r = StatisticsReport(freqs, "", source_file="sample.txt")

        stats = r.calculate_statistics()
        assert stats["total_word_count"] == 28
        assert stats["most_frequent_word"] == "python"

        out = tmp_path / "final.txt"
        r.export_report(str(out))
        assert "python" in out.read_text()

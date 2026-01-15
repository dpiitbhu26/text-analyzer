"""WordCounter tests"""

import pytest
from src.word_counter import WordCounter, STOP_WORDS


class TestInit:
    def test_defaults(self):
        c = WordCounter()
        assert len(c._ignored) == 25
        assert "the" in c._ignored

    def test_custom_stops(self):
        c = WordCounter(stop_words=["foo", "bar"])
        assert "foo" in c._ignored
        assert "the" not in c._ignored

    def test_no_stops(self):
        c = WordCounter(stop_words=[])
        assert len(c._ignored) == 0


class TestTokenize:
    @pytest.fixture
    def counter(self):
        return WordCounter()

    def test_basic(self, counter):
        assert counter.tokenize("hello world") == ["hello", "world"]

    def test_empty(self, counter):
        assert counter.tokenize("") == []

    def test_short_words(self, counter):
        # should filter out i, am, a
        result = counter.tokenize("i am a developer")
        assert result == ["developer"]

    def test_exactly_3_chars(self, counter):
        assert "cat" in counter.tokenize("the cat sat")

    def test_numbers(self, counter):
        assert "123" in counter.tokenize("test 123 456")


class TestCountFrequencies:
    @pytest.fixture
    def counter(self):
        return WordCounter()

    def test_basic(self, counter):
        freqs = counter.count_frequencies(["hello", "world", "hello"])
        assert freqs["hello"] == 2
        assert freqs["world"] == 1

    def test_empty(self, counter):
        assert counter.count_frequencies([]) == {}

    def test_stops_filtered(self, counter):
        freqs = counter.count_frequencies(["the", "hello", "and"])
        assert "the" not in freqs
        assert "hello" in freqs

    def test_only_stops(self, counter):
        assert counter.count_frequencies(["the", "and", "is"]) == {}

    def test_all_stops(self):
        c = WordCounter()
        assert c.count_frequencies(STOP_WORDS) == {}


class TestTopN:
    @pytest.fixture
    def counter(self):
        c = WordCounter()
        c.count_frequencies(["apple", "apple", "apple", "banana", "banana", "cherry"])
        return c

    def test_basic(self, counter):
        top = counter.get_top_n_words(2)
        assert top[0] == ("apple", 3)
        assert top[1] == ("banana", 2)

    def test_zero(self, counter):
        assert counter.get_top_n_words(0) == []

    def test_negative(self, counter):
        with pytest.raises(ValueError):
            counter.get_top_n_words(-1)

    def test_more_than_exists(self, counter):
        assert len(counter.get_top_n_words(100)) == 3

    def test_tie_alphabetical(self):
        c = WordCounter()
        c.count_frequencies(["zebra", "apple"])
        # same count, should be alphabetical
        top = c.get_top_n_words(2)
        assert top[0][0] == "apple"


class TestPrefix:
    @pytest.fixture
    def counter(self):
        c = WordCounter()
        c.count_frequencies(["apple", "application", "banana", "apricot"])
        return c

    def test_match(self, counter):
        result = counter.get_words_starting_with("app")
        assert "apple" in result
        assert "application" in result
        assert "apricot" not in result

    def test_case_insensitive(self, counter):
        assert counter.get_words_starting_with("APP") == counter.get_words_starting_with("app")

    def test_no_match(self, counter):
        assert counter.get_words_starting_with("xyz") == []

    def test_empty_prefix(self, counter):
        # should return all words
        assert len(counter.get_words_starting_with("")) == 4

    def test_sorted(self, counter):
        result = counter.get_words_starting_with("a")
        assert result == sorted(result)


class TestIntegration:
    def test_full_flow(self):
        c = WordCounter()
        words = c.tokenize("the quick brown fox jumps over the lazy dog")
        freqs = c.count_frequencies(words)
        
        assert "the" not in freqs  # stop word
        assert "quick" in freqs
        assert len(c.get_top_n_words(3)) == 3

    def test_copy_returned(self):
        c = WordCounter()
        c.count_frequencies(["hello"])
        copy = c.word_frequencies
        copy["hello"] = 999
        assert c.word_frequencies["hello"] == 1

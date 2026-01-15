<<<<<<< HEAD
# text-analyzer
=======
# Text Analyzer

Analyzes text files - counts words, calculates stats, generates reports.

## What it does

- Reads text files (UTF-8 or latin-1)
- Normalizes text (lowercase, strips punctuation)
- Counts word frequencies (skips common words like "the", "and", etc)
- Calculates stats: word counts, averages, longest/most frequent words
- Exports formatted reports

## Setup

```bash
cd text-analyzer
python3 -m venv venv
source venv/bin/activate   # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

**Requirements:** Python 3.8+

## Quick example

```python
from src import TextReader, WordCounter, StatisticsReport

# read and clean up the text
reader = TextReader("data/sample_text.txt")
text = reader.normalize_text(reader.read_file())

# count words
counter = WordCounter()
words = counter.tokenize(text)
freqs = counter.count_frequencies(words)

# top 10 words
for word, count in counter.get_top_n_words(10):
    print(f"{word}: {count}")

# generate report
report = StatisticsReport(freqs, text, source_file="sample_text.txt")
report.export_report("output/report.txt")
```

## Sample output

Console:

```
code: 20
data: 16
development: 11
...
```

Report file:

```
TEXT ANALYSIS REPORT
====================
File: sample_text.txt
Generated: 2026-01-13 20:54:48

STATISTICS
----------
Total Words: 1001
Unique Words: 663
Average Word Length: 7.24
Longest Word: deserialization
Most Frequent Word: code (20 occurrences)

TOP 10 MOST FREQUENT WORDS
---------------------------
1. code - 20 occurrences
2. data - 16 occurrences
...
```

## Running tests

```bash
pytest                              # all tests
pytest --cov=src                    # with coverage
pytest tests/test_word_counter.py   # specific file
```

Coverage: ~96%

## How it works

**Normalization:** lowercase everything, remove punctuation, collapse whitespace

**Filtering:**

- Skip words under 3 characters
- Skip 25 common stop words (the, and, is, at, which, etc)

**Ties:** When words tie for longest or most frequent, picks alphabetically first

## Stop words

```
the, and, is, at, which, on, a, an, as, are,
was, were, been, be, have, has, had, do, does,
did, will, would, could, should, may
```

## Limitations

- Reads whole file into memory (not great for huge files)
- Only keeps a-z, 0-9 after normalization (strips unicode letters)
- English-focused stop word list

## Troubleshooting

**File not found** - check the path, try absolute path

**Empty results** - might be all stop words or short words, try `stop_words=[]`

**Import errors** - make sure venv is activated, run from project root
>>>>>>> 2bc9d26 (initial commit)

# Regex Scan Corpus for *Shuenjoyu* Paratext Analysis

Companion code repository for the paper **"副文本与深度翻译视角下《主角》日译本的译者阐释体系研究"** (*The Translator's Interpretive System in the Japanese Translation of Chen Yan's* The Protagonist: *A Paratextual and Thick Translation Perspective*).

## Overview

This repository contains the full-text regex scanning pipeline used to identify and classify 820 marked paratextual phenomena across 12,460 lines of the Japanese translation *Shuenjoyu* (《主演女優》, Vol. I). The scan covers 411,511 characters and identifies six categories of marked paratext as defined under Genette's (1997) framework. An additional 306 unmarked implicit paratextual additions were identified through AI-assisted bilingual close reading (not part of the regex pipeline), bringing the total paratextual/interpreting phenomena to 1,126.

## File Structure

```
├── README.md                  # This file
├── regex_patterns.py          # Compiled regex patterns for all paratext types
├── scan_pipeline.py           # End-to-end scanning, dedup, and classification pipeline
├── requirements.txt           # Python dependencies
└── sample_output.json         # Anonymized sample output (10 records per category)
```

## Regex Pattern Categories

| Category | Pattern ID | Count | Description |
|----------|-----------|-------|-------------|
| Parenthetical explanations | `PAREN_NOTE` | 439 | Inline notes embedded in `（ ）` within the text body |
| Numbered translator's notes | `FNOTE_MARK` | 59 | Footnote-style notes marked with `（注）` (58) or `（訳注）` (1) |
| Bilingual explanatory pairs | `BILING_PAIR` | 290 | Chinese original + Japanese explanation (arrow: 3, bracket: 285, structural: 2) |
| Internal cross-references | `XREF` | 16 | Cross-page references (e.g., `上卷五九ページ参照`) |
| Illustration credits | `ILLUS_CREDIT` | 4 | Image/illustration source annotations |
| External paratext items | `EXT_PARATEXT` | 12 | Cover, preface, author message, colophon, etc. (manually catalogued) |
| **Marked paratext total** | | **820** | 12 + 59 + 439 + 290 + 16 + 4 |

Additionally, 669 ruby (*furigana*) glosses were identified (pattern `RUBY_GLOSS`) but excluded from the paratextual count per Genette's strict definition. The gloss `イチンオー→易青娥` repeats 792 times across the volume, reflecting the translator's systematic redundancy strategy.

## Beyond Regex: Unmarked Implicit Additions

The regex scan captures only formally marked paratext. Through AI-assisted bilingual close reading of all 12,460 lines, an additional **306 unmarked implicit paratextual additions** were identified, classified into four types:

| Type | Code | Count | % |
|------|------|-------|---|
| Semantic Extension | SEM | 160 | 52.3% |
| Information Increment | INF | 107 | 35.0% |
| Structural Embedding | SYN | 22 | 7.2% |
| Cultural Analogy | ANA | 17 | 5.6% |

These fully embedded additions have no formal markers and are invisible to regex scanning — they constitute a "deep paratext" layer only detectable through systematic bilingual close reading.

**Combined total: 820 (marked) + 306 (unmarked) = 1,126 paratextual/interpreting phenomena.**

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run full scan (requires OCR-cleaned text file)
python scan_pipeline.py --input path/to/shuenjoyu_vol1_clean.txt --output results.json

# Run scan with detailed per-category breakdown
python scan_pipeline.py --input path/to/shuenjoyu_vol1_clean.txt --output results.json --verbose
```

## Input Data

The scan expects a UTF-8 encoded plain-text file that has been:
1. OCR'd from the Japanese print edition using Tesseract 5.x with Japanese language pack (accuracy ~97.3%)
2. Cleaned: removal of line-break noise, normalization of fullwidth/halfwidth characters
3. Preserved: original page-number markers, all note symbols, and ruby annotations

## Citation

If you use this code in your research, please cite:

> 孙凡. 副文本与深度翻译视角下《主角》日译本的译者阐释体系研究[D]. 兰州: 兰州理工大学, 2026.

## License

MIT License. The regex patterns are provided for reproducibility; the scanned text of *Shuenjoyu* is not included due to copyright restrictions.

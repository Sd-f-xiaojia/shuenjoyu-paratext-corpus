# Regex Scan Corpus for *Shuenjoyu* Paratext Analysis

Companion code repository for the paper **"副文本与深度翻译视角下《主角》日译本的译者阐释体系研究"** (*The Translator's Interpretive System in the Japanese Translation of Chen Yan's* The Protagonist: *A Paratextual and Thick Translation Perspective*).

## Overview

This repository contains the full-text regex scanning pipeline used to identify and classify 866 paratextual phenomena across 30,120 lines of the Japanese translation *Shuenjoyu* (《主演女優》, Vol. I). The scan covers 430,457 characters and identifies six categories of paratext as defined under Genette's (1997) framework.

## File Structure

```
regex-corpus/
├── README.md                  # This file
├── regex_patterns.py          # Compiled regex patterns for all paratext types
├── scan_pipeline.py           # End-to-end scanning, dedup, and classification pipeline
├── requirements.txt           # Python dependencies
└── sample_output.json         # Anonymized sample output (10 records per category)
```

## Regex Pattern Categories

| Category | Pattern ID | Count | Description |
|----------|-----------|-------|-------------|
| Parenthetical explanations | `PAREN_NOTE` | 503 | Inline notes embedded in `（ ）` within the text body |
| Numbered translator's notes | `FNOTE_MARK` | 59 | Footnote-style notes marked with `（注）` or `（訳注）` |
| Bilingual explanatory pairs | `BILING_PAIR` | 251 | Chinese original + Japanese explanation (e.g., `九岩沟→陝西省秦嶺山中の村`) |
| Internal cross-references | `XREF` | 15 | Cross-page references (e.g., `上卷五九ページ参照`) |
| Illustration credits | `ILLUS_CREDIT` | 26 | Image/illustration source annotations |
| External paratext items | `EXT_PARATEXT` | 12 | Cover, preface, author message, colophon, etc. (manually catalogued) |

Additionally, 1,041 ruby (*furigana*) glosses were identified (pattern `RUBY_GLOSS`) but excluded from the paratextual count per Genette's strict definition.

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

> [Author(s)]. 副文本与深度翻译视角下《主角》日译本的译者阐释体系研究[J]. 

## License

MIT License. The regex patterns are provided for reproducibility; the scanned text of *Shuenjoyu* is not included due to copyright restrictions.

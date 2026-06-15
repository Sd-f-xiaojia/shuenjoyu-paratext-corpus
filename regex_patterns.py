"""
Regex patterns for full-text paratext scanning of Shuenjoyu (《主演女優》) Vol. I.
All patterns are compiled with re.UNICODE | re.DOTALL | re.MULTILINE flags.
"""

import re

# ============================================================
# Category A: Parenthetical Explanations 括号文内注释 (503 found)
# ============================================================
# Matches Japanese fullwidth parentheses containing explanatory text
# embedded in the translation body text.
# Excludes: ruby gloss markers 〔...〕, pure punctuation enclosures,
# and OCR artifacts with unmatched brackets.

PAREN_NOTE = re.compile(
    r'（'                           # Fullwidth left parenthesis
    r'(?![）\s]{0,2})'             # Not empty/whitespace-only
    r'[^）]{2,}'                    # Content: 2+ chars (excludes single-char fillers)
    r'）',                          # Fullwidth right parenthesis
    re.UNICODE
)

# Sub-classification patterns for PAREN_NOTE (applied to captured content)
PAREN_SUBCLASS = {
    'vocabulary_gloss': re.compile(
        r'^[぀-ゟ゠-ヿ一-鿿]{1,8}$'  # Short kana/kanji gloss
    ),
    'place_admin': re.compile(
        r'(県|省|市|地区|公社|村|庁|所在地|地方)'
    ),
    'character_role': re.compile(
        r'(師|役|者|員|長|主|官|兵|匠|人|係|僧|侶)'
    ),
    'historical_era': re.compile(
        r'(民国|元年|清代|明代|唐代|宋代|時代|期|世紀|年)'
    ),
    'food_culture': re.compile(
        r'(料理|麺|粉|粥|餅|菜|肉|酒|茶|菓子|旧暦|中秋|端午|節句)'
    ),
    'long_explanatory': re.compile(
        r'.{40,}'  # 40+ chars → long-form explanatory note
    ),
    'object_instrument': re.compile(
        r'(楽器|道具|器具|製品|品|ブランド|機|器)'
    ),
}

# ============================================================
# Category B: Numbered Translator's Notes 脚注式译注 (59 found)
# ============================================================
# Matches （注） and （訳注） markers in the text body.
# These are inline footnote-like references to end-of-section notes.

FNOTE_MARK = re.compile(
    r'（(?:訳)?注'                  # （注） or （訳注）
    r'(?:\s*[^）]*)?'              # Optional note content inline
    r'）',
    re.UNICODE
)

# Distinguish explicit 訳注 from plain 注
FNOTE_EXPLICIT = re.compile(r'（訳注')
FNOTE_IMPLICIT = re.compile(r'（注(?!訳)')

# ============================================================
# Category C: Bilingual Explanatory Pairs 双语对照注释 (251 found)
# ============================================================
# Matches patterns where Chinese original text is juxtaposed with
# Japanese explanation, typically separated by → or 〔...〕 structure.

# Pattern C1: Chinese→Japanese (arrow-separated)
BILING_ARROW = re.compile(
    r'[一-鿿㐀-䶿]{1,20}'   # Chinese characters (1-20)
    r'\s*→\s*'                                # Arrow separator
    r'[^\n]{2,80}',                           # Japanese explanation
    re.UNICODE
)

# Pattern C2: Chinese〔Japanese reading〕
BILING_BRACKET = re.compile(
    r'[一-鿿㐀-䶿]{1,20}'   # Chinese original
    r'\s*〔'                                   # Opening bracket
    r'[^\n]{1,40}'                            # Japanese gloss
    r'〕',                                     # Closing bracket
    re.UNICODE
)

# Sub-classification patterns
BILING_SUBCLASS = {
    'measurement': re.compile(
        r'(グラム|キロ|メートル|センチ|リットル|斤|里|尺|寸|畝|頃|石|斗)'
    ),
    'place_admin': re.compile(
        r'(県|省|市|地区|村|山|川|湖|海)'
    ),
    'opera_art': re.compile(
        r'(劇|曲|腔|調|板|弦|鼓|鑼|笛|琴|舞|歌|芝居|役者|舞台)'
    ),
    'food': re.compile(
        r'(料理|麺|粉|粥|餅|菜|肉|酒|茶|味噌|スープ|鍋)'
    ),
    'character_title': re.compile(
        r'(師|匠|主|長|役|者|先生|夫人|女房|旦那|娘|息子)'
    ),
    'political_history': re.compile(
        r'(革命|文革|四旧|人民|公社|党|政治|運動|闘争|路線)'
    ),
}

# ============================================================
# Category D: Internal Cross-References 跨页内部参照 (15 found)
# ============================================================

XREF = re.compile(
    r'(?:上|中|下)巻'               # Volume reference
    r'\s*[^\n]{0,10}?\s*'           # Optional intervening text
    r'(?:ページ|頁|p\.?)'           # Page markers
    r'\s*\d+'                        # Page number
    r'(?:参照|参考|を見よ|を参照|のこと)?',  # Optional reference phrase
    re.UNICODE
)

# ============================================================
# Category E: Ruby/Furigana Glosses 片假名音注 (1,041 found, EXCLUDED)
# ============================================================
# Matches Japanese ruby phonetic annotations in 〔...〕 brackets.
# These are classified as part of the Japanese writing system,
# NOT as paratext under Genette's definition.

RUBY_GLOSS = re.compile(
    r'〔'                            # Opening ruby bracket
    r'[^\n]{1,30}?'                  # Phonetic gloss (katakana)
    r'〕',                            # Closing ruby bracket
    re.UNICODE
)

# ============================================================
# Category F: OCR Page-Number Markers 页码标记 (225 found, EXCLUDED)
# ============================================================
# Matches residual page-number artifacts from OCR processing.
# These are material traces of digitization, not paratext.

PAGE_MARKER = re.compile(
    r'^\s*\d{1,4}\s*$',             # Standalone numbers (potential page markers)
    re.MULTILINE
)

# Refined: page markers embedded in body text
PAGE_MARKER_INLINE = re.compile(
    r'(?:［|\[)\s*\d{1,4}\s*(?:］|\])'  # [123] or ［123］
    r'|'
    r'^\s*[-–—]+\s*\d{1,4}\s*[-–—]+\s*$',  # --- 123 ---
    re.MULTILINE | re.UNICODE
)

# ============================================================
# Category G: Illustration Credits 插图标注 (26 found)
# ============================================================

ILLUS_CREDIT = re.compile(
    r'(?:図|写真|イラスト|挿絵|口絵|カット|絵)'
    r'[^\n]{0,30}?'
    r'(?:提供|撮影|作|画|筆|所蔵|出典|転載|許可|©|ⓒ)',
    re.UNICODE
)

# ============================================================
# Utility: OCR Artifact Detection
# ============================================================

OCR_ARTIFACT = re.compile(
    r'[■□◆◇△▲▼▽●○★☆]+'        # Decoration characters
    r'|'
    r'[\x00-\x08\x0b\x0c\x0e-\x1f]',  # Control characters
    re.UNICODE
)

# ============================================================
# Pattern Registry (for pipeline use)
# ============================================================

PATTERN_REGISTRY = {
    # Paratextual categories (included in count)
    'paren_note':        ('括号文内注释', PAREN_NOTE, True),
    'fnote_mark':        ('脚注式译注', FNOTE_MARK, True),
    'biling_arrow':      ('双语对照(箭头式)', BILING_ARROW, True),
    'biling_bracket':    ('双语对照(括号式)', BILING_BRACKET, True),
    'xref':              ('跨页内部参照', XREF, True),
    'illus_credit':      ('插图标注', ILLUS_CREDIT, True),

    # Excluded from paratext count
    'ruby_gloss':        ('片假名音注', RUBY_GLOSS, False),
    'page_marker':       ('OCR页码标记', PAGE_MARKER, False),
    'page_marker_inline':('OCR页码标记(行内)', PAGE_MARKER_INLINE, False),
}

SUBCLASS_REGISTRY = {
    'paren_note': PAREN_SUBCLASS,
    'biling_arrow': BILING_SUBCLASS,
    'biling_bracket': BILING_SUBCLASS,
}

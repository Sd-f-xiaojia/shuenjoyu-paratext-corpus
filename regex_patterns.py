"""
Regex patterns for full-text paratext scanning of Shuenjoyu (《主演女優》) Vol. I.
All patterns are compiled with re.UNICODE flags.

Paper data reference (终版):
  Marked paratext total: 820
    外副文本: 12 (manually catalogued)
    脚注式译注: 59 (58注 + 1訳注)
    括号文内注释: 439
    双语对照注释: 290 (箭头式3 + 括号式285 + 结构式2)
    跨页内部参照: 16
    插图标注: 4
  Excluded: 片假名音注 669 (イチンオー→易青娥 repeats 792x)
  Unmarked implicit (via close reading, not regex): 306
  Combined total: 820 + 306 = 1,126
"""

import re

# ============================================================
# Category A: Parenthetical Explanations 括号文内注释 (439 found)
# ============================================================
# Sub-classification:
#   词汇对译/简短解释: 328 (74.7%)
#   地名/行政制度解释: 28 (6.4%)
#   人物/角色说明: 24 (5.5%)
#   时代/历史背景: 5 (1.1%)
#   食物/文化解释: 13 (3.0%)
#   长文解释性注释: 1 (0.2%)
#   器物/乐器说明: 13 (3.0%)
#   其他: 27 (6.2%)

PAREN_NOTE = re.compile(
    r'（'                           # Fullwidth left parenthesis
    r'(?![）\s]{0,2})'             # Not empty/whitespace-only
    r'[^）]{2,}'                    # Content: 2+ chars
    r'）',                          # Fullwidth right parenthesis
    re.UNICODE
)

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
# Sub-classification:
#   政治历史语境注释: 14
#   秦腔戏曲专业知识注释: 13
#   古典文学典故注释: 5
#   民俗文化与社会制度注释: 2
#   地名/行政制度注释: 9
#   戏曲史知识注释: 0
#   其他: 15
#   Explicit 訳注: 1
#   Total: 58 + 1 = 59

FNOTE_MARK = re.compile(
    r'（(?:訳)?注'                  # （注） or （訳注）
    r'(?:\s*[^）]*)?'              # Optional note content inline
    r'）',
    re.UNICODE
)

FNOTE_EXPLICIT = re.compile(r'（訳注')
FNOTE_IMPLICIT = re.compile(r'（注(?!訳)')

# ============================================================
# Category C: Bilingual Explanatory Pairs 双语对照注释 (290 found)
# ============================================================
# Composition:
#   箭头式: 3, 括号式: 285, 结构式: 2
# Sub-classification:
#   度量衡单位换算: 14
#   地名/行政制度: 25
#   戏曲艺术术语: 52
#   食物/料理: 12
#   人物/角色称谓: 24
#   政治/历史术语: 7
#   其他: 156

# Pattern C1: Chinese→Japanese (arrow-separated), 3 found
BILING_ARROW = re.compile(
    r'[一-鿿㐀-䶿]{1,20}'          # Chinese characters (1-20)
    r'\s*→\s*'                      # Arrow separator
    r'[^\n]{2,80}',                 # Japanese explanation
    re.UNICODE
)

# Pattern C2: Chinese〔Japanese reading〕, 285 found
BILING_BRACKET = re.compile(
    r'[一-鿿㐀-䶿]{1,20}'          # Chinese original
    r'\s*〔'                         # Opening bracket
    r'[^\n]{1,40}'                  # Japanese gloss
    r'〕',                           # Closing bracket
    re.UNICODE
)

# Pattern C3: Structural bilingual (inline apposition without brackets), 2 found
BILING_STRUCTURAL = re.compile(
    r'[一-鿿]{2,10}'                # Chinese term
    r'(?:とは|は|という|といい|と呼ばれる|のことで)'
    r'[^\n]{5,60}',                 # Japanese explanation
    re.UNICODE
)

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
# Category D: Internal Cross-References 跨页内部参照 (16 found)
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
# Category E: Ruby/Furigana Glosses 片假名音注 (669 found, EXCLUDED)
# ============================================================
# イチンオー→易青娥 repeats 792 times.
# EXCLUDED under Genette's strict definition: ruby is part of
# the Japanese writing system, not paratext.

RUBY_GLOSS = re.compile(
    r'〔'                            # Opening ruby bracket
    r'[^\n]{1,30}?'                  # Phonetic gloss (katakana)
    r'〕',                            # Closing ruby bracket
    re.UNICODE
)

# ============================================================
# Category F: OCR Page-Number Markers (EXCLUDED)
# ============================================================

PAGE_MARKER = re.compile(
    r'^\s*\d{1,4}\s*$',             # Standalone numbers
    re.MULTILINE
)

PAGE_MARKER_INLINE = re.compile(
    r'(?:［|\[)\s*\d{1,4}\s*(?:］|\])'
    r'|'
    r'^\s*[-–—]+\s*\d{1,4}\s*[-–—]+\s*$',
    re.MULTILINE | re.UNICODE
)

# ============================================================
# Category G: Illustration Credits 插图标注 (4 found)
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
    r'[■□◆◇△▲▼▽●○★☆]+'
    r'|'
    r'[\x00-\x08\x0b\x0c\x0e-\x1f]',
    re.UNICODE
)

# ============================================================
# Pattern Registry (for pipeline use)
# ============================================================

PATTERN_REGISTRY = {
    # Paratextual categories (included in count)
    'paren_note':         ('括号文内注释', PAREN_NOTE, True),
    'fnote_mark':         ('脚注式译注', FNOTE_MARK, True),
    'biling_arrow':       ('双语对照(箭头式)', BILING_ARROW, True),
    'biling_bracket':     ('双语对照(括号式)', BILING_BRACKET, True),
    'biling_structural':  ('双语对照(结构式)', BILING_STRUCTURAL, True),
    'xref':               ('跨页内部参照', XREF, True),
    'illus_credit':       ('插图标注', ILLUS_CREDIT, True),

    # Excluded from paratext count
    'ruby_gloss':         ('片假名音注', RUBY_GLOSS, False),
    'page_marker':        ('OCR页码标记', PAGE_MARKER, False),
    'page_marker_inline': ('OCR页码标记(行内)', PAGE_MARKER_INLINE, False),
}

SUBCLASS_REGISTRY = {
    'paren_note': PAREN_SUBCLASS,
    'biling_arrow': BILING_SUBCLASS,
    'biling_bracket': BILING_SUBCLASS,
    'biling_structural': BILING_SUBCLASS,
}

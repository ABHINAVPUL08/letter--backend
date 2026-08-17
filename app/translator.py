"""Convert name, date, and A-number into Hindi or Punjabi script."""

from __future__ import annotations

import re

_LANGUAGE_NAMES = {
    "hindi": "Hindi (Devanagari script)",
    "punjabi": "Punjabi (Gurmukhi script)",
}

HINDI_DIGITS = str.maketrans("0123456789", "०१२३४५६७८९")
PUNJABI_DIGITS = str.maketrans("0123456789", "੦੧੨੩੪੫੬੭੮੯")

_DIGRAPHS = (
    "aa",
    "ee",
    "oo",
    "ai",
    "au",
    "kh",
    "gh",
    "ch",
    "jh",
    "th",
    "dh",
    "ph",
    "bh",
    "sh",
    "ng",
)

_HINDI = {
    "vowels": {
        "a": ("अ", ""),
        "aa": ("आ", "ा"),
        "i": ("इ", "ि"),
        "ee": ("ई", "ी"),
        "u": ("उ", "ु"),
        "oo": ("ऊ", "ू"),
        "e": ("ए", "े"),
        "ai": ("ऐ", "ै"),
        "o": ("ओ", "ो"),
        "au": ("औ", "ौ"),
    },
    "cons": {
        "k": "क",
        "kh": "ख",
        "g": "ग",
        "gh": "घ",
        "c": "क",
        "ch": "च",
        "j": "ज",
        "jh": "झ",
        "t": "त",
        "th": "थ",
        "d": "द",
        "dh": "ध",
        "n": "न",
        "ng": "ङ",
        "p": "प",
        "ph": "फ",
        "f": "फ",
        "b": "ब",
        "bh": "भ",
        "m": "म",
        "y": "य",
        "r": "र",
        "l": "ल",
        "v": "व",
        "w": "व",
        "sh": "श",
        "s": "स",
        "h": "ह",
        "q": "क",
        "x": "क्स",
        "z": "ज़",
    },
}

_PUNJABI = {
    "vowels": {
        "a": ("ਅ", ""),
        "aa": ("ਆ", "ਾ"),
        "i": ("ਇ", "ਿ"),
        "ee": ("ਈ", "ੀ"),
        "u": ("ਉ", "ੁ"),
        "oo": ("ਊ", "ੂ"),
        "e": ("ਏ", "ੇ"),
        "ai": ("ਐ", "ੈ"),
        "o": ("ਓ", "ੋ"),
        "au": ("ਔ", "ੌ"),
    },
    "cons": {
        "k": "ਕ",
        "kh": "ਖ",
        "g": "ਗ",
        "gh": "ਘ",
        "c": "ਕ",
        "ch": "ਚ",
        "j": "ਜ",
        "jh": "ਝ",
        "t": "ਤ",
        "th": "ਥ",
        "d": "ਦ",
        "dh": "ਧ",
        "n": "ਨ",
        "ng": "ਙ",
        "p": "ਪ",
        "ph": "ਫ",
        "f": "ਫ",
        "b": "ਬ",
        "bh": "ਭ",
        "m": "ਮ",
        "y": "ਯ",
        "r": "ਰ",
        "l": "ਲ",
        "v": "ਵ",
        "w": "ਵ",
        "sh": "ਸ਼",
        "s": "ਸ",
        "h": "ਹ",
        "q": "ਕ",
        "x": "ਕਸ",
        "z": "ਜ਼",
    },
}


def _tokenize(word: str) -> list[str]:
    text = re.sub(r"[^a-z]", "", word.lower())
    tokens: list[str] = []
    i = 0
    while i < len(text):
        if text[i : i + 2] in _DIGRAPHS:
            tokens.append(text[i : i + 2])
            i += 2
        else:
            tokens.append(text[i])
            i += 1
    return tokens


def _transliterate_word(word: str, language: str) -> str:
    table = _PUNJABI if language == "punjabi" else _HINDI
    vowels = table["vowels"]
    cons = table["cons"]
    tokens = _tokenize(word)
    if not tokens:
        return word
    out: list[str] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in vowels:
            out.append(vowels[tok][0])
            i += 1
            continue
        base = cons.get(tok, tok)
        nxt = tokens[i + 1] if i + 1 < len(tokens) else None
        if nxt in vowels:
            independent, matra = vowels[nxt]
            out.append(base + matra if matra or nxt == "a" else independent)
            if nxt == "a":
                out[-1] = base
            i += 2
        else:
            out.append(base)
            i += 1
    return "".join(out)


def to_native_digits(text: str, language: str) -> str:
    if language == "hindi":
        return text.translate(HINDI_DIGITS)
    if language == "punjabi":
        return text.translate(PUNJABI_DIGITS)
    return text


def localize_date(date_text: str, language: str) -> str:
    return to_native_digits(date_text, language)


def localize_a_number(a_number: str, language: str) -> str:
    return to_native_digits(a_number, language)


def _local_name(english_name: str, language: str) -> str:
    parts = [p.strip() for p in english_name.split(",")]
    converted = [_transliterate_word(p, language) if p else p for p in parts]
    return ", ".join(converted)


def transliterate_client_name(english_name: str, language: str) -> str:
    language = (language or "").strip().lower()
    english_name = (english_name or "").strip()
    if not english_name or language not in _LANGUAGE_NAMES:
        return english_name
    return _local_name(english_name, language)

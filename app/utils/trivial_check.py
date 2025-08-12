"""Very small heuristic to short-circuit trivial chat messages.

If the user's text contains any of the predefined Armenian phrases, we treat it
as trivial/small-talk and can fast-path it in handlers.
"""

TRIVIAL_PATTERNS = [
    "բարև",
    "բարև ջան",
    "բարևիկ",
    "ո՞նց ես",
    "ինչ ես անում",
    "ինչ ես",
    "ես ուրախ եմ",
    "այո",
    "ոչ",
    "հահա",
    "լավ",
    "լավ եմ",
    "հա լավ է",
]


def is_trivial_question(text: str) -> bool:
    """Return True if the text likely represents trivial/small-talk content."""
    lowered = text.lower()
    return any(p in lowered for p in TRIVIAL_PATTERNS)

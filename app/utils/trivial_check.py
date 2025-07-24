TRIVIAL_PATTERNS = [
    "բարև", "բարև ջան", "բարևիկ", "ո՞նց ես", "ինչ ես անում", "ինչ ես",
    "ես ուրախ եմ", "այո", "ոչ", "հահա", "լավ", "լավ եմ", "հա լավ է"
]

def is_trivial_question(text: str) -> bool:
    lowered = text.lower()
    return any(p in lowered for p in TRIVIAL_PATTERNS)

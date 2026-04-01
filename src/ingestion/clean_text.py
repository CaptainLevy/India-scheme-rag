import os
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import PROCESSED_DATA_PATH


NOISE_BLOCK_PATTERNS = [
    # Common portal navigation header that appears before real content.
    re.compile(
        r"Back\s*Details\s*Benefits\s*Eligibility\s*Application\s*Process\s*"
        r"Documents\s*Required\s*Frequently\s*Asked\s*Questions\s*"
        r"Sources\s*And\s*References\s*Feedback",
        flags=re.IGNORECASE,
    ),
    # Login/apply popup text captured in many files.
    re.compile(
        r"Ok\s*You\s*need\s*to\s*before\s*applying\s*for\s*schemes\s*Cancel\s*Ok",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"It\s*seems\s*you\s*have\s*already\s*initiated\s*your\s*application\s*"
        r"earlier\.?\s*To\s*know\s*more\s*please\s*visit\s*Cancel",
        flags=re.IGNORECASE,
    ),
    re.compile(r"Apply\s*Now\s*Check\s*Eligibility", flags=re.IGNORECASE),
]

NOISE_PHRASE_PATTERNS = [
    re.compile(r"EngEnglish/?", flags=re.IGNORECASE),
    re.compile(r"You\s*need\s*to\s*before\s*applying\s*for\s*schemes", flags=re.IGNORECASE),
    re.compile(r"Cancel\s*Ok\s*Cancel", flags=re.IGNORECASE),
    re.compile(r"Cancel\s*Sign\s*Out", flags=re.IGNORECASE),
    re.compile(r"Are\s*you\s*sure\s*you\s*want\s*to\s*sign\s*out\??", flags=re.IGNORECASE),
    re.compile(r"\bSign\s*In\b", flags=re.IGNORECASE),
    re.compile(r"\bSign\s*Out\b", flags=re.IGNORECASE),
    re.compile(r"Something\s*went\s*wrong\.\s*Please\s*try\s*again\s*later\.", flags=re.IGNORECASE),
    re.compile(r"\bOk\b", flags=re.IGNORECASE),
    re.compile(r"[^\x00-\x7F]+"),
]

def clean_text(text):
    """Remove recurring portal UI boilerplate while preserving scheme content."""

    for pattern in NOISE_BLOCK_PATTERNS:
        text = pattern.sub(" ", text)

    for pattern in NOISE_PHRASE_PATTERNS:
        text = pattern.sub(" ", text)

    # Clean up extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def clean_all_files():
    """Clean all extracted text files."""
    from tqdm import tqdm

    txt_files = [
        f for f in os.listdir(PROCESSED_DATA_PATH)
        if f.endswith(".txt")
    ]

    print(f"🧹 Cleaning {len(txt_files)} text files...")

    for txt_file in tqdm(txt_files, desc="Cleaning files"):
        file_path = os.path.join(PROCESSED_DATA_PATH, txt_file)

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        cleaned = clean_text(text)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned)

    print(f"\n✅ Successfully cleaned: {len(txt_files)} files")
    print(f"📁 Saved to: {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    clean_all_files()
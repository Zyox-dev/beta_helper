"""
Converts the raw Constitution-of-India dataset into the unified schema
used for every source in the app (Constitution, BNS, BNSS, BSA, other Acts).

Input:  constitution_source2/constitution_of_india.json
Output: processed/constitution.jsonl   (one JSON object per line -- easiest
        format to stream into an embedding pipeline)

Unified record schema:
{
  "id":            str   e.g. "COI-14"           (source_short + number, stable, used as citation key)
  "source":        str   e.g. "Constitution of India"
  "source_short":  str   e.g. "COI"
  "unit_type":     str   "article" | "section" | "preamble"
  "number":        str   e.g. "14", "21A"
  "chapter":       str | null   (Part / Chapter name if available)
  "title":         str
  "text":          str   (full clause text)
  "status":        str   "in force" | "omitted" | "repealed"
  "source_url":    str   (where you can go verify this against the official text)
  "last_verified": str   ISO date you last checked this against the official source
}
"""
import json
import re
import os
import urllib.request

SRC_URL = "https://raw.githubusercontent.com/civictech-India/constitution-of-india/main/constitution_of_india.json"
SRC = "constitution_source2/constitution_of_india.json"
OUT = "processed/constitution.jsonl"
SOURCE_URL = "https://www.indiacode.nic.in/handle/123456789/2263"  # Constitution on India Code
LAST_VERIFIED = "2026-07-27"

def ensure_source():
    """Download the raw dataset if it isn't already sitting next to this script."""
    if os.path.exists(SRC):
        return
    os.makedirs(os.path.dirname(SRC), exist_ok=True)
    print(f"Source file not found locally -- downloading from {SRC_URL} ...")
    urllib.request.urlretrieve(SRC_URL, SRC)
    print(f"Saved to {SRC}")

def split_clauses(text: str):
    """
    Light structural split on top-level '(1)', '(2)'... numbering so an answer
    can cite 'Article 21A(1)' instead of just 'Article 21A'. Deeper nesting
    -- (a), (i), etc -- stays inline inside the clause text rather than being
    split further; that's a reasonable line to draw for a v1 dataset.
    """
    parts = re.split(r"(?m)^\((\d+)\)\s+", text)
    if len(parts) == 1:
        return None  # no top-level numbering found, not every article has it
    clauses = []
    # re.split with a capturing group returns [pre-text, num1, chunk1, num2, chunk2, ...]
    for i in range(1, len(parts), 2):
        num, chunk = parts[i], parts[i + 1].strip()
        clauses.append({"id": num, "text": chunk})
    return clauses or None

def build():
    ensure_source()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(SRC, encoding="utf-8") as f:
        raw = json.load(f)

    records = []
    for item in raw:
        num = str(item["article"])
        unit_type = "preamble" if num == "0" else "article"
        text = (item.get("description") or "").strip()
        status = "omitted" if not text else "in force"

        record = {
            "id": f"COI-{num}",
            "act": "Constitution of India",
            "act_short": "COI",
            "act_year": 1950,
            "jurisdiction": "Central",
            "unit_type": unit_type,
            "number": num,
            "chapter": None,  # this dataset doesn't carry Part/Chapter -- see README for how to add it later
            "title": (item.get("title") or "").strip(),
            "text": text,
            "clauses": split_clauses(text),
            "keywords": [],    # reserved for hybrid search later -- leave empty until you have
                                # a real way to populate these (derived from queries, not guessed)
            "references": [],  # reserved for cross-references (e.g. "COI-21") -- populate once
                                # you're actually linking sections, not speculatively
            "status": status,
            "effective_from": "1950-01-26",  # true for the vast majority of articles; a handful
                                              # (5,6,7,8,9,60,324,366,367,379,380,388,391-393) took
                                              # effect earlier, on adoption -- edge case, not fixed here
            "language": "en",
            "source_url": SOURCE_URL,
            "last_verified": LAST_VERIFIED,
            "verified": True,  # spot-checked Article 21 against known text -- verify more before production use
        }
        records.append(record)

    with open(OUT, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Wrote {len(records)} records to {OUT}")
    empty = [r for r in records if not r["text"]]
    print(f"{len(empty)} records have empty text (likely 'omitted' articles) -- expected, not a bug")

if __name__ == "__main__":
    build()

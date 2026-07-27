"""
Fallback parser for a bare-act PDF (use scrape_indiacode.py instead when possible --
this is only for Acts you can't get cleanly off India Code).

THE PROBLEM THIS SOLVES:
Bare-act PDFs (BNS, BNSS, BSA, etc.) print two columns per page: the main
numbered section text on the left ~80%, and a short marginal title note on
the right ~20% (e.g. "Short title, commencement and application."). Plain
`pdftotext`-style extraction reads left-to-right per line and jumbles these
together, or dumps all the marginal notes as a separate block far from the
sections they belong to.

v2 note: the first version of this script matched section N to
margin_notes_all[N] by LIST POSITION. That's wrong whenever a margin note is
missing, split across a page break, or a chapter heading sneaks into the
margin column -- every title after that point silently shifts to the wrong
section. Fixed here: each section-start line and each margin note keep their
(page, y-position), and a title is matched to the section whose header is
closest in vertical position on the same page. Wrong-page or no-match cases
are left with title="" rather than guessed, so they're visible in the output
instead of silently wrong.

Still NOT handled (left out on purpose -- see README): footnote markers like
"Inserted by Act..."/"Substituted by...", schedules/tables, and sub-clause
hierarchy below one level. If you hit an Act where these matter, treat this
as a starting point, not a finished tool.

HOW TO USE
1. pip install pdfplumber --break-system-packages
2. Download the PDF from an OFFICIAL source (India Code / e-Gazette, not a
   news aggregator -- verify it's the FINAL enacted text, not a withdrawn bill)
3. Set PDF_PATH, SOURCE_NAME, SOURCE_SHORT, MARGIN_X_THRESHOLD below
4. Run and manually check ~10 output sections against the PDF by eye
"""
import json
import re
import time
import pdfplumber

# ---- CONFIGURE THIS PER ACT ----
PDF_PATH = "REPLACE_ME.pdf"
SOURCE_NAME = "Bharatiya Nyaya Sanhita, 2023"
SOURCE_SHORT = "BNS"
SOURCE_URL = "REPLACE_ME"  # the official PDF/gazette URL you downloaded this from
ACT_YEAR = 2023
JURISDICTION = "Central"
EFFECTIVE_FROM = "2024-07-01"
OUT_PATH = f"../processed/{SOURCE_SHORT.lower()}.jsonl"
MARGIN_X_THRESHOLD = 0.78   # fraction of page width; words starting right of this
                            # are treated as marginal note column. Tune per PDF --
                            # print word x0/page width for a sample page first.
TITLE_Y_TOLERANCE = 25      # points; how far (vertically, same page) a margin
                            # note can be from a section header and still count
                            # as its title. Tune against a sample page.
# ---------------------------------

SECTION_START_RE = re.compile(r"^(\d+[A-Z]{0,2})\.\s+")            # 12. / 12A. / 12AA.
CHAPTER_RE = re.compile(r"^CHAPTER\s*[-\u2013\u2014]?\s*([IVXLC]+)\b", re.IGNORECASE)
CLAUSE_RE = re.compile(r"(?m)^\((\d+)\)\s+")

# Lines that are page furniture, not law text -- extend this per-PDF as you
# spot more junk in your output (running titles, bill numbers, etc).
FOOTER_NOISE_RE = re.compile(
    r"^\d{1,4}$"                                   # bare page number
    r"|^TO BE INTRODUCED IN LOK SABHA$"
    r"|^Bill No\.?\s*\d+ of \d{4}$"
    r"|^THE .+ ACT,? \d{4}$",                        # running page-header repeating the act's title
    re.IGNORECASE,
)


def extract_columns(pdf_path):
    """Yield (page_number, main_lines, margin_lines) where each line is
    (y_top, text) -- keeping position instead of flattening it is what makes
    accurate title-matching possible."""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            width = page.width
            words = page.extract_words()
            main_words = [w for w in words if w["x0"] < width * MARGIN_X_THRESHOLD]
            margin_words = [w for w in words if w["x0"] >= width * MARGIN_X_THRESHOLD]

            def to_lines(word_list):
                lines = {}
                for w in word_list:
                    key = round(w["top"] / 3) * 3  # cluster within ~3pt instead of exact-pixel rounding
                    lines.setdefault(key, []).append(w["text"])
                out = []
                for y in sorted(lines):
                    text = " ".join(lines[y]).strip()
                    if text and not FOOTER_NOISE_RE.match(text):
                        out.append((y, text))
                return out

            yield page_num, to_lines(main_words), to_lines(margin_words)


def build_sections(pdf_path):
    sections = []          # dicts: number, chapter, page, y, body_lines
    margin_by_page = {}    # page_num -> list of (y, text)
    current = None
    current_chapter = None

    for page_num, main_lines, margin_lines in extract_columns(pdf_path):
        margin_by_page[page_num] = margin_lines

        for y, line in main_lines:
            chapter_match = CHAPTER_RE.match(line)
            if chapter_match:
                current_chapter = line.strip()
                continue

            sec_match = SECTION_START_RE.match(line)
            if sec_match:
                if current:
                    sections.append(current)
                current = {
                    "number": sec_match.group(1),
                    "chapter": current_chapter,
                    "page": page_num,
                    "y": y,
                    "body_lines": [line],
                }
            elif current:
                current["body_lines"].append(line)

    if current:
        sections.append(current)

    # Match each section to the nearest margin note ON THE SAME PAGE, by
    # vertical distance -- not by list position. No match within tolerance
    # -> title left blank rather than guessed.
    for sec in sections:
        candidates = margin_by_page.get(sec["page"], [])
        best = None
        best_dist = None
        for y, text in candidates:
            dist = abs(y - sec["y"])
            if dist <= TITLE_Y_TOLERANCE and (best_dist is None or dist < best_dist):
                best, best_dist = text, dist
        sec["title"] = best or ""

    return sections


def split_clauses(text: str):
    parts = CLAUSE_RE.split(text)
    if len(parts) == 1:
        return None
    clauses = []
    for i in range(1, len(parts), 2):
        clauses.append({"id": parts[i], "text": parts[i + 1].strip()})
    return clauses or None


def to_records(sections):
    records = []
    for sec in sections:
        body_text = " ".join(sec["body_lines"])
        records.append({
            "id": f"{SOURCE_SHORT}-{sec['number']}",
            "act": SOURCE_NAME,
            "act_short": SOURCE_SHORT,
            "act_year": ACT_YEAR,
            "jurisdiction": JURISDICTION,
            "unit_type": "section",
            "number": sec["number"],
            "chapter": sec["chapter"],
            "title": sec["title"].strip(".").strip(),
            "text": body_text,
            "clauses": split_clauses(body_text),
            "status": "in force",
            "effective_from": EFFECTIVE_FROM,
            "language": "en",
            "source_url": SOURCE_URL,
            "last_verified": time.strftime("%Y-%m-%d"),
            "verified": False,  # this came off a PDF heuristic -- flip to True only after you've checked it
        })
    return records


if __name__ == "__main__":
    if PDF_PATH == "REPLACE_ME.pdf":
        raise SystemExit("Set PDF_PATH to a real, officially-sourced PDF first.")

    sections = build_sections(PDF_PATH)
    records = to_records(sections)
    missing_titles = [r for r in records if not r["title"]]

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Wrote {len(records)} sections to {OUT_PATH}")
    print(f"{len(missing_titles)} sections have no matched title -- "
          f"check TITLE_Y_TOLERANCE or fill these in by hand: "
          f"{[r['number'] for r in missing_titles[:15]]}")
    print("All records are marked verified=False. Spot-check a sample "
          "against the source PDF before flipping that flag or using this "
          "in anything user-facing.")

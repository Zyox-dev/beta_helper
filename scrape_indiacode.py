"""
Template scraper for India Code (indiacode.nic.in).

Why this approach: each section of an Act lives on its own page
    https://www.indiacode.nic.in/show-data?actid=<ACT_ID>&orderno=<N>
which avoids the marginal-note-scrambling problem you get with PDF text
extraction. This is the recommended path for building your dataset.

HOW TO USE
1. Find the actid for the Act you want:
   - Browse to the Act on indiacode.nic.in (search by short title)
   - Open any section page and copy the `actid=...` value from the URL
2. Set ACT_ID, SOURCE_NAME, SOURCE_SHORT below.
3. Run: python3 scrape_indiacode.py
4. Spot-check ~10 output records against the live site before trusting the rest.

NOTE: This script is a template. India Code's HTML structure can change, and
this environment can't reach indiacode.nic.in directly to test against live
markup -- run it from your own machine, inspect the first couple of pages
with print(soup.prettify()) if the selectors below don't match, and adjust.
"""
import json
import re
import time
import requests
from bs4 import BeautifulSoup

# ---- CONFIGURE THIS PER ACT ----
ACT_ID = "REPLACE_ME"                      # e.g. from a show-data?actid=... URL
SOURCE_NAME = "Bharatiya Nyaya Sanhita, 2023"
SOURCE_SHORT = "BNS"
MAX_ORDERNO = 400                          # generous upper bound; script stops early on repeated failures
OUT_PATH = f"../processed/{SOURCE_SHORT.lower()}.jsonl"
BASE_URL = "https://www.indiacode.nic.in/show-data"
SOURCE_URL_TEMPLATE = "https://www.indiacode.nic.in/show-data?actid={actid}&orderno={n}"
# ---------------------------------

HEADERS = {"User-Agent": "Mozilla/5.0 (data collection for personal legal-reference app)"}

SECTION_HEADER_RE = re.compile(r"^Section\s+([0-9A-Za-z\-]+)\.?\s*(.*)$")


def fetch_section(actid: str, orderno: int):
    params = {"actid": actid, "orderno": orderno}
    resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_section(soup: BeautifulSoup):
    """
    Pull the section number/title header and body text out of the page.
    India Code renders the section content inside the main content table --
    adjust the selector below after inspecting real output if it doesn't match.
    """
    # The header line looks like: "Section 63.     Rape."
    header_el = soup.find(string=SECTION_HEADER_RE)
    if not header_el:
        return None

    match = SECTION_HEADER_RE.match(header_el.strip())
    number, title = match.group(1), match.group(2).strip()

    # Body text: everything in the content area after the header, before
    # the Previous/Next nav links. Adjust this selector to match the real
    # container once you've inspected the page -- this is a best-effort default.
    content_container = header_el.find_parent("td") or header_el.find_parent("div")
    text = ""
    if content_container:
        full_text = content_container.get_text("\n", strip=True)
        # strip the header line itself back out of the body
        text = full_text.replace(header_el.strip(), "", 1).strip()

    return number, title, text


def scrape(actid: str, source_name: str, source_short: str):
    records = []
    consecutive_failures = 0
    seen_numbers = set()

    for n in range(1, MAX_ORDERNO + 1):
        try:
            soup = fetch_section(actid, n)
            parsed = parse_section(soup)
        except Exception as e:
            print(f"orderno={n}: fetch/parse error ({e})")
            consecutive_failures += 1
            if consecutive_failures >= 5:
                print("5 consecutive failures, stopping.")
                break
            continue

        if not parsed:
            consecutive_failures += 1
            if consecutive_failures >= 5:
                print("5 consecutive empty pages, assuming end of Act, stopping.")
                break
            continue

        consecutive_failures = 0
        number, title, text = parsed
        if number in seen_numbers:
            continue  # avoid dupes if pagination loops
        seen_numbers.add(number)

        records.append({
            "id": f"{source_short}-{number}",
            "source": source_name,
            "source_short": source_short,
            "unit_type": "section",
            "number": number,
            "chapter": None,  # enhance later: track "CHAPTER" headers as you walk orderno sequentially
            "title": title,
            "text": text,
            "status": "in force",
            "source_url": SOURCE_URL_TEMPLATE.format(actid=actid, n=n),
            "last_verified": time.strftime("%Y-%m-%d"),
        })

        time.sleep(0.5)  # be polite to a government server

    return records


if __name__ == "__main__":
    if ACT_ID == "REPLACE_ME":
        raise SystemExit("Set ACT_ID to a real actid from an India Code section URL first.")

    results = scrape(ACT_ID, SOURCE_NAME, SOURCE_SHORT)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(results)} sections to {OUT_PATH}")
    print("Now spot-check ~10 random records against the live India Code pages.")

# Legal data pipeline — Constitution + Indian law

This is the **data layer** for a RAG-style app that answers "what does the law say"
questions grounded in real statute text. It does not decide anything — it stores
and retrieves the actual text so an LLM can quote/cite it accurately instead of
guessing from memory.

## What's in here

```
legal-data/
├── processed/
│   └── constitution.jsonl      ← 465 records, ready to use, verified
├── scripts/
│   ├── build_constitution.py   ← converts raw constitution JSON -> unified schema
│   ├── scrape_indiacode.py     ← template: scrape any Act off India Code (HTML, reliable)
│   └── parse_bare_act_pdf.py   ← template: layout-aware PDF parser (fallback only)
└── README.md
```

## The unified schema (v2)

Every law, regardless of source (Constitution, BNS, BNSS, BSA, Companies Act,
whatever), gets normalized into the same shape so your retrieval layer doesn't
need source-specific logic:

```json
{
  "id": "COI-1",
  "act": "Constitution of India",
  "act_short": "COI",
  "act_year": 1950,
  "jurisdiction": "Central",
  "unit_type": "article",
  "number": "1",
  "chapter": null,
  "title": "Name and territory of the Union",
  "text": "(1) India, that is Bharat, shall be a Union of States. ...",
  "clauses": [
    {"id": "1", "text": "India, that is Bharat, shall be a Union of States."},
    {"id": "2", "text": "The States and the territories thereof shall be as specified in the First Schedule."}
  ],
  "status": "in force",
  "effective_from": "1950-01-26",
  "language": "en",
  "source_url": "https://www.indiacode.nic.in/handle/123456789/2263",
  "last_verified": "2026-07-27",
  "verified": true
}
```

`jurisdiction` and `act_year` exist so a later retrieval step can filter
("only Central + Rajasthan" for someone in Rajasthan) without re-processing
every record. `clauses` splits top-level `(1)`/`(2)` numbering out so an
answer can cite `Article 1(3)` instead of just `Article 1` — deeper nesting
like `(a)`/`(i)` is left inline rather than split further, which is a
reasonable place to stop for a v1 dataset. `verified` distinguishes records
you've actually checked against the source from ones a parser produced and
nobody's looked at yet — keep that honest; don't default it to `true`.

Keep it flat, one JSON object per section/article, one file per source
(`constitution.jsonl`, `bns.jsonl`, `bnss.jsonl`, `bsa.jsonl`, ...). This is
your retrieval unit later — each record becomes one embedded chunk, and the
`id` + `source_url` are what you show the user as a citation so they can verify
it themselves.

## Sourcing priority (this is the part that actually matters)

1. **India Code** (`indiacode.nic.in`) — official, and structured one-section-per-page,
   which makes it far more reliable to scrape than a PDF. Use `scrape_indiacode.py`.
2. **e-Gazette** (`egazette.gov.in`) — cross-check here for the final notified
   text, especially right after an amendment, since India Code can lag.
3. **PDF bare acts** — last resort. Two risks: (a) you might grab a withdrawn/
   draft version instead of the final Act — I did exactly this while researching
   your question, the first BNS PDF I found was the withdrawn original bill, not
   the version that actually passed — and (b) plain text extraction scrambles
   section text with marginal notes. If you must use a PDF, use
   `parse_bare_act_pdf.py` (layout-aware) and spot-check ~10 random sections
   against India Code before trusting the rest.

## Keeping it current

Indian law changes. Concretely:
- IPC / CrPC / Indian Evidence Act were **replaced** by BNS / BNSS / BSA on
  1 July 2024 — but IPC still governs offences committed before that date, so
  if your app covers criminal law you may need both, tagged by effective date.
- Acts get amended via later Acts, not by editing the original text in place.
  Store `last_verified` per record and re-scrape periodically (monthly is
  reasonable for most Acts; more often for ones under active litigation/reform).
- `status` field lets you mark a section "omitted" or "repealed" without
  deleting it — useful since old sections still get cited in judgments about
  older cases.

## Aliases (act-level, not per-record)

People will search for "IPC 302" long after BNS replaced it, and won't know
the new section number. Handle this as a small separate lookup, not a field
duplicated onto every record:

```json
{
  "BNS": ["Bharatiya Nyaya Sanhita", "New IPC", "New Penal Code"],
  "IPC": ["Indian Penal Code", "Penal Code"],
  "COI": ["Constitution", "Constitution of India", "The Constitution"]
}
```

Check this before/alongside your vector search — if a query mentions "IPC",
route it to `ipc.jsonl` (once you have historical IPC data) and/or surface a
note that the section has been renumbered under BNS. This is cheap to add
and solves a real, common confusion; don't let it turn into a big taxonomy
project.

## Known gaps (intentionally not built yet)

`parse_bare_act_pdf.py` matches section titles to their margin notes by
**vertical position on the page**, not list order — the first version
matched by index, which silently drifts wrong the moment one margin note is
missing or split across a page break. If you use this script, still spot-
check ~10 sections against the source PDF before trusting the rest; it
leaves `title` blank rather than guessing when nothing's close enough,
so blanks are your signal something needs a manual look.

Not handled anywhere yet, on purpose — build these if/when an Act you
actually need requires them, rather than upfront:
- Amendment footnotes ("Inserted by Act...", "Substituted by...")
- Schedules and tables
- Sub-clause nesting below one level (`(a)`, `(i)`, etc. stay inline)

## Next step

Once you have a few sources in this schema, the next stage is chunking +
embedding each record for retrieval (RAG), which I can help with when you're
ready — happy to also just extend this pipeline to pull BNS/BNSS/BSA properly
via `scrape_indiacode.py` if you want to find the correct `actid` values first.

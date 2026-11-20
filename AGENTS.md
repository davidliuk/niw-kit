# AGENTS.md

A workspace for one person's EB-2 National Interest Waiver (NIW) I-140
self-petition: templates, a playbook, and a reproducible PDF toolchain. It
holds the applicant's real evidence and status, so correctness outranks
speed. Nothing here is legal advice; counsel decides what to claim.

## Layout

| Path | Contents |
| --- | --- |
| `README.md` | Overview and quick start (Chinese) |
| `playbook/` | Method guides: roadmap, legal standard, writing, letters, evidence, online filing, review, common weaknesses, RFE (Chinese) |
| `case-template/` | Blank case: `case.json`, `workproduct/` drafts and controls, `letters/`, `data/` registry and manifest, `rfe-template/` (English) |
| `cases/<id>/` | The applicant's case, created with `make new` |
| `tools/kit.py` | Build and check engine; `tools/` modules are its helpers |
| `templates/` | Typst theme and draft banner |
| `tests/` | Engine and template tests |

Inside a case: `workproduct/` and `data/` are tracked; `evidence/`,
`source_documents/`, `private/`, and `output/` are ignored by Git.

## Guardrails

1. **Never invent facts.** Every factual claim in a draft cites its record: an
   exhibit (`[Exhibit D-1]`), a `source_documents/` path, or a dated note in
   `07_Factual_Verification_Questionnaire.md`. Metrics carry their snapshot
   date. When a fact is missing, ask the applicant; leave the `{{PLACEHOLDER}}`.
2. **Privacy.** Tracked files hold dates, categories, and receipt numbers only.
   A-numbers, SEVIS IDs, passport/visa/I-94 numbers, birth date, addresses, and
   salary stay in the ignored `private/` and `source_documents/`. Do not upload
   identity or immigration documents to third-party services.
3. **Primary sources for law, forms, and fees**: eCFR, the USCIS Policy Manual,
   USCIS form pages, AAO precedent decisions, the visa bulletin. Re-check
   time-sensitive items (fees, form editions, filing channel, upload limits)
   on the day they matter, and label secondary summaries as secondary.
4. **One endeavor, stated once.** The one-sentence proposed endeavor is locked
   in `case.json` (`locked_phrases`); `make check` fails if the petition,
   endeavor statement, or roadmap drift from it. Change it in all places at
   once, and never after filing (an RFE response may not change it).
5. **Frozen filed record.** After filing, run `make freeze LABEL=filed-<date>`
   and tag the commit. Do not edit the filed drafts or evidence; an RFE response
   goes in `cases/<id>/rfe-<notice-date>/` with new exhibit series.
6. **Automated access respects site protection.** If a site blocks automated
   clients (travel.state.gov often does), report it and stop.

## Conventions

- Templates: `{{UPPER_SNAKE}}` placeholders; drafting guidance in
  `<!-- GUIDE: ... -->` comments, which never reach the PDF.
- Exhibit citations: `[Exhibit B-1]`, `[Exhibits D-1, D-2]`, `[Exhibits D-1–D-3]`
  (en dash). Every registered exhibit must be cited at least once in a
  filing-facing document, and every citation must resolve.
- A Markdown horizontal rule (`---`) becomes a page break in the PDF.
- Filing-facing text is English; the playbook is Chinese.

## Commands

```bash
make bootstrap                 # once: Homebrew tools + Python env
make new ID=<id> NAME="<Full Name>"
make check CASE=cases/<id>     # draft gate
make final CASE=cases/<id>     # filing gate: no placeholders, no stubs
make review | binder | preview | online
make freeze LABEL=filed-YYYY-MM-DD
make test
```

## Done means

- `make test` passes and `make check` passes for the case.
- Before filing: `make final` passes, every page of `output/online/` has been
  looked at by a human, and the filed set is frozen.

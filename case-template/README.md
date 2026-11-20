# {{APPLICANT_FULL_NAME}} — EB-2 NIW Case

<!-- GUIDE: Keep this file current. It is the first thing you (or an agent) read when you come back to the case. -->

| Item | Value |
| --- | --- |
| Stage | {{STAGE}} <!-- drafting / evidence / review / filed / RFE / approved --> |
| Proposed endeavor | See `case.json` → `locked_phrases` |
| Target filing date | {{TARGET_FILING_DATE}} |
| Filed | {{FILING_DATE_AND_RECEIPT_NUMBER}} |
| Frozen record | `data/frozen_record.json`, Git tag {{TAG}} |

## Files

| Path | Role | Filed? |
| --- | --- | --- |
| `workproduct/01_Petition_Letter.md` | Legal and factual argument | Yes |
| `workproduct/02_Proposed_Endeavor_Statement.md` | Exhibit H-1, signed | Yes |
| `workproduct/03_Personal_Statement.md` | Exhibit H-2, signed | Yes |
| `workproduct/04_Officer_Roadmap.md` | One-page map to the record | Yes |
| `workproduct/05_Exhibit_List_and_Evidence_Map.md` | Exhibit index; tables generated from the registry | Yes |
| `workproduct/06`–`16` | Private controls: ledger, facts, evidence requests, forms, filing, review, RFE plan | No |
| `letters/` | Letter requests, fact sheets, skeletons, translator certification | No |
| `data/exhibit_registry.json` | Every exhibit: ID, title, payload path, source, date, what it supports | — |
| `data/package_manifest.json` | Which drafts are filing-facing and their packet order | — |
| `rfe-template/` | Copy to `rfe-<notice-date>/` if an RFE arrives | — |

## Open items

<!-- GUIDE: The short list of what blocks filing. Detail lives in 12_Final_Readiness_Matrix.md. -->

- {{OPEN_ITEM}}

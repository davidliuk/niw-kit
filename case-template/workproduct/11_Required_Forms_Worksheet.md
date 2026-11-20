# Required Forms Worksheet

**Applicant / Self-Petitioner:** {{APPLICANT_LEGAL_NAME}}\
**Prepared:** {{DATE}}\
**Purpose:** Private control. Do not file.

<!-- GUIDE: One row per form that leaves your hands. A form is final only when
its exact file sits at the final path, its SHA-256 is recorded here, and a
second person (or you, on a later day) has reviewed it. If a final file
changes after its hash is recorded, the review starts over. Keep official
blanks, review prefills, and editable working copies out of the final folder. -->

## 1. Form Sources (download on the filing date)

| Form | Official source | Edition / OMB expiration seen | Verified on | Blank SHA-256 |
| --- | --- | --- | --- | --- |
| I-140 + instructions | https://www.uscis.gov/i-140 | {{EDITION}} | {{DATE}} | {{SHA256}} |
| ETA-9089 Appendix A | DOL forms page (dol.gov/agencies/eta/foreign-labor/forms) | {{OMB_EXP}} | {{DATE}} | {{SHA256}} |
| ETA-9089 Final Determination | DOL forms page | {{OMB_EXP}} | {{DATE}} | {{SHA256}} |
| ETA-9089 main form (only if required on filing day) | DOL forms page / flag.dol.gov | {{OMB_EXP}} | {{DATE}} | {{SHA256}} |
| I-907 + instructions (optional) | https://www.uscis.gov/i-907 | {{EDITION}} | {{DATE}} | {{SHA256}} |
| G-1145 (paper only) | https://www.uscis.gov/g-1145 | {{EDITION}} | {{DATE}} | {{SHA256}} |
| G-1055 fee schedule (reference) | https://www.uscis.gov/g-1055 | {{EDITION}} | {{DATE}} | {{SHA256}} |

## 2. Final Payload Control

| Form | Final file path | Expected pages | Actual pages | Signature type | Signed by / date | Widget-free | Unencrypted | Letter size | Size (MB) | SHA-256 | Reviewer / date |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- | ---: | --- | --- |
| I-140 | `private/forms/final/Form_I-140_Signed_Scan.pdf` | {{N}} | | Handwritten ink, scanned | | [ ] | [ ] | [ ] | | | |
| ETA-9089 Appendix A | `private/forms/final/Form_ETA-9089_Appendix_A.pdf` | {{N}} | | None on form (adopted through Final Determination) | n/a | [ ] | [ ] | [ ] | | | |
| ETA-9089 Final Determination | `private/forms/final/Form_ETA-9089_Final_Determination_Signed.pdf` | {{N}} | | Handwritten ink, scanned (sections per decision) | | [ ] | [ ] | [ ] | | | |
| ETA-9089 main form (if required) | `private/forms/final/Form_ETA-9089.pdf` | {{N}} | | {{TYPE}} | | [ ] | [ ] | [ ] | | | |
| I-907 (optional) | `private/forms/final/Form_I-907_Signed_Scan.pdf` | {{N}} | | Handwritten ink, scanned | | [ ] | [ ] | [ ] | | | |
| G-1145 (paper only) | `private/forms/final/Form_G-1145.pdf` | {{N}} | | Not required | n/a | [ ] | [ ] | [ ] | | | |

<!-- GUIDE: Checks you can run locally (macOS / Linux):
  shasum -a 256 <file>                 # record the hash
  qpdf --check <file>                  # structure, encryption
  qpdf --show-npages <file>            # page count
  pdfinfo <file>                       # page size, encryption (poppler)
A widget is an interactive form field. A scan has none; a PDF exported from a
fillable form may still have them. Flatten (print to PDF or rasterize), then
re-open and confirm every filled value and signature is still visible. -->

## 3. Field Reconciliation (fill before signing)

| Field | I-140 | Appendix A | Final Determination | Petition / H-1 / H-3 | Source exhibit | Match |
| --- | --- | --- | --- | --- | --- | --- |
| Legal name | | | | | A-1 | [ ] |
| Mailing address | | | n/a | signature block | private map | [ ] |
| Qualifying degree, field, institution, date | Part 3 / 5 as applicable | Education section | n/a | | B-1, B-2 | [ ] |
| Current employer, title, start date | Part 5 | Experience section | n/a | | C-1 | [ ] |
| Intended occupation / SOC | Part 6 | (job info if asked) | n/a | Petition, H-1 | B-3 or O*NET exhibit | [ ] |
| Endeavor description | Part 6 + Part 11 | n/a | n/a | H-1 canonical sentence | H-1 | [ ] |
| Signature date | Signature part | n/a | Sections B / D | Signature blocks | | [ ] |

## 4. Final Determination Decision Log

| Question | Decision | Basis (source + date) | Decided by / date |
| --- | --- | --- | --- |
| Which sections does the self-petitioner sign? | {{DECISION}} | I-140 checklist wording | |
| Title entered in the petitioner section | {{DECISION}} | | |
| Government-use section left blank? | {{DECISION}} | Form labels | |
| Attorney / agent section | {{DECISION}} | | |
| Both signatures in ink on the same day, one scan | {{DECISION}} | | |
| Portal category for each ETA-9089 document | {{DECISION}} | Live upload screen | |

## 5. Finalization Steps (each form)

1. Download the filing-day edition; record its hash in §1.
2. Complete every applicable field from the fact record (`07_Factual_Verification_Questionnaire.md`).
3. Print, ink-sign, date (where a signature is required).
4. Scan the complete document in page order, upright, Letter size, readable.
5. Save to the final path; check pages, encryption, widgets, size.
6. Record SHA-256 and reviewer in §2.
7. Rebuild the upload set; confirm the manifest reports the same hash.
8. Store the ink-signed originals in a safe physical place: {{LOCATION}}.

# Form I-140 Online Filing Control

**Applicant / Self-Petitioner:** {{APPLICANT_LEGAL_NAME}}\
**Classification:** EB-2 advanced-degree professional requesting a National Interest Waiver\
**Method:** USCIS online account, completed-PDF upload\
**Planned filing date:** {{DATE}}\
**Purpose:** Private control. Do not file.

<!-- GUIDE: The live account controls. This worksheet tells you what to check,
in what order, and what to save. Portal wording, categories, and limits change
without notice; check each one on the live screen on filing day and record what
it shows. If official pages and the live account conflict, record the conflict
and resolve it before filing. -->

## 0. Submission Record (fill in after submitting)

| Field | Value |
| --- | --- |
| Submitted at (local time and time zone) | {{DATETIME_TZ}} |
| Portal confirmation text (verbatim) | {{TEXT}} |
| Receipt number | {{RECEIPT_NUMBER}} (record in private status file) |
| Receipt / priority date on I-797C | {{DATE}} |
| Concurrent forms accepted | {{I907_YES_NO}} |
| Fees paid (per Pay.gov confirmation) | {{AMOUNTS}} |
| Principal-form SHA-256 | {{SHA256}} |
| Upload manifest SHA-256 | {{SHA256}} |
| Filed-record tag / archive location | {{TAG_OR_PATH}} |

<!-- GUIDE: Priority date. The priority date is the date the petition is
properly filed (8 CFR 204.5(d); receipt rules in 8 CFR 103.2(a)(7)). USCIS
may date receipts on its own clock, which can differ from your local time zone,
and different screens may show different dates. Record the exact time you
pressed submit, then treat the mailed I-797C as controlling. A rejected filing gets no receipt date; watch
the account for a rejection notice. -->

## 1. Public-Page Check (filing day)

| Check | Source | Verified on | Result |
| --- | --- | --- | --- |
| I-140 listed under "Upload Completed PDF Online" | https://www.uscis.gov/file-online/forms-available-to-file-online | | |
| I-140 edition and "File Online" link | https://www.uscis.gov/i-140 | | |
| Self-petitioner filing tips (Part 1 fee questions) | https://www.uscis.gov/i-140 | | |
| Fee schedule edition and amounts | https://www.uscis.gov/g-1055 | | |
| I-907 eligibility, fee, concurrent-filing rule | https://www.uscis.gov/i-907 | | |
| NIW initial evidence (ETA-9089 documents) | I-140 initial-evidence checklist | | |
| Upload format and size rules | USCIS online filing tips / live upload screen | | |

**Stop rule:** if I-140 is no longer offered for PDF upload, the account lacks the NIW self-petition path, the fee differs from your G-1055 calculation, or the required documents changed, do not submit. Rebuild the controls first.

## 2. Account Workflow (check each step on the live account)

1. Sign in to your own USCIS online account (my.uscis.gov). Never use a preparer's account for a self-petition.
2. Start Form I-140 → choose the completed-PDF upload route → select the NIW self-petition path.
3. Answer the portal's screening questions consistently with the PDF.
4. Upload the principal form (ink-signed I-140 scan).
5. If offered and decided, attach the concurrent I-907 scan.
6. Upload ETA-9089 documents and evidence in the portal categories.
7. Review the summary; compare every file name and category against the manifest.
8. Complete the attestation (this does not replace the ink signature on the PDF).
9. Pay through the Pay.gov redirect.
10. Save the confirmation page, Pay.gov receipt, and case card.

## 3. Form I-140 Field Worksheet (NIW-critical parts)

<!-- GUIDE: Enter identifiers only in the form. This worksheet stores where
each value comes from, not the value itself, for anything private. -->

### Part 1: Petitioner

| Item | Entry | Source |
| --- | --- | --- |
| Name | {{LEGAL_NAME}} | Exhibit A-1 |
| Company / organization | Not applicable (individual) | |
| Mailing address | see private field map | Account profile, reconfirmed {{DATE}} |
| Nonprofit / government research question | Per USCIS self-petitioner tip ({{ANSWER}}) | uscis.gov/i-140, verified {{DATE}} |
| 25-or-fewer employees question | Per USCIS self-petitioner tip ({{ANSWER}}) | uscis.gov/i-140, verified {{DATE}} |

### Part 2: Petition Type

| Item | Entry |
| --- | --- |
| NIW (advanced degree or exceptional ability) | Yes; item number per current edition: {{ITEM}} |
| Basis relied on | Advanced degree |
| Amended petition / Schedule A | No (unless true) |

### Parts 3–4: Beneficiary and Processing

| Item | Entry | Source |
| --- | --- | --- |
| Identity, birth, citizenship, identifiers | see private field map | A-1, A-2, A-3 |
| Last arrival, I-94, status, authorized stay | see private field map | A-3 (pull the latest I-94 the week of filing) |
| Adjustment or consular processing | {{CHOICE}} (one only) | Strategy decision |
| Foreign address / native-script name | see private field map | |
| Prior petitions / proceedings | {{ANSWER}} | Records |

### Part 5: Self-Petitioner Information

| Item | Entry | Note |
| --- | --- | --- |
| Type of petitioner | Self | |
| Current occupation | {{CURRENT_OCCUPATION}} | Your present job; may differ from Part 6 |
| Annual income | from private salary record | Enter on the form only; do not upload salary documents |
| Employer-only items | Not applicable per form convention | |

### Part 6: Proposed Employment (consistency with the endeavor)

| Item | Entry | Consistency check |
| --- | --- | --- |
| 1 Job title | {{OCCUPATION_TITLE}} | Same occupation as Petition, H-1, B-3 evaluation / O*NET exhibit |
| 2 SOC code | {{SOC_CODE}} | Matches O*NET / BLS SOC title |
| 3 Nontechnical description | {{ENDEAVOR_SHORT_FORM}} "Full text: Part 11" | Full canonical endeavor sentence in Part 11 |
| 4 Full-time | {{YES_NO}} | Must match how H-1 describes your time |
| 5 Hours if part-time | {{HOURS_OR_BLANK}} | |
| 6 Permanent | {{YES_NO}} | Multi-year program, not temporary |
| 7 New position | {{YES_NO}} | Refers to an employer-created position |
| 8 Wage | {{WAGE_OR_BLANK}} | Do not copy current salary unless it is the Part 6 job |
| 9 Worksite | {{WORKSITE_OR_SAME_AS_PART1}} | Do not copy current employer site by reflex |

<!-- GUIDE: Part 6 notes.
- The NIW waives the job offer. Part 6 describes the endeavor's occupation,
  not necessarily your current job (8 CFR 204.5(k)(4)(ii); Policy Manual Vol. 6,
  Part F, Ch. 5). Do not invent an employer, wage, or worksite.
- Keep Part 5 (current occupation) and Part 6 (intended occupation) distinct
  and explain the difference in Part 11 so it is not read as inconsistency.
- The printed description box is small. Put a short form in the box and the
  full sentence in Part 11, keyed by page, part, and item.
- Any portal question that repeats Part 6 gets the same answers.
- These are decision points. Record your choice and reason; consider a limited
  attorney review. -->

Part 11 draft entries:

| Page / Part / Item | Text |
| --- | --- |
| {{PAGE}} / 6 / 3 | {{FULL_ENDEAVOR_SENTENCE}} |
| {{PAGE}} / 6 / 4–9 | {{EXPLANATION_PART5_VS_PART6_NO_JOB_OFFER}} |

### Parts 7–11

- [ ] Part 7: every spouse and child.
- [ ] Signature part: contact details; print, ink-sign, date, scan whole form.
- [ ] Interpreter / preparer parts: only if used.
- [ ] Part 11: every continuation keyed to page / part / item.

## 4. Upload Plan (check on the live upload screen)

| Constraint | Value on the live screen | Verified on filing day |
| --- | --- | --- |
| Accepted formats | {{RESULT}} | {{DATE}} |
| Max size per file | {{RESULT}} | {{DATE}} |
| Files per upload action | {{RESULT}} | {{DATE}} |
| Encrypted PDFs accepted? | {{RESULT}} | {{DATE}} |

The kit builds each file under 11.5 MB by default (`upload_limit_bytes` in
`case.json`). If the live screen shows a lower per-file limit, lower that value
and rebuild.

Portal categories (illustrative; use the labels the live portal shows):

| Portal category | What goes there | Files | Upload actions |
| --- | --- | ---: | ---: |
| Upload Form I-140 | Ink-signed I-140 scan | 1 | 1 |
| Upload Concurrent PDF(s) | Ink-signed I-907 scan (if used) | 1 | 1 |
| (I-140) Form ETA-9089 | Signed Final Determination (and main ETA-9089 if you decided it is required) | {{N}} | |
| (I-140) Form ETA Appendix A | Appendix A | 1 | 1 |
| (I-140) Evidence Supporting National Interest Waiver | Petition letter, index, D–J exhibits, H-1, H-2, H-3 | {{N}} | {{N}} |
| (I-140) An official academic record | B-series | {{N}} | {{N}} |
| (I-140) Additional Evidence | A-series, C-series | {{N}} | {{N}} |
| Proof of exceptional abilities / ETA-750 | Leave empty for the advanced-degree route | 0 | 0 |

Batch checklist (copy per category; batch size = files per upload action on the live screen):

| Batch | Files | Uploaded | Preview opened |
| --- | --- | --- | --- |
| 1 | {{FILE_1}} … {{FILE_N}} | [ ] | [ ] |

<!-- GUIDE: Upload notes.
- Upload separate, named exhibits; never the consolidated review binder.
- Build every file below the live per-file limit with margin. Split a large exhibit into
  "Part 1 / Part 2" rather than compressing it until it is unreadable.
- PDFs with interactive form fields (fillable certificates, signed
  translations made in a PDF editor) can lose visible content when flattened
  or stripped. Rasterize those pages, then look at them.
- File names: ASCII letters, digits, dot, dash, underscore, parentheses; start
  with the exhibit ID so the officer sees the order.
- Upload each translated exhibit as one PDF: original + translation +
  certification. -->

## 5. Payment

- [ ] Displayed total equals your computed total (`09_Forms_and_Assembly_Checklist.md` §6). If not, stop.
- [ ] Payment opens from the USCIS flow (Pay.gov redirect).
- [ ] Payment method on the live screen: {{METHOD}}.
- [ ] Funds, limits, issuer alerts checked.
- [ ] Save Pay.gov confirmation (private record; no card or bank numbers in evidence).

## 6. Filing-Day Checklist

- [ ] §1 public-page checks done and recorded.
- [ ] Account offers NIW self-petition PDF upload; concurrent forms as decided; no unintended I-485.
- [ ] I-140 scan: complete, upright, readable, unencrypted, Letter size, ink signature visible, hash matches `11_Required_Forms_Worksheet.md`.
- [ ] ETA-9089 documents: complete, signed as decided, hashes match.
- [ ] Narrative documents signed; translations signed; hashes match.
- [ ] Every address and identifier matches its source.
- [ ] Manifest and portal list agree file by file.
- [ ] Final summary saved before payment.
- [ ] Attestation completed; payment made.
- [ ] Confirmation, receipt number, Pay.gov receipt, exact uploaded files saved together.

## 7. Post-Filing Record

| Item | Saved at (private path) | Date |
| --- | --- | --- |
| Portal confirmation page (PDF / screenshot) | | |
| Pay.gov confirmation(s) | | |
| Case card showing forms filed | | |
| Premium-processing receipt e-mail (if any) | | |
| I-797C receipt notice(s) | | |
| Exact uploaded files + manifest + hashes | | |
| Filed-record tag (version control) | | |

- [ ] Add the receipt number and deadlines to the private status timeline.
- [ ] Watch the account for rejection, RFE, or biometrics notices.
- [ ] Keep the filed set immutable. Later evidence gets new exhibit IDs in a separate folder.
- [ ] Update the address with USCIS within the required time after any move (uscis.gov/ar-11).

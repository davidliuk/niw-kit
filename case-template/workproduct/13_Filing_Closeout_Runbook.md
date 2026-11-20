# Filing Closeout Runbook

**Applicant:** {{APPLICANT_LEGAL_NAME}}\
**Target filing date:** {{DATE}}\
**Method:** {{ONLINE_PDF_UPLOAD_OR_PAPER}}\
**Purpose:** Private execution control. Do not file.

<!-- GUIDE: Run these steps in order during the final one to two weeks. Each
step depends on the one before it. Any change to wording, metrics, or evidence
after step 4 voids the narrative signatures and the visual review: go back to
step 3. Plan for at least one full re-run. -->

## Step 1. Freeze Facts (T-14 to T-7 days)

- [ ] Reconfirm every changeable fact in `07_Factual_Verification_Questionnaire.md`: status, I-94, employment, addresses, family, publication outcomes, author lists.
- [ ] Apply a publication-status upgrade only with a title-bearing primary record; otherwise keep the conservative status.
- [ ] Refresh public metrics within about 7 days of filing. Save each source page as a dated PDF capture with URL and retrieval time; record the per-source snapshot date and SHA-256.
- [ ] Rebuild every exhibit that carries a refreshed number.
- [ ] Search filing documents for every repeated number and date; one value per source everywhere.
- [ ] Confirm the endeavor sentence in `case.json` `locked_phrases` is final.

Done when: no open `APPLICANT_CONFIRMED` fact carries a filing claim. Date: {{DATE}}

## Step 2. Final Letters and Third-Party Signatures (T-21 to T-7)

- [ ] Letters signed on letterhead, dated before the filing date, matching the fact record.
- [ ] Every letter states first-hand facts (what the writer saw, used, or did), not general praise.
- [ ] Set a letter cutoff date. The petition must stand without any letter that misses it.

Letter cutoff: {{DATE}}

## Step 3. Translations (T-21 to T-5)

- [ ] Freeze each preparation copy (record SHA-256) before sending it to the translator.
- [ ] Translator compares against the complete source, including seals and stamps, then signs and dates the certification.
- [ ] Signed packet is visibly signed and flat (no interactive signature field); record its SHA-256.
- [ ] If the source or preparation copy changes, the translator re-signs.

## Step 4. Final Unsigned Build and Narrative Freeze (T-5)

```bash
make check CASE=cases/{{CASE_ID}}
make preview CASE=cases/{{CASE_ID}}   # online set, drafts allowed until forms and signatures exist
```

- [ ] Read the petition letter, H-1, and H-2 PDFs from `output/online/` end to end.
- [ ] Record each exact unsigned PDF's SHA-256 (`shasum -a 256 <file>`).
- [ ] Do not edit after this point without returning to this step.

## Step 5. Narrative Signatures (T-4)

- [ ] Print each complete PDF, sign and date in ink, scan every page to the signed path in `private/`.
- [ ] Check: all pages, upright, readable, Letter size, signature and date visible.
- [ ] Record each signed scan's SHA-256 next to its unsigned-source hash (`09_Forms_and_Assembly_Checklist.md` §7).

## Step 6. Required Forms (T-4 to T-2)

- [ ] Download filing-day editions; record in `11_Required_Forms_Worksheet.md` §1.
- [ ] Complete I-140 (Part 6 consistent with the endeavor; Part 11 continuations), Appendix A, Final Determination, optional I-907.
- [ ] Reconcile every field (§3 of the worksheet).
- [ ] Ink-sign, date, scan complete forms; keep originals.
- [ ] Check pages, encryption, widgets, Letter size, file size; record SHA-256 and reviewer.

## Step 7. Rebuild and Fail-Closed Gate (T-2)

```bash
make final CASE=cases/{{CASE_ID}}
make online CASE=cases/{{CASE_ID}}
```

- [ ] `make final` passes: no placeholders, no stubs, every citation resolves, every exhibit cited.
- [ ] Manifest includes the signed narratives, signed translations, and required forms by their recorded hashes.
- [ ] No file over the upload limit; no encryption; widget pages flattened.
- [ ] No salary letter, private reports, review binder, or drafts in the upload set.

A failed hash, page count, size, or gate is a stop. Fix the source; never bypass the check.

## Step 8. Whole-Package Visual QA (T-2 to T-1)

- [ ] Look at every page of `output/online/` in upload order (contact sheets are fine).
- [ ] Check: no blank, cropped, rotated, blurred, duplicated, mislabeled, or misordered page; every signature, date, seal, and translation certification visible; flattened pages still show their filled values.
- [ ] Record reviewer and date: {{REVIEWER}} / {{DATE}}.

## Step 9. Filing Day

- [ ] Re-verify the live items in `09_Forms_and_Assembly_Checklist.md` §11 (edition, online path, fees, I-907, ETA-9089 requirement, upload limits, payment route).
- [ ] Pull the latest I-94; confirm status and addresses once more.
- [ ] Follow `10_Online_I140_Filing_Control.md` §2–§6.
- [ ] Compare portal upload list to manifest file by file; open representative previews (each form, signed narratives, translated exhibits).
- [ ] Save the final summary before paying.
- [ ] Attest; pay through the Pay.gov redirect.
- [ ] Note the exact submit time and time zone.

If anything on the live portal differs materially from the controlled package: stop, reconcile, and file another day.

## Step 10. After Filing (same day and first weeks)

- [ ] Save together, privately: confirmation page, Pay.gov receipts, case card, premium-processing e-mail, exact uploaded files, manifest, hash list.
- [ ] Freeze the filed record:

```bash
make freeze CASE=cases/{{CASE_ID}} LABEL=filed-{{YYYY_MM_DD}}
git tag {{TAG_NAME}}
```

- [ ] Add receipt number, receipt date, and premium-processing deadline to the private status timeline.
- [ ] Save the I-797C notice(s) when they arrive; confirm classification, receipt date, and fees accepted.
- [ ] Watch the account for rejection, RFE, or other notices.
- [ ] Keep the ink-signed originals.
- [ ] Do not edit filed drafts or evidence. Post-filing evidence goes into a separate RFE folder with new exhibit series.
- [ ] Maintain nonimmigrant status and employment authorization independently of the I-140.

| Item | Path / location | Date |
| --- | --- | --- |
| Filed record tag | {{TAG_NAME}} | |
| Hash list | {{PATH}} | |
| Ink-signed originals | {{LOCATION}} | |
| I-797C | {{PATH}} | |

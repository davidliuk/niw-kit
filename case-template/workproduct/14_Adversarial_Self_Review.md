# Adversarial Self-Review (Officer-Style Checklist)

Petitioner: {{PETITIONER_NAME}}
Review round: {{REVIEW_ROUND_NUMBER}} — {{REVIEW_DATE}}
Reviewer: {{REVIEWER_NAME_OR_ROLE}} (self / collaborator / AI agent / attorney)
Documents reviewed (with version or commit): {{DOCUMENT_VERSIONS}}
Purpose: private quality control; never file this document.

<!-- GUIDE: Read the record the way an officer drafting an RFE would. The goal
is not to confirm the petition is good; it is to find every sentence an
officer could write against it. Answer each question Y, N, or P (partial).
Score P as N when you decide what to fix. A "Y" counts only when you can fill
the "Evidence that proves it" column with an exhibit ID and page. If the
evidence column would say "the petition says so" or "the applicant's
statement", the answer is N. -->

<!-- GUIDE: Re-run this checklist after every substantive edit round and once
more on the frozen filing build. Record each run in the review round log
(playbook/07_review_method.md). Before using it, re-read the current USCIS
Policy Manual, Vol. 6, Part F, Ch. 5 and Matter of Dhanasar, 26 I&N Dec. 884
(AAO 2016); the questions below paraphrase those sources and do not replace
them. -->

## Severity Scale

| Rating | Meaning |
| --- | --- |
| BLOCKER | Do not file until fixed (missing required document, factual error, inconsistency with a form). |
| HIGH | Likely RFE or denial ground if unchanged. Every item marked **[Core]** below defaults to HIGH. |
| MEDIUM | Real weakness; fix it or accept it consciously and record why. |
| LOW | Clarity, navigation, or presentation. |

<!-- GUIDE: Calibration warning. Treat an internal label such as "supported
but adjudicator-sensitive", "credible", or "complete with adjudicator risk"
as "expect this element to be contested". Do not let a softened label stand
in for a HIGH rating. -->

## How to Read the Tables

- **#**: stable item ID; cite it in the review log.
- **Test question**: answer from the record, not from memory.
- **Y/N/P**: your answer.
- **Evidence that proves it**: exhibit ID + page (e.g., `E-1 p. 3`), or "none".
- **Sev. if N**: the default severity when the answer is N or P. Raise it if
  the gap is central to your theory.
- **[Core]**: the question tracks a requirement in Matter of Dhanasar or the
  Policy Manual (Vol. 6, Pt. F, Ch. 5, Sec. D) that officers test directly.
  Treat these as the officer's checklist.

---

## 1. Threshold: EB-2 Classification

| # | Test question | Y/N/P | Evidence that proves it | Sev. if N |
| --- | --- | --- | --- | --- |
| T-1 | Does an official record show the advanced degree was **awarded** (not just completed) before the filing date? | | B-1, B-2 | BLOCKER |
| T-2 | If relying on a bachelor's plus five years of progressive experience, do employer letters document each period, duties, and progression? | | B-1, C-1, C-2 | BLOCKER |
| T-3 | Is a foreign degree supported by a credential evaluation and certified translations? | | B-3 | BLOCKER |
| T-4 | Does the record show the intended occupation is a profession requiring that degree (e.g., an official occupational source)? | | B-3 | HIGH |
| T-5 | If exceptional ability is also claimed, does the record meet at least three of the 8 CFR 204.5(k)(3)(ii) criteria with documents, not assertions? If not claimed, does the petition say so plainly? | | | MEDIUM |
| T-6 | Are status documents current and consistent with the form answers (names, dates, classification)? | | A-1–A-3 | BLOCKER |

## 2. Prong 1: Substantial Merit (and Endeavor Definition)

| # | Test question | Y/N/P | Evidence that proves it | Sev. if N |
| --- | --- | --- | --- | --- |
| M-1 | Is the proposed endeavor one specific undertaking, more specific than an occupation or a field ("AI research", "software engineering")? | | H-1 | HIGH |
| M-2 | Does the endeavor statement name the problem, the method, the outputs, the beneficiaries, and how progress will be measured? | | H-1 | HIGH |
| M-3 | Is the identical endeavor sentence used in the petition, H-1, H-2, the form, and any letter that describes it? | | H-1, H-2, form | HIGH |
| M-4 | Are side activities (employment, other projects) framed as channels or validation settings of the one endeavor, not as separate endeavors? | | H-1 | MEDIUM |
| M-5 | Is merit shown by the endeavor's own technical value (results, method), with government or industry sources only as context? | | D-1, G-1 | MEDIUM |
| M-6 | Could the endeavor survive an RFE without being changed? (An RFE response may clarify but not materially change it; Matter of Izummi, 22 I&N Dec. 169 (Assoc. Comm'r 1998).) | | H-1 | HIGH |

## 3. Prong 1: National Importance

<!-- GUIDE: The officer's question is the "potential prospective impact" of
this specific endeavor (Dhanasar, 26 I&N Dec. at 889), not the importance of
the field. For technology endeavors the Policy Manual (Vol. 6, Pt. F, Ch. 5,
Sec. D) points to interest in adoption or licensing and to impact on others'
development of similar technology. -->

| # | Test question | Y/N/P | Evidence that proves it | Sev. if N |
| --- | --- | --- | --- | --- |
| N-1 | **[Core]** Does the record distinguish the applicant's work from ongoing research in the field: what existed before, what this work does differently, and who followed or measured against it? | | D-1, D-2, E-2 | HIGH |
| N-2 | **[Core]** Is there objective evidence that specific, named stakeholders (labs, departments, companies, developers, maintainers, agencies) adopted, implemented, integrated, or otherwise used the work? | | E-1–E-3, I-3 | HIGH |
| N-3 | **[Core]** Does that use evidence appear **in the brief body** (a table: who, institution, what they did, page cite), not only inside an exhibit? | | Petition § {{SECTION}} | HIGH |
| N-4 | **[Core]** Does the argument rest on this endeavor's mechanism of impact, rather than on evidence that the field (e.g., AI, clean energy, healthcare) is important? | | | HIGH |
| N-5 | **[Core]** Does the record explain how the endeavor will be implemented, disseminated, and used: channels, audiences, licenses, timeline? | | H-1, E-1 | HIGH |
| N-6 | **[Core]** Is impact shown to reach beyond the applicant's employer and clients? ("Benefits to a specific employer alone, even an employer with a national footprint, are not sufficiently relevant"; Policy Manual Vol. 6, Pt. F, Ch. 5.) | | E-1–E-3 | HIGH |
| N-7 | If the applicant is a full-time employee, does the record show who owns the outputs and that publishing them is consistent with the employment agreement and IP policy? | | C-1, applicant confirmation | HIGH |
| N-8 | **[Core]** Is every item in the officer's typical list answered (nationally significant problem, improved practice or technology, policy or standards, economic benefit, jobs, health or safety, security, infrastructure), either with evidence or with an explicit "not relied on"? | | | MEDIUM |
| N-9 | If the endeavor has several components, is third-party use mapped to each component, with candid weight (established / research-stage / prospective)? | | E-1, H-1 | HIGH |
| N-10 | Are government policy documents used only as context, each tied in one sentence to a specific output, with no claim of endorsement? | | G-1, G-2 | MEDIUM |
| N-11 | Does the record avoid claiming "first", "only", or "widely adopted" unless a source states it? | | | HIGH |
| N-12 | Are platform counters (stars, forks, downloads, views) labeled as attention, never as users or deployment? | | E-1 | MEDIUM |
| N-13 | Is there an independent third-party characterization of the work's place in the field (a survey, review article, benchmark paper, standards document) quoted with page cite? | | D-3, E-2 | MEDIUM |

## 4. Prong 2: Well Positioned to Advance the Endeavor

| # | Test question | Y/N/P | Evidence that proves it | Sev. if N |
| --- | --- | --- | --- | --- |
| W-1 | **[Core]** Is there a concrete plan: dated milestones (quarterly for year one), deliverables, measurable targets, and public channels? | | H-1 | HIGH |
| W-2 | **[Core]** Is there evidence of ongoing collaborations (a collaborator's letter, joint outputs dated after filing preparation, shared repositories)? | | I-2, D-1 | HIGH |
| W-3 | **[Core]** Is there evidence of funding, resources, or institutional support, or a documented cost basis showing who pays for what (redacted invoices, compute credits, lab access)? | | I-2, H-1 | HIGH |
| W-4 | **[Core]** Are citations, publications, and peer review tied to concrete progress or stakeholder interest (which citing works used the method versus merely cited it)? | | D-2, D-4, E-2 | HIGH |
| W-5 | **[Core]** Is there evidence of interest from relevant parties (invitations, inquiries, letters from users, requests for collaboration) that the applicant did not initiate? | | I-3, E-3 | HIGH |
| W-6 | Is the applicant's individual role in each team output documented by something other than the applicant's own statement (author contribution notes, commit history, collaborator letter)? | | D-1, E-1, I-2 | HIGH |
| W-7 | If the applicant works full time, does the plan explain how the endeavor proceeds alongside the job (cadence, resources, no reliance on employer time or confidential systems)? | | H-1 | HIGH |
| W-8 | Does the plan avoid depending on an unconfirmed job, grant, appointment, or institution? | | H-1 | HIGH |
| W-9 | Are citation comparisons, if any, field-matched and methodologically explained (source, date, scope)? If not, are percentiles left out? | | D-2 | MEDIUM |
| W-10 | Are self-nominated or reciprocal review roles described as such (never as "invited")? | | F-1 | HIGH |
| W-11 | Is education presented as one supporting factor, stated exactly (degree level, field), never as the main showing? | | B-1 | LOW |

## 5. Prong 3: On Balance, Beneficial to Waive the Job Offer and Labor Certification

| # | Test question | Y/N/P | Evidence that proves it | Sev. if N |
| --- | --- | --- | --- | --- |
| BAL-1 | **[Core]** Does Prong 3 explain why labor certification is impractical **for this specific endeavor**, using this record's facts, rather than in general? | | Petition § {{SECTION}} | HIGH |
| BAL-2 | **[Core]** Does it show the U.S. benefits from the applicant's contributions even if qualified U.S. workers are available, with evidence (not just the sentence)? | | E-1–E-3 | HIGH |
| BAL-3 | **[Core]** Does it address each factor the officer may list: restriction on the work, skills that cannot be articulated in a labor certification, urgency, impracticality of a job offer, job creation, self-employment? For each: evidence, or an explicit "not relied on". | | | HIGH |
| BAL-4 | Does it avoid arguing a labor shortage, irreplaceability, career convenience, or the wish to change employers? | | | HIGH |
| BAL-5 | If urgency is claimed, is it shown by dated evidence of the field's pace and of uptake of this work, not asserted? | | E-2, G-2 | MEDIUM |
| BAL-6 | Does Prong 3 stand on its own instead of restating Prongs 1 and 2? | | | MEDIUM |
| BAL-7 | If the STEM-degree factor is used, is the degree stated exactly and tied to the endeavor, with the field shown on a current official critical-technology list? | | B-1, G-2 | LOW |

## 6. Evidence Quality

| # | Test question | Y/N/P | Evidence that proves it | Sev. if N |
| --- | --- | --- | --- | --- |
| Q-1 | Does every factual sentence in the petition cite an exhibit and page? ("Going on record without supporting documentary evidence" is insufficient; Matter of Soffici, 22 I&N Dec. 158 (Assoc. Comm'r 1998).) | | claim ledger | HIGH |
| Q-2 | Does each exhibit open with what it proves (one cover page), before any methodology or reconciliation detail? | | | HIGH |
| Q-3 | Is the strongest evidence on the first page an officer reads for each prong (petition opening, exhibit covers, roadmap)? | | | HIGH |
| Q-4 | Are qualifications and limits stated once, briefly, instead of repeated so often that they bury the claim? | | | MEDIUM |
| Q-5 | Does every metric carry its snapshot date and source, and is the filing-date snapshot preserved separately from later updates? (Eligibility is assessed at filing; Matter of Katigbak, 14 I&N Dec. 45 (Reg'l Comm'r 1971).) | | data/ snapshots | HIGH |
| Q-6 | Are publication statuses (preprint, accepted, published) stated exactly as the primary record shows on the filing date? | | D-1 | HIGH |
| Q-7 | Are self-citations and coauthor citations identified and excluded from any "independent" claim? | | D-2 | HIGH |
| Q-8 | Are foreign-language documents accompanied by complete certified translations? | | | BLOCKER |
| Q-9 | Is internal audit vocabulary ("source-valid", "raw union", "freshness layer") kept out of officer-facing text? | | | LOW |

## 7. Letters

| # | Test question | Y/N/P | Evidence that proves it | Sev. if N |
| --- | --- | --- | --- | --- |
| L-1 | **[Core]** Does each letter state first-hand facts (what the writer saw, used, or did with the work) rather than the importance of the field or conclusory praise? | | I-1–I-3 | HIGH |
| L-2 | Does the record include at least one letter from someone with no prior relationship who used or evaluated the work (I-1 or I-3)? | | I-1, I-3 | HIGH |
| L-3 | Does each letter disclose the writer's relationship to the applicant and the basis of knowledge? | | | HIGH |
| L-4 | Is each letter paired with an independent record (the writer's paper, repository, issue thread) that corroborates its facts? | | | HIGH |
| L-5 | Does a collaborator letter (I-2) state the applicant's individual role and the continuing collaboration and resources? | | I-2 | HIGH |
| L-6 | Does every letter use the same endeavor wording and avoid legal conclusions ("meets the NIW standard")? | | | MEDIUM |
| L-7 | Are template-sounding letters avoided (no shared phrasing across writers)? | | | MEDIUM |

## 8. Consistency Across Documents and Forms

| # | Test question | Y/N/P | Evidence that proves it | Sev. if N |
| --- | --- | --- | --- | --- |
| CON-1 | Do names (including any professional or alternate name), dates, titles, and employers match across the form, CV, statements, letters, and exhibits? | | A-1, H-3 | BLOCKER |
| CON-2 | Does each number appear with the same value and date everywhere it is used (one source of truth)? | | data/ | HIGH |
| CON-3 | Does the job title and occupation on the form match the degree-based profession argued in the petition? | | form, B-3 | BLOCKER |
| CON-4 | Is there exactly one "final" version of each document, with every superseded variant removed from the upload set? | | upload manifest | BLOCKER |
| CON-5 | Do exhibit IDs cited in the petition resolve to the exhibit list and the uploaded files, with correct page numbers? | | exhibit index | HIGH |
| CON-6 | Do signatures and dates belong to the exact final version that is uploaded? | | | BLOCKER |
| CON-7 | Are fees, form edition, filing address or online path re-checked on uscis.gov on the filing date? | | | BLOCKER |

---

## 9. The Officer's Paragraph Test

<!-- GUIDE: For each element, write the one paragraph an officer would put in
an RFE or denial if they read the record unsympathetically. Use the
officer's vocabulary. If you can write a convincing paragraph, the element
is not yet proven. Then write the single sentence + exhibit that refutes it.
If you cannot refute it with an exhibit, the fix is new evidence, not new
wording. -->

| Element | Officer's adverse paragraph (draft it) | Refutation: sentence + exhibit + page | Fix type (evidence / wording / none) |
| --- | --- | --- | --- |
| National importance | {{ADVERSE_PARAGRAPH_NI}} | {{REFUTATION_NI}} | |
| Well positioned | {{ADVERSE_PARAGRAPH_P2}} | {{REFUTATION_P2}} | |
| Balance | {{ADVERSE_PARAGRAPH_P3}} | {{REFUTATION_P3}} | |

## 10. Round Summary

| Element | Items N or P | Highest severity | Fix type | Owner | Due |
| --- | --- | --- | --- | --- | --- |
| Threshold | | | | | |
| Substantial merit | | | | | |
| National importance | | | | | |
| Well positioned | | | | | |
| Balance | | | | | |
| Evidence quality | | | | | |
| Letters | | | | | |
| Consistency | | | | | |

**Decision:** {{FILE_NOW / FIX_THEN_RERUN / COLLECT_EVIDENCE_FIRST}}

<!-- GUIDE: If any [Core] item is still N and the fix type is "evidence",
writing more text will not close it. Decide whether to collect the evidence
before filing or to file and accept a likely RFE. Record which, and why. -->

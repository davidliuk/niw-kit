# Factual Verification Questionnaire and Canonical Fact Record

**Applicant:** {{APPLICANT_LEGAL_NAME}}\
**Prepared:** {{DATE}}\
**Last verified:** {{DATE}}\
**Purpose:** Private control. Do not file.

<!-- GUIDE: This file is the single source of truth for every fact that appears
in the petition letter, H-1, H-2, H-3, the exhibit index, and the forms. Draft
nothing until the fact exists here with a source. When two documents disagree,
fix the fact here first, then propagate it everywhere. Before signing anything,
re-read every row whose value can change (address, employment, metrics,
publication status). -->

<!-- GUIDE: Privacy. Do not type A-number, SEVIS ID, passport, visa, I-94, or
EAD card numbers, date of birth, SSN, salary, or bank details into this file.
Write "see private field map" and keep those values in an ignored file under
private/ (for example private/forms/field_map.json). This file may be shared
with a reviewer; the field map may not. -->

## Status Codes

| Code | Meaning |
| --- | --- |
| `VERIFIED_DOC` | Confirmed from a document in `source_documents/` |
| `VERIFIED_PUBLIC` | Confirmed from a public source on the stated date; capture preserved |
| `APPLICANT_CONFIRMED` | Stated by the applicant; no document yet. Cannot carry a core claim |
| `TO_COLLECT` | Document must be obtained before filing |
| `OPTIONAL_RFE` | Useful later; not planned for the initial filing |
| `EXCLUDED` | Internal only; never cite or upload |

Each row records: **value**, **source** (exhibit ID or `source_documents/` path), **status**, **verified on**, and **discrepancy notes**.

## 1. Identity and Immigration Status

| Fact | Value | Source | Status | Verified on | Discrepancy notes |
| --- | --- | --- | --- | --- | --- |
| Legal name (family / given / middle) | {{LEGAL_NAME}} | Exhibit A-1 | | | <!-- GUIDE: Must match passport exactly, including middle-name handling. --> |
| Other / preferred professional name | {{PREFERRED_NAME_OR_NONE}} | Public profiles | | | <!-- GUIDE: If public records use another name, state the linkage once in H-2 and decide how the form's "other names used" item treats it. --> |
| Country of citizenship / birth | {{COUNTRY}} | Exhibit A-1 | | | |
| Current nonimmigrant status | {{STATUS_CLASS}} | Exhibit A-2 | | | |
| Status validity window | {{STATUS_START}} to {{STATUS_END}} | Exhibit A-2 | | | |
| Last admission date and class | {{LAST_ADMISSION}} | Exhibit A-3 | | | |
| Authorized stay until | {{I94_ADMIT_UNTIL}} | Exhibit A-3 | | | |
| Mailing address | see private field map | Applicant | | | <!-- GUIDE: Reconfirm on filing day; must equal the online-account profile and Form I-140 Parts 1 and 3. --> |
| Physical address (if different) | see private field map | Applicant | | | |
| Foreign address / last permanent residence abroad | see private field map | Applicant | | | <!-- GUIDE: Form I-140 asks for it, sometimes in native script. --> |
| Email / telephone | see private field map | Applicant | | | |
| Prior immigrant petitions, removal proceedings, prior labor certification | {{YES_NO_DETAILS}} | Applicant + records | | | <!-- GUIDE: Answer from records, never from memory or the binder. --> |
| Spouse and children (all, even if not immigrating) | see private field map | Civil documents | | | |
| Intended processing: adjustment of status or consular | {{AOS_OR_CONSULAR}} | Strategy decision | | | <!-- GUIDE: Choose one; it drives Form I-140 Part 4. --> |

## 2. Education (EB-2 Threshold)

<!-- GUIDE: The advanced-degree threshold (8 CFR 204.5(k)(2), (k)(3)(i)) is
proved by a U.S. master's or higher, a foreign equivalent, or a bachelor's plus
five years of progressive post-degree experience. Use the official wording from
the diploma and transcript, not the CV. A foreign degree needs a credential
evaluation (B-3) and certified translation. -->

| Fact | Value | Source | Status | Verified on | Discrepancy notes |
| --- | --- | --- | --- | --- | --- |
| Qualifying degree title (exact) | {{DEGREE_TITLE}} | Exhibit B-1 | | | |
| Major / field (exact) | {{MAJOR}} | Exhibit B-2 | | | |
| Institution and country | {{INSTITUTION}}, {{COUNTRY}} | Exhibit B-1 | | | |
| Conferral date (not "graduation") | {{CONFERRAL_DATE}} | Exhibit B-1 / B-2 | | | |
| Foreign-degree equivalency | {{EQUIVALENCY_OR_NA}} | Exhibit B-3 | | | |
| Prior degree(s) | {{PRIOR_DEGREE}} | {{EXHIBIT_ID}} | | | <!-- GUIDE: Needed for ETA-9089 Appendix A education entries. --> |
| GPA / rank claims | {{ONLY_IF_OFFICIALLY_CERTIFIED}} | {{EXHIBIT_ID}} | | | <!-- GUIDE: Quote the certified figure and its as-of date. Never convert a rank into "top X%" unless the school states it. --> |
| Post-degree experience (if bachelor's + 5 route) | {{EMPLOYER_DATES_SUMMARY}} | Exhibit C-series | | | |

## 3. Employment

| Fact | Value | Source | Status | Verified on | Discrepancy notes |
| --- | --- | --- | --- | --- | --- |
| Current employer legal name | {{EMPLOYER_LEGAL_NAME}} | Exhibit C-1 | | | |
| Exact title (as HR states it) | {{EXACT_TITLE}} | Exhibit C-1 | | | |
| Start date / full-time status | {{START_DATE}} / {{FT_PT}} | Exhibit C-1 | | | |
| Work location | {{WORK_LOCATION}} | Exhibit C-1 | | | |
| Duties (factual, non-confidential) | {{DUTIES_SUMMARY}} | C-1 or H-2 | | | <!-- GUIDE: If only the applicant describes the duties, label them applicant-described. --> |
| Prior positions | {{PRIOR_POSITIONS}} | Exhibit C-2 | | | |
| Outside-activity / IP policy permits the independent work | {{CONFIRMED_YES_NO}} | Employee handbook / agreement | | | <!-- GUIDE: Confirm privately before claiming independent research or open-source work done while employed. Do not file the policy. --> |

<!-- GUIDE: Employer-impact rule. A revenue, latency, or reliability figure
that no manager letter or record can verify stays out of the filing. Describe
the work qualitatively. Never disclose confidential architecture, internal
project names, or internal metrics. A salary-bearing verification letter is not
an exhibit; request a no-salary version for C-1. -->

## 4. Proposed Endeavor

| Item | Value | Source | Status | Notes |
| --- | --- | --- | --- | --- |
| Canonical endeavor sentence | {{ENDEAVOR_SENTENCE}} | H-1 | | <!-- GUIDE: One sentence: what you will build, for whom, how it is disseminated, where in the U.S. it is validated. Petition, H-1, H-2, H-3 and Form I-140 Part 6 must all use it. Lock it in case.json `locked_phrases` so `make check` catches drift. --> |
| Short form for the I-140 Part 6 box | {{ENDEAVOR_SHORT_FORM}} | Form I-140 | | <!-- GUIDE: The printed box holds only a few lines. Use a short form that points to Part 11, and put the full sentence in Part 11. --> |
| Intended occupation and SOC code | {{OCCUPATION_TITLE}} / {{SOC_CODE}} | O*NET / BLS SOC | | <!-- GUIDE: The intended occupation (Part 6) can differ from current occupation (Part 5). Explain the difference in Part 11. --> |
| Delivery channels | {{CHANNELS}} | H-1 | | |
| Milestones (Year 1, Years 2-3, Years 4-5) | {{MILESTONES}} | H-1 | | |
| Resources, collaborators, funding | {{RESOURCES}} | H-1 + I-series / documents | | <!-- GUIDE: State only what a document or first-hand letter supports. Ongoing collaborations, funding, and institutional support are useful Prong Two evidence. --> |

## 5. Publications (one row per work)

| Title | Venue | Status (exact) | Status record | Author position / count | Contribution notation | Applicant's personal role | Exhibit | Verified on |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {{TITLE}} | {{VENUE}} | {{ACCEPTED_PUBLISHED_UNDER_REVIEW_PREPRINT}} | {{DECISION_NOTICE_OR_PROCEEDINGS_RECORD}} | {{N_OF_M}} | {{FOOTNOTE_TEXT_VERBATIM}} | {{WHAT_YOU_DESIGNED_BUILT_WROTE}} | D-1 | |

<!-- GUIDE: Status discipline. "Accepted" needs a title-bearing decision
record; "published" needs an official proceedings or journal record. A number-
only decision email needs a second record that links the number to the title.
Copy contribution footnotes verbatim ("core contribution" is not "equal
contribution"). Never infer acceptance from a coauthor message or a preprint. -->

## 6. Projects and Open-Source Work (one row per project)

| Project | Applicant role | Proof of role (commits, PRs, team page) | Public metrics | Snapshot date (per source) | Exhibit | Limitations |
| --- | --- | --- | --- | --- | --- | --- |
| {{PROJECT}} | {{ROLE}} | {{PROOF}} | {{METRIC_AND_VALUE}} | {{SNAPSHOT_DATE}} | E-1 | <!-- GUIDE: An open pull request is not merged; a fork or star is attention, not adoption. --> |

## 7. Claimed Impacts (one row per claim)

| Claim as it will appear | Metric / fact | Value | Scope (what is counted) | Snapshot date | Source / capture | Independent of applicant? | Exhibit | Limitation sentence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {{CLAIM}} | {{METRIC}} | {{VALUE}} | {{SCOPE}} | {{DATE}} | {{URL_OR_PATH}} | {{YES_NO_UNKNOWN}} | E-1 | {{LIMITATION}} |

<!-- GUIDE: Impact rules.
- Every metric carries its own snapshot date; do not force different sources
  onto one date.
- Counts from different platforms (Google Scholar, Semantic Scholar, GitHub)
  are not additive. Report each with its source.
- Separate "cites" from "uses". A citation shows awareness; adoption needs a
  record that a third party implemented, integrated, deployed, or built on the
  work. A record that shows only the importance of the field does not show
  the importance of the endeavor (Matter of Dhanasar, 26 I&N Dec. at 889).
- Note author overlap and self-citation for every citing or using record.
- Access-controlled data (repository traffic, internal dashboards) needs a
  dated capture plus an applicant certification of method, or it is omitted. -->

## 8. Peer Review and Service

| Venue | Role | Dates | Number of reviews | Record | Exhibit | Verified on |
| --- | --- | --- | --- | --- | --- | --- |
| {{VENUE}} | {{ROLE}} | {{DATES}} | {{COUNT}} | {{INVITATION_AND_ACKNOWLEDGMENT}} | F-1 | |

<!-- GUIDE: Do not file confidential review text. -->

## 9. Awards

| Award | Issuer | Level / selectivity record | Date | Translation needed | Exhibit | Verified on |
| --- | --- | --- | --- | --- | --- | --- |
| {{AWARD}} | {{ISSUER}} | {{OFFICIAL_CRITERIA_OR_NONE}} | {{DATE}} | {{YES_NO}} | J-1 | |

<!-- GUIDE: An award without official context (criteria, applicant pool,
issuer description) carries little weight. Do not stack award names. -->

## 10. Letters

| Writer | Relationship (independent / collaborator / user) | First-hand facts the letter confirms | Status | Exhibit |
| --- | --- | --- | --- | --- |
| {{WRITER}} | {{RELATIONSHIP}} | {{FACTS}} | {{REQUESTED_DRAFT_SIGNED}} | I-1 |

## 11. Open Questions for the Applicant

| # | Question | Blocks which document | Answer | Date answered |
| --- | --- | --- | --- | --- |
| 1 | {{QUESTION}} | {{DOC}} | | |

## 12. Sensitive Files Not Planned as Exhibits

| File (private path) | Why excluded | Release only if |
| --- | --- | --- |
| Salary-bearing employment letter | Compensation not needed | Officer requests income evidence |
| Offer letter | Adds irrelevant terms | Specific RFE need |
| Tax, payroll, bank records | Not probative of merits | Specific RFE need |
| Confidentiality / invention agreements | Not probative | Counsel advises |

## 13. Applicant Certification Before Signing

- [ ] Every first-person sentence is accurate today.
- [ ] Every public profile cited refers to me.
- [ ] Every date, title, and status matches its official record.
- [ ] No confidential employer information is disclosed.
- [ ] The endeavor reflects genuine present intent.
- [ ] Every row above marked `APPLICANT_CONFIRMED` that carries a filing claim has been upgraded or removed.

Signed / initialed: {{INITIALS}} Date: {{DATE}}

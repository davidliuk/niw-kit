# Exhibit {{M_ID}}: Use of {{WORK_NAME}} by Unaffiliated Groups

Answers the finding that the record lacks objective evidence that the
endeavor "{{QUOTED_ADOPTION_FINDING}}" [Notice p. {{PAGE}}], and
{{OTHER_FINDINGS_ANSWERED}} (Response Map rows {{MAP_ROWS}}).

<!-- GUIDE: Purpose. When a notice says no stakeholder uses the work, an
exhibit number alone is easy to overlook. Put this table, or its Part A, in
the brief's own text (outline Section I.A) and state whether the underlying
exhibit was filed with the petition but not named in the notice.

Policy hooks (verify the wording in 03_Policy_Sources.md before quoting):
Policy Manual Vol. 6, Pt. F, Ch. 5, Sec. D lists, for technology endeavors,
interest in adoption or licensing and impact on others' development of similar
technology (prong 1), and how the person's work is being used by others
(prong 2). -->

<!-- GUIDE: Verification. Check every row against the citing work's PDF and
record the page. Record the date you verified the filed exhibit (file name and
hash if you keep a manifest). Quotes are verbatim; mark paraphrases. -->

Verified against {{SOURCE_EXHIBIT_OR_FILES}} on {{VERIFICATION_DATE}}.

## Independence Check (Apply to Every Row Before It Enters the Table)

| Test | How to check | Fails if |
| --- | --- | --- |
| No shared authors | Compare the citing work's full author list with every author of the applicant's work (watch for same-name different people; confirm by affiliation) | Any person appears on both |
| Not the applicant's own lab, advisor, department, or employer | First-page affiliations and acknowledgments | Overlap that a reader would call affiliated |
| Real use, not a citation | Find the sentence that says what they did (ran, built on, reimplemented, compared) | Only a reference-list or related-work mention |
| New results, not copied numbers | Compare their reported numbers with the applicant's paper | Their "baseline" rows equal the applicant's published rows; then it is a quoted comparison, not a replication |
| Source verified | Full text read (not just an abstract or index) | Full text could not be accessed; list it as unverified and exclude it from counts |
| Date class | Posting or publication date vs. the priority date | Post-filing items mixed into the filing-date table |

<!-- GUIDE: Excluded items go in the exclusion log at the end with the reason.
Keeping the log protects credibility: an officer who finds one inflated row
will discount the rest. -->

## Part A. Uses in the Filed Record, Ordered by Depth of Use

<!-- GUIDE: Depth order: ran released code or data → built on output or
artifacts → reused a component → reimplemented → controlled comparison →
compared against → weaker forms (quoted numbers, surrogate baseline). Label
the weak rows as weak; never merge them into a stronger class. -->

| # | Citing work (ID) | Institutions (first page) | Exact use, with a short verbatim quote | Page cite | Endeavor component | Use class |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | {{CITING_WORK_TITLE}} ({{ARXIV_DOI_OR_VENUE}}) | {{INSTITUTIONS}} | {{EXACT_USE_AND_QUOTE}} | {{PAGE}} | {{COMPONENT}} | {{RAN_BUILT_ON_REIMPLEMENTED_COMPARED}} |

## Part B. By Stakeholder Group Named in the Notice

<!-- GUIDE: Use the notice's own list of stakeholder types (for example:
academic departments, research laboratories, industry labs, independent
developers, open-source maintainers). If a group has no row, say so rather
than stretch a row to fit. Affiliations show where authors work, not that the
institution endorsed or deployed the work: write "researchers at", not
"adopted by". -->

| Stakeholder group (notice p. {{PAGE}}) | Part A rows | Basis |
| --- | --- | --- |
| {{STAKEHOLDER_GROUP}} | {{ROWS}} | {{BASIS}} |
| {{GROUP_WITH_NO_ROWS}} | None | State the gap |

## Part C. By Endeavor Component (Candid Weight)

<!-- GUIDE: Map against the components in the filed endeavor statement.
Candor is persuasive: "established" for components with third-party use,
"research-stage" where use is early, "not yet shown; prospective" where there
is none, and point to the plan that addresses it. -->

| Endeavor component (filed statement) | Third-party use at filing | Rows |
| --- | --- | --- |
| {{COMPONENT}} | {{ESTABLISHED_RESEARCH_STAGE_OR_NOT_YET}} | {{ROWS}} |

## Part D. Independent Measurements (Optional)

<!-- GUIDE: Use only measurements the later group ran itself on settings not
copied from the applicant's paper. Report every loss alongside the gains.
Each later paper usually reports that its own method beats the applicant's;
say so. Being measured against shows influence, not lasting superiority. -->

| Citing work | Setting | Baseline → applicant's method | Their own run? | Page |
| --- | --- | --- | --- | --- |
| {{CITING_WORK}} | {{SETTING}} | {{RESULT}} | {{YES_NO}} | {{PAGE}} |

## Part E. Records Outside the Filed Exhibit (Separate Exhibits)

<!-- GUIDE: Keep these out of Part A. Records that existed at filing but were
not submitted go in the N-series with their original dates; post-filing uses
go in the L-series as continued progress. Each needs its own dated capture. -->

| Proposed exhibit | Citing work | Date | Existed at filing? | Exact use | Page |
| --- | --- | --- | --- | --- | --- |
| {{EXHIBIT_ID}} | {{CITING_WORK}} | {{DATE}} | {{YES_NO}} | {{USE}} | {{PAGE}} |

## Exclusion Log

| Citing work | Reason excluded |
| --- | --- |
| {{CITING_WORK}} | {{SHARED_AUTHOR_OR_CITES_DIFFERENT_WORK_OR_UNVERIFIED_OR_REFERENCE_ONLY}} |

## What Not to Say

- Not "adopted by {{INSTITUTION}}": researchers there used it in a paper.
- Not "N groups ran the code" unless every one of them ran the released code.
- Not "replicated" for rows that quote the applicant's numbers.
- Not "first" unless the record proves it.
- Not counts (citations, stars, downloads, forks) presented as users or
  deployment.

# RFE Response: Notice of {{NOTICE_DATE}}

Request for Evidence on the EB-2 NIW Form I-140, receipt {{RECEIPT_NUMBER}}.
The original notice is stored at `source_documents/{{NOTICE_FILE_PATH}}`
(ignored by Git; it carries identifiers and a mailing address).

<!-- GUIDE: Copy this folder to cases/<id>/rfe-<notice-date>/ on the day the
notice arrives. The filed record (workproduct/, evidence/, the filing tag)
stays frozen. This folder holds the response only. Method:
playbook/09_rfe_response.md. Legal standard: playbook/02_legal_standard.md. -->

## Folder Rules

1. The filed record is frozen. Do not edit filed drafts or exhibits; cite them
   by their filed IDs.
2. New evidence gets a new exhibit series (K onward). Never reuse or renumber a
   filed exhibit ID (A–J). Series are defined in `01_Response_Outline.md`.
3. The proposed endeavor is quoted unchanged from the filing (Matter of Izummi,
   22 I&N Dec. 169, 175 (Assoc. Comm'r 1998)).
4. Eligibility is measured at filing (8 CFR 103.2(b)(1), (b)(12); Matter of
   Katigbak, 14 I&N Dec. 45 (Reg'l Comm'r 1971)). Every post-filing record
   carries its date and is offered as corroboration or continued progress.
5. One complete response. A partial response is treated as a request for a
   decision on the record (8 CFR 103.2(b)(11)). Nothing can follow later.
6. Every factual sentence in the brief cites an exhibit and page.
7. Privacy: tracked files hold dates, categories, and receipt numbers only.

| File | Purpose |
| --- | --- |
| `01_Response_Outline.md` | Brief skeleton: each section names the finding it answers and its exhibits |
| `02_Response_Map.md` | Every finding and listed factor in the notice → answer → section → exhibits → status |
| `03_Policy_Sources.md` | Dated primary-source checklist; refresh before drafting legal text |
| `04_Letter_Outreach_Plan.md` | Letter targets, ask, deadline, cutoff, status |
| `05_Adoption_Table.md` | Third-party use table for the brief body |

## Deadline and Delivery

<!-- GUIDE: Use the due date printed on the notice. The response must be
RECEIVED by that date (8 CFR 103.2(a)(7)(i)), not mailed. The maximum RFE
period is 12 weeks and no extension may be granted (8 CFR 103.2(b)(8)(iv)).
For a notice served by mail, 8 CFR 103.8(b) adds 3 days; do not add them
yourself on top of the printed date. If two dates seem possible, use the
earlier. -->

| Item | Date / Value | Source |
| --- | --- | --- |
| Notice date | {{NOTICE_DATE}} | Notice p. 1 |
| Response must be received by | **{{RESPONSE_DUE_DATE}}** | Notice p. {{DUE_DATE_PAGE}} |
| Priority (filing) date stated in the notice | {{PRIORITY_DATE}} | Notice p. {{PRIORITY_DATE_PAGE}} |
| Processing type | {{REGULAR_OR_PREMIUM}} | Receipt notice |
| Response channel | {{ONLINE_OR_MAIL}} — checked {{CHANNEL_CHECK_DATE}} | See channel check below |
| Mailing address (if mailing) | Per notice coversheet; kept in `private/` | Notice p. {{ADDRESS_PAGE}} |

### Channel Check

<!-- GUIDE: Do this before assembling, and record what you saw. A case filed
online can usually be answered online or by mail, but answer once only. USCIS
has described the online RFE portal as a single submission with an upload
limit, with extra files sent through the "Unsolicited Evidence" tool at the
same time (USCIS stakeholder Q&A, 2023; guidance, not regulation). Upload
limits and file-size rules change: check the account and
https://www.uscis.gov/file-online/tips-for-filing-forms-online on the day. -->

- [ ] Logged into the USCIS online account on {{CHANNEL_CHECK_DATE}}; RFE
      response portal present: {{YES_NO}}; upload limit shown: {{UPLOAD_LIMIT}}.
- [ ] Notice instructions on response location and coversheet read:
      {{NOTICE_INSTRUCTIONS_SUMMARY}}.
- [ ] Channel chosen: {{ONLINE_OR_MAIL}}. Only this channel will be used.
- [ ] If mailing: notice and coversheet on top; trackable courier; ship by
      {{SHIP_BY_DATE}}.

## What the Notice Decides and Contests

| Element | Finding in the notice | Notice page |
| --- | --- | --- |
| EB-2 ({{ADVANCED_DEGREE_OR_EXCEPTIONAL_ABILITY}}) | {{ESTABLISHED_OR_NOT}} | {{PAGE}} |
| Prong 1, substantial merit | {{ESTABLISHED_OR_NOT}} | {{PAGE}} |
| Prong 1, national importance | {{ESTABLISHED_OR_NOT}} | {{PAGE}} |
| Prong 2, well positioned | {{ESTABLISHED_OR_NOT}} | {{PAGE}} |
| Prong 3, balance | {{ESTABLISHED_OR_NOT}} | {{PAGE}} |

<!-- GUIDE: Elements the notice establishes are confirmed in one sentence in
the brief and not reargued. Elements it contests are mapped finding by
finding in 02_Response_Map.md. -->

## Internal Milestones

<!-- GUIDE: Work backward from the due date. Mark holidays, signers' travel,
and term ends first. The letter cutoff is fixed: whatever is signed by then
goes in; the draft is never held for a late letter. -->

| Milestone | Target date | Status |
| --- | --- | --- |
| Finding table and response map complete | {{MAP_DONE_DATE}} | {{STATUS}} |
| Policy sources refreshed (`03`) | {{SOURCES_DATE}} | {{STATUS}} |
| Letter requests sent | {{OUTREACH_SENT_DATE}} | {{STATUS}} |
| Letter drafts returned | {{LETTER_DRAFTS_DATE}} | {{STATUS}} |
| **Letter cutoff** (signed PDFs in hand) | **{{LETTER_CUTOFF_DATE}}** | {{STATUS}} |
| New exhibits captured and registered | {{EXHIBITS_DONE_DATE}} | {{STATUS}} |
| Full draft complete | {{DRAFT_DONE_DATE}} | {{STATUS}} |
| Self-audit (pinpoints, quotes, dates, independence) | {{AUDIT_DATE}} | {{STATUS}} |
| Optional limited-scope attorney review | {{ATTORNEY_REVIEW_DATE}} | {{STATUS}} |
| Final package frozen | {{FINAL_DATE}} | {{STATUS}} |
| Submitted / shipped (confirmation saved) | {{SUBMIT_DATE}} | {{STATUS}} |

## Post-Filing Evidence Log

<!-- GUIDE: One row per new record. "As of" is the record's own date, not the
capture date. Classify each as "existed at filing" (new evidence of a
filing-date fact) or "post-filing" (continued progress). -->

| Proposed exhibit | Record | As of | Existed at filing? | Use in the response | Gate before use |
| --- | --- | --- | --- | --- | --- |
| {{EXHIBIT_ID}} | {{RECORD_DESCRIPTION}} | {{RECORD_DATE}} | {{YES_NO}} | {{USE}} | {{GATE}} |

## Open Items

- [ ] {{OPEN_ITEM}}

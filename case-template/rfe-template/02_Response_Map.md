# Response Map

Every finding and listed factor in the notice of {{NOTICE_DATE}}, in the
notice's order, with the one-sentence answer, the brief section in
`01_Response_Outline.md`, the exhibits, and status. A condensed version
(finding, answer, section, exhibits) is reproduced after the brief's
introduction.

Quotes checked against the original notice on {{QUOTE_CHECK_DATE}}. Page
numbers are the notice's own page footers.

<!-- GUIDE: Build this table before drafting anything else.
- One row per sentence that states a deficiency, and one row per item in any
  list of evidence types or factors the notice gives, even ones you will not
  rely on (answer "Not relied on" and say why in a few words).
- Quote exactly; paraphrase only where the notice is too long, and mark it.
- Type: GAP (missing evidence), STANDARD (a test that belongs to another
  element), OVERLOOKED (filed evidence the notice does not mention),
  DISCRETION (weighing concern).
- An answer is a drafting target until its exhibits are in hand. Status:
  READY, PENDING (evidence being collected), DRAFT, NOT RELIED ON.
- Elements the notice establishes get one row each, answered "Established;
  not reargued." -->

## Elements Established by the Notice

| Element | Notice page | Treatment |
| --- | --- | --- |
| {{ESTABLISHED_ELEMENT}} | {{PAGE}} | Established; not reargued |

## Prong 1: National Importance

| # | Finding (notice page) | Type | One-sentence answer | Section | Exhibits | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | "{{QUOTED_FINDING}}" (p. {{PAGE}}) | {{TYPE}} | {{ANSWER}} | {{SECTION}} | {{EXHIBITS}} | {{STATUS}} |
| 2 | "{{QUOTED_FINDING}}" (p. {{PAGE}}) | {{TYPE}} | {{ANSWER}} | {{SECTION}} | {{EXHIBITS}} | {{STATUS}} |
| 3 | Listed factor: "{{LISTED_FACTOR}}" (p. {{PAGE}}) | — | {{ANSWER_OR_NOT_RELIED_ON}} | {{SECTION}} | {{EXHIBITS}} | {{STATUS}} |

## Prong 2: Well Positioned

| # | Finding (notice page) | Type | One-sentence answer | Section | Exhibits | Status |
| --- | --- | --- | --- | --- | --- | --- |
| {{N}} | "{{QUOTED_FINDING}}" (p. {{PAGE}}) | {{TYPE}} | {{ANSWER}} | {{SECTION}} | {{EXHIBITS}} | {{STATUS}} |
| {{N}} | Listed evidence: "{{LISTED_EVIDENCE_TYPE}}" (p. {{PAGE}}) | — | {{ANSWER_OR_NOT_RELIED_ON}} | {{SECTION}} | {{EXHIBITS}} | {{STATUS}} |

## Prong 3: Balance

| # | Finding (notice page) | Type | One-sentence answer | Section | Exhibits | Status |
| --- | --- | --- | --- | --- | --- | --- |
| {{N}} | "{{QUOTED_FINDING}}" (p. {{PAGE}}) | {{TYPE}} | {{ANSWER}} | III | {{EXHIBITS}} | {{STATUS}} |
| {{N}} | Listed factor: "{{LISTED_FACTOR}}" (p. {{PAGE}}) | — | {{ANSWER_OR_NOT_RELIED_ON}} | III | {{EXHIBITS}} | {{STATUS}} |

## Statements That Apply to the Whole Record

<!-- GUIDE: Notices often include general statements such as "going on record
without supporting documentary evidence is not sufficient" or "unsubstantiated
claims are insufficient." Map each to the drafting rule that answers it
(every factual sentence cites an exhibit and page). -->

| # | Statement (notice page) | Answer | Section |
| --- | --- | --- | --- |
| {{N}} | "{{GENERAL_STATEMENT}}" (p. {{PAGE}}) | Every factual sentence cites an exhibit and page. | All |

## Coverage Check

- [ ] Every page of the notice was read for findings, including footnotes and
      evidence lists.
- [ ] Row count matches the number of distinct findings and listed factors:
      {{ROW_COUNT}}.
- [ ] Every section of `01_Response_Outline.md` answers at least one row, and
      every row points to a section.
- [ ] No row has status PENDING at the letter cutoff without a fallback answer.

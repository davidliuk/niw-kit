#let legal-accent = rgb("#243b53")
#let legal-muted = rgb("#52606d")
#let legal-rule = rgb("#9fb3c8")
#let legal-table-rule = rgb("#bcccdc")
#let legal-table-fill = rgb("#f0f4f8")

#set par(
  justify: true,
  leading: 0.55em,
  spacing: 0.72em,
  first-line-indent: 0pt,
)
#set heading(numbering: none)
#set list(indent: 1.25em, body-indent: 0.6em, spacing: 0.72em)
#set enum(indent: 1.25em, body-indent: 0.6em, spacing: 0.72em)
#show link: set text(fill: legal-accent)

#show heading.where(level: 1): it => block(
  width: 100%,
  above: 10pt,
  below: 12pt,
  breakable: false,
  sticky: true,
)[
  #align(center)[
    #text(
      size: 18pt,
      weight: "bold",
      tracking: 0.25pt,
      fill: legal-accent,
      hyphenate: false,
    )[#it.body]
  ]
]

#show heading.where(level: 2): it => block(
  width: 100%,
  above: 14pt,
  below: 7pt,
  breakable: false,
  sticky: true,
  stroke: (bottom: 0.75pt + legal-rule),
  inset: (bottom: 4pt),
)[
  #text(
    size: 14pt,
    weight: "bold",
    fill: legal-accent,
    hyphenate: false,
  )[#it.body]
]

#show heading.where(level: 3): it => block(
  above: 10pt,
  below: 7.5pt,
  breakable: false,
  sticky: true,
)[
  #text(
    size: 12.25pt,
    weight: "bold",
    fill: legal-accent,
    hyphenate: false,
  )[#it.body]
]

#show heading.where(level: 4): it => block(
  above: 8pt,
  below: 7pt,
  breakable: false,
  sticky: true,
)[
  #text(
    size: 11.75pt,
    weight: "bold",
    fill: legal-muted,
    hyphenate: false,
  )[#it.body]
]

#show quote.where(block: true): it => block(
  width: 100%,
  above: 7pt,
  below: 8pt,
  breakable: true,
  inset: (left: 14pt, right: 12pt, top: 8pt, bottom: 8pt),
  fill: rgb("#f7f9fc"),
  stroke: (left: 2.2pt + legal-accent),
)[
  #it.body
]

// Pandoc emits Markdown tables wrapped in `#figure(align(center)[#table(...)])`.
// Typst figure blocks are not breakable by default, so a table taller than the
// remaining page overflows and collapses its rows instead of paginating.
// Making figure blocks breakable lets long tables split across pages; it is a
// no-op for tables that already fit.
#show figure: set block(breakable: true)

// Keep complete rows together, while allowing long tables to paginate.
// Pandoc's semantic table.header repeats automatically on continuation pages.
#show table: it => {
  set text(size: 9pt, hyphenate: false)
  set par(justify: false, leading: 0.55em, spacing: 0.12em)
  set table.cell(breakable: false)
  show table.cell.where(y: 0): set text(weight: "bold", fill: legal-accent)
  it
}
#set table(
  inset: (x: 6pt, y: 6pt),
  stroke: (x, y) => (
    bottom: 0.4pt + legal-table-rule,
    top: if y == 0 { 0.8pt + legal-rule } else { none },
  ),
  fill: (x, y) => if y == 0 { legal-table-fill }
    else if calc.odd(y) { rgb("#fafbfd") },
)

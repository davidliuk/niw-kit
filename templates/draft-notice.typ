#let notice-color = rgb("#8a1c1c")
#let notice-fill = rgb("#fff5f5")

#set page(
  footer: context align(center)[
    #text(size: 8pt, fill: notice-color)[
      DRAFT — FACTUAL AND LEGAL REVIEW REQUIRED ·
      #counter(page).display("1")
    ]
  ]
)

#block(
  width: 100%,
  inset: (x: 10pt, y: 7pt),
  fill: notice-fill,
  stroke: 0.9pt + notice-color,
  radius: 2.5pt,
)[
  #align(center)[
    #text(weight: "bold", size: 9.5pt, fill: notice-color)[
      DRAFT — FACTUAL AND LEGAL REVIEW REQUIRED
    ]
  ]
]

#v(8pt)

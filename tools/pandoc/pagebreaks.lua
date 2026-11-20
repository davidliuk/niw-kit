-- A Markdown horizontal rule (---) becomes a page break in the PDF.
function HorizontalRule()
  return pandoc.RawBlock("typst", "#pagebreak()")
end

local column_layouts = {
  -- Header signature (lowercase, "|"-joined) -> relative column widths.
  -- Add a row here when a recurring table needs fixed proportions.
  ["exhibit|title|source|date|supports"] = {0.09, 0.23, 0.21, 0.15, 0.32},
  ["element|core proposition|strongest exhibits"] = {0.22, 0.48, 0.30},
  ["phase|deliverable|evidence of completion"] = {0.25, 0.32, 0.43},
  ["metric|snapshot"] = {0.24, 0.76},
}

local function header_signature(table_block)
  if not table_block.head or #table_block.head.rows == 0 then
    return nil
  end

  local headers = {}
  for _, cell in ipairs(table_block.head.rows[1].cells) do
    local value = pandoc.utils.stringify(cell.contents)
    value = value:lower():gsub("%s+", " ")
    headers[#headers + 1] = value
  end
  return table.concat(headers, "|")
end

function Table(table_block)
  local widths = column_layouts[header_signature(table_block)]
  -- Pandoc wraps Typst tables in align(center). Resolve default column
  -- alignment explicitly so prose does not inherit that centering; preserve
  -- deliberate numeric/right/center alignment in the Markdown source.
  for index, spec in ipairs(table_block.colspecs) do
    local alignment = spec[1]
    if alignment == "AlignDefault" then
      alignment = "AlignLeft"
    end
    local width = spec[2]
    if widths ~= nil and #widths == #table_block.colspecs then
      width = widths[index]
    end
    table_block.colspecs[index] = {alignment, width}
  end
  return table_block
end

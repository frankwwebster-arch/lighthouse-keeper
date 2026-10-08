/** A small CSV reader: a header row, commas, and "quoted, fields" with "" for a quote. */
export function parseCsv(text: string): Record<string, string>[] {
  const rows: string[][] = []
  let row: string[] = []
  let cell = ''
  let quoted = false
  for (let i = 0; i < text.length; i++) {
    const c = text[i]
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') (cell += '"'), i++
      else if (c === '"') quoted = false
      else cell += c
    } else if (c === '"') quoted = true
    else if (c === ',') row.push(cell), (cell = '')
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++
      row.push(cell)
      rows.push(row)
      row = []
      cell = ''
    } else cell += c
  }
  if (cell || row.length) rows.push([...row, cell])
  const [head, ...body] = rows.filter((r) => r.some((x) => x.trim()))
  return body.map((r) => Object.fromEntries(head.map((h, i) => [h.trim(), (r[i] ?? '').trim()])))
}

export interface UpgradeRow {
  object: string
  tier: number
  name: string
  price: number
}

/** The game's part of data/upgrades.csv: which object, which tier, its name and price. Rows with no name are gaps still to fill. */
export const upgradeRows = (text: string): UpgradeRow[] =>
  parseCsv(text)
    .filter((r) => r.object && r.name && Number(r.tier) >= 1)
    .map((r) => ({ object: r.object, tier: Number(r.tier), name: r.name, price: Math.max(0, Math.round(Number(r.price) || 0)) }))

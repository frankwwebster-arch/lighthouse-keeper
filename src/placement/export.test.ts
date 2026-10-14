import fs from 'node:fs'
import path from 'node:path'
import { describe, expect, it } from 'vitest'
import { EXPORT_PATH, ROW_COLUMNS, buildExport, exportText } from './exportTables'

/** Regenerate with `npm run export:placement`. */
describe('route tables for Codex\'s lattice and real-room review pages', () => {
  it('the committed export is current and byte-identical on regeneration', () => {
    const text = exportText()
    expect(exportText()).toBe(text)
    if (process.env.PLACEMENT_EXPORT_WRITE === '1') {
      fs.mkdirSync(path.dirname(EXPORT_PATH), { recursive: true })
      fs.writeFileSync(EXPORT_PATH, text)
    }
    expect(fs.readFileSync(EXPORT_PATH, 'utf8')).toBe(text)
  })

  it('lattice: 1-4 steps both ways; only the full candidate supports every one', () => {
    const lattice = buildExport().lattice.profiles
    const col = (name: (typeof ROW_COLUMNS)[number]) => ROW_COLUMNS.indexOf(name)
    for (const p of lattice) {
      expect(p.routes).toHaveLength(8)
      for (const r of p.routes) {
        if (!('rows' in r)) continue
        const rows = r.rows as unknown[][]
        expect(rows.reduce((a, x) => a + (x[col('dxKu')] as number), 0)).toBe(r.toKu)
        expect(rows[rows.length - 1][col('xKu')]).toBe(r.toKu)
      }
    }
    const supported = (id: string) => lattice.find((p) => p.profile === id)!.routes.filter((r) => r.supported).map((r) => r.steps)
    expect(supported('approved-v1')).toEqual([])
    expect(supported('candidate-42')).toEqual([1, 1, 3, 3])
    expect(supported('candidate-42-f5')).toEqual([1, 1, 2, 2, 3, 3, 4, 4])
  })

  it('real room: the full candidate joins every anchor pair; the approved default brings him in from the door', () => {
    const real = buildExport().realRoom.profiles
    const full = real.find((p) => p.profile === 'candidate-42-f5')!
    expect(full.validation.filter((i) => i.severity === 'error')).toEqual([])
    expect(full.routes.filter((r) => !r.supported)).toEqual([])
    const approved = real.find((p) => p.profile === 'approved-v1')!
    expect(approved.routes.filter((r) => r.supported).map((r) => `${r.from}>${r.to}`)).toEqual(['door:door>bookshelf.browse', 'door:door>tv.use', 'door:door>piano.play', 'door:door>armchair.seat'])
  })
})

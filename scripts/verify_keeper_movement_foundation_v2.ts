#!/usr/bin/env node
/** Verify the presentation-only V2 correction and its immutable V1 authority. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-movement-foundation-2026-10-14-v2')
const REGISTER = path.join(PACK, 'batch-register.json')
const GATE = path.join(ROOT, 'public/keeper-review/keeper-root-motion-gate-v2/index.html')
const CIRCULATION = path.join(ROOT, 'public/keeper-review/keeper-vertical-circulation-v2/index.html')
const fail = (message: string): never => { throw new Error(`Keeper movement foundation V2: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, path.join(PACK, 'HANDOFF.md'), GATE, CIRCULATION]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-movement-foundation-2026-10-14-v2' || record.status !== 'presentation-correction-awaiting-review') fail('identity/status changed')
for (const authority of [record.v1Authority, record.geometryAuthority]) {
  const file = path.join(ROOT, authority.file)
  if (!fs.existsSync(file) || hash(file) !== authority.sha256) fail(`V1 authority changed: ${authority.file}`)
}
if (hash(GATE) !== record.pages.rootMotion.sha256 || hash(CIRCULATION) !== record.pages.verticalCirculation.sha256) fail('review page changed')
for (const [key, value] of Object.entries(record.unchanged)) if (value !== true) fail(`${key} must remain unchanged`)

const gate = fs.readFileSync(GATE, 'utf8')
const circulation = fs.readFileSync(CIRCULATION, 'utf8')
for (const phrase of ['What are you looking at?', 'one logical pixel farther', 'Same</b>Keeper pictures', '76 ku = 9.5 lp', '84 ku = 10.5 lp', 'registered floor anchor (16 lp from the cell', '.start{left:160px', '.finish.current{left:236px', '.finish.candidate{left:244px', 'Loading and decoding the five unique approved frames', 'Promise.all(unique.map(preload))', 'image.decode', 'Previous frame', 'Next frame']) if (!gate.includes(phrase)) fail(`root page omits ${phrase}`)
for (const phrase of ['Vertical circulation V2', '4× authoring scale · not a fixed final screen size', 'responsive 1200 × 760 scene', '.game{width:622px;height:562px}', '@media(max-width:1450px)', '32 × 40 lp box', '128 × 160 CSS pixels', 'not as a literal device preview', 'Previous frame', 'Next frame']) if (!circulation.includes(phrase)) fail(`circulation page omits ${phrase}`)
for (const forbidden of ['Exact proposed game scale', 'Exact game scale · 4 CSS px per logical px']) if (gate.includes(forbidden) || circulation.includes(forbidden)) fail(`misleading scale label survived: ${forbidden}`)
for (const html of [gate, circulation]) {
  const script = html.split('<script>')[1]?.split('</script>')[0]
  if (!script) fail('review script missing')
  new Function(script)
}
const urls = [...gate.matchAll(/\/keeper-review\/keeper-root-motion-gate-v1\/assets\/[A-Za-z0-9._-]+\.png/g)].map((m) => m[0])
if (new Set(urls).size !== 5) fail('V2 must reuse exactly five V1 archived frame URLs')
if (!gate.includes('"deltas":[2,6,12,18,18,12,6,2]') || !gate.includes('"deltas":[3,7,13,19,19,13,7,3]')) fail('root profiles changed')
console.log('Keeper movement foundation V2 verified: V1 pixels/geometry unchanged, root decision clarified and responsive scale language corrected.')

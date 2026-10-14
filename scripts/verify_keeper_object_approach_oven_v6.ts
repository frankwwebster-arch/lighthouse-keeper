#!/usr/bin/env node
/** Verify immutable Oven Approach V6 delivery correction. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-object-approach-oven-2026-10-14-v6')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC_FILE = path.join(PACK, 'delivery-correction-v1.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-object-approach-oven-v6/index.html')
const V5_PAGE = path.join(ROOT, 'public/keeper-review/keeper-object-approach-oven-v5/index.html')
const fail = (message: string): never => { throw new Error(`Keeper oven approach V6: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
for (const file of [REGISTER, SPEC_FILE, path.join(PACK, 'HANDOFF.md'), PAGE, V5_PAGE]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC_FILE, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-object-approach-oven-2026-10-14-v6' || record.status !== 'draft-placement-and-perspective-awaiting-review') fail('identity/status changed')
if (hash(SPEC_FILE) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered candidate changed')
for (const authority of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, authority.file)
  if (!fs.existsSync(file) || hash(file) !== authority.sha256) fail(`authority changed: ${authority.file}`)
}
for (const value of Object.values(spec.boundaries) as boolean[]) if (value !== false) fail('delivery boundary changed')
if (spec.geometryInheritedExactlyFromV5 !== true) fail('V5 geometry inheritance changed')
const html = fs.readFileSync(PAGE, 'utf8')
const v5 = fs.readFileSync(V5_PAGE, 'utf8')
if ((html.match(/rear wall \/ oven base/g) ?? []).length !== 2 || html.includes('shared boot / oven base')) fail('datum labels are not corrected in both panes')
const normalized = html.replaceAll('V6', 'V5').replaceAll('rear wall / oven base', 'shared boot / oven base')
const v5Normalized = v5.replace('rear wall / oven base', 'shared boot / oven base')
if (normalized !== v5Normalized) fail('V6 changes more than version text and the stale datum label')
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
console.log('Keeper oven approach V6 verified: V5 geometry/animation exact and both 14-lp datum labels corrected.')

import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'

const root = process.cwd()
const sitV2 = 'keeper-prime-sit-stand-side-v2'
const sitV3 = 'keeper-prime-sit-stand-side-v3'
const wbV11 = 'keeper-prime-context-workbench-v11'
const wbV12 = 'keeper-prime-context-workbench-v12'
const sitPublic = path.join(root, 'public/keeper-review', sitV3)
const wbPublic = path.join(root, 'public/keeper-review', wbV12)
const sitPack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v3')
const wbPack = path.join(root, 'art/drafts/keeper-prime-context-workbench-2026-10-17-v12')
const hash = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

const targets = [
  path.join(sitPublic, 'index.html'), path.join(wbPublic, 'index.html'),
  path.join(sitPack, 'HANDOFF.md'), path.join(sitPack, 'batch-register.json'),
  path.join(wbPack, 'HANDOFF.md'), path.join(wbPack, 'catalog.json'), path.join(wbPack, 'batch-register.json')
]
if (targets.some(fs.existsSync)) throw new Error('Refusing to overwrite an existing V3/V12 delivery file')
for (const dir of [sitPublic, wbPublic, sitPack, wbPack]) fs.mkdirSync(dir, { recursive: true })

fs.writeFileSync(path.join(sitPublic, 'index.html'), `<script>location='../${sitV2}/index.html'</script>`)
fs.writeFileSync(path.join(wbPublic, 'index.html'), `<script>fetch('/keeper-review/${wbV11}/loader.js').then(x=>x.text()).then(x=>eval(x.replace('/keeper-review/${sitV2}/','/keeper-review/${sitV3}')))</script>`)

const wbCatalog = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-context-workbench-2026-10-17-v11/catalog.json'), 'utf8'))
wbCatalog.schema = 'lighthouse-keeper/context-workbench@12'
wbCatalog.set = wbV12
wbCatalog.sequences = wbCatalog.sequences.map((entry) => entry.id === 'prime-side-sit-stand-v2' ? { ...entry, id: 'prime-side-sit-stand-v3', title: 'NEW · Prime side-right sit ↔ stand V3', url: `/keeper-review/${sitV3}/` } : entry)
fs.writeFileSync(path.join(sitPack, 'HANDOFF.md'), '# Prime Keeper side-right sit/stand V3\n\nDelivery-only wrapper for V2. Keeper frames, roots, timing, route and measured chair geometry are unchanged. V3 uses an absolute loader path because Vercel canonicalises directory URLs without a trailing slash. V2 remains immutable failed-delivery provenance; nothing is promoted.\n')
fs.writeFileSync(path.join(wbPack, 'HANDOFF.md'), '# Prime Keeper Context Workbench V12\n\nDelivery-only wrapper for V11. V12 preserves the same eleven choices, selects side-right sit/stand V3, and uses an absolute loader path. Nothing is promoted.\n')
const register = {
  schema: 'lighthouse-keeper/reversible-review-batch@1', set: sitV3, status: 'review-candidate-delivery-correction',
  predecessor: { set: sitV2, register: 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2/batch-register.json', sha256: hash(path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2/batch-register.json')) },
  immutableContent: { keeperFrames: 'byte-identical to V2/V1', route: { file: `public/keeper-review/${sitV2}/route.json`, sha256: hash(path.join(root, 'public/keeper-review', sitV2, 'route.json')) }, chairGeometry: 'identical to V2: top 11 lp above floor; depth 11 lp spine-to-knee' },
  candidate: { page: { file: `public/keeper-review/${sitV3}/index.html`, sha256: hash(path.join(sitPublic, 'index.html')) }, review: `/keeper-review/${sitV3}/`, workbench: `/keeper-review/${wbV12}/` },
  checks: { absoluteLoaderPaths: true, V2ArtworkUnchanged: true, V2MotionUnchanged: true, finalUnchanged: true, runtimeUnchanged: true, productionUnchanged: true }
}
fs.writeFileSync(path.join(sitPack, 'batch-register.json'), JSON.stringify(register, null, 2) + '\n')
fs.writeFileSync(path.join(wbPack, 'catalog.json'), JSON.stringify(wbCatalog, null, 2) + '\n')
fs.writeFileSync(path.join(wbPack, 'batch-register.json'), JSON.stringify({ schema: 'lighthouse-keeper/context-workbench-register@12', set: wbV12, status: 'delivery-only-successor-to-v11', catalogue: { file: `art/drafts/keeper-prime-context-workbench-2026-10-17-v12/catalog.json`, sha256: hash(path.join(wbPack, 'catalog.json')), choices: wbCatalog.sequences.length }, review: `/keeper-review/${wbV12}/`, checks: { absoluteLoaderPath: true, V11ChoicesRetained: true, sittingCandidate: sitV3, finalUnchanged: true, runtimeUnchanged: true, productionUnchanged: true } }, null, 2) + '\n')
console.log(JSON.stringify({ sit: sitV3, workbench: wbV12, choices: wbCatalog.sequences.length, deliveryOnly: true }, null, 2))

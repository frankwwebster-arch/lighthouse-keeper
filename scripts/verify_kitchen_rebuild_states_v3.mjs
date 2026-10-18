import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-rebuild-states-2026-10-18-v3'
const raw = path.join(root, 'art/raw', set)
const draft = path.join(root, 'art/drafts', set)
const source = path.join(root, 'art/source', set, 'generated')
const page = path.join(root, 'public/keeper-review/kitchen-rebuild-states-v3/index.html')
const archive = path.join(root, 'review-archive/sets/kitchen-rebuild-states-v3.json')
const v2 = path.join(root, 'art/raw/kitchen-rebuild-states-2026-10-18-v2')
const binV31 = path.join(root, 'art/raw/kitchen-bin-effects-2026-10-18-v31')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const at = (im, x, y) => (y * im.width + x) * 4
const alpha = (im, x, y) => im.data[at(im, x, y) + 3]
const size = (im, expected, label) => assert.deepEqual([im.width, im.height], expected, `${label} dimensions drifted`)
const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json'), 'utf8'))

assert.equal(sha(path.join(source, 'user-approved-broken-effects.png')), '75899da25b94494545263afbd49b17663c93442725d6043e9bb9782f1f1c41ee')
assert.equal(sha(path.join(source, 'canon-height-table-chair-source.png')), '6e60ddfe6ba9c205618dbdb4404f6f4b31d2a612ae5b884482ae07ff7b6086a1')
assert.equal(catalogue.set, set); assert.equal(catalogue.version, 3)
assert.equal(catalogue.status, 'effect-placement-workbench-awaiting-review')
assert.equal(catalogue.method.objectArtSeparateFromEffects, true)
assert.equal(catalogue.method.userTransformableEffects, true)
assert.deepEqual(catalogue.method.transformControls, ['drag', 'resize', 'crop', 'nudge', 'local-save', 'json-export'])
assert.deepEqual(catalogue.table, {origin: [680, 129], widthPixels: 80, footLineY: 208, tableTopY: 150, chairSeatY: 177})
assert.equal(catalogue.promotion, 'none'); assert.equal(catalogue.runtimeWiring, 'unchanged')

for (const [name, meta] of Object.entries(catalogue.outputs)) {
  const file = path.join(raw, name); assert.ok(fs.existsSync(file), `missing ${name}`)
  assert.equal(sha(file), meta.sha256, `${name} hash drifted`); size(png(file), meta.pixels, name)
}

for (const asset of ['fridge', 'kettle', 'oven', 'bowl']) for (const state of catalogue.states[asset]) {
  assert.equal(sha(path.join(raw, `${asset}-${state}.png`)), sha(path.join(v2, `${asset}-${state}.png`)), `${asset} ${state} should remain exact V2`)
}
for (const asset of ['toaster', 'basin']) {
  for (const state of catalogue.states[asset].filter(s => s !== 'broken')) assert.equal(sha(path.join(raw, `${asset}-${state}.png`)), sha(path.join(v2, `${asset}-${state}.png`)))
  const broken = png(path.join(raw, `${asset}-broken.png`)); size(broken, [84, 133], `${asset} broken extended`)
  let headroomArt = 0; for (let y = 0; y < 35; y++) for (let x = 0; x < 84; x++) if (alpha(broken, x, y)) headroomArt++
  assert.ok(headroomArt > 30, `${asset} broken top is still cropped`)
}

const table = png(path.join(raw, 'table-chair.png')); size(table, [84, 79], 'table-chair')
let top = 79, bottom = -1; for (let y = 0; y < 79; y++) for (let x = 0; x < 84; x++) if (alpha(table, x, y)) { top = Math.min(top, y); bottom = Math.max(bottom, y) }
assert.equal(129 + top, 150, 'tabletop no longer begins at canon room y150')
assert.equal(129 + bottom + 1, 208, 'furniture foot line no longer ends at canon room y208')

assert.equal(Object.keys(catalogue.effectFamilies).length, 10)
assert.equal(Object.keys(catalogue.effects).length, 30)
for (const [family, familyMeta] of Object.entries(catalogue.effectFamilies)) {
  assert.equal(familyMeta.models.length, 3, `${family} does not offer three models`)
  assert.ok(familyMeta.models.includes(familyMeta.default))
  for (const name of familyMeta.models) {
    const meta = catalogue.effects[name]; assert.equal(meta.family, family); assert.equal(meta.frames, 40); assert.equal(meta.fps, 4); assert.equal(meta.durationSeconds, 10)
    assert.equal(meta.reusable, true); assert.equal(meta.effectOnly, true); assert.equal(meta.editableTransform, true); assert.deepEqual(meta.cellPixels, [120, 144])
    const strip = png(path.join(raw, meta.file)); size(strip, [4800, 144], name)
    const hashes = new Set(); let visibleFrames = 0
    for (let frame = 0; frame < 40; frame++) {
      const bytes = Buffer.alloc(120 * 144 * 4); let visible = 0
      for (let y = 0; y < 144; y++) for (let x = 0; x < 120; x++) {
        const sourceOffset = at(strip, frame * 120 + x, y), targetOffset = (y * 120 + x) * 4
        strip.data.copy(bytes, targetOffset, sourceOffset, sourceOffset + 4)
        if (strip.data[sourceOffset + 3]) visible++
        if (x === 0 || x === 119 || y === 0 || y === 143) assert.equal(strip.data[sourceOffset + 3], 0, `${name} frame ${frame} touches a shared edge`)
      }
      if (visible) visibleFrames++; hashes.add(crypto.createHash('sha256').update(bytes).digest('hex'))
    }
    assert.ok(visibleFrames >= 8, `${name} is not visibly animated`)
    assert.ok(hashes.size >= 4, `${name} lacks motion/timing variation`)
  }
}

// The approved V31 smell remains pixel-exact inside the common 120x144 wrapper.
const approvedSmell = png(path.join(binV31, 'fx-stench-miasma-f40.png'))
const wrappedSmell = png(path.join(raw, catalogue.effects['bin-broken-smell--classic'].file))
for (let frame = 0; frame < 40; frame++) for (let y = 0; y < 80; y++) for (let x = 0; x < 80; x++) {
  const a = at(approvedSmell, frame * 80 + x, y), b = at(wrappedSmell, frame * 120 + x + 20, y + 60)
  for (let c = 0; c < 4; c++) assert.equal(wrappedSmell.data[b + c], approvedSmell.data[a + c], `approved smell changed at frame ${frame}`)
}

// Warning art is locked to the On-state room coordinates in every spatial model.
const warning = png(path.join(raw, catalogue.effects['oven-broken-flicker--classic'].file))
const frameBox = frame => { let minX=120,minY=144,maxX=-1,maxY=-1; for(let y=0;y<144;y++)for(let x=0;x<120;x++)if(alpha(warning,frame*120+x,y)){minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x);maxY=Math.max(maxY,y)} return [318+minX,74+minY,318+maxX+1,74+maxY+1] }
assert.deepEqual(frameBox(0), [393, 129, 411, 147], 'red warning no longer matches the On lamp')
assert.deepEqual(frameBox(5), [347, 175, 397, 194], 'cavity flicker no longer matches the On cavity')

const html = fs.readFileSync(page, 'utf8')
for (const pattern of [/Promise\.all\(DATA\.media\.map\(load\)/, /i\.decode\(\)/, /onpointerdown/, /onpointermove/, /localStorage\.setItem/, /navigator\.clipboard/, /Download JSON/, /Crop left/, /Shift\+arrow/, /effectFamilies/, /three animated models/]) assert.match(html, pattern)

assert.ok(fs.existsSync(archive), 'archive manifest missing; run npm run archive:keeper-review')
const manifest = JSON.parse(fs.readFileSync(archive, 'utf8')); assert.equal(manifest.set, 'kitchen-rebuild-states-v3')
const archived = new Set(Object.keys(manifest.entries).map(entry => path.basename(entry)))
for (const name of Object.keys(catalogue.outputs)) assert.ok(archived.has(name), `${name} was not content-addressed`)
console.log('Kitchen Rebuild V3 verified: 10 reusable effect families, 3 animated models each, drag/resize/crop persistence/export, exact oven anchors, restored toast/tap headroom, canon furniture datums')

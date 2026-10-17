import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const source = path.join(root, 'art/source/kitchen-rear-wall-flow-2026-10-17-v22')
const raw = path.join(root, 'art/raw/kitchen-rear-wall-flow-2026-10-17-v22')
const draft = path.join(root, 'art/drafts/kitchen-rear-wall-flow-2026-10-17-v22')
const v21Raw = path.join(root, 'art/raw/kitchen-final-assets-2026-10-17-v21')
const pageFile = path.join(root, 'public/keeper-review/kitchen-rear-wall-flow-v22/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-rear-wall-flow-v22.json')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const pixel = (image, x, y) => Array.from(image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4))

const outputPins = {
  'alignment-guide.png': '4ef7a64b035363bf07a161d30be73279be6064d87b0d14576c2b9f5e3f7698c9',
  'full-kitchen-upgrade1.png': '3de553ac384eb63d4e960c84073481c48d56b6d25afc008566ec50575c10cf8c',
  'full-kitchen.png': '8dbba02b4f664db40085975510372ab30abd545df869a2ef46609ffc188c69e4',
  'v21-before.png': 'd3b6aedd1f6d0fefff7b2543f66cfe05737c55f419f8dab92de73423730d9925',
  'v22-after.png': '805fbbe37833bcc30b9e464af31c2f51d693c59f081b72d82a53eeaa6f6f883c',
}
for (const [file, expected] of Object.entries(outputPins)) {
  assert.equal(sha(path.join(raw, file)), expected, `${file} deterministic output changed`)
}

assert.equal(sha(path.join(source, 'continuous-run-reference.png')), '5d5451acbaa81a48918268d25482a1d3f657a77c441c9d5b4f87ed547d4f9707')
assert.equal(sha(path.join(v21Raw, 'full-kitchen.png')), 'b6d1074e7492c2f5439ec032e6573ae194988e7d9e12cc6b123ce62c9b92f73f', 'V21 basic room changed')
assert.equal(sha(path.join(v21Raw, 'full-kitchen-upgrade1.png')), 'bef3f8c4a42750c354e55eb04bce9b6b25ce413bfc82362b182ca852a108d623', 'V21 upgrade room changed')

const data = JSON.parse(fs.readFileSync(path.join(draft, 'layout-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
assert.equal(data.version, 22)
assert.equal(data.status, 'rear-wall-flow-correction-awaiting-visual-acceptance')
assert.deepEqual(data.room, { lp: [193, 56], pixels: [772, 224], footLineLp: 52, foregroundLp: 4 })
assert.deepEqual(data.fittedRun, {
  bays: 6,
  bayWidthLp: 21,
  runWidthLp: 126,
  startLp: 21,
  worktopYpx: 134,
  bodyBottomYpx: 199,
  depthAuthority: 'V21 kettle bay',
  construction: 'one shared carcass; per-bay centre treatments; outer end caps only',
})
assert.equal(data.sources.v21RawTreeSha256, 'fb4b4f8c955a3fae7fdf2ca39f56b14f81d5fc3aaceef11b6dca64bbeb88a453')
assert.equal(data.sources.v21SourceTreeSha256, '6c07271938076ff396575ed5f1f878544127d921f5df21572030b233dffc53be')
for (const key of ['approved', 'promoted', 'runtimeChanged', 'finalChanged', 'keeperChanged']) assert.equal(register[key], false)
assert.equal(register.v21Preserved, true)

const basic = png(path.join(raw, 'full-kitchen.png'))
const upgrade = png(path.join(raw, 'full-kitchen-upgrade1.png'))
const guide = png(path.join(raw, 'alignment-guide.png'))
const before = png(path.join(raw, 'v21-before.png'))
const after = png(path.join(raw, 'v22-after.png'))
assert.deepEqual([basic.width, basic.height], [772, 224])
assert.deepEqual([upgrade.width, upgrade.height], [772, 224])
assert.deepEqual([guide.width, guide.height], [772, 224])
assert.deepEqual([before.width, before.height], [504, 112])
assert.deepEqual([after.width, after.height], [504, 112])

// One worktop: the structural rows cross all six bays without a break or a
// freestanding end cap at an internal 21-lp boundary.
for (let x = 84; x < 588; x++) {
  assert.deepEqual(pixel(basic, x, 134), [6, 27, 56, 255], `rear edge broke at x=${x}`)
  assert.deepEqual(pixel(basic, x, 138), [168, 255, 240, 255], `highlight broke at x=${x}`)
  assert.deepEqual(pixel(basic, x, 150), [6, 27, 56, 255], `fascia broke at x=${x}`)
}

// The kettle-authority front terminates on one common line. Only the shared,
// recessed toe-kick may continue toward the foot line.
for (let x = 88; x < 584; x++) {
  assert.deepEqual(pixel(basic, x, 199), [6, 27, 56, 255], `body/plinth line broke at x=${x}`)
  assert.deepEqual(pixel(basic, x, 207), [6, 27, 56, 255], `toe-kick line broke at x=${x}`)
}

// The two room variants differ only inside the oven treatment, never in the
// shared carcass or any neighbouring asset.
let changed = 0
for (let y = 0; y < 224; y++) for (let x = 0; x < 772; x++) {
  const a = pixel(basic, x, y), b = pixel(upgrade, x, y)
  if (a.some((value, index) => value !== b[index])) {
    changed++
    assert.ok(x >= 342 && x < 414 && y < 199, `oven variant escaped treatment window at ${x},${y}`)
  }
}
assert.ok(changed > 100, 'oven tiers must visibly differ')

// All foreground pixels remain the common room floor; fitted art ends at the
// 52-lp line and leaves the final 4 lp clear.
for (const image of [basic, upgrade]) for (let y = 208; y < 224; y++) for (let x = 84; x < 588; x++) {
  const [r, g, b] = pixel(image, x, y)
  assert.ok(!(b > r * 1.3 && b > g * 1.05), `fitted run intrudes into foreground at ${x},${y}`)
}

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /One continuous fitted galley/)
assert.match(page, /kettle bay's rear-wall depth/)
assert.match(page, /one uninterrupted worktop/)
assert.match(page, /Promise\.all\(files\.map/)
assert.ok(page.includes('/keeper-review/kitchen-rear-wall-flow-v22/assets/full-kitchen.png'))
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-rear-wall-flow-v22'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, Object.keys(outputPins).length)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V22 rear-wall continuous run verified')

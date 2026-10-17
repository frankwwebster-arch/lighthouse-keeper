import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const source = path.join(root, 'art/source/kitchen-final-assets-2026-10-17-v21')
const raw = path.join(root, 'art/raw/kitchen-final-assets-2026-10-17-v21')
const draft = path.join(root, 'art/drafts/kitchen-final-assets-2026-10-17-v21')
const pageFile = path.join(root, 'public/keeper-review/kitchen-final-assets-v21/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-final-assets-v21.json')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const alphaBounds = image => {
  const xs = [], ys = []
  for (let y = 0; y < image.height; y++) for (let x = 0; x < image.width; x++) {
    if (image.data[(y * image.width + x) * 4 + 3] >= 8) { xs.push(x); ys.push(y) }
  }
  return { minX: Math.min(...xs), minY: Math.min(...ys), maxX: Math.max(...xs), maxY: Math.max(...ys), width: Math.max(...xs) - Math.min(...xs) + 1, height: Math.max(...ys) - Math.min(...ys) + 1 }
}
const pixel = (image, x, y) => Array.from(image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4))
const data = JSON.parse(fs.readFileSync(path.join(draft, 'asset-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
const objectDimensions = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_object_dimensions.json'), 'utf8'))

const sourcePins = {
  'basic-oven-source.png': '0adbd9dd89aea4594dfdc6e601c1855414c5db1b744e186f0f427abd97915423',
  'pedal-bin-source.png': 'c75bca8c78f3e5f46cb8e810004aff5a7bb7fc03d2ef6b162edaed4948cd33b1',
  'table-chair-source.png': '45a662ca150897caa37443b439b2e99fe1c988ad4493e8020c7d1d3ad0086708',
}
for (const [file, expected] of Object.entries(sourcePins)) assert.equal(sha(path.join(source, file)), expected, `${file} source changed`)

const outputPins = {
  'basic-oven.png': '45658c2649d10efc896d646821b16e12d3a19fc401d04168e00ace3a6f016ba8',
  'chair.png': '69d1188adb69678299d072e2cdc500ccbd3821d75a1f139cb1063ecfe53d87df',
  'fridge.png': 'e59142a1ed4d7181daa2b4968061642416e3d3352c1cbd3fd7e053676c25da6c',
  'full-kitchen-upgrade1.png': 'bef3f8c4a42750c354e55eb04bce9b6b25ce413bfc82362b182ca852a108d623',
  'full-kitchen.png': 'b6d1074e7492c2f5439ec032e6573ae194988e7d9e12cc6b123ce62c9b92f73f',
  'kettle.png': 'a3b7d1ea445b66a5c72d6c52d290fd9d2e1859342867cbf0f5392db460daad37',
  'mixer.png': 'de45048124ad67398f84ac86c7cf3d359c21334c39422d2fbe1b4bac5238f47f',
  'pedal-bin.png': '90652f844bd9d6a7ef84b63ee257f6bdc0d8e5817bde3449de192c8ab138f802',
  'sink.png': '9bad73df84998eb6187e5ee78a0a9784535c5fc529786060704547f7985f5bb9',
  'table-chair-fit.png': 'b73a2fef54acce931194cf151a047bf7a01469bd937bb3ff7fcdf485ae9cd1fb',
  'table-chair.png': 'bef1250d1d4aeb590dbd297a7ab46c1a184266b5b3e882b101de654e0385d1df',
  'table.png': '582fbf39719bbda940d2dadf3821852f3415b984c93787f3d7ce6d1a118b74ad',
  'toaster.png': '2bf3b2b2c14c9a87ef2165b45c6cedd3dd109d7ecdeb9b1af79b1a8acf5f97fe',
  'upgrade-oven.png': '57b0fdb6c0b2193ab6f481a4b9f45eb4bd19450d7c420eaf2136a7e27eafce2c',
}
for (const [file, expected] of Object.entries(outputPins)) assert.equal(sha(path.join(raw, file)), expected, `${file} deterministic output changed`)

assert.equal(data.version, 21)
assert.equal(data.status, 'complete-final-candidate-awaiting-visual-acceptance')
assert.deepEqual(data.room, { lp: [193, 56], pixels: [772, 224], footLineLp: 52, foregroundLp: 4 })
assert.deepEqual(data.ovenTiers.basic, { cabinetBayLp: 21, applianceInsetLp: 15, doors: 1 })
assert.equal(data.ovenTiers.upgrade1.doors, 2)
assert.deepEqual(data.pedalBin, { standalone: true, widthLp: 10, heightLp: 13 })
assert.deepEqual(data.tableForOne, {
  chairs: 1,
  chairSeatSupportLp: 7.75,
  chairDepthLp: 8.625,
  shinClearanceLp: 0.5,
  tabletopLp: 14.5,
  tabletopThicknessLp: 1.5,
  tableWidthLp: 20,
  authority: '/keeper-review/keeper-prime-sit-stand-side-v6',
})
assert.equal(data.assets.length, 9)
assert.deepEqual(objectDimensions.furniture.kitchenTableForOneV21, {
  surfaceHeight: 14.5,
  topThickness: 1.5,
  width: 20,
  chairCount: 1,
  chairSeatTopHeight: 7.75,
  chairDepth: 8.625,
  chairShinClearance: 0.5,
  authority: 'data/keeper_prime_seat_geometry_v3.json and the approved Side-right Sit/Stand V6 final seated hand line',
  scope: 'Kitchen V21 side-right one-person table only; does not replace the general dining-table or runtime datums.',
  status: 'final-candidate-authoring-datums-awaiting-visual-acceptance',
})
for (const record of data.assets) assert.equal(sha(path.join(raw, record.file)), record.sha256, `${record.file} catalogue hash drifted`)
for (const key of ['approved', 'promoted', 'runtimeChanged', 'finalChanged', 'keeperChanged']) assert.equal(register[key], false, `${key} must remain false`)
assert.equal(register.completeAssetSet, true)
assert.equal(register.predecessor.commit, '2d67163')

const basic = png(path.join(raw, 'basic-oven.png'))
const upgrade = png(path.join(raw, 'upgrade-oven.png'))
const bin = png(path.join(raw, 'pedal-bin.png'))
const chair = png(path.join(raw, 'chair.png'))
const table = png(path.join(raw, 'table.png'))
const pair = png(path.join(raw, 'table-chair.png'))
const full = png(path.join(raw, 'full-kitchen.png'))
const fullUpgrade = png(path.join(raw, 'full-kitchen-upgrade1.png'))
const fit = png(path.join(raw, 'table-chair-fit.png'))
assert.deepEqual([basic.width, basic.height], [108, 120])
assert.deepEqual([upgrade.width, upgrade.height], [84, 120])
assert.deepEqual([bin.width, bin.height], [64, 76])
assert.deepEqual([chair.width, chair.height], [35, 79])
assert.deepEqual([table.width, table.height], [80, 58])
assert.deepEqual([pair.width, pair.height], [168, 96])
assert.deepEqual([full.width, full.height], [772, 224])
assert.deepEqual([fullUpgrade.width, fullUpgrade.height], [772, 224])
assert.deepEqual([fit.width, fit.height], [688, 224])
assert.deepEqual(alphaBounds(basic), { minX: 12, minY: 31, maxX: 95, maxY: 107, width: 84, height: 77 })
assert.deepEqual(alphaBounds(bin), { minX: 12, minY: 12, maxX: 51, maxY: 63, width: 40, height: 52 })
assert.equal(alphaBounds(chair).width, 35)
assert.equal(alphaBounds(chair).height, 79)
assert.equal(alphaBounds(table).width, 80)
assert.equal(alphaBounds(table).height, 58)

// Every cell used as an isolated asset retains a transparent safety gutter.
for (const image of [basic, bin, pair]) {
  for (let x = 0; x < image.width; x++) {
    assert.equal(pixel(image, x, 0)[3], 0)
    assert.equal(pixel(image, x, image.height - 1)[3], 0)
  }
  for (let y = 0; y < image.height; y++) {
    assert.equal(pixel(image, 0, y)[3], 0)
    assert.equal(pixel(image, image.width - 1, y)[3], 0)
  }
}

// The full-room floor channel (rows 208–223) is clear of blue cabinet art.
for (const image of [full, fullUpgrade]) for (let y = 208; y < 224; y++) for (let x = 0; x < 772; x++) {
  const [r, g, b] = pixel(image, x, y)
  assert.ok(!(b > r * 1.3 && b > g * 1.05), `cabinet/furniture intrudes into foreground at ${x},${y}`)
}

// Five internal fitted-run joins have continuous sea-glass worktop bridges.
for (let seam = 1; seam < 6; seam++) {
  const x = 84 + seam * 84
  for (let y = 137; y <= 143; y++) {
    const [r, g, b] = pixel(full, x, y)
    assert.ok(g > 110 && b > 110 && g > r * 1.1, `worktop discontinuity at seam ${seam}, y=${y}`)
  }
}

// The two room variants differ only in the selected oven bay.
let changed = 0
for (let y = 0; y < 224; y++) for (let x = 0; x < 772; x++) {
  const a = pixel(full, x, y), b = pixel(fullUpgrade, x, y)
  if (a.some((value, index) => value !== b[index])) {
    changed++
    assert.ok(x >= 84 + 3 * 84 && x < 84 + 4 * 84, `oven variant changed outside oven bay at ${x},${y}`)
  }
}
assert.ok(changed > 100, 'basic and upgrade room must visibly differ')

assert.match(page, /Full kitchen · every asset in situ/)
assert.match(page, /Basic oven/)
assert.match(page, /Upgrade 1 oven/)
assert.match(page, /7\.75 lp/)
assert.match(page, /14\.5 lp/)
assert.match(page, /exactly one V6-sized chair/)
assert.match(page, /Promise\.all\(preload\.map/)
assert.ok(page.includes('/keeper-review/kitchen-final-assets-v21/assets/full-kitchen.png'))
assert.ok(page.includes("'full-kitchen-upgrade1.png'"))
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-final-assets-v21'/)
assert.match(nextConfig, /destination: '\/keeper-review\/kitchen-final-assets-v21\/index\.html'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, Object.keys(outputPins).length)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V21 complete final candidate verified')

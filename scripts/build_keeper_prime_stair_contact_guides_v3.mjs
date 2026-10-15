#!/usr/bin/env node
/** Build exact two-step stair contact guides before finished-art rendering. */
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v3')
const guideDir = path.join(pack, 'guides')
fs.mkdirSync(guideDir, { recursive: true })
const S = 2
const W = 256
const H = 320
const colours = {
  background: [15, 28, 36, 255],
  body: [225, 233, 238, 255],
  joint: [255, 222, 119, 255],
  near: [255, 82, 100, 255],
  far: [69, 211, 255, 255],
  tread: [124, 147, 160, 255],
  contact: [117, 230, 167, 255],
  forbidden: [255, 90, 90, 110],
}
const frames = [
  { root: [0, 0], support: 'far', contacts: { far: 'lower' }, near: { knee: [108, 257], ankle: [91, 280], heel: [74, 299], toe: [103, 299] }, far: { knee: [128, 266], ankle: [128, 292], heel: [110, 316], toe: [138, 316] } },
  { root: [1, 0], support: 'far', contacts: { far: 'lower' }, near: { knee: [149, 247], ankle: [166, 268], heel: [148, 282], toe: [179, 282] }, far: { knee: [122, 266], ankle: [120, 292], heel: [102, 316], toe: [130, 316] } },
  { root: [2, 0], support: 'far', contacts: { far: 'lower', near: 'upper' }, near: { knee: [150, 251], ankle: [160, 270], heel: [145, 286], toe: [176, 286] }, far: { knee: [118, 266], ankle: [112, 292], heel: [94, 316], toe: [122, 316] } },
  { root: [5.25, 3.75], support: 'near', contacts: { near: 'lower' }, near: { knee: [144, 266], ankle: [144, 292], heel: [126, 316], toe: [156, 316] }, far: { knee: [108, 253], ankle: [90, 275], heel: [73, 290], toe: [102, 290] } },
  { root: [5.25, 3.75], support: 'near', contacts: { near: 'lower' }, near: { knee: [142, 266], ankle: [142, 292], heel: [124, 316], toe: [154, 316] }, far: { knee: [110, 257], ankle: [93, 280], heel: [76, 299], toe: [105, 299] } },
  { root: [6.25, 3.75], support: 'near', contacts: { near: 'lower' }, near: { knee: [124, 266], ankle: [120, 292], heel: [102, 316], toe: [132, 316] }, far: { knee: [151, 247], ankle: [168, 268], heel: [150, 282], toe: [181, 282] } },
  { root: [7.25, 3.75], support: 'near', contacts: { near: 'lower', far: 'upper' }, near: { knee: [118, 266], ankle: [112, 292], heel: [94, 316], toe: [124, 316] }, far: { knee: [151, 251], ankle: [161, 270], heel: [146, 286], toe: [177, 286] } },
  { root: [10.5, 7.5], support: 'far', contacts: { far: 'lower' }, near: { knee: [108, 253], ankle: [90, 275], heel: [73, 290], toe: [102, 290] }, far: { knee: [144, 266], ankle: [144, 292], heel: [126, 316], toe: [156, 316] } },
]

const setPixel = (png, x, y, colour) => {
  x = Math.round(x * S)
  y = Math.round(y * S)
  if (x < 0 || y < 0 || x >= png.width || y >= png.height) return
  const offset = (y * png.width + x) * 4
  for (let channel = 0; channel < 4; channel++) png.data[offset + channel] = colour[channel]
}
const disc = (png, x, y, radius, colour) => {
  for (let py = y - radius; py <= y + radius; py++) for (let px = x - radius; px <= x + radius; px++) if ((px - x) ** 2 + (py - y) ** 2 <= radius ** 2) setPixel(png, px, py, colour)
}
const line = (png, a, b, width, colour) => {
  const steps = Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) * 2)
  for (let step = 0; step <= steps; step++) {
    const t = step / steps
    disc(png, a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, width / 2, colour)
  }
}
const rect = (png, x, y, width, height, colour) => {
  for (let py = y; py < y + height; py++) for (let px = x; px < x + width; px++) setPixel(png, px, py, colour)
}
const drawLimb = (png, hip, leg, colour) => {
  line(png, hip, leg.knee, 7, colour)
  line(png, leg.knee, leg.ankle, 7, colour)
  line(png, leg.heel, leg.toe, 8, colour)
  line(png, leg.ankle, [(leg.heel[0] + leg.toe[0]) / 2, (leg.heel[1] + leg.toe[1]) / 2], 7, colour)
  for (const point of [hip, leg.knee, leg.ankle]) disc(png, point[0], point[1], 5, colours.joint)
}

const records = []
for (let index = 0; index < frames.length; index++) {
  const frame = frames[index]
  const png = new PNG({ width: W * S, height: H * S })
  rect(png, 0, 0, W, H, colours.background)
  // Three exact stair surfaces: current support, +1 riser and +2 risers.
  for (const [y, x0] of [[316, 34], [286, 118], [256, 202]]) {
    line(png, [x0, y], [Math.min(252, x0 + 58), y], 2, colours.tread)
    rect(png, x0, y + 2, Math.min(58, 252 - x0), 9, colours.forbidden)
  }
  // Stable torso/head scaffold; legs are the binding authority.
  line(png, [128, 222], [128, 122], 10, colours.body)
  disc(png, 132, 84, 29, colours.body)
  line(png, [116, 125], [95, 172], 7, colours.body)
  line(png, [140, 125], [161, 172], 7, colours.body)
  drawLimb(png, [120, 224], frame.near, colours.near)
  drawLimb(png, [134, 224], frame.far, colours.far)
  for (const [legName, level] of Object.entries(frame.contacts)) {
    const leg = frame[legName]
    line(png, leg.heel, leg.toe, 3, colours.contact)
    disc(png, leg.toe[0], leg.toe[1], 4, colours.contact)
    if ((level === 'lower' && leg.toe[1] !== 316) || (level === 'upper' && leg.toe[1] !== 286)) throw new Error(`frame ${index + 1} contact datum mismatch`)
  }
  const file = path.join(guideDir, `stair-contact-guide-right-f${index + 1}.png`)
  fs.writeFileSync(file, PNG.sync.write(png, { colorType: 6 }))
  records.push({ frame: index + 1, file: path.relative(root, file), rootOffsetLp: frame.root, supportLeg: frame.support, contacts: frame.contacts, nearLeg: frame.near, farLeg: frame.far })
}

const sheet = new PNG({ width: W * S * 4, height: H * S * 2 })
for (let index = 0; index < records.length; index++) {
  const guide = PNG.sync.read(fs.readFileSync(path.join(root, records[index].file)))
  const x0 = (index % 4) * guide.width
  const y0 = Math.floor(index / 4) * guide.height
  for (let y = 0; y < guide.height; y++) {
    const sourceStart = y * guide.width * 4
    const targetStart = ((y0 + y) * sheet.width + x0) * 4
    guide.data.copy(sheet.data, targetStart, sourceStart, sourceStart + guide.width * 4)
  }
}
const sheetPath = path.join(guideDir, 'stair-contact-guide-right-8pose.png')
fs.writeFileSync(sheetPath, PNG.sync.write(sheet, { colorType: 6 }))

const contract = {
  schema: 'lighthouse-keeper/stair-contact-rig@1',
  direction: 'right-facing authoring; exact horizontal mirror produces leftward gameplay flight',
  cell: [256, 320],
  density: 8,
  treadRunLp: 5.25,
  riserHeightLp: 3.75,
  cycleRunLp: 10.5,
  cycleRiseLp: 7.5,
  colours: { nearLeg: '#ff5264', farLeg: '#45d3ff', exactSoleContact: '#75e6a7', forbiddenBelowTread: '#ff5a5a' },
  rules: ['F1-F4 advances near leg one riser while far leg supports.', 'F5-F8 advances far leg one riser while near leg supports.', 'A planted sole is exactly on y=316; a reaching sole is exactly one 30-source-pixel riser above at y=286.', 'No finished opaque boot pixel may enter the red forbidden-below-tread region at its world x-position.'],
  frames: records,
  contactSheet: path.relative(root, sheetPath),
}
fs.writeFileSync(path.join(pack, 'stair-contact-rig-v3.json'), `${JSON.stringify(contract, null, 2)}\n`)
console.log(JSON.stringify({ guides: records.length, contract: path.relative(root, path.join(pack, 'stair-contact-rig-v3.json')) }, null, 2))

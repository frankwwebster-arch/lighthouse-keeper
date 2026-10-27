#!/usr/bin/env node

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ROOT = path.resolve(__dirname, '../..')
const OUT = path.join(__dirname, 'outputs')
const SCALE = 2
const WIDTH = 2048
const HEIGHT = 576

const SOURCE = path.join(ROOT, 'review/kitchen-proof-v8-assets-v1/outputs')
const KEEPER = path.join(ROOT, 'review/kitchen-proof-v3/sources/prime/keeper_prime_master-neutral-standing-side-right_f1.png')
const CONCEPT = path.join(__dirname, 'sources/imagegen/room-shell-style-concept.png')
const REFERENCE = path.join(ROOT, 'reference/shell/room-shell-reference-01.png')

const WINDOWS = [
  { bounds: [622, 106, 790, 274], panes: [[638, 122, 700, 185], [712, 122, 774, 185], [638, 197, 700, 258], [712, 197, 774, 258]] },
  { bounds: [1294, 106, 1462, 274], panes: [[1310, 122, 1372, 185], [1384, 122, 1446, 185], [1310, 197, 1372, 258], [1384, 197, 1446, 258]] },
]

const rgb = (hex, alpha = 255) => {
  const value = Number.parseInt(hex.replace('#', ''), 16)
  return [(value >> 16) & 255, (value >> 8) & 255, value & 255, alpha]
}

const COLORS = {
  ink: rgb('#3C2419'),
  inkSoft: rgb('#68422C'),
  plaster: rgb('#F5E7C9'),
  plasterLight: rgb('#FBF2DE'),
  plasterShade: rgb('#E8CFAB'),
  wood: rgb('#B96F32'),
  woodLight: rgb('#D69449'),
  woodDark: rgb('#70401F'),
  woodDeep: rgb('#4A2B1D'),
  floor: rgb('#D99747'),
  floorLight: rgb('#E9B264'),
  floorDark: rgb('#A85E2E'),
  slab: rgb('#6C432C'),
  brass: rgb('#E0A735'),
  magenta: [255, 0, 255, 255],
}

function blank(width, height, color = [0, 0, 0, 0]) {
  const image = new PNG({ width, height })
  for (let i = 0; i < image.data.length; i += 4) {
    image.data[i] = color[0]
    image.data[i + 1] = color[1]
    image.data[i + 2] = color[2]
    image.data[i + 3] = color[3]
  }
  return image
}

function blendPixel(image, x, y, color) {
  x = Math.round(x)
  y = Math.round(y)
  if (x < 0 || y < 0 || x >= image.width || y >= image.height) return
  const offset = (y * image.width + x) * 4
  const sa = color[3] / 255
  const da = image.data[offset + 3] / 255
  const oa = sa + da * (1 - sa)
  if (oa === 0) return
  for (let channel = 0; channel < 3; channel++) {
    image.data[offset + channel] = Math.round((color[channel] * sa + image.data[offset + channel] * da * (1 - sa)) / oa)
  }
  image.data[offset + 3] = Math.round(oa * 255)
}

function rect(image, x0, y0, x1, y1, color) {
  const left = Math.max(0, Math.floor(x0))
  const top = Math.max(0, Math.floor(y0))
  const right = Math.min(image.width, Math.ceil(x1))
  const bottom = Math.min(image.height, Math.ceil(y1))
  for (let y = top; y < bottom; y++) {
    for (let x = left; x < right; x++) blendPixel(image, x, y, color)
  }
}

function polygon(image, points, color) {
  const minY = Math.max(0, Math.floor(Math.min(...points.map((point) => point[1]))))
  const maxY = Math.min(image.height - 1, Math.ceil(Math.max(...points.map((point) => point[1]))))
  for (let y = minY; y <= maxY; y++) {
    const scanY = y + 0.5
    const intersections = []
    for (let i = 0; i < points.length; i++) {
      const a = points[i]
      const b = points[(i + 1) % points.length]
      if ((a[1] <= scanY && b[1] > scanY) || (b[1] <= scanY && a[1] > scanY)) {
        intersections.push(a[0] + ((scanY - a[1]) * (b[0] - a[0])) / (b[1] - a[1]))
      }
    }
    intersections.sort((a, b) => a - b)
    for (let i = 0; i + 1 < intersections.length; i += 2) {
      for (let x = Math.ceil(intersections[i]); x < intersections[i + 1]; x++) blendPixel(image, x, y, color)
    }
  }
}

function disc(image, cx, cy, radius, color) {
  const r2 = radius * radius
  for (let y = Math.floor(cy - radius); y <= Math.ceil(cy + radius); y++) {
    for (let x = Math.floor(cx - radius); x <= Math.ceil(cx + radius); x++) {
      const dx = x - cx
      const dy = y - cy
      if (dx * dx + dy * dy <= r2) blendPixel(image, x, y, color)
    }
  }
}

function line(image, x0, y0, x1, y1, width, color) {
  const dx = x1 - x0
  const dy = y1 - y0
  const steps = Math.max(1, Math.ceil(Math.hypot(dx, dy) * 1.25))
  for (let i = 0; i <= steps; i++) {
    const t = i / steps
    disc(image, x0 + dx * t, y0 + dy * t, width / 2, color)
  }
}

function polyline(image, points, width, color, closed = false) {
  const total = closed ? points.length : points.length - 1
  for (let i = 0; i < total; i++) line(image, ...points[i], ...points[(i + 1) % points.length], width, color)
}

function ellipse(image, cx, cy, rx, ry, color) {
  for (let y = Math.floor(cy - ry); y <= Math.ceil(cy + ry); y++) {
    for (let x = Math.floor(cx - rx); x <= Math.ceil(cx + rx); x++) {
      if (((x - cx) ** 2) / (rx ** 2) + ((y - cy) ** 2) / (ry ** 2) <= 1) blendPixel(image, x, y, color)
    }
  }
}

const s = (value) => value * SCALE
const ps = (points) => points.map(([x, y]) => [s(x), s(y)])
const rectS = (image, x0, y0, x1, y1, color) => rect(image, s(x0), s(y0), s(x1), s(y1), color)
const polygonS = (image, points, color) => polygon(image, ps(points), color)
const lineS = (image, x0, y0, x1, y1, width, color) => line(image, s(x0), s(y0), s(x1), s(y1), s(width), color)
const polylineS = (image, points, width, color, closed = false) => polyline(image, ps(points), s(width), color, closed)
const ellipseS = (image, cx, cy, rx, ry, color) => ellipse(image, s(cx), s(cy), s(rx), s(ry), color)

function lcg(seed = 0x4b495443) {
  let state = seed >>> 0
  return () => {
    state = (1664525 * state + 1013904223) >>> 0
    return state / 0x100000000
  }
}

function drawPanelDoor(image, side) {
  if (side === 'left') {
    // The door is deliberately at the stage-front edge: its tall near jamb
    // reaches the floor front, while the far edge recedes toward the back wall.
    const frame = [[7, 112], [248, 183], [248, 462], [7, 544]]
    const door = [[28, 136], [224, 194], [224, 454], [28, 516]]
    polygonS(image, frame, COLORS.woodDeep)
    polygonS(image, door, COLORS.wood)
    polylineS(image, door, 3, COLORS.ink, true)
    polygonS(image, [[47, 169], [204, 212], [204, 294], [47, 268]], COLORS.woodLight)
    polygonS(image, [[47, 286], [204, 307], [204, 426], [47, 475]], rgb('#A96331'))
    polylineS(image, [[47, 169], [204, 212], [204, 294], [47, 268]], 3, COLORS.inkSoft, true)
    polylineS(image, [[47, 286], [204, 307], [204, 426], [47, 475]], 3, COLORS.inkSoft, true)
    lineS(image, 30, 145, 30, 512, 8, COLORS.woodLight)
    lineS(image, 224, 196, 224, 451, 7, COLORS.woodDark)
    ellipseS(image, 185, 329, 8, 10, COLORS.ink)
    ellipseS(image, 184, 327, 5, 7, COLORS.brass)
  } else {
    const frame = [[2041, 112], [2000, 183], [2000, 462], [2041, 544]]
    const door = [[2028, 137], [2011, 197], [2011, 451], [2028, 516]]
    polygonS(image, frame, COLORS.woodDeep)
    polygonS(image, door, COLORS.wood)
    polylineS(image, door, 3, COLORS.ink, true)
    polygonS(image, [[2026, 168], [2015, 214], [2015, 294], [2026, 267]], COLORS.woodLight)
    polygonS(image, [[2026, 286], [2015, 307], [2015, 425], [2026, 476]], rgb('#A96331'))
    lineS(image, 2030, 145, 2030, 512, 7, COLORS.woodLight)
    lineS(image, 2010, 198, 2010, 451, 5, COLORS.woodDark)
    ellipseS(image, 2018, 330, 3.5, 7, COLORS.brass)
  }
}

function drawWindow(image, { bounds }) {
  const [x0, y0, x1, y1] = bounds
  rectS(image, x0, y0, x1, y1, COLORS.woodDeep)
  rectS(image, x0 + 5, y0 + 5, x1 - 5, y1 - 5, COLORS.wood)
  rectS(image, x0 + 12, y0 + 12, x1 - 12, y1 - 12, COLORS.inkSoft)
  // Chunky cap and sill remain inside the authoritative 168 x 168 bounds.
  // This lets furniture meet y=274 without covering a frame pixel.
  rectS(image, x0, y0, x1, y0 + 14, COLORS.woodDark)
  rectS(image, x0 + 4, y0 + 3, x1 - 4, y0 + 10, COLORS.woodLight)
  rectS(image, x0, y1 - 16, x1, y1, COLORS.woodDark)
  rectS(image, x0 + 4, y1 - 13, x1 - 4, y1 - 5, COLORS.woodLight)
  rectS(image, x0 + 77, y0 + 11, x0 + 91, y1 - 11, COLORS.woodDark)
  rectS(image, x0 + 80, y0 + 11, x0 + 88, y1 - 11, COLORS.woodLight)
  rectS(image, x0 + 11, y0 + 79, x1 - 11, y0 + 93, COLORS.woodDark)
  rectS(image, x0 + 11, y0 + 82, x1 - 11, y0 + 90, COLORS.woodLight)
}

function downsample2(source) {
  const output = blank(source.width / 2, source.height / 2)
  for (let y = 0; y < output.height; y++) {
    for (let x = 0; x < output.width; x++) {
      const sums = [0, 0, 0, 0]
      for (let oy = 0; oy < 2; oy++) {
        for (let ox = 0; ox < 2; ox++) {
          const sourceOffset = (((y * 2 + oy) * source.width) + (x * 2 + ox)) * 4
          for (let channel = 0; channel < 4; channel++) sums[channel] += source.data[sourceOffset + channel]
        }
      }
      const targetOffset = (y * output.width + x) * 4
      for (let channel = 0; channel < 4; channel++) output.data[targetOffset + channel] = Math.round(sums[channel] / 4)
    }
  }
  return output
}

function drawShell() {
  const image = blank(WIDTH * SCALE, HEIGHT * SCALE, COLORS.plaster)
  const random = lcg()

  rectS(image, 0, 0, WIDTH, HEIGHT, COLORS.plaster)
  rectS(image, 290, 32, 1995, 460, COLORS.plasterLight)
  polygonS(image, [[0, 0], [290, 32], [290, 460], [0, 544]], COLORS.plasterShade)
  polygonS(image, [[1995, 32], [2048, 0], [2048, 544], [1995, 460]], rgb('#ECD8B8'))

  // Quiet plaster marks; they add material without gradients or cast shadows.
  for (let i = 0; i < 150; i++) {
    const x = 315 + random() * 1645
    const y = 58 + random() * 360
    const length = 4 + random() * 18
    lineS(image, x, y, x + length, y + (random() - 0.5) * 2, 0.7, [193, 155, 108, 28])
  }

  // Ceiling and shallow beams converge inward toward the room centre.
  rectS(image, 0, 0, WIDTH, 22, COLORS.woodDark)
  rectS(image, 0, 22, WIDTH, 32, COLORS.wood)
  lineS(image, 0, 31, WIDTH, 31, 3, COLORS.inkSoft)
  for (const beam of [
    [[80, 0], [170, 0], [470, 45], [426, 45]],
    [[570, 0], [640, 0], [800, 45], [759, 45]],
    [[990, 0], [1058, 0], [1074, 45], [1034, 45]],
    [[1414, 0], [1484, 0], [1306, 45], [1266, 45]],
    [[1874, 0], [1964, 0], [1635, 45], [1592, 45]],
  ]) {
    polygonS(image, beam, COLORS.wood)
    polylineS(image, beam, 3, COLORS.inkSoft, true)
    lineS(image, beam[0][0] + 8, beam[0][1] + 2, beam[3][0] + 7, beam[3][1] - 3, 2, COLORS.woodLight)
  }

  // Honey timber floor, with the authoritative back/front/slab datums.
  rectS(image, 0, 460, WIDTH, 544, COLORS.floor)
  polygonS(image, [[0, 460], [290, 460], [0, 544]], COLORS.floorDark)
  polygonS(image, [[1995, 460], [2048, 460], [2048, 544]], rgb('#C97B39'))
  for (const y of [474, 489, 504, 519, 535]) {
    lineS(image, 0, y, WIDTH, y, 2, COLORS.floorDark)
    lineS(image, 0, y - 2, WIDTH, y - 2, 1, [244, 197, 119, 150])
  }
  lineS(image, 290, 460, 0, 544, 4, COLORS.inkSoft)
  lineS(image, 1995, 460, 2048, 544, 4, COLORS.inkSoft)
  rectS(image, 0, 544, WIDTH, 576, COLORS.slab)
  rectS(image, 0, 544, WIDTH, 550, COLORS.woodDeep)
  lineS(image, 0, 544, WIDTH, 544, 4, COLORS.ink)

  // Back-wall skirting and one-point side-wall returns.
  rectS(image, 290, 441, 1995, 460, COLORS.woodDark)
  rectS(image, 290, 445, 1995, 454, COLORS.wood)
  lineS(image, 290, 441, 1995, 441, 3, COLORS.inkSoft)
  polygonS(image, [[0, 514], [290, 441], [290, 460], [0, 544]], COLORS.woodDark)
  polygonS(image, [[1995, 441], [2048, 514], [2048, 544], [1995, 460]], COLORS.woodDark)

  drawPanelDoor(image, 'left')
  drawPanelDoor(image, 'right')
  for (const window of WINDOWS) drawWindow(image, window)

  const shell = downsample2(image)
  // Apply glass after antialiasing: exact #FF00FF, crisp edges, no fringe.
  for (const window of WINDOWS) for (const pane of window.panes) rect(shell, ...pane, COLORS.magenta)
  return shell
}

function loadPng(file) {
  return PNG.sync.read(fs.readFileSync(file))
}

function alphaComposite(target, source, left, top) {
  for (let sy = 0; sy < source.height; sy++) {
    const ty = top + sy
    if (ty < 0 || ty >= target.height) continue
    for (let sx = 0; sx < source.width; sx++) {
      const tx = left + sx
      if (tx < 0 || tx >= target.width) continue
      const sourceOffset = (sy * source.width + sx) * 4
      blendPixel(target, tx, ty, [source.data[sourceOffset], source.data[sourceOffset + 1], source.data[sourceOffset + 2], source.data[sourceOffset + 3]])
    }
  }
}

function asset(name) {
  return loadPng(path.join(SOURCE, name))
}

function furnish(shell) {
  const room = PNG.sync.read(PNG.sync.write(shell))
  const placements = [
    ['cream_larder_fridge-1x.png', 391, 485, 'bottom'],
    ['belfast_sink_cabinet-1x.png', 622, 485, 'bottom'],
    ['painted_base_cupboard-1x.png', 811, 485, 'bottom'],
    ['old_school_cooker-1x.png', 1063, 485, 'bottom'],
    ['scrubbed_pine_table-1x.png', 1252, 502, 'bottom'],
    ['wooden_chair_side-1x.png', 1294, 502, 'bottom'],
    ['wooden_chair_side_mirrored-1x.png', 1378, 502, 'bottom'],
    ['painted_dresser-1x.png', 1555, 485, 'bottom'],
    ['painted_base_cupboard-1x.png', 1735, 485, 'bottom'],
    ['enamel_pedal_bin-1x.png', 1945, 485, 'bottom'],
    ['painted_wall_cupboard-1x.png', 1735, 266, 'bottom'],
  ]
  for (const [name, x, datum] of placements) {
    const image = asset(name)
    alphaComposite(room, image, x, datum - image.height)
  }
  for (const [name, centre, datum] of [
    ['enamel_electric_kettle-1x.png', 874, 314],
    ['cream_toaster-1x.png', 1630, 314],
    ['stand_mixer-1x.png', 1798, 314],
  ]) {
    const image = asset(name)
    alphaComposite(room, image, Math.round(centre - image.width / 2), datum - image.height)
  }
  const keeper = loadPng(KEEPER)
  // Prime's visible sole datum is source y=316. Stop 8 is x=958.
  alphaComposite(room, keeper, 958 - 134, 502 - 316)
  return room
}

function scaleNearest(source, factor) {
  const width = Math.max(1, Math.round(source.width * factor))
  const height = Math.max(1, Math.round(source.height * factor))
  const output = blank(width, height)
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const sx = Math.min(source.width - 1, Math.floor(x / factor))
      const sy = Math.min(source.height - 1, Math.floor(y / factor))
      const sourceOffset = (sy * source.width + sx) * 4
      const targetOffset = (y * width + x) * 4
      source.data.copy(output.data, targetOffset, sourceOffset, sourceOffset + 4)
    }
  }
  return output
}

const FONT = {
  ' ': ['000','000','000','000','000','000','000'],
  '0': ['111','101','101','101','101','101','111'], '1': ['010','110','010','010','010','010','111'],
  '2': ['111','001','001','111','100','100','111'], '3': ['111','001','001','111','001','001','111'],
  '4': ['101','101','101','111','001','001','001'], '5': ['111','100','100','111','001','001','111'],
  '6': ['111','100','100','111','101','101','111'], '7': ['111','001','001','010','010','010','010'],
  '8': ['111','101','101','111','101','101','111'], '9': ['111','101','101','111','001','001','111'],
  'A': ['010','101','101','111','101','101','101'], 'B': ['110','101','101','110','101','101','110'],
  'C': ['111','100','100','100','100','100','111'], 'D': ['110','101','101','101','101','101','110'],
  'E': ['111','100','100','110','100','100','111'], 'F': ['111','100','100','110','100','100','100'],
  'G': ['111','100','100','101','101','101','111'], 'H': ['101','101','101','111','101','101','101'],
  'I': ['111','010','010','010','010','010','111'], 'J': ['001','001','001','001','101','101','111'],
  'K': ['101','101','110','100','110','101','101'], 'L': ['100','100','100','100','100','100','111'],
  'M': ['101','111','111','101','101','101','101'], 'N': ['101','111','111','111','111','111','101'],
  'O': ['111','101','101','101','101','101','111'], 'P': ['111','101','101','111','100','100','100'],
  'Q': ['111','101','101','101','111','001','001'], 'R': ['110','101','101','110','101','101','101'],
  'S': ['111','100','100','111','001','001','111'], 'T': ['111','010','010','010','010','010','010'],
  'U': ['101','101','101','101','101','101','111'], 'V': ['101','101','101','101','101','101','010'],
  'W': ['101','101','101','101','111','111','101'], 'X': ['101','101','101','010','101','101','101'],
  'Y': ['101','101','101','010','010','010','010'], 'Z': ['111','001','001','010','100','100','111'],
  ':': ['000','010','010','000','010','010','000'], '.': ['000','000','000','000','000','010','010'],
  '×': ['000','101','010','101','000','000','000'], '·': ['000','000','010','000','000','000','000'],
}

function text(image, x, y, value, size, color) {
  let cursor = x
  for (const raw of value.toUpperCase()) {
    const glyph = FONT[raw] ?? FONT[' ']
    for (let gy = 0; gy < glyph.length; gy++) {
      for (let gx = 0; gx < glyph[gy].length; gx++) {
        if (glyph[gy][gx] === '1') rect(image, cursor + gx * size, y + gy * size, cursor + (gx + 1) * size, y + (gy + 1) * size, color)
      }
    }
    cursor += size * 4
  }
}

function threeScaleSheet(furnished) {
  const sheet = blank(4400, 2140, rgb('#121B22'))
  text(sheet, 150, 35, 'KITCHEN V8 ROOM SHELL · THREE SCALE REVIEW', 7, rgb('#FAEECF'))
  text(sheet, 150, 96, '2× DETAIL · EXACT 1:1 · EXACT 12.5%', 4, rgb('#BDD5DB'))
  const doubled = scaleNearest(furnished, 2)
  alphaComposite(sheet, doubled, 152, 145)
  text(sheet, 152, 1315, '2× FULL ROOM DETAIL', 5, rgb('#FAD774'))
  alphaComposite(sheet, furnished, 152, 1385)
  text(sheet, 2240, 1390, 'EXACT 1:1 · 2048 × 576', 5, rgb('#FAD774'))
  const small = scaleNearest(furnished, 0.125)
  alphaComposite(sheet, small, 2240, 1490)
  text(sheet, 2240, 1580, 'EXACT 12.5% TOWER VIEW', 5, rgb('#FAD774'))
  text(sheet, 2240, 1645, 'FUTURE 252 PX RANGE DEFERRED · NOT DRAWN', 4, rgb('#BDD5DB'))
  text(sheet, 2240, 1700, 'PRIME KEEPER EXACT 1:1 IN FRONT OF FURNITURE', 4, rgb('#BDD5DB'))
  return sheet
}

function sha256(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
}

function pngInfo(file) {
  const image = loadPng(file)
  return { canvasPx: [image.width, image.height], bytes: fs.statSync(file).size, sha256: sha256(file) }
}

function savePng(file, image) {
  fs.writeFileSync(file, PNG.sync.write(image, { colorType: 6, inputColorType: 6 }))
}

function main() {
  fs.mkdirSync(OUT, { recursive: true })
  for (const required of [SOURCE, KEEPER, CONCEPT, REFERENCE]) {
    if (!fs.existsSync(required)) throw new Error(`missing required source: ${required}`)
  }

  const shell = drawShell()
  const furnished = furnish(shell)
  const threeScale = threeScaleSheet(furnished)
  const outputs = {
    'outputs/kitchen-v8-room-shell-empty-1x.png': shell,
    'outputs/kitchen-v8-room-furnished-1x.png': furnished,
    'outputs/kitchen-v8-room-three-scale.png': threeScale,
  }
  for (const [relative, image] of Object.entries(outputs)) savePng(path.join(__dirname, relative), image)

  const inputFiles = [
    'cream_larder_fridge-1x.png', 'belfast_sink_cabinet-1x.png', 'painted_base_cupboard-1x.png',
    'old_school_cooker-1x.png', 'scrubbed_pine_table-1x.png', 'wooden_chair_side-1x.png',
    'wooden_chair_side_mirrored-1x.png', 'painted_dresser-1x.png', 'enamel_pedal_bin-1x.png',
    'enamel_electric_kettle-1x.png', 'cream_toaster-1x.png', 'stand_mixer-1x.png', 'painted_wall_cupboard-1x.png',
  ]
  const manifest = {
    schema: 'lighthouse-keeper/kitchen-v8-room-shell@1',
    status: 'review-candidate',
    runtimeMutation: false,
    canonMutation: false,
    modulePx: [2048, 576],
    backWallLineY: 460,
    floorFrontY: 544,
    floorSlabPx: [544, 576],
    walkY: 502,
    backWallSpanPx: [290, 1995],
    windowBoundsPx: WINDOWS.map((window) => window.bounds),
    windowPanesPx: WINDOWS.flatMap((window) => window.panes),
    glassColor: '#FF00FF',
    doors: { left: 'stage-front side wall', right: 'stage-front side wall' },
    primeKeeper: { file: path.relative(ROOT, KEEPER), sha256: sha256(KEEPER), soleY: 502, stop: 8, centreX: 958 },
    furnitureAuthority: 'review/kitchen-proof-v8-assets-v1',
    standardUnitWidthPx: 126,
    futureRangeWidthPx: 252,
    futureRangeDrawn: false,
    styleSources: {
      [path.relative(ROOT, REFERENCE)]: sha256(REFERENCE),
      [path.relative(ROOT, CONCEPT)]: sha256(CONCEPT),
    },
    inputFiles: Object.fromEntries(inputFiles.map((name) => [path.relative(ROOT, path.join(SOURCE, name)), sha256(path.join(SOURCE, name))])),
    files: Object.fromEntries(Object.keys(outputs).map((relative) => [relative, pngInfo(path.join(__dirname, relative))])),
  }
  fs.writeFileSync(path.join(__dirname, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`)
  console.log(path.join(__dirname, 'outputs/kitchen-v8-room-shell-empty-1x.png'))
  console.log(path.join(__dirname, 'outputs/kitchen-v8-room-furnished-1x.png'))
  console.log(path.join(__dirname, 'outputs/kitchen-v8-room-three-scale.png'))
}

main()

#!/usr/bin/env node
/**
 * Seeds data/activity-stories/pictures.json, the shared picture library for
 * bubble stories, from Codex's immutable Prime Rear Action Choreography V2
 * catalogue and the Composer V7 symbols. Pictures are referenced, never
 * copied: every version points at an archived /keeper-review/ URL and pins
 * its SHA-256 and measured alpha bounds.
 *
 * Run once to seed. Afterwards Codex adds versions by hand (see
 * data/activity-stories/README.md) and `npm run verify:activity-stories`
 * re-measures them. Re-running keeps every version already listed.
 *
 *   node scripts/build_activity_story_library.mjs
 */

import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..')
const PACK = path.join(ROOT, 'art/drafts/claude-activity-cloud-review-pack-2026-10-20-v1')
const OUT = path.join(ROOT, 'data/activity-stories/pictures.json')
const archive = JSON.parse(fs.readFileSync(path.join(ROOT, 'review-archive/index.json'), 'utf8')).legacyPaths

const v2 = JSON.parse(fs.readFileSync(path.join(PACK, 'metadata/choreography-v2-catalogue.json'), 'utf8'))
const v7 = JSON.parse(fs.readFileSync(path.join(PACK, 'metadata/composer-v7-catalogue.json'), 'utf8')).components

/** Alpha > 8 bounding box of a 256 × 256 cell, as [x0, y0, x1, y1]. */
export function alphaBounds(file) {
  const png = PNG.sync.read(fs.readFileSync(file))
  let x0 = png.width, y0 = png.height, x1 = -1, y1 = -1
  for (let y = 0; y < png.height; y++)
    for (let x = 0; x < png.width; x++)
      if (png.data[(y * png.width + x) * 4 + 3] > 8) {
        if (x < x0) x0 = x
        if (x > x1) x1 = x
        if (y < y0) y0 = y
        if (y > y1) y1 = y
      }
  return { cell: [png.width, png.height], bounds: [x0, y0, x1 + 1, y1 + 1] }
}

function archived(url) {
  const entry = archive[url]
  if (!entry) throw new Error(`not in review-archive/index.json: ${url}`)
  return { entry, file: path.join(ROOT, entry.object) }
}

const LABELS = {
  'bbq-grill': 'Barbecue grill', 'bbq-charcoal': 'Charcoal', 'bbq-sausages': 'Sausages', 'bbq-hotdogs': 'Hot dogs', 'bbq-burgers': 'Burgers',
  'sandwich-bread': 'Bread', 'sandwich-ham': 'Ham', 'sandwich-lettuce': 'Lettuce', 'sandwich-tomato': 'Tomato', 'cooking-sandwich': 'Finished sandwich',
  'washing-plate': 'Plate', 'washing-liquid': 'Washing-up liquid', 'washing-sponge': 'Sponge', 'washing-droplets': 'Rinse water', 'washing-cutlery': 'Clean cutlery',
  'repair-toolbox': 'Toolbox', 'repair-boat-hull-patch': 'Hull patch', 'repair-hammer-nails': 'Hammer and nails', 'repair-wrench-cog': 'Wrench and cog', 'repair-rope-knot': 'Rope knot',
  'symbol-heat-curls': 'Heat curls', 'symbol-sizzle-spark': 'Sizzle spark', 'symbol-motion-ticks': 'Motion ticks', 'symbol-water-droplets': 'Water droplets', 'symbol-soap-bubbles': 'Soap bubbles', 'symbol-impact-star': 'Impact star',
  'symbol-heat-shimmer': 'Heat shimmer', 'symbol-pleasant-aroma': 'Pleasant aroma', 'symbol-foul-odour': 'Foul odour', 'symbol-electrical-arc': 'Electrical arc', 'symbol-welding-sparks': 'Welding sparks', 'symbol-exclamation-mark': 'Exclamation mark', 'symbol-question-mark': 'Question mark',
}
/** Claude's Activity Cloud Review of 20 Oct 2026 asked for these three to be redrawn. */
const REWORK = {
  'symbol-heat-shimmer': 'Reads as small flames and twins heat curls; redraw as horizontal ripples.',
  'symbol-pleasant-aroma': 'Reads as two question marks at game size; redraw as open S-wisps in cream and brass.',
  'symbol-welding-sparks': 'Blurs into the sizzle spark; needs a hot-white core and a one-sided spray.',
}

const previous = fs.existsSync(OUT) ? JSON.parse(fs.readFileSync(OUT, 'utf8')) : null
const pictures = {}

function add(id, kind, family, url, sourceSet, added) {
  const { entry, file } = archived(url)
  const { cell, bounds } = alphaBounds(file)
  const seeded = { v: 1, url, sha256: entry.sha256, cell, bounds, added, source: sourceSet, by: 'codex' }
  const old = previous?.pictures?.[id]
  pictures[id] = old ?? { kind, family, label: LABELS[id] ?? id, current: 1, versions: [seeded] }
  if (!old && REWORK[id]) pictures[id].review = { status: 'rework-requested', note: REWORK[id] }
}

for (const [id, c] of Object.entries(v2.inheritedComponents)) add(id, 'object', c.family ?? id.split('-')[0], c.src, c.sourceSet, '2026-10-19')
for (const [id, c] of Object.entries(v2.symbols)) add(id, 'mark', c.family, c.src, c.sourceSet, '2026-10-20')
for (const [id, c] of Object.entries(v7)) if (id.startsWith('symbol-')) add(id, 'mark', c.family, c.src, c.sourceSet, '2026-10-20')

const rear = v2.sequence.slice(v2.actionStartIndex).map((f) => {
  const { entry } = archived(f.src)
  return { url: f.src, sha256: entry.sha256, ms: f.durationMs }
})

const library = {
  schema: 'lighthouse-keeper/activity-picture-library@1',
  about: 'Shared picture library for bubble stories. Stories name pictures by id; each picture keeps every version, and `current` says which one stories use. See data/activity-stories/README.md.',
  keeper: {
    note: 'Approved Prime rear-work loop (24 frames). Immutable: never edited here.',
    rearWork: previous?.keeper?.rearWork ?? rear,
  },
  pictures: Object.fromEntries(Object.entries(pictures).sort(([a], [b]) => a.localeCompare(b))),
}

fs.mkdirSync(path.dirname(OUT), { recursive: true })
fs.writeFileSync(OUT, JSON.stringify(library, null, 2) + '\n')
console.log(`wrote ${path.relative(ROOT, OUT)}: ${Object.keys(library.pictures).length} pictures, ${library.keeper.rearWork.length} keeper frames`)

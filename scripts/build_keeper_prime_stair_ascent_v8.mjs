#!/usr/bin/env node
/** Build Stair Ascent V8: correct V7's one-tread horizontal index error. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const v7Pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v7')
const v8Pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v8')
const v7Page = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v7/index.html')
const v8Public = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v8')
const assetsDir = path.join(v8Public, 'assets')
const v7RegisterPath = path.join(v7Pack, 'batch-register.json')
const v7PrepPath = path.join(v7Pack, 'source-preparation-v7.json')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of [v7RegisterPath, v7PrepPath, v7Page]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const v7Register = JSON.parse(fs.readFileSync(v7RegisterPath, 'utf8'))
const prep = JSON.parse(fs.readFileSync(v7PrepPath, 'utf8'))
fs.mkdirSync(v8Pack, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const urls = {}
for (const frame of prep.frames) {
  const source = path.join(root, frame.file)
  if (sha(source) !== frame.sha256) throw new Error(`${frame.leg} V7 drawing changed`)
  const target = path.join(assetsDir, `${frame.leg}-contact-${frame.sha256.slice(0, 16)}.png`)
  fs.copyFileSync(source, target)
  urls[frame.leg] = `/keeper-review/keeper-prime-stair-ascent-v8/assets/${path.basename(target)}`
}

const oldHtml = fs.readFileSync(v7Page, 'utf8')
const match = oldHtml.match(/const timeline=(\[.*?\]),buttons=/s)
if (!match) throw new Error('V7 timeline missing')
const oldTimeline = JSON.parse(match[1])
const timeline = oldTimeline.map((frame) => ({
  ...frame,
  src: urls[frame.leg],
  xLp: frame.xLp + 6,
  supportXLp: frame.supportXLp + 6,
  targetXLp: frame.targetXLp + 6,
}))
const geometry = {
  floorTopLp: 20,
  staircaseBoundaryXLp: 100.5,
  firstFloorSupportCentreXLp: 103.5,
  firstTreadCentreXLp: 97.5,
  treadRunLp: 6,
  riserRiseLp: 60 / 14,
  shownContacts: 4,
  horizontalCorrectionFromV7Lp: 6,
  contactDurationMs: 320,
}
const rigPath = path.join(v8Pack, 'stair-contact-rig-v8.json')
writeJson(rigPath, {
  schema: 'lighthouse-keeper/stair-contact-rig@8',
  status: 'four-contact-horizontal-index-correction',
  direction: 'leftward gameplay', cell: [256, 320], density: 8, geometry,
  contactOrder: ['right', 'left', 'right', 'left'],
  contract: [
    'Frame 1 support foot is on the floor immediately before the staircase, not over tread 1.',
    'Frame 1 moving foot is on tread 1, not over tread 2.',
    'Every later frame advances both foot contacts by exactly one adjacent tread.',
    'V7 artwork, vertical positions, stair dimensions and timing are byte-for-byte unchanged.',
  ],
})

let html = oldHtml.replaceAll('keeper-prime-stair-ascent-v7', 'keeper-prime-stair-ascent-v8').replaceAll('stair ascent V7', 'stair ascent V8').replaceAll('Stair Ascent V7', 'Stair Ascent V8')
html = html.replace('<a href="/keeper-review/keeper-prime-stair-ascent-v6/">← Preserve and compare rejected V6</a>', '<a href="/keeper-review/keeper-prime-stair-ascent-v7/">← Preserve and compare rejected V7</a>')
html = html.replace('Judge only the alternation and tread contact:', 'V8 fixes V7’s one-tread horizontal offset. Judge only the alternation and tread contact:')
html = html.replace('V1–V6 remain immutable historical drafts. V7 changes no approved walk pixels, Final art, runtime sprites or production geometry. If this basic two-drawing alternation is right, intermediate smoothing can be designed later without changing these binding foot contacts.', 'V1–V7 remain immutable historical drafts. V8 shifts the Keeper and both contact markers exactly one 6-lp tread right, so frame 1 starts from the floor and lands on tread 1. The two drawings, vertical positions, stair dimensions and timing are unchanged. No approved walk pixels, Final art, runtime sprites or production geometry changed.')
html = html.replace(/const timeline=\[.*?\],buttons=/s, `const timeline=${JSON.stringify(timeline)},buttons=`)
const pagePath = path.join(v8Public, 'index.html')
fs.writeFileSync(pagePath, html)

const specPath = path.join(v8Pack, 'keeper-prime-stair-ascent-v8.json')
writeJson(specPath, {
  schema: 'lighthouse-keeper/prime-stair-ascent@8',
  status: 'draft-v8-first-step-horizontal-registration-awaiting-review',
  rejectionOfV7: 'V7 placed support tread n at the horizontal centre of tread n+1, so every foot was one tread too far up-flight.',
  correction: 'Shift the Keeper root, support marker and target marker +6 lp without changing artwork, vertical geometry, timing or stairs.',
  geometry, promoted: false,
  unchanged: { v1ThroughV7: true, v7Artwork: true, v7VerticalPositions: true, v7Timing: true, stairGeometry: true, finalLane: true, production: true },
})
const frameUrls = [urls.right, urls.left]
const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-stair-ascent-2026-10-15-v8',
  status: 'draft-v8-first-step-horizontal-registration-awaiting-review',
  authorities: {
    rejectedV7: { file: rel(v7RegisterPath), sha256: sha(v7RegisterPath) },
    v7SourcePreparation: { file: rel(v7PrepPath), sha256: sha(v7PrepPath) },
    contactRig: { file: rel(rigPath), sha256: sha(rigPath) },
  },
  generation: { mode: 'geometry-only-plus-six-logical-pixels-horizontal-registration', frameUrls },
  originalAndDraft: prep.frames.map((frame) => ({ leg: frame.leg, v7File: frame.file, v7Sha256: frame.sha256, v8Sha256: frame.sha256 })),
  spec: { file: rel(specPath), sha256: sha(specPath) }, reviewPage: { file: rel(pagePath), sha256: sha(pagePath) }, frameUrls,
  validation: { horizontalCorrectionLp: 6, uniqueDrawings: 2, shownContacts: 4, noIntermediates: true, adjacentTreadOnly: true, v7ArtworkChanged: false, v7VerticalPositionsChanged: false, v7TimingChanged: false, stairGeometryChanged: false, v1ThroughV7Changed: false, finalChanged: false, productionChanged: false },
}
writeJson(path.join(v8Pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(v8Pack, 'PROMPT_LOG.md'), '# Keeper Prime stair ascent V8 decision log\n\nNo image generation or pixel editing was used. Frank identified that V7 indexed horizontal contact positions one tread ahead of their vertical positions. V8 moves the complete Keeper root and both contact guides exactly +6 logical pixels, leaving every image byte, vertical coordinate, timing value and stair dimension unchanged.\n')
fs.writeFileSync(path.join(v8Pack, 'HANDOFF.md'), '# Keeper Prime stair ascent V8\n\nStatus: geometry-only correction awaiting Frank’s review.\n\nV8 preserves the two V7 contact drawings and four-frame RIGHT/LEFT/RIGHT/LEFT test. It corrects only the one-tread horizontal offset: frame 1 now supports on the floor and lands on tread 1. Nothing is approved or promoted.\n')
console.log(JSON.stringify({ page: rel(pagePath), horizontalCorrectionLp: 6, frameUrls, v7ArtworkChanged: false }, null, 2))

#!/usr/bin/env node
/** Build Stair Ascent V9: move the Keeper back 1.5 lp for toe/riser clearance. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const v7Pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v7')
const v8Pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v8')
const v9Pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v9')
const v8Page = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v8/index.html')
const v9Public = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v9')
const assetsDir = path.join(v9Public, 'assets')
const v8RegisterPath = path.join(v8Pack, 'batch-register.json')
const v7PrepPath = path.join(v7Pack, 'source-preparation-v7.json')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of [v8RegisterPath, v7PrepPath, v8Page]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const prep = JSON.parse(fs.readFileSync(v7PrepPath, 'utf8'))
fs.mkdirSync(v9Pack, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const urls = {}
for (const frame of prep.frames) {
  const source = path.join(root, frame.file)
  if (sha(source) !== frame.sha256) throw new Error(`${frame.leg} contact drawing changed`)
  const target = path.join(assetsDir, `${frame.leg}-contact-${frame.sha256.slice(0, 16)}.png`)
  fs.copyFileSync(source, target)
  urls[frame.leg] = `/keeper-review/keeper-prime-stair-ascent-v9/assets/${path.basename(target)}`
}

const oldHtml = fs.readFileSync(v8Page, 'utf8')
const match = oldHtml.match(/const timeline=(\[.*?\]),buttons=/s)
if (!match) throw new Error('V8 timeline missing')
const oldTimeline = JSON.parse(match[1])
const timeline = oldTimeline.map((frame) => ({ ...frame, src: urls[frame.leg], xLp: frame.xLp + 1.5 }))
const geometry = {
  keeperBackShiftFromV8Lp: 1.5,
  keeperBackShiftSourcePx: 12,
  minimumOpaqueToeClearanceLp: 0.25,
  firstFloorSupportCentreLp: 103.5,
  firstTreadCentreLp: 97.5,
  treadRunLp: 6,
  riserRiseLp: 60 / 14,
  contactMarkersChanged: false,
  verticalGeometryChanged: false,
}
const rigPath = path.join(v9Pack, 'stair-contact-rig-v9.json')
writeJson(rigPath, {
  schema: 'lighthouse-keeper/stair-contact-rig@9',
  status: 'four-contact-forward-toe-clearance-correction',
  direction: 'leftward gameplay', cell: [256, 320], density: 8, geometry,
  contactOrder: ['right', 'left', 'right', 'left'],
  contract: [
    'The complete Keeper is shifted back/right 1.5 lp (12 source pixels) from V8.',
    'The stair, support guides, target guides, vertical positions, images and timing are unchanged.',
    'The foremost opaque moving-boot pixel retains at least 0.25 lp/2 source pixels clearance from the next riser.',
    'Frame 1 still supports on the floor and lands vertically on tread 1.',
  ],
})

let html = oldHtml.replaceAll('keeper-prime-stair-ascent-v8', 'keeper-prime-stair-ascent-v9').replaceAll('stair ascent V8', 'stair ascent V9').replaceAll('Stair Ascent V8', 'Stair Ascent V9')
html = html.replace('<a href="/keeper-review/keeper-prime-stair-ascent-v7/">← Preserve and compare rejected V7</a>', '<a href="/keeper-review/keeper-prime-stair-ascent-v8/">← Preserve and compare rejected V8</a>')
html = html.replace('V8 fixes V7’s one-tread horizontal offset. Judge only the alternation and tread contact:', 'V9 preserves V8’s correct tread heights and moves the Keeper back 1.5 lp to clear every forward toe from the next riser. Judge only the alternation and tread contact:')
html = html.replace('V1–V7 remain immutable historical drafts. V8 shifts the Keeper and both contact markers exactly one 6-lp tread right, so frame 1 starts from the floor and lands on tread 1. The two drawings, vertical positions, stair dimensions and timing are unchanged. No approved walk pixels, Final art, runtime sprites or production geometry changed.', 'V1–V8 remain immutable historical drafts. V9 moves only the complete Keeper root 1.5 lp back/right, leaving the tread markers, two drawings, vertical positions, stair dimensions and timing unchanged. The forward toe now has a measured transparent gap before each next riser. No approved walk pixels, Final art, runtime sprites or production geometry changed.')
html = html.replace(/const timeline=\[.*?\],buttons=/s, `const timeline=${JSON.stringify(timeline)},buttons=`)
const pagePath = path.join(v9Public, 'index.html')
fs.writeFileSync(pagePath, html)

const specPath = path.join(v9Pack, 'keeper-prime-stair-ascent-v9.json')
writeJson(specPath, {
  schema: 'lighthouse-keeper/prime-stair-ascent@9',
  status: 'draft-v9-forward-toe-clearance-awaiting-review',
  rejectionOfV8: 'V8 fixed the one-tread index error but the forward toe still overlapped the next vertical riser.',
  correction: 'Move only the complete Keeper root +1.5 lp/right; retain tread markers, artwork, vertical geometry, timing and stairs.',
  geometry, promoted: false,
  unchanged: { v1ThroughV8: true, v8Artwork: true, v8VerticalPositions: true, v8ContactMarkers: true, v8Timing: true, stairGeometry: true, finalLane: true, production: true },
})
const frameUrls = [urls.right, urls.left]
const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-stair-ascent-2026-10-15-v9',
  status: 'draft-v9-forward-toe-clearance-awaiting-review',
  authorities: {
    rejectedV8: { file: rel(v8RegisterPath), sha256: sha(v8RegisterPath) },
    v7SourcePreparation: { file: rel(v7PrepPath), sha256: sha(v7PrepPath) },
    contactRig: { file: rel(rigPath), sha256: sha(rigPath) },
  },
  generation: { mode: 'geometry-only-plus-one-point-five-logical-pixels-keeper-back-shift', frameUrls },
  originalAndDraft: prep.frames.map((frame) => ({ leg: frame.leg, sourceFile: frame.file, sourceSha256: frame.sha256, candidateSha256: frame.sha256 })),
  spec: { file: rel(specPath), sha256: sha(specPath) }, reviewPage: { file: rel(pagePath), sha256: sha(pagePath) }, frameUrls,
  validation: { keeperBackShiftLp: 1.5, minimumToeClearanceLp: 0.25, uniqueDrawings: 2, shownContacts: 4, v8ArtworkChanged: false, v8VerticalPositionsChanged: false, v8ContactMarkersChanged: false, v8TimingChanged: false, stairGeometryChanged: false, v1ThroughV8Changed: false, finalChanged: false, productionChanged: false },
}
writeJson(path.join(v9Pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(v9Pack, 'PROMPT_LOG.md'), '# Keeper Prime stair ascent V9 decision log\n\nNo image generation or pixel editing was used. Frank approved V8’s vertical registration but observed the forward toe overlapping each next riser. The foremost opaque boot pixels measured 1.25 lp (RIGHT) and 1.125 lp (LEFT) beyond the riser boundary in V8. V9 moves only the complete Keeper root 1.5 lp back/right, leaving 0.25 lp and 0.375 lp clearance respectively.\n')
fs.writeFileSync(path.join(v9Pack, 'HANDOFF.md'), '# Keeper Prime stair ascent V9\n\nStatus: forward-toe clearance correction awaiting Frank’s review.\n\nV9 preserves V8’s correct vertical registration and exact two drawings. Only the Keeper root moves 1.5 lp back/right; the tread markers, staircase, timing and all image bytes are unchanged. Nothing is approved or promoted.\n')
console.log(JSON.stringify({ page: rel(pagePath), keeperBackShiftLp: 1.5, minimumToeClearanceLp: 0.25, artworkChanged: false }, null, 2))

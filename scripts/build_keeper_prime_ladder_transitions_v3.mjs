#!/usr/bin/env node
/** Build Ladder Transition V3: complete ladder plus alpha-opaque Keeper art. */

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const v2Set = 'keeper-prime-ladder-transitions-v2'
const set = 'keeper-prime-ladder-transitions-v3'
const v2Pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v2')
const pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v3')
const framesDir = path.join(pack, 'drafts/frames')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const v2SpecFile = path.join(v2Pack, 'keeper-prime-ladder-transitions-v2.json')
const v2RegisterFile = path.join(v2Pack, 'batch-register.json')
const v2PageFile = path.join(root, 'public/keeper-review', v2Set, 'index.html')
const specFile = path.join(pack, 'keeper-prime-ladder-transitions-v3.json')
const pageFile = path.join(publicDir, 'index.html')
const threshold = 128

const read = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = file => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => {
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n')
}

for (const file of [v2SpecFile, v2RegisterFile, v2PageFile]) if (!fs.existsSync(file)) throw new Error(`missing ${file}`)
fs.mkdirSync(framesDir, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const v2Spec = read(v2SpecFile)
const v2Register = read(v2RegisterFile)
const spec = structuredClone(v2Spec)
spec.set = set
spec.layering = {
  orderBackToFront: ['ladder', 'keeper', 'floor', 'door', 'guides'],
  keeperAlphaMode: 'binary-threshold-128-after-registration',
  ladderPixelsSuppressed: false,
  purpose: 'make Keeper paint opaque while preserving all genuine transparent gaps and every ladder pixel',
}
spec.opacity = {
  threshold,
  operation: 'alpha >= 128 becomes 255; alpha < 128 becomes 0; retained RGB is unchanged',
  appliesTo: 'all 29 unique Keeper review frames',
}

const urlMap = new Map()
const publishedAssets = []
const alphaNormalization = []
for (const entry of v2Register.publishedAssets) {
  const source = path.join(root, entry.source)
  if (!fs.existsSync(source) || sha(source) !== entry.sourceSha256) throw new Error(`V2 source drift: ${entry.source}`)
  const input = PNG.sync.read(fs.readFileSync(source))
  const output = new PNG({ width: input.width, height: input.height })
  const before = { transparent: 0, semiTransparent: 0, opaque: 0 }
  const after = { transparent: 0, opaque: 0 }
  for (let offset = 0; offset < input.data.length; offset += 4) {
    const alpha = input.data[offset + 3]
    if (alpha === 0) before.transparent++
    else if (alpha === 255) before.opaque++
    else before.semiTransparent++
    if (alpha >= threshold) {
      output.data[offset] = input.data[offset]
      output.data[offset + 1] = input.data[offset + 1]
      output.data[offset + 2] = input.data[offset + 2]
      output.data[offset + 3] = 255
      after.opaque++
    } else {
      output.data[offset] = 0
      output.data[offset + 1] = 0
      output.data[offset + 2] = 0
      output.data[offset + 3] = 0
      after.transparent++
    }
  }
  const oldBase = path.basename(entry.published, '.png')
  const draft = path.join(framesDir, `${oldBase}-opaque.png`)
  fs.writeFileSync(draft, PNG.sync.write(output))
  const digest = sha(draft)
  const publicName = `${oldBase}-opaque-${digest.slice(0, 16)}.png`
  const published = path.join(assetsDir, publicName)
  fs.copyFileSync(draft, published)
  const url = `/keeper-review/${set}/assets/${publicName}`
  urlMap.set(entry.url, url)
  publishedAssets.push({
    source: rel(source),
    sourceSha256: entry.sourceSha256,
    draft: rel(draft),
    draftSha256: digest,
    published: rel(published),
    url,
    bytes: fs.statSync(published).size,
    changeScope: 'alpha-only threshold after registration',
  })
  alphaNormalization.push({
    source: rel(source),
    sourceSha256: entry.sourceSha256,
    draft: rel(draft),
    draftSha256: digest,
    pixels: [input.width, input.height],
    threshold,
    before,
    after,
    retainedRgbChangedPixels: 0,
  })
}

for (const route of Object.values(spec.routes)) for (const frame of route.frames) {
  const nextUrl = urlMap.get(frame.src)
  if (!nextUrl) throw new Error(`unmapped V2 URL: ${frame.src}`)
  frame.src = nextUrl
  delete frame.ladderOcclusion
}
writeJson(specFile, spec)

let html = fs.readFileSync(v2PageFile, 'utf8')
html = html.replaceAll('Keeper Prime ladder transitions V2', 'Keeper Prime ladder transitions V3')
html = html.replace(
  'Timing and layering correction of V1: faster turns, slower climbing, and no central-rung flash through the Keeper. Every character pixel is unchanged.',
  'Opacity correction of V2: the complete ladder now remains present in every frame, while the Keeper alone is alpha-hardened after registration. Timing and geometry are unchanged.',
)
html = html.replace(
  'Four exact mirrored left/right gait cycles close the storey without phase remainder. Turns now run at 20 fps and climbing at 6.67 fps; V1 artwork and geometry are unchanged.',
  'Four exact mirrored left/right gait cycles close the storey without phase remainder. Turns remain 20 fps and climbing 6.67 fps. No ladder pixel is hidden by a review mask.',
)
html = html.replace('.rungOccluder{position:absolute;background:linear-gradient(#173440,#102833);background-repeat:no-repeat;z-index:3}', '')
const v2Architecture = "function architecture(world,scale,frame){world.innerHTML='';const add=(className,left,top,width,height)=>{const e=document.createElement('div');e.className=className;e.style.left=px(left,scale);e.style.top=px(top,scale);e.style.width=px(width,scale);e.style.height=px(height,scale);world.append(e);return e};const offset=frame.ladderOffsetLp||0;add('rail',95,4,1.5,112);add('rail',111.5,4,1.5,112);for(let y=3.5+offset;y<=116;y+=7.5)add('rung',95,y,18,1);if(frame.ladderOcclusion==='central-body'){const top=frame.rootYLp-38,shield=add('rungOccluder',frame.xLp-6,top,12,38);shield.style.backgroundSize=`100% ${132*scale}px`;shield.style.backgroundPosition=`0 ${-top*scale}px`}add('floor',0,116,172,16);add('floor',0,56,95,4);add('floor',113,56,59,4);if(routeId==='approach'||routeId==='full')add('door',8,68,24,48);if(routeId==='exit'||routeId==='full')add('door',158,8,14,48)}"
const v3Architecture = "function architecture(world,scale,frame){world.innerHTML='';const add=(className,left,top,width,height)=>{const e=document.createElement('div');e.className=className;e.style.left=px(left,scale);e.style.top=px(top,scale);e.style.width=px(width,scale);e.style.height=px(height,scale);world.append(e);return e};const offset=frame.ladderOffsetLp||0;add('rail',95,4,1.5,112);add('rail',111.5,4,1.5,112);for(let y=3.5+offset;y<=116;y+=7.5)add('rung',95,y,18,1);add('floor',0,116,172,16);add('floor',0,56,95,4);add('floor',113,56,59,4);if(routeId==='approach'||routeId==='full')add('door',8,68,24,48);if(routeId==='exit'||routeId==='full')add('door',158,8,14,48)}"
if (!html.includes(v2Architecture)) throw new Error('V2 architecture function changed')
html = html.replace(v2Architecture, v3Architecture)
html = html.replace(
  '<section class="metrics"><article><b>20 fps</b>faster turn cadence</article>',
  '<section class="metrics"><article><b>Opaque Keeper</b>alpha ≥128 hardened after resize</article><article><b>Complete ladder</b>zero suppressed rung pixels</article><article><b>20 fps</b>faster turn cadence</article>',
)
html = html.replace(
  'First inspect the bottom turn: central rungs must stay behind the Keeper with no flash, while both side rails remain visible. Then judge the faster turn, the slower climb, the uninterrupted floor crossing and the top dismount. Hand/foot rung contact remains the accepted V1 tolerance.',
  'First inspect the bottom turn and climbing loop: the ladder must remain structurally complete with rungs visible through genuine gaps, but never bleed through painted Keeper pixels. Timing, roots, geometry and the accepted hand/foot rung tolerance are unchanged from V2.',
)
html = html.replace(/const SPEC=.*?;\nconst routeSelect=/s, `const SPEC=${JSON.stringify(spec)};\nconst routeSelect=`)
fs.writeFileSync(pageFile, html)

fs.writeFileSync(path.join(pack, 'HANDOFF.md'), `# Keeper Prime ladder transitions V3

V3 removes V2's rectangular rung occluder completely. Every ladder rail and rung is drawn in every frame. Each of the 29 unique Keeper review images is instead alpha-normalized after registration: alpha >= ${threshold} becomes fully opaque, alpha < ${threshold} becomes fully transparent, and RGB is unchanged for every retained pixel. V2 timing, frame order, roots, geometry and accepted hand/foot-to-rung tolerance are exact. Nothing is promoted.

Review: \`/keeper-review/${set}/\`.
`)

const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-ladder-transitions-2026-10-16-v3',
  status: 'draft-awaiting-visual-review',
  purpose: 'Keep the ladder structurally complete and make only the registered Keeper art opaque.',
  authorities: {
    v2Spec: { file: rel(v2SpecFile), sha256: sha(v2SpecFile) },
    v2Register: { file: rel(v2RegisterFile), sha256: sha(v2RegisterFile) },
    v2Page: { file: rel(v2PageFile), sha256: sha(v2PageFile) },
  },
  alphaNormalization,
  spec: { file: rel(specFile), sha256: sha(specFile) },
  reviewPage: { file: rel(pageFile), sha256: sha(pageFile), publicReview: `/keeper-review/${set}/`, preloadsAllUniqueFrames: true },
  publishedAssets,
  changes: {
    v2RungOccluderRemoved: true,
    ladderPixelsSuppressed: false,
    keeperRgbChanged: false,
    keeperAlphaThreshold: threshold,
    rootOrGeometryChanged: false,
    timingChangedFromV2: false,
    rungContactChanged: false,
  },
  validation: { productionChanged: false, runtimeChanged: false, finalChanged: false },
  approvalBoundary: { candidateApproved: false, finalLaneEntryAllowed: false, productionPromotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and ${rel(publicDir)}; V1/V2, approved sources, Final, runtime and production remain unchanged.`,
}
writeJson(path.join(pack, 'batch-register.json'), register)

console.log(JSON.stringify({
  page: rel(pageFile),
  uniqueFrames: publishedAssets.length,
  threshold,
  timing: spec.timing,
  ladderPixelsSuppressed: false,
}, null, 2))

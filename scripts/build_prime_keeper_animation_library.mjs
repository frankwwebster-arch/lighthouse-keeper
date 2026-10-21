import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')

function read(relative) {
  return fs.readFileSync(path.join(root, relative), 'utf8')
}

function readJson(relative) {
  return JSON.parse(read(relative))
}

function embeddedJson(relative, name) {
  const source = read(relative)
  const declarationMarker = `const ${name}=`
  const assignmentMarker = `${name}=`
  const start = source.indexOf(declarationMarker) >= 0
    ? source.indexOf(declarationMarker)
    : source.indexOf(assignmentMarker)
  const marker = source.startsWith(declarationMarker, start) ? declarationMarker : assignmentMarker
  if (start < 0) throw new Error(`${relative} has no ${marker}`)
  const valueStart = start + marker.length
  let depth = 0
  let quoted = false
  let escaped = false
  for (let index = valueStart; index < source.length; index += 1) {
    const char = source[index]
    if (quoted) {
      if (escaped) escaped = false
      else if (char === '\\') escaped = true
      else if (char === '"') quoted = false
      continue
    }
    if (char === '"') quoted = true
    else if (char === '{' || char === '[') depth += 1
    else if (char === '}' || char === ']') {
      depth -= 1
      if (depth === 0) return JSON.parse(source.slice(valueStart, index + 1))
    }
  }
  throw new Error(`${relative} has an unterminated ${name} value`)
}

function frames(entries, defaultDurationMs = 100) {
  return entries.map((entry, index) => typeof entry === 'string'
    ? { src: entry, durationMs: defaultDurationMs, label: `Frame ${index + 1}` }
    : {
        src: entry.src,
        durationMs: entry.durationMs ?? defaultDurationMs,
        label: entry.label ?? entry.pose ?? entry.phase ?? `Frame ${index + 1}`,
        phase: entry.phase,
        flipX: Boolean(entry.flipX),
      })
}

function pingPong(entries) {
  return [...entries, ...entries.slice(0, -1).reverse()]
}

function clip(details, entries) {
  if (!entries.length || entries.some((entry) => !entry.src)) throw new Error(`${details.id} has invalid frames`)
  const base = details.reviewUrl.endsWith('/') ? details.reviewUrl : `${details.reviewUrl}/`
  return {
    ...details,
    frames: entries.map((entry) => ({
      ...entry,
      src: entry.src.startsWith('/') ? entry.src : `${base}${entry.src}`,
    })),
  }
}

const walkHtml = 'public/keeper-review/keeper-prime-walk-v7/index.html'
const walkSources = embeddedJson(walkHtml, 'frames')
const walkLabels = embeddedJson(walkHtml, 'labels')
const walkFrames = walkSources.map((src, index) => ({ src, durationMs: 100, label: walkLabels[index] }))

const stopFrames = frames(embeddedJson('public/keeper-review/keeper-prime-stop-walk-stop-v2/index.html', 'route'))
const frontSideFrames = frames(embeddedJson('public/keeper-review/keeper-prime-turn-front-side-v1/index.html', 'frames'), 62.5)
const sideBackFrames = frames(embeddedJson('public/keeper-review/keeper-prime-turn-side-back-v10/index.html', 'frames'), 62.5)
const stairAscentFrames = frames(embeddedJson('public/keeper-review/keeper-prime-stair-ascent-v16/index.html', 'timeline'), 110)
const stairTransitionSpec = embeddedJson('public/keeper-review/keeper-prime-stair-transitions-v6/index.html', 'SPEC')
const stairDescentSpec = embeddedJson('public/keeper-review/keeper-prime-stair-descent-v2/index.html', 'SPEC')
const ladderSpec = embeddedJson('public/keeper-review/keeper-prime-ladder-transitions-v5/index.html', 'SPEC')
const sideRight = readJson('public/keeper-review/keeper-prime-sit-stand-side-v2/route.json')
const sideLeft = readJson('review-archive/objects/5c/5cb0f5dc44a84a83e7c55a9ad573cc5c09afb4a7719c753c896cc9a5bfb5fdc6.json')
const sitFront = readJson('review-archive/objects/8b/8bca3cc27af7c341cb86f8770513fd2128e416e46c5c7698c4e0985fb5dd6c8c.json')
const sitBack = readJson('review-archive/objects/b1/b117b53cf7f849783b3a8348e8bd2b01296ca4068607153746e527ca5bad3e96.json')
const darts = readJson('review-archive/objects/c9/c9ae9f4eb70f36f83a722a6f0d28baa6926d2657bad0eaaf76b5fe570ca62240.json')
const rearAction = readJson('public/keeper-review/keeper-prime-rear-action-sequence-v1/catalogue.json')
const runtimeBankPath = path.join(root, 'data/keeper_prime_runtime_bank.json')
const runtimeBank = fs.existsSync(runtimeBankPath) ? readJson('data/keeper_prime_runtime_bank.json') : { assets: [] }

const common = { approvedBy: 'Frank', productionState: 'Approved review authority · not yet promoted to runtime' }
const clips = [
  clip({ ...common, id: 'walk-v7', title: 'Walk cycle', version: 'Prime Walk V7', category: 'Locomotion', approvedOn: '2026-10-14', scope: 'Eight-phase side walk; Prime locomotion authority.', startPose: 'walking-side-right', endPose: 'walking-side-right', loop: true, reviewUrl: '/keeper-review/keeper-prime-walk-v7/' }, walkFrames),
  clip({ ...common, id: 'stop-walk-stop-v2', title: 'Stop → walk → stop', version: 'Prime Stop–Walk–Stop V2', category: 'Locomotion', approvedOn: '2026-10-14', scope: 'Approved acceleration, walk cadence and exact reverse deceleration.', startPose: 'standing-side-right', endPose: 'standing-side-right', loop: false, reviewUrl: '/keeper-review/keeper-prime-stop-walk-stop-v2/' }, stopFrames),
  clip({ ...common, id: 'turn-front-side-v1', title: 'Front ↔ side turn', version: 'Prime Turn Front–Side V1', category: 'Turns', approvedOn: '2026-10-13', scope: 'Approved turn with one accepted minor 45° cadence limitation.', startPose: 'standing-front', endPose: 'standing-side-right', loop: false, reviewUrl: '/keeper-review/keeper-prime-turn-front-side-v1/' }, frontSideFrames),
  clip({ ...common, id: 'turn-side-back-v10', title: 'Side ↔ back turn', version: 'Prime Turn Side–Back V10', category: 'Turns', approvedOn: '2026-10-14', scope: 'Exact nine-frame V9 turn authority, hash-pinned by the V10 review.', startPose: 'standing-side-right', endPose: 'standing-back', loop: false, reviewUrl: '/keeper-review/keeper-prime-turn-side-back-v10/' }, sideBackFrames),
  clip({ ...common, id: 'stair-ascent-v16', title: 'Stair ascent', version: 'Prime Stair Ascent V16 · V17 approval', category: 'Circulation', approvedOn: '2026-10-16', scope: 'Four-drawing, 27-frame climb over the fixed fourteen-riser flight.', startPose: 'stair-lower-contact', endPose: 'stair-upper-contact', loop: false, reviewUrl: '/keeper-review/keeper-prime-stair-ascent-v16/' }, stairAscentFrames),
  clip({ ...common, id: 'stair-descent-v2', title: 'Stair descent', version: 'Prime Stair Descent V2', category: 'Circulation', approvedOn: '2026-10-16', scope: 'Approved descent with the visible overstride accepted until final balustrade scenery.', startPose: 'standing-upper-landing', endPose: 'standing-lower-floor', loop: false, reviewUrl: '/keeper-review/keeper-prime-stair-descent-v2/' }, frames(stairDescentSpec.routes.descentOnly.frames)),
  clip({ ...common, id: 'stair-route-v6', title: 'Complete stair route', version: 'Prime Stair Transitions V6', category: 'Circulation', approvedOn: '2026-10-16', scope: 'Approved door-to-door route and door-hidden scale handoff.', startPose: 'hidden-lower-door', endPose: 'hidden-upper-door', loop: false, reviewUrl: '/keeper-review/keeper-prime-stair-transitions-v6/' }, frames(stairTransitionSpec.routes.fullFlow.frames)),
  clip({ ...common, id: 'ladder-route-v5', title: 'Complete ladder route', version: 'Prime Ladder Transitions V5', category: 'Circulation', approvedOn: '2026-10-16', scope: 'All 111 Keeper route frames approved; V6 corrected only the door presentation.', startPose: 'hidden-lower-door', endPose: 'hidden-upper-door', loop: false, reviewUrl: '/keeper-review/keeper-prime-ladder-transitions-v6/' }, frames(ladderSpec.routes.full.frames)),
  clip({ ...common, id: 'sit-side-right-v6', title: 'Sit / stand · side right', version: 'Prime Sit–Stand Side V6', category: 'Sit & stand', approvedOn: '2026-10-17', scope: 'Six approved action poses and measured side-right seat geometry.', startPose: 'standing-side-right', endPose: 'standing-side-right', loop: true, reviewUrl: '/keeper-review/keeper-prime-sit-stand-side-v6/' }, pingPong(frames(sideRight.action.frames, 125))),
  clip({ ...common, id: 'sit-side-left-v1', title: 'Sit / stand · side left', version: 'Prime Sit–Stand Side-left V1', category: 'Sit & stand', approvedOn: '2026-10-17', scope: 'Exact mirrored six-pose side-left authority.', startPose: 'standing-side-left', endPose: 'standing-side-left', loop: true, reviewUrl: '/keeper-review/keeper-prime-sit-stand-side-left-v1/' }, pingPong(frames(sideLeft.action.frames, 125))),
  clip({ ...common, id: 'sit-front-v4', title: 'Sit / stand · front', version: 'Prime Sit–Stand Front V4', category: 'Sit & stand', approvedOn: '2026-10-18', scope: 'Approved six-pose front action with locked elbow span.', startPose: 'standing-front', endPose: 'standing-front', loop: true, reviewUrl: '/keeper-review/keeper-prime-sit-stand-front-v4/' }, pingPong(frames(sitFront.action.frames, 125))),
  clip({ ...common, id: 'sit-back-v2', title: 'Sit / stand · back', version: 'Prime Sit–Stand Back V2', category: 'Sit & stand', approvedOn: '2026-10-18', scope: 'Approved six-pose rear action using only Prime palette authorities.', startPose: 'standing-back', endPose: 'standing-back', loop: true, reviewUrl: '/keeper-review/keeper-prime-sit-stand-back-v2/' }, pingPong(frames(sitBack.action.frames, 125))),
  clip({ ...common, id: 'darts-context-v8', title: 'Play darts', version: 'Prime Darts Context V8', category: 'Activities', approvedOn: '2026-10-17', scope: 'Approved contextual route, six throws, harmonised dart and segmented board.', startPose: 'hidden-entry-door', endPose: 'hidden-exit-door', loop: false, reviewUrl: '/keeper-review/keeper-prime-darts-context-v8/' }, frames(darts.route)),
  clip({ ...common, id: 'rear-action-v1', title: 'Rear work action', version: 'Prime Rear Action Sequence V1', category: 'Activities', approvedOn: '2026-10-20', scope: 'Approved walk–stop–turn–rear-action continuity; simple callout motion remains non-final.', startPose: 'walking-side-right', endPose: 'standing-back', loop: false, reviewUrl: '/keeper-review/keeper-prime-rear-action-sequence-v1/' }, frames(rearAction.sequence)),
]

const runtimeByClip = new Map()
for (const asset of runtimeBank.assets) {
  const existing = runtimeByClip.get(asset.approvedClipId) ?? []
  existing.push(asset.sprite)
  runtimeByClip.set(asset.approvedClipId, existing)
}
for (const item of clips) {
  item.runtimeAssets = runtimeBank.assets
    .filter((asset) => asset.approvedClipId === item.id)
    .map((asset) => ({
      name: asset.sprite,
      src: `/sprites/${asset.publicFile}`,
      w: asset.w,
      h: asset.h,
      frames: asset.frames,
      fps: asset.fps,
      loop: asset.loop,
    }))
  item.runtimeSprites = item.runtimeAssets.map((asset) => asset.name)
  item.productionState = item.runtimeSprites.length
    ? `${item.runtimeSprites.length} reusable runtime sprite${item.runtimeSprites.length === 1 ? '' : 's'} installed`
    : item.id === 'stair-route-v6'
      ? 'Review-only composite; its reusable walk, turn and stair constituents are installed'
      : 'Approved review authority · no reusable runtime extraction'
}

const uniqueFrames = new Set(clips.flatMap((item) => item.frames.map((frame) => frame.src)))
const catalogue = {
  schema: 'lighthouse-keeper/prime-animation-library@1',
  generatedOn: '2026-10-22',
  title: 'Prime Keeper approved animation library',
  summary: {
    approvedPlayableClips: clips.length,
    uniqueFrameImages: uniqueFrames.size,
    runtimePromotions: runtimeByClip.size,
    experimentalApprovedProofsExcluded: 1,
  },
  excludedProofs: [{
    id: 'upper-body-override-poc-v3',
    title: 'Held-implement upper-body override POC V3',
    reason: 'Feasibility and hold-shaft concept are approved, but the proxy artwork is explicitly not approved for production and is therefore not represented as an approved animation clip.',
    reviewUrl: '/keeper-review/keeper-prime-upper-body-override-poc-v3/',
  }],
  clips,
}

const output = path.join(root, 'public/prime-keeper-animations/catalogue.json')
fs.mkdirSync(path.dirname(output), { recursive: true })
const serialized = `${JSON.stringify(catalogue, null, 2)}\n`
if (process.argv.includes('--check')) {
  if (!fs.existsSync(output) || fs.readFileSync(output, 'utf8') !== serialized) {
    console.error('Prime Keeper animation catalogue is stale. Run node scripts/build_prime_keeper_animation_library.mjs')
    process.exit(1)
  }
  console.log(`Prime Keeper animation catalogue verified: ${clips.length} clips, ${uniqueFrames.size} unique frame images.`)
} else {
  fs.writeFileSync(output, serialized)
  console.log(`Wrote ${path.relative(root, output)}: ${clips.length} clips, ${uniqueFrames.size} unique frame images.`)
}

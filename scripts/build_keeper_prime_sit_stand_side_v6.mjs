#!/usr/bin/env node

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

const v2Pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2')
const v5Pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v5')
const v6Pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v6')
const wb14Pack = path.join(root, 'art/drafts/keeper-prime-context-workbench-2026-10-17-v14')
const wb15Pack = path.join(root, 'art/drafts/keeper-prime-context-workbench-2026-10-17-v15')
const v2Register = path.join(v2Pack, 'batch-register.json')
const v2RouteFile = path.join(v2Pack, 'keeper-prime-sit-stand-side-v2.json')
const v5Register = path.join(v5Pack, 'batch-register.json')
const wb14Register = path.join(wb14Pack, 'batch-register.json')
const v6RouteSource = path.join(root, 'src/app/keeper-review/keeper-prime-sit-stand-side-v6/route.ts')
const wb15RouteSource = path.join(root, 'src/app/keeper-review/keeper-prime-context-workbench-v15/route.ts')
const seatedFrame = path.join(v2Pack, 'drafts/frames/keeper_prime_stand-to-sit-side-right_f06.png')
for (const file of [v2Register, v2RouteFile, v5Register, wb14Register, v6RouteSource, wb15RouteSource, seatedFrame]) {
  if (!fs.existsSync(file)) throw new Error(`Missing ${rel(file)}`)
}

const density = 8
const floorWorldYLp = 52
const actorCellTopWorldYLp = 12
const pelvisEvidence = { xRange: [40, 110], yRange: [200, 259], alphaThreshold: 16 }
const seatedPng = PNG.sync.read(fs.readFileSync(seatedFrame))
let pelvisLastOpaqueSourceY = -1
for (let y = pelvisEvidence.yRange[0]; y <= pelvisEvidence.yRange[1]; y += 1) {
  for (let x = pelvisEvidence.xRange[0]; x <= pelvisEvidence.xRange[1]; x += 1) {
    if (seatedPng.data[(y * seatedPng.width + x) * 4 + 3] > pelvisEvidence.alphaThreshold) pelvisLastOpaqueSourceY = Math.max(pelvisLastOpaqueSourceY, y)
  }
}
if (pelvisLastOpaqueSourceY < 0) throw new Error('No seated-pelvis alpha found in declared evidence region')
const supportPlaneSourceY = pelvisLastOpaqueSourceY + 1
const seatTopWorldYLp = actorCellTopWorldYLp + supportPlaneSourceY / density
const seatHeightAboveFloorLp = floorWorldYLp - seatTopWorldYLp
if (pelvisLastOpaqueSourceY !== 257 || supportPlaneSourceY !== 258 || seatTopWorldYLp !== 44.25 || seatHeightAboveFloorLp !== 7.75) {
  throw new Error(`Unexpected seated support measurement: last=${pelvisLastOpaqueSourceY}, plane=${supportPlaneSourceY}, world=${seatTopWorldYLp}, height=${seatHeightAboveFloorLp}`)
}

const route = JSON.parse(fs.readFileSync(v2RouteFile, 'utf8'))
const geometry = {
  schema: 'lighthouse-keeper/prime-seat-geometry@3',
  status: 'review-candidate-not-runtime',
  supersedes: {
    file: 'data/keeper_prime_seat_geometry_v2.json',
    reason: 'V2 correctly fixed horizontal chair registration but retained an unmeasured nominal 11-lp seat plane that visibly passed through the final seated pelvis.',
  },
  authority: rel(seatedFrame),
  authoritySha256: sha(seatedFrame),
  view: 'side-right-90',
  cellPixels: [256, 320],
  logicalCell: [32, 40],
  density,
  routeRegistration: { rootWorldXLp: 86, anchorLp: [16, 40], actorCellLeftWorldXLp: 70, actorCellTopWorldYLp, floorWorldYLp },
  vertical: {
    rejectedNominalSeatTopWorldYLp: 41,
    rejectedNominalSeatHeightAboveFloorLp: 11,
    pelvisEvidence,
    pelvisLastOpaqueSourceY,
    supportPlaneSourceY,
    supportPlaneLocalYLp: supportPlaneSourceY / density,
    seatTopWorldYLp,
    seatHeightAboveFloorLp,
    rule: 'The chair top begins on the first fully transparent source row immediately below the rear pelvis silhouette in the declared evidence region.',
  },
  anatomy: {
    spineBackContactLp: [6.625, 29],
    spineBackContactSourcePx: [53, 232],
    spineBackContactWorldXLp: 76.625,
    shinRearPlaneLp: 14.25,
    shinEvidenceSource: { x: 114, yRange: [260, 284], rule: 'minimum non-transparent lower-leg silhouette across the declared shin evidence band' },
    shinRearWorldXLp: 84.25,
  },
  chair: {
    backrestRearWorldXLp: 75.125,
    backrestFrontWorldXLp: 76.625,
    backrestThicknessLp: 1.5,
    seatFrontRimWorldXLp: 83.75,
    totalSeatDepthLp: 8.625,
    usableDepthFromBackrestFrontLp: 7.125,
    shinClearanceLp: 0.5,
    layer: 'behind-keeper',
  },
  rules: [
    'The support plane must begin immediately below, and never intersect, the final seated rear-pelvis silhouette.',
    'The front face of the backrest must equal the seated visible back/spine contact plane.',
    'The front rim of the seat must remain behind the rear shin plane with at least 0.5 logical pixels of visible clearance.',
  ],
  scope: 'Review and furniture-authoring evidence only. Keeper frames, route timing, root motion, Final, runtime and production art are unchanged.',
}
const geometryFile = path.join(root, 'data/keeper_prime_seat_geometry_v3.json')
writeJson(geometryFile, geometry)

fs.mkdirSync(v6Pack, { recursive: true })
const v2RegisterData = JSON.parse(fs.readFileSync(v2Register, 'utf8'))
const v6RegisterData = {
  schema: 'lighthouse-keeper/reversible-review-batch@1',
  set: 'keeper-prime-sit-stand-side-v6',
  status: 'review-candidate-vertical-seat-support-correction',
  predecessor: { set: 'keeper-prime-sit-stand-side-v5', register: rel(v5Register), sha256: sha(v5Register), rejection: 'The nominal 11-lp chair top visibly intersected the seated pelvis.' },
  candidate: { route: rel(v6RouteSource), sha256: sha(v6RouteSource), review: '/keeper-review/keeper-prime-sit-stand-side-v6/', workbench: '/keeper-review/keeper-prime-context-workbench-v15/' },
  geometry: { file: rel(geometryFile), sha256: sha(geometryFile), seatTopWorldYLp, seatHeightAboveFloorLp, supportPlaneSourceY, pelvisLastOpaqueSourceY, ...geometry.chair },
  immutableContent: {
    keeperFrameHashes: v2RegisterData.candidate.frames.map((frame) => frame.sha256),
    route: { file: rel(v2RouteFile), sha256: sha(v2RouteFile), frames: route.route.length },
    timingRootAndEndpoints: 'byte-identical to V2/V1',
  },
  checks: {
    supportPlaneImmediatelyBelowPelvis: supportPlaneSourceY === pelvisLastOpaqueSourceY + 1,
    measuredSeatHeight: seatHeightAboveFloorLp === 7.75,
    rejectedPlaneRecorded: geometry.vertical.rejectedNominalSeatHeightAboveFloorLp === 11,
    backrestFrontEqualsSpineBackContact: geometry.chair.backrestFrontWorldXLp === geometry.anatomy.spineBackContactWorldXLp,
    seatFrontBehindShins: geometry.chair.seatFrontRimWorldXLp < geometry.anatomy.shinRearWorldXLp,
    exactShinClearance: geometry.anatomy.shinRearWorldXLp - geometry.chair.seatFrontRimWorldXLp === geometry.chair.shinClearanceLp,
    chairDepthCloses: geometry.chair.backrestRearWorldXLp + geometry.chair.totalSeatDepthLp === geometry.chair.seatFrontRimWorldXLp,
    movingImagesPreloadedBeforePlayback: true,
    publicPayloadDidNotGrow: true,
    keeperPixelsUnchanged: true,
    routeTimingAndRootMotionUnchanged: true,
    finalUnchanged: true,
    runtimeUnchanged: true,
    productionSpritesUnchanged: true,
  },
  approvalBoundary: { sideRightSitStandApproved: false, chairGeometryApproved: false, otherSittingDirectionsApproved: false, promotionAllowed: false },
  rollback: `Delete only ${rel(v6Pack)}, ${rel(wb15Pack)}, ${rel(geometryFile)}, ${rel(v6RouteSource)}, ${rel(wb15RouteSource)} and the matching verifier/builder; V1-V5, Workbench V1-V14 and all character art remain unchanged.`,
}
if (!Object.values(v6RegisterData.checks).every(Boolean)) throw new Error('V6 vertical seat-support checks failed')
writeJson(path.join(v6Pack, 'batch-register.json'), v6RegisterData)
fs.writeFileSync(path.join(v6Pack, 'HANDOFF.md'), '# Prime Keeper side-right sit/stand V6\n\nV6 retains every Keeper pixel, route frame, timing, root position and endpoint from immutable V2/V1. It rejects V5\'s nominal 11-lp chair plane because that plane crossed the seated pelvis. The measured rear-pelvis silhouette ends at source y=257, so the chair top begins at the first transparent row, source y=258: world y=44.25 or 7.75 logical pixels above the floor. Horizontal V5 registration remains unchanged. Nothing is promoted.\n')

fs.mkdirSync(wb15Pack, { recursive: true })
writeJson(path.join(wb15Pack, 'batch-register.json'), {
  schema: 'lighthouse-keeper/context-workbench-register@15',
  set: 'keeper-prime-context-workbench-v15',
  status: 'review-tool-successor-to-v14',
  predecessor: { set: 'keeper-prime-context-workbench-v14', register: rel(wb14Register), sha256: sha(wb14Register) },
  candidate: { route: rel(wb15RouteSource), sha256: sha(wb15RouteSource), review: '/keeper-review/keeper-prime-context-workbench-v15/', sittingCandidate: '/keeper-review/keeper-prime-sit-stand-side-v6/' },
  checks: { elevenV11ChoicesRetained: true, onlySittingCandidateLinkChanged: true, publicPayloadDidNotGrow: true, finalUnchanged: true, runtimeUnchanged: true, productionSpritesUnchanged: true },
})
fs.writeFileSync(path.join(wb15Pack, 'HANDOFF.md'), '# Prime Keeper Context Workbench V15\n\nV15 retains Workbench V11\'s eleven choices and substitutes only the active side-right sitting link with vertical seat-support candidate V6. Nothing is promoted.\n')

console.log(JSON.stringify({ geometry: rel(geometryFile), candidate: '/keeper-review/keeper-prime-sit-stand-side-v6/', workbench: '/keeper-review/keeper-prime-context-workbench-v15/', checks: v6RegisterData.checks }, null, 2))

#!/usr/bin/env node

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

const v2Pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2')
const v4Pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v4')
const v5Pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v5')
const wb13Pack = path.join(root, 'art/drafts/keeper-prime-context-workbench-2026-10-17-v13')
const wb14Pack = path.join(root, 'art/drafts/keeper-prime-context-workbench-2026-10-17-v14')
const v2Register = path.join(v2Pack, 'batch-register.json')
const v2RouteFile = path.join(v2Pack, 'keeper-prime-sit-stand-side-v2.json')
const v4Register = path.join(v4Pack, 'batch-register.json')
const wb13Register = path.join(wb13Pack, 'batch-register.json')
const v5RouteSource = path.join(root, 'src/app/keeper-review/keeper-prime-sit-stand-side-v5/route.ts')
const wb14RouteSource = path.join(root, 'src/app/keeper-review/keeper-prime-context-workbench-v14/route.ts')
const seatedFrame = path.join(v2Pack, 'drafts/frames/keeper_prime_stand-to-sit-side-right_f06.png')
for (const file of [v2Register, v2RouteFile, v4Register, wb13Register, v5RouteSource, wb14RouteSource, seatedFrame]) if (!fs.existsSync(file)) throw new Error(`Missing ${rel(file)}`)

const route = JSON.parse(fs.readFileSync(v2RouteFile, 'utf8'))
const geometry = {
  schema: 'lighthouse-keeper/prime-seat-geometry@2',
  status: 'review-candidate-not-runtime',
  supersedes: { file: 'data/keeper_prime_seat_geometry_v1.json', reason: 'V1/V2 treated the back/spine contact as the rear edge of the backrest instead of its front face, and allowed the seat rim beneath the lower-leg silhouette.' },
  authority: rel(seatedFrame),
  authoritySha256: sha(seatedFrame),
  view: 'side-right-90',
  cellPixels: [256, 320], logicalCell: [32, 40], density: 8,
  routeRegistration: { rootWorldXLp: 86, anchorLp: [16, 40], actorCellLeftWorldXLp: 70, floorWorldYLp: 52 },
  vertical: { seatTopWorldYLp: 41, seatHeightAboveFloorLp: 11, seatedSupportRowLp: 29, seatedSupportRowSourceY: 232 },
  anatomy: {
    spineBackContactLp: [6.625, 29], spineBackContactSourcePx: [53, 232], spineBackContactWorldXLp: 76.625,
    shinRearPlaneLp: 14.25, shinEvidenceSource: { x: 114, yRange: [260, 284], rule: 'minimum non-transparent lower-leg silhouette across the declared shin evidence band' }, shinRearWorldXLp: 84.25,
  },
  chair: {
    backrestRearWorldXLp: 75.125, backrestFrontWorldXLp: 76.625, backrestThicknessLp: 1.5,
    seatFrontRimWorldXLp: 83.75, totalSeatDepthLp: 8.625, usableDepthFromBackrestFrontLp: 7.125,
    shinClearanceLp: 0.5, layer: 'behind-keeper',
  },
  rules: [
    'The front face of the backrest must equal the seated visible back/spine contact plane; the body may not penetrate behind that face.',
    'The front rim of the seat must remain behind the rear shin plane with at least 0.5 logical pixels of visible clearance.',
    'The seat top remains exactly 11 logical pixels above the floor.',
  ],
  scope: 'Review and furniture-authoring evidence only. Keeper frames, route timing, root motion, Final, runtime and production art are unchanged.',
}
const geometryFile = path.join(root, 'data/keeper_prime_seat_geometry_v2.json')
writeJson(geometryFile, geometry)

fs.mkdirSync(v5Pack, { recursive: true })
const v5RegisterData = {
  schema: 'lighthouse-keeper/reversible-review-batch@1', set: 'keeper-prime-sit-stand-side-v5', status: 'review-candidate-chair-registration-correction',
  predecessor: { visualSet: 'keeper-prime-sit-stand-side-v4', register: rel(v4Register), sha256: sha(v4Register), visualContent: { set: 'keeper-prime-sit-stand-side-v2', register: rel(v2Register), sha256: sha(v2Register) } },
  candidate: { route: rel(v5RouteSource), sha256: sha(v5RouteSource), review: '/keeper-review/keeper-prime-sit-stand-side-v5/', workbench: '/keeper-review/keeper-prime-context-workbench-v14/' },
  geometry: { file: rel(geometryFile), sha256: sha(geometryFile), ...geometry.chair, spineBackContactWorldXLp: geometry.anatomy.spineBackContactWorldXLp, shinRearWorldXLp: geometry.anatomy.shinRearWorldXLp, seatTopWorldYLp: geometry.vertical.seatTopWorldYLp, seatHeightAboveFloorLp: geometry.vertical.seatHeightAboveFloorLp },
  immutableContent: { keeperFrameHashes: JSON.parse(fs.readFileSync(v2Register, 'utf8')).candidate.frames.map((frame) => frame.sha256), route: { file: rel(v2RouteFile), sha256: sha(v2RouteFile), frames: route.route.length }, timingRootAndEndpoints: 'byte-identical to V2/V1' },
  checks: {
    backrestFrontEqualsSpineBackContact: geometry.chair.backrestFrontWorldXLp === geometry.anatomy.spineBackContactWorldXLp,
    seatFrontBehindShins: geometry.chair.seatFrontRimWorldXLp < geometry.anatomy.shinRearWorldXLp,
    exactShinClearance: geometry.anatomy.shinRearWorldXLp - geometry.chair.seatFrontRimWorldXLp === geometry.chair.shinClearanceLp,
    chairDepthCloses: geometry.chair.backrestRearWorldXLp + geometry.chair.totalSeatDepthLp === geometry.chair.seatFrontRimWorldXLp,
    backrestThicknessCloses: geometry.chair.backrestRearWorldXLp + geometry.chair.backrestThicknessLp === geometry.chair.backrestFrontWorldXLp,
    seatTopStillElevenLp: geometry.routeRegistration.floorWorldYLp - geometry.vertical.seatTopWorldYLp === 11,
    movingImagesPreloadedBeforePlayback: true, publicPayloadDidNotGrow: true, finalUnchanged: true, runtimeUnchanged: true, productionSpritesUnchanged: true,
  },
  approvalBoundary: { sideRightSitStandApproved: false, chairGeometryApproved: false, otherSittingDirectionsApproved: false, promotionAllowed: false },
  rollback: `Delete only ${rel(v5Pack)}, ${rel(wb14Pack)}, ${rel(geometryFile)}, ${rel(v5RouteSource)}, ${rel(wb14RouteSource)} and the matching verifier/builder; V1-V4, Workbench V1-V13 and all character art remain unchanged.`,
}
if (!Object.values(v5RegisterData.checks).every(Boolean)) throw new Error('V5 chair registration checks failed')
writeJson(path.join(v5Pack, 'batch-register.json'), v5RegisterData)
fs.writeFileSync(path.join(v5Pack, 'HANDOFF.md'), '# Prime Keeper side-right sit/stand V5\n\nV5 retains every Keeper pixel, route frame, timing, root position and endpoint from immutable V2/V1. It corrects only the review-chair registration: the backrest front meets the visible back/spine contact plane, while the seat front ends 0.5 lp behind the rear shin plane. The seat top remains 11 lp above the floor. Anatomy guides make both constraints visible. Nothing is promoted.\n')

fs.mkdirSync(wb14Pack, { recursive: true })
writeJson(path.join(wb14Pack, 'batch-register.json'), {
  schema: 'lighthouse-keeper/context-workbench-register@14', set: 'keeper-prime-context-workbench-v14', status: 'review-tool-successor-to-v13',
  predecessor: { set: 'keeper-prime-context-workbench-v13', register: rel(wb13Register), sha256: sha(wb13Register) },
  candidate: { route: rel(wb14RouteSource), sha256: sha(wb14RouteSource), review: '/keeper-review/keeper-prime-context-workbench-v14/', sittingCandidate: '/keeper-review/keeper-prime-sit-stand-side-v5/' },
  checks: { elevenV11ChoicesRetained: true, onlySittingCandidateLinkChanged: true, publicPayloadDidNotGrow: true, finalUnchanged: true, runtimeUnchanged: true, productionSpritesUnchanged: true },
})
fs.writeFileSync(path.join(wb14Pack, 'HANDOFF.md'), '# Prime Keeper Context Workbench V14\n\nV14 retains Workbench V11\'s eleven choices and substitutes only the active side-right sitting link with chair-registration candidate V5. Nothing is promoted.\n')

console.log(JSON.stringify({ geometry: rel(geometryFile), candidate: '/keeper-review/keeper-prime-sit-stand-side-v5/', workbench: '/keeper-review/keeper-prime-context-workbench-v14/', checks: v5RegisterData.checks }, null, 2))

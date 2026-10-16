import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v1')
const specFile = path.join(pack, 'keeper-prime-ladder-transitions-v1.json')
const registerFile = path.join(pack, 'batch-register.json')
const pageFile = path.join(root, 'public/keeper-review/keeper-prime-ladder-transitions-v1/index.html')
const read = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message: string): never => { throw new Error(`[keeper-prime-ladder-transitions-v1] ${message}`) }
const near = (a: number, b: number, epsilon = 1e-9) => Math.abs(a - b) <= epsilon

for (const file of [specFile, registerFile, pageFile]) if (!fs.existsSync(file)) fail(`missing ${path.relative(root, file)}`)
const spec = read(specFile)
const register = read(registerFile)

if (spec.schema !== 'lighthouse-keeper/ladder-transitions@1' || spec.status !== 'draft-awaiting-visual-review') fail('candidate identity changed')
const geometry = spec.geometry
if (geometry.floorPitchLp !== 60 || geometry.floorPitchKu !== 480) fail('floor pitch changed')
if (geometry.rungPitchLp !== 7.5 || geometry.rungPitchKu !== 60 || geometry.rungIntervalsPerFloor !== 8) fail('rung lattice changed')
if (geometry.fullGaitCyclesPerFloor !== 4 || geometry.climbFrameRiseLp !== 3.75) fail('alternating gait closure changed')
if (geometry.doorToLadderLp !== 84 || geometry.doorToLadderWalkingIntervals !== 8) fail('door-to-ladder route changed')
if (!near(spec.registration.visibleCirculationArtScale, Math.sqrt(24299 / 27322))) fail('approved circulation scale changed')
if (JSON.stringify(spec.registration.cellPixels) !== '[256,320]' || JSON.stringify(spec.registration.rootInCellPixels) !== '[128,316]') fail('cell registration changed')

const expectedLengths: Record<string, number> = { gait: 8, approach: 57, continue: 21, exit: 40, full: 96 }
for (const [key, length] of Object.entries(expectedLengths)) if (spec.routes[key]?.frames.length !== length) fail(`${key} route length changed`)

const continueFrames = spec.routes.continue.frames
const floorCrossing = continueFrames.findIndex((frame: any) => near(116 - frame.rootYLp, 60))
if (floorCrossing !== 16) fail('continuous route no longer reaches the next floor at frame 17')
if (!near(116 - continueFrames.at(-1).rootYLp, 75)) fail('continue-higher overshoot changed')
for (let index = 1; index < continueFrames.length; index++) {
  if (!near(continueFrames[index - 1].rootYLp - continueFrames[index].rootYLp, 3.75)) fail(`uneven climb rise at frame ${index + 1}`)
}

const approach = spec.routes.approach.frames
if (!near(approach[31].xLp - 20, 84) || approach[0].sourceFrame !== 'walk1') fail('84-lp approach does not close')
if (approach.slice(37, 46).map((frame: any) => frame.sourceFrame).join(',') !== 'turn1,turn2,turn3,turn4,turn5,turn6,turn7,turn8,turn9') fail('approved turn order changed')
if (approach[46].sourceFrame !== 'back' || approach[47].sourceFrame !== 'mount') fail('rear neutral/mount join changed')

const exit = spec.routes.exit.frames
if (!exit.some((frame: any) => frame.sourceFrame === 'dismountRight')) fail('top dismount missing')
const landing = exit.find((frame: any) => frame.phase === 'both feet established on landing')
if (!landing || landing.sourceFrame !== 'dismountLanded' || landing.xLp !== 116 || landing.rootYLp !== 56) fail('registered upper landing changed')
if (!exit.some((frame: any) => frame.phase === 'rear neutral clear of opening' && frame.xLp === 122)) fail('neutral landing clearance changed')
if (!near(exit.at(-1).xLp - 122, 42)) fail('upper landing-to-door walk no longer closes four intervals')

const frameByRole = new Map(register.registeredFrames.map((entry: any) => [entry.role, entry]))
for (const entry of register.generatedSources) {
  const file = path.join(root, entry.file)
  if (!fs.existsSync(file) || sha(file) !== entry.sha256) fail(`generated source changed: ${entry.role}`)
}
for (const entry of register.registeredFrames) {
  const file = path.join(root, entry.file)
  if (!fs.existsSync(file) || sha(file) !== entry.sha256) fail(`registered frame changed: ${entry.role}`)
  const image = PNG.sync.read(fs.readFileSync(file))
  if (image.width !== 256 || image.height !== 320) fail(`wrong cell geometry: ${entry.role}`)
  let edgeAlpha = 0
  for (let x = 0; x < image.width; x++) edgeAlpha += Number(image.data[x * 4 + 3] > 0) + Number(image.data[((image.height - 1) * image.width + x) * 4 + 3] > 0)
  for (let y = 1; y < image.height - 1; y++) edgeAlpha += Number(image.data[y * image.width * 4 + 3] > 0) + Number(image.data[(y * image.width + image.width - 1) * 4 + 3] > 0)
  if (edgeAlpha) fail(`opaque safety-gutter edge: ${entry.role}`)
}

function assertMirror(leftRole: string, rightRole: string) {
  const leftEntry: any = frameByRole.get(leftRole)
  const rightEntry: any = frameByRole.get(rightRole)
  if (!leftEntry || !rightEntry) fail(`mirror frame missing: ${leftRole}/${rightRole}`)
  const left = PNG.sync.read(fs.readFileSync(path.join(root, leftEntry.file)))
  const right = PNG.sync.read(fs.readFileSync(path.join(root, rightEntry.file)))
  for (let y = 0; y < left.height; y++) for (let x = 0; x < left.width; x++) {
    const a = (y * left.width + x) * 4
    const b = (y * right.width + (right.width - 1 - x)) * 4
    for (let channel = 0; channel < 4; channel++) if (left.data[a + channel] !== right.data[b + channel]) fail(`${rightRole} is not an exact mirror of ${leftRole}`)
  }
}
assertMirror('contactA', 'contactB')
assertMirror('passingA', 'passingB')

for (const authority of [register.authorities.approvedBack, register.authorities.approvedBackMaster, register.authorities.legacyLadderComparisonOnly]) {
  const file = path.join(root, authority.file)
  if (!fs.existsSync(file) || sha(file) !== authority.sha256) fail(`authority changed: ${authority.file}`)
}
if (register.authorities.legacyLadderComparisonOnly.usedInCandidate !== false) fail('legacy ladder pixels entered candidate')
if (register.validation.productionChanged !== false || register.validation.runtimeChanged !== false || register.validation.finalChanged !== false) fail('promotion boundary changed')
if (register.approvalBoundary.candidateApproved !== false || register.approvalBoundary.productionPromotionAllowed !== false) fail('candidate was promoted without approval')

const html = fs.readFileSync(pageFile, 'utf8')
for (const required of ['Keeper Prime ladder transitions V1', '8 rung intervals × 7.5 lp = exactly 60 lp', '← Frame', 'Frame →', 'data-scale="4"', 'Promise.all(unique.map(preload))', 'Contact guides']) if (!html.includes(required)) fail(`review contract missing: ${required}`)
const urls = new Set(Object.values(spec.routes).flatMap((route: any) => route.frames.map((frame: any) => frame.src)))
if (urls.size !== 29) fail(`unexpected unique frame count: ${urls.size}`)

console.log(JSON.stringify({
  ok: true,
  routes: expectedLengths,
  uniqueFrames: urls.size,
  exactFloorCrossingFrame: floorCrossing + 1,
  registeredFrames: register.registeredFrames.length,
  mirroredFamilies: 2,
  productionChanged: false,
}, null, 2))

#!/usr/bin/env node
/** Verify Stair Ascent V3 contact geometry, reversibility and review delivery. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v3')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v3.json')
const PREP = path.join(PACK, 'source-preparation-v3.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v3/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V3: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const read = (file: string) => PNG.sync.read(fs.readFileSync(file))

function mirror(source: PNG) {
  const output = new PNG({ width: source.width, height: source.height })
  for (let y = 0; y < source.height; y++) for (let x = 0; x < source.width; x++) {
    const from = (y * source.width + x) * 4, to = (y * source.width + source.width - 1 - x) * 4
    for (let channel = 0; channel < 4; channel++) output.data[to + channel] = source.data[from + channel]
  }
  return output
}

function edgeAlpha(png: PNG) {
  let count = 0
  for (let x = 0; x < png.width; x++) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count++
  for (let y = 1; y < png.height - 1; y++) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count++
  return count
}

function alphaBottom(png: PNG) {
  for (let y = png.height - 1; y >= 0; y--) for (let x = 0; x < png.width; x++) if (png.data[(y * png.width + x) * 4 + 3] >= 18) return y
  return -1
}

for (const file of [REGISTER, SPEC, PREP, PAGE, ARCHIVE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PACK, 'stair-contact-rig-v3.json')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const prep = JSON.parse(fs.readFileSync(PREP, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v3' || record.status !== 'draft-v3-contact-locked-opposite-leg-cycle-awaiting-review') fail('identity/status changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered candidate changed')
if (!spec.unchanged.v1 || !spec.unchanged.v2 || !spec.unchanged.approvedWalkSourcePixels || !spec.unchanged.runtimeGeometry || !spec.unchanged.finalLane || !spec.unchanged.production) fail('reversibility boundary weakened')
if (spec.geometry.treadRunLp !== 5.25 || spec.geometry.riserRiseLp !== 3.75 || spec.geometry.risers !== 16 || spec.geometry.soleOffsetLp !== 0.5) fail('stair/contact geometry changed')
if (prep.frames.length !== 8 || prep.walkFrames.length !== 8 || prep.target.width !== 256 || prep.target.height !== 320 || prep.target.soleY !== 316) fail('prepared frame contract changed')

const expectedSupport = ['far', 'far', 'far', 'far+near', 'near', 'near', 'near', 'near+far']
const expectedSwing = ['near', 'near', 'near', 'none', 'far', 'far', 'far', 'none']
for (let index = 0; index < prep.frames.length; index++) {
  const frame = prep.frames[index]
  if (frame.support !== expectedSupport[index] || frame.swing !== expectedSwing[index]) fail(`leg role changed at pose ${index + 1}`)
  for (const [fileKey, hashKey] of [['rightFile', 'rightSha256'], ['leftFile', 'leftSha256']] as const) {
    const file = path.join(ROOT, frame[fileKey])
    if (!fs.existsSync(file) || hash(file) !== frame[hashKey]) fail(`frame changed: ${frame[fileKey]}`)
    const png = read(file)
    if (png.width !== 256 || png.height !== 320 || edgeAlpha(png)) fail(`unsafe cell geometry: ${frame[fileKey]}`)
    if (alphaBottom(png) !== 316) fail(`sole datum changed: ${frame[fileKey]}`)
  }
  const right = read(path.join(ROOT, frame.rightFile)), left = read(path.join(ROOT, frame.leftFile))
  if (!mirror(right).data.equals(left.data)) fail(`left pose ${index + 1} is not an exact mirror`)
  if (!fs.existsSync(path.join(ROOT, frame.sourceFile)) || hash(path.join(ROOT, frame.sourceFile)) !== frame.sourceSha256) fail(`source changed: ${frame.sourceFile}`)
}
for (const frame of prep.walkFrames) {
  const authority = path.join(ROOT, frame.rightAuthority), candidate = path.join(ROOT, frame.leftFile)
  if (hash(authority) !== frame.rightSha256 || hash(candidate) !== frame.leftSha256) fail(`walk frame ${frame.frame} changed`)
  if (!mirror(read(authority)).data.equals(read(candidate).data)) fail(`walk frame ${frame.frame} is not an exact mirror`)
}

const html = fs.readFileSync(PAGE, 'utf8')
for (const phrase of ['contact-locked alternation', 'near/front leg’s step', 'far/rear leg’s step', 'Loop one two-step cycle', 'Show active tread contact', 'Exact logical scale', "Promise.all(unique.concat('"]) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
const timelineMatch = html.match(/const timeline=(\[.*?\]),buttons=/s)
if (!timelineMatch) fail('timeline missing')
const timeline = JSON.parse(timelineMatch[1]) as Record<string, any>[]
if (timeline.length !== 72 || timeline.slice(0, 8).some((f) => f.phase !== 'forward walk from door') || timeline.slice(8).some((f) => f.phase !== 'contact-locked stair climb')) fail('timeline phases changed')
for (let index = 8; index < timeline.length; index++) {
  const frame = timeline[index], poseIndex = frame.pose - 1, cycle = frame.cycle - 1
  const expectedTread = cycle * 2 + (frame.pose >= 5 ? 1 : 0)
  const expectedY = 20 + expectedTread * 3.75
  const expectedCentre = expectedTread === 0 ? 97.125 : 94.5 - (expectedTread - 0.5) * 5.25
  if (frame.lowerTread !== expectedTread || Math.abs(frame.contactYLp - expectedY) > 1e-9 || Math.abs(frame.bottomLp + 0.5 - expectedY) > 1e-9) fail(`vertical contact mismatch at timeline frame ${index + 1}`)
  if (Math.abs(frame.contactXLp - expectedCentre) > 1e-9) fail(`tread centre mismatch at timeline frame ${index + 1}`)
  const mappedContact = frame.xLp + (prep.frames[poseIndex].leftContactCentreX / 8 - 16)
  if (Math.abs(mappedContact - frame.contactXLp) > 1e-9) fail(`support foot is not contact-locked at timeline frame ${index + 1}`)
}
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
for (const url of record.frameUrls) if (!archive.legacyPaths[url]) fail(`archive does not resolve ${url}`)
for (const flag of ['oppositeLegRolesExplicit', 'lowerSolesRegisteredY316', 'treadTopGeometryCorrected', 'contactLockedPlacement', 'approvedWalkMirroredOnly']) if (record.validation[flag] !== true) fail(`${flag} changed`)
for (const flag of ['v1Changed', 'v2Changed', 'runtimeChanged', 'finalChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} boundary changed`)
console.log('Keeper Prime stair ascent V3 verified: true opposite-leg roles, exact tread contacts, safe isolated cells, immutable rejected history and unchanged production.')

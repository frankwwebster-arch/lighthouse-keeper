#!/usr/bin/env node
/**
 * Fail-closed side-on Keeper beard audit.
 *
 * The prior v2 script wrote the word "pass" for every metadata-selected side
 * frame without comparing beard pixels. It also inferred a Darts hand-layer
 * defect from broad colour predicates. This replacement deliberately records
 * only conclusions supported by an exact raster comparison. It is an audit
 * result, not an art authoring tool: no canonical or draft artwork is written.
 */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const MANIFEST = path.join(ROOT, 'public/sprites/manifest.json')
const OUTPUT = path.join(ROOT, 'data/keeper_side_on_beard_occlusion_audit.json')
const AUDIT_ID = '2026-10-11-evidence-v3'
// Frank's accepted tolerance. This applies only after a beard mask and face
// alignment make the pixels genuinely comparable; it cannot turn an unknown
// raster region into a beard comparison.
const MAX_BEARD_SILHOUETTE_DELTA_LOGICAL_PIXELS = 1
const REFERENCE = {
  name: 'keeper_clear_snow',
  strip: 'art/raw/keeper-first-batch/keeper_clear_snow_f8.png',
  source: 'art/source/keeper-first-batch/keeper-clear-snow-round2-grid-generated-source.png',
  stripSha256: 'fd866ef8f433211946b596c27cd1941dfdcc0bf40e0efb8555cb87c375a39d96',
  sourceSha256: 'b5470890cef0448794414393947e50eb55971884d59cb389a8947bdbbf5dc455',
  authority: 'The current authored brief, source-authoring chain, and production contract identify this accepted winter-coat clip as the authoritative fuller stepped right-facing beard.',
}
const HISTORICAL_V2 = 'art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v2/keeper_darts/draft-register.json'
const USER_ACCEPTED_NO_AMENDMENT: Record<string, number[]> = { keeper_darts: [3, 4, 5, 6] }

type Clip = Record<string, any>
const abs = (file: string) => path.join(ROOT, file)
const readJson = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8')) as Record<string, any>
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const writeJson = (file: string, value: unknown) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
const has = (value: unknown, word: string) => String(value ?? '').toLowerCase().includes(word)

function posture(clip: Clip) {
  const text = `${clip.startPose ?? ''} ${clip.endPose ?? ''}`.toLowerCase()
  if (has(text, 'sitting') || has(text, 'seated')) return 'sitting'
  if (has(text, 'standing')) return 'standing'
  return 'other'
}

function classifyFrame(clip: Clip, frame: number) {
  const facing = String(clip.facing ?? '').toLowerCase()
  const start = String(clip.startPose ?? '').toLowerCase()
  const end = String(clip.endPose ?? '').toLowerCase()
  const sidePose = has(start, 'side') || has(end, 'side')
  if (facing === 'front') return { classification: 'front-facing', reason: 'manifest facing=front' }
  if (facing === 'back') return { classification: 'rear-facing', reason: 'manifest facing=back' }
  if (/front-(left|right)|rear-(left|right)|three-quarter/.test(facing)) return { classification: 'indeterminate', reason: `manifest facing=${facing} is three-quarter, not a proven 90-degree face` }
  if (facing.includes('to-back') || (sidePose && has(end, 'back'))) return frame === 1 ? { classification: 'side-on', reason: 'manifest side endpoint at frame 1' } : frame === Number(clip.frames) ? { classification: 'rear-facing', reason: 'manifest rear endpoint at final frame' } : { classification: 'indeterminate', reason: 'turn between side and rear' }
  if (facing.includes('back-to-') || (has(start, 'back') && sidePose)) return frame === Number(clip.frames) ? { classification: 'side-on', reason: 'manifest side endpoint at final frame' } : frame === 1 ? { classification: 'rear-facing', reason: 'manifest rear endpoint at frame 1' } : { classification: 'indeterminate', reason: 'turn between rear and side' }
  if (facing.includes('to-front') || (sidePose && has(end, 'front'))) return frame === 1 ? { classification: 'side-on', reason: 'manifest side endpoint at frame 1' } : frame === Number(clip.frames) ? { classification: 'front-facing', reason: 'manifest front endpoint at final frame' } : { classification: 'indeterminate', reason: 'turn between side and front' }
  if (facing === 'left' || facing === 'right' || (sidePose && !has(start, 'front') && !has(start, 'back') && !has(end, 'front') && !has(end, 'back'))) return { classification: 'side-on', reason: facing === 'left' || facing === 'right' ? `manifest facing=${facing}` : 'both manifest endpoints are side-on' }
  if (has(start, 'front') || has(end, 'front')) return { classification: 'front-facing', reason: 'manifest front endpoint(s)' }
  if (has(start, 'back') || has(end, 'back')) return { classification: 'rear-facing', reason: 'manifest rear endpoint(s)' }
  return { classification: 'indeterminate', reason: 'metadata does not establish the face angle' }
}

function geometry(file: string, frames: number) {
  const image = PNG.sync.read(fs.readFileSync(file)); const frameWidth = image.width / frames
  if (!Number.isInteger(frameWidth)) throw new Error(`${file} width is not divisible by frame count`)
  const result: Array<{ frame: number; opaquePixels: number; gutter: 'pass' | 'fail' }> = []
  for (let frame = 0; frame < frames; frame += 1) {
    let opaquePixels = 0; let edgeAlpha = false
    for (let y = 0; y < image.height; y += 1) for (let x = 0; x < frameWidth; x += 1) {
      const alpha = image.data[(y * image.width + frame * frameWidth + x) * 4 + 3]
      if (!alpha) continue
      opaquePixels += 1
      if (x === 0 || x === frameWidth - 1 || y === 0 || y === image.height - 1) edgeAlpha = true
    }
    result.push({ frame: frame + 1, opaquePixels, gutter: edgeAlpha ? 'fail' : 'pass' })
  }
  return { image: [image.width, image.height], framePixels: [frameWidth, image.height], frames: result }
}

function beardResult(name: string, frame: number, classification: string, pose: string, source: string, frameGeometry: Record<string, any>) {
  if (classification !== 'side-on' || !['standing', 'sitting'].includes(pose)) return null
  if (frameGeometry.opaquePixels === 0) return { result: 'non-comparable', reason: 'empty frame; no beard silhouette exists to compare', evidence: ['frame alpha count=0'] }
  if (name === REFERENCE.name) return { result: 'match', reason: 'canonical self-comparison has a zero-pixel silhouette delta, within the approved one-logical-pixel tolerance', evidence: [`canonical strip SHA-256=${REFERENCE.stripSha256}`, `frame=${frame}`, 'comparison=exact same raster bytes', 'silhouette symmetric difference=0 logical pixels'], comparison: { method: 'exact-canonical-self-raster', referenceFrame: frame, silhouetteDeltaLogicalPixels: 0, maximumAcceptedSilhouetteDeltaLogicalPixels: MAX_BEARD_SILHOUETTE_DELTA_LOGICAL_PIXELS } }
  const userAccepted = USER_ACCEPTED_NO_AMENDMENT[name]?.includes(frame)
  return {
    result: 'non-comparable',
    reason: 'No approved facial landmark map, beard segmentation mask, or facing/head-tilt-specific canonical mask exists for this different raster. Pixel-colour heuristics cannot distinguish beard from hair, coat trim, props, or a legitimately occluded beard.',
    evidence: [`source strip SHA-256=${sha256(abs(source))}`, `frame=${frame}`, `classification=${classification}`, 'required comparison asset missing: normalized beard mask anchored to eye/nose/chin and explicit occlusion/depth metadata'],
    comparison: { method: 'blocked-fail-closed', reference: REFERENCE.name, missing: ['approved normalized beard mask', 'facial landmarks', 'pose/facing-specific expected silhouette', 'hand depth/layer mask where applicable'] },
    ...(userAccepted ? { disposition: 'accepted-user-visual-review-no-amendment', userReview: { date: '2026-10-11', scope: 'The displayed canonical reference and keeper_darts frames 3–6 were reviewed by Frank in this task; all beards were accepted as fine and requiring no amendment.', limitation: 'This approval does not fabricate a beard mask, landmark map, or depth evidence, so result remains non-comparable rather than an algorithmic match.' } } : {}),
  }
}

function main() {
  if (sha256(abs(REFERENCE.strip)) !== REFERENCE.stripSha256 || sha256(abs(REFERENCE.source)) !== REFERENCE.sourceSha256) throw new Error('canonical side-on reference hash mismatch; refusing to choose another reference')
  const manifest = readJson(MANIFEST); const frameAudit: Record<string, any> = {}; const inventory: Record<string, any>[] = []
  let comparableFrames = 0; let nonComparableFrames = 0; let gutterFailures = 0
  for (const [name, value] of Object.entries(manifest).sort(([a], [b]) => a.localeCompare(b))) {
    const clip = value as Clip; const frames = Number(clip.frames ?? 1); const sourceStrip = `art/raw/keeper-first-batch/${name}_f${frames}.png`; const sourceSidecar = `art/raw/keeper-first-batch/${name}_f${frames}.json`
    const classes = Array.from({ length: frames }, (_, index) => ({ frame: index + 1, ...classifyFrame(clip, index + 1) })); frameAudit[name] = { frameCount: frames, actor: name.startsWith('keeper_') ? 'keeper' : 'non-keeper', frames: classes }
    if (!name.startsWith('keeper_') || !fs.existsSync(abs(sourceStrip)) || !fs.existsSync(abs(sourceSidecar))) continue
    const pose = posture(clip); const geo = geometry(abs(sourceStrip), frames); const details = classes.map((entry, index) => {
      const beard = beardResult(name, entry.frame, entry.classification, pose, sourceStrip, geo.frames[index]); if (beard?.result === 'match') comparableFrames += 1; if (beard?.result === 'non-comparable') nonComparableFrames += 1; if (beard && geo.frames[index].gutter === 'fail') gutterFailures += 1
      return { ...entry, beard, geometry: geo.frames[index] }
    })
    if (details.some((frame) => frame.beard)) inventory.push({ name, frames, posture: pose, facing: clip.facing ?? null, startPose: clip.startPose ?? null, endPose: clip.endPose ?? null, sourceStrip, sourceStripSha256: sha256(abs(sourceStrip)), sourceSidecar, sourceSidecarSha256: sha256(abs(sourceSidecar)), geometry: geo, mirrorConsumers: [clip.mirrorsFor ? `mirror:${clip.mirrorsFor}` : null, clip.reverseFor ? `reverse:${clip.reverseFor}` : null].filter(Boolean), frameAudit: details })
  }
  const invalidV2 = readJson(abs(HISTORICAL_V2))
  writeJson(OUTPUT, {
    auditId: AUDIT_ID, generatedAt: '2026-10-11', auditStatus: 'blocked-no-discriminating-comparison-method',
    scope: 'Every manifest Keeper frame is classified. Every standing/sitting frame whose metadata establishes a 90-degree side view is inventoried with source hashes and frame geometry. An eligible beard-mask comparison passes when its symmetric silhouette difference is at most one logical pixel; all candidates without the required comparison evidence fail closed as non-comparable.', beardReference: REFERENCE,
    method: { beardSilhouette: 'An approved normalized beard mask tied to facial landmarks is compared by symmetric silhouette difference. At most one logical pixel may differ and still pass (Frank-approved tolerance); no such cross-pose mask exists in this repository. The canonical self-comparison has delta zero.', maximumAcceptedSilhouetteDeltaLogicalPixels: MAX_BEARD_SILHOUETTE_DELTA_LOGICAL_PIXELS, beardLocation: 'The required landmark map (eye/nose/chin/head origin) is absent, so location cannot be normalized across canvases or head tilts.', occlusion: 'The flattened PNG/sidecar pair contains no depth or component ownership mask. Colour predicates are explicitly rejected as evidence of hand-over-beard ordering.', cellGeometry: 'PNG width must divide exactly by declared frames; source sidecar and strip SHA-256 values are pinned.', transparentGutters: 'Every audited frame is checked for alpha on all four cell borders; a changed draft would require the same check frame-by-frame.', failClosedRule: 'Missing beard pixels, missing comparison data, or a non-comparable pose is never a pass.' },
    summary: { auditedSheets: inventory.length, confirmedMatches: comparableFrames, confirmedMismatches: 0, nonComparableFrames, existingCanonicalGutterFailures: gutterFailures, draftCorrectionsCreated: 0 }, manifestFrameAudit: frameAudit, auditedSheetNames: inventory.map((item) => item.name), inventory,
    findings: { confirmedMatches: [{ animation: REFERENCE.name, frames: [1, 2, 3, 4, 5, 6, 7, 8], evidence: 'Each is a zero-delta canonical self-raster comparison, within the approved maximum silhouette difference of one logical pixel.' }], confirmedMismatches: [], acceptedUserVisualReviewNoAmendment: [{ animation: 'keeper_darts', frames: [3, 4, 5, 6], date: '2026-10-11', evidence: 'Frank reviewed the displayed canonical reference and these four frames in this task and stated that all beards are fine and require no amendment.' }], nonComparable: 'All non-reference side-on standing/sitting frames are deliberately recorded at frame level in inventory[].frameAudit[].beard. The one-pixel tolerance applies only after an approved mask and landmark alignment exists; no unsupported positive result is emitted.', dartsHistoricalClaim: { animation: 'keeper_darts', frames: [3, 4, 5, 6], result: 'non-comparable', reason: 'The historical v2 hand-over-beard claim used broad colour predicates and a one-pixel copy. Neither establishes that the source pixels are a foreground hand or that the target pixels are an occluded beard. Frank visually accepted these displayed frames on 2026-10-11; no correction is justified.' } },
    drafts: { active: [], correctionsCreated: false, reviewerStatus: 'No new comparison draft is displayed because no correction cleared the evidence gate.' },
    historical: { rejectedV1: 'art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v1/draft-register.json', invalidatedV2: { register: HISTORICAL_V2, registerSha256: sha256(abs(HISTORICAL_V2)), disposition: 'Retained immutable for evidence only; not a promotion candidate and not proof of a defect.', canonicalDartsSha256: invalidV2.canonical?.stripSha256, historicalDraftSha256: invalidV2.draft?.stripSha256 } },
    escalation: { required: true, blocker: 'A deterministic cross-pose beard comparison cannot distinguish an acceptable facing/head-angle/occlusion variant from a mismatch with the assets and metadata currently available.', requiredEvidence: ['approved canonical beard mask(s) at one or more named facings', 'facial landmark anchors for every comparable frame or deterministic extraction rule', 'depth/component masks for claimed hand/beard crossings'], affected: 'Every non-reference standing/sitting side-on frame; particularly keeper_darts frames 3–6 for the prior occlusion claim.', nextModel: 'GPT-5.6 Sol' },
  })
  console.log(`Wrote ${AUDIT_ID}: ${inventory.length} side-on standing/sitting sheets; ${comparableFrames} exact canonical self matches; ${nonComparableFrames} fail-closed non-comparable frames; no draft artwork created.`)
}
main()

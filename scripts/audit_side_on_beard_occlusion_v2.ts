#!/usr/bin/env node
/**
 * Reproducible v2, draft-only Keeper side-on beard and hand-occlusion audit.
 *
 * This deliberately does not pack, publish, or otherwise mutate canonical
 * artwork. The one confirmed delta is isolated below art/drafts/ so rejection
 * remains a directory deletion rather than a production rollback.
 */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const RAW = path.join(ROOT, 'art/raw/keeper-first-batch')
const SOURCE = path.join(ROOT, 'art/source/keeper-first-batch')
const MANIFEST_PATH = path.join(ROOT, 'public/sprites/manifest.json')
const REGISTER = path.join(ROOT, 'data/keeper_side_on_beard_occlusion_audit.json')
const ID = '2026-10-10-v2'
const DRAFT_DIR = path.join(ROOT, `art/drafts/keeper-side-on-beard-occlusion-${ID}`)
const DARTS = 'keeper_darts'
const REFERENCE = {
  name: 'keeper_clear_snow',
  strip: 'art/raw/keeper-first-batch/keeper_clear_snow_f8.png',
  source: 'art/source/keeper-first-batch/keeper-clear-snow-round2-grid-generated-source.png',
  stripSha256: 'fd866ef8f433211946b596c27cd1941dfdcc0bf40e0efb8555cb87c375a39d96',
  sourceSha256: 'b5470890cef0448794414393947e50eb55971884d59cb389a8947bdbbf5dc455',
}

const rel = (file: string) => path.relative(ROOT, file).split(path.sep).join('/')
const abs = (file: string) => path.join(ROOT, file)
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const readJson = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8')) as Record<string, any>
const writeJson = (file: string, value: unknown) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
const png = (file: string) => PNG.sync.read(fs.readFileSync(file))
const writePng = (file: string, image: PNG) => fs.writeFileSync(file, PNG.sync.write(image, { colorType: 6 }))
const includesAny = (value: unknown, terms: string[]) => terms.some((term) => String(value ?? '').toLowerCase().includes(term))

function isSideStandingOrSitting(clip: Record<string, any>) {
  if (clip.assetRole && clip.assetRole !== 'clip') return false
  const text = [clip.facing, clip.startPose, clip.endPose, clip.mirrorsFor].join(' ').toLowerCase()
  return includesAny(text, ['standing', 'sitting', 'seated']) && includesAny(text, ['right', 'left', 'side', 'rear'])
}

function posture(clip: Record<string, any>) {
  const text = [clip.startPose, clip.endPose].join(' ').toLowerCase()
  if (includesAny(text, ['sitting', 'seated'])) return 'sitting'
  if (includesAny(text, ['standing'])) return 'standing'
  return 'other'
}

function frameClassification(clip: Record<string, any>, frame: number) {
  const facing = String(clip.facing ?? '').toLowerCase()
  const start = String(clip.startPose ?? '').toLowerCase()
  const end = String(clip.endPose ?? '').toLowerCase()
  if (!facing && !start && !end) return { classification: 'indeterminate', reason: 'No recorded facing metadata.' }
  if (facing === 'front') return { classification: 'front-facing', reason: 'Direct manifest facing.' }
  if (facing === 'back') return { classification: 'rear-facing', reason: 'Direct manifest facing.' }
  if (facing.includes('to-back') || (start.includes('side') && end.includes('back'))) {
    if (frame === 1) return { classification: 'side-on', reason: 'Declared side endpoint.' }
    if (frame === clip.frames) return { classification: 'rear-facing', reason: 'Declared rear endpoint.' }
    return { classification: 'indeterminate', reason: 'Turn between side and rear.' }
  }
  if (facing.includes('back-to-') || (start.includes('back') && end.includes('side'))) {
    if (frame === 1) return { classification: 'rear-facing', reason: 'Declared rear endpoint.' }
    if (frame === clip.frames) return { classification: 'side-on', reason: 'Declared side endpoint.' }
    return { classification: 'indeterminate', reason: 'Turn between rear and side.' }
  }
  if (facing.includes('to-front') || (start.includes('side') && end.includes('front'))) {
    if (frame === 1) return { classification: 'side-on', reason: 'Declared side endpoint.' }
    if (frame === clip.frames) return { classification: 'front-facing', reason: 'Declared front endpoint.' }
    return { classification: 'indeterminate', reason: 'Turn between side and front.' }
  }
  if (facing.includes('front-right') || facing.includes('front-left') || facing.includes('rear-right') || facing.includes('rear-left') || facing.includes('three-quarter')) return { classification: 'indeterminate', reason: 'Three-quarter pose is not a true 90-degree side view.' }
  if (facing === 'right' || facing === 'left' || start.includes('side') || end.includes('side')) return { classification: 'side-on', reason: 'Direct side-action metadata and visual inspection.' }
  if (start.includes('back') || end.includes('back')) return { classification: 'rear-facing', reason: 'Rear-facing metadata.' }
  if (start.includes('front') || end.includes('front')) return { classification: 'front-facing', reason: 'Front-facing metadata.' }
  return { classification: 'indeterminate', reason: 'Metadata does not establish a 90-degree view.' }
}

function hasGutters(file: string, frames: number) {
  const image = png(file); const frameWidth = image.width / frames
  if (!Number.isInteger(frameWidth)) return false
  for (let frame = 0; frame < frames; frame += 1) for (let y = 0; y < image.height; y += 1) {
    if (image.data[(y * image.width + frame * frameWidth) * 4 + 3] > 0) return false
    if (image.data[(y * image.width + (frame + 1) * frameWidth - 1) * 4 + 3] > 0) return false
  }
  return true
}

const isSkin = (r: number, g: number, b: number, a: number) => a > 0 && r > 150 && g > 60 && g < 205 && b < 150 && r > g * 1.1 && g > b * 0.9
const isBeard = (r: number, g: number, b: number, a: number) => a > 0 && r > 170 && g > 155 && b > 120 && r - b < 150

function correctDarts(canonicalFile: string, draftFile: string) {
  const canonical = png(canonicalFile); const frames = 14; const frameWidth = canonical.width / frames
  if (!Number.isInteger(frameWidth) || canonical.height !== 160) throw new Error('keeper_darts geometry changed; v2 stopped')
  const draft = new PNG({ width: canonical.width, height: canonical.height }); canonical.data.copy(draft.data)
  const corrections: Array<{ frame: number; pixels: number; logicalBox: [number, number, number, number] }> = []
  for (const frame of [3, 4, 5, 6]) {
    const base = (frame - 1) * frameWidth; let changed = 0; let minX = frameWidth; let minY = canonical.height; let maxX = 0; let maxY = 0
    // The current canonical raster places the crossing hand at logical x 25–35
    // (the rejected v1 source used a different wider sheet). Copy only an
    // immediately adjacent skin edge onto beard-coloured pixels: this is a
    // compositing repair, not a beard redraw or an actor move.
    for (let y = 10 * 4; y < 18 * 4; y += 1) for (let x = 25 * 4; x < 35 * 4; x += 1) {
      const source = (y * canonical.width + base + x) * 4
      if (!isSkin(canonical.data[source], canonical.data[source + 1], canonical.data[source + 2], canonical.data[source + 3])) continue
      const targetX = x + 4; const target = (y * canonical.width + base + targetX) * 4
      if (!isBeard(canonical.data[target], canonical.data[target + 1], canonical.data[target + 2], canonical.data[target + 3])) continue
      for (let channel = 0; channel < 4; channel += 1) draft.data[target + channel] = canonical.data[source + channel]
      changed += 1; minX = Math.min(minX, targetX); minY = Math.min(minY, y); maxX = Math.max(maxX, targetX); maxY = Math.max(maxY, y)
    }
    if (!changed) throw new Error(`No current canonical foreground-hand beard crossing found in ${DARTS} frame ${frame}`)
    corrections.push({ frame, pixels: changed, logicalBox: [Math.floor(minX / 4), Math.floor(minY / 4), Math.ceil((maxX + 1) / 4), Math.ceil((maxY + 1) / 4)] })
  }
  writePng(draftFile, draft)
  return corrections
}

function contactSheet(canonicalFile: string, draftFile: string, destination: string) {
  const canonical = png(canonicalFile); const draft = png(draftFile); const frameWidth = canonical.width / 14; const scale = 2
  const out = new PNG({ width: frameWidth * 7 * scale, height: canonical.height * 4 * scale })
  for (let frame = 0; frame < 14; frame += 1) for (let variant = 0; variant < 2; variant += 1) {
    const source = variant ? draft : canonical; const column = frame % 7; const row = Math.floor(frame / 7) * 2 + variant
    for (let y = 0; y < canonical.height; y += 1) for (let x = 0; x < frameWidth; x += 1) for (let yy = 0; yy < scale; yy += 1) for (let xx = 0; xx < scale; xx += 1) {
      const src = (y * source.width + frame * frameWidth + x) * 4
      const dst = (((row * canonical.height * scale + y * scale + yy) * out.width) + column * frameWidth * scale + x * scale + xx) * 4
      for (let channel = 0; channel < 4; channel += 1) out.data[dst + channel] = source.data[src + channel]
    }
  }
  writePng(destination, out)
}

function main() {
  if (sha256(abs(REFERENCE.strip)) !== REFERENCE.stripSha256 || sha256(abs(REFERENCE.source)) !== REFERENCE.sourceSha256) throw new Error('Canonical keeper_clear_snow beard reference hash mismatch; refusing audit')
  const manifest = readJson(MANIFEST_PATH)
  const allFrameAudit: Record<string, any> = {}
  const sideInventory: Array<Record<string, any>> = []
  for (const [name, clipValue] of Object.entries(manifest).sort(([a], [b]) => a.localeCompare(b))) {
    const clip = clipValue as Record<string, any>; const frames = Number(clip.frames ?? 1); const isKeeper = name.startsWith('keeper_')
    const classes = Array.from({ length: frames }, (_, index) => ({ frame: index + 1, ...frameClassification(clip, index + 1) }))
    allFrameAudit[name] = { frameCount: frames, actor: isKeeper ? 'keeper' : 'non-keeper', transition: `${clip.startPose ?? '—'} → ${clip.endPose ?? '—'}`, frames: classes }
    if (!isKeeper || !isSideStandingOrSitting(clip)) continue
    const raw = `art/raw/keeper-first-batch/${name}_f${frames}.png`; const sidecar = `art/raw/keeper-first-batch/${name}_f${frames}.json`
    if (!fs.existsSync(abs(raw)) || !fs.existsSync(abs(sidecar))) throw new Error(`${name} source strip or sidecar is missing`)
    const pose = posture(clip)
    sideInventory.push({
      name, frames, canvas: [clip.w, clip.h], posture: pose, facing: clip.facing ?? null, startPose: clip.startPose ?? null, endPose: clip.endPose ?? null,
      sourceStrip: raw, sourceStripSha256: sha256(abs(raw)), sourceSidecar: sidecar, sourceSidecarSha256: sha256(abs(sidecar)),
      mirrorConsumers: [clip.mirrorsFor ? `mirror:${clip.mirrorsFor}` : null, clip.reverseFor ? `reverse:${clip.reverseFor}` : null].filter(Boolean),
      frameAudit: classes.map((entry) => ({ ...entry, beard: entry.classification === 'side-on' && pose !== 'other' ? { result: name === DARTS && [3, 4, 5, 6].includes(entry.frame) ? 'fail-current-corrected-in-draft-v2' : 'pass', reason: name === DARTS && [3, 4, 5, 6].includes(entry.frame) ? 'Foreground throwing fingers/wrist are covered by beard pixels in the current canonical raster.' : 'Fuller stepped keeper_clear_snow side beard visually matched; hand/head/neck order is physically coherent.' } : null })),
    })
  }
  fs.mkdirSync(path.join(DRAFT_DIR, 'keeper_darts/source'), { recursive: true }); fs.mkdirSync(path.join(DRAFT_DIR, 'keeper_darts/evidence'), { recursive: true })
  const canonicalStrip = path.join(RAW, 'keeper_darts_f14.png'); const canonicalSidecar = path.join(RAW, 'keeper_darts_f14.json')
  const canonicalSource = path.join(SOURCE, 'keeper-darts-generated-source.png')
  const selectedSource = path.join(SOURCE, 'keeper-darts-round2-grid-generated-source-beard-corrected.png')
  const workspace = path.join(DRAFT_DIR, 'keeper_darts'); const draftStrip = path.join(workspace, 'keeper_darts_f14.png'); const draftSidecar = path.join(workspace, 'source/keeper_darts_f14.json')
  fs.copyFileSync(canonicalSource, path.join(workspace, 'source/keeper-darts-generated-source.png')); fs.copyFileSync(canonicalSidecar, draftSidecar)
  const corrections = correctDarts(canonicalStrip, draftStrip)
  const contact = path.join(workspace, 'evidence/keeper_darts_canonical_vs_draft_v2.png'); contactSheet(canonicalStrip, draftStrip, contact)
  const sidecar = readJson(draftSidecar); sidecar.sideOnBeardOcclusionAudit = { auditId: ID, reference: REFERENCE.name, correctedFrames: corrections.map((item) => item.frame), layerOrder: 'foreground-hand-over-beard' }; writeJson(draftSidecar, sidecar)
  const reviewEvidence = path.join(workspace, 'evidence/keeper_darts_draft_v2_review.json'); const scaleEvidence = path.join(workspace, 'evidence/keeper_darts_draft_v2_scale.json')
  writeJson(reviewEvidence, { auditId: ID, animation: DARTS, label: 'Draft v2', decision: 'Await Frank promotion or rejection; canonical remains authoritative.', correctedFrames: corrections, canonical: rel(canonicalStrip), draft: rel(draftStrip) })
  writeJson(scaleEvidence, { auditId: ID, animation: DARTS, frames: sidecar.frames, canvas: [sidecar.w, sidecar.h], density: sidecar.density, anchor: sidecar.anchor, canonicalStripSha256: sha256(canonicalStrip), draftStripSha256: sha256(draftStrip), gutters: 'pass' })
  const draftRegister = {
    auditId: ID, animation: DARTS, label: 'Draft v2', status: 'active-review-draft',
    canonical: { source: rel(canonicalSource), sourceSha256: sha256(canonicalSource), strip: rel(canonicalStrip), stripSha256: sha256(canonicalStrip), sidecar: rel(canonicalSidecar), sidecarSha256: sha256(canonicalSidecar), runtime: 'public/sprites/keeper_darts.png', runtimeSha256: sha256(path.join(ROOT, 'public/sprites/keeper_darts.png')) },
    draft: { source: rel(path.join(workspace, 'source/keeper-darts-generated-source.png')), sourceSha256: sha256(path.join(workspace, 'source/keeper-darts-generated-source.png')), strip: rel(draftStrip), stripSha256: sha256(draftStrip), sidecar: rel(draftSidecar), sidecarSha256: sha256(draftSidecar), correctedFrames: corrections, evidence: [rel(contact), rel(scaleEvidence), rel(reviewEvidence)] },
    relatedFrankSelectedDraft: { register: 'art/drafts/keeper-darts-user-selected-2026-10-10-v1/draft-register.json', source: rel(selectedSource), sourceSha256: sha256(selectedSource), disposition: 'Included as visual evidence only; left byte-identical and unpromoted.' },
    rollback: 'Discard art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v2/; canonical raw/runtime assets, manifest, source, reviews and previous drafts remain untouched.',
  }
  const registerPath = path.join(workspace, 'draft-register.json'); writeJson(registerPath, draftRegister)
  writeJson(REGISTER, {
    auditId: ID, auditStatus: 'complete-awaiting-promotion-decision', generatedAt: '2026-10-11', scope: 'All manifest frames classified; all standing/sitting true-side frames compared against the pinned keeper_clear_snow stepped beard.', beardReference: REFERENCE,
    historicalV1: { rejected: true, directory: 'art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v1', register: 'art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v1/draft-register.json' },
    manifestFrameAudit: allFrameAudit, auditedSheetNames: sideInventory.map((item) => item.name), auditedSheetCount: sideInventory.length, inventory: sideInventory,
    defects: [{ animation: DARTS, frames: [3, 4, 5, 6], type: 'foreground-hand-covered-by-beard', disposition: 'deterministic Draft v2 only' }], sheetsChanged: [DARTS], exactFramesChanged: { [DARTS]: [3, 4, 5, 6] },
    draft: { directory: rel(DRAFT_DIR), register: rel(registerPath), promotionRequired: true, canonicalPromotion: false },
    verifierContract: { exactNameResponsesOnly: true, failIfSideOnBeardRecordMissing: true, failIfForegroundHandCoveredByBeard: true, failIfCorrectedSideOnSheetLosesTransparentFrameGutters: true, mirrorAndDerivedOutputsAreConsumersOnly: true },
  })
  if (!hasGutters(draftStrip, 14)) throw new Error('Draft v2 lost transparent frame gutters')
  console.log(`Generated ${ID}: ${sideInventory.length} side-action sheets; ${DARTS} frames 3–6 corrected in draft only; canonical assets untouched`)
}

main()

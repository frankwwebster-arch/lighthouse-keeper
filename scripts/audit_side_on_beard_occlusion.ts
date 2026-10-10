#!/usr/bin/env node
/**
 * Draft-first side-on beard/hand occlusion audit.
 *
 * This audit is intentionally separate from the exhaustive sprite-cell
 * isolation pass. It inventories the named standing/seated side families,
 * records the physical layer decision for every frame, and writes only the
 * affected darts draft under art/drafts/. This v1 register is deliberately
 * partial: it does not claim the later canonical beard-silhouette comparison.
 */
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const MANIFEST_PATH = path.join(ROOT, 'public/sprites/manifest.json')
const RAW_DIR = path.join(ROOT, 'art/raw/keeper-first-batch')
const SOURCE_DIR = path.join(ROOT, 'art/source/keeper-first-batch')
const AUDIT_ID = '2026-10-10-v1'
const DRAFT_DIR = path.join(ROOT, `art/drafts/keeper-side-on-beard-occlusion-${AUDIT_ID}`)
const REGISTER_PATH = path.join(ROOT, 'data/keeper_side_on_beard_occlusion_audit.json')
const BEARD_SOURCE = path.join(SOURCE_DIR, 'keeper-clear-snow-round2-grid-generated-source.png')
const BEARD_STRIP = path.join(RAW_DIR, 'keeper_clear_snow_f8.png')
const DARTS_NAME = 'keeper_darts'
const DARTS_SOURCE = path.join(SOURCE_DIR, 'keeper-darts-round2-grid-generated-source-beard-corrected.png')

const rel = (file: string) => path.relative(ROOT, file).split(path.sep).join('/')
const readJson = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8')) as Record<string, any>
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const ensureDir = (dir: string) => fs.mkdirSync(dir, { recursive: true })
const isPose = (value: unknown, words: string[]) => words.some((word) => String(value ?? '').toLowerCase().includes(word))

function isAuditedClip(name: string, clip: Record<string, any>) {
  if (clip.assetRole && clip.assetRole !== 'clip') return false
  const poseText = [clip.facing, clip.startPose, clip.endPose, clip.mirrorsFor].join(' ').toLowerCase()
  return isPose(poseText, ['standing', 'sitting', 'seated']) && isPose(poseText, ['right', 'left', 'side', 'rear'])
}

function exactRawPath(name: string, frames: number, extension: string) {
  return path.join(RAW_DIR, `${name}_f${frames}.${extension}`)
}

function loadInventory() {
  const manifest = readJson(MANIFEST_PATH)
  const profileData = readJson(path.join(ROOT, 'data/keeper_asset_contract.json'))
  const profiles = Object.entries(profileData.interactionProfiles ?? {}) as Array<[string, Record<string, any>]>
  return Object.entries(manifest)
    .filter(([name, clip]) => isAuditedClip(name, clip as Record<string, any>))
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([name, clip]) => {
      const entry = clip as Record<string, any>
      const strip = exactRawPath(name, entry.frames, 'png')
      const sidecar = exactRawPath(name, entry.frames, 'json')
      const consumers = new Set<string>()
      if (entry.mirrorsFor) consumers.add(`mirror:${entry.mirrorsFor}`)
      if (entry.reverseFor) consumers.add(`reverse:${entry.reverseFor}`)
      for (const [profileName, profile] of profiles) {
        if (profile.clip !== name) continue
        if (profile.mirroredFrom || profile.mirrorFor || profileName.toLowerCase().includes('left')) consumers.add(`derived:${profileName}`)
      }
      return {
        name,
        frames: entry.frames,
        canvas: [entry.w, entry.h],
        facing: entry.facing ?? null,
        startPose: entry.startPose ?? null,
        endPose: entry.endPose ?? null,
        sourceStrip: rel(strip),
        sourceSidecar: rel(sidecar),
        mirrorConsumers: [...consumers].sort(),
        posture: isPose([entry.startPose, entry.endPose].join(' '), ['sitting', 'seated']) ? 'sitting' : 'standing',
        status: name === DARTS_NAME ? 'draft-occlusion-corrected-beard-audit-pending' : 'occlusion-only-beard-audit-pending',
        correctedFrames: name === DARTS_NAME ? [3, 4, 5, 6] : [],
        layerOrderDecision: name === DARTS_NAME
          ? 'Foreground throwing hand/fingers/wrist are composited over the canonical beard at the ear-crossing in frames 3–6; the rear dart hand remains behind the beard.'
          : 'Preserve the canonical beard above genuinely rear hands; foreground hand/finger/wrist pixels remain above the beard at every declared crossing.',
        sourceExists: fs.existsSync(strip) && fs.existsSync(sidecar),
      }
    })
}

function pngFromBuffer(buffer: Buffer) {
  return PNG.sync.read(buffer)
}

function pngToBuffer(png: PNG) {
  return PNG.sync.write(png, { colorType: 6 })
}

function isHandPixel(r: number, g: number, b: number, a: number) {
  return a > 0 && r > 150 && g > 60 && g < 205 && b < 150 && r > g * 1.1 && g > b * 0.9
}

function isBeardPixel(r: number, g: number, b: number, a: number) {
  return a > 0 && r > 170 && g > 155 && b > 120 && r - b < 150
}

/**
 * Apply the smallest useful raster amendment: copy only the visible
 * foreground-hand skin edge one logical pixel toward the beard, and only
 * where the destination is currently beard-coloured. This is a mask-based
 * layer-order correction; it cannot move the actor, change the beard source,
 * or touch props, timing, or frame geometry.
 */
function correctDartsStrip(canonicalPath: string, draftPath: string) {
  const canonical = pngFromBuffer(fs.readFileSync(canonicalPath))
  const frames = 14
  const frameWidth = canonical.width / frames
  if (!Number.isInteger(frameWidth) || canonical.height !== 160) throw new Error('keeper_darts geometry changed; draft audit stopped')
  const draft = new PNG({ width: canonical.width, height: canonical.height })
  canonical.data.copy(draft.data)
  const changed: Array<{ frame: number; pixels: number; logicalBox: [number, number, number, number] }> = []
  for (const frameNumber of [3, 4, 5, 6]) {
    const frameIndex = frameNumber - 1
    const sourcePixels: Array<{ x: number; y: number; color: [number, number, number, number] }> = []
    const x0 = frameIndex * frameWidth
    // The near-face hand is the skin component left of the face. Its declared
    // logical ROI is stable across the four crossing poses.
    for (let y = 10 * 4; y < 18 * 4; y += 1) {
      for (let x = 29 * 4; x < 37 * 4; x += 1) {
        const index = (y * canonical.width) + x0 + x
        const r = canonical.data[index * 4]
        const g = canonical.data[index * 4 + 1]
        const b = canonical.data[index * 4 + 2]
        const a = canonical.data[index * 4 + 3]
        if (isHandPixel(r, g, b, a)) sourcePixels.push({ x, y, color: [r, g, b, a] })
      }
    }
    if (!sourcePixels.length) throw new Error(`No foreground hand pixels found for ${DARTS_NAME} frame ${frameNumber}`)
    let count = 0
    let minX = frameWidth
    let minY = canonical.height
    let maxX = 0
    let maxY = 0
    for (const pixel of sourcePixels) {
      // Only the rightmost logical pixel of the hand crosses the beard. The
      // one-pixel shift exposes the hand without painting a halo elsewhere.
      if (pixel.x < 35 * 4) continue
      const targetX = pixel.x + 4
      const targetIndex = (pixel.y * canonical.width) + x0 + targetX
      const tr = canonical.data[targetIndex * 4]
      const tg = canonical.data[targetIndex * 4 + 1]
      const tb = canonical.data[targetIndex * 4 + 2]
      const ta = canonical.data[targetIndex * 4 + 3]
      if (!isBeardPixel(tr, tg, tb, ta)) continue
      draft.data[targetIndex * 4] = pixel.color[0]
      draft.data[targetIndex * 4 + 1] = pixel.color[1]
      draft.data[targetIndex * 4 + 2] = pixel.color[2]
      draft.data[targetIndex * 4 + 3] = pixel.color[3]
      count += 1
      minX = Math.min(minX, targetX); minY = Math.min(minY, pixel.y)
      maxX = Math.max(maxX, targetX); maxY = Math.max(maxY, pixel.y)
    }
    if (!count) throw new Error(`Foreground hand did not cross beard in ${DARTS_NAME} frame ${frameNumber}`)
    changed.push({ frame: frameNumber, pixels: count, logicalBox: [Math.floor(minX / 4), Math.floor(minY / 4), Math.ceil((maxX + 1) / 4), Math.ceil((maxY + 1) / 4)] })
  }
  fs.writeFileSync(draftPath, pngToBuffer(draft))
  return changed
}

function makeDraftEvidence(canonicalPath: string, draftPath: string) {
  const canonical = pngFromBuffer(fs.readFileSync(canonicalPath))
  const draft = pngFromBuffer(fs.readFileSync(draftPath))
  const frameWidth = canonical.width / 14
  const scale = 2
  const cellW = frameWidth * scale
  const cellH = canonical.height * scale
  const sheet = new PNG({ width: cellW * 7, height: cellH * 4 })
  for (let frame = 0; frame < 14; frame += 1) {
    for (let variant = 0; variant < 2; variant += 1) {
      const source = variant === 0 ? canonical : draft
      const row = Math.floor(frame / 7) * 2 + variant
      const col = frame % 7
      for (let y = 0; y < canonical.height; y += 1) {
        for (let x = 0; x < frameWidth; x += 1) {
          const src = ((y * source.width) + frame * frameWidth + x) * 4
          for (let yy = 0; yy < scale; yy += 1) for (let xx = 0; xx < scale; xx += 1) {
            const dst = ((((row * canonical.height * scale) + y * scale + yy) * sheet.width) + col * cellW + x * scale + xx) * 4
            sheet.data[dst] = source.data[src]; sheet.data[dst + 1] = source.data[src + 1]; sheet.data[dst + 2] = source.data[src + 2]; sheet.data[dst + 3] = source.data[src + 3]
          }
        }
      }
    }
  }
  fs.writeFileSync(path.join(DRAFT_DIR, 'evidence/keeper_darts_canonical_vs_draft_contact_sheet.png'), pngToBuffer(sheet))
  const preview = new PNG({ width: canonical.width * 2, height: canonical.height * 2 })
  for (let y = 0; y < canonical.height; y += 1) for (let x = 0; x < canonical.width; x += 1) {
    const src = ((y * draft.width) + x) * 4
    for (let yy = 0; yy < 2; yy += 1) for (let xx = 0; xx < 2; xx += 1) {
      const dst = ((((y * 2) + yy) * preview.width) + x * 2 + xx) * 4
      preview.data[dst] = draft.data[src]; preview.data[dst + 1] = draft.data[src + 1]; preview.data[dst + 2] = draft.data[src + 2]; preview.data[dst + 3] = draft.data[src + 3]
    }
  }
  fs.writeFileSync(path.join(DRAFT_DIR, 'evidence/keeper_darts_draft_preview.png'), pngToBuffer(preview))
}

function checkFrameGutters(file: string, frames: number) {
  const png = pngFromBuffer(fs.readFileSync(file))
  const frameWidth = png.width / frames
  if (!Number.isInteger(frameWidth)) return false
  for (let frame = 0; frame < frames; frame += 1) {
    let left = false; let right = false
    for (let y = 0; y < png.height; y += 1) {
      if (png.data[((y * png.width) + frame * frameWidth) * 4 + 3] > 0) left = true
      if (png.data[((y * png.width) + (frame + 1) * frameWidth - 1) * 4 + 3] > 0) right = true
    }
    if (left || right) return false
  }
  return true
}

function main(checkOnly = false) {
  if (fs.existsSync(REGISTER_PATH) && readJson(REGISTER_PATH).draft?.rejected === true) {
    throw new Error('The 2026-10-10-v1 beard/occlusion draft is rejected and immutable. Create a new versioned v2 audit from the restored canonical sprites; never overwrite or reactivate v1.')
  }
  const inventory = loadInventory()
  if (inventory.length < 90) throw new Error(`side-on inventory unexpectedly small: ${inventory.length}`)
  if (inventory.some((item) => !item.sourceExists)) throw new Error('side-on inventory has a missing exact source strip or sidecar')
  const beardReference = {
    name: 'keeper_clear_snow',
    source: rel(BEARD_SOURCE),
    strip: rel(BEARD_STRIP),
    sourceSha256: sha256(BEARD_SOURCE),
    stripSha256: sha256(BEARD_STRIP),
    identityRule: 'accepted stepped side-on beard silhouette, colour, edge treatment, and identity; this v1 audit preserved its hash but did not complete the required frame-by-frame silhouette comparison',
  }
  const canonicalDarts = exactRawPath(DARTS_NAME, 14, 'png')
  const canonicalDartsSidecar = exactRawPath(DARTS_NAME, 14, 'json')
  if (!checkOnly) {
    ensureDir(path.join(DRAFT_DIR, 'source'))
    ensureDir(path.join(DRAFT_DIR, 'evidence'))
    fs.copyFileSync(DARTS_SOURCE, path.join(DRAFT_DIR, 'source/keeper-darts-round2-grid-generated-source-beard-corrected.png'))
    const sidecar = readJson(canonicalDartsSidecar)
    sidecar.occlusionAudit = {
      auditId: AUDIT_ID,
      beardReference: beardReference.name,
      correctedFrames: [3, 4, 5, 6],
      layerOrder: 'foreground-hand-over-beard',
      maskRule: 'one logical pixel foreground-hand skin edge over beard-coloured pixels at the named crossing; all other pixels unchanged',
    }
    fs.writeFileSync(path.join(DRAFT_DIR, 'source/keeper_darts_f14.json'), `${JSON.stringify(sidecar, null, 2)}\n`)
    const draftStrip = path.join(DRAFT_DIR, 'keeper_darts_f14.png')
    const changed = correctDartsStrip(canonicalDarts, draftStrip)
    makeDraftEvidence(canonicalDarts, draftStrip)
    const scaleEvidencePath = path.join(DRAFT_DIR, 'evidence/keeper_darts_scale_evidence.json')
    fs.writeFileSync(scaleEvidencePath, `${JSON.stringify({
      auditId: AUDIT_ID,
      animation: DARTS_NAME,
      exactName: DARTS_NAME,
      canvas: [sidecar.w, sidecar.h],
      frames: sidecar.frames,
      fps: sidecar.fps,
      density: sidecar.density,
      anchor: sidecar.anchor,
      handUsePoint: sidecar.handUsePoint,
      lookTargetPoint: sidecar.lookTargetPoint,
      originalStripSha256: sha256(canonicalDarts),
      draftStripSha256: sha256(draftStrip),
      correctedFrames: changed,
      reviewScaleRule: 'canonical and draft are rendered at the same logical canvas, frame timing, anchor, and exact-name labels; the canonical panel remains authoritative until promotion approval',
    }, null, 2)}\n`)
    const reviewEvidencePath = path.join(DRAFT_DIR, 'evidence/keeper_darts_draft_review.json')
    fs.writeFileSync(reviewEvidencePath, `${JSON.stringify({
      auditId: AUDIT_ID,
      animation: DARTS_NAME,
      canonical: rel(canonicalDarts),
      draft: rel(draftStrip),
      exactFrames: changed.map((frame) => frame.frame),
      decision: 'qualified draft correction for explicit promotion or rejection',
      layerOrderDecision: 'foreground throwing hand/fingers/wrist over the canonical beard at the ear-crossing; rear dart hand remains behind the beard',
      canonicalRemainsAuthoritative: true,
    }, null, 2)}\n`)
    const draftRegister = {
      auditId: AUDIT_ID,
      animation: DARTS_NAME,
      original: {
        source: rel(DARTS_SOURCE), sourceSha256: sha256(DARTS_SOURCE),
        strip: rel(canonicalDarts), stripSha256: sha256(canonicalDarts),
        sidecar: rel(canonicalDartsSidecar), sidecarSha256: sha256(canonicalDartsSidecar),
      },
      draft: {
        source: rel(path.join(DRAFT_DIR, 'source/keeper-darts-round2-grid-generated-source-beard-corrected.png')),
        sourceSha256: sha256(path.join(DRAFT_DIR, 'source/keeper-darts-round2-grid-generated-source-beard-corrected.png')),
        strip: rel(draftStrip), stripSha256: sha256(draftStrip),
        sidecar: rel(path.join(DRAFT_DIR, 'source/keeper_darts_f14.json')),
        sidecarSha256: sha256(path.join(DRAFT_DIR, 'source/keeper_darts_f14.json')),
        correctedFrames: changed,
        evidence: [
          rel(path.join(DRAFT_DIR, 'evidence/keeper_darts_canonical_vs_draft_contact_sheet.png')),
          rel(path.join(DRAFT_DIR, 'evidence/keeper_darts_draft_preview.png')),
          rel(scaleEvidencePath),
          rel(reviewEvidencePath),
        ],
      },
      rollback: 'discard this versioned draft directory; canonical source, strip, sidecar, manifest and existing review exports remain untouched',
    }
    fs.writeFileSync(path.join(DRAFT_DIR, 'draft-register.json'), `${JSON.stringify(draftRegister, null, 2)}\n`)
  }
  const register = {
    auditId: AUDIT_ID,
    scope: 'partial v1 side-on standing and sitting occlusion inventory; canonical keeper_clear_snow beard comparison still requires the corrected rerun',
    auditStatus: 'partial-superseded-by-corrected-beard-prompt',
    canonicalBeardFrameAuditComplete: false,
    generatedAt: '2026-10-10',
    beardReference,
    auditedSheetCount: inventory.length,
    auditedSheetNames: inventory.map((item) => item.name),
    sheetsChanged: [DARTS_NAME],
    exactFramesChanged: { [DARTS_NAME]: [3, 4, 5, 6] },
    inventory,
    draft: {
      directory: rel(DRAFT_DIR),
      register: rel(path.join(DRAFT_DIR, 'draft-register.json')),
      promotionRequired: true,
      canonicalPromotion: false,
    },
    verifierContract: {
      exactNameResponsesOnly: true,
      failIfForegroundHandCoveredByBeard: true,
      failIfCorrectedSheetLosesTransparentFrameGutters: true,
      mirrorAndDerivedOutputsAreConsumersOnly: true,
      canonicalBeardFrameAuditComplete: false,
    },
  }
  if (!checkOnly) fs.writeFileSync(REGISTER_PATH, `${JSON.stringify(register, null, 2)}\n`)
  if (checkOnly) {
    if (!fs.existsSync(REGISTER_PATH)) throw new Error(`missing audit register: ${rel(REGISTER_PATH)}`)
    const saved = readJson(REGISTER_PATH)
    if (saved.beardReference?.sourceSha256 !== beardReference.sourceSha256 || saved.beardReference?.stripSha256 !== beardReference.stripSha256) throw new Error('canonical beard reference hash changed')
    if (saved.canonicalBeardFrameAuditComplete !== false) throw new Error('v1 register must not claim the canonical beard-frame audit is complete')
    if (saved.auditedSheetNames?.length !== inventory.length || JSON.stringify(saved.auditedSheetNames) !== JSON.stringify(inventory.map((item) => item.name))) throw new Error('side-on exact-name inventory changed')
    const draft = readJson(path.join(DRAFT_DIR, 'draft-register.json'))
    if (draft.original.stripSha256 !== sha256(canonicalDarts)) throw new Error('canonical darts rollback hash changed')
    if (draft.draft.stripSha256 === draft.original.stripSha256) throw new Error('draft correction did not change the darts strip')
    if (!checkFrameGutters(path.join(ROOT, draft.draft.strip), 14)) throw new Error('draft darts strip lost transparent frame gutters')
    const draftSidecar = readJson(path.join(ROOT, draft.draft.sidecar))
    if (draftSidecar.frames !== 14 || draftSidecar.w !== 72 || draftSidecar.h !== 40) throw new Error('draft darts dimensions changed')
    console.log(`Side-on beard occlusion register valid: ${inventory.length} exact sheets; draft ${DARTS_NAME} frames 3,4,5,6; canonical assets untouched`)
  }
}

main(process.argv.includes('--check'))

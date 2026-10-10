#!/usr/bin/env node
/** Permanent verifier for the first side-on beard/hand occlusion audit. */
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const REGISTER_PATH = path.join(ROOT, 'data/keeper_side_on_beard_occlusion_audit.json')
const MANIFEST = JSON.parse(fs.readFileSync(path.join(ROOT, 'public/sprites/manifest.json'), 'utf8')) as Record<string, any>
const register = JSON.parse(fs.readFileSync(REGISTER_PATH, 'utf8')) as Record<string, any>
const fail = (message: string): never => { throw new Error(`side-on beard occlusion: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const absolute = (relative: string) => path.join(ROOT, relative)
const isPose = (value: unknown, words: string[]) => words.some((word) => String(value ?? '').toLowerCase().includes(word))
const isAuditedClip = (clip: Record<string, any>) => {
  if (clip.assetRole && clip.assetRole !== 'clip') return false
  const text = [clip.facing, clip.startPose, clip.endPose, clip.mirrorsFor].join(' ').toLowerCase()
  return isPose(text, ['standing', 'sitting', 'seated']) && isPose(text, ['right', 'left', 'side', 'rear'])
}

function png(file: string) {
  return PNG.sync.read(fs.readFileSync(file))
}

function hasTransparentFrameGutters(file: string, frames: number) {
  const image = png(file)
  if (!Number.isInteger(image.width / frames)) return false
  const frameWidth = image.width / frames
  for (let frame = 0; frame < frames; frame += 1) {
    for (let y = 0; y < image.height; y += 1) {
      if (image.data[((y * image.width) + frame * frameWidth) * 4 + 3] > 0) return false
      if (image.data[((y * image.width) + (frame + 1) * frameWidth - 1) * 4 + 3] > 0) return false
    }
  }
  return true
}

function verifyForegroundHandDraft(draftFile: string, sidecar: Record<string, any>, correctedFrames: Array<{ frame: number; logicalBox: [number, number, number, number] }>) {
  const image = png(draftFile)
  const frameWidth = image.width / sidecar.frames
  for (const correction of correctedFrames) {
    const [x0, y0, x1, y1] = correction.logicalBox
    let skin = 0
    let beard = 0
    for (let y = y0 * 4; y < y1 * 4; y += 1) for (let x = x0 * 4; x < x1 * 4; x += 1) {
      const index = ((y * image.width) + (correction.frame - 1) * frameWidth + x) * 4
      const r = image.data[index]; const g = image.data[index + 1]; const b = image.data[index + 2]; const a = image.data[index + 3]
      if (a > 0 && r > 150 && g > 60 && g < 205 && b < 150 && r > g * 1.1 && g > b * 0.9) skin += 1
      if (a > 0 && r > 170 && g > 155 && b > 120 && r - b < 150) beard += 1
    }
    if (!skin || beard > skin * 4) fail(`foreground hand is not visibly over beard in draft frame ${correction.frame}`)
  }
}

const inventory = Object.entries(MANIFEST)
  .filter(([, clip]) => isAuditedClip(clip as Record<string, any>))
  .sort(([left], [right]) => left.localeCompare(right))
  .map(([name]) => name)
if (register.auditedSheetNames?.join('\n') !== inventory.join('\n')) fail('exact-name inventory drifted')
if (register.auditedSheetCount !== inventory.length) fail('audited sheet count drifted')
if (register.verifierContract?.exactNameResponsesOnly !== true) fail('exact-name response contract missing')
if (register.verifierContract?.failIfForegroundHandCoveredByBeard !== true) fail('foreground-hand failure contract missing')
if (register.verifierContract?.failIfCorrectedSideOnSheetLosesTransparentFrameGutters !== true && register.verifierContract?.failIfCorrectedSheetLosesTransparentFrameGutters !== true) fail('corrected-sheet gutter contract missing')
if (register.canonicalBeardFrameAuditComplete !== false || register.verifierContract?.canonicalBeardFrameAuditComplete !== false) fail('partial v1 register incorrectly claims the canonical beard-frame audit is complete')

for (const record of register.inventory as Array<Record<string, any>>) {
  const clip = MANIFEST[record.name]
  if (!clip || clip.frames !== record.frames || clip.w !== record.canvas[0] || clip.h !== record.canvas[1]) fail(`${record.name} no longer matches manifest dimensions`) 
  const strip = absolute(record.sourceStrip)
  const sidecarPath = absolute(record.sourceSidecar)
  if (!fs.existsSync(strip) || !fs.existsSync(sidecarPath)) fail(`${record.name} exact source strip or sidecar missing`)
  const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8')) as Record<string, any>
  if (sidecar.frames !== record.frames || sidecar.w !== record.canvas[0] || sidecar.h !== record.canvas[1]) fail(`${record.name} sidecar dimensions drifted`)
  if (!hasTransparentFrameGutters(strip, record.frames)) fail(`${record.name} source strip has shared-edge alpha`)
}

if (register.beardReference?.sourceSha256 !== sha256(absolute(register.beardReference.source))) fail('canonical beard source reference hash changed')
if (register.beardReference?.stripSha256 !== sha256(absolute(register.beardReference.strip))) fail('canonical beard strip reference hash changed')

const draftRegisterPath = absolute(register.draft.register)
if (!fs.existsSync(draftRegisterPath)) fail('draft register missing')
const draftRegister = JSON.parse(fs.readFileSync(draftRegisterPath, 'utf8')) as Record<string, any>
if (draftRegister.animation !== 'keeper_darts') fail('draft register attached to the wrong exact animation')
if (draftRegister.original.stripSha256 !== sha256(absolute(draftRegister.original.strip))) fail('canonical darts rollback hash changed')
if (draftRegister.original.sidecarSha256 !== sha256(absolute(draftRegister.original.sidecar))) fail('canonical darts sidecar rollback hash changed')
if (draftRegister.draft.stripSha256 !== sha256(absolute(draftRegister.draft.strip))) fail('draft strip hash register is stale')
if (draftRegister.draft.sidecarSha256 !== sha256(absolute(draftRegister.draft.sidecar))) fail('draft sidecar hash register is stale')
if (draftRegister.draft.stripSha256 === draftRegister.original.stripSha256) fail('draft does not contain an occlusion delta')
const draftSidecar = JSON.parse(fs.readFileSync(absolute(draftRegister.draft.sidecar), 'utf8')) as Record<string, any>
if (!hasTransparentFrameGutters(absolute(draftRegister.draft.strip), draftSidecar.frames)) fail('corrected draft lost transparent frame gutters')
verifyForegroundHandDraft(absolute(draftRegister.draft.strip), draftSidecar, draftRegister.draft.correctedFrames)
for (const evidence of draftRegister.draft.evidence as string[]) if (!fs.existsSync(absolute(evidence))) fail(`draft evidence missing: ${evidence}`)

console.log(`Verified partial side-on occlusion register: ${inventory.length} exact sheets; ${register.sheetsChanged.length} draft sheet; canonical beard-frame rerun still required; production untouched`)

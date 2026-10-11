#!/usr/bin/env node
/** Permanent verifier for the complete, reversible v2 side-on audit. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const register = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/keeper_side_on_beard_occlusion_audit.json'), 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'public/sprites/manifest.json'), 'utf8')) as Record<string, any>
const fail = (message: string): never => { throw new Error(`side-on beard occlusion: ${message}`) }
const absolute = (file: string) => path.join(ROOT, file)
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const isSkin = (r: number, g: number, b: number, a: number) => a > 0 && r > 150 && g > 60 && g < 205 && b < 150 && r > g * 1.1 && g > b * 0.9
const isBeard = (r: number, g: number, b: number, a: number) => a > 0 && r > 170 && g > 155 && b > 120 && r - b < 150

function gutters(file: string, frames: number) {
  const image = PNG.sync.read(fs.readFileSync(file)); const width = image.width / frames
  if (!Number.isInteger(width)) return false
  for (let frame = 0; frame < frames; frame += 1) for (let y = 0; y < image.height; y += 1) {
    if (image.data[(y * image.width + frame * width) * 4 + 3] > 0) return false
    if (image.data[(y * image.width + (frame + 1) * width - 1) * 4 + 3] > 0) return false
  }
  return true
}

if (register.auditId !== '2026-10-10-v2' || register.auditStatus !== 'complete-awaiting-promotion-decision') fail('v2 audit register is missing or stale')
if (register.beardReference?.stripSha256 !== sha256(absolute(register.beardReference.strip))) fail('canonical beard strip hash changed')
if (register.beardReference?.sourceSha256 !== sha256(absolute(register.beardReference.source))) fail('canonical beard source hash changed')
if (!register.historicalV1?.rejected || !fs.existsSync(absolute(register.historicalV1.register))) fail('rejected v1 archive is not preserved')
if (register.auditedSheetCount !== register.inventory.length || register.auditedSheetNames.join('\n') !== register.inventory.map((item: any) => item.name).join('\n')) fail('side-action exact-name inventory drifted')

for (const [name, clip] of Object.entries(manifest)) {
  const entry = register.manifestFrameAudit?.[name]
  if (!entry) fail(`${name} is missing an exact-name frame audit`)
  if (!Array.isArray(entry.frames) || entry.frames.length !== (clip as any).frames) fail(`${name} frame classification is incomplete`)
  for (const frame of entry.frames) if (!['side-on', 'front-facing', 'rear-facing', 'indeterminate'].includes(frame.classification)) fail(`${name} has an invalid frame classification`)
}
if (Object.keys(register.manifestFrameAudit).length !== Object.keys(manifest).length) fail('manifest frame audit contains stale names')

for (const item of register.inventory as Array<Record<string, any>>) {
  const raw = absolute(item.sourceStrip); const sidecar = absolute(item.sourceSidecar)
  if (!fs.existsSync(raw) || !fs.existsSync(sidecar)) fail(`${item.name} source strip or sidecar is missing`)
  if (sha256(raw) !== item.sourceStripSha256 || sha256(sidecar) !== item.sourceSidecarSha256) fail(`${item.name} canonical source changed after audit`)
  if (!gutters(raw, item.frames)) fail(`${item.name} canonical strip lost a transparent frame gutter`)
  if (item.frameAudit.length !== item.frames) fail(`${item.name} side-action frames are incomplete`)
  for (const frame of item.frameAudit) if (frame.classification === 'side-on' && item.posture !== 'other' && !frame.beard) fail(`${item.name} frame ${frame.frame} lacks a side-on beard decision`)
}

const draftRegister = JSON.parse(fs.readFileSync(absolute(register.draft.register), 'utf8')) as Record<string, any>
if (draftRegister.animation !== 'keeper_darts' || draftRegister.label !== 'Draft v2') fail('Draft v2 is detached from keeper_darts')
for (const section of ['canonical', 'draft']) for (const key of section === 'canonical' ? ['source', 'strip', 'sidecar', 'runtime'] : ['source', 'strip', 'sidecar']) {
  const file = absolute(draftRegister[section][key]); if (!fs.existsSync(file) || sha256(file) !== draftRegister[section][`${key}Sha256`]) fail(`draft ${section} ${key} hash is stale`)
}
if (draftRegister.canonical.stripSha256 === draftRegister.draft.stripSha256) fail('Draft v2 has no pixel delta')
if (!gutters(absolute(draftRegister.draft.strip), 14)) fail('Draft v2 lost its transparent frame gutters')
const corrected = draftRegister.draft.correctedFrames.map((item: any) => item.frame)
if (corrected.join(',') !== '3,4,5,6') fail('Draft v2 corrected-frame register drifted')
const canonicalDarts = PNG.sync.read(fs.readFileSync(absolute(draftRegister.canonical.strip)))
const draftDarts = PNG.sync.read(fs.readFileSync(absolute(draftRegister.draft.strip)))
const dartsFrameWidth = canonicalDarts.width / 14
for (const correction of draftRegister.draft.correctedFrames as Array<Record<string, any>>) {
  let deltaPixels = 0
  const [left, top, right, bottom] = correction.logicalBox as number[]
  for (let y = 0; y < canonicalDarts.height; y += 1) for (let x = 0; x < dartsFrameWidth; x += 1) {
    const at = (y * canonicalDarts.width + ((correction.frame - 1) * dartsFrameWidth + x)) * 4
    const changed = [0, 1, 2, 3].some((channel) => canonicalDarts.data[at + channel] !== draftDarts.data[at + channel])
    if (!changed) continue
    deltaPixels += 1
    if (x < left * 4 || x >= right * 4 || y < top * 4 || y >= bottom * 4) fail(`Draft v2 frame ${correction.frame} changes pixels outside its declared hand/beard box`)
    if (!isBeard(canonicalDarts.data[at], canonicalDarts.data[at + 1], canonicalDarts.data[at + 2], canonicalDarts.data[at + 3])) fail(`Draft v2 frame ${correction.frame} changes a non-beard canonical pixel`)
    if (!isSkin(draftDarts.data[at], draftDarts.data[at + 1], draftDarts.data[at + 2], draftDarts.data[at + 3])) fail(`Draft v2 frame ${correction.frame} does not restore a foreground skin pixel over the beard`)
  }
  if (deltaPixels !== correction.pixels) fail(`Draft v2 frame ${correction.frame} changed-pixel count is stale`)
}
const selected = draftRegister.relatedFrankSelectedDraft
if (!selected || !fs.existsSync(absolute(selected.register)) || sha256(absolute(selected.source)) !== selected.sourceSha256) fail('Frank-selected darts draft was not preserved byte-for-byte')
for (const evidence of draftRegister.draft.evidence) if (!fs.existsSync(absolute(evidence))) fail(`Draft v2 evidence missing: ${evidence}`)
console.log(`Verified v2 side-on beard audit: ${register.auditedSheetCount} exact side-action sheets; all manifest frames classified; keeper_darts frames 3–6 isolated as Draft v2; canonical assets unchanged`)

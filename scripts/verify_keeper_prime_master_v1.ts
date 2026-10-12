#!/usr/bin/env node
/** Deterministically verify the reversible Keeper Prime Master V1 pack. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-master-2026-10-12-v1')
const REGISTER = path.join(PACK, 'master-pack-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-master-v1/index.html')
const fail = (message: string): never => { throw new Error(`Keeper Prime Master V1: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, PUBLIC, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.packId !== 'keeper-prime-master-2026-10-12-v1' || register.status !== 'draft-awaiting-visual-approval') fail('pack identity/status changed')
if (register.candidate?.promotionAllowed !== false || register.validation?.finalAnimations !== 0) fail('approval boundary changed')
if (register.identityRules?.uniform !== 'one broad pale chest-and-sleeve band; do not restore the legacy double stripe') fail('single-band uniform decision changed')

const verifyRecord = (record: Record<string, any>, label: string) => {
  const file = path.join(ROOT, record.file)
  if (!fs.existsSync(file)) fail(`${label} is missing`)
  if (sha256(file) !== record.sha256) fail(`${label} hash changed`)
  return file
}
verifyRecord(register.references.frame6, 'Frame 6 authority')
verifyRecord(register.references.v11, 'V11 reference')
verifyRecord(register.generatedSource, 'selected generated source')
const candidateFile = verifyRecord(register.candidate, 'candidate')
const sidecarFile = path.join(ROOT, register.candidate.sidecar)
if (sha256(sidecarFile) !== register.candidate.sidecarSha256) fail('candidate sidecar hash changed')
const sidecar = JSON.parse(fs.readFileSync(sidecarFile, 'utf8'))
const png = PNG.sync.read(fs.readFileSync(candidateFile))
if (png.width !== sidecar.w * sidecar.density || png.height !== sidecar.h * sidecar.density || sidecar.frames !== 1) fail('candidate geometry disagrees with sidecar')
if (png.width !== 256 || png.height !== 320 || sidecar.density !== 8 || JSON.stringify(sidecar.anchor) !== '[16,40]') fail('master cell/density/anchor changed')

let opaque = 0
let edge = 0
let x0 = png.width; let y0 = png.height; let x1 = 0; let y1 = 0
for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
  const alpha = png.data[((y * png.width) + x) * 4 + 3]
  if (alpha > 0) {
    opaque += 1
    x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x + 1); y1 = Math.max(y1, y + 1)
    if (x === 0 || y === 0 || x === png.width - 1 || y === png.height - 1) edge += 1
  }
}
if (!opaque) fail('candidate is empty')
if (edge !== 0 || register.validation.opaqueCellEdgePixels !== 0 || !register.validation.transparentSafetyGutter) fail('candidate touches a cell edge')
if (JSON.stringify([x0, y0, x1, y1]) !== JSON.stringify(register.geometry.normalizedOpaqueBoundsExclusive)) fail('recorded opaque bounds changed')

for (const [name, record] of Object.entries(register.masksAndGuides as Record<string, any>)) {
  const file = verifyRecord(record, `${name} guide`)
  const mask = PNG.sync.read(fs.readFileSync(file))
  if (mask.width !== 256 || mask.height !== 320) fail(`${name} guide geometry changed`)
  if (JSON.stringify(record.boundsExclusive) !== JSON.stringify(register.geometry.landmarksSourcePixels[`${name.replace('eye-left', 'leftEye').replace('eye-right', 'rightEye').replace('beard-envelope', 'beardEnvelope').replace('head-envelope', 'headEnvelope').replace('chest-band', 'chestBand')}BoundsExclusive`])) {
    fail(`${name} guide bounds disagree with landmarks`)
  }
}
verifyRecord(register.evidence.comparison, 'comparison evidence')
verifyRecord(register.evidence.landmarkOverlay, 'landmark overlay')
if ((register.rejectedGeneratedProvenance as any[]).length !== 3) fail('rejected generated provenance is incomplete')
for (const [index, record] of (register.rejectedGeneratedProvenance as any[]).entries()) verifyRecord(record, `rejected source ${index + 1}`)

const html = fs.readFileSync(PUBLIC, 'utf8')
for (const phrase of ['Draft · awaiting visual approval', 'Final contains 0 animations', 'one broad pale chest band', 'Masks and guides', register.candidate.sha256]) {
  if (!html.includes(phrase)) fail(`public review omits ${phrase}`)
}
console.log(`Keeper Prime Master V1 verified: ${opaque} non-transparent pixels, 0 edge pixels, Final count 0.`)

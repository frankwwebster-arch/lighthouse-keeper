#!/usr/bin/env node
/** Verify the V2 approved-model full-motion turn redraws. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const BATCH = path.join(ROOT, 'art/drafts/keeper-full-face-standard-turn-redraw-2026-10-12-v2')
const REGISTER = path.join(BATCH, 'batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/full-face-standard-turn-redraw-v2')
const CANON = path.join(ROOT, 'art/drafts/keeper-full-face-canon-pack-2026-10-12-v1/drafts/keeper_full-face-canon_standard-neutral_f1.png')
const EXPECTED_NAMES = ['keeper_turn_front', 'keeper_turn_left_front']
const fail = (message: string): never => { throw new Error(`keeper full-face turn redraw v2: ${message}`) }
const json = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8')) as Record<string, any>
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const absolute = (relative: string) => path.join(ROOT, relative)

for (const file of [REGISTER, CANON, path.join(PUBLIC, 'index.html')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const register = json(REGISTER)
if (register.batchId !== 'keeper-full-face-standard-turn-redraw-2026-10-12-v2') fail('unexpected batch id')
if (register.status !== 'awaiting-explicit-user-approval') fail('batch is not approval-gated')
if (register.checks?.productionChanged !== false || register.checks?.exactCanonicalFinalFrames !== true || register.checks?.smoothF5ToF6Geometry !== true) fail('batch scope gates changed')
if (register.canonSha256 !== sha256(CANON)) fail('approved canon hash changed')
if (JSON.stringify(register.scope) !== JSON.stringify(EXPECTED_NAMES)) fail('batch scope changed')
if (!String(register.supersedes?.decision).includes('V1 F5-only transplant rejected')) fail('V1 rejection/supersession is not recorded')
if (register.documentationAudit?.result !== 'pass' || register.documentationAudit?.filesReconciled?.length !== 4) fail('documentation audit is missing')

const canon = PNG.sync.read(fs.readFileSync(CANON))
for (const name of EXPECTED_NAMES) {
  const record = register.candidates.find((candidate: Record<string, any>) => candidate.animation === name)
  if (!record) fail(`missing ${name} record`)
  for (const variant of ['canonical', 'draft']) for (const kind of ['strip', 'sidecar']) {
    const file = absolute(record[variant][kind])
    if (!fs.existsSync(file) || sha256(file) !== record[variant][`${kind}Sha256`]) fail(`${name} ${variant} ${kind} missing or stale`)
  }
  const source = absolute(record.generatedSource.file)
  if (!fs.existsSync(source) || sha256(source) !== record.generatedSource.sha256 || record.generatedSource.tool !== 'built-in image_gen') fail(`${name} generated source provenance changed`)
  for (const required of ['exact final front-facing pose', 'Frame 5 must already be almost canonical', 'no jump']) if (!record.generatedSource.prompt.includes(required)) fail(`${name} prompt omits ${required}`)
  const sidecar = json(absolute(record.draft.sidecar))
  if (sidecar.frames !== 6 || sidecar.w !== 32 || sidecar.h !== 40 || sidecar.density !== 4 || sidecar.fps !== 4) fail(`${name} sidecar contract changed`)
  if (sidecar.startPose !== (name === 'keeper_turn_front' ? 'standing-side-right' : 'standing-side-left') || sidecar.endPose !== 'standing-front') fail(`${name} endpoint contract changed`)
  if (sidecar.amendment?.lockedCanonicalEndpointFrame !== 6 || JSON.stringify(sidecar.amendment?.authoredFrames) !== '[1,2,3,4,5]') fail(`${name} authored-frame boundary changed`)
  const original = PNG.sync.read(fs.readFileSync(absolute(record.canonical.strip)))
  const draft = PNG.sync.read(fs.readFileSync(absolute(record.draft.strip)))
  const frameWidth = sidecar.w * sidecar.density
  const frameHeight = sidecar.h * sidecar.density
  if (draft.width !== frameWidth * 6 || draft.height !== frameHeight || original.width !== draft.width || original.height !== draft.height) fail(`${name} strip/sidecar geometry mismatch`)
  const alphaValues = new Set<number>()
  const changedFrames = new Set<number>()
  for (let y = 0; y < draft.height; y += 1) for (let x = 0; x < draft.width; x += 1) {
    const offset = ((y * draft.width) + x) * 4
    const frame = Math.floor(x / frameWidth)
    const localX = x % frameWidth
    const different = draft.data[offset] !== original.data[offset] || draft.data[offset + 1] !== original.data[offset + 1] || draft.data[offset + 2] !== original.data[offset + 2] || draft.data[offset + 3] !== original.data[offset + 3]
    if (different) changedFrames.add(frame + 1)
    alphaValues.add(draft.data[offset + 3])
    if (draft.data[offset + 3] > 0 && (localX === 0 || localX === frameWidth - 1 || y === 0 || y === frameHeight - 1)) fail(`${name} frame ${frame + 1} touches a cell edge`)
  }
  if ([...changedFrames].sort().join(',') !== '1,2,3,4,5') fail(`${name} changed frames are not exactly F1-F5`)
  if ([...alphaValues].sort((a, b) => a - b).join(',') !== '0,255') fail(`${name} alpha is not binary`)
  for (let y = 0; y < canon.height; y += 1) for (let x = 0; x < canon.width; x += 1) {
    const draftOffset = ((y * draft.width) + (5 * frameWidth) + x) * 4
    const canonOffset = ((y * canon.width) + x) * 4
    for (let channel = 0; channel < 4; channel += 1) if (draft.data[draftOffset + channel] !== canon.data[canonOffset + channel]) fail(`${name} F6 is not exact canon`)
  }
  const metrics = record.endpointContinuity
  if (Math.abs(metrics.widthDeltaPixels) > 4 || Math.abs(metrics.heightDeltaPixels) > 2 || Math.abs(metrics.centreXDeltaPixels) > 1 || metrics.baselineDeltaPixels !== 0) fail(`${name} F5→F6 geometry is too discontinuous`)
  if (record.frameEvidence.length !== 6 || record.frameEvidence.filter((frame: Record<string, any>) => frame.redrawn).map((frame: Record<string, any>) => frame.frame).join(',') !== '1,2,3,4,5') fail(`${name} frame evidence changed`)
  for (const evidence of record.evidence) if (!fs.existsSync(absolute(evidence))) fail(`${name} missing evidence ${evidence}`)
}

const page = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const value of [...EXPECTED_NAMES, 'V2 full-motion redraw', 'Frame 6 is restored from the approved canon exactly', 'production unchanged']) if (!page.includes(value)) fail(`public page omits ${value}`)
for (const match of page.matchAll(/(?:src|href)="([^"]+)"/g)) {
  if (!match[1].startsWith('assets/')) continue
  const file = path.join(PUBLIC, match[1])
  if (!fs.existsSync(file)) fail(`public page references missing ${match[1]}`)
  const hashPrefix = path.basename(file).match(/-([0-9a-f]{16})\.(?:gif|png)$/)?.[1]
  if (!hashPrefix || !sha256(file).startsWith(hashPrefix)) fail(`public asset hash filename is stale: ${match[1]}`)
}
console.log('Verified V2 turn redraws: F1-F5 full-motion redrafts, exact canon F6 endpoints, smooth endpoint geometry, binary alpha and zero cell-edge pixels')

#!/usr/bin/env node

import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const rel = (file) => path.join(root, file)
const json = (file) => JSON.parse(fs.readFileSync(rel(file), 'utf8'))
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(rel(file))).digest('hex')
const register = json('art/drafts/keeper-prime-sit-stand-front-2026-10-17-v4/batch-register.json')
const v3 = json('art/drafts/keeper-prime-sit-stand-front-2026-10-17-v3/batch-register.json')
const data = json('art/drafts/keeper-prime-sit-stand-front-2026-10-17-v4/keeper-prime-sit-stand-front-v4.json')
const rejection = json('docs/review/keeper-prime-sit-stand-front-v3-rejection-2026-10-18.json')
const page = fs.readFileSync(rel('src/app/keeper-review/keeper-prime-sit-stand-front-v4/route.ts'), 'utf8')

assert.equal(register.status, 'front-frame32-elbow-width-locked-v4-awaiting-frank')
assert.equal(rejection.decision, 'rejected-lowering-elbow-width-drift-frames-28-through-32')
assert.equal(register.supersedes.rejection.sha256, sha(register.supersedes.rejection.file))
assert.equal(register.supersedes.immutableV3.sha256, sha(register.supersedes.immutableV3.register))
assert.equal(register.supersedes.immutableV3.routeDataSha256, sha(register.supersedes.immutableV3.routeData))
assert.equal(rejection.rejectedHashes.reviewRoute, sha('src/app/keeper-review/keeper-prime-sit-stand-front-v3/route.ts'))
assert.deepEqual(rejection.rejectedHashes.keeperFrames, v3.candidate.frames.map((frame) => frame.sha256))
assert.equal(data.route.length, 59)
assert.deepEqual(register.candidate.frames.map((frame) => frame.bounds.width), [152, 143, 143, 143, 143, 143])
assert.deepEqual(register.candidate.frames.map((frame) => frame.bounds.height), [298, 286, 276, 270, 266, 264])
for (const index of [0, 5]) assert.equal(register.candidate.frames[index].sha256, v3.candidate.frames[index].sha256)
for (const index of [1, 2, 3, 4]) assert.notEqual(register.candidate.frames[index].sha256, v3.candidate.frames[index].sha256)
const frame32ElbowSpan = register.candidate.frames[5].elbowSpanPx
assert.equal(frame32ElbowSpan, 143)
assert.deepEqual(register.candidate.frames.slice(1).map((frame) => frame.elbowSpanPx), [143, 143, 143, 143, 143])
for (let routeIndex = 27; routeIndex <= 31; routeIndex += 1) {
  const actionIndex = routeIndex - 25
  assert.equal(data.route[routeIndex].actionFrame, actionIndex)
  assert.equal(data.route[routeIndex].src, data.action.frames[actionIndex - 1].src)
}
for (const frame of register.candidate.frames) {
  assert.equal(frame.sha256, sha(frame.file)); assert.equal(frame.sourceSha256, sha(frame.source))
  const png = PNG.sync.read(fs.readFileSync(rel(frame.file))); assert.deepEqual([png.width, png.height], [256, 320]); assert.equal(frame.edgeAlphaPixels, 0); assert.ok(frame.transparentGutterPx >= 4); assert.equal(frame.bounds.maxY, 315)
}
for (const [direction, strip] of [['forward', register.candidate.forwardStrip], ['reverse', register.candidate.reverseStrip]]) {
  assert.equal(strip.sha256, sha(strip.file)); const png = PNG.sync.read(fs.readFileSync(rel(strip.file))); assert.deepEqual([png.width, png.height], [1536, 320])
  const frames = direction === 'forward' ? register.candidate.frames : [...register.candidate.frames].reverse()
  for (let i = 0; i < 6; i += 1) { const expected = PNG.sync.read(fs.readFileSync(rel(frames[i].file))); for (let y = 0; y < 320; y += 1) assert.ok(png.data.subarray(((y * 1536) + i * 256) * 4, ((y * 1536) + i * 256) * 4 + 1024).equals(expected.data.subarray(y * 1024, y * 1024 + 1024))) }
}
for (const frame of data.route) assert.ok(register.publishedAssets.some((asset) => asset.url === frame.src))
for (const [name, value] of Object.entries(register.checks)) assert.equal(value, true, `${name} failed`)
for (const flag of ['frontV4Approved', 'backSitStandApproved', 'rearAngleSitStandApproved', 'promotionAllowed', 'finalChanged', 'runtimeChanged', 'productionChanged']) assert.equal(register.approvalBoundary[flag], false)
for (const token of ['getV3', 'keeper-prime-sit-stand-front-v4', 'Frame-32 elbow-width-locked Prime redraw', 'Front V1–V3 are rejected for width drift']) assert.ok(page.includes(token), `page missing ${token}`)

console.log('Keeper Prime front sit/stand V4 verified: V3 immutable, frames 28–32 locked to exact frame-32 143px elbow span with monotonic articulated lowering, exact endpoints and 59-frame context preserved; nothing promoted.')

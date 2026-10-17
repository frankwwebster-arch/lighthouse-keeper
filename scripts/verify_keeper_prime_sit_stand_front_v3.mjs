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
const register = json('art/drafts/keeper-prime-sit-stand-front-2026-10-17-v3/batch-register.json')
const v2 = json('art/drafts/keeper-prime-sit-stand-front-2026-10-17-v2/batch-register.json')
const data = json('art/drafts/keeper-prime-sit-stand-front-2026-10-17-v3/keeper-prime-sit-stand-front-v3.json')
const rejection = json('docs/review/keeper-prime-sit-stand-front-v2-rejection-2026-10-17.json')
const page = fs.readFileSync(rel('src/app/keeper-review/keeper-prime-sit-stand-front-v3/route.ts'), 'utf8')

assert.equal(register.status, 'front-complete-context-width-smoothed-v3-awaiting-frank')
assert.equal(rejection.decision, 'rejected-complete-context-width-snap-frames-29-and-30')
assert.equal(register.supersedes.rejection.sha256, sha(register.supersedes.rejection.file))
assert.equal(register.supersedes.immutableV2.sha256, sha(register.supersedes.immutableV2.register))
assert.equal(register.supersedes.immutableV2.routeDataSha256, sha(register.supersedes.immutableV2.routeData))
assert.equal(rejection.rejectedHashes.reviewRoute, sha('src/app/keeper-review/keeper-prime-sit-stand-front-v2/route.ts'))
assert.deepEqual(rejection.rejectedHashes.keeperFrames, v2.candidate.frames.map((frame) => frame.sha256))
assert.equal(data.route.length, 59)
assert.deepEqual(register.candidate.frames.map((frame) => frame.bounds.width), [152, 157, 158, 158, 150, 143])
for (const index of [0, 1, 3, 4, 5]) assert.equal(register.candidate.frames[index].sha256, v2.candidate.frames[index].sha256)
assert.notEqual(register.candidate.frames[2].sha256, v2.candidate.frames[2].sha256)
assert.ok(register.candidate.frames[2].bounds.width < v2.candidate.frames[2].bounds.width)
assert.equal(register.candidate.frames[2].bounds.width, register.candidate.frames[3].bounds.width)
assert.equal(data.route[28].actionFrame, 3)
assert.equal(data.route[29].actionFrame, 4)
assert.equal(data.route[28].src, data.action.frames[2].src)
assert.equal(data.route[29].src, data.action.frames[3].src)
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
for (const flag of ['frontV3Approved', 'backSitStandApproved', 'rearAngleSitStandApproved', 'promotionAllowed', 'finalChanged', 'runtimeChanged', 'productionChanged']) assert.equal(register.approvalBoundary[flag], false)
for (const token of ['getV2', 'keeper-prime-sit-stand-front-v3', 'Complete-context width-smoothed Prime redraw', 'Front V1 and V2 are rejected for width drift']) assert.ok(page.includes(token), `page missing ${token}`)

console.log('Keeper Prime front sit/stand V3 verified: V2 immutable, complete-context frame 29 F3 width spike redrawn to match frame 30 F4, exact endpoints and 59-frame context preserved; nothing promoted.')

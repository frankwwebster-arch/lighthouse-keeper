import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const source = path.join(root, 'art/source/kitchen-continuous-run-approved-2026-10-17-v23/approved-image-1.png')
const raw = path.join(root, 'art/raw/kitchen-continuous-run-approved-2026-10-17-v23/full-kitchen-approved.png')
const draft = path.join(root, 'art/drafts/kitchen-continuous-run-approved-2026-10-17-v23')
const pageFile = path.join(root, 'public/keeper-review/kitchen-continuous-run-approved-v23/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-continuous-run-approved-v23.json')
const approvedSha = '5d5451acbaa81a48918268d25482a1d3f657a77c441c9d5b4f87ed547d4f9707'
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

assert.equal(sha(source), approvedSha, 'approved Image 1 source changed')
assert.equal(sha(raw), approvedSha, 'raw master must be byte-identical to approved Image 1')
assert.deepEqual(fs.readFileSync(raw), fs.readFileSync(source), 'no transformation is permitted after approval')

const image = PNG.sync.read(fs.readFileSync(raw))
assert.deepEqual([image.width, image.height], [2170, 725])
const pointX = Math.round(image.width * 0.373)
const pointY = Math.round(image.height * 0.569)
const offset = (pointY * image.width + pointX) * 4
assert.deepEqual(Array.from(image.data.subarray(offset, offset + 4)), [222, 19, 12, 255], 'approval point pixel changed')

const data = JSON.parse(fs.readFileSync(path.join(draft, 'approval-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
assert.equal(data.version, 23)
assert.equal(data.status, 'approved-visual-authority-unpromoted')
assert.deepEqual(data.approval, {
  date: '2026-10-17',
  comment: 'this is correct',
  image: 'Image 1',
  point: { xPercent: 37.3, yPercent: 56.9, comment: 'this is correct' },
})
assert.deepEqual(data.master.transformationsAfterApproval, [])
assert.deepEqual(data.boundaries, {
  approved: true,
  promoted: false,
  runtimeChanged: false,
  finalChanged: false,
  keeperChanged: false,
})
assert.equal(register.v22Preserved, true)

const v22Raw = path.join(root, 'art/raw/kitchen-rear-wall-flow-2026-10-17-v22/full-kitchen.png')
assert.equal(sha(v22Raw), '8dbba02b4f664db40085975510372ab30abd545df869a2ef46609ffc188c69e4', 'V22 must remain immutable rejection provenance')

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /Frank: “this is correct.”/)
assert.match(page, /Exact Image 1/)
assert.match(page, /left:37\.3%;top:56\.9%/)
assert.match(page, /No image-generation retry or post-processing/)
assert.ok(page.includes('/keeper-review/kitchen-continuous-run-approved-v23/assets/full-kitchen-approved.png'))
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-continuous-run-approved-v23'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 1)
  const record = Object.values(archive.entries)[0]
  assert.equal(record.sha256, approvedSha)
  assert.equal(sha(path.join(root, record.object)), approvedSha)
}

console.log('Kitchen V23 exact Image 1 visual authority verified')

#!/usr/bin/env node
/** Verify V18's reversible stair-ascent beard-continuity correction. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-stair-ascent-v18'
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-22-v18')
const registerPath = path.join(pack, 'batch-register.json')
const rigPath = path.join(pack, 'stair-contact-rig-v18.json')
const specPath = path.join(pack, 'keeper-prime-stair-ascent-v18.json')
const pagePath = path.join(root, 'public/keeper-review', set, 'index.html')
const v16RigPath = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16/stair-contact-rig-v16.json')
const manifestPath = path.join(root, 'review-archive/sets', `${set}.json`)
const archivePath = path.join(root, 'review-archive/index.json')
const fail = (message) => { throw new Error(`Prime Keeper stair ascent V18: ${message}`) }
const hash = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))

for (const file of [registerPath, rigPath, specPath, pagePath, v16RigPath, manifestPath, archivePath, path.join(pack, 'HANDOFF.md'), path.join(pack, 'PROMPT_LOG.md')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(root, file)}`)
}

const register = readJson(registerPath)
const rig = readJson(rigPath)
const spec = readJson(specPath)
const v16Rig = readJson(v16RigPath)
const manifest = readJson(manifestPath)
const archive = readJson(archivePath)
const html = fs.readFileSync(pagePath, 'utf8')
if (register.batchId !== 'keeper-prime-stair-ascent-2026-10-22-v18' || register.status !== 'beard-continuity-correction-awaiting-review' || spec.promoted !== false) fail('identity, status or promotion boundary changed')
for (const entry of [register.authority, register.rig, register.spec, register.reviewPage]) {
  const file = path.join(root, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`registered file changed: ${entry.file}`)
}
if (rig.timeline.length !== 27 || register.validation.timelineFrames !== 27 || rig.uniqueDrawings !== 4) fail('timeline or unique-drawing count changed')
if (JSON.stringify(rig.geometry) !== JSON.stringify(v16Rig.geometry) || JSON.stringify(rig.endpoint) !== JSON.stringify(v16Rig.endpoint)) fail('V16 geometry or endpoint changed')
for (let index = 0; index < rig.timeline.length; index += 1) {
  const original = v16Rig.timeline[index]
  const draft = rig.timeline[index]
  for (const key of Object.keys(original).filter((key) => key !== 'src')) if (JSON.stringify(original[key]) !== JSON.stringify(draft[key])) fail(`frame ${index + 1} changed ${key}`)
}

function edgeAlpha(image) {
  let count = 0
  for (let x = 0; x < image.width; x += 1) for (const y of [0, image.height - 1]) if (image.data[(y * image.width + x) * 4 + 3]) count += 1
  for (let y = 1; y < image.height - 1; y += 1) for (const x of [0, image.width - 1]) if (image.data[(y * image.width + x) * 4 + 3]) count += 1
  return count
}

for (const asset of register.assets) {
  const originalPath = path.join(root, asset.original)
  const draftPath = path.join(root, asset.draft)
  if (hash(originalPath) !== asset.originalSha256 || hash(draftPath) !== asset.draftSha256) fail(`${asset.role} hash changed`)
  const original = PNG.sync.read(fs.readFileSync(originalPath))
  const draft = PNG.sync.read(fs.readFileSync(draftPath))
  if (draft.width !== 256 || draft.height !== 320 || edgeAlpha(draft)) fail(`${asset.role} violates cell geometry or transparent gutter`)
  if (asset.changed) {
    const correction = register.corrections[asset.role]
    const mask = PNG.sync.read(fs.readFileSync(path.join(root, correction.mask.file)))
    if (hash(path.join(root, correction.mask.file)) !== correction.mask.sha256) fail(`${asset.role} mask hash changed`)
    let changed = 0
    for (let pixel = 0; pixel < draft.width * draft.height; pixel += 1) {
      const offset = pixel * 4
      const differs = [0, 1, 2, 3].some((channel) => original.data[offset + channel] !== draft.data[offset + channel])
      if (!differs) continue
      changed += 1
      const y = Math.floor(pixel / draft.width)
      if (!mask.data[offset + 3] || y < 112 || y > 164) fail(`${asset.role} changed outside its beard mask/band`)
    }
    if (changed !== correction.changedPixels || changed < 1000) fail(`${asset.role} changed-pixel count drifted`)
    if (correction.correctedBeard.pixels !== register.beardAuthority.pixels || JSON.stringify(correction.correctedBeard.boundsInclusive) !== JSON.stringify(register.beardAuthority.boundsInclusive)) fail(`${asset.role} beard signature differs from authority`)
  } else if (!fs.readFileSync(originalPath).equals(fs.readFileSync(draftPath))) fail(`${asset.role} passing authority is not byte-identical`)
}

if (register.validation.correctedContactDrawings !== 2 || register.validation.unchangedPassingDrawings !== 2 || !register.validation.transparentCellEdges || !register.validation.immutableV16 || register.validation.runtimeChanged || register.validation.productionChanged) fail('validation boundary changed')
for (const phrase of ['Play both', 'Previous frame', 'Next frame', 'Approved V16 · beard flicker', 'V18 candidate · locked beard', 'Promise.all(unique.map(preload))', 'All unique images decoded', 'nothing promoted']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (manifest.set !== set || Object.keys(manifest.entries).length !== register.frameUrls.length) fail('archive set identity or entry count changed')
for (const url of register.frameUrls) if (!manifest.entries[url] || !archive.legacyPaths[url]) fail(`archive cannot resolve ${url}`)
try { fs.lstatSync(path.join(path.dirname(pagePath), 'assets')); fail('public page still contains physical review binaries') } catch (error) { if (String(error.message).startsWith('Prime Keeper stair ascent V18:')) throw error; if (error.code !== 'ENOENT') throw error }
console.log('Prime Keeper stair ascent V18 verified: two masked contact-beard corrections; four exact shared beard signatures; immutable V16, 27-frame timing/geometry, transparent gutters and production boundary preserved.')

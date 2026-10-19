#!/usr/bin/env node
/** Verify the reversible layered Prime hold_shaft_two_hand V1 review draft. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const pack = 'art/drafts/keeper-prime-hold-shaft-two-hand-layered-2026-10-19-v1'
const dataFile = `${pack}/keeper-prime-hold-shaft-two-hand-layered-v1.json`
const pocFile = 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v3/keeper-prime-upper-body-override-poc-v3.json'
const approvalFile = 'docs/review/keeper-prime-upper-body-override-poc-v3-approval-2026-10-19.json'
const read = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'))
const bytes = file => fs.readFileSync(path.join(root, file))
const text = file => fs.readFileSync(path.join(root, file), 'utf8')
const sha = file => crypto.createHash('sha256').update(bytes(file)).digest('hex')
const png = file => PNG.sync.read(bytes(file))
const data = read(dataFile)
const register = read(`${pack}/batch-register.json`)
const poc = read(pocFile)
const approval = read(approvalFile)
const reviewer = text(`${pack}/reviewer.html`)
const shell = text('public/keeper-review/keeper-prime-hold-shaft-two-hand-layered-v1/index.html')
const archiveManifest = read('review-archive/sets/keeper-prime-hold-shaft-two-hand-layered-v1.json')

assert.equal(data.schema, 'lighthouse-keeper/separable-held-body@1')
assert.equal(data.set, 'keeper-prime-hold-shaft-two-hand-layered-v1')
assert.equal(register.set, data.set)
assert.equal(data.status, 'versioned-reversible-layered-prime-draft-awaiting-frank')
assert.equal(data.gripProfile, 'hold_shaft_two_hand')
assert.equal(approval.approvedContract.gripProfile, data.gripProfile)
assert.equal(data.contract.approvedMotionFoundation, poc.set)
assert.equal(data.contract.approvedMotionDecisionSha256, sha(approvalFile))
assert.deepEqual(data.route, poc.route, 'approved POC V3 route must remain byte-for-byte equivalent as JSON')
assert.equal(data.route.length, 33)
assert.deepEqual(data.contract.layerOrder, ['lowerBodyAuthority', 'lowerBodyOcclusionFill', 'torsoHead', 'heldArms'])
assert.equal(data.contract.exactWalkV6LowerBody, true)
assert.equal(data.contract.exactTurnV9LowerBody, true)
assert.equal(data.contract.maximumVisibleHands, 2)
assert.equal(data.contract.propPixels, 0)
assert.equal(data.contract.propLayerPresent, false)
assert.equal(data.contract.oneShotPlayback, true)
assert.equal(data.contract.runtimeChanged, false)
assert.equal(data.contract.finalChanged, false)

for (const boundary of ['layeredArtworkApproved', 'implementIncluded', 'broomIncluded', 'runtimeChanged',
  'finalChanged', 'productionArtworkChanged', 'promotionPerformed']) {
  assert.equal(register.approvalBoundary[boundary], false, `approval boundary ${boundary}`)
}
assert.equal(register.approvalBoundary.motionFoundationApproved, true)
assert.equal(sha(register.authorities.approvedPocV3.file), register.authorities.approvedPocV3.sha256)
assert.equal(sha(register.authorities.approvedPocV3Decision.file), register.authorities.approvedPocV3Decision.sha256)
for (const source of Object.values(register.sources)) assert.equal(sha(source.file), source.sha256)
for (const authority of [...register.authorities.walkV6, ...register.authorities.turnV9]) {
  assert.equal(sha(authority.file), authority.sha256)
  assert.equal(sha(authority.registeredFile), authority.registeredSha256)
}

const gait = ['left-foot contact', 'left-foot down', 'left-foot passing', 'left-foot up',
  'right-foot contact', 'right-foot down', 'right-foot passing', 'right-foot up']
const frames = Object.values(data.frames)
const walks = frames.filter(frame => frame.kind.startsWith('walk-'))
const turns = frames.filter(frame => frame.kind.startsWith('turn-'))
assert.deepEqual(walks.map(frame => frame.gaitFrame), [1, 2, 3, 4, 5, 6, 7, 8])
assert.deepEqual(walks.map(frame => frame.gaitPhase), gait)
assert.deepEqual(turns.map(frame => frame.turnFrame), [1, 2, 3, 4, 5, 6, 7, 8, 9])
assert.deepEqual(turns.map(frame => frame.angleDegrees), [90, 98, 105, 120, 135, 150, 165, 172.5, 180])
assert.equal(new Set(walks.map(frame => frame.composite.sha256)).size, 8)
assert.equal(new Set(turns.map(frame => frame.composite.sha256)).size, 9)

function alphaOver(bottom, top) {
  const output = Buffer.alloc(bottom.data.length)
  for (let offset = 0; offset < output.length; offset += 4) {
    const ba = bottom.data[offset + 3] / 255
    const ta = top.data[offset + 3] / 255
    const outA = ta + ba * (1 - ta)
    output[offset + 3] = Math.round(outA * 255)
    if (!outA) continue
    for (let channel = 0; channel < 3; channel++) {
      output[offset + channel] = Math.round((top.data[offset + channel] * ta + bottom.data[offset + channel] * ba * (1 - ta)) / outA)
    }
  }
  return { width: bottom.width, height: bottom.height, data: output }
}

function edgeAlpha(image) {
  let count = 0
  for (let x = 0; x < image.width; x++) for (const y of [0, image.height - 1]) if (image.data[(y * image.width + x) * 4 + 3]) count++
  for (let y = 1; y < image.height - 1; y++) for (const x of [0, image.width - 1]) if (image.data[(y * image.width + x) * 4 + 3]) count++
  return count
}

for (const frame of frames) {
  assert.equal(frame.motionFoundation.set, poc.set)
  assert.equal(frame.motionFoundation.candidateSha256, poc.frames[frame.id].candidate.sha256)
  assert.equal(frame.authority.sha256, poc.frames[frame.id].authority.sha256)
  assert.deepEqual(frame.authority.translationOnlyOffsetPx, poc.frames[frame.id].translationOnlyOffsetPx)
  assert.equal(frame.generatedUpperSource.sha256, register.sources[frame.kind.startsWith('walk-') ? 'walkUpperBody' : 'turnUpperBody'].sha256)
  assert.equal(frame.hands.maximumAllowed, 2)
  assert.ok(frame.hands.visibleComponentCount <= 2, `${frame.id} visible-hand limit`)
  assert.equal(frame.colourEvidence.nonAuthorityRgbPixels, 0)
  assert.equal(frame.colourEvidence.matchingAuthorityPalette, true)
  assert.equal(frame.ownership.recompositionExact, true)
  assert.equal(frame.ownership.torsoArmOverlapPixels, 0)
  assert.equal(frame.ownership.propLayerPresent, false)
  assert.deepEqual(frame.ownership.layerOrder, data.contract.layerOrder)
  assert.equal(frame.layers.lowerBodyAuthority.audit.changedPixels, 0)
  assert.equal(frame.layers.lowerBodyAuthority.audit.missingPixels, 0)
  assert.equal(frame.layers.lowerBodyAuthority.audit.coveragePercent, 100)
  assert.equal(frame.layers.lowerBodyAuthority.audit.oldArmOrHandSkinPixels, 0)
  assert.equal(frame.layers.lowerBodyOcclusionFill.audit.authorityClaimed, false)
  assert.equal(frame.layers.lowerBodyOcclusionFill.audit.separateReversibleLayer, true)

  const files = {
    authority: frame.authority.registeredFile,
    lower: frame.layers.lowerBodyAuthority.file,
    fill: frame.layers.lowerBodyOcclusionFill.file,
    torso: frame.layers.torsoHead.file,
    arms: frame.layers.heldArms.file,
    composite: frame.composite.file,
    lowerMask: frame.masks.lowerBodyAuthority.file,
    armMask: frame.masks.heldArmOwnership.file,
  }
  for (const [part, file] of Object.entries(files)) {
    const image = png(file)
    assert.deepEqual([image.width, image.height], [384, 320], `${frame.id} ${part} geometry`)
    if (!part.endsWith('Mask') && part !== 'authority') assert.equal(edgeAlpha(image), 0, `${frame.id} ${part} shared-edge alpha`)
  }
  for (const part of ['lowerBodyAuthority', 'lowerBodyOcclusionFill', 'torsoHead', 'heldArms']) {
    assert.equal(sha(frame.layers[part].file), frame.layers[part].sha256, `${frame.id} ${part} hash`)
  }
  assert.equal(sha(frame.composite.file), frame.composite.sha256)
  assert.equal(sha(frame.masks.lowerBodyAuthority.file), frame.masks.lowerBodyAuthority.sha256)
  assert.equal(sha(frame.masks.heldArmOwnership.file), frame.masks.heldArmOwnership.sha256)
  assert.equal(sha(frame.gripGuide.file), frame.gripGuide.sha256)
  assert.equal(frame.composite.edgeAlphaPixels, 0)
  assert.ok(frame.composite.transparentGutterPx >= 4)

  const authority = png(files.authority)
  const lower = png(files.lower)
  const mask = png(files.lowerMask)
  for (let offset = 0; offset < mask.data.length; offset += 4) {
    if (!mask.data[offset]) continue
    for (let channel = 0; channel < 4; channel++) {
      assert.equal(lower.data[offset + channel], authority.data[offset + channel], `${frame.id} exact lower byte ${offset + channel}`)
    }
  }
  const torso = png(files.torso)
  const arms = png(files.arms)
  for (let offset = 3; offset < torso.data.length; offset += 4) {
    assert.ok(!(torso.data[offset] && arms.data[offset]), `${frame.id} torso/arm overlap`)
  }
  const recomposed = alphaOver(alphaOver(alphaOver(lower, png(files.fill)), torso), arms)
  const composite = png(files.composite)
  assert.equal(recomposed.data.length, composite.data.length)
  for (let pixel = 0; pixel < composite.width * composite.height; pixel++) {
    const offset = pixel * 4
    assert.ok(Math.abs(recomposed.data[offset + 3] - composite.data[offset + 3]) <= 1, `${frame.id} recomposition alpha ${pixel}`)
    if (!composite.data[offset + 3]) continue // transparent RGB bytes have no visible ownership
    for (let channel = 0; channel < 3; channel++) {
      assert.ok(Math.abs(recomposed.data[offset + channel] - composite.data[offset + channel]) <= 1,
        `${frame.id} recomposition pixel ${pixel} channel ${channel}`)
    }
  }
}

const rightWalk = data.route.slice(0, 8)
const leftWalk = data.route.slice(25)
for (let i = 1; i < rightWalk.length; i++) assert.equal(rightWalk[i].rootXLp - rightWalk[i - 1].rootXLp, 2.625)
for (let i = 1; i < leftWalk.length; i++) assert.equal(leftWalk[i - 1].rootXLp - leftWalk[i].rootXLp, 2.625)
assert.equal(data.route[17].presentationOffsetXLp, -1)
assert.equal(data.route[17].renderAnchorXLp, 30.25)

for (const asset of register.publishedAssets) assert.equal(sha(asset.source), asset.sourceSha256)
assert.equal(archiveManifest.set, data.set)
assert.equal(Object.keys(archiveManifest.entries).length, register.publishedAssets.length)
assert.equal(archiveManifest.page.sha256, sha(register.candidate.publicShell.file))
for (const asset of register.publishedAssets) {
  const legacyPath = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
  const archived = archiveManifest.entries[legacyPath]
  assert.ok(archived, `archive entry missing: ${legacyPath}`)
  assert.equal(archived.sha256, asset.sourceSha256)
  assert.equal(sha(archived.object), archived.sha256)
  assert.equal(archived.url, asset.url)
}
for (const sheet of Object.values(register.candidate.sheets)) assert.equal(sha(sheet.file), sheet.sha256)
assert.equal(sha(register.candidate.routeData.file), register.candidate.routeData.sha256)
assert.equal(sha(register.candidate.reviewer.file), register.candidate.reviewer.sha256)
assert.equal(sha(register.candidate.publicShell.file), register.candidate.publicShell.sha256)

for (const token of [
  'Exact approved lower bodies', 'Separable torso + arms', 'No implement', 'Nothing promoted',
  'occlusion-fill layer', 'Large · 6 px/lp', 'Gameplay · 4 px/lp', 'Literal · 1 px/lp',
  "['ghost','lower','fill','torso','arms','guide']", 'Loading and decoding every unique frame',
  'img.decode', 'if(i===sequence.length-1){stop();return}', 'lowerBodyOcclusionFill',
]) assert.ok(reviewer.includes(token), `reviewer omits ${token}`)
assert.ok(!reviewer.includes('i=(i+1)%sequence.length;show();timer=setTimeout'))
assert.doesNotMatch(shell, /\/main\/art\/drafts/)
assert.ok(shell.includes('__LAYERED_V1_COMMIT__') || /lighthouse-keeper\/[0-9a-f]{8,40}\/art\/drafts\/keeper-prime-hold-shaft-two-hand-layered-2026-10-19-v1\/reviewer\.html/.test(shell))

console.log(`Prime layered hold_shaft_two_hand V1 verified: ${frames.length} separable frames, exact declared lower-body authority bytes, explicit occlusion fills, unchanged approved 33-frame route, no prop, and no production promotion.`)

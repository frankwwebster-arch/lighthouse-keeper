#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-rear-action-sequence-v1'
const draft = 'art/drafts/keeper-prime-rear-action-sequence-2026-10-20-v1'
const abs = value => path.join(root, value)
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')

const source = json('public/keeper-review/activity-cloud-composer-v6/catalogue.json')
const catalogue = json(`public/keeper-review/${set}/catalogue.json`)
const draftCatalogue = json(`${draft}/catalogue.json`)
const register = json(`${draft}/batch-register.json`)
const page = fs.readFileSync(abs(`public/keeper-review/${set}/index.html`), 'utf8')

assert.equal(catalogue.schema, 'lighthouse-keeper/keeper-prime-rear-action-sequence@1')
assert.equal(catalogue.set, set)
assert.equal(catalogue.status, 'immutable-reversible-review-candidate-not-approved')
assert.deepEqual(catalogue, draftCatalogue)
assert.equal(catalogue.sourceCatalogue.set, 'activity-cloud-composer-v6')
assert.equal(catalogue.sourceCatalogue.sha256, sha(catalogue.sourceCatalogue.file), 'source catalogue drift')
assert.equal(catalogue.sequence.length, 52)
assert.equal(catalogue.actionStartIndex, 28)
assert.deepEqual(catalogue.sequence, source.route.slice(0, 52), 'sequence changed inherited route bytes')
assert.deepEqual(catalogue.phaseCounts, {
  'approved walk': 16,
  'approved deceleration': 4,
  'approved turn away': 8,
  'Prime rear-work action': 24,
})

const exactRear = source.reviewReferences.exactRear
assert.equal(catalogue.sequence[27].src, exactRear, 'turn does not land on exact rear neutral')
assert.equal(catalogue.sequence[28].src, exactRear, 'action F1 is not exact rear neutral')
assert.equal(catalogue.sequence[50].src, exactRear, 'action F23 is not exact rear neutral')
assert.equal(catalogue.sequence[51].src, exactRear, 'action F24 is not exact rear neutral')
assert.equal(catalogue.sequence[27].x, catalogue.sequence[28].x, 'turn-to-action root moved')
for (const frame of catalogue.sequence.slice(28)) assert.equal(frame.x, catalogue.sequence[28].x, 'action root moved')
assert.ok(Math.abs(catalogue.sequenceDurationMs - 8433.333333333334) < 0.001)

assert.deepEqual(catalogue.callout, {
  frames: 42,
  fps: 8,
  quietTailFrames: 5,
  startsWithAction: true,
  placement: 'raised-above-cap',
})
assert.deepEqual(Object.keys(catalogue.recipes), ['garden-bbq', 'make-sandwich', 'washing-up', 'make-tea', 'general-mending'])
assert.equal(catalogue.defaultRecipe, 'garden-bbq')
for (const [key, recipe] of Object.entries(catalogue.recipes)) {
  assert.equal(recipe.bodyCompatibility, 'rear-work-with-context', `${key} is not rear-work compatible`)
  assert.ok(recipe.elements.length >= 4 && recipe.elements.length <= 5, `${key} must contain four or five elements`)
  assert.ok(recipe.sfx, `${key} is missing an SFX declaration`)
  for (const component of recipe.elements) {
    assert.ok(source.components[component], `${key} references unknown ${component}`)
    assert.equal(source.components[component].cellPixels.join('x'), '256x256', `${component} cell geometry drift`)
  }
}

assert.deepEqual(catalogue.controls, ['body', 'callout', 'treatment', 'sfx-declaration', 'timeline', 'loop'])
assert.equal(catalogue.separation.bodySilent, true)
assert.equal(catalogue.separation.contextBakedIntoKeeper, false)
assert.equal(catalogue.separation.componentsIndependent, true)
assert.equal(catalogue.separation.sfxIndependent, true)
assert.equal(catalogue.approvalBoundary.runtimeChanged, false)
assert.equal(catalogue.approvalBoundary.finalChanged, false)
assert.equal(catalogue.approvalBoundary.kitchenChanged, false)
assert.equal(catalogue.approvalBoundary.deployed, false)

assert.equal(register.schema, 'lighthouse-keeper/keeper-prime-rear-action-sequence-register@1')
assert.equal(register.candidate.sequenceFrames, 52)
assert.equal(register.candidate.actionStartIndex, 28)
assert.equal(register.checks.preloadAndDecodeBeforePlayback, true)
assert.equal(register.checks.singleSynchronizedClock, true)
assert.equal(register.checks.calloutHiddenBeforeAction, true)
assert.equal(register.checks.bodyCalloutSfxIndependent, true)
assert.equal(register.checks.noNewMedia, true)
assert.equal(sha(register.files.catalogue.file), register.files.catalogue.sha256)
assert.equal(sha(register.files.page.file), register.files.page.sha256)
assert.equal(sha(register.files.template.file), register.files.template.sha256)
assert.equal(register.files.page.sha256, register.files.template.sha256)

assert.match(page, /Prime walk → stop → turn → perform action/)
assert.match(page, /Promise\.all/)
assert.match(page, /img\.decode/)
assert.match(page, /requestAnimationFrame/)
assert.match(page, /elapsed>=actionStart/)
assert.match(page, /calloutVisible/)
assert.match(page, /bodyVisible/)
assert.match(page, /muted/)
assert.match(page, /Open radial · no bubble/)
assert.match(page, /Activity bustle · bubble/)
assert.doesNotMatch(page, /<div[^>]+class="[^"]*counter/i)
assert.doesNotMatch(page, /kitchenChanged\s*:\s*true/)
const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)]
assert.equal(scripts.length, 1)
new vm.Script(scripts[0][1])

console.log(JSON.stringify({
  set,
  sequenceFrames: 52,
  phases: catalogue.phaseCounts,
  durationSeconds: Number((catalogue.sequenceDurationMs / 1000).toFixed(3)),
  activitySets: Object.keys(catalogue.recipes).length,
  exactRearSeam: true,
  synchronizedCallout: true,
  newMedia: 0,
  runtimeChanged: false,
  kitchenChanged: false,
  deployed: false,
}, null, 2))

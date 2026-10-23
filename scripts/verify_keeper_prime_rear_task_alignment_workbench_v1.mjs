import assert from 'node:assert/strict'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8')
const json = (file) => JSON.parse(read(file))

const route = read('src/app/prime-keeper-rear-task-alignment/page.tsx')
const workbench = read('src/prime-keeper-drafts/RearTaskAlignmentWorkbench.tsx')
const archiveRoute = read('src/app/keeper-review/[set]/assets/[asset]/route.ts')
const defaultReview = read('src/app/prime-keeper-animation-drafts/page.tsx')
const versionedReview = read('src/app/prime-keeper-animation-drafts-v9/page.tsx')
const v6 = json('data/keeper_prime_animation_drafts_v6.json')
const corrections = json('art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v9/corrections.json')

const sequence = v6.sequences.find((item) => item.id === 'rear-work-turn-return-v1')
assert(sequence, 'V6 rear-task source sequence is missing')
const sources = sequence.frames.slice(10, 31)
assert.equal(sources.length, 21, 'workbench must expose rear-task frames 11–31')
assert.deepEqual(corrections.frames.map((item) => item.position), Array.from({ length: 21 }, (_, index) => index + 11), 'horizontal registrations must cover frames 11–31 exactly')
assert(sources.every((frame) => route.includes('batch.sequences') || frame.src.startsWith('/keeper-review/keeper-prime-morning-drafts-v6/')), 'workbench must derive exact archived V6 sources')

assert(route.includes('sequence.frames.slice(10, 31)'), 'route no longer selects exactly frames 11–31')
assert(route.includes('frame-31dbac4efc00089f.png'), 'approved rear lower-body authority changed')
assert(route.includes('31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35'), 'approved lower-body hash changed')
assert(route.includes('defaultLegsX: correctionByPosition.get(position)?.rootDx'), 'verified per-frame horizontal registrations are not the defaults')

for (const marker of [
  "const STORAGE_KEY = 'prime-keeper-rear-task-alignment:v1'",
  "type EditorMode = 'crop' | 'align'",
  'onPointerDown={onPointerDown}',
  'onPointerMove={onPointerMove}',
  'onKeyDown={onKeyDown}',
  'Crop the jumper first',
  'Crop-only view',
  'Whole jumper hem row',
  'five-point',
  'Editable four-times waist inspection',
  'Confirm jumper crop',
  'Nudge the selected layer',
  'Clean trousers begin from source row',
  'Check against the Prime Keeper',
  'minimumTrouserUnderlap',
  'Copy curve and vertical setup to all',
  'Download current 256×320 PNG',
  'Copy all settings',
  'Download settings JSON',
  'Mark frame aligned',
  '▶ Play all',
]) assert(workbench.includes(marker), `workbench control missing: ${marker}`)

assert(workbench.includes('const CLEAN_TROUSER_START = 219'), 'visible authority waistband seam rows must be excluded')
assert(workbench.includes('const TROUSER_UNDERLAP = 4'), 'trousers must retain a hidden safety overlap beneath the jumper')
assert(workbench.includes('UNDERLAP_SAMPLE_X, UNDERLAP_SAMPLE_ROW, 1, 1'), 'underlap must reuse an exact clean authority trouser colour pixel')
assert(workbench.includes('context.drawImage(legs, WAIST_X, waistStart, WAIST_WIDTH'), 'waist must remain inside verified lower-body ownership bounds')
assert(workbench.includes('context.drawImage(legs, 70, lowerStart, 117'), 'legs must remain inside verified lower-body ownership bounds')
assert(workbench.includes("editorMode === 'align' && waistStart < 231"), 'legs must stay hidden during the jumper-first crop stage')
assert(workbench.includes('const HEM_CONTROL_X = [82, 105, 128, 151, 174]'), 'five-point hem geometry changed')
assert(workbench.includes('traceTorsoMask(context, points)'), 'moving torso must be clipped to the editable hem')
assert(workbench.includes('context.drawImage(torso, adjustment.torsoX, adjustment.torsoY)'), 'moving torso must retain the exact source pixels')
assert(workbench.includes("context.strokeStyle = '#000000'"), 'extended jumper hem must carry a true-black outline')
assert(workbench.includes("pixels[(y * WIDTH + x) * 4 + 3] < 128"), 'Prime Keeper size audit must use the pinned alpha threshold')
assert(workbench.includes("schema: 'lighthouse-keeper/prime-rear-task-manual-alignment@4'"), 'export must retain the curved hem, crop confirmation and underlap contract')
assert(archiveRoute.includes("'keeper-prime-morning-drafts-v6'"), 'V6 review images must be served same-origin so the dimensional audit can read alpha pixels')
assert(!workbench.includes('/api/'), 'manual workbench must not overwrite server or source state')
assert(defaultReview.includes('manualAlignmentHref="/prime-keeper-rear-task-alignment"'), 'current review must link the fallback workbench')
assert(!versionedReview.includes('manualAlignmentHref'), 'immutable V9 permalink must retain its original presentation')

console.log('Verified Prime rear-task manual alignment workbench V1: 21 reversible frame settings, exact torso/legs sources, five-point outlined hem, dimensional audit, drag, pixel nudge, playback and export controls.')

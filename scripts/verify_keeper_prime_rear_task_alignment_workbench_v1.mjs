import assert from 'node:assert/strict'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8')
const json = (file) => JSON.parse(read(file))

const route = read('src/app/prime-keeper-rear-task-alignment/page.tsx')
const upperSeamRoute = read('src/app/prime-keeper-rear-task-alignment-v2/page.tsx')
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
assert(upperSeamRoute.includes('sequence.frames.slice(10, 31)'), 'upper-seam route no longer selects exactly frames 11–31')
assert(upperSeamRoute.includes('joinStrategy="upper-jumper-seam"'), 'V2 must select the upper-jumper-seam compositor')
assert(upperSeamRoute.includes('?manual-alignment=upper-seam-v2'), 'V2 must use a fresh asset URL prefix')
assert(upperSeamRoute.includes('31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35'), 'V2 approved authority hash changed')

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
  'Show exact Prime ghost',
  'Hide exact Prime ghost',
  'Prime Keeper ghost opacity',
  'minimumTrouserUnderlap',
  'Copy curve and vertical setup to all',
  'Download current 256×320 PNG',
  'Copy all settings',
  'Download settings JSON',
  'Mark frame aligned',
  '▶ Play all',
]) assert(workbench.includes(marker), `workbench control missing: ${marker}`)

assert(workbench.includes('const CLEAN_TROUSER_START = 219'), 'visible authority waistband seam rows must be excluded')
assert(workbench.includes('const AUTHORITY_WAISTBAND_START = 201'), 'approved upper jumper-band seam row changed')
assert(workbench.includes("const UPPER_SEAM_STORAGE_KEY = 'prime-keeper-rear-task-alignment:v2:upper-seam'"), 'V2 must not reuse V1 browser settings')
assert(workbench.includes('function drawJumperBodyExtension('), 'upper-seam compositor must extend exact moving jumper-body pixels to the approved band')
assert(workbench.includes('context.drawImage(legs, AUTHORITY_WAISTBAND_X, waistStart, AUTHORITY_WAISTBAND_WIDTH'), 'upper-seam compositor must preserve the complete exact approved band')
assert(workbench.includes('if (!upperSeamJoin) {\n      traceHem(context, points)'), 'upper-seam crop must not draw a replacement black seam')
assert(workbench.includes('const TROUSER_UNDERLAP = 4'), 'trousers must retain a hidden safety overlap beneath the jumper')
assert(workbench.includes('context.drawImage(legs, WAIST_X + column, sourceY, 1, 1'), 'underlap must extend exact approved trouser pixels column-by-column')
assert(workbench.includes('const TROUSER_OUTLINE_LEFT_X = 83'), 'left trouser outline extension changed')
assert(workbench.includes('const TROUSER_OUTLINE_RIGHT_X = 171'), 'right trouser outline extension changed')
assert(workbench.includes('context.drawImage(legs, WAIST_X, waistStart, WAIST_WIDTH'), 'waist must remain inside verified lower-body ownership bounds')
assert(workbench.includes('context.drawImage(legs, 70, lowerStart, 117'), 'legs must remain inside verified lower-body ownership bounds')
assert(workbench.includes("if (editorMode === 'align' && upperSeamJoin)"), 'V2 lower authority must stay hidden during the upper-seam crop stage')
assert(workbench.includes("} else if (editorMode === 'align') {"), 'V1 legs must stay hidden during the jumper-first crop stage')
assert(workbench.includes('const HEM_CONTROL_X = [82, 105, 128, 151, 174]'), 'five-point hem geometry changed')
assert(workbench.includes('traceTorsoMask(context, points)'), 'moving torso must be clipped to the editable hem')
assert(workbench.includes('context.drawImage(torso, adjustment.torsoX, adjustment.torsoY)'), 'moving torso must retain the exact source pixels')
assert(workbench.includes("context.strokeStyle = '#000000'"), 'extended jumper hem must carry a true-black outline')
assert(workbench.includes("pixels[(y * WIDTH + x) * 4 + 3] < 128"), 'Prime Keeper size audit must use the pinned alpha threshold')
assert(workbench.includes('ghostContext.drawImage(legs, 0, 0)'), 'Prime ghost must use the exact approved rear authority at canonical position and scale')
assert(workbench.includes('className={styles.primeGhost}'), 'Prime ghost must remain a separate non-destructive canvas layer')
assert(workbench.includes("link.href = canvasRef.current?.toDataURL('image/png')"), 'download must exclude the separate Prime ghost overlay')
assert(workbench.includes("'lighthouse-keeper/prime-rear-task-manual-alignment@4'"), 'V1 export must retain the curved hem, crop confirmation and underlap contract')
assert(workbench.includes("'lighthouse-keeper/prime-rear-task-upper-seam-alignment@1'"), 'V2 export must identify the corrected upper-seam contract')
assert(archiveRoute.includes("'keeper-prime-morning-drafts-v6'"), 'V6 review images must be served same-origin so the dimensional audit can read alpha pixels')
assert(!workbench.includes('/api/'), 'manual workbench must not overwrite server or source state')
assert(defaultReview.includes('keeper_prime_animation_drafts_v11'), 'current review must advance to the complete-arm V11 correction')
assert(!defaultReview.includes('manualAlignmentHref='), 'superseded seam-alignment workbench must not remain the primary review action')
assert(!versionedReview.includes('manualAlignmentHref'), 'immutable V9 permalink must retain its original presentation')

console.log('Verified Prime rear-task manual alignment workbenches: immutable V1 lower-seam fallback plus V2 upper-seam removal with exact approved band/lower seam, separate settings, exact-Prime ghost and reversible exports.')

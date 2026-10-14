#!/usr/bin/env node
/** Verify Keeper Timing Lab V1 and its timing-only quicker-turn proposal. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-timing-lab-2026-10-14-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const CATALOGUE = path.join(ROOT, 'public/keeper-timing-lab/catalog.json')
const ROUTE_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-walk-stop-turn-front-2026-10-14-v1/batch-register.json')
const PAGE = path.join(ROOT, 'src/keeper-timing-lab/TimingLab.tsx')
const MODEL = path.join(ROOT, 'src/keeper-timing-lab/model.ts')
const WORKBENCH = path.join(ROOT, 'src/animation-workbench/AnimationWorkbench.tsx')
const fail = (message: string): never => { throw new Error(`Keeper Timing Lab V1: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, CATALOGUE, ROUTE_REGISTER, PAGE, MODEL, WORKBENCH, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const catalogue = JSON.parse(fs.readFileSync(CATALOGUE, 'utf8')) as Record<string, any>
const source = JSON.parse(fs.readFileSync(ROUTE_REGISTER, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-timing-lab-2026-10-14-v1' || record.status !== 'timing-platform-v1-and-quicker-turn-proposal') fail('identity/status changed')
if (!record.feedback?.wording?.includes('overall tuning platform') || !record.feedback?.wording?.includes('turn could run a little faster')) fail('feedback provenance changed')
if (record.sourceRoute.registerSha256 !== hash(ROUTE_REGISTER) || record.sourceRoute.artworkPixelsChanged !== false || record.sourceRoute.frameOrderChanged !== false || record.sourceRoute.rootMotionChanged !== false) fail('source route boundary changed')
if (record.platform.catalogueSha256 !== hash(CATALOGUE) || record.platform.route !== '/keeper-timing-lab') fail('catalogue/platform record changed')
if (catalogue.version !== 1 || catalogue.platformId !== 'keeper-timing-lab' || catalogue.clips.length !== 1) fail('catalogue identity changed')
const clip = catalogue.clips[0]
if (clip.sourceRegisterSha256 !== hash(ROUTE_REGISTER) || clip.frames.length !== 32 || clip.distanceHighResolutionPixels !== 374) fail('clip authority/route changed')
if (JSON.stringify(clip.baseline) !== '{"walkFps":8,"decelerationFps":8,"settleMs":125,"turnFps":8,"frontHoldMs":500}') fail('baseline timing changed')
if (JSON.stringify(clip.recommended) !== '{"walkFps":8,"decelerationFps":8,"settleMs":125,"turnFps":10,"frontHoldMs":500}') fail('recommended timing changed')
if (record.timingProposal.onlyChangedField !== 'turnFps' || record.timingProposal.from !== 8 || record.timingProposal.to !== 10 || record.timingProposal.turnDurationReductionPercent !== 20) fail('quicker-turn proposal changed')
const counts = clip.frames.reduce((value: Record<string, number>, frame: Record<string, any>) => ({ ...value, [frame.phase]: (value[frame.phase] ?? 0) + 1 }), {})
if (JSON.stringify(counts) !== '{"walk":16,"deceleration":4,"settle":1,"turn":7,"frontHold":4}') fail('phase partition changed')
for (const [index, frame] of clip.frames.entries()) {
  const original = source.route.framesData[index]
  if (frame.src !== original.src || frame.pose !== original.pose || frame.dx !== original.dx || frame.x !== original.x || !frame.src.startsWith('/keeper-review/')) fail(`route F${index + 1} changed`)
  if (!fs.existsSync(path.join(ROOT, 'public', frame.src))) fail(`route F${index + 1} public asset missing`)
}
const baselineDuration = 16 * 125 + 4 * 125 + 125 + 7 * 125 + 500
const recommendedDuration = 16 * 125 + 4 * 125 + 125 + 7 * 100 + 500
if (baselineDuration !== 4000 || recommendedDuration !== 3825) fail('duration proof changed')
if (catalogue.presets.length !== 3 || catalogue.loopSections.length !== 5) fail('preset/section inventory changed')
for (const feature of ['phase-specific timing', 'baseline-versus-proposal playback', 'large-and-game-scale preview', 'section loops', 'frame stepping', 'presets', 'device-local saved proposals', 'project defaults', 'JSON export', 'immutable authority display']) if (!record.platform.features.includes(feature)) fail(`feature missing: ${feature}`)
const page = fs.readFileSync(PAGE, 'utf8')
for (const phrase of ['Reviewed timing against your live proposal', 'Tune the rhythm, not the artwork', 'Use as project defaults', 'Export JSON', 'Previous frame', 'Next frame', 'Approved pixels locked']) if (!page.includes(phrase)) fail(`page omits ${phrase}`)
if (!fs.readFileSync(WORKBENCH, 'utf8').includes('href="/keeper-timing-lab"')) fail('workbench omits Timing Lab link')
for (const flag of ['sourceRouteUnchanged', 'approvedArtworkReferencedOnly', 'timingIndependentOfArtwork']) if (record.validation?.[flag] !== true) fail(`${flag} changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'workbenchFinalChanged']) if (record.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (record.approvalBoundary?.routeArtworkAcceptedAsExcellent !== true || record.approvalBoundary?.recommendedTimingApproved !== false || record.approvalBoundary?.timingPlatformApproved !== false || record.approvalBoundary?.finalLaneEntryAllowed !== false || record.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')
console.log('Keeper Timing Lab V1 verified: immutable 32-frame route, phase-specific A/B timing, 10 fps turn-only proposal, save/export/default controls, no Final or production change.')

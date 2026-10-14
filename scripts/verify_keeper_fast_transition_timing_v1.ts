#!/usr/bin/env node
/** Verify approved Fast Timing V1 without widening its scope to action timing. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-fast-transition-timing-2026-10-14-v1')
const REGISTER = path.join(PACK, 'approval-register.json')
const SOURCE_CATALOGUE = path.join(ROOT, 'public/keeper-timing-lab/catalog.json')
const CATALOGUE = path.join(ROOT, 'public/keeper-timing-lab/catalog-v2.json')
const POLICY = path.join(ROOT, 'data/keeper_timing_policy.json')
const ROUTE_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-walk-stop-turn-front-2026-10-14-v1/batch-register.json')
const RUNTIME_MANIFEST = path.join(ROOT, 'public/sprites/manifest.json')
const WORKBENCH = path.join(ROOT, 'data/keeper_animation_workbench.json')
const PAGE = path.join(ROOT, 'src/keeper-timing-lab/TimingLab.tsx')
const fail = (message: string): never => { throw new Error(`Keeper Fast Timing V1: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const read = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8')) as Record<string, any>

for (const file of [REGISTER, SOURCE_CATALOGUE, CATALOGUE, POLICY, ROUTE_REGISTER, RUNTIME_MANIFEST, WORKBENCH, PAGE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}

const record = read(REGISTER)
const source = read(SOURCE_CATALOGUE)
const catalogue = read(CATALOGUE)
const policy = read(POLICY)
const route = read(ROUTE_REGISTER)
const expected = { walkFps: 10, decelerationFps: 12, settleMs: 0, turnFps: 16, frontHoldMs: 625 }

if (record.batchId !== 'keeper-fast-transition-timing-2026-10-14-v1' || record.status !== 'approved-transition-timing-authority') fail('identity/status changed')
if (record.approval?.approvalWording !== 'approve fast timing v1' || record.approval?.approvedOn !== '2026-10-14') fail('approval provenance changed')
if (JSON.stringify(record.approval?.profile) !== JSON.stringify(expected)) fail('approved profile changed')
if (record.source?.timingLabV1CatalogueSha256 !== hash(SOURCE_CATALOGUE) || hash(SOURCE_CATALOGUE) !== '95d85d2754f8c443f80cc778bdd7800973fc869422c43aa95cdb9c98c9542689') fail('V1 catalogue history changed')
if (record.source?.routeRegisterSha256 !== hash(ROUTE_REGISTER) || hash(ROUTE_REGISTER) !== '730dec649217466bde895875d07e6729fe759d19d436cb93203698d41a94ab10') fail('source route changed')
if (record.candidate?.catalogueSha256 !== hash(CATALOGUE)) fail('V2 catalogue hash changed')
if (record.candidate?.projectTimingPolicySha256 !== hash(POLICY) || catalogue.projectTimingPolicy?.sha256 !== hash(POLICY)) fail('project timing policy hash changed')
if (catalogue.version !== 2 || catalogue.platformId !== 'keeper-timing-lab' || catalogue.clips?.length !== 1) fail('catalogue identity changed')
if (JSON.stringify(catalogue.defaults) !== JSON.stringify(expected) || JSON.stringify(catalogue.approvedTransitionProfile?.profile) !== JSON.stringify(expected)) fail('repository transition default changed')
if (catalogue.approvedTransitionProfile?.status !== 'approved-transition-authority' || catalogue.approvedTransitionProfile?.approvalWording !== 'approve fast timing v1') fail('catalogue approval changed')
for (const phrase of ['action entry', 'action loops', 'action exit', 'comic reactions', 'prop choreography', 'activity-specific performance timing']) {
  if (!catalogue.approvedTransitionProfile.excludes.includes(phrase)) fail(`action exclusion missing: ${phrase}`)
}
if (!catalogue.approvedTransitionProfile.policy.includes('never inherits Fast Timing V1')) fail('action timing independence changed')
if (policy.policyId !== 'keeper-fast-transition-timing-v1' || policy.status !== 'approved-project-timing-policy' || JSON.stringify(policy.transitionProfile) !== JSON.stringify(expected)) fail('project timing policy changed')
if (policy.actionTiming?.inheritsTransitionProfile !== false || !policy.actionTiming?.rule?.includes('never inherits Fast Timing V1')) fail('project action timing boundary changed')
if (policy.runtimeIntegration?.implemented !== false) fail('runtime integration was claimed without a separate promotion')

const sourceClip = source.clips[0]
const clip = catalogue.clips[0]
if (clip.status !== 'artwork-and-fast-transition-timing-approved' || clip.timingAuthority !== 'keeper-fast-transition-timing-v1') fail('clip timing authority changed')
if (JSON.stringify(clip.recommended) !== JSON.stringify(expected)) fail('clip approved timing changed')
if (clip.frames.length !== 32 || clip.distanceHighResolutionPixels !== 374 || JSON.stringify(clip.frames) !== JSON.stringify(sourceClip.frames)) fail('frame order, URLs or root motion changed')
if (clip.sourceRegisterSha256 !== hash(ROUTE_REGISTER) || JSON.stringify(clip.endpointContract) !== JSON.stringify(route.endpointContract)) fail('route authority or endpoint contract changed')
for (const frame of clip.frames) if (!fs.existsSync(path.join(ROOT, 'public', frame.src))) fail(`missing approved frame ${frame.src}`)

const counts = clip.frames.reduce((value: Record<string, number>, frame: Record<string, any>) => ({ ...value, [frame.phase]: (value[frame.phase] ?? 0) + 1 }), {})
if (JSON.stringify(counts) !== '{"walk":16,"deceleration":4,"settle":1,"turn":7,"frontHold":4}') fail('phase partition changed')
const duration = counts.walk * 1000 / expected.walkFps + counts.deceleration * 1000 / expected.decelerationFps + expected.settleMs + counts.turn * 1000 / expected.turnFps + expected.frontHoldMs
if (Math.abs(duration - 2995.833333333333) > 1e-9 || record.candidate.baselineDurationMs !== 4000) fail('duration proof changed')

if (record.unchangedAuthorities?.runtimeManifestSha256 !== hash(RUNTIME_MANIFEST) || hash(RUNTIME_MANIFEST) !== 'a3097b45ceda663a77033db869d0b4e51b3223e4a258dc65ccef5dd55115f174') fail('runtime manifest changed')
if (record.unchangedAuthorities?.workbenchCatalogueSha256 !== hash(WORKBENCH) || hash(WORKBENCH) !== '6c349a70f591cba21016cf9a7a49424b971d8aed895504ba775ebd158017c658') fail('workbench lanes changed')
for (const key of ['artworkPixelsChanged', 'frameOrderChanged', 'rootMotionChanged', 'endpointContractChanged', 'productionSpritesChanged', 'runtimeManifestChanged', 'workbenchFinalChanged', 'actionTimingChanged']) {
  if (record.immutableBoundaries?.[key] !== false) fail(`${key} boundary changed`)
}

const page = fs.readFileSync(PAGE, 'utf8')
for (const phrase of ['catalog-v2.json', 'Fast Timing V1 is approved', 'Action animation timing remains independent', 'Use as personal preview default', 'Reset to approved', 'Fast between activities; expressive inside them']) {
  if (!page.includes(phrase)) fail(`Timing Lab omits ${phrase}`)
}

console.log('Keeper Fast Timing V1 verified: 10 fps walk, 12 fps deceleration, zero settle, 16 fps turn and 625 ms endpoint hold; approved only for transitions, with artwork, action timing, Final and production unchanged.')

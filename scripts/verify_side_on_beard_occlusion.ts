#!/usr/bin/env node
/** Verify that the evidence-based beard audit cannot silently become permissive. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'
const ROOT = path.resolve(import.meta.dirname, '..')
const audit = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/keeper_side_on_beard_occlusion_audit.json'), 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'public/sprites/manifest.json'), 'utf8')) as Record<string, any>
const absolute = (file: string) => path.join(ROOT, file)
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message: string): never => { throw new Error(`side-on beard audit: ${message}`) }
if (audit.auditId !== '2026-10-11-evidence-v3' || audit.auditStatus !== 'blocked-no-discriminating-comparison-method') fail('evidence-based fail-closed audit is absent or stale')
if (sha256(absolute(audit.beardReference.strip)) !== audit.beardReference.stripSha256 || sha256(absolute(audit.beardReference.source)) !== audit.beardReference.sourceSha256) fail('canonical beard reference hash changed')
if (audit.method?.maximumAcceptedSilhouetteDeltaLogicalPixels !== 1) fail('the approved one-logical-pixel beard-silhouette tolerance is missing or changed')
if (Object.keys(audit.manifestFrameAudit).length !== Object.keys(manifest).length) fail('manifest frame audit is incomplete or stale')
if (audit.summary.confirmedMismatches !== 0 || audit.summary.draftCorrectionsCreated !== 0 || audit.drafts.active.length !== 0) fail('a correction was claimed without a discriminating comparison method')
let gutterFailures = 0
for (const [name, clip] of Object.entries(manifest)) { const entry = audit.manifestFrameAudit[name]; if (!entry || entry.frames.length !== (clip as any).frames) fail(`${name} has incomplete frame classification`) }
for (const sheet of audit.inventory as Array<Record<string, any>>) {
  if (sha256(absolute(sheet.sourceStrip)) !== sheet.sourceStripSha256 || sha256(absolute(sheet.sourceSidecar)) !== sheet.sourceSidecarSha256) fail(`${sheet.name} source changed after audit`)
  const image = PNG.sync.read(fs.readFileSync(absolute(sheet.sourceStrip))); const width = image.width / sheet.frames; if (!Number.isInteger(width)) fail(`${sheet.name} frame geometry is no longer integral`)
  for (const frame of sheet.frameAudit) { let edgeAlpha = false; const index = frame.frame - 1; for (let y = 0; y < image.height; y += 1) for (const x of [0, width - 1]) if (image.data[(y * image.width + index * width + x) * 4 + 3] > 0) edgeAlpha = true
    for (let x = 0; x < width; x += 1) for (const y of [0, image.height - 1]) if (image.data[(y * image.width + index * width + x) * 4 + 3] > 0) edgeAlpha = true
    if (frame.geometry.gutter !== (edgeAlpha ? 'fail' : 'pass')) fail(`${sheet.name} frame ${frame.frame} gutter evidence drifted`)
    const beard = frame.beard; if (!beard) continue
    if (edgeAlpha) gutterFailures += 1
    if (!['match', 'mismatch', 'non-comparable'].includes(beard.result)) fail(`${sheet.name} frame ${frame.frame} has an invalid beard result`)
    if (beard.result === 'match' && (sheet.name !== audit.beardReference.name || beard.comparison?.method !== 'exact-canonical-self-raster' || beard.comparison?.silhouetteDeltaLogicalPixels !== 0 || beard.comparison?.maximumAcceptedSilhouetteDeltaLogicalPixels !== 1)) fail(`${sheet.name} frame ${frame.frame} claims an unsupported beard match`)
    if (beard.result === 'mismatch') fail(`${sheet.name} frame ${frame.frame} claims a mismatch although this blocked audit has no discriminating comparator`)
    if (beard.result === 'non-comparable' && !beard.evidence?.some((item: string) => item.includes('required comparison asset missing'))) fail(`${sheet.name} frame ${frame.frame} non-comparability lacks exact missing evidence`)
    if (beard.disposition === 'accepted-user-visual-review-no-amendment' && (!beard.userReview || sheet.name !== 'keeper_darts' || ![3, 4, 5, 6].includes(frame.frame))) fail(`${sheet.name} frame ${frame.frame} has an unsupported user-visual beard disposition`)
  }
}
const accepted = audit.findings?.acceptedUserVisualReviewNoAmendment
if (!Array.isArray(accepted) || accepted.length !== 1 || accepted[0].animation !== 'keeper_darts' || accepted[0].frames.join(',') !== '3,4,5,6') fail('the limited Darts no-amendment visual review is absent or altered')
const historical = audit.historical?.invalidatedV2
if (!historical || !fs.existsSync(absolute(historical.register)) || sha256(absolute(historical.register)) !== historical.registerSha256) fail('invalid historical v2 evidence is not preserved')
if (audit.summary.existingCanonicalGutterFailures !== gutterFailures) fail('canonical gutter-failure count drifted')
console.log(`Verified fail-closed beard audit: ${audit.summary.auditedSheets} side-on sheets, ${audit.summary.confirmedMatches} exact self matches, ${audit.summary.nonComparableFrames} non-comparable frames, no art correction.`)

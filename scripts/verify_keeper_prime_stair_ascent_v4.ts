#!/usr/bin/env node
/** Verify Stair Ascent V4 is presentation-only and leaves V3 immutable. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v4')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v4.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v4/index.html')
const V3_PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v3/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const SET_MANIFEST = path.join(ROOT, 'review-archive/sets/keeper-prime-stair-ascent-v4.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V4: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
for (const file of [REGISTER, SPEC, PAGE, V3_PAGE, ARCHIVE, SET_MANIFEST, path.join(PACK, 'HANDOFF.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const html = fs.readFileSync(PAGE, 'utf8')
const v3Html = fs.readFileSync(V3_PAGE, 'utf8')
if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v4' || record.status !== 'draft-v4-foreground-banister-occlusion-awaiting-review') fail('identity/status changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`V3 authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered V4 candidate changed')
for (const flag of ['v3Page', 'mediaBytes', 'artwork', 'timing', 'rootMotion', 'stairGeometry', 'finalLane', 'production']) if (spec.unchanged[flag] !== true) fail(`${flag} boundary weakened`)
if (spec.mask.zIndex !== 7 || spec.mask.defaultVisible !== true || spec.mask.stringerPolygonPercent.length !== 4) fail('foreground mask geometry changed')

const timeline = (source: string) => source.match(/const timeline=(\[.*?\]),buttons=/s)?.[1]
const v4Timeline = timeline(html)?.replaceAll('/keeper-prime-stair-ascent-v4/', '/keeper-prime-stair-ascent-v3/')
if (!v4Timeline || v4Timeline !== timeline(v3Html)) fail('V3 timeline/root/timing changed')
const urls = (source: string) => [...new Set(source.match(/\/keeper-review\/keeper-prime-stair-ascent-v3\/assets\/[A-Za-z0-9._-]+/g) ?? [])].sort()
const v3Urls = urls(v3Html)
const v4Urls = [...new Set(html.match(/\/keeper-review\/keeper-prime-stair-ascent-v4\/assets\/[A-Za-z0-9._-]+/g) ?? [])].sort()
if (v3Urls.length !== 17 || v4Urls.length !== 17) fail('frame URL set changed')
if (JSON.stringify(v4Urls.map((url) => url.replace('/keeper-prime-stair-ascent-v4/', '/keeper-prime-stair-ascent-v3/'))) !== JSON.stringify(v3Urls)) fail('V4 aliases do not map one-to-one to V3')
if ((html.match(/class="foregroundBanister"/g) ?? []).length !== 2) fail('foreground mask is not present in both scale views')
for (const phrase of ['foreground bannister mask', 'Foreground bannister mask', 'closed foreground stair stringer', 'Toggle the mask off', 'z-index:7', 'hideBanister']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
try {
  fs.lstatSync(path.join(path.dirname(PAGE), 'assets'))
  fail('V4 public page contains physical binary assets')
} catch (error: any) {
  if (error.message?.startsWith('Keeper Prime stair ascent V4:')) throw error
  if (error.code !== 'ENOENT') throw error
}
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(SET_MANIFEST, 'utf8')) as Record<string, any>
if (manifest.set !== 'keeper-prime-stair-ascent-v4' || Object.keys(manifest.entries).length !== 17) fail('V4 archive manifest changed')
for (let index = 0; index < record.frameUrls.length; index += 1) {
  const v4Url = record.frameUrls[index]
  const v3Url = record.presentation.sourceFrameUrls[index]
  if (!archive.legacyPaths[v4Url] || !manifest.entries[v4Url]) fail(`archive does not resolve V4 URL ${v4Url}`)
  if (archive.legacyPaths[v4Url].sha256 !== archive.legacyPaths[v3Url].sha256) fail(`V4/V3 bytes differ for ${v4Url}`)
}
for (const flag of ['v3PageChanged', 'characterPixelsChanged', 'timingChanged', 'rootMotionChanged', 'stairGeometryChanged', 'finalChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} changed`)
console.log('Keeper Prime stair ascent V4 verified: exact V3 motion/media with a default-on foreground stringer and bannister mask only; no duplicated binaries or promotion.')

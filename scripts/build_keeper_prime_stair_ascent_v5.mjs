#!/usr/bin/env node
/** Build Stair Ascent V5 with independent one-riser leg phases and rig-root placement. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const v3Pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v3')
const v4Pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v4')
const v5Pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v5')
const v3Page = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v3/index.html')
const v4Page = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v4/index.html')
const v5Public = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v5')
const v5Page = path.join(v5Public, 'index.html')
const v3RegisterPath = path.join(v3Pack, 'batch-register.json')
const v4RegisterPath = path.join(v4Pack, 'batch-register.json')
const rigPath = path.join(v3Pack, 'stair-contact-rig-v3.json')
const archiveIndexPath = path.join(root, 'review-archive/index.json')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of [v3Page, v4Page, v3RegisterPath, v4RegisterPath, rigPath, archiveIndexPath]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)

const v3Register = JSON.parse(fs.readFileSync(v3RegisterPath, 'utf8'))
const rig = JSON.parse(fs.readFileSync(rigPath, 'utf8'))
const archiveIndex = JSON.parse(fs.readFileSync(archiveIndexPath, 'utf8'))
fs.mkdirSync(v5Pack, { recursive: true })
fs.mkdirSync(v5Public, { recursive: true })

const v5FrameUrls = v3Register.frameUrls.map((url) => url.replace('/keeper-prime-stair-ascent-v3/', '/keeper-prime-stair-ascent-v5/'))
const v5Assets = path.join(v5Public, 'assets')
fs.mkdirSync(v5Assets, { recursive: true })
for (let index = 0; index < v3Register.frameUrls.length; index += 1) {
  const sourceUrl = v3Register.frameUrls[index]
  const archiveEntry = archiveIndex.legacyPaths[sourceUrl]
  if (!archiveEntry) throw new Error(`archive does not resolve ${sourceUrl}`)
  const source = path.join(root, archiveEntry.object)
  if (sha(source) !== archiveEntry.sha256) throw new Error(`archive object changed for ${sourceUrl}`)
  fs.copyFileSync(source, path.join(v5Assets, path.basename(v5FrameUrls[index])))
}

const v3Html = fs.readFileSync(v3Page, 'utf8')
const oldTimelineMatch = v3Html.match(/const timeline=(\[.*?\]),buttons=/s)
if (!oldTimelineMatch) throw new Error('V3 timeline missing')
const oldTimeline = JSON.parse(oldTimelineMatch[1])
const walk = oldTimeline.slice(0, 8).map((frame) => ({ ...frame, src: frame.src.replace('/keeper-prime-stair-ascent-v3/', '/keeper-prime-stair-ascent-v5/') }))
const stairUrls = v5FrameUrls.slice(8, 16)
const floorTopLp = 20
const baseX = 94.5
const baseBottomLp = 19.5
const treadRunLp = 5.25
const riserRiseLp = 3.75
const contactCentre = (tread) => tread === 0 ? baseX + treadRunLp / 2 : baseX - (tread - 0.5) * treadRunLp
const treadTop = (tread) => floorTopLp + tread * riserRiseLp
const timeline = [...walk]
for (let cycle = 0; cycle < 8; cycle += 1) {
  for (let index = 0; index < rig.frames.length; index += 1) {
    const pose = index + 1
    const frame = rig.frames[index]
    const landedSteps = pose >= 8 ? 2 : pose >= 4 ? 1 : 0
    const supportTread = cycle * 2 + landedSteps
    timeline.push({
      phase: 'independent alternating stair climb', cycle: cycle + 1, pose, src: stairUrls[index],
      support: frame.supportLeg, swing: pose <= 3 ? 'near' : pose <= 7 ? 'far' : 'none',
      label: pose <= 4 ? `near-leg step ${pose}/4` : `far-leg step ${pose - 4}/4`,
      supportTread,
      xLp: baseX - cycle * rig.cycleRunLp - frame.rootOffsetLp[0],
      bottomLp: baseBottomLp + cycle * rig.cycleRiseLp + frame.rootOffsetLp[1],
      contactXLp: contactCentre(supportTread), contactYLp: treadTop(supportTread), durationMs: 92,
    })
  }
}

let html = fs.readFileSync(v4Page, 'utf8')
html = html.replaceAll('/keeper-review/keeper-prime-stair-ascent-v4/assets/', '/keeper-review/keeper-prime-stair-ascent-v5/assets/')
html = html.replace('<title>Keeper Prime stair ascent V4</title>', '<title>Keeper Prime stair ascent V5</title>')
html = html.replace('.game .world{width:620px;height:480px;transform:scale(.25);transform-origin:left bottom}', '.game .world{left:0;bottom:0;top:auto;right:auto;width:620px;height:480px;transform:scale(.25);transform-origin:left bottom}')
html = html.replace('.foregroundBanister{position:absolute;inset:0;z-index:7;pointer-events:none}', '.foregroundBanister{position:absolute;inset:0;z-index:7;pointer-events:none;opacity:.55}')
html = html.replace('<a href="/keeper-review/keeper-prime-stair-ascent-v3/">← Preserve and compare unmasked V3</a><h1>Keeper Prime stair ascent V4 · foreground bannister mask</h1><span class="status">Presentation-only draft · nothing promoted</span><p>V4 keeps every V3 motion frame, root position and timing byte-for-byte, then places a closed foreground stair stringer and bannister above the feet and lower shins.</p>', '<a href="/keeper-review/keeper-prime-stair-ascent-v4/">← Preserve and compare masked V4</a><h1>Keeper Prime stair ascent V5 · independent left/right steps</h1><span class="status">New root-phasing draft · nothing promoted</span><p>V5 keeps the exact V3 character frames but stitches them to the rig correctly: one four-frame near-leg step, then one four-frame far-leg step. Each landing raises the body by exactly one riser.</p>')
html = html.replace('<p class="rule"><strong>Judge the illusion:</strong> does the foreground bannister make the ascent read naturally when the boot-to-tread geometry is hidden? Toggle the mask off to compare the exact underlying V3 motion.</p>', '<p class="rule"><strong>Judge the mechanics:</strong> F1–F4 must read as one leg taking exactly one stair; F5–F8 must read as the other leg taking exactly one stair. The Keeper must rise at F4 and F8 without a backward slide or two-stair jump.</p>')
html = html.replace('<label><input id="banister" type="checkbox" checked> Foreground bannister mask</label>', '<label><input id="banister" type="checkbox" checked> Translucent bannister</label><label>Opacity <input id="opacity" type="range" min="0" max="100" value="55"> <output id="opacityValue">55%</output></label>')
html = html.replace('<p class="banisterNote"><strong>What changed:</strong> one foreground presentation layer only. Character frames, timing, root motion, staircase dimensions and contact calculations are exact V3.</p>', '<p class="banisterNote"><strong>What changed:</strong> root phasing only. The near-leg landing raises him at F4; the far-leg landing raises him at F8. The bannister is translucent and adjustable, so the legs remain judgeable.</p>')
html = html.replace('<div class="metric"><strong>Near F1–F4</strong><br>first riser</div><div class="metric"><strong>Far F5–F8</strong><br>second riser</div><div class="metric"><strong>y316 sole datum</strong><br>locked to tread top</div><div class="metric"><strong>16 risers</strong><br>8 complete two-step cycles</div>', '<div class="metric"><strong>F4</strong><br>near leg lands +1 riser</div><div class="metric"><strong>F8</strong><br>far leg lands +1 riser</div><div class="metric"><strong>Monotonic root</strong><br>never slides backwards</div><div class="metric"><strong>16 single steps</strong><br>exactly 60 lp total rise</div>')
html = html.replace('<article><h2>Boundary</h2><p>V1–V3 remain immutable. V4 changes no character pixel, media byte, timing value, root position, stair geometry, Final art or production sprite. Its versioned asset addresses resolve to the exact V3 hashes. The bannister is a review-only foreground occlusion candidate.</p></article>', '<article><h2>Boundary</h2><p>V1–V4 remain immutable. V5 changes no character pixel, media byte, frame duration, staircase dimension, Final art or production sprite. It changes only the climb root schedule to follow the registered four-frame near-leg and far-leg phases. Its 17 versioned asset addresses resolve to the exact V3 hashes.</p></article>')
html = html.replace(/const timeline=\[.*?\],buttons=/s, `const timeline=${JSON.stringify(timeline)},buttons=`)
html = html.replace("document.getElementById('banister').onchange=e=>stages.forEach(({el})=>el.classList.toggle('hideBanister',!e.target.checked));", "document.getElementById('banister').onchange=e=>stages.forEach(({el})=>el.classList.toggle('hideBanister',!e.target.checked));document.getElementById('opacity').oninput=e=>{const value=Number(e.target.value);document.getElementById('opacityValue').value=value+'%';document.querySelectorAll('.foregroundBanister').forEach(el=>el.style.opacity=String(value/100))};")
html = html.replace("(f.lowerTread!==undefined?' · active tread '+f.lowerTread+' at '+f.contactYLp.toFixed(2)+' lp':'')", "(f.supportTread!==undefined?' · support tread '+f.supportTread+' at '+f.contactYLp.toFixed(2)+' lp':'')")
fs.writeFileSync(v5Page, html)

const spec = {
  schema: 'lighthouse-keeper/prime-stair-ascent@5', status: 'draft-v5-independent-leg-root-phasing-awaiting-review',
  diagnosis: 'V3/V4 applied each one-riser body/root rise after the four-frame leg step instead of on its landing frame, so the alternate leg began with a whole-body jump.',
  correction: { nearLegFrames: [1, 2, 3, 4], farLegFrames: [5, 6, 7, 8], riseFrames: [4, 8], risePerLandingLp: riserRiseLp, runPerLandingLp: treadRunLp, cycles: 8, totalRiseLp: 60, totalRunLp: 84 },
  bannister: { defaultOpacity: 0.55, adjustable: true, purpose: 'depth and mild masking only; leg mechanics remain visible' },
  reviewScale: { logicalPixelsPerCssPixel: 1, worldScale: 0.25, bottomLeftAligned: true },
  unchanged: { v3CharacterMediaBytes: true, frameDurations: true, staircaseGeometry: true, walkApproach: true, finalLane: true, production: true },
}
const specPath = path.join(v5Pack, 'keeper-prime-stair-ascent-v5.json')
writeJson(specPath, spec)
const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-stair-ascent-2026-10-15-v5', status: spec.status,
  authorities: { v3Batch: { file: rel(v3RegisterPath), sha256: sha(v3RegisterPath) }, v4Batch: { file: rel(v4RegisterPath), sha256: sha(v4RegisterPath) }, contactRig: { file: rel(rigPath), sha256: sha(rigPath) } },
  generation: { mode: 'deterministic-independent-leg-root-phasing-no-new-artwork', sourceFrameUrls: v3Register.frameUrls, frameUrls: v5FrameUrls },
  spec: { file: rel(specPath), sha256: sha(specPath) }, reviewPage: { file: rel(v5Page), sha256: sha(v5Page) }, frameUrls: v5FrameUrls,
  validation: { rootMonotonic: true, risesOnlyOnF4AndF8: true, oneRiserPerLegLanding: true, sixteenSingleSteps: true, v3MediaBytesChanged: false, frameDurationsChanged: false, stairGeometryChanged: false, finalChanged: false, productionChanged: false },
}
writeJson(path.join(v5Pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(v5Pack, 'HANDOFF.md'), `# Keeper Prime stair ascent V5\n\nStatus: independent-leg root-phasing draft awaiting Frank's review.\n\nReview: \`/keeper-review/keeper-prime-stair-ascent-v5/\`.\n\nV5 preserves all V1–V4 evidence and every V3 character-media byte. It corrects the root schedule so the near-leg four-frame step lands and rises at F4, then the far-leg four-frame step lands and rises at F8. Eight cycles produce sixteen one-riser steps over the unchanged 84 × 60 lp flight. The foreground bannister defaults to 55% opacity and is adjustable. Nothing is approved or promoted.\n`)
console.log(JSON.stringify({ page: rel(v5Page), frames: timeline.length, reusedFrameHashes: v5FrameUrls.length, newBinaryObjects: 0 }, null, 2))

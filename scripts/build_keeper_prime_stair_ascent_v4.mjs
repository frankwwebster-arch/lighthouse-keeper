#!/usr/bin/env node
/** Build Stair Ascent V4 as an exact V3 motion presentation with foreground occlusion. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const v3Pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v3')
const v4Pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v4')
const v3Page = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v3/index.html')
const v4Public = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v4')
const v4Page = path.join(v4Public, 'index.html')
const v3RegisterPath = path.join(v3Pack, 'batch-register.json')
const archiveIndexPath = path.join(root, 'review-archive/index.json')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of [v3Page, v3RegisterPath, archiveIndexPath]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const v3Register = JSON.parse(fs.readFileSync(v3RegisterPath, 'utf8'))
const archiveIndex = JSON.parse(fs.readFileSync(archiveIndexPath, 'utf8'))
fs.mkdirSync(v4Pack, { recursive: true })
fs.mkdirSync(v4Public, { recursive: true })

const v4FrameUrls = v3Register.frameUrls.map((url) => url.replace('/keeper-prime-stair-ascent-v3/', '/keeper-prime-stair-ascent-v4/'))
const v4Assets = path.join(v4Public, 'assets')
fs.mkdirSync(v4Assets, { recursive: true })
for (let index = 0; index < v3Register.frameUrls.length; index += 1) {
  const sourceUrl = v3Register.frameUrls[index]
  const archiveEntry = archiveIndex.legacyPaths[sourceUrl]
  if (!archiveEntry) throw new Error(`archive does not resolve ${sourceUrl}`)
  const source = path.join(root, archiveEntry.object)
  if (sha(source) !== archiveEntry.sha256) throw new Error(`archive object changed for ${sourceUrl}`)
  fs.copyFileSync(source, path.join(v4Assets, path.basename(v4FrameUrls[index])))
}

const maskCss = `.foregroundBanister{position:absolute;inset:0;z-index:7;pointer-events:none}.hideBanister .foregroundBanister{display:none}.stringerPanel{position:absolute;inset:0;background:linear-gradient(180deg,#496675,#294653);clip-path:polygon(6.8% 22.2%,67% 77.7%,67% 97.7%,6.8% 42.7%);filter:drop-shadow(0 2px 0 #132a35)}.stringerCap,.handRail{position:absolute;left:34px;width:413px;transform:rotate(35.54deg);transform-origin:left center;border-radius:8px;background:#78909b;box-shadow:0 0 0 3px #1b303a}.stringerCap{top:105px;height:10px}.handRail{top:82px;height:12px}.baluster{position:absolute;width:8px;height:60px;background:#496675;border:2px solid #1b303a;border-radius:5px}.banisterNote{border-left:4px solid #ffbd72;background:#2b2419;padding:12px 14px}`
const balusters = [[78,116],[162,176],[246,236],[330,296]].map(([left, top]) => `<span class="baluster" style="left:${left}px;top:${top}px"></span>`).join('')
const maskMarkup = `<div class="foregroundBanister" aria-hidden="true"><div class="stringerPanel"></div><div class="stringerCap"></div><div class="handRail"></div>${balusters}</div>`

let html = fs.readFileSync(v3Page, 'utf8')
html = html.replaceAll('/keeper-review/keeper-prime-stair-ascent-v3/assets/', '/keeper-review/keeper-prime-stair-ascent-v4/assets/')
html = html.replace('<title>Keeper Prime stair ascent V3</title>', '<title>Keeper Prime stair ascent V4</title>')
html = html.replace('</style>', `${maskCss}</style>`)
html = html.replace('<a href="/keeper-review/keeper-prime-stair-ascent-v2/">← Preserve and compare rejected V2</a><h1>Keeper Prime stair ascent V3 · contact-locked alternation</h1><span class="status">New draft · nothing promoted</span><p>V3 replaces the false phase labels with a visible two-step cycle: near leg climbs, then far leg climbs. The lowest sole is locked to the actual tread top, never to the bottom of the stair block.</p>', '<a href="/keeper-review/keeper-prime-stair-ascent-v3/">← Preserve and compare unmasked V3</a><h1>Keeper Prime stair ascent V4 · foreground bannister mask</h1><span class="status">Presentation-only draft · nothing promoted</span><p>V4 keeps every V3 motion frame, root position and timing byte-for-byte, then places a closed foreground stair stringer and bannister above the feet and lower shins.</p>')
html = html.replace('<p class="rule"><strong>Judge two things:</strong> F1–F4 must be the near/front leg’s step; F5–F8 must be the far/rear leg’s step. No sole may flash below its active tread.</p>', '<p class="rule"><strong>Judge the illusion:</strong> does the foreground bannister make the ascent read naturally when the boot-to-tread geometry is hidden? Toggle the mask off to compare the exact underlying V3 motion.</p>')
html = html.replace('<label><input id="contacts" type="checkbox"> Show active tread contact</label>', '<label><input id="banister" type="checkbox" checked> Foreground bannister mask</label><label><input id="contacts" type="checkbox"> Show active tread contact</label>')
html = html.replace(/(<img class="walker"[^>]*>)/g, `$1${maskMarkup}`)
html = html.replace('<section class="metrics">', '<p class="banisterNote"><strong>What changed:</strong> one foreground presentation layer only. Character frames, timing, root motion, staircase dimensions and contact calculations are exact V3.</p><section class="metrics">')
html = html.replace('<article><h2>Boundary</h2><p>V1 and V2 remain immutable rejected evidence. V3 changes no approved walk pixels, runtime geometry, Final art or production sprites. Stair dismount is still a separate later gate.</p></article>', '<article><h2>Boundary</h2><p>V1–V3 remain immutable. V4 changes no character pixel, media byte, timing value, root position, stair geometry, Final art or production sprite. Its versioned asset addresses resolve to the exact V3 hashes. The bannister is a review-only foreground occlusion candidate.</p></article>')
html = html.replace("document.getElementById('contacts').onchange=e=>stages.forEach(({el})=>el.classList.toggle('showContact',e.target.checked));Promise.all", "document.getElementById('banister').onchange=e=>stages.forEach(({el})=>el.classList.toggle('hideBanister',!e.target.checked));document.getElementById('contacts').onchange=e=>stages.forEach(({el})=>el.classList.toggle('showContact',e.target.checked));Promise.all")
fs.writeFileSync(v4Page, html)

const spec = {
  schema: 'lighthouse-keeper/prime-stair-ascent@4',
  status: 'draft-v4-foreground-banister-occlusion-awaiting-review',
  basis: 'Exact immutable V3 motion and review timeline.',
  change: 'Foreground-only closed stringer band, handrail and balusters obscure boots/lower shins while leaving knees and body visible.',
  mask: { stage: [620, 480], stringerPolygonPercent: [[6.8,22.2],[67,77.7],[67,97.7],[6.8,42.7]], railAngleDeg: 35.54, zIndex: 7, defaultVisible: true },
  unchanged: { v3Page: true, mediaBytes: true, artwork: true, timing: true, rootMotion: true, stairGeometry: true, finalLane: true, production: true },
}
const specPath = path.join(v4Pack, 'keeper-prime-stair-ascent-v4.json')
writeJson(specPath, spec)
const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-stair-ascent-2026-10-15-v4', status: spec.status,
  authorities: { v3Batch: { file: rel(v3RegisterPath), sha256: sha(v3RegisterPath) }, v3Page: { file: rel(v3Page), sha256: sha(v3Page) } },
  presentation: { kind: 'foreground-css-occlusion', characterAssetsReusedByHash: true, sourceFrameUrls: v3Register.frameUrls, frameUrls: v4FrameUrls },
  spec: { file: rel(specPath), sha256: sha(specPath) }, reviewPage: { file: rel(v4Page), sha256: sha(v4Page) }, frameUrls: v4FrameUrls,
  validation: { v3PageChanged: false, characterPixelsChanged: false, timingChanged: false, rootMotionChanged: false, stairGeometryChanged: false, finalChanged: false, productionChanged: false },
}
writeJson(path.join(v4Pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(v4Pack, 'HANDOFF.md'), `# Keeper Prime stair ascent V4\n\nStatus: foreground-bannister presentation draft awaiting Frank's review.\n\nReview: \`/keeper-review/keeper-prime-stair-ascent-v4/\`.\n\nV4 reuses the exact immutable V3 animation and archived media. Its only change is a foreground closed stringer/bannister layer which masks boots and lower shins. The review toggle exposes the unmasked V3 underneath. Nothing is approved or promoted.\n`)
console.log(JSON.stringify({ page: rel(v4Page), reusedFrameHashes: v3Register.frameUrls.length, newBinaryObjects: 0 }, null, 2))

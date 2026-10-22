#!/usr/bin/env node
/** Build a reversible V18 review that removes the V16 stair-ascent beard flicker. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-stair-ascent-v18'
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-22-v18')
const frameDir = path.join(pack, 'drafts/frames')
const evidenceDir = path.join(pack, 'evidence/masks')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const v16Pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16')
const v16RegisterPath = path.join(v16Pack, 'batch-register.json')
const v16RigPath = path.join(v16Pack, 'stair-contact-rig-v16.json')
const sourceByRole = {
  'contact:left': path.join(v16Pack, 'drafts/frames/keeper_prime_stair_left-contact-clean_side-left_f01.png'),
  'contact:right': path.join(v16Pack, 'drafts/frames/keeper_prime_stair_right-contact-complete-toecap_side-left_f01.png'),
  'passing:left': path.join(v16Pack, 'drafts/frames/keeper_prime_stair_left-foot-passing-compact_side-left_f01.png'),
  'passing:right': path.join(v16Pack, 'drafts/frames/keeper_prime_stair_right-foot-passing-balanced_side-left_f01.png'),
}
const authorityPath = sourceByRole['passing:left']
const shaBytes = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
const sha = (file) => shaBytes(fs.readFileSync(file))
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

for (const file of [v16RegisterPath, v16RigPath, ...Object.values(sourceByRole)]) {
  if (!fs.existsSync(file)) throw new Error(`Missing authority: ${rel(file)}`)
}

const v16Register = JSON.parse(fs.readFileSync(v16RegisterPath, 'utf8'))
const v16Rig = JSON.parse(fs.readFileSync(v16RigPath, 'utf8'))
const authority = PNG.sync.read(fs.readFileSync(authorityPath))
const WIDTH = authority.width
const HEIGHT = authority.height
if (WIDTH !== 256 || HEIGHT !== 320) throw new Error(`Unexpected authority cell ${WIDTH}x${HEIGHT}`)

function beardCore(image) {
  const eligible = new Uint8Array(WIDTH * HEIGHT)
  const visited = new Uint8Array(WIDTH * HEIGHT)
  for (let y = 85; y < 165; y += 1) {
    for (let x = 55; x < 145; x += 1) {
      const offset = (y * WIDTH + x) * 4
      const [red, green, blue, alpha] = image.data.subarray(offset, offset + 4)
      if (alpha > 20 && red > 185 && green > 165 && blue > 140 && Math.max(red, green, blue) - Math.min(red, green, blue) < 100) eligible[y * WIDTH + x] = 1
    }
  }
  let largest = []
  for (let start = 0; start < eligible.length; start += 1) {
    if (!eligible[start] || visited[start]) continue
    const queue = [start]
    const component = []
    visited[start] = 1
    while (queue.length) {
      const pixel = queue.pop()
      component.push(pixel)
      const y = Math.floor(pixel / WIDTH)
      const x = pixel - y * WIDTH
      for (let dy = -1; dy <= 1; dy += 1) {
        for (let dx = -1; dx <= 1; dx += 1) {
          const nextX = x + dx
          const nextY = y + dy
          if (nextX < 0 || nextX >= WIDTH || nextY < 0 || nextY >= HEIGHT) continue
          const next = nextY * WIDTH + nextX
          if (eligible[next] && !visited[next]) {
            visited[next] = 1
            queue.push(next)
          }
        }
      }
    }
    if (component.length > largest.length) largest = component
  }
  if (largest.length < 1500) throw new Error(`Beard core unexpectedly small: ${largest.length}`)
  const mask = new Uint8Array(WIDTH * HEIGHT)
  for (const pixel of largest) mask[pixel] = 1
  return mask
}

function dilate(mask, radius) {
  const output = new Uint8Array(mask.length)
  for (let y = 0; y < HEIGHT; y += 1) {
    for (let x = 0; x < WIDTH; x += 1) {
      if (!mask[y * WIDTH + x]) continue
      for (let dy = -radius; dy <= radius; dy += 1) {
        for (let dx = -radius; dx <= radius; dx += 1) {
          if (dx * dx + dy * dy > radius * radius) continue
          const nextX = x + dx
          const nextY = y + dy
          if (nextX >= 0 && nextX < WIDTH && nextY >= 0 && nextY < HEIGHT) output[nextY * WIDTH + nextX] = 1
        }
      }
    }
  }
  return output
}

function edgeAlpha(image) {
  let count = 0
  for (let x = 0; x < WIDTH; x += 1) for (const y of [0, HEIGHT - 1]) if (image.data[(y * WIDTH + x) * 4 + 3]) count += 1
  for (let y = 1; y < HEIGHT - 1; y += 1) for (const x of [0, WIDTH - 1]) if (image.data[(y * WIDTH + x) * 4 + 3]) count += 1
  return count
}

function writeMask(file, mask) {
  const image = new PNG({ width: WIDTH, height: HEIGHT })
  for (let pixel = 0; pixel < mask.length; pixel += 1) {
    if (!mask[pixel]) continue
    image.data[pixel * 4] = 255
    image.data[pixel * 4 + 1] = 255
    image.data[pixel * 4 + 2] = 255
    image.data[pixel * 4 + 3] = 255
  }
  fs.writeFileSync(file, PNG.sync.write(image))
}

function beardBounds(image) {
  const mask = beardCore(image)
  let minX = WIDTH
  let minY = HEIGHT
  let maxX = -1
  let maxY = -1
  let pixels = 0
  for (let pixel = 0; pixel < mask.length; pixel += 1) {
    if (!mask[pixel]) continue
    const y = Math.floor(pixel / WIDTH)
    const x = pixel - y * WIDTH
    minX = Math.min(minX, x)
    minY = Math.min(minY, y)
    maxX = Math.max(maxX, x)
    maxY = Math.max(maxY, y)
    pixels += 1
  }
  return { pixels, boundsInclusive: [minX, minY, maxX, maxY] }
}

fs.mkdirSync(frameDir, { recursive: true })
fs.mkdirSync(evidenceDir, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const authorityMask = dilate(beardCore(authority), 6)
const draftByRole = {}
const corrections = {}
for (const role of ['contact:left', 'contact:right']) {
  const source = PNG.sync.read(fs.readFileSync(sourceByRole[role]))
  const sourceMask = dilate(beardCore(source), 6)
  const editMask = new Uint8Array(WIDTH * HEIGHT)
  const draft = PNG.sync.read(fs.readFileSync(sourceByRole[role]))
  let changedPixels = 0
  for (let pixel = 0; pixel < editMask.length; pixel += 1) {
    const y = Math.floor(pixel / WIDTH)
    if (y < 112 || y > 164 || (!sourceMask[pixel] && !authorityMask[pixel])) continue
    editMask[pixel] = 1
    const offset = pixel * 4
    if ([0, 1, 2, 3].some((channel) => source.data[offset + channel] !== authority.data[offset + channel])) changedPixels += 1
    authority.data.copy(draft.data, offset, offset, offset + 4)
  }
  const slug = role.replace(':', '-')
  const draftPath = path.join(frameDir, `keeper_prime_stair_${slug}-beard-normalised_side-left_f01.png`)
  const maskPath = path.join(evidenceDir, `${slug}-beard-normalisation-mask.png`)
  fs.writeFileSync(draftPath, PNG.sync.write(draft))
  writeMask(maskPath, editMask)
  if (edgeAlpha(draft)) throw new Error(`${role} touches a shared cell edge`)
  draftByRole[role] = draftPath
  corrections[role] = {
    original: { file: rel(sourceByRole[role]), sha256: sha(sourceByRole[role]) },
    draft: { file: rel(draftPath), sha256: sha(draftPath) },
    mask: { file: rel(maskPath), sha256: sha(maskPath), bandInclusive: [112, 164], dilationRadiusPx: 6 },
    changedPixels,
    originalBeard: beardBounds(source),
    correctedBeard: beardBounds(draft),
  }
}
draftByRole['passing:left'] = sourceByRole['passing:left']
draftByRole['passing:right'] = sourceByRole['passing:right']

const authorityBounds = beardBounds(authority)
for (const role of Object.keys(draftByRole)) {
  const image = PNG.sync.read(fs.readFileSync(draftByRole[role]))
  const bounds = beardBounds(image)
  if (JSON.stringify(bounds) !== JSON.stringify(authorityBounds)) throw new Error(`${role} beard does not match the approved passing authority`)
  if (edgeAlpha(image)) throw new Error(`${role} touches a shared cell edge`)
}

const candidateUrls = {}
const assets = []
for (const [role, source] of Object.entries(draftByRole)) {
  const digest = sha(source)
  const filename = `${role.replace(':', '-')}-${digest.slice(0, 16)}.png`
  const target = path.join(assetsDir, filename)
  fs.copyFileSync(source, target)
  const url = `/keeper-review/${set}/assets/${filename}`
  candidateUrls[role] = url
  assets.push({ role, original: rel(sourceByRole[role]), originalSha256: sha(sourceByRole[role]), draft: rel(source), draftSha256: digest, url, changed: source !== sourceByRole[role] })
}

const originalUrls = {}
for (const entry of v16Register.assets) originalUrls[entry.role] = entry.url
const correctedTimeline = v16Rig.timeline.map((frame) => ({ ...frame, src: candidateUrls[`${frame.kind}:${frame.movingLeg}`] }))
const originalTimeline = v16Rig.timeline.map((frame) => ({ ...frame }))
const rigPath = path.join(pack, 'stair-contact-rig-v18.json')
writeJson(rigPath, {
  schema: 'lighthouse-keeper/stair-contact-rig@18',
  status: 'beard-continuity-correction-awaiting-review',
  direction: v16Rig.direction,
  cell: v16Rig.cell,
  density: v16Rig.density,
  geometry: v16Rig.geometry,
  uniqueDrawings: 4,
  timeline: correctedTimeline,
  endpoint: v16Rig.endpoint,
  beardAuthority: { role: 'passing:left', file: rel(authorityPath), sha256: sha(authorityPath), ...authorityBounds },
  contract: [
    'V16 remains immutable and is shown beside this version.',
    'All four unique drawings use the exact approved passing-pose beard core bounds and pixel count.',
    'Only the two contact drawings change, inside their recorded beard masks and y=112..164 inclusive.',
    'Every pixel above y=112 and below y=164 remains byte-identical to V16.',
    'The 27-frame timeline, timing, root positions, stair contacts, body poses, boots, palette and cell geometry remain exact.',
    'This is a reversible review draft; runtime and production remain unchanged pending approval.',
  ],
})

const geometry = v16Rig.geometry
const stairs = Array.from({ length: geometry.risers }, (_, index) => {
  const n = index + 1
  return `<span class="step" style="left:${(geometry.stairBaseRightLp - n * geometry.treadRunLp) * 4}px;bottom:${geometry.floorTopLp * 4}px;width:${geometry.treadRunLp * 4}px;height:${n * geometry.riserRiseLp * 4}px"></span>`
}).join('')
const stage = (id, title) => `<section><h2>${title}</h2><div class="stageScroll"><div class="stage"><div class="stairs">${stairs}</div><div class="floor"></div><div class="landing"></div><img id="${id}" class="walker" alt="${title}"></div></div></section>`
const cards = ['contact:left', 'passing:right', 'contact:right', 'passing:left'].map((role) => `<article class="card"><h3>${role.replace(':', ' · ')}</h3><div class="pair"><figure><div class="portrait"><img src="${originalUrls[role]}" alt="V16 ${role}"></div><figcaption>Approved V16</figcaption></figure><figure><div class="portrait"><img src="${candidateUrls[role]}" alt="V18 ${role}"></div><figcaption>${role.startsWith('contact') ? 'Corrected V18' : 'Exact unchanged authority'}</figcaption></figure></div></article>`).join('')
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper stair ascent V18 · beard continuity</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.48 system-ui,sans-serif}header,main{max-width:1420px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:14px;margin:18px 0}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.views{display:grid;grid-template-columns:1fr 1fr;gap:16px}.stageScroll{overflow:auto}.stage{position:relative;overflow:hidden;background:#122b37;border:1px solid #496878;width:620px;height:480px}.step{position:absolute;background:#526675;border-top:3px solid #d0dee6;border-left:1px solid #263d49}.floor{position:absolute;left:${geometry.stairBaseRightLp * 4}px;right:0;bottom:0;height:${geometry.floorTopLp * 4}px;background:#526675;border-top:3px solid #d0dee6}.landing{position:absolute;left:0;bottom:${(geometry.floorTopLp + geometry.flightRiseLp) * 4}px;width:${(geometry.stairBaseRightLp - geometry.flightRunLp) * 4}px;height:3px;background:#d0dee6}.walker{position:absolute;width:128px;height:160px;object-fit:contain;z-index:4;image-rendering:auto}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.card{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:14px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pair figure{margin:0;text-align:center}.portrait{height:250px;overflow:hidden;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/16px 16px;position:relative}.portrait img{position:absolute;width:384px;height:480px;max-width:none;left:50%;top:-68px;transform:translateX(-50%);image-rendering:auto}.pair figcaption{color:#bdd3dd;margin-top:5px}.note{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:15px;margin:18px 0}@media(max-width:900px){.views,.grid{grid-template-columns:1fr}.stage{transform-origin:left top}.pair{grid-template-columns:1fr 1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-stair-ascent-v16/">← Immutable approved V16</a><h1>Prime Keeper stair ascent V18 · beard continuity correction</h1><span class="status">Reversible correction draft · nothing promoted</span><p><strong>V16 alternates between different lower-beard silhouettes. V18 gives all four drawings the exact same approved passing-pose beard construction.</strong></p></header><main><p class="rule"><strong>Judge one thing:</strong> the bottom and outer edge of the beard should remain visually locked while his legs and arms alternate. The body action, stair contacts, pace, colours and registration must feel identical to V16.</p><div class="controls"><button id="play" disabled>Play both</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><label>Frame speed <input id="speed" type="range" min="70" max="260" step="5" value="110"> <output id="speedValue">110 ms</output></label><span id="loading" class="readout">Preloading and decoding all unique images…</span><span id="readout" class="readout"></span></div><div class="views">${stage('before', 'Approved V16 · beard flicker')}${stage('after', 'V18 candidate · locked beard')}</div><h2>All four unique drawings · magnified head check</h2><div class="grid">${cards}</div><article class="note"><h2>Reversible boundary</h2><p>The approved V16 images are untouched. V18 changes only the two contact drawings, within recorded masks around the lower beard. The two passing drawings are byte-identical authorities. Rejecting this amendment means discarding the V18 directory alone; runtime and production are unchanged until explicit approval.</p></article></main><script>
const original=${JSON.stringify(originalTimeline)},corrected=${JSON.stringify(correctedTimeline)},buttons=[...document.querySelectorAll('button')];let index=0,timer=null,hold=110;const unique=[...new Set([...original.map(frame=>frame.src),...corrected.map(frame=>frame.src)])];function render(){const a=original[index],b=corrected[index];for(const [image,frame] of [[before,a],[after,b]]){image.src=frame.src;image.style.left=((frame.xLp-16)*4)+'px';image.style.bottom=(frame.bottomLp*4)+'px'}readout.textContent='F'+(index+1)+'/27 · '+b.label+(index===26?' · TOP REACHED':'')}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){if(index>=corrected.length-1)return stop();index++;render();timer=setTimeout(tick,index===corrected.length-1?corrected[index].durationMs:hold)}function playBoth(){stop();if(index>=corrected.length-1)index=0;render();timer=setTimeout(tick,hold)}function preload(src){return new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{const decoded=image.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};image.onerror=()=>reject(new Error(src));image.src=src})}play.onclick=playBoth;pause.onclick=stop;prev.onclick=()=>{stop();index=Math.max(0,index-1);render()};next.onclick=()=>{stop();index=Math.min(corrected.length-1,index+1);render()};restart.onclick=()=>{stop();index=0;render();playBoth()};speed.oninput=event=>{hold=Number(event.target.value);speedValue.value=hold+' ms';if(timer)playBoth()};Promise.all(unique.map(preload)).then(()=>{buttons.forEach(button=>button.disabled=false);loading.textContent='All unique images decoded';render();playBoth()}).catch(error=>{loading.textContent='An image failed to decode; playback remains locked. '+error.message})
</script></body></html>`
const pagePath = path.join(publicDir, 'index.html')
fs.writeFileSync(pagePath, html)

const specPath = path.join(pack, 'keeper-prime-stair-ascent-v18.json')
writeJson(specPath, {
  schema: 'lighthouse-keeper/prime-stair-ascent@18',
  status: 'beard-continuity-correction-awaiting-review',
  scope: 'Correct only the contact-pose lower beards while retaining the exact approved V16 stair choreography.',
  promoted: false,
  immutableAuthority: rel(v16RegisterPath),
  unchanged: { timeline: true, timing: true, rootPositions: true, stairContacts: true, bodyPosesOutsideMasks: true, palette: true, cellGeometry: true, runtime: true, production: true },
})
const registerPath = path.join(pack, 'batch-register.json')
const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-stair-ascent-2026-10-22-v18',
  status: 'beard-continuity-correction-awaiting-review',
  authority: { file: rel(v16RegisterPath), sha256: sha(v16RegisterPath) },
  generation: { mode: 'built-in-image-edit-study-rejected-for-global-drift; final candidate uses deterministic masked transplant from exact approved passing-left beard authority' },
  beardAuthority: { file: rel(authorityPath), sha256: sha(authorityPath), ...authorityBounds },
  corrections,
  assets,
  rig: { file: rel(rigPath), sha256: sha(rigPath) },
  spec: { file: rel(specPath), sha256: sha(specPath) },
  reviewPage: { file: rel(pagePath), sha256: sha(pagePath) },
  frameUrls: Object.values(candidateUrls),
  comparisonUrls: Object.values(originalUrls),
  validation: {
    uniqueDrawings: 4,
    timelineFrames: correctedTimeline.length,
    correctedContactDrawings: 2,
    unchangedPassingDrawings: 2,
    commonBeard: authorityBounds,
    transparentCellEdges: true,
    immutableV16: true,
    runtimeChanged: false,
    productionChanged: false,
  },
}
writeJson(registerPath, register)
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), `# Prime Keeper stair ascent V18\n\nStatus: reversible beard-continuity correction awaiting Frank's review.\n\nReview: \`/keeper-review/${set}/\`.\n\nV16 is immutable. V18 deterministically replaces only the lower-beard mask in its two contact drawings with pixels from the exact approved passing-left beard authority. The four resulting beard cores share ${authorityBounds.pixels} pixels and bounds ${authorityBounds.boundsInclusive.join(', ')}. The 27-frame stair timeline, timing, positions, contacts, remaining body art, palette and cell geometry are unchanged. Runtime and production are unchanged pending explicit approval.\n`)
fs.writeFileSync(path.join(pack, 'PROMPT_LOG.md'), `# Prompt log\n\nA built-in precise-object-edit study was requested using V16 LEFT contact as the edit target and V16 LEFT passing as the beard authority. The study was rejected because it changed global scale, line weight and non-beard pixels. It is not included in the candidate.\n\nThe reviewable result is deterministic: exact approved passing-left beard pixels are transplanted only through the recorded union mask on the two V16 contact drawings.\n`)
console.log(JSON.stringify({ page: rel(pagePath), pack: rel(pack), changedPixels: Object.fromEntries(Object.entries(corrections).map(([role, value]) => [role, value.changedPixels])), beard: authorityBounds }, null, 2))

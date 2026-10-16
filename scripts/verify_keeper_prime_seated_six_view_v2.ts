import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const pack = path.join(root, 'art/drafts/keeper-prime-seated-six-view-2026-10-17-v2')
const proofFile = path.join(pack, 'keeper-prime-seated-six-view-v2.json')
const registerFile = path.join(pack, 'batch-register.json')
const pageFile = path.join(root, 'public/keeper-review/keeper-prime-seated-six-view-v2/index.html')
const read = (file:string) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file:string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message:string):never => { throw new Error(`[keeper-prime-seated-six-view-v2] ${message}`) }
for (const file of [proofFile, registerFile, pageFile]) if (!fs.existsSync(file)) fail(`missing ${path.relative(root, file)}`)
const proof = read(proofFile), register = read(registerFile)
if (proof.schema !== 'lighthouse-keeper/seated-contact-proof@1' || proof.status !== 'review-draft-no-promotion') fail('proof identity/status changed')
if (proof.chair.surfaceTopLp !== 29 || proof.chair.surfaceTopPixel !== 232 || proof.chair.heightAboveFloorLp !== 11 || proof.chair.renderLayer !== 'behind-keeper') fail('chair contact geometry changed')
if (!proof.loading.firstViewRenderedBeforePreload || !proof.loading.primaryViewsGateControls || proof.loading.auxiliaryComparisonsGateControls) fail('resilient loading contract changed')
if (proof.views.length !== 6) fail('expected six views')
for (const view of proof.views) {
  const file = path.join(root, view.source)
  if (!fs.existsSync(file) || sha(file) !== view.sha256) fail(`${view.id} source/hash changed`)
  const png = PNG.sync.read(fs.readFileSync(file))
  const [x,y] = view.contact.pixel
  if (x !== 128 || y !== 232 || view.contact.logical.join(',') !== '16,29') fail(`${view.id} contact coordinate changed`)
  if (png.data[(y * png.width + x) * 4 + 3] < 192) fail(`${view.id} pelvis is not opaque on chair top`)
  for (const row of [231,232,233]) {
    let count = 0
    for (let column = 0; column < png.width; column++) if (png.data[(row * png.width + column) * 4 + 3] >= 192) count++
    if (count < 96) fail(`${view.id} has a gap/sparse pelvis at chair plane row ${row}`)
  }
}
for (const [key,value] of Object.entries(proof.boundaries)) if (value !== false) fail(`${key} boundary changed`)
if (register.contactProof.sha256 !== sha(proofFile) || register.page.sha256 !== sha(pageFile)) fail('register hashes stale')
const html = fs.readFileSync(pageFile, 'utf8')
for (const phrase of ['render();Promise.allSettled', 'chair top + pelvis contact · y 29 lp', 'All six physical contacts', 'first view is visible immediately', 'top:72.5%', 'z-index:1']) if (!html.includes(phrase)) fail(`page missing ${phrase}`)
if (html.indexOf('render();Promise.allSettled') > html.indexOf('buttons.forEach(x=>x.disabled=false)')) fail('controls can unlock before first render/load gate')
console.log(JSON.stringify({ ok:true, views:6, seatTopLp:29, seatTopPixel:232, seatHeightLp:11, firstViewImmediate:true, sourcePixelsChanged:false }, null, 2))

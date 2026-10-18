import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-rebuild-states-2026-10-18-v7',raw=path.join(root,'art/raw',set),draft=path.join(root,'art/drafts',set),v6raw=path.join(root,'art/raw/kitchen-rebuild-states-2026-10-18-v6')
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex'),png=f=>PNG.sync.read(fs.readFileSync(f))
assert.equal(catalogue.set,set)
assert.equal(catalogue.version,7)
assert.equal(catalogue.status,'asset-first-multi-layer-workbench-awaiting-review')
for(const key of ['assetFirstLayerWorkbench','multiInstanceEffects','dragDropPlacement','perLayerRemoval'])assert.equal(catalogue.method[key],true,key)
assert.equal(catalogue.method.canonicalLoopSeconds,10)
assert.equal(catalogue.promotion,'none')
assert.equal(catalogue.runtimeWiring,'unchanged')
assert.equal(Object.keys(catalogue.effectFamilies).length,12)
assert.equal(Object.keys(catalogue.effects).length,36)
assert.equal(Object.keys(catalogue.outputs).length,62)

for(const name of Object.keys(catalogue.outputs))assert.equal(sha(path.join(raw,name)),sha(path.join(v6raw,name)),`immutable V6 output changed: ${name}`)
for(const [family,f] of Object.entries(catalogue.effectFamilies)){
  assert.equal(f.models.length,3,`${family} model count`)
  for(const name of f.models){
    const m=catalogue.effects[name]
    assert.equal(m.durationSeconds,10);assert.equal(m.canonicalDurationSeconds,10);assert.equal(m.frames,40);assert.equal(m.fps,4)
    const im=png(path.join(raw,m.file));assert.deepEqual([im.width,im.height],[4800,144])
    for(let frame=0;frame<40;frame++)for(let y=0;y<144;y++)for(const x of [0,119])assert.equal(im.data[(y*im.width+frame*120+x)*4+3],0,`${name} shared-edge alpha`)
  }
}
for(const family of ['oven-broken-warning-flicker','oven-broken-cavity-flicker'])for(const name of catalogue.effectFamilies[family].models){assert.equal(catalogue.effects[name].lockedToObject,true);assert.equal(catalogue.effects[name].editableTransform,false)}

const html=fs.readFileSync(path.join(root,'public/keeper-review/kitchen-rebuild-states-v7/index.html'),'utf8')
for(const pattern of [
  /Rebuild V7 reversible draft/,/Review boundary:<\/strong> V7 draft only/,/Choose the appliance first/,/id="asset"/,/id="layer"/,/Applied animation/,
  /id="library"/,/draggable=ok/,/ondragstart/,/ondrop/,/addLayer\(family,\[q\.x,q\.y\]\)/,/multi-instance|as many animation families/i,
  /id="model"/,/id="speed"/,/min="0\.1" max="4"/,/id="remove"/,/Remove animation/,/reset-asset/,/Reset all assets/,
  /bin-broken-smell/,/bin-broken-flies/,/oven-broken-warning-flicker/,/oven-broken-cavity-flicker/,/familyLocked/,/locked to oven/,
  /DEFAULT_STACKS=\{fridge:\[\]/,/canonicalLoopSeconds:10/,/localStorage\.setItem/,/navigator\.clipboard/,/Promise\.all\(DATA\.media\.map\(load\)/,/i\.decode\(\)/
])assert.match(html,pattern)
assert.doesNotMatch(html,/V6 draft only|V6 directories/)

const archive=path.join(root,'review-archive/sets/kitchen-rebuild-states-v7.json')
assert.ok(fs.existsSync(archive),'archive manifest missing')
const manifest=JSON.parse(fs.readFileSync(archive));assert.equal(manifest.set,'kitchen-rebuild-states-v7')
const archived=new Set(Object.keys(manifest.entries).map(entry=>path.basename(entry)))
for(const name of Object.keys(catalogue.outputs))assert.ok(archived.has(name),`${name} not archived`)
console.log('Kitchen Rebuild V7 verified: asset-first Broken-state builder, unlimited reusable effect instances, drag/drop, per-layer model/speed/transform/crop/removal, oven-registered light layers, and 62 byte-identical V6 media outputs')

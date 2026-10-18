import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-rebuild-states-2026-10-18-v8',raw=path.join(root,'art/raw',set),draft=path.join(root,'art/drafts',set),v7raw=path.join(root,'art/raw/kitchen-rebuild-states-2026-10-18-v7')
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex'),png=f=>PNG.sync.read(fs.readFileSync(f))
assert.equal(catalogue.set,set);assert.equal(catalogue.version,8);assert.equal(catalogue.status,'coherent-broken-oven-state-swap-awaiting-review')
assert.equal(catalogue.method.assetFirstLayerWorkbench,true);assert.equal(catalogue.method.fullStateFlickerSwap,true);assert.equal(catalogue.method.brokenOvenDerivedFromOn,true)
assert.equal(catalogue.promotion,'none');assert.equal(catalogue.runtimeWiring,'unchanged')
assert.equal(Object.keys(catalogue.effectFamilies).length,12);assert.equal(Object.keys(catalogue.effects).length,36);assert.equal(Object.keys(catalogue.outputs).length,62)

const changed=new Set(['oven-broken.png','fx-oven-broken-cavity-flicker--classic-f40.png','fx-oven-broken-cavity-flicker--slow-f40.png','fx-oven-broken-cavity-flicker--erratic-f40.png'])
for(const name of Object.keys(catalogue.outputs))if(!changed.has(name))assert.equal(sha(path.join(raw,name)),sha(path.join(v7raw,name)),`immutable V7 output changed: ${name}`)
assert.notEqual(sha(path.join(raw,'oven-broken.png')),sha(path.join(v7raw,'oven-broken.png')))
const oven=png(path.join(raw,'oven-broken.png')),on=png(path.join(raw,'oven-on.png'))
assert.deepEqual([oven.width,oven.height],[84,120])
// Hob, shared cabinet body and fascia remain byte-identical to On; only the
// indicator, cavity contents and centred door projection may change.
for(let y=0;y<56;y++)for(let x=0;x<84;x++){const i=(y*84+x)*4;assert.deepEqual([...oven.data.subarray(i,i+4)],[...on.data.subarray(i,i+4)],`On-derived oven changed above fascia at ${x},${y}`)}
// Straight-toward-camera projection keeps every source x coordinate: the
// deterministic builder performs vertical-only nearest-neighbour foreshortening.
const builder=fs.readFileSync(path.join(root,'scripts/build_kitchen_rebuild_states_v8.py'),'utf8')
for(const pattern of [/crop\(\(0, 67, 72, 107\)\)\.resize\(\(72, 37\)/,/alpha_composite\(door, \(0, 70\)\)/,/three-pixel horizontal cavity reveal/,/burnt_contents\(on\)/])assert.match(builder,pattern)
assert.match(builder,/V7_RAW \/ "oven-standard\.png"/)
assert.doesNotMatch(builder,/old_broken|V7_RAW \/ "oven-broken\.png"/)

for(const name of catalogue.effectFamilies['oven-broken-cavity-flicker'].models){const m=catalogue.effects[name],im=png(path.join(raw,m.file));assert.equal(m.fullStateSwap,true);assert.equal(m.lockedToObject,true);assert.deepEqual(m.origin,[334,96]);assert.deepEqual(m.size,[88,124]);assert.deepEqual(m.cellPixels,[88,124]);assert.deepEqual([im.width,im.height],[3520,124]);for(let frame=0;frame<40;frame++){for(let x=0;x<88;x++)for(const y of [0,1,122,123])assert.equal(im.data[(y*im.width+frame*88+x)*4+3],0,`${name} horizontal gutter`);for(let y=0;y<124;y++)for(const x of [0,1,86,87])assert.equal(im.data[(y*im.width+frame*88+x)*4+3],0,`${name} shared-edge gutter`)}}
for(const [family,f] of Object.entries(catalogue.effectFamilies))for(const name of f.models){const m=catalogue.effects[name];assert.equal(m.frames,40);assert.equal(m.fps,4);assert.equal(m.canonicalDurationSeconds,10)}

const html=fs.readFileSync(path.join(root,'public/keeper-review/kitchen-rebuild-states-v8/index.html'),'utf8')
for(const pattern of [/Rebuild V8 reversible draft/,/Review boundary:<\/strong> V8 draft only/,/complete, exactly registered Broken oven/,/does not place a separate cavity graphic/,/function layerOrder/,/oven-broken-cavity-flicker'\?-20/,/id="asset"/,/id="library"/,/id="remove"/,/ondragstart/,/ondrop/,/localStorage\.setItem/,/Promise\.all\(DATA\.media\.map\(load\)/])assert.match(html,pattern)
assert.doesNotMatch(html,/V7 draft only|V7 directories/)
const archive=path.join(root,'review-archive/sets/kitchen-rebuild-states-v8.json');assert.ok(fs.existsSync(archive),'archive manifest missing')
const manifest=JSON.parse(fs.readFileSync(archive));assert.equal(manifest.set,'kitchen-rebuild-states-v8');const archived=new Set(Object.keys(manifest.entries).map(entry=>path.basename(entry)));for(const name of Object.keys(catalogue.outputs))assert.ok(archived.has(name),`${name} not archived`)
console.log('Kitchen Rebuild V8 verified: broken oven derives from exact On model, door foreshortens vertically toward camera with no side skew, full-state dark/lit swaps preserve one silhouette, and every 10-second strip retains isolated gutters')

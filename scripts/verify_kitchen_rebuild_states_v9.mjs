import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-rebuild-states-2026-10-19-v9',raw=path.join(root,'art/raw',set),draft=path.join(root,'art/drafts',set),v8raw=path.join(root,'art/raw/kitchen-rebuild-states-2026-10-18-v8')
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex'),png=f=>PNG.sync.read(fs.readFileSync(f))
assert.equal(catalogue.set,set);assert.equal(catalogue.version,9);assert.equal(catalogue.status,'irregular-failing-bulb-timing-awaiting-review')
assert.equal(catalogue.method.assetFirstLayerWorkbench,true);assert.equal(catalogue.method.fullStateFlickerSwap,true);assert.equal(catalogue.method.irregularFaultTiming,true);assert.equal(catalogue.method.noShortCadenceRepeat,true)
assert.equal(catalogue.promotion,'none');assert.equal(catalogue.runtimeWiring,'unchanged');assert.equal(Object.keys(catalogue.outputs).length,62)

const changed=new Set(['fx-oven-broken-cavity-flicker--classic-f40.png','fx-oven-broken-cavity-flicker--slow-f40.png','fx-oven-broken-cavity-flicker--erratic-f40.png'])
for(const name of Object.keys(catalogue.outputs))if(!changed.has(name))assert.equal(sha(path.join(raw,name)),sha(path.join(v8raw,name)),`accepted V8 output changed: ${name}`)
assert.equal(sha(path.join(raw,'oven-broken.png')),sha(path.join(v8raw,'oven-broken.png')),'accepted Broken oven geometry changed')

const expected={
 'oven-broken-cavity-flicker--classic':{label:'random',frames:[2,6,7,13,19,22,23,24,31,35,38]},
 'oven-broken-cavity-flicker--slow':{label:'sputtering',frames:[1,4,10,11,16,21,22,29,33,34,35]},
 'oven-broken-cavity-flicker--erratic':{label:'near-blow',frames:[3,9,15,16,24,29,31,33,34,36,38]},
}
const parent=png(path.join(v8raw,'fx-oven-broken-cavity-flicker--classic-f40.png'))
for(const [name,want] of Object.entries(expected)){
 const m=catalogue.effects[name],im=png(path.join(raw,m.file));assert.equal(m.model,want.label);assert.deepEqual(m.timingFrames,want.frames);assert.equal(m.timingGrammar,'irregular-dark-holds-isolated-flashes-and-short-stutters');assert.equal(m.fullStateSwap,true);assert.equal(m.lockedToObject,true);assert.deepEqual(m.origin,[334,96]);assert.deepEqual(m.size,[88,124]);assert.deepEqual(m.cellPixels,[88,124]);assert.deepEqual([im.width,im.height],[3520,124])
 const active=new Set(want.frames),bits=[]
 for(let frame=0;frame<40;frame++){
  let opaque=false
  for(let y=0;y<124;y++)for(let x=0;x<88;x++){const i=(y*im.width+frame*88+x)*4,a=im.data[i+3];if(a)opaque=true;if(x<2||x>85||y<2||y>121)assert.equal(a,0,`${name} frame ${frame} gutter`);if(active.has(frame)){const p=(y*parent.width+4*88+x)*4;assert.deepEqual([...im.data.subarray(i,i+4)],[...parent.data.subarray(p,p+4)],`${name} frame ${frame} changed accepted V8 lit pixels`)}}
  assert.equal(opaque,active.has(frame),`${name} frame ${frame} on/off timing`);bits.push(opaque)
 }
 for(let period=1;period<=10;period++)assert.equal(bits.every((value,index)=>value===bits[index%period]),false,`${name} repeats a short ${period}-frame cadence`)
 const runs=[];let run=0;for(const value of bits){if(value)run++;else if(run){runs.push(run);run=0}}if(run)runs.push(run);assert.ok(runs.includes(1));assert.ok(runs.some(n=>n>=2&&n<=3));assert.ok(Math.max(...runs)<=3)
}
for(const family of Object.values(catalogue.effectFamilies))for(const name of family.models){const m=catalogue.effects[name];assert.equal(m.frames,40);assert.equal(m.fps,4);assert.equal(m.canonicalDurationSeconds,10)}

const html=fs.readFileSync(path.join(root,'public/keeper-review/kitchen-rebuild-states-v9/index.html'),'utf8')
for(const pattern of [/Rebuild V9 reversible draft/,/Review boundary:<\/strong> V9 draft only/,/uneven dark holds, isolated flashes and short electrical stutters/,/never a regular pulse/,/kitchen-rebuild-v9-asset-layer-config/,/kitchen-rebuild-v9-asset-layers\.json/,/function layerOrder/,/id="asset"/,/id="remove"/,/Promise\.all\(DATA\.media\.map\(load\)/])assert.match(html,pattern)
assert.doesNotMatch(html,/V8 draft only|kitchen-rebuild-v8-asset-layer-config/)
const archive=path.join(root,'review-archive/sets/kitchen-rebuild-states-v9.json');assert.ok(fs.existsSync(archive),'archive manifest missing')
const manifest=JSON.parse(fs.readFileSync(archive));assert.equal(manifest.set,'kitchen-rebuild-states-v9');const archived=new Set(Object.keys(manifest.entries).map(entry=>path.basename(entry)));for(const name of Object.keys(catalogue.outputs))assert.ok(archived.has(name),`${name} not archived`)
console.log('Kitchen Rebuild V9 verified: accepted V8 oven geometry is byte-exact; three full-state internal-light models use irregular failing-bulb flashes without a short repeating cadence; all strips retain 40 isolated frames over ten seconds')

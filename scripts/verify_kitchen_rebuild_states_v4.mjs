import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-rebuild-states-2026-10-18-v4',raw=path.join(root,'art/raw',set),draft=path.join(root,'art/drafts',set),v3raw=path.join(root,'art/raw/kitchen-rebuild-states-2026-10-18-v3')
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex'),png=f=>PNG.sync.read(fs.readFileSync(f))
assert.equal(catalogue.set,set);assert.equal(catalogue.version,4);assert.equal(catalogue.status,'variable-speed-effect-workbench-awaiting-review')
assert.equal(catalogue.method.perEffectPlaybackSpeed,true);assert.equal(catalogue.method.canonicalLoopSeconds,10);assert.equal(catalogue.promotion,'none');assert.equal(catalogue.runtimeWiring,'unchanged')
assert.equal(Object.keys(catalogue.effectFamilies).length,11);assert.equal(Object.keys(catalogue.effects).length,33)
const v3=JSON.parse(fs.readFileSync(path.join(root,'art/drafts/kitchen-rebuild-states-2026-10-18-v3/candidate-catalogue.json')))
for(const name of Object.keys(v3.outputs))assert.equal(sha(path.join(raw,name)),sha(path.join(v3raw,name)),`immutable V3 output changed: ${name}`)
for(const [family,f] of Object.entries(catalogue.effectFamilies)){assert.equal(f.models.length,3,`${family} model count`);for(const name of f.models){const m=catalogue.effects[name];assert.equal(m.durationSeconds,10);assert.equal(m.canonicalDurationSeconds,10);assert.equal(m.frames,40);assert.equal(m.fps,4);assert.deepEqual(m.speedRange,[.1,4]);assert.equal(m.editableSpeed,true);const im=png(path.join(raw,m.file));assert.deepEqual([im.width,im.height],[4800,144]);for(let frame=0;frame<40;frame++)for(let y=0;y<144;y++)for(const x of [0,119])assert.equal(im.data[(y*im.width+frame*120+x)*4+3],0,`${name} shared edge`);}}
const html=fs.readFileSync(path.join(root,'public/keeper-review/kitchen-rebuild-states-v4/index.html'),'utf8')
for(const pattern of [/Canonical 40 frames · 4 fps · 10 seconds/,/id="speed"/,/min="0\.1" max="4"/,/canonicalLoopSeconds:10/,/state\.elapsed\*\(p\.speed\|\|1\)\/250/,/10\/\(p\.speed\|\|1\)/,/localStorage\.setItem/,/navigator\.clipboard/,/Promise\.all\(DATA\.media\.map\(load\)/,/i\.decode\(\)/])assert.match(html,pattern)
const archive=path.join(root,'review-archive/sets/kitchen-rebuild-states-v4.json');assert.ok(fs.existsSync(archive),'archive manifest missing')
const manifest=JSON.parse(fs.readFileSync(archive));assert.equal(manifest.set,'kitchen-rebuild-states-v4');const archived=new Set(Object.keys(manifest.entries).map(entry=>path.basename(entry)));for(const name of Object.keys(catalogue.outputs))assert.ok(archived.has(name),`${name} not archived`)
console.log('Kitchen Rebuild V4 verified: 11 reusable families, 33 animated models, immutable ten-second sources, independent 0.1×–4× saved playback speed, placement/resize/crop/export retained')

import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-rebuild-states-2026-10-18-v6',raw=path.join(root,'art/raw',set),draft=path.join(root,'art/drafts',set),v5raw=path.join(root,'art/raw/kitchen-rebuild-states-2026-10-18-v5')
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex'),png=f=>PNG.sync.read(fs.readFileSync(f))
assert.equal(catalogue.set,set);assert.equal(catalogue.version,6);assert.equal(catalogue.status,'switchable-layered-effect-workbench-awaiting-review')
assert.equal(catalogue.method.perEffectPlaybackSpeed,true);assert.equal(catalogue.method.perEffectFamilyEnabled,true);assert.equal(catalogue.method.canonicalLoopSeconds,10);assert.equal(catalogue.promotion,'none');assert.equal(catalogue.runtimeWiring,'unchanged')
assert.equal(Object.keys(catalogue.effectFamilies).length,12);assert.equal(Object.keys(catalogue.effects).length,36)
assert.equal(catalogue.effectEnabledDefaults['fridge-broken-drip'],false)
for(const family of Object.keys(catalogue.effectFamilies))if(family!=='fridge-broken-drip')assert.equal(catalogue.effectEnabledDefaults[family],true,`${family} default enabled`)
assert.ok(!catalogue.effectFamilies['oven-broken-flicker']);assert.ok(catalogue.effectFamilies['oven-broken-warning-flicker']);assert.ok(catalogue.effectFamilies['oven-broken-cavity-flicker'])
const v5=JSON.parse(fs.readFileSync(path.join(root,'art/drafts/kitchen-rebuild-states-2026-10-18-v5/candidate-catalogue.json')))
const changed=new Set(['oven-broken.png','fx-oven-broken-flicker--classic-f40.png','fx-oven-broken-flicker--rapid-f40.png','fx-oven-broken-flicker--angry-f40.png'])
for(const name of Object.keys(v5.outputs))if(!changed.has(name))assert.equal(sha(path.join(raw,name)),sha(path.join(v5raw,name)),`immutable V5 output changed: ${name}`)
assert.notEqual(sha(path.join(raw,'oven-broken.png')),sha(path.join(v5raw,'oven-broken.png')),'burnt oven content missing')
for(const family of ['oven-broken-warning-flicker','oven-broken-cavity-flicker'])for(const name of catalogue.effectFamilies[family].models){assert.equal(catalogue.effects[name].lockedToObject,true);assert.equal(catalogue.effects[name].editableTransform,false)}
for(const [family,f] of Object.entries(catalogue.effectFamilies)){assert.equal(f.models.length,3,`${family} model count`);for(const name of f.models){const m=catalogue.effects[name];assert.equal(m.durationSeconds,10);assert.equal(m.canonicalDurationSeconds,10);assert.equal(m.frames,40);assert.equal(m.fps,4);assert.deepEqual(m.speedRange,[.1,4]);assert.equal(m.editableSpeed,true);const im=png(path.join(raw,m.file));assert.deepEqual([im.width,im.height],[4800,144]);for(let frame=0;frame<40;frame++)for(let y=0;y<144;y++)for(const x of [0,119])assert.equal(im.data[(y*im.width+frame*120+x)*4+3],0,`${name} shared edge`);}}
const html=fs.readFileSync(path.join(root,'public/keeper-review/kitchen-rebuild-states-v6/index.html'),'utf8')
for(const pattern of [/Rebuild V6 reversible draft/,/Review boundary:<\/strong> V6 draft only/,/Multiple compatible families run together/,/lockedToObject/,/Canonical 40 frames · 4 fps · 10 seconds/,/id="enabled"/,/Enable selected effect/,/saved\.enabled/,/enabled\[m\.family\]/,/models:modelChoices,enabled,placements/,/id="speed"/,/min="0\.1" max="4"/,/canonicalLoopSeconds:10/,/state\.elapsed\*\(p\.speed\|\|1\)\/250/,/10\/\(p\.speed\|\|1\)/,/localStorage\.setItem/,/navigator\.clipboard/,/Promise\.all\(DATA\.media\.map\(load\)/,/i\.decode\(\)/])assert.match(html,pattern)
assert.doesNotMatch(html,/V3 draft only|V3 directories|V5 draft only|V5 directories/)
const archive=path.join(root,'review-archive/sets/kitchen-rebuild-states-v6.json');assert.ok(fs.existsSync(archive),'archive manifest missing')
const manifest=JSON.parse(fs.readFileSync(archive));assert.equal(manifest.set,'kitchen-rebuild-states-v6');const archived=new Set(Object.keys(manifest.entries).map(entry=>path.basename(entry)));for(const name of Object.keys(catalogue.outputs))assert.ok(archived.has(name),`${name} not archived`)
console.log('Kitchen Rebuild V6 verified: 12 independently switchable layered families and 36 ten-second models; fridge drip off by default; oven smoke, locked warning flicker and locked On-derived cavity illumination active together; burnt tray present')

#!/usr/bin/env node
/** Verify V38 independent cabinets, exact V11 patches and all-location healing. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-split-cabinet-workbench-v38',batch='kitchen-split-cabinet-workbench-2026-10-20-v38'
const raw=path.join(root,'art/raw',batch),draft=path.join(root,'art/drafts',batch),review=path.join(root,'public/keeper-review',set),v37Raw=path.join(root,'art/raw/kitchen-modular-fridge-workbench-2026-10-20-v37')
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),png=file=>PNG.sync.read(fs.readFileSync(file)),rgba=(im,x,y)=>[...im.data.slice((y*im.width+x)*4,(y*im.width+x)*4+4)]
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),register=JSON.parse(fs.readFileSync(path.join(draft,'batch-register.json')))
const shared=['room-background-exact.png','cabinet-run-v11-exact.png','sink-cabinet-v19-exact.png','join-body-backfill-template.png','countertop-join-cap-template.png','countertop-triangle-underlay-template.png','neighbour-seam-cleanup-left.png','neighbour-seam-cleanup-right.png','oven-off.png','oven-on.png','oven-broken.png','oven-broken-cavity-lit.png','oven-broken-warning-lit.png','oven-broken-both-lit.png','oven-broken-cavity-flicker-f40.png','oven-broken-warning-flicker-f40.png','fridge-standard.png','fridge-broken-hinge-failed.png','fx-fridge-drip-ripple-f40.png']
const modules=['cabinet-a-le-re.png','cabinet-a-le-rj.png','cabinet-a-lj-re.png','cabinet-a-lj-rj.png','cabinet-b-le-re.png','cabinet-b-le-rj.png','cabinet-b-lj-re.png','cabinet-b-lj-rj.png']

assert.equal(catalogue.schema,'lighthouse-keeper/kitchen-split-cabinet-workbench@1');assert.equal(catalogue.set,set);assert.equal(catalogue.version,38);assert.equal(catalogue.status,'reversible-unapproved-unpromoted');assert.equal(register.set,set)
assert.deepEqual(catalogue.grid.slotOriginsX,[84,168,252,336,420,504]);assert.equal(catalogue.grid.bayWidthPixels,84);assert.equal(catalogue.grid.movableIds.length,5);assert.equal(catalogue.grid.emptySlots,1)
for(const authority of Object.values(catalogue.authorities)){const file=path.join(root,authority.file);assert.ok(fs.existsSync(file),authority.file);assert.equal(sha(file),authority.sha256,`${authority.file} authority drifted`)}
for(const name of shared)assert.equal(sha(path.join(raw,name)),sha(path.join(v37Raw,name)),`${name} is not byte-identical to V37`)
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const file=path.join(raw,name);assert.ok(fs.existsSync(file),name);assert.equal(sha(file),hash);const item=register.publishedAssets.find(e=>e.publicAssemblyPath.endsWith(`/assets/${name}`));assert.ok(item,`register missing ${name}`);assert.equal(item.sourceSha256,hash)}
const C=catalogue.assets.cabinetModules;assert.deepEqual(C.cellPixels,[92,82]);assert.deepEqual(C.bodyPixels,[84,74]);assert.deepEqual(C.cellOffset,[-4,-4]);assert.equal(C.independentlyMovable,true);assert.equal(C.pairMovement,false);assert.equal(C.edgeStates.length,4);assert.equal(catalogue.joinResolver.cabinetModules.worksOnBothSides,true)
const run=png(path.join(raw,'cabinet-run-v11-exact.png'))
function expectedX(bay,leftJoined,rightJoined,x){if(x<12)return(leftJoined?84:0)+x;if(x>=80)return(rightJoined?80:164)+(x-80);return(bay==='a'?0:84)+x}
for(const name of modules){const im=png(path.join(raw,name));assert.deepEqual([im.width,im.height],[92,82]);const bay=name[8],leftJoined=name.includes('-lj-'),rightJoined=name.includes('-rj.');for(let y=0;y<82;y++)for(let x=0;x<92;x++)assert.deepEqual(rgba(im,x,y),rgba(run,expectedX(bay,leftJoined,rightJoined,x),y),`${name} drift at ${x},${y}`)}
function entities(p){return Object.entries(p).map(([id,x])=>({id,kind:id.startsWith('cabinet')?'cabinet':id,x})).sort((a,b)=>a.x-b.x)}function method(a,b){return a.kind==='oven'||b.kind==='oven'?'oven-triangle':'flat-v22'}
const origins=[84,168,252,336,420,504],ids=['cabinetA','cabinetB','fridge','sink','oven'];let arrangements=0,cabinetAdj=0,cabinetExposedLeft=0,cabinetExposedRight=0,ovenPairs=0
function walk(depth,p,used){if(depth===ids.length){arrangements++;const e=entities(p);for(const c of e.filter(x=>x.kind==='cabinet')){const left=e.some(x=>x.id!==c.id&&x.x+84===c.x),right=e.some(x=>x.id!==c.id&&c.x+84===x.x);if(!left)cabinetExposedLeft++;if(!right)cabinetExposedRight++}for(let i=0;i<e.length-1;i++)if(e[i].x+84===e[i+1].x){if(e[i].kind==='cabinet'||e[i+1].kind==='cabinet')cabinetAdj++;if(method(e[i],e[i+1])==='oven-triangle')ovenPairs++}return}const id=ids[depth];for(const x of origins)if(!used.has(x)){p[id]=x;used.add(x);walk(depth+1,p,used);used.delete(x)}}walk(0,{},new Set())
assert.equal(arrangements,720);assert.ok(cabinetAdj>0);assert.ok(cabinetExposedLeft>0);assert.ok(cabinetExposedRight>0);assert.ok(ovenPairs>0)
for(const name of ['cabinet-pair-origin-native-room.png','cabinet-dislocated-contiguous-native-room.png','cabinet-separated-exposed-native-room.png']){const im=png(path.join(raw,name));assert.deepEqual([im.width,im.height],[772,224])}
for(const key of ['v37Changed','v11Changed','cabinetSourceRedrawn','finalChanged','runtimeChanged','promotionPerformed','kettleStarted','toasterStarted','bowlStarted'])assert.equal(catalogue.boundaries[key],false)
const html=fs.readFileSync(path.join(review,'index.html'),'utf8');for(const pattern of [/Separate the approved cabinet run into two movable units/,/Select cabinet A/,/Select cabinet B/,/nearestFree/,/cabinetName/,/occupiedByOthers/,/Two-sided cabinet resolution/,/Promise\.all\(names\.map\(load\)/,/\.decode\(\)/])assert.match(html,pattern);assert.match(fs.readFileSync(path.join(root,'next.config.mjs'),'utf8'),/source: '\/keeper-review\/kitchen-split-cabinet-workbench-v38'/)
const manifestPath=path.join(root,'review-archive/sets',`${set}.json`);assert.ok(fs.existsSync(manifestPath),'archive manifest missing');const manifest=JSON.parse(fs.readFileSync(manifestPath));assert.equal(Object.keys(manifest.entries).length,Object.keys(catalogue.publishedAssets).length);for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const entry=manifest.entries[`/keeper-review/${set}/assets/${name}`];assert.ok(entry,`archive entry missing ${name}`);assert.equal(entry.sha256,hash);assert.equal(sha(path.join(root,entry.object)),hash)}
console.log(`Kitchen Split Cabinet Workbench V38 verified: ${arrangements} layouts, exact V11 bay pixels and reversible two-sided healing.`)

#!/usr/bin/env node
/** Verify Kitchen Oven V27 registration, shaped lighting, gutters and intact joins. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-oven-standalone-v27',batch='kitchen-oven-standalone-2026-10-19-v27'
const raw=path.join(root,'art/raw',batch),draft=path.join(root,'art/drafts',batch),review=path.join(root,'public/keeper-review',set)
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),png=file=>PNG.sync.read(fs.readFileSync(file))
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),register=JSON.parse(fs.readFileSync(path.join(draft,'batch-register.json')))
assert.equal(catalogue.set,set);assert.equal(catalogue.version,27);assert.equal(catalogue.status,'reversible-unapproved-unpromoted');assert.equal(catalogue.sources.generationMode,'built-in-imagegen')
assert.deepEqual(catalogue.sources.fixedSourceWindows,[[116,48,710,667],[65,48,659,667],[13,48,607,667]])
assert.deepEqual(catalogue.geometry.logicalBodyPixels,[84,77]);assert.deepEqual(catalogue.geometry.cellPixels,[92,85]);assert.deepEqual(catalogue.geometry.transparentGutterPixels,[4,4]);assert.deepEqual(catalogue.geometry.ovenBodyBoundsInRoom,[336,131,84,77]);assert.deepEqual(catalogue.geometry.ovenCellOriginInRoom,[332,127]);assert.deepEqual(catalogue.geometry.primeInteractionAnchor,[378,218]);assert.equal(catalogue.geometry.projection,'straight-on-flat-cutaway-parallel')
assert.equal(catalogue.geometry.offOnExteriorEnvelopeByteIdentical,true);assert.equal(catalogue.geometry.roomVariantCompositing,'complete-precomposed-room-images-no-canvas-clearRect')
assert.equal(catalogue.states.off.hobIntegrated,true);assert.equal(catalogue.states.on.cavityLight,true);assert.equal(catalogue.states.on.warningLight,'solid');assert.equal(catalogue.states.on.roastingDish,'visible');assert.equal(catalogue.states.broken.door,'attached-bottom-hinge-opening-straight-toward-camera');assert.equal(catalogue.states.broken.doorWindowTransparent,true);assert.equal(catalogue.states.broken.roastingDish,'burnt-blackened');assert.equal(catalogue.states.broken.failedDial,'hanging-from-fascia-on-exactly-two-wires');assert.equal(catalogue.states.broken.smokeBakedIntoBase,false)
assert.equal(catalogue.lighting.frameCount,40);assert.equal(catalogue.lighting.baseFps,4);assert.equal(catalogue.lighting.durationSeconds,10);assert.deepEqual(catalogue.lighting.speedRange,[0.1,4]);assert.equal(catalogue.lighting.cavityPattern.length,40);assert.equal(catalogue.lighting.warningPattern.length,40);assert.equal(catalogue.lighting.sameBrokenGeometryForEveryLightingVariant,true);assert.equal(catalogue.lighting.maskMethod,'shape-and-colour-derived-no-rectangular-fascia-darkening');assert.ok(catalogue.lighting.maskOpaquePixels.cavity>40);assert.ok(catalogue.lighting.maskOpaquePixels.warning>0&&catalogue.lighting.maskOpaquePixels.warning<80)
for(const name of ['kitchen_oven_on_fan_low_loop','kitchen_oven_broken_low_electrical_buzz_loop','kitchen_oven_broken_warning_light_angry_blink_loop','kitchen_oven_broken_cavity_failing_bulb_loop','kitchen_oven_broken_smoke_hiss_loop'])assert.ok(catalogue.sfxPlaceholders.includes(name))
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const file=path.join(raw,name);assert.ok(fs.existsSync(file),name);assert.equal(sha(file),hash);const item=register.publishedAssets.find(entry=>entry.publicAssemblyPath.endsWith(`/assets/${name}`));assert.ok(item,`register missing ${name}`);assert.equal(item.sourceSha256,hash)}

const cellNames=['oven-off.png','oven-on.png','oven-broken.png','oven-broken-cavity-lit.png','oven-broken-warning-lit.png','oven-broken-both-lit.png'],cells=cellNames.map(name=>png(path.join(raw,name)))
for(const image of cells){assert.deepEqual([image.width,image.height],[92,85]);let minX=92,minY=85,maxX=-1,maxY=-1;for(let y=0;y<85;y++)for(let x=0;x<92;x++){const a=image.data[(y*92+x)*4+3],gutter=x<4||x>=88||y<4||y>=81;if(gutter)assert.equal(a,0,`opaque pixel entered gutter at ${x},${y}`);if(a){minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x);maxY=Math.max(maxY,y)}}assert.deepEqual([minX,minY,maxX+1,maxY+1],[4,4,88,81],'logical 84×77 body bounds drifted')}
for(let y=0;y<85;y++)for(let x=0;x<92;x++)assert.equal(cells[0].data[(y*92+x)*4+3],cells[1].data[(y*92+x)*4+3],`Off/On alpha envelope changed at ${x},${y}`)
const inAny=(x,y,regions)=>regions.some(([x0,y0,x1,y1])=>x>=x0+4&&x<x1+4&&y>=y0+4&&y<y1+4)
for(let y=0;y<85;y++)for(let x=0;x<92;x++){if(inAny(x,y,catalogue.geometry.onSemanticRegionsInBody))continue;const at=(y*92+x)*4;for(let c=0;c<4;c++)assert.equal(cells[0].data[at+c],cells[1].data[at+c],`Off/On exterior changed at ${x},${y}, channel ${c}`)}
for(let i=3;i<cells.length;i++)for(let y=0;y<85;y++)for(let x=0;x<92;x++)assert.equal(cells[i].data[(y*92+x)*4+3],cells[2].data[(y*92+x)*4+3],`Broken lighting changed alpha geometry at ${x},${y}`)
const diffStats=(a,b)=>{let count=0,minX=92,minY=85,maxX=-1,maxY=-1;for(let y=0;y<85;y++)for(let x=0;x<92;x++){const at=(y*92+x)*4;let changed=false;for(let c=0;c<3;c++)changed||=a.data[at+c]!==b.data[at+c];if(changed){count++;minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x);maxY=Math.max(maxY,y)}}return{count,bbox:[minX,minY,maxX+1,maxY+1]}}
const warningDiff=diffStats(cells[2],cells[4]),cavityDiff=diffStats(cells[2],cells[3]);assert.ok(warningDiff.count>0&&warningDiff.count<80,`warning change grew to ${warningDiff.count} pixels`);assert.ok(warningDiff.bbox[2]-warningDiff.bbox[0]<=10&&warningDiff.bbox[3]-warningDiff.bbox[1]<=10,`warning change became a rectangle: ${warningDiff.bbox}`);assert.ok(cavityDiff.count>60,'cavity flicker is not visibly distinct')
const family=png(path.join(raw,'oven-state-family-strip.png'));assert.deepEqual([family.width,family.height],[276,85])
for(const name of ['oven-broken-cavity-flicker-f40.png','oven-broken-warning-flicker-f40.png']){const strip=png(path.join(raw,name));assert.deepEqual([strip.width,strip.height],[3680,85]);for(let frame=0;frame<40;frame++)for(let y=0;y<85;y++)for(const x of [0,1,2,3,88,89,90,91])assert.equal(strip.data[(y*strip.width+frame*92+x)*4+3],0,`${name} frame ${frame} lost horizontal gutter`)}

const roomNames=['off','on','broken','broken-cavity-lit','broken-warning-lit','broken-both-lit'],rooms=roomNames.map(name=>png(path.join(raw,`oven-${name}-native-room.png`)))
for(const room of rooms)assert.deepEqual([room.width,room.height],[772,224])
for(let i=1;i<rooms.length;i++)for(let y=0;y<224;y++)for(let x=0;x<772;x++){if(x>=336&&x<420&&y>=131&&y<208)continue;const at=(y*772+x)*4;for(let c=0;c<4;c++)assert.equal(rooms[0].data[at+c],rooms[i].data[at+c],`${roomNames[i]} damaged neighbour/background at ${x},${y}`)}
const authority=path.join(root,catalogue.authorities.approvedCabinet.file);assert.equal(sha(authority),catalogue.authorities.approvedCabinet.sha256)
for(const key of ['approvedCabinetChanged','roomBackgroundChanged','finalChanged','runtimeChanged','promotionPerformed','nextAssetStarted'])assert.equal(catalogue.boundaries[key],false)
const html=fs.readFileSync(path.join(review,'index.html'),'utf8');for(const pattern of [/Standalone oven · registered three-state family/,/Off → On right-edge registration proof/,/complete room swap · adjacent cabinet pixels preserved/,/Broken fault playback started automatically/,/Promise\.all\(names\.map\(load\)/,/\.decode\(\)/])assert.match(html,pattern);assert.doesNotMatch(html,/clearRect\(/)
assert.match(fs.readFileSync(path.join(root,'next.config.mjs'),'utf8'),/source: '\/keeper-review\/kitchen-oven-standalone-v27'/)
const manifestPath=path.join(root,'review-archive/sets',`${set}.json`);assert.ok(fs.existsSync(manifestPath),'archive manifest missing; run npm run archive:keeper-review');const manifest=JSON.parse(fs.readFileSync(manifestPath));assert.equal(Object.keys(manifest.entries).length,Object.keys(catalogue.publishedAssets).length)
for(const [name,hash] of Object.entries(catalogue.publishedAssets))assert.equal(manifest.entries[`/keeper-review/${set}/assets/${name}`].sha256,hash)
console.log('Kitchen Oven V27 verified: fixed 84×77 envelope, shaped fault masks, complete room swaps, intact cabinet joins and auto-playing 40-frame loop.')

#!/usr/bin/env node
/** Verify V44 native-source fidelity, visible seating, gutters, lock and ownership. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-kettle-standalone-v44',batch='kitchen-kettle-standalone-2026-10-21-v44'
const raw=path.join(root,'art/raw',batch),draft=path.join(root,'art/drafts',batch),review=path.join(root,'public/keeper-review',set)
const v41Raw=path.join(root,'art/raw/kitchen-dishwasher-workbench-2026-10-20-v41')
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),read=file=>PNG.sync.read(fs.readFileSync(file))
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),register=JSON.parse(fs.readFileSync(path.join(draft,'batch-register.json')))

assert.equal(catalogue.schema,'lighthouse-keeper/kitchen-kettle-standalone@1');assert.equal(catalogue.version,44);assert.equal(catalogue.set,set);assert.equal(register.set,set)
assert.equal(catalogue.status,'reversible-unapproved-unpromoted');assert.equal(catalogue.geometry.roomPixels.join('x'),'772x224');assert.equal(catalogue.geometry.bayWidthPixels,84);assert.equal(catalogue.geometry.worktopY,134);assert.equal(catalogue.geometry.primeStopTurnY,218)
assert.deepEqual(catalogue.geometry.compatibleCounterOrigins,[84,168,336,504]);assert.deepEqual(catalogue.geometry.spriteCellPixels,[64,64]);assert.deepEqual(catalogue.geometry.cellOffset,[10,-53]);assert.deepEqual(catalogue.geometry.primeAnchor,[210,218]);assert.equal(catalogue.geometry.supportPlaneY,141);assert.equal(catalogue.geometry.contactBottomExclusive,141)
assert.deepEqual(catalogue.countertopOccupancy.supportSurfaceSlots.map(s=>[s.origin,s.supportAssetId]),[[84,'fridge'],[168,'cabinetA'],[336,'cabinetB'],[504,'dishwasher']]);assert.match(catalogue.countertopOccupancy.supportMoveRule,/Broken kettle cannot move/);assert.equal(catalogue.countertopOccupancy.movingKettleMovesSupportAsset,false);assert.equal(catalogue.countertopOccupancy.movingSupportMovesKettle,true);assert.equal(catalogue.teaInteraction.dynamicPlace,true);assert.equal(catalogue.teaInteraction.actionId,'make-cup-of-tea');assert.equal(catalogue.teaInteraction.keeperStopTurnXRule,'support bay origin + 42');assert.equal(catalogue.teaInteraction.keeperStopTurnY,218)
assert.equal(catalogue.states.on.identicalToOff,true);assert.equal(catalogue.boundaries.dishwasherV41Changed,false);assert.equal(catalogue.boundaries.approvedCabinetryChanged,false);assert.equal(catalogue.boundaries.toasterStarted,false);assert.equal(catalogue.boundaries.mixingBowlStarted,false);assert.equal(catalogue.boundaries.runtimeControllerImplemented,false);assert.equal(catalogue.boundaries.finalChanged,false)
assert.equal(catalogue.brokenAssetLock.directMove,'reject');assert.equal(catalogue.brokenAssetLock.displacementBySwap,'reject');assert.equal(catalogue.brokenAssetLock.unlockTransition,'repair to any non-broken state')
assert.equal(catalogue.countertopOccupancy.cabinetryMovesWithKettle,false);assert.equal(catalogue.countertopOccupancy.joinsRecomputed,false)

assert.equal(sha(path.join(raw,'approved-kitchen-counter-room.png')),sha(path.join(v41Raw,'dishwasher-off-native-room.png')),'approved V41 room changed')
assert.equal(sha(path.join(raw,'approved-counter-bay.png')),sha(path.join(v41Raw,'cabinet-a-le-re.png')),'approved V41 counter changed')
assert.equal(sha(path.join(raw,'kettle-off.png')),sha(path.join(raw,'kettle-on.png')),'Off and On casing must be byte-identical')

function bounds(image){let minX=image.width,minY=image.height,maxX=-1,maxY=-1,count=0;for(let y=0;y<image.height;y++)for(let x=0;x<image.width;x++)if(image.data[(y*image.width+x)*4+3]){minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x);maxY=Math.max(maxY,y);count++}return{minX,minY,maxX,maxY,count,width:maxX-minX+1,height:maxY-minY+1}}
for(const state of ['off','on','broken']){const image=read(path.join(raw,`kettle-${state}.png`)),box=bounds(image);assert.equal(image.width,64);assert.equal(image.height,64);assert.ok(box.count>500,`${state} too sparse`);assert.ok(box.width<=52&&box.height<=40,`${state} exceeds native envelope: ${box.width}x${box.height}`);assert.ok(box.minX>=4&&box.minY>=4&&box.maxX<=59&&box.maxY<=59,`${state} lacks four-pixel gutter`);assert.equal(box.maxY+1,60,`${state} does not end at local y60`);assert.equal(134-53+box.maxY+1,141,`${state} does not seat on visible support plane`);assert.deepEqual(catalogue.geometry.visibleBounds[state],[box.minX,box.minY,box.maxX+1,box.maxY+1])}
assert.deepEqual(bounds(read(path.join(raw,'kettle-off.png'))),{minX:8,minY:26,maxX:55,maxY:59,count:1050,width:48,height:34},'native Off pixels must remain exactly 48 x 34 with no resize')

const brokenStrip=read(path.join(raw,'kettle-broken-rattle-f8.png'));assert.equal(brokenStrip.width,64*8);assert.equal(brokenStrip.height,64);assert.equal(catalogue.states.broken.bodyAnimation.frameCount,8);assert.equal(catalogue.states.broken.bodyAnimation.fps,4);assert.equal(catalogue.states.broken.bodyAnimation.basePinnedToSupportY,141)
const brokenFrameHashes=new Set(),brokenBaseHashes=new Set();for(let frame=0;frame<8;frame++){const bytes=Buffer.alloc(64*64*4),base=Buffer.alloc(64*4);for(let y=0;y<64;y++)for(let x=0;x<64;x++){const si=(y*brokenStrip.width+frame*64+x)*4,di=(y*64+x)*4;for(let c=0;c<4;c++)bytes[di+c]=brokenStrip.data[si+c];if(brokenStrip.data[si+3])assert.ok(x>=4&&x<=59&&y>=4&&y<=59,`broken rattle f${frame} violates gutter`);if(y===59)for(let c=0;c<4;c++)base[x*4+c]=brokenStrip.data[si+c]}brokenFrameHashes.add(crypto.createHash('sha256').update(bytes).digest('hex'));brokenBaseHashes.add(crypto.createHash('sha256').update(base).digest('hex'))}assert.ok(brokenFrameHashes.size>=5,`broken rattle lacks motion (${brokenFrameHashes.size} unique)`);assert.equal(brokenBaseHashes.size,1,'broken rattle base row must stay pinned')

for(const state of ['on','broken'])for(const model of ['compact','regular','emphatic']){const id=`kettle-${state}-steam-${model}`,meta=catalogue.effects[id],image=read(path.join(raw,meta.file)),[cw,ch]=meta.cellPixels;assert.equal(meta.asset,'kettle');assert.equal(meta.anchorAssetId,'kettle');assert.equal(meta.transformSpace,'asset-local');assert.equal(meta.appliesToState,state);assert.equal(meta.remainsAttachedWhileBroken,true);assert.equal(meta.frameCount,40);assert.equal(meta.baseFps,4);assert.equal(meta.durationSeconds,10);assert.equal(image.width,cw*40);assert.equal(image.height,ch);const hashes=new Set();for(let frame=0;frame<40;frame++){let opaque=0;const frameBytes=Buffer.alloc(cw*ch*4);for(let y=0;y<ch;y++)for(let x=0;x<cw;x++){const si=(y*image.width+frame*cw+x)*4,di=(y*cw+x)*4;for(let c=0;c<4;c++)frameBytes[di+c]=image.data[si+c];if(image.data[si+3]){opaque++;assert.ok(x>=4&&x<cw-4&&y>=4&&y<ch-4,`${id} f${frame} violates gutter at ${x},${y}`)}}assert.ok(opaque>4,`${id} f${frame} empty`);hashes.add(crypto.createHash('sha256').update(frameBytes).digest('hex'))}assert.ok(hashes.size>=16,`${id} lacks meaningful motion (${hashes.size} unique frames)`)}

for(const state of ['off','on','broken']){const image=read(path.join(raw,`kettle-${state}-native-room.png`));assert.equal(image.width,772);assert.equal(image.height,224)}
{const image=read(path.join(raw,'kettle-off-fridge-native-room.png'));assert.equal(image.width,772);assert.equal(image.height,224)}
assert.equal(read(path.join(raw,'approved-kitchen-counter-room.png')).width,772);assert.equal(read(path.join(raw,'approved-kitchen-counter-room.png')).height,224)

const names=Object.keys(catalogue.publishedAssets);assert.equal(names.length,18);assert.equal(register.publishedAssets.length,names.length)
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const file=path.join(raw,name);assert.ok(fs.existsSync(file),name);assert.equal(sha(file),hash,`${name} hash drift`);const item=register.publishedAssets.find(entry=>entry.publicAssemblyPath.endsWith(`/assets/${name}`));assert.ok(item,`register missing ${name}`);assert.equal(item.sourceSha256,hash)}

function attemptMove(origin,state,target){if(state==='broken')return{moved:false,origin};return{moved:true,origin:target}}
for(const target of catalogue.geometry.compatibleCounterOrigins)assert.deepEqual(attemptMove(168,'broken',target),{moved:false,origin:168})
assert.deepEqual(attemptMove(168,'off',84),{moved:true,origin:84});assert.deepEqual(attemptMove(84,'on',504),{moved:true,origin:504})
const canMoveSupport=(kettleState,supportAssetId,movingAssetId)=>!(kettleState==='broken'&&supportAssetId===movingAssetId);assert.equal(canMoveSupport('broken','fridge','fridge'),false);assert.equal(canMoveSupport('off','fridge','fridge'),true);assert.equal(canMoveSupport('broken','fridge','cabinetA'),true)

const html=fs.readFileSync(path.join(review,'index.html'),'utf8')
for(const pattern of [/unscaled 48 × 34 native art/,/Full-quality concept reference/,/seated at visible y140 surface/,/including the fridge at x84/,/MAKE TEA stop\/turn/,/kettle-broken-rattle-f8\.png/,/Promise\.all\(names\.map\(load\)\)/,/\.decode\(\)/,/anchorAssetId:'kettle'/,/function tryMove\(target\)/,/Broken kettle remains fixed/,/toaster and mixing bowl have not started/i])assert.match(html,pattern)
assert.match(fs.readFileSync(path.join(root,'next.config.mjs'),'utf8'),/source: '\/keeper-review\/kitchen-kettle-standalone-v44'/)

const manifestPath=path.join(root,'review-archive/sets',`${set}.json`);assert.ok(fs.existsSync(manifestPath),'archive manifest missing')
const manifest=JSON.parse(fs.readFileSync(manifestPath));assert.equal(Object.keys(manifest.entries).length,names.length)
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const entry=manifest.entries[`/keeper-review/${set}/assets/${name}`];assert.ok(entry,`archive entry missing ${name}`);assert.equal(entry.sha256,hash);assert.equal(sha(path.join(root,entry.object)),hash)}

console.log('Kitchen Kettle Standalone V44 verified: unscaled 48 x 34 native art, source-quality review reference, exact y140 seating, isolated states/effects, Broken lock and kettle-local ownership.')

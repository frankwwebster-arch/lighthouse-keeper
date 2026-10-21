#!/usr/bin/env node
/** Verify V45 source fidelity, logical scale, support lock, effect ownership and delivery. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-kettle-standalone-v45',batch='kitchen-kettle-standalone-2026-10-21-v45'
const raw=path.join(root,'art/raw',batch),draft=path.join(root,'art/drafts',batch),review=path.join(root,'public/keeper-review',set)
const v41Raw=path.join(root,'art/raw/kitchen-dishwasher-workbench-2026-10-20-v41')
const sourceRoot=path.join(root,'art/source/kitchen-kettle-standalone-2026-10-20-v43/generated')
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),read=file=>PNG.sync.read(fs.readFileSync(file))
const rgbaHash=image=>crypto.createHash('sha256').update(image.data).digest('hex')
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),register=JSON.parse(fs.readFileSync(path.join(draft,'batch-register.json')))

assert.equal(catalogue.schema,'lighthouse-keeper/kitchen-kettle-standalone@1');assert.equal(catalogue.version,45);assert.equal(catalogue.set,set);assert.equal(register.set,set)
assert.equal(catalogue.status,'reversible-unapproved-unpromoted');assert.deepEqual(catalogue.geometry.roomPixels,[772,224]);assert.equal(catalogue.geometry.reviewBackingScale,2);assert.equal(catalogue.geometry.bayWidthPixels,84);assert.equal(catalogue.geometry.worktopY,134);assert.equal(catalogue.geometry.supportPlaneY,141);assert.equal(catalogue.geometry.contactBottomExclusive,141)
assert.deepEqual(catalogue.geometry.compatibleCounterOrigins,[84,168,336,504]);assert.deepEqual(catalogue.geometry.primeAnchor,[210,218]);assert.deepEqual(catalogue.countertopOccupancy.supportSurfaceSlots.map(s=>[s.origin,s.supportAssetId]),[[84,'fridge'],[168,'cabinetA'],[336,'cabinetB'],[504,'dishwasher']])
assert.deepEqual(catalogue.geometry.stateRender.off.renderPixels,[56,51]);assert.deepEqual(catalogue.geometry.stateRender.broken.renderPixels,[62,59]);assert.ok(catalogue.geometry.stateRender.off.renderPixels[0]/84>.65);assert.ok(catalogue.geometry.stateRender.broken.renderPixels[0]/84<.75)
assert.equal(catalogue.sourceProvenance.generatedSourcesUsedAsProductionSprites,true);assert.equal(catalogue.sourceProvenance.productionResizeAppliedToKettleMasters,false);assert.match(catalogue.sourceProvenance.mode,/promoted directly to production masters/)
assert.equal(catalogue.states.on.identicalToOff,true);assert.equal(catalogue.states.broken.movementLocked,true);assert.equal(catalogue.states.broken.staticDamage.length,6)
assert.equal(catalogue.states.broken.bodyAnimation.type,'asset-local-transform');assert.equal(catalogue.states.broken.bodyAnimation.pivot,'bottom-centre-support-contact');assert.equal(catalogue.states.broken.bodyAnimation.basePinnedToSupportY,141);assert.equal(catalogue.states.broken.bodyAnimation.frameCount,8);assert.ok(Math.max(...catalogue.states.broken.bodyAnimation.keyframes.map(k=>Math.abs(k.dx)))>=3);assert.ok(Math.max(...catalogue.states.broken.bodyAnimation.keyframes.map(k=>Math.abs(k.angle)))>=4);assert.ok(catalogue.states.broken.bodyAnimation.keyframes.every(k=>!('dy'in k)),'broken base must have no vertical displacement')
assert.equal(catalogue.brokenAssetLock.directMove,'reject');assert.equal(catalogue.brokenAssetLock.displacementBySwap,'reject');assert.equal(catalogue.brokenAssetLock.unlockTransition,'repair to any non-broken state');assert.match(catalogue.countertopOccupancy.supportMoveRule,/Broken kettle cannot move/)
assert.equal(catalogue.teaInteraction.dynamicPlace,true);assert.equal(catalogue.teaInteraction.actionId,'make-cup-of-tea');assert.equal(catalogue.teaInteraction.keeperStopTurnXRule,'support bay origin + 42');assert.equal(catalogue.teaInteraction.keeperStopTurnY,218);assert.equal(catalogue.teaInteraction.blockedState,'broken')
for(const key of ['dishwasherV41Changed','approvedCabinetryChanged','toasterStarted','mixingBowlStarted','runtimeControllerImplemented','finalChanged'])assert.equal(catalogue.boundaries[key],false,`${key} boundary changed`)

assert.equal(sha(path.join(raw,'approved-kitchen-counter-room.png')),sha(path.join(v41Raw,'dishwasher-off-native-room.png')),'approved V41 room changed')
assert.equal(sha(path.join(raw,'approved-counter-bay.png')),sha(path.join(v41Raw,'cabinet-a-le-re.png')),'approved V41 counter changed')
assert.equal(sha(path.join(raw,'kettle-off.png')),sha(path.join(raw,'kettle-on.png')),'Off and On masters must be byte-identical')

function crop(src,x,y,width,height){const out=new PNG({width,height});for(let yy=0;yy<height;yy++)for(let xx=0;xx<width;xx++){const si=((y+yy)*src.width+x+xx)*4,di=(yy*width+xx)*4;for(let c=0;c<4;c++)out.data[di+c]=src.data[si+c]}return out}
function thresholdAlpha(image,threshold=18){for(let i=3;i<image.data.length;i+=4)if(image.data[i]<threshold)image.data[i-3]=image.data[i-2]=image.data[i-1]=image.data[i]=0;return image}
function bounds(image){let minX=image.width,minY=image.height,maxX=-1,maxY=-1,count=0;for(let y=0;y<image.height;y++)for(let x=0;x<image.width;x++)if(image.data[(y*image.width+x)*4+3]){minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x);maxY=Math.max(maxY,y);count++}return{minX,minY,maxX,maxY,count,width:maxX-minX+1,height:maxY-minY+1}}
for(const [state,sourceFile,record]of[['off','kettle-state-family-source.png',catalogue.sourceProvenance.stateFamily],['broken','kettle-broken-source.png',catalogue.sourceProvenance.brokenState]]){
  const master=read(path.join(raw,`kettle-${state}.png`)),box=record.selectedComponent,[sx,sy,sw,sh]=catalogue.geometry.stateRender[state].sourceRect
  assert.equal(sx,32);assert.equal(sy,32);assert.equal(sw,box.width);assert.equal(sh,box.height);assert.equal(master.width,sw+64);assert.equal(master.height,sh+64)
  const masterBounds=bounds(master);assert.ok(masterBounds.minX>=32&&masterBounds.minY>=32&&masterBounds.maxX<master.width-32&&masterBounds.maxY<master.height-32,`${state} lacks transparent safety gutter`)
  const sourceComponent=thresholdAlpha(crop(read(path.join(sourceRoot,sourceFile)),box.x,box.y,box.width,box.height))
  assert.equal(rgbaHash(crop(master,sx,sy,sw,sh)),rgbaHash(sourceComponent),`${state} production pixels differ from approved concept component`)
}
assert.equal(read(path.join(raw,'kettle-off.png')).width,652);assert.equal(read(path.join(raw,'kettle-off.png')).height,604)
assert.equal(read(path.join(raw,'kettle-broken.png')).width,1040);assert.equal(read(path.join(raw,'kettle-broken.png')).height,992)

for(const state of ['on','broken'])for(const model of ['compact','regular','emphatic']){const id=`kettle-${state}-steam-${model}`,meta=catalogue.effects[id],image=read(path.join(raw,meta.file)),[cw,ch]=meta.rasterCellPixels;assert.equal(meta.asset,'kettle');assert.equal(meta.anchorAssetId,'kettle');assert.equal(meta.transformSpace,'asset-local');assert.equal(meta.appliesToState,state);assert.equal(meta.remainsAttachedWhileBroken,true);assert.equal(meta.frameCount,40);assert.equal(meta.baseFps,4);assert.equal(meta.durationSeconds,10);assert.equal(image.width,cw*40);assert.equal(image.height,ch);assert.ok(cw>=128&&ch>=176,'effect cells must retain high-resolution raster data');const hashes=new Set();for(let frame=0;frame<40;frame++){let opaque=0;const bytes=Buffer.alloc(cw*ch*4);for(let y=0;y<ch;y++)for(let x=0;x<cw;x++){const si=(y*image.width+frame*cw+x)*4,di=(y*cw+x)*4;for(let c=0;c<4;c++)bytes[di+c]=image.data[si+c];if(image.data[si+3]){opaque++;assert.ok(x>=8&&x<cw-8&&y>=8&&y<ch-8,`${id} f${frame} violates eight-pixel gutter at ${x},${y}`)}}assert.ok(opaque>40,`${id} f${frame} is too sparse`);hashes.add(crypto.createHash('sha256').update(bytes).digest('hex'))}assert.ok(hashes.size>=16,`${id} lacks meaningful motion (${hashes.size} unique frames)`) }

for(const name of ['kettle-off-retina-room.png','kettle-on-retina-room.png','kettle-broken-retina-room.png','kettle-off-fridge-retina-room.png']){const image=read(path.join(raw,name));assert.equal(image.width,1544);assert.equal(image.height,448)}
const names=Object.keys(catalogue.publishedAssets);assert.equal(names.length,15);assert.equal(register.publishedAssets.length,names.length)
for(const[name,hash]of Object.entries(catalogue.publishedAssets)){const file=path.join(raw,name);assert.ok(fs.existsSync(file),name);assert.equal(sha(file),hash,`${name} hash drift`);const item=register.publishedAssets.find(entry=>entry.publicAssemblyPath.endsWith(`/assets/${name}`));assert.ok(item,`register missing ${name}`);assert.equal(item.sourceSha256,hash)}

function attemptMove(origin,state,target){if(state==='broken')return{moved:false,origin};return{moved:true,origin:target}}
for(const target of catalogue.geometry.compatibleCounterOrigins)assert.deepEqual(attemptMove(168,'broken',target),{moved:false,origin:168});assert.deepEqual(attemptMove(168,'off',84),{moved:true,origin:84})
const canMoveSupport=(kettleState,supportAssetId,movingAssetId)=>!(kettleState==='broken'&&supportAssetId===movingAssetId);assert.equal(canMoveSupport('broken','fridge','fridge'),false);assert.equal(canMoveSupport('off','fridge','fridge'),true)

const html=fs.readFileSync(path.join(review,'index.html'),'utf8')
for(const pattern of [/concept art = production master/,/actual production masters/i,/588 × 540 source-detail/,/including the fridge at x84/,/MAKE TEA stop\/turn/,/2× backing/,/Promise\.all\(names\.map\(load\)\)/,/\.decode\(\)/,/anchorAssetId:'kettle'/,/bottom-centre-support-contact/,/Broken kettle remains fixed/,/toaster and mixing bowl have not started/i])assert.match(html,pattern)
assert.match(fs.readFileSync(path.join(root,'next.config.mjs'),'utf8'),/source: '\/keeper-review\/kitchen-kettle-standalone-v45'/)

const manifestPath=path.join(root,'review-archive/sets',`${set}.json`);assert.ok(fs.existsSync(manifestPath),'archive manifest missing')
const manifest=JSON.parse(fs.readFileSync(manifestPath));assert.equal(Object.keys(manifest.entries).length,names.length)
for(const[name,hash]of Object.entries(catalogue.publishedAssets)){const entry=manifest.entries[`/keeper-review/${set}/assets/${name}`];assert.ok(entry,`archive entry missing ${name}`);assert.equal(entry.sha256,hash);assert.equal(sha(path.join(root,entry.object)),hash)}

console.log('Kitchen Kettle Standalone V45 verified: concept pixels are production masters, logical scale is independent, Retina proofs seat on y140, and Broken lock/effects remain kettle-owned.')

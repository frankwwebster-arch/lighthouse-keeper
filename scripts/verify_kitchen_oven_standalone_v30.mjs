#!/usr/bin/env node
/** Verify Oven V30 foreground protection and exact-adjacency join healing. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-oven-standalone-v30',batch='kitchen-oven-standalone-2026-10-20-v30',v29Batch='kitchen-oven-standalone-2026-10-20-v29'
const raw=path.join(root,'art/raw',batch),v29Raw=path.join(root,'art/raw',v29Batch),draft=path.join(root,'art/drafts',batch),review=path.join(root,'public/keeper-review',set)
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),png=file=>PNG.sync.read(fs.readFileSync(file))
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),register=JSON.parse(fs.readFileSync(path.join(draft,'batch-register.json')))

assert.equal(catalogue.set,set);assert.equal(catalogue.version,30);assert.equal(catalogue.status,'reversible-unapproved-unpromoted')
assert.equal(catalogue.sources.generationMode,'deterministic-existing-pixel-compositing')
assert.deepEqual(catalogue.geometry.logicalBodyPixels,[84,77]);assert.deepEqual(catalogue.geometry.cellPixels,[92,85]);assert.deepEqual(catalogue.geometry.transparentGutterPixels,[4,4])
assert.deepEqual(catalogue.geometry.ovenBodyBoundsInRoom,[336,131,84,77]);assert.deepEqual(catalogue.geometry.ovenCellOriginInRoom,[332,127]);assert.deepEqual(catalogue.geometry.primeInteractionAnchor,[378,218])
assert.equal(catalogue.foregroundProtection.object,'broken dangling dial');assert.equal(catalogue.foregroundProtection.dialReceivesCavityLight,false);assert.deepEqual(catalogue.foregroundProtection.affectedLitStates,['oven-broken-cavity-lit.png','oven-broken-both-lit.png'])
assert.equal(catalogue.joinHealing.method,'approved-v22-countertop-underlay');assert.deepEqual(catalogue.joinHealing.templatePixels,[24,12]);assert.deepEqual(catalogue.joinHealing.sharedEdgeX,[336,420]);assert.deepEqual(catalogue.joinHealing.destinationOrigins,[[324,134],[408,134]])
assert.equal(catalogue.joinHealing.embeddedInOvenSprite,false);assert.equal(catalogue.joinHealing.embeddedInCabinetSprite,false);assert.equal(catalogue.joinHealing.leftAndRightIndependent,true)
assert.equal(catalogue.lighting.frameCount,40);assert.equal(catalogue.lighting.baseFps,4);assert.equal(catalogue.lighting.durationSeconds,10);assert.deepEqual(catalogue.lighting.speedRange,[0.1,4]);assert.equal(catalogue.lighting.danglingDialForegroundProtected,true)

for(const authority of Object.values(catalogue.authorities)){const file=path.join(root,authority.file);assert.ok(fs.existsSync(file),authority.file);assert.equal(sha(file),authority.sha256,`${authority.file} authority drifted`)}
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const file=path.join(raw,name);assert.ok(fs.existsSync(file),name);assert.equal(sha(file),hash);const item=register.publishedAssets.find(entry=>entry.publicAssemblyPath.endsWith(`/assets/${name}`));assert.ok(item,`register missing ${name}`);assert.equal(item.sourceSha256,hash)}

const stateNames=['oven-off.png','oven-on.png','oven-broken.png','oven-broken-cavity-lit.png','oven-broken-warning-lit.png','oven-broken-both-lit.png']
const unchanged=new Set(['oven-off.png','oven-on.png','oven-broken.png','oven-broken-warning-lit.png'])
const rows=new Set();for(const [y,x0,x1] of catalogue.foregroundProtection.cellRows)for(let x=x0;x<x1;x++)rows.add(`${x},${y}`)
const dark=png(path.join(raw,'oven-broken.png'))
for(const name of stateNames){
  const image=png(path.join(raw,name)),authority=png(path.join(v29Raw,name));assert.deepEqual([image.width,image.height],[92,85]);let changes=0
  for(let y=0;y<85;y++)for(let x=0;x<92;x++){
    const at=(y*92+x)*4,gutter=x<4||x>=88||y<4||y>=81;if(gutter)assert.equal(image.data[at+3],0,`${name} opaque gutter at ${x},${y}`)
    let changed=false;for(let c=0;c<4;c++)changed||=image.data[at+c]!==authority.data[at+c]
    if(changed){assert.ok(rows.has(`${x},${y}`),`${name} changed outside dial foreground at ${x},${y}`);changes++}
  }
  if(unchanged.has(name))assert.equal(changes,0,`${name} must remain byte-identical to V29`);else assert.ok(changes>20,`${name} did not protect the dangling dial`)
}
for(const name of ['oven-broken-cavity-lit.png','oven-broken-both-lit.png']){const image=png(path.join(raw,name));for(const key of rows){const [x,y]=key.split(',').map(Number),at=(y*92+x)*4;for(let c=0;c<4;c++)assert.equal(image.data[at+c],dark.data[at+c],`${name} dial is not foreground-protected at ${x},${y}`)}}
const lit=png(path.join(raw,'oven-broken-cavity-lit.png'));let cavityDiff=0;for(let y=20;y<69;y++)for(let x=12;x<80;x++){if(rows.has(`${x},${y}`))continue;const at=(y*92+x)*4;for(let c=0;c<3;c++)if(lit.data[at+c]!==dark.data[at+c]){cavityDiff++;break}}assert.ok(cavityDiff>1000,'cavity light was lost while protecting the dial')

const family=png(path.join(raw,'oven-state-family-strip.png'));assert.deepEqual([family.width,family.height],[276,85])
for(const name of ['oven-broken-cavity-flicker-f40.png','oven-broken-warning-flicker-f40.png']){const strip=png(path.join(raw,name));assert.deepEqual([strip.width,strip.height],[3680,85]);for(let frame=0;frame<40;frame++)for(let y=0;y<85;y++)for(const x of [0,1,2,3,88,89,90,91])assert.equal(strip.data[(y*strip.width+frame*92+x)*4+3],0,`${name} frame ${frame} lost gutter`)}
assert.equal(sha(path.join(raw,'oven-broken-warning-flicker-f40.png')),sha(path.join(v29Raw,'oven-broken-warning-flicker-f40.png')),'warning-only loop must remain byte-identical')

const roomNames=['off','on','broken','broken-cavity-lit','broken-warning-lit','broken-both-lit']
for(const name of roomNames){const room=png(path.join(raw,`oven-${name}-native-room.png`)),authority=png(path.join(v29Raw,`oven-${name}-native-room.png`));assert.deepEqual([room.width,room.height],[772,224]);let joinChanges=0,dialChanges=0;for(let y=0;y<224;y++)for(let x=0;x<772;x++){const at=(y*772+x)*4;let changed=false;for(let c=0;c<4;c++)changed||=room.data[at+c]!==authority.data[at+c];if(!changed)continue;const inJoin=(x>=324&&x<348&&y>=134&&y<146)||(x>=408&&x<432&&y>=134&&y<146),cellX=x-332,cellY=y-127,inDial=rows.has(`${cellX},${cellY}`);assert.ok(inJoin||inDial,`${name} room changed outside join/dial at ${x},${y}`);if(inJoin)joinChanges++;if(inDial)dialChanges++}assert.ok(joinChanges>0,`${name} has no visible countertop healing`);if(name==='broken-cavity-lit'||name==='broken-both-lit')assert.ok(dialChanges>20,`${name} room lost foreground dial correction`);else assert.equal(dialChanges,0,`${name} room changed the dial unexpectedly`)}

for(const [name,size] of [['room-background-exact.png',[772,224]],['cabinet-run-v11-exact.png',[176,82]],['countertop-join-heal-template.png',[24,12]],['oven-join-raw-focus.png',[124,28]],['oven-join-healed-focus.png',[124,28]],['oven-v29-lit-dial-focus.png',[22,28]],['oven-v30-protected-dial-focus.png',[22,28]]]){const image=png(path.join(raw,name));assert.deepEqual([image.width,image.height],size,`${name} dimensions drifted`)}
assert.equal(sha(path.join(raw,'room-background-exact.png')),catalogue.authorities.roomBackground.sha256);assert.equal(sha(path.join(raw,'cabinet-run-v11-exact.png')),catalogue.authorities.approvedCabinet.sha256);assert.equal(sha(path.join(raw,'countertop-join-heal-template.png')),catalogue.authorities.approvedJoinCap.sha256)

const v29Data=JSON.parse(fs.readFileSync(path.join(root,'art/drafts',v29Batch,'candidate-catalogue.json')));assert.deepEqual(catalogue.states,v29Data.states);assert.deepEqual(catalogue.lighting.cavityPattern,v29Data.lighting.cavityPattern);assert.deepEqual(catalogue.lighting.warningPattern,v29Data.lighting.warningPattern);assert.deepEqual(catalogue.sfxPlaceholders,v29Data.sfxPlaceholders)
for(const key of ['v29Changed','offChanged','onChanged','brokenDarkChanged','cabinetChanged','roomBackgroundChanged','finalChanged','runtimeChanged','promotionPerformed','nextAssetStarted'])assert.equal(catalogue.boundaries[key],false)

const html=fs.readFileSync(path.join(review,'index.html'),'utf8');for(const pattern of [/protected dial and healed joins/,/exactLeftAdjacency/,/exactRightAdjacency/,/countertop-join-heal-template/,/dial foreground protected/,/Promise\.all\(names\.map\(load\)/,/\.decode\(\)/])assert.match(html,pattern);assert.doesNotMatch(html,/clearRect\(/)
assert.match(fs.readFileSync(path.join(root,'next.config.mjs'),'utf8'),/source: '\/keeper-review\/kitchen-oven-standalone-v30'/)
const manifestPath=path.join(root,'review-archive/sets',`${set}.json`);assert.ok(fs.existsSync(manifestPath),'archive manifest missing; run npm run archive:keeper-review:set');const manifest=JSON.parse(fs.readFileSync(manifestPath));assert.equal(Object.keys(manifest.entries).length,Object.keys(catalogue.publishedAssets).length)
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const entry=manifest.entries[`/keeper-review/${set}/assets/${name}`];assert.ok(entry,`archive entry missing ${name}`);assert.equal(entry.sha256,hash);assert.ok(fs.existsSync(path.join(root,entry.object)),`${name} archive object missing`);assert.equal(sha(path.join(root,entry.object)),hash)}
console.log('Kitchen Oven V30 verified: the dangling dial stays in front of cavity light; both V-shaped countertop gaps heal only through exact-adjacency underlays; geometry and Prime anchor remain exact.')

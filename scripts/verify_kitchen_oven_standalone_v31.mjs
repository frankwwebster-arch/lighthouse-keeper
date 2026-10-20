#!/usr/bin/env node
/** Verify Oven V31's seamless countertop cap and blue body backfill. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-oven-standalone-v31',batch='kitchen-oven-standalone-2026-10-20-v31',v30Batch='kitchen-oven-standalone-2026-10-20-v30'
const raw=path.join(root,'art/raw',batch),v30Raw=path.join(root,'art/raw',v30Batch),draft=path.join(root,'art/drafts',batch),review=path.join(root,'public/keeper-review',set)
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),png=file=>PNG.sync.read(fs.readFileSync(file))
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),register=JSON.parse(fs.readFileSync(path.join(draft,'batch-register.json')))
const states=['oven-off.png','oven-on.png','oven-broken.png','oven-broken-cavity-lit.png','oven-broken-warning-lit.png','oven-broken-both-lit.png']
const loops=['oven-state-family-strip.png','oven-broken-cavity-flicker-f40.png','oven-broken-warning-flicker-f40.png']

function composite(dst,src,dx,dy,sx=0,sy=0,w=src.width,h=src.height){
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
    const si=((sy+y)*src.width+sx+x)*4,di=((dy+y)*dst.width+dx+x)*4,a=src.data[si+3]/255,da=dst.data[di+3]/255,oa=a+da*(1-a)
    if(!oa)continue
    for(let c=0;c<3;c++)dst.data[di+c]=Math.round((src.data[si+c]*a+dst.data[di+c]*da*(1-a))/oa)
    dst.data[di+3]=Math.round(oa*255)
  }
}
const clone=image=>PNG.sync.read(PNG.sync.write(image))
const pixel=(image,x,y)=>[...image.data.slice((y*image.width+x)*4,(y*image.width+x)*4+4)]

assert.equal(catalogue.set,set);assert.equal(catalogue.version,31);assert.equal(catalogue.status,'reversible-unapproved-unpromoted')
assert.equal(catalogue.sources.generationMode,'deterministic-existing-pixel-layered-compositing')
assert.deepEqual(catalogue.geometry.logicalBodyPixels,[84,77]);assert.deepEqual(catalogue.geometry.cellPixels,[92,85]);assert.deepEqual(catalogue.geometry.transparentGutterPixels,[4,4])
assert.deepEqual(catalogue.geometry.ovenBodyBoundsInRoom,[336,131,84,77]);assert.deepEqual(catalogue.geometry.ovenCellOriginInRoom,[332,127]);assert.deepEqual(catalogue.geometry.primeInteractionAnchor,[378,218])
assert.equal(catalogue.foregroundProtection.dialReceivesCavityLight,false)
assert.equal(catalogue.joinHealing.method,'approved-v22-two-layer-seamless-join');assert.deepEqual(catalogue.joinHealing.sharedEdgeX,[336,420]);assert.equal(catalogue.joinHealing.leftAndRightIndependent,true)
assert.deepEqual(catalogue.joinHealing.bodyBackfill.sourceCrop,[0,0,6,63]);assert.deepEqual(catalogue.joinHealing.bodyBackfill.destinationOrigins,[[333,145],[417,145]]);assert.equal(catalogue.joinHealing.bodyBackfill.placement,'behind assets')
assert.deepEqual(catalogue.joinHealing.countertopCap.sourceCrop,[0,0,16,12]);assert.deepEqual(catalogue.joinHealing.countertopCap.destinationOrigins,[[328,134],[412,134]]);assert.equal(catalogue.joinHealing.countertopCap.placement,'in front of assets');assert.equal(catalogue.joinHealing.countertopCap.seamVisible,false)
assert.deepEqual(catalogue.joinHealing.drawOrder,['room background','active blue body backfills','cabinet neighbours','standalone oven','active seamless countertop caps'])
assert.equal(catalogue.joinHealing.embeddedInOvenSprite,false);assert.equal(catalogue.joinHealing.embeddedInCabinetSprite,false)
assert.equal(catalogue.lighting.frameCount,40);assert.equal(catalogue.lighting.baseFps,4);assert.equal(catalogue.lighting.durationSeconds,10);assert.deepEqual(catalogue.lighting.speedRange,[0.1,4])

for(const authority of Object.values(catalogue.authorities)){const file=path.join(root,authority.file);assert.ok(fs.existsSync(file),authority.file);assert.equal(sha(file),authority.sha256,`${authority.file} authority drifted`)}
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const file=path.join(raw,name);assert.ok(fs.existsSync(file),name);assert.equal(sha(file),hash);const item=register.publishedAssets.find(entry=>entry.publicAssemblyPath.endsWith(`/assets/${name}`));assert.ok(item,`register missing ${name}`);assert.equal(item.sourceSha256,hash)}

for(const name of [...states,...loops])assert.equal(sha(path.join(raw,name)),sha(path.join(v30Raw,name)),`${name} must remain byte-identical to V30`)
for(const name of states){const image=png(path.join(raw,name));assert.deepEqual([image.width,image.height],[92,85]);for(let y=0;y<85;y++)for(let x=0;x<92;x++){if(x<4||x>=88||y<4||y>=81)assert.equal(image.data[(y*92+x)*4+3],0,`${name} opaque gutter at ${x},${y}`)}}
assert.deepEqual([png(path.join(raw,'oven-broken-cavity-flicker-f40.png')).width,png(path.join(raw,'oven-broken-cavity-flicker-f40.png')).height],[3680,85])
assert.deepEqual([png(path.join(raw,'oven-broken-warning-flicker-f40.png')).width,png(path.join(raw,'oven-broken-warning-flicker-f40.png')).height],[3680,85])

const background=png(path.join(raw,'room-background-exact.png')),cabinet=png(path.join(raw,'cabinet-run-v11-exact.png')),body=png(path.join(raw,'join-body-backfill-template.png')),cap=png(path.join(raw,'countertop-seamless-cap-template.png'))
assert.deepEqual([background.width,background.height],[772,224]);assert.deepEqual([cabinet.width,cabinet.height],[176,82]);assert.deepEqual([body.width,body.height],[14,63]);assert.deepEqual([cap.width,cap.height],[24,12])
assert.equal(sha(path.join(raw,'join-body-backfill-template.png')),catalogue.authorities.approvedBodyBackfill.sha256);assert.equal(sha(path.join(raw,'countertop-seamless-cap-template.png')),catalogue.authorities.approvedCountertopCap.sha256)

for(const state of ['off','on','broken','broken-cavity-lit','broken-warning-lit','broken-both-lit']){
  const actual=png(path.join(raw,`oven-${state}-native-room.png`)),expected=clone(background),oven=png(path.join(raw,`oven-${state}.png`))
  composite(expected,body,333,145,0,0,6,63);composite(expected,body,417,145,0,0,6,63)
  composite(expected,cabinet,164,130);composite(expected,cabinet,416,130);composite(expected,oven,332,127)
  composite(expected,cap,328,134,0,0,16,12);composite(expected,cap,412,134,0,0,16,12)
  assert.deepEqual(actual.data,expected.data,`${state} room violates layered draw order`)
  for(const edge of [336,420])for(let y=0;y<12;y++)for(let x=0;x<16;x++)assert.deepEqual(pixel(actual,edge-8+x,134+y),pixel(cap,x,y),`${state} countertop seam remains at ${edge-8+x},${134+y}`)
  for(const [x0,x1] of [[335,337],[419,421]])for(let y=146;y<208;y++)for(let x=x0;x<x1;x++)assert.notDeepEqual(pixel(actual,x,y),pixel(background,x,y),`${state} wall remains visible in body gap at ${x},${y}`)
  const v30=png(path.join(v30Raw,`oven-${state}-native-room.png`));let changed=0
  for(let y=0;y<224;y++)for(let x=0;x<772;x++){const at=(y*772+x)*4;let diff=false;for(let c=0;c<4;c++)diff||=actual.data[at+c]!==v30.data[at+c];if(!diff)continue;const replacedV30Underlay=((x>=324&&x<348)||(x>=408&&x<432))&&y>=134&&y<146,bodyBackfill=((x>=333&&x<339)||(x>=417&&x<423))&&y>=145&&y<208;assert.ok(replacedV30Underlay||bodyBackfill,`${state} changed outside declared join layers at ${x},${y}`);changed++}assert.ok(changed>100,`${state} did not receive layered healing`)
}

for(const [name,size] of [['oven-v30-underlay-join-focus.png',[124,90]],['oven-v31-layered-join-focus.png',[124,90]],['oven-v30-protected-dial-focus.png',[22,28]]]){const image=png(path.join(raw,name));assert.deepEqual([image.width,image.height],size)}
const v30=JSON.parse(fs.readFileSync(path.join(root,'art/drafts',v30Batch,'candidate-catalogue.json')));assert.deepEqual(catalogue.states,v30.states);assert.deepEqual(catalogue.lighting,v30.lighting);assert.deepEqual(catalogue.sfxPlaceholders,v30.sfxPlaceholders)
for(const key of ['v30Changed','ovenSpritesChanged','cabinetChanged','v22JoinAuthorityChanged','roomBackgroundChanged','finalChanged','runtimeChanged','promotionPerformed','nextAssetStarted'])assert.equal(catalogue.boundaries[key],false)

const html=fs.readFileSync(path.join(review,'index.html'),'utf8');for(const pattern of [/continuous worktop and blue gap healing/,/drawJoinBody/,/drawJoinCap/,/exactLeftAdjacency/,/exactRightAdjacency/,/blue backfill → assets → seamless countertop cap/,/Promise\.all\(names\.map\(load\)/,/\.decode\(\)/])assert.match(html,pattern);assert.doesNotMatch(html,/clearRect\(/)
assert.match(fs.readFileSync(path.join(root,'next.config.mjs'),'utf8'),/source: '\/keeper-review\/kitchen-oven-standalone-v31'/)
const manifestPath=path.join(root,'review-archive/sets',`${set}.json`);assert.ok(fs.existsSync(manifestPath),'archive manifest missing; run npm run archive:keeper-review:set');const manifest=JSON.parse(fs.readFileSync(manifestPath));assert.equal(Object.keys(manifest.entries).length,Object.keys(catalogue.publishedAssets).length)
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const entry=manifest.entries[`/keeper-review/${set}/assets/${name}`];assert.ok(entry,`archive entry missing ${name}`);assert.equal(entry.sha256,hash);assert.ok(fs.existsSync(path.join(root,entry.object)),`${name} archive object missing`);assert.equal(sha(path.join(root,entry.object)),hash)}
console.log('Kitchen Oven V31 verified: each snapped edge uses a seam-free foreground countertop cap and cabinet-blue body backfill; all oven sprites, geometry and Prime anchor remain exact.')

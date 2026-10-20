#!/usr/bin/env node
/** Verify Oven V32 retains V30 triangles while removing cabinet-facing seams. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-oven-standalone-v32',batch='kitchen-oven-standalone-2026-10-20-v32',v30Batch='kitchen-oven-standalone-2026-10-20-v30'
const raw=path.join(root,'art/raw',batch),v30Raw=path.join(root,'art/raw',v30Batch),draft=path.join(root,'art/drafts',batch),review=path.join(root,'public/keeper-review',set)
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),png=file=>PNG.sync.read(fs.readFileSync(file)),clone=image=>PNG.sync.read(PNG.sync.write(image)),pixel=(im,x,y)=>[...im.data.slice((y*im.width+x)*4,(y*im.width+x)*4+4)]
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),register=JSON.parse(fs.readFileSync(path.join(draft,'batch-register.json')))
const states=['oven-off.png','oven-on.png','oven-broken.png','oven-broken-cavity-lit.png','oven-broken-warning-lit.png','oven-broken-both-lit.png'],loops=['oven-state-family-strip.png','oven-broken-cavity-flicker-f40.png','oven-broken-warning-flicker-f40.png']

function composite(dst,src,dx,dy,sx=0,sy=0,w=src.width,h=src.height){for(let y=0;y<h;y++)for(let x=0;x<w;x++){const si=((sy+y)*src.width+sx+x)*4,di=((dy+y)*dst.width+dx+x)*4,a=src.data[si+3]/255,da=dst.data[di+3]/255,oa=a+da*(1-a);if(!oa)continue;for(let c=0;c<3;c++)dst.data[di+c]=Math.round((src.data[si+c]*a+dst.data[di+c]*da*(1-a))/oa);dst.data[di+3]=Math.round(oa*255)}}

assert.equal(catalogue.set,set);assert.equal(catalogue.version,32);assert.equal(catalogue.status,'reversible-unapproved-unpromoted');assert.equal(catalogue.sources.generationMode,'deterministic-existing-pixel-masked-compositing')
assert.deepEqual(catalogue.geometry.logicalBodyPixels,[84,77]);assert.deepEqual(catalogue.geometry.cellPixels,[92,85]);assert.deepEqual(catalogue.geometry.transparentGutterPixels,[4,4]);assert.deepEqual(catalogue.geometry.ovenBodyBoundsInRoom,[336,131,84,77]);assert.deepEqual(catalogue.geometry.primeInteractionAnchor,[378,218]);assert.equal(catalogue.foregroundProtection.dialReceivesCavityLight,false)
assert.equal(catalogue.joinHealing.method,'triangular-underlay-with-cabinet-facing-seam-cleanup');assert.deepEqual(catalogue.joinHealing.sharedEdgeX,[336,420]);assert.equal(catalogue.joinHealing.leftAndRightIndependent,true)
assert.deepEqual(catalogue.joinHealing.bodyBackfill.destinationOrigins,[[333,145],[417,145]]);assert.deepEqual(catalogue.joinHealing.triangularSurface.destinationOrigins,[[324,134],[408,134]]);assert.equal(catalogue.joinHealing.triangularSurface.ovenFacingDiagonalRetained,true)
assert.deepEqual(catalogue.joinHealing.cabinetSeamCleanup.destinationOrigins,[[330,134],[420,134]]);assert.equal(catalogue.joinHealing.cabinetSeamCleanup.cabinetFacingDiagonalRetained,false);assert.equal(catalogue.joinHealing.cabinetSeamCleanup.rowColoursFromApprovedV22,true)
assert.deepEqual(catalogue.joinHealing.drawOrder,['room background','active blue body backfill and triangular surface underlay','cabinet neighbours','standalone oven','active cabinet-facing seam cleanup']);assert.equal(catalogue.joinHealing.embeddedInOvenSprite,false);assert.equal(catalogue.joinHealing.embeddedInCabinetSprite,false)
assert.equal(catalogue.lighting.frameCount,40);assert.equal(catalogue.lighting.baseFps,4);assert.equal(catalogue.lighting.durationSeconds,10);assert.deepEqual(catalogue.lighting.speedRange,[0.1,4])

for(const authority of Object.values(catalogue.authorities)){const file=path.join(root,authority.file);assert.ok(fs.existsSync(file),authority.file);assert.equal(sha(file),authority.sha256,`${authority.file} authority drifted`)}
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const file=path.join(raw,name);assert.ok(fs.existsSync(file),name);assert.equal(sha(file),hash);const item=register.publishedAssets.find(entry=>entry.publicAssemblyPath.endsWith(`/assets/${name}`));assert.ok(item,`register missing ${name}`);assert.equal(item.sourceSha256,hash)}
for(const name of [...states,...loops])assert.equal(sha(path.join(raw,name)),sha(path.join(v30Raw,name)),`${name} must remain byte-identical to V30`)
for(const name of states){const image=png(path.join(raw,name));assert.deepEqual([image.width,image.height],[92,85]);for(let y=0;y<85;y++)for(let x=0;x<92;x++)if(x<4||x>=88||y<4||y>=81)assert.equal(image.data[(y*92+x)*4+3],0,`${name} opaque gutter at ${x},${y}`)}

const background=png(path.join(raw,'room-background-exact.png')),cabinet=png(path.join(raw,'cabinet-run-v11-exact.png')),body=png(path.join(raw,'join-body-backfill-template.png')),triangle=png(path.join(raw,'countertop-triangle-underlay-template.png')),leftCleanup=png(path.join(raw,'cabinet-seam-cleanup-left.png')),rightCleanup=png(path.join(raw,'cabinet-seam-cleanup-right.png'))
assert.deepEqual([background.width,background.height],[772,224]);assert.deepEqual([cabinet.width,cabinet.height],[176,82]);assert.deepEqual([body.width,body.height],[14,63]);assert.deepEqual([triangle.width,triangle.height],[24,12]);assert.deepEqual([leftCleanup.width,leftCleanup.height],[6,12]);assert.deepEqual([rightCleanup.width,rightCleanup.height],[6,12])
assert.equal(sha(path.join(raw,'join-body-backfill-template.png')),catalogue.authorities.approvedBodyBackfill.sha256);assert.equal(sha(path.join(raw,'countertop-triangle-underlay-template.png')),catalogue.authorities.approvedCountertopRows.sha256)
for(let y=0;y<12;y++)for(let x=0;x<6;x++){
  const leftActive=y>0||x>=2,rightActive=y>0||x<=4,source=pixel(triangle,0,y)
  assert.equal(pixel(leftCleanup,x,y)[3]>0,leftActive,`left cleanup mask drift at ${x},${y}`);assert.equal(pixel(rightCleanup,x,y)[3]>0,rightActive,`right cleanup mask drift at ${x},${y}`)
  if(leftActive)assert.deepEqual(pixel(leftCleanup,x,y),source);if(rightActive)assert.deepEqual(pixel(rightCleanup,x,y),source)
}

for(const state of ['off','on','broken','broken-cavity-lit','broken-warning-lit','broken-both-lit']){
  const actual=png(path.join(raw,`oven-${state}-native-room.png`)),expected=clone(background),oven=png(path.join(raw,`oven-${state}.png`))
  composite(expected,body,333,145,0,0,6,63);composite(expected,triangle,324,134);composite(expected,body,417,145,0,0,6,63);composite(expected,triangle,408,134);composite(expected,cabinet,164,130);composite(expected,cabinet,416,130);composite(expected,oven,332,127);composite(expected,leftCleanup,330,134);composite(expected,rightCleanup,420,134)
  assert.deepEqual(actual.data,expected.data,`${state} room violates V32 draw order`)
  for(let y=0;y<12;y++)for(let x=0;x<6;x++){
    const la=pixel(leftCleanup,x,y)[3]>0,ra=pixel(rightCleanup,x,y)[3]>0
    if(la)assert.deepEqual(pixel(actual,330+x,134+y),pixel(leftCleanup,x,y),`${state} left cabinet seam remains at ${330+x},${134+y}`)
    if(ra)assert.deepEqual(pixel(actual,420+x,134+y),pixel(rightCleanup,x,y),`${state} right cabinet seam remains at ${420+x},${134+y}`)
    if(la)assert.equal(pixel(oven,330+x-332,134+y-127)[3],0,`${state} left cleanup crosses oven diagonal`)
    if(ra)assert.equal(pixel(oven,420+x-332,134+y-127)[3],0,`${state} right cleanup crosses oven diagonal`)
  }
  for(const [x0,x1] of [[335,337],[419,421]])for(let y=146;y<208;y++)for(let x=x0;x<x1;x++)assert.notDeepEqual(pixel(actual,x,y),pixel(background,x,y),`${state} wall remains visible in body gap at ${x},${y}`)
  const v30=png(path.join(v30Raw,`oven-${state}-native-room.png`));let changed=0
  for(let y=0;y<224;y++)for(let x=0;x<772;x++){const at=(y*772+x)*4;let diff=false;for(let c=0;c<4;c++)diff||=actual.data[at+c]!==v30.data[at+c];if(!diff)continue;const cleanup=((x>=330&&x<336)||(x>=420&&x<426))&&y>=134&&y<146,bodyFill=((x>=333&&x<339)||(x>=417&&x<423))&&y>=145&&y<208;assert.ok(cleanup||bodyFill,`${state} changed outside seam cleanup/body fill at ${x},${y}`);changed++}assert.ok(changed>100,`${state} did not receive V32 healing`)
}

for(const [name,size] of [['oven-v30-triangle-seam-focus.png',[124,90]],['oven-v31-flattened-focus.png',[124,90]],['oven-v32-triangle-clean-focus.png',[124,90]],['oven-v30-protected-dial-focus.png',[22,28]]]){const image=png(path.join(raw,name));assert.deepEqual([image.width,image.height],size)}
const v30=JSON.parse(fs.readFileSync(path.join(root,'art/drafts',v30Batch,'candidate-catalogue.json')));assert.deepEqual(catalogue.states,v30.states);assert.deepEqual(catalogue.lighting,v30.lighting);assert.deepEqual(catalogue.sfxPlaceholders,v30.sfxPlaceholders)
for(const key of ['v30Changed','v31Changed','ovenSpritesChanged','cabinetChanged','v22JoinAuthorityChanged','roomBackgroundChanged','finalChanged','runtimeChanged','promotionPerformed','nextAssetStarted'])assert.equal(catalogue.boundaries[key],false)
const html=fs.readFileSync(path.join(review,'index.html'),'utf8');for(const pattern of [/triangular transition without the cabinet seam/,/drawTriangle/,/cabinet-seam-cleanup-left/,/cabinet-seam-cleanup-right/,/exactLeftAdjacency/,/exactRightAdjacency/,/blue backfill \+ triangle behind → assets → cabinet seam cleanup/,/Promise\.all\(names\.map\(load\)/,/\.decode\(\)/])assert.match(html,pattern);assert.doesNotMatch(html,/clearRect\(/)
assert.match(fs.readFileSync(path.join(root,'next.config.mjs'),'utf8'),/source: '\/keeper-review\/kitchen-oven-standalone-v32'/)
const manifestPath=path.join(root,'review-archive/sets',`${set}.json`);assert.ok(fs.existsSync(manifestPath),'archive manifest missing; run npm run archive:keeper-review:set');const manifest=JSON.parse(fs.readFileSync(manifestPath));assert.equal(Object.keys(manifest.entries).length,Object.keys(catalogue.publishedAssets).length)
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const entry=manifest.entries[`/keeper-review/${set}/assets/${name}`];assert.ok(entry,`archive entry missing ${name}`);assert.equal(entry.sha256,hash);assert.ok(fs.existsSync(path.join(root,entry.object)),`${name} archive object missing`);assert.equal(sha(path.join(root,entry.object)),hash)}
console.log('Kitchen Oven V32 verified: the V30 triangular oven-facing edges remain intact, only cabinet-facing seams are masked, and blue body backfills close both exact snapped gaps.')

#!/usr/bin/env node
/** Verify Oven V28 changes only V27's upper sixteen body rows. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-oven-standalone-v28',batch='kitchen-oven-standalone-2026-10-20-v28',v27Batch='kitchen-oven-standalone-2026-10-19-v27'
const raw=path.join(root,'art/raw',batch),v27Raw=path.join(root,'art/raw',v27Batch),draft=path.join(root,'art/drafts',batch),review=path.join(root,'public/keeper-review',set)
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),png=file=>PNG.sync.read(fs.readFileSync(file))
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),register=JSON.parse(fs.readFileSync(path.join(draft,'batch-register.json')))

assert.equal(catalogue.set,set);assert.equal(catalogue.version,28);assert.equal(catalogue.status,'reversible-unapproved-unpromoted')
assert.equal(catalogue.sources.generationMode,'built-in-imagegen');assert.deepEqual(catalogue.sources.hobSourceWindow,[111,46,710,658])
assert.deepEqual(catalogue.geometry.logicalBodyPixels,[84,77]);assert.deepEqual(catalogue.geometry.cellPixels,[92,85]);assert.deepEqual(catalogue.geometry.transparentGutterPixels,[4,4])
assert.deepEqual(catalogue.geometry.ovenBodyBoundsInRoom,[336,131,84,77]);assert.deepEqual(catalogue.geometry.ovenCellOriginInRoom,[332,127]);assert.deepEqual(catalogue.geometry.primeInteractionAnchor,[378,218])
assert.equal(catalogue.geometry.projection,'cabinet-v11-shallow-straight-on-flat-cutaway');assert.deepEqual(catalogue.geometry.hobReplacementRowsInBody,[0,16]);assert.deepEqual(catalogue.geometry.brokenFixedShelfPatchInBody,[8,26,76,67])
assert.equal(catalogue.geometry.offOnExteriorEnvelopeByteIdentical,true);assert.equal(catalogue.geometry.roomVariantCompositing,'complete-precomposed-room-images-no-canvas-clearRect')
assert.equal(catalogue.lighting.frameCount,40);assert.equal(catalogue.lighting.baseFps,4);assert.equal(catalogue.lighting.durationSeconds,10);assert.deepEqual(catalogue.lighting.speedRange,[0.1,4])
assert.equal(catalogue.lighting.cavityPattern.length,40);assert.equal(catalogue.lighting.warningPattern.length,40)

for(const authority of Object.values(catalogue.authorities)){const file=path.join(root,authority.file);assert.ok(fs.existsSync(file),authority.file);assert.equal(sha(file),authority.sha256,`${authority.file} authority drifted`)}
for(const source of Object.values(catalogue.sources).filter(value=>value&&typeof value==='object'&&value.file)){const file=path.join(root,source.file);assert.ok(fs.existsSync(file),source.file);assert.equal(sha(file),source.sha256,`${source.file} source drifted`)}
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const file=path.join(raw,name);assert.ok(fs.existsSync(file),name);assert.equal(sha(file),hash);const item=register.publishedAssets.find(entry=>entry.publicAssemblyPath.endsWith(`/assets/${name}`));assert.ok(item,`register missing ${name}`);assert.equal(item.sourceSha256,hash)}

const stateNames=['oven-off.png','oven-on.png','oven-broken.png','oven-broken-cavity-lit.png','oven-broken-warning-lit.png','oven-broken-both-lit.png']
const cells=stateNames.map(name=>png(path.join(raw,name))),v27Cells=stateNames.map(name=>png(path.join(v27Raw,name)))
for(let i=0;i<cells.length;i++){
  const image=cells[i],authority=v27Cells[i];assert.deepEqual([image.width,image.height],[92,85]);assert.deepEqual([authority.width,authority.height],[92,85])
  let minX=92,minY=85,maxX=-1,maxY=-1,changedInBand=0,changedInShelf=0
  for(let y=0;y<85;y++)for(let x=0;x<92;x++){
    const at=(y*92+x)*4,a=image.data[at+3],gutter=x<4||x>=88||y<4||y>=81
    if(gutter)assert.equal(a,0,`${stateNames[i]} opaque gutter pixel at ${x},${y}`)
    if(a){minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x);maxY=Math.max(maxY,y)}
    let changed=false;for(let c=0;c<4;c++)changed||=image.data[at+c]!==authority.data[at+c]
    const inHob=y>=4&&y<20,inShelf=i>=2&&x>=12&&x<80&&y>=30&&y<71
    if(changed){assert.ok(inHob||inShelf,`${stateNames[i]} changed outside declared patches at ${x},${y}`);if(inHob)changedInBand++;if(inShelf)changedInShelf++}
  }
  assert.deepEqual([minX,minY,maxX+1,maxY+1],[4,4,88,81],`${stateNames[i]} 84x77 envelope drifted`);assert.ok(changedInBand>100,`${stateNames[i]} did not receive the perspective correction`);if(i>=2)assert.ok(changedInShelf>300,`${stateNames[i]} did not receive the fixed-shelf correction`)
}

for(let y=4;y<20;y++)for(let x=4;x<88;x++){const at=(y*92+x)*4;for(let i=1;i<cells.length;i++)for(let c=0;c<4;c++)assert.equal(cells[i].data[at+c],cells[0].data[at+c],`shared V28 hob differs in ${stateNames[i]} at ${x},${y}`)}
for(let y=0;y<85;y++)for(let x=0;x<92;x++)assert.equal(cells[0].data[(y*92+x)*4+3],cells[1].data[(y*92+x)*4+3],`Off/On alpha envelope differs at ${x},${y}`)

const family=png(path.join(raw,'oven-state-family-strip.png'));assert.deepEqual([family.width,family.height],[276,85])
for(const name of ['oven-broken-cavity-flicker-f40.png','oven-broken-warning-flicker-f40.png']){const strip=png(path.join(raw,name));assert.deepEqual([strip.width,strip.height],[3680,85]);for(let frame=0;frame<40;frame++)for(let y=0;y<85;y++)for(const x of [0,1,2,3,88,89,90,91])assert.equal(strip.data[(y*strip.width+frame*92+x)*4+3],0,`${name} frame ${frame} lost gutter`)}
for(const name of ['oven-v27-perspective-focus.png','oven-v28-perspective-focus.png']){const image=png(path.join(raw,name));assert.deepEqual([image.width,image.height],[172,66])}

const roomNames=['off','on','broken','broken-cavity-lit','broken-warning-lit','broken-both-lit'],rooms=roomNames.map(name=>png(path.join(raw,`oven-${name}-native-room.png`)))
for(const room of rooms)assert.deepEqual([room.width,room.height],[772,224])
for(let i=1;i<rooms.length;i++)for(let y=0;y<224;y++)for(let x=0;x<772;x++){if(x>=336&&x<420&&y>=131&&y<208)continue;const at=(y*772+x)*4;for(let c=0;c<4;c++)assert.equal(rooms[0].data[at+c],rooms[i].data[at+c],`${roomNames[i]} damaged neighbour/background at ${x},${y}`)}
const v27Data=JSON.parse(fs.readFileSync(path.join(root,'art/drafts',v27Batch,'candidate-catalogue.json')));assert.deepEqual(catalogue.states,v27Data.states);assert.deepEqual(catalogue.lighting.cavityPattern,v27Data.lighting.cavityPattern);assert.deepEqual(catalogue.lighting.warningPattern,v27Data.lighting.warningPattern);assert.deepEqual(catalogue.sfxPlaceholders,v27Data.sfxPlaceholders)
for(const key of ['v27StateFamilyChangedOutsideDeclaredPatches','approvedCabinetChanged','roomBackgroundChanged','finalChanged','runtimeChanged','promotionPerformed','nextAssetStarted'])assert.equal(catalogue.boundaries[key],false)

const html=fs.readFileSync(path.join(review,'index.html'),'utf8');for(const pattern of [/Standalone oven · shallow cabinet-matched hob/,/Perspective correction · 4× native pixels/,/Only the upper sixteen native body rows and the declared Broken cavity\/door patch may change/,/Broken dish on fixed shelf/,/Promise\.all\(names\.map\(load\)/,/\.decode\(\)/])assert.match(html,pattern);assert.doesNotMatch(html,/clearRect\(/)
assert.match(fs.readFileSync(path.join(root,'next.config.mjs'),'utf8'),/source: '\/keeper-review\/kitchen-oven-standalone-v28'/)
const manifestPath=path.join(root,'review-archive/sets',`${set}.json`);assert.ok(fs.existsSync(manifestPath),'archive manifest missing; run npm run archive:keeper-review:set');const manifest=JSON.parse(fs.readFileSync(manifestPath));assert.equal(Object.keys(manifest.entries).length,Object.keys(catalogue.publishedAssets).length)
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const entry=manifest.entries[`/keeper-review/${set}/assets/${name}`];assert.ok(entry,`archive entry missing ${name}`);assert.equal(entry.sha256,hash);assert.ok(fs.existsSync(path.join(root,entry.object)),`${name} archive object missing`);assert.equal(sha(path.join(root,entry.object)),hash)}
console.log('Kitchen Oven V28 verified: only the shallow-hob and Broken fixed-shelf patches changed; lighting, envelope, room joins and Prime anchor remain exact.')

#!/usr/bin/env node
/** Verify Oven V29 changes only V28's Broken fixed-shelf patch. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-oven-standalone-v29',batch='kitchen-oven-standalone-2026-10-20-v29',v28Batch='kitchen-oven-standalone-2026-10-20-v28'
const raw=path.join(root,'art/raw',batch),v28Raw=path.join(root,'art/raw',v28Batch),draft=path.join(root,'art/drafts',batch),review=path.join(root,'public/keeper-review',set)
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),png=file=>PNG.sync.read(fs.readFileSync(file))
const catalogue=JSON.parse(fs.readFileSync(path.join(draft,'candidate-catalogue.json'))),register=JSON.parse(fs.readFileSync(path.join(draft,'batch-register.json')))

assert.equal(catalogue.set,set);assert.equal(catalogue.version,29);assert.equal(catalogue.status,'reversible-unapproved-unpromoted')
assert.equal(catalogue.sources.generationMode,'built-in-imagegen');assert.deepEqual(catalogue.sources.fixedShelfSourceWindow,[1451,35,2058,698])
assert.deepEqual(catalogue.geometry.logicalBodyPixels,[84,77]);assert.deepEqual(catalogue.geometry.cellPixels,[92,85]);assert.deepEqual(catalogue.geometry.transparentGutterPixels,[4,4])
assert.deepEqual(catalogue.geometry.ovenBodyBoundsInRoom,[336,131,84,77]);assert.deepEqual(catalogue.geometry.ovenCellOriginInRoom,[332,127]);assert.deepEqual(catalogue.geometry.primeInteractionAnchor,[378,218])
assert.equal(catalogue.geometry.projection,'cabinet-v11-shallow-straight-on-flat-cutaway');assert.deepEqual(catalogue.geometry.brokenFixedShelfPatchInBody,[14,35,70,51]);assert.equal(catalogue.geometry.brokenShelfAlignment,'roast-top-matches-on-state-with-lower-tray-occluded-by-door');assert.deepEqual(catalogue.geometry.brokenDarkPatchRgbScale,[0.33,0.39,0.6])
assert.equal(catalogue.geometry.offOnExteriorEnvelopeByteIdentical,true);assert.equal(catalogue.geometry.roomVariantCompositing,'complete-precomposed-room-images-no-canvas-clearRect')
assert.equal(catalogue.lighting.frameCount,40);assert.equal(catalogue.lighting.baseFps,4);assert.equal(catalogue.lighting.durationSeconds,10);assert.deepEqual(catalogue.lighting.speedRange,[0.1,4])
assert.equal(catalogue.lighting.cavityPattern.length,40);assert.equal(catalogue.lighting.warningPattern.length,40)

for(const authority of Object.values(catalogue.authorities)){const file=path.join(root,authority.file);assert.ok(fs.existsSync(file),authority.file);assert.equal(sha(file),authority.sha256,`${authority.file} authority drifted`)}
for(const source of Object.values(catalogue.sources).filter(value=>value&&typeof value==='object'&&value.file)){const file=path.join(root,source.file);assert.ok(fs.existsSync(file),source.file);assert.equal(sha(file),source.sha256,`${source.file} source drifted`)}
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const file=path.join(raw,name);assert.ok(fs.existsSync(file),name);assert.equal(sha(file),hash);const item=register.publishedAssets.find(entry=>entry.publicAssemblyPath.endsWith(`/assets/${name}`));assert.ok(item,`register missing ${name}`);assert.equal(item.sourceSha256,hash)}

const stateNames=['oven-off.png','oven-on.png','oven-broken.png','oven-broken-cavity-lit.png','oven-broken-warning-lit.png','oven-broken-both-lit.png']
const cells=stateNames.map(name=>png(path.join(raw,name))),v28Cells=stateNames.map(name=>png(path.join(v28Raw,name)))
for(let i=0;i<cells.length;i++){
  const image=cells[i],authority=v28Cells[i];assert.deepEqual([image.width,image.height],[92,85]);assert.deepEqual([authority.width,authority.height],[92,85])
  let minX=92,minY=85,maxX=-1,maxY=-1,changedInShelf=0
  for(let y=0;y<85;y++)for(let x=0;x<92;x++){
    const at=(y*92+x)*4,a=image.data[at+3],gutter=x<4||x>=88||y<4||y>=81
    if(gutter)assert.equal(a,0,`${stateNames[i]} opaque gutter pixel at ${x},${y}`)
    if(a){minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x);maxY=Math.max(maxY,y)}
    let changed=false;for(let c=0;c<4;c++)changed||=image.data[at+c]!==authority.data[at+c]
    const inShelf=i>=2&&x>=18&&x<74&&y>=39&&y<55
    if(changed){assert.ok(inShelf,`${stateNames[i]} changed outside declared Broken shelf patch at ${x},${y}`);changedInShelf++}
  }
  assert.deepEqual([minX,minY,maxX+1,maxY+1],[4,4,88,81],`${stateNames[i]} 84x77 envelope drifted`);if(i<2)assert.equal(changedInShelf,0,`${stateNames[i]} must remain byte-identical to V28`);else assert.ok(changedInShelf>100,`${stateNames[i]} did not receive the lowered fixed-shelf correction`)
}

for(let y=4;y<20;y++)for(let x=4;x<88;x++){const at=(y*92+x)*4;for(let i=1;i<cells.length;i++)for(let c=0;c<4;c++)assert.equal(cells[i].data[at+c],cells[0].data[at+c],`shared V29 hob differs in ${stateNames[i]} at ${x},${y}`)}
for(let y=0;y<85;y++)for(let x=0;x<92;x++)assert.equal(cells[0].data[(y*92+x)*4+3],cells[1].data[(y*92+x)*4+3],`Off/On alpha envelope differs at ${x},${y}`)

const family=png(path.join(raw,'oven-state-family-strip.png'));assert.deepEqual([family.width,family.height],[276,85])
for(const name of ['oven-broken-cavity-flicker-f40.png','oven-broken-warning-flicker-f40.png']){const strip=png(path.join(raw,name));assert.deepEqual([strip.width,strip.height],[3680,85]);for(let frame=0;frame<40;frame++)for(let y=0;y<85;y++)for(const x of [0,1,2,3,88,89,90,91])assert.equal(strip.data[(y*strip.width+frame*92+x)*4+3],0,`${name} frame ${frame} lost gutter`)}
for(const name of ['oven-v28-shelf-focus.png','oven-v29-shelf-focus.png']){const image=png(path.join(raw,name));assert.deepEqual([image.width,image.height],[72,45])}

const roomNames=['off','on','broken','broken-cavity-lit','broken-warning-lit','broken-both-lit'],rooms=roomNames.map(name=>png(path.join(raw,`oven-${name}-native-room.png`)))
for(const room of rooms)assert.deepEqual([room.width,room.height],[772,224])
for(let i=1;i<rooms.length;i++)for(let y=0;y<224;y++)for(let x=0;x<772;x++){if(x>=336&&x<420&&y>=131&&y<208)continue;const at=(y*772+x)*4;for(let c=0;c<4;c++)assert.equal(rooms[0].data[at+c],rooms[i].data[at+c],`${roomNames[i]} damaged neighbour/background at ${x},${y}`)}
const v28Data=JSON.parse(fs.readFileSync(path.join(root,'art/drafts',v28Batch,'candidate-catalogue.json')));assert.deepEqual(catalogue.states,v28Data.states);assert.deepEqual(catalogue.lighting.cavityPattern,v28Data.lighting.cavityPattern);assert.deepEqual(catalogue.lighting.warningPattern,v28Data.lighting.warningPattern);assert.deepEqual(catalogue.sfxPlaceholders,v28Data.sfxPlaceholders)
for(const key of ['v28StateFamilyChangedOutsideDeclaredPatch','approvedCabinetChanged','roomBackgroundChanged','finalChanged','runtimeChanged','promotionPerformed','nextAssetStarted'])assert.equal(catalogue.boundaries[key],false)

const html=fs.readFileSync(path.join(review,'index.html'),'utf8');for(const pattern of [/Standalone oven · corrected Broken shelf height/,/Broken shelf correction · 4× native pixels/,/Only the declared Broken cavity\/door patch may change/,/When the smoke is added/,/asset-first effects workbench/,/Promise\.all\(names\.map\(load\)/,/\.decode\(\)/])assert.match(html,pattern);assert.doesNotMatch(html,/clearRect\(/)
assert.match(fs.readFileSync(path.join(root,'next.config.mjs'),'utf8'),/source: '\/keeper-review\/kitchen-oven-standalone-v29'/)
const manifestPath=path.join(root,'review-archive/sets',`${set}.json`);assert.ok(fs.existsSync(manifestPath),'archive manifest missing; run npm run archive:keeper-review:set');const manifest=JSON.parse(fs.readFileSync(manifestPath));assert.equal(Object.keys(manifest.entries).length,Object.keys(catalogue.publishedAssets).length)
for(const [name,hash] of Object.entries(catalogue.publishedAssets)){const entry=manifest.entries[`/keeper-review/${set}/assets/${name}`];assert.ok(entry,`archive entry missing ${name}`);assert.equal(entry.sha256,hash);assert.ok(fs.existsSync(path.join(root,entry.object)),`${name} archive object missing`);assert.equal(sha(path.join(root,entry.object)),hash)}
console.log('Kitchen Oven V29 verified: Off and On remain byte-identical to V28; only the Broken fixed-shelf patch changed; lighting, envelope, room joins and Prime anchor remain exact.')

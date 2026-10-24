#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import { PNG } from 'pngjs'
const json=file=>JSON.parse(fs.readFileSync(file,'utf8')), hashBytes=bytes=>crypto.createHash('sha256').update(bytes).digest('hex'), hash=file=>hashBytes(fs.readFileSync(file))
const record=json('data/kitchen_room_layout_review_v6.json'), register=json(record.nativeAssets.register), v4=json('art/drafts/kitchen-room-layout-review-2026-10-24-v4/native-assets/extraction-register.json')
const page=fs.readFileSync('public/keeper-review/kitchen-room-layout-v6/index.html','utf8'), route=fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v6/route.ts','utf8'), archiveRoute=fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts','utf8')
assert.equal(hash(record.nativeAssets.register),record.nativeAssets.registerSha256)
assert.equal(hash(register.sources.loose.file),register.sources.loose.sha256)
assert.equal(hash(register.sources.furniture.file),register.sources.furniture.sha256)
assert.equal(hash('public/sprites/room_kitchen.png'),'c1cb3c90b911ea09ae13d8fd09297787b990b0997dc589fb9e6a62c658099eff')
for(const [version,expected] of Object.entries({v1:'3638a275b375ce8731aa4b924522f8f37f44f453044ab9a7c4ca68644d3c25b6',v2:'e9d9d5031961365dfb28ab89ca80ded68f30c34b1a389409d637353da69fddc2',v3:'2fb71a7db5f0a87da27ee4f3555e03688622ab90d14a0536215e0ca081e944e8',v4:'09041a86287b8d34cf4a1938a0c5a571f9540e318a22c2bd68540e35b42399a5',v5:'7e2855e17986b3283067de270869053d3507c6586fcf4151a6cc6dcca48112be'}))assert.equal(hash(`public/keeper-review/kitchen-room-layout-${version}/index.html`),expected,`${version} page changed`)
assert.equal(register.schema,'lighthouse-keeper/kitchen-native-assets@6')
for(const key of ['scaleApplied','downscalingApplied','resamplingApplied','colourTransformApplied'])assert.equal(register[key],false)
assert.equal(register.placement.furnitureAnchorPaces,16)
assert.equal(register.placement.chairDepthOffsetPixels,24)
assert.deepEqual(register.placement.furnitureLayerOrder,['table','rear-seated-keeper','chair'])
assert.equal(record.boundary.runtimeChanged,false);assert.equal(record.boundary.gameplayChanged,false);assert.equal(record.boundary.approvedFittedUnitsChanged,false)
const pngs={}
for(const [id,output] of Object.entries(register.outputs)){const bytes=fs.readFileSync(output.file);assert.equal(hashBytes(bytes),output.sha256,`${id} hash changed`);const png=PNG.sync.read(bytes);pngs[id]=png;assert.deepEqual([png.width,png.height],output.dimensions)}
for(const id of ['fitted-units-static','fitted-overlay-on','fitted-overlay-broken','dishwasher-warning-1','dishwasher-warning-2','dishwasher-warning-3','oven-broken-cavity-light','broken-floor-water'])assert.equal(register.outputs[id].sha256,v4.outputs[id].sha256,`${id} differs from locked V4`)
assert.equal(register.outputs['fitted-units-static'].sha256,'ba84022371aea330e2fe50e5ad8fb37bf9d210aa1e09649d7f2fc69f460f49b1')
const looseIds=['toaster-off','toaster-on','toaster-broken','kettle-off','kettle-on','kettle-broken','bin-standard','bin-broken','bowl-standard','bowl-broken','table-standard','chair-standard']
for(const id of looseIds){const png=pngs[id];assert.equal(register.outputs[id].contactShadowIncluded,false,`${id} must be shadowless`);assert.equal(register.outputs[id].downscalingApplied,false);for(let inset=0;inset<8;inset++){for(let x=0;x<png.width;x++){assert.equal(png.data[(inset*png.width+x)*4+3],0);assert.equal(png.data[((png.height-1-inset)*png.width+x)*4+3],0)}for(let y=0;y<png.height;y++){assert.equal(png.data[(y*png.width+inset)*4+3],0);assert.equal(png.data[(y*png.width+png.width-1-inset)*4+3],0)}}}
assert.equal(register.outputs['kettle-off'].sha256,register.outputs['kettle-on'].sha256)
assert.deepEqual(register.globalStateMap.on,{toaster:'on',kettle:'on',bin:'standard',bowl:'standard'})
for(const required of ["const ROOT='/keeper-review/kitchen-room-layout-v6/assets/'",'FLOOR_CENTRES=[114,1710,1824,1938]',"floor:{bin:0,table:2,chair:2}",'.asset.table{z-index:3}',"name==='chair'?FLOOR_Y+24:FLOOR_Y","i.style.top=(FLOOR_Y+24-KEEPER_H)+'px'",'id="showSeat" type="checkbox" checked','id="primeScale" class="primeScale" hidden'])assert.ok(page.includes(required),`V6 page missing ${required}`)
assert.ok(route.includes('/keeper-review/kitchen-room-layout-v6/index.html'));assert.ok(archiveRoute.includes("'kitchen-room-layout-v6'"))
const archive=json('review-archive/index.json'), expected=[['prime-keeper-neutral-native-256x320.png',register.keeperPresentation.neutral.sha256],['prime-keeper-seated-back-native-256x320.png',register.keeperPresentation.seated.sha256],...Object.values(register.outputs).map(output=>[output.publicReviewFile.split('/').pop(),output.sha256])]
for(const [asset,expectedHash] of expected){const pathname=`/keeper-review/kitchen-room-layout-v6/assets/${asset}`,entry=archive.legacyPaths[pathname];assert.ok(entry,`${pathname} not archived`);assert.equal(entry.sha256,expectedHash);assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//,'')}`),true);assert.equal(fs.existsSync(`public${pathname}`),false)}
console.log('Kitchen room layout review V6 verified: shadowless loose assets, pace-16 table, rear-seat depth stack and locked fitted base.')

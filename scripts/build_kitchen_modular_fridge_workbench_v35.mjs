#!/usr/bin/env node
/** Build V35: coordinated current-geometry fridge inside the approved workbench. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-modular-fridge-workbench-v35',batch='kitchen-modular-fridge-workbench-2026-10-20-v35'
const raw=path.join(root,'art/raw',batch),draft=path.join(root,'art/drafts',batch),review=path.join(root,'public/keeper-review',set)
const template=path.join(root,'scripts/templates/kitchen_modular_fridge_workbench_v35.html')
const v33Raw=path.join(root,'art/raw/kitchen-modular-join-workbench-2026-10-20-v33')
const v33Catalogue=path.join(root,'art/drafts/kitchen-modular-join-workbench-2026-10-20-v33/candidate-catalogue.json')
const v33Approval=path.join(root,'docs/review/kitchen-modular-join-workbench-v33-approval-2026-10-20.json')
const v34Rejection=path.join(root,'docs/review/kitchen-modular-fridge-workbench-v34-rejection-2026-10-20.json')
const provenance=path.join(draft,'generation-provenance.json')
const shared=['room-background-exact.png','cabinet-run-v11-exact.png','sink-cabinet-v19-exact.png','join-body-backfill-template.png','countertop-join-cap-template.png','countertop-triangle-underlay-template.png','neighbour-seam-cleanup-left.png','neighbour-seam-cleanup-right.png','oven-off.png','oven-on.png','oven-broken.png','oven-broken-cavity-lit.png','oven-broken-warning-lit.png','oven-broken-both-lit.png','oven-broken-cavity-flicker-f40.png','oven-broken-warning-flicker-f40.png']
const fridge=['fridge-standard.png','fridge-broken-hinge-failed.png','fx-fridge-drip-ripple-f40.png']
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),read=file=>PNG.sync.read(fs.readFileSync(file)),clone=image=>PNG.sync.read(PNG.sync.write(image))
const copy=(source,name=path.basename(source))=>{const file=path.join(raw,name);fs.copyFileSync(source,file);return file},write=(image,name)=>{const file=path.join(raw,name);fs.writeFileSync(file,PNG.sync.write(image));return file}
function composite(dst,src,dx,dy,sx=0,sy=0,w=src.width,h=src.height){for(let y=0;y<h;y++)for(let x=0;x<w;x++){if(dx+x<0||dy+y<0||dx+x>=dst.width||dy+y>=dst.height)continue;const si=((sy+y)*src.width+sx+x)*4,di=((dy+y)*dst.width+dx+x)*4,a=src.data[si+3]/255,da=dst.data[di+3]/255,oa=a+da*(1-a);if(!oa)continue;for(let c=0;c<3;c++)dst.data[di+c]=Math.round((src.data[si+c]*a+dst.data[di+c]*da*(1-a))/oa);dst.data[di+3]=Math.round(oa*255)}}
function clear(image,x,y,w,h){for(let yy=Math.max(0,y);yy<Math.min(image.height,y+h);yy++)for(let xx=Math.max(0,x);xx<Math.min(image.width,x+w);xx++)for(let c=0;c<4;c++)image.data[(yy*image.width+xx)*4+c]=0}
function correctedSink(sink,cabinet){const out=clone(sink);clear(out,0,26,12,82);composite(out,cabinet,0,26,0,0,12,82);return out}
function entities(pos){return[{id:'cabinet',kind:'cabinet',x:168,w:168},...['sink','oven','fridge'].map(id=>({id,kind:id,x:pos[id],w:84}))].sort((a,b)=>a.x-b.x)}
function joinMethod(a,b){if(a.kind==='oven'||b.kind==='oven')return'oven-triangle';return'flat-v22'}
function joins(pos){const e=entities(pos),out=[];for(let i=0;i<e.length-1;i++)if(e[i].x+e[i].w===e[i+1].x)out.push({left:e[i],right:e[i+1],edge:e[i+1].x,method:joinMethod(e[i],e[i+1])});return out.filter(j=>j.method!=='none')}

for(const file of [template,v33Catalogue,v33Approval,v34Rejection,provenance,...shared.map(n=>path.join(v33Raw,n)),...fridge.map(n=>path.join(raw,n))])if(!fs.existsSync(file))throw new Error(`Missing authority: ${file}`)
fs.mkdirSync(draft,{recursive:true});for(const item of fs.readdirSync(draft))if(item!=='generation-provenance.json')fs.rmSync(path.join(draft,item),{recursive:true,force:true});fs.mkdirSync(review,{recursive:true});for(const item of fs.readdirSync(review))fs.rmSync(path.join(review,item),{recursive:true,force:true});fs.mkdirSync(raw,{recursive:true})
const outputs=[];for(const name of shared)outputs.push(copy(path.join(v33Raw,name)));for(const name of fridge)outputs.push(path.join(raw,name))
const I=Object.fromEntries([...shared,...fridge].map(name=>[name,read(path.join(raw,name))]));I.correctedSink=correctedSink(I['sink-cabinet-v19-exact.png'],I['cabinet-run-v11-exact.png'])
function roomProof(fridgeState='standard',pos={fridge:84,oven:336,sink:420}){const room=clone(I['room-background-exact.png']),js=joins(pos);for(const j of js){composite(room,I['join-body-backfill-template.png'],j.edge-3,145,0,0,6,63);if(j.method==='oven-triangle')composite(room,I['countertop-triangle-underlay-template.png'],j.edge-12,134)}composite(room,I['cabinet-run-v11-exact.png'],164,130);const sinkHasLeft=entities(pos).some(e=>e.id!=='sink'&&e.x+e.w===pos.sink);composite(room,sinkHasLeft?I['sink-cabinet-v19-exact.png']:I.correctedSink,pos.sink-4,104);composite(room,I['oven-off.png'],pos.oven-4,127);composite(room,I[fridgeState==='broken'?'fridge-broken-hinge-failed.png':'fridge-standard.png'],pos.fridge-30,130);for(const j of js){if(j.method==='flat-v22')composite(room,I['countertop-join-cap-template.png'],j.edge-8,134,0,0,16,12);else if(j.method==='oven-triangle')composite(room,I[j.left.kind==='oven'?'neighbour-seam-cleanup-right.png':'neighbour-seam-cleanup-left.png'],j.left.kind==='oven'?j.edge:j.edge-6,134)}return room}
outputs.push(write(roomProof('standard'),'fridge-standard-native-room.png'));outputs.push(write(roomProof('broken'),'fridge-broken-native-room.png'));outputs.push(write(roomProof('standard',{fridge:504,oven:336,sink:420}),'cabinet-oven-sink-fridge-native-room.png'))
const v33=JSON.parse(fs.readFileSync(v33Catalogue,'utf8')),publishedAssets=Object.fromEntries(outputs.map(file=>[path.basename(file),sha(file)]))
const catalogue={
  schema:'lighthouse-keeper/kitchen-modular-fridge-workbench@1',set,version:35,status:'reversible-unapproved-unpromoted',
  authorities:{v33Approval:{file:path.relative(root,v33Approval),sha256:sha(v33Approval)},v33Catalogue:{file:path.relative(root,v33Catalogue),sha256:sha(v33Catalogue)},v34Rejection:{file:path.relative(root,v34Rejection),sha256:sha(v34Rejection)},generationProvenance:{file:path.relative(root,provenance),sha256:sha(provenance)}},
  grid:{...v33.grid,defaultFridgeOriginX:84,threeMovableAssets:true},
  assets:{...v33.assets,fridge:{bodyPixels:[84,74],roomBodyBounds:[0,134,84,208],cellPixels:[144,90],cellOffset:[-30,-4],states:['standard','broken'],standardOpaqueBounds:[27,1,114,82],brokenOpaqueBounds:[27,1,118,87],brokenOverflowPixels:{left:3,right:4,maximumAllowed:4},staticPoolIncludedInBroken:true,effect:{file:'fx-fridge-drip-ripple-f40.png',cellPixels:[144,90],frames:40,fps:4,durationSeconds:10,separate:true,removable:true,speedRange:[0.1,4]},sfxCues:['kitchen_fridge_low_electrical_buzz_loop','kitchen_fridge_water_drip_slow']}},
  snapContract:{...v33.snapContract,allThreeAssetsCanBeAdjacent:true,eachAssetExcludesBothOtherOccupiedOrigins:true},
  joinResolver:{...v33.joinResolver,precedence:['pair containing oven → V32 triangular join','every other adjacent pair, including every fridge pair → exact V22 flat join','unjoined sink left edge → V25 cutout rounded end','unjoined oven or fridge edge → native finished end'],fridgePair:{backgroundLayer:'six-pixel V22 cabinet-blue body backfill',foregroundLayer:'exact sixteen-pixel V22 countertop cap',reason:'the fridge worktop must become one continuous slab with either neighbour in every legal slot'},drawOrder:['room background','all active body backfills and oven triangular underlays','fixed cabinet, sink, oven and fridge layers','V22 flat caps and V32 neighbour-side cleanup masks','separate removable fridge drip/ripple layer']},
  sources:{generationMode:'fresh-coordinated-imagegen-family-plus-deterministic-native-registration',fridgePixelsByteIdenticalToV39:false,v33PixelsByteIdenticalToApprovedWorkbench:true,imageGenerationUsedForV35:true},publishedAssets,
  boundaries:{v33Changed:false,v34Changed:false,fridgeSpritesChanged:true,sinkSpriteChanged:false,ovenSpritesChanged:false,cabinetChanged:false,roomBackgroundChanged:false,finalChanged:false,runtimeChanged:false,promotionPerformed:false,nextAssetStarted:false},
}
const catalogueFile=path.join(draft,'candidate-catalogue.json');fs.writeFileSync(catalogueFile,JSON.stringify(catalogue,null,2)+'\n')
const shell=path.join(review,'index.html');fs.writeFileSync(shell,fs.readFileSync(template,'utf8').replace('__DATA__',JSON.stringify(catalogue)))
const register={schema:'lighthouse-keeper/reversible-review-batch@1',set,status:'reversible-unapproved-unpromoted',candidate:{catalogue:{file:path.relative(root,catalogueFile),sha256:sha(catalogueFile)},publicShell:{file:path.relative(root,shell),sha256:sha(shell)}},sources:[v33Approval,v33Catalogue,v34Rejection,provenance].map(file=>({file:path.relative(root,file),sha256:sha(file)})),publishedAssets:outputs.map(file=>({source:path.relative(root,file),sourceSha256:sha(file),publicAssemblyPath:path.posix.join('public/keeper-review',set,'assets',path.basename(file))}))}
fs.writeFileSync(path.join(draft,'batch-register.json'),JSON.stringify(register,null,2)+'\n')
console.log('Built Kitchen Modular Fridge Workbench V35: current-geometry fridge plus exact all-location countertop healing')

#!/usr/bin/env node
/** Build V33: one movable sink-and-oven snap/healing workbench. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-modular-join-workbench-v33',batch='kitchen-modular-join-workbench-2026-10-20-v33'
const raw=path.join(root,'art/raw',batch),draft=path.join(root,'art/drafts',batch),review=path.join(root,'public/keeper-review',set)
const template=path.join(root,'scripts/templates/kitchen_modular_join_workbench_v33.html')
const v22Raw=path.join(root,'art/raw/kitchen-countertop-join-cap-2026-10-19-v22')
const v22Approval=path.join(root,'docs/review/kitchen-countertop-join-cap-v22-approval-2026-10-19.json')
const v25Catalogue=path.join(root,'art/drafts/kitchen-exposed-end-cutout-2026-10-19-v25/candidate-catalogue.json')
const v32Raw=path.join(root,'art/raw/kitchen-oven-standalone-2026-10-20-v32')
const v32Catalogue=path.join(root,'art/drafts/kitchen-oven-standalone-2026-10-20-v32/candidate-catalogue.json')
const ovenStates=['oven-off.png','oven-on.png','oven-broken.png','oven-broken-cavity-lit.png','oven-broken-warning-lit.png','oven-broken-both-lit.png']
const ovenLoops=['oven-broken-cavity-flicker-f40.png','oven-broken-warning-flicker-f40.png']
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const read=file=>PNG.sync.read(fs.readFileSync(file)),clone=image=>PNG.sync.read(PNG.sync.write(image))
const copy=(source,name=path.basename(source))=>{const file=path.join(raw,name);fs.copyFileSync(source,file);return file}
const write=(image,name)=>{const file=path.join(raw,name);fs.writeFileSync(file,PNG.sync.write(image));return file}

function composite(dst,src,dx,dy,sx=0,sy=0,w=src.width,h=src.height,opacity=1){
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
    if(dx+x<0||dy+y<0||dx+x>=dst.width||dy+y>=dst.height)continue
    const si=((sy+y)*src.width+sx+x)*4,di=((dy+y)*dst.width+dx+x)*4,a=src.data[si+3]/255*opacity,da=dst.data[di+3]/255,oa=a+da*(1-a)
    if(!oa)continue
    for(let c=0;c<3;c++)dst.data[di+c]=Math.round((src.data[si+c]*a+dst.data[di+c]*da*(1-a))/oa)
    dst.data[di+3]=Math.round(oa*255)
  }
}
function clear(image,x,y,w,h){for(let yy=Math.max(0,y);yy<Math.min(image.height,y+h);yy++)for(let xx=Math.max(0,x);xx<Math.min(image.width,x+w);xx++)for(let c=0;c<4;c++)image.data[(yy*image.width+xx)*4+c]=0}
function crop(image,x,y,w,h){const out=new PNG({width:w,height:h});for(let yy=0;yy<h;yy++)for(let xx=0;xx<w;xx++){const si=((y+yy)*image.width+x+xx)*4,di=(yy*w+xx)*4;for(let c=0;c<4;c++)out.data[di+c]=image.data[si+c]}return out}
function correctedSink(sink,cabinet){const out=clone(sink);clear(out,0,26,12,82);composite(out,cabinet,0,26,0,0,12,82);return out}
function entities(sinkX,ovenX){return[{id:'cabinet',kind:'cabinet',x:168,w:168},{id:'sink',kind:'sink',x:sinkX,w:84},{id:'oven',kind:'oven',x:ovenX,w:84}].sort((a,b)=>a.x-b.x)}
function joins(sinkX,ovenX){const e=entities(sinkX,ovenX),out=[];for(let i=0;i<e.length-1;i++)if(e[i].x+e[i].w===e[i+1].x)out.push({left:e[i],right:e[i+1],edge:e[i+1].x,method:e[i].kind==='oven'||e[i+1].kind==='oven'?'oven-triangle':'flat-v22'});return out}
function composeRoom({sinkX,ovenX,ovenName='oven-off.png',heal=true}){
  const room=clone(images.background),js=heal?joins(sinkX,ovenX):[]
  for(const j of js){composite(room,images.body,j.edge-3,145,0,0,6,63);if(j.method==='oven-triangle')composite(room,images.triangle,j.edge-12,134);}
  composite(room,images.cabinet,164,130)
  const sinkHasLeft=entities(sinkX,ovenX).some(e=>e.id!=='sink'&&e.x+e.w===sinkX)
  composite(room,heal&&!sinkHasLeft?images.correctedSink:images.sink,sinkX-4,104)
  composite(room,images[ovenName],ovenX-4,127)
  for(const j of js){if(j.method==='flat-v22')composite(room,images.flat,j.edge-8,134,0,0,16,12);else if(j.left.kind==='oven')composite(room,images.cleanupRight,j.edge,134);else composite(room,images.cleanupLeft,j.edge-6,134)}
  return room
}

const required=[template,v22Approval,v25Catalogue,v32Catalogue,...['room-background-exact.png','cabinet-run-v11-exact.png','sink-cabinet-v19-exact.png','join-body-backfill-template.png','countertop-join-cap-template.png'].map(n=>path.join(v22Raw,n)),...['countertop-triangle-underlay-template.png','cabinet-seam-cleanup-left.png','cabinet-seam-cleanup-right.png',...ovenStates,...ovenLoops].map(n=>path.join(v32Raw,n))]
for(const file of required)if(!fs.existsSync(file))throw new Error(`Missing authority: ${file}`)
for(const dir of [raw,draft,review]){fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir,{recursive:true})}

const outputs=[]
for(const [source,name] of [
  [path.join(v22Raw,'room-background-exact.png'),'room-background-exact.png'],[path.join(v22Raw,'cabinet-run-v11-exact.png'),'cabinet-run-v11-exact.png'],[path.join(v22Raw,'sink-cabinet-v19-exact.png'),'sink-cabinet-v19-exact.png'],[path.join(v22Raw,'join-body-backfill-template.png'),'join-body-backfill-template.png'],[path.join(v22Raw,'countertop-join-cap-template.png'),'countertop-join-cap-template.png'],[path.join(v32Raw,'countertop-triangle-underlay-template.png'),'countertop-triangle-underlay-template.png'],[path.join(v32Raw,'cabinet-seam-cleanup-left.png'),'neighbour-seam-cleanup-left.png'],[path.join(v32Raw,'cabinet-seam-cleanup-right.png'),'neighbour-seam-cleanup-right.png'],...ovenStates.map(n=>[path.join(v32Raw,n),n]),...ovenLoops.map(n=>[path.join(v32Raw,n),n])
])outputs.push(copy(source,name))

const images={background:read(path.join(v22Raw,'room-background-exact.png')),cabinet:read(path.join(v22Raw,'cabinet-run-v11-exact.png')),sink:read(path.join(v22Raw,'sink-cabinet-v19-exact.png')),body:read(path.join(v22Raw,'join-body-backfill-template.png')),flat:read(path.join(v22Raw,'countertop-join-cap-template.png')),triangle:read(path.join(v32Raw,'countertop-triangle-underlay-template.png')),cleanupLeft:read(path.join(v32Raw,'cabinet-seam-cleanup-left.png')),cleanupRight:read(path.join(v32Raw,'cabinet-seam-cleanup-right.png'))}
for(const name of ovenStates)images[name]=read(path.join(v32Raw,name))
images.correctedSink=correctedSink(images.sink,images.cabinet)
if(images.background.width!==772||images.background.height!==224||images.cabinet.width!==176||images.cabinet.height!==82||images.sink.width!==92||images.sink.height!==108)throw new Error('Approved room/cabinet/sink geometry drifted')

const ovenThenSink=composeRoom({ovenX:336,sinkX:420}),sinkThenOven=composeRoom({sinkX:336,ovenX:420})
outputs.push(write(ovenThenSink,'oven-then-sink-native-room.png'));outputs.push(write(sinkThenOven,'sink-then-oven-native-room.png'))
outputs.push(write(crop(ovenThenSink,316,126,208,90),'oven-then-sink-join-focus.png'));outputs.push(write(crop(sinkThenOven,316,126,208,90),'sink-then-oven-join-focus.png'))

const v32=JSON.parse(fs.readFileSync(v32Catalogue,'utf8')),publishedAssets=Object.fromEntries(outputs.map(file=>[path.basename(file),sha(file)]))
const catalogue={
  schema:'lighthouse-keeper/kitchen-modular-join-workbench@1',set,version:33,status:'reversible-unapproved-unpromoted',
  authorities:{v22Approval:{file:path.relative(root,v22Approval),sha256:sha(v22Approval)},v25Catalogue:{file:path.relative(root,v25Catalogue),sha256:sha(v25Catalogue)},v32Catalogue:{file:path.relative(root,v32Catalogue),sha256:sha(v32Catalogue)}},
  grid:{originX:84,bayWidthPixels:84,slotOriginsX:[84,168,252,336,420,504],freeOriginsX:[84,336,420,504],fixedCabinetOriginsX:[168,252],primeStopTurnY:218,defaultSinkOriginX:420,defaultOvenOriginX:336,overlapAllowed:false},
  assets:{cabinet:{bodyPixels:[168,74],cellPixels:[176,82],cellOrigin:[164,130]},sink:{bodyPixels:[84,74],cellPixels:[92,108],cellOffset:[-4,-30]},oven:{bodyPixels:[84,77],cellPixels:[92,85],cellOffset:[-4,-4],states:['off','on','broken'],lighting:v32.lighting}},
  snapContract:{freePointerPreviewAllowed:true,nearestLegalUnoccupiedSlotShownDuringDrag:true,commitOccursOnPointerRelease:true,committedOriginAlwaysExactGridValue:true,fixedCabinetAndOtherMovableAssetRejected:true,interactionAnchorDerivedFromSnappedBodyMidpoint:true,imprecisePointerCoordinateNeverPersisted:true,sinkAndOvenCanBeAdjacentInEitherOrder:true},
  joinResolver:{
    exactAdjacencyRequired:true,leftAndRightIndependent:true,
    precedence:['pair containing oven → V32 triangular join','cabinet↔sink → V22 flat join','unjoined sink left edge → V25 cutout rounded end','unjoined oven edge → no bridge'],
    ovenPair:{backgroundLayers:['six-pixel V22 cabinet-blue body backfill','24 × 12 V30/V32 triangular countertop underlay'],foregroundLayer:'six-pixel V32 neighbour-side seam cleanup',ovenFacingDiagonalRetained:true,worksWith:['cabinet↔oven','sink↔oven','oven↔sink']},
    sinkCabinetPair:{backgroundLayer:'six-pixel V22 cabinet-blue body backfill',foregroundLayer:'16 × 12 V22 row-matched flat cap'},
    sinkExposedLeft:{isolatedLayer:true,clearWindow:[0,26,12,82],replacementSource:['cabinet-run-v11-exact.png',0,0,12,82],roundedEndOnlyWhenNoExactLeftNeighbour:true},
    drawOrder:['room background','all active body backfills and triangular underlays','fixed cabinet and movable appliance layers','V22 flat caps and V32 neighbour-side cleanup masks'],embeddedInSourceAssets:false,
  },
  sources:{generationMode:'deterministic-existing-pixel-masked-compositing',allSinkAndOvenSpritesByteIdenticalToAuthorities:true},publishedAssets,
  boundaries:{v22Changed:false,v25Changed:false,v32Changed:false,sinkSpriteChanged:false,ovenSpritesChanged:false,cabinetChanged:false,roomBackgroundChanged:false,finalChanged:false,runtimeChanged:false,promotionPerformed:false,nextAssetStarted:false},
}
const catalogueFile=path.join(draft,'candidate-catalogue.json');fs.writeFileSync(catalogueFile,JSON.stringify(catalogue,null,2)+'\n')
const shell=path.join(review,'index.html');fs.writeFileSync(shell,fs.readFileSync(template,'utf8').replace('__DATA__',JSON.stringify(catalogue)))
const register={schema:'lighthouse-keeper/reversible-review-batch@1',set,status:'reversible-unapproved-unpromoted',candidate:{catalogue:{file:path.relative(root,catalogueFile),sha256:sha(catalogueFile)},publicShell:{file:path.relative(root,shell),sha256:sha(shell)}},sources:[v22Approval,v25Catalogue,v32Catalogue].map(file=>({file:path.relative(root,file),sha256:sha(file)})),publishedAssets:outputs.map(file=>({source:path.relative(root,file),sourceSha256:sha(file),publicAssemblyPath:path.posix.join('public/keeper-review',set,'assets',path.basename(file))}))}
fs.writeFileSync(path.join(draft,'batch-register.json'),JSON.stringify(register,null,2)+'\n')
console.log('Built Kitchen Modular Join Workbench V33: movable sink and oven with pair-aware exact-snap healing')

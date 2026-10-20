#!/usr/bin/env node
/** Build Oven V32: retain triangular joins and remove only cabinet-facing seams. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd(),set='kitchen-oven-standalone-v32',batch='kitchen-oven-standalone-2026-10-20-v32'
const raw=path.join(root,'art/raw',batch),draft=path.join(root,'art/drafts',batch),review=path.join(root,'public/keeper-review',set)
const template=path.join(root,'scripts/templates/kitchen_oven_standalone_v32.html')
const v30Batch='kitchen-oven-standalone-2026-10-20-v30',v30Raw=path.join(root,'art/raw',v30Batch),v30Catalogue=path.join(root,'art/drafts',v30Batch,'candidate-catalogue.json')
const v31Raw=path.join(root,'art/raw/kitchen-oven-standalone-2026-10-20-v31')
const v22Raw=path.join(root,'art/raw/kitchen-countertop-join-cap-2026-10-19-v22'),v22Approval=path.join(root,'docs/review/kitchen-countertop-join-cap-v22-approval-2026-10-19.json')
const states=['oven-off.png','oven-on.png','oven-broken.png','oven-broken-cavity-lit.png','oven-broken-warning-lit.png','oven-broken-both-lit.png']
const loops=['oven-state-family-strip.png','oven-broken-cavity-flicker-f40.png','oven-broken-warning-flicker-f40.png']
const roomStates=['off','on','broken','broken-cavity-lit','broken-warning-lit','broken-both-lit']
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),read=file=>PNG.sync.read(fs.readFileSync(file)),clone=image=>PNG.sync.read(PNG.sync.write(image))
const write=(image,name)=>{const file=path.join(raw,name);fs.writeFileSync(file,PNG.sync.write(image));return file}
const copy=(source,name=path.basename(source))=>{const file=path.join(raw,name);fs.copyFileSync(source,file);return file}

function composite(dst,src,dx,dy,sx=0,sy=0,w=src.width,h=src.height){
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
    const si=((sy+y)*src.width+sx+x)*4,di=((dy+y)*dst.width+dx+x)*4,a=src.data[si+3]/255,da=dst.data[di+3]/255,oa=a+da*(1-a)
    if(!oa)continue
    for(let c=0;c<3;c++)dst.data[di+c]=Math.round((src.data[si+c]*a+dst.data[di+c]*da*(1-a))/oa)
    dst.data[di+3]=Math.round(oa*255)
  }
}

function crop(image,x,y,w,h){
  const out=new PNG({width:w,height:h})
  for(let yy=0;yy<h;yy++)for(let xx=0;xx<w;xx++){const si=((y+yy)*image.width+x+xx)*4,di=(yy*w+xx)*4;for(let c=0;c<4;c++)out.data[di+c]=image.data[si+c]}
  return out
}

function makeCleanup(cap,side){
  const out=new PNG({width:6,height:12})
  for(let y=0;y<12;y++)for(let x=0;x<6;x++){
    const active=y>0||(side==='left'?x>=2:x<=4)
    if(!active)continue
    const si=y*cap.width*4,di=(y*6+x)*4
    for(let c=0;c<4;c++)out.data[di+c]=cap.data[si+c]
  }
  return out
}

function composeRoom(background,cabinet,oven,body,triangle,leftCleanup,rightCleanup,{heal=true,left=true,right=true}={}){
  const room=clone(background),l=heal&&left,r=heal&&right
  if(l){composite(room,body,333,145,0,0,6,63);composite(room,triangle,324,134)}
  if(r){composite(room,body,417,145,0,0,6,63);composite(room,triangle,408,134)}
  if(left)composite(room,cabinet,164,130)
  if(right)composite(room,cabinet,416,130)
  composite(room,oven,332,127)
  if(l)composite(room,leftCleanup,330,134)
  if(r)composite(room,rightCleanup,420,134)
  return room
}

for(const required of [template,v30Catalogue,v22Approval,path.join(v31Raw,'oven-v30-underlay-join-focus.png'),path.join(v31Raw,'oven-v31-layered-join-focus.png'),...states.map(n=>path.join(v30Raw,n)),...loops.map(n=>path.join(v30Raw,n)),path.join(v30Raw,'room-background-exact.png'),path.join(v30Raw,'cabinet-run-v11-exact.png'),path.join(v30Raw,'oven-v30-protected-dial-focus.png'),path.join(v22Raw,'join-body-backfill-template.png'),path.join(v22Raw,'countertop-join-cap-template.png')])if(!fs.existsSync(required))throw new Error(`Missing authority: ${required}`)
for(const dir of [raw,draft,review]){fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir,{recursive:true})}

const v30=JSON.parse(fs.readFileSync(v30Catalogue,'utf8')),outputs=[]
for(const name of [...states,...loops])outputs.push(copy(path.join(v30Raw,name),name))
for(const [source,name] of [[path.join(v30Raw,'room-background-exact.png'),'room-background-exact.png'],[path.join(v30Raw,'cabinet-run-v11-exact.png'),'cabinet-run-v11-exact.png'],[path.join(v30Raw,'oven-v30-protected-dial-focus.png'),'oven-v30-protected-dial-focus.png'],[path.join(v22Raw,'join-body-backfill-template.png'),'join-body-backfill-template.png'],[path.join(v22Raw,'countertop-join-cap-template.png'),'countertop-triangle-underlay-template.png']])outputs.push(copy(source,name))
const background=read(path.join(v30Raw,'room-background-exact.png')),cabinet=read(path.join(v30Raw,'cabinet-run-v11-exact.png')),body=read(path.join(v22Raw,'join-body-backfill-template.png')),triangle=read(path.join(v22Raw,'countertop-join-cap-template.png'))
if(background.width!==772||background.height!==224||cabinet.width!==176||cabinet.height!==82||body.width!==14||body.height!==63||triangle.width!==24||triangle.height!==12)throw new Error('Approved room or V22 join geometry drifted')
const leftCleanup=makeCleanup(triangle,'left'),rightCleanup=makeCleanup(triangle,'right')
outputs.push(write(leftCleanup,'cabinet-seam-cleanup-left.png'));outputs.push(write(rightCleanup,'cabinet-seam-cleanup-right.png'))

const healed={}
for(const state of roomStates){const oven=read(path.join(v30Raw,`oven-${state}.png`));healed[state]=composeRoom(background,cabinet,oven,body,triangle,leftCleanup,rightCleanup);outputs.push(write(healed[state],`oven-${state}-native-room.png`))}
outputs.push(copy(path.join(v31Raw,'oven-v30-underlay-join-focus.png'),'oven-v30-triangle-seam-focus.png'))
outputs.push(copy(path.join(v31Raw,'oven-v31-layered-join-focus.png'),'oven-v31-flattened-focus.png'))
outputs.push(write(crop(healed.broken,316,126,124,90),'oven-v32-triangle-clean-focus.png'))

const publishedAssets=Object.fromEntries(outputs.map(file=>[path.basename(file),sha(file)]))
const catalogue={
  schema:'lighthouse-keeper/kitchen-standalone-state-family@1',set,version:32,status:'reversible-unapproved-unpromoted',
  authorities:{v30Catalogue:{file:path.relative(root,v30Catalogue),sha256:sha(v30Catalogue)},approvedBodyBackfill:{file:path.relative(root,path.join(v22Raw,'join-body-backfill-template.png')),sha256:sha(path.join(v22Raw,'join-body-backfill-template.png'))},approvedCountertopRows:{file:path.relative(root,path.join(v22Raw,'countertop-join-cap-template.png')),sha256:sha(path.join(v22Raw,'countertop-join-cap-template.png'))},joinApproval:{file:path.relative(root,v22Approval),sha256:sha(v22Approval)},roomBackground:v30.authorities.roomBackground,approvedCabinet:v30.authorities.approvedCabinet},
  sources:{generationMode:'deterministic-existing-pixel-masked-compositing',v30AssetHashes:Object.fromEntries([...states,...loops].map(name=>[name,sha(path.join(v30Raw,name))]))},
  geometry:v30.geometry,foregroundProtection:v30.foregroundProtection,
  joinHealing:{
    method:'triangular-underlay-with-cabinet-facing-seam-cleanup',sharedEdgeX:[336,420],activation:'exact snapped adjacency on the corresponding oven edge',leftAndRightIndependent:true,
    bodyBackfill:{template:'join-body-backfill-template.png',sourceCrop:[0,0,6,63],destinationOrigins:[[333,145],[417,145]],placement:'behind assets'},
    triangularSurface:{template:'countertop-triangle-underlay-template.png',templatePixels:[24,12],destinationOrigins:[[324,134],[408,134]],placement:'behind assets',ovenFacingDiagonalRetained:true},
    cabinetSeamCleanup:{templates:['cabinet-seam-cleanup-left.png','cabinet-seam-cleanup-right.png'],templatePixels:[6,12],destinationOrigins:[[330,134],[420,134]],placement:'in front of assets',cabinetFacingDiagonalRetained:false,rowColoursFromApprovedV22:true},
    drawOrder:['room background','active blue body backfill and triangular surface underlay','cabinet neighbours','standalone oven','active cabinet-facing seam cleanup'],embeddedInOvenSprite:false,embeddedInCabinetSprite:false,
  },
  states:v30.states,lighting:v30.lighting,sfxPlaceholders:v30.sfxPlaceholders,publishedAssets,
  boundaries:{v30Changed:false,v31Changed:false,ovenSpritesChanged:false,cabinetChanged:false,v22JoinAuthorityChanged:false,roomBackgroundChanged:false,finalChanged:false,runtimeChanged:false,promotionPerformed:false,nextAssetStarted:false},
}
const catalogueFile=path.join(draft,'candidate-catalogue.json');fs.writeFileSync(catalogueFile,JSON.stringify(catalogue,null,2)+'\n')
const shell=path.join(review,'index.html');fs.writeFileSync(shell,fs.readFileSync(template,'utf8').replace('__DATA__',JSON.stringify(catalogue)))
const register={schema:'lighthouse-keeper/reversible-review-batch@1',set,status:'reversible-unapproved-unpromoted',candidate:{catalogue:{file:path.relative(root,catalogueFile),sha256:sha(catalogueFile)},publicShell:{file:path.relative(root,shell),sha256:sha(shell)}},sources:[v30Catalogue,v22Approval,path.join(v22Raw,'join-body-backfill-template.png'),path.join(v22Raw,'countertop-join-cap-template.png')].map(file=>({file:path.relative(root,file),sha256:sha(file)})),publishedAssets:outputs.map(file=>({source:path.relative(root,file),sourceSha256:sha(file),publicAssemblyPath:path.posix.join('public/keeper-review',set,'assets',path.basename(file))}))}
fs.writeFileSync(path.join(draft,'batch-register.json'),JSON.stringify(register,null,2)+'\n')
console.log('Built Kitchen Oven V32: V30 triangles retained, cabinet-facing diagonal seams removed, blue body backfills retained')

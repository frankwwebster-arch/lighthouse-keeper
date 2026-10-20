#!/usr/bin/env node
/** Build Oven V31 with the exact approved V22 two-layer join treatment. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root=process.cwd()
const set='kitchen-oven-standalone-v31'
const batch='kitchen-oven-standalone-2026-10-20-v31'
const raw=path.join(root,'art/raw',batch)
const draft=path.join(root,'art/drafts',batch)
const review=path.join(root,'public/keeper-review',set)
const template=path.join(root,'scripts/templates/kitchen_oven_standalone_v31.html')
const v30Batch='kitchen-oven-standalone-2026-10-20-v30'
const v30Raw=path.join(root,'art/raw',v30Batch)
const v30Catalogue=path.join(root,'art/drafts',v30Batch,'candidate-catalogue.json')
const v22Raw=path.join(root,'art/raw/kitchen-countertop-join-cap-2026-10-19-v22')
const v22Approval=path.join(root,'docs/review/kitchen-countertop-join-cap-v22-approval-2026-10-19.json')

const states=['oven-off.png','oven-on.png','oven-broken.png','oven-broken-cavity-lit.png','oven-broken-warning-lit.png','oven-broken-both-lit.png']
const loops=['oven-state-family-strip.png','oven-broken-cavity-flicker-f40.png','oven-broken-warning-flicker-f40.png']
const roomStates=['off','on','broken','broken-cavity-lit','broken-warning-lit','broken-both-lit']
const edges=[336,420]
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const read=file=>PNG.sync.read(fs.readFileSync(file))
const write=(image,name)=>{const file=path.join(raw,name);fs.writeFileSync(file,PNG.sync.write(image));return file}
const copy=(source,name=path.basename(source))=>{const file=path.join(raw,name);fs.copyFileSync(source,file);return file}
const clone=image=>PNG.sync.read(PNG.sync.write(image))

function composite(dst,src,dx,dy,sx=0,sy=0,w=src.width,h=src.height){
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
    const si=((sy+y)*src.width+sx+x)*4,di=((dy+y)*dst.width+dx+x)*4
    const a=src.data[si+3]/255,da=dst.data[di+3]/255,oa=a+da*(1-a)
    if(!oa)continue
    for(let c=0;c<3;c++)dst.data[di+c]=Math.round((src.data[si+c]*a+dst.data[di+c]*da*(1-a))/oa)
    dst.data[di+3]=Math.round(oa*255)
  }
}

function crop(image,x,y,w,h){
  const out=new PNG({width:w,height:h})
  for(let yy=0;yy<h;yy++)for(let xx=0;xx<w;xx++){
    const si=((y+yy)*image.width+x+xx)*4,di=(yy*w+xx)*4
    for(let c=0;c<4;c++)out.data[di+c]=image.data[si+c]
  }
  return out
}

function composeRoom(background,cabinet,oven,bodyFill,cap,{heal=true,left=true,right=true}={}){
  const room=clone(background),active=[]
  if(heal&&left){composite(room,bodyFill,333,145,0,0,6,63);active.push(336)}
  if(heal&&right){composite(room,bodyFill,417,145,0,0,6,63);active.push(420)}
  if(left)composite(room,cabinet,164,130)
  if(right)composite(room,cabinet,416,130)
  composite(room,oven,332,127)
  for(const edge of active)composite(room,cap,edge-8,134,0,0,16,12)
  return room
}

for(const required of [template,v30Catalogue,v22Approval,...states.map(n=>path.join(v30Raw,n)),...loops.map(n=>path.join(v30Raw,n)),path.join(v30Raw,'room-background-exact.png'),path.join(v30Raw,'cabinet-run-v11-exact.png'),path.join(v30Raw,'oven-v30-protected-dial-focus.png'),path.join(v22Raw,'join-body-backfill-template.png'),path.join(v22Raw,'countertop-join-cap-template.png')])if(!fs.existsSync(required))throw new Error(`Missing authority: ${required}`)
for(const dir of [raw,draft,review]){fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir,{recursive:true})}

const v30=JSON.parse(fs.readFileSync(v30Catalogue,'utf8'))
const outputs=[]
for(const name of [...states,...loops])outputs.push(copy(path.join(v30Raw,name),name))
outputs.push(copy(path.join(v30Raw,'room-background-exact.png')))
outputs.push(copy(path.join(v30Raw,'cabinet-run-v11-exact.png')))
outputs.push(copy(path.join(v30Raw,'oven-v30-protected-dial-focus.png')))
outputs.push(copy(path.join(v22Raw,'join-body-backfill-template.png'),'join-body-backfill-template.png'))
outputs.push(copy(path.join(v22Raw,'countertop-join-cap-template.png'),'countertop-seamless-cap-template.png'))

const background=read(path.join(v30Raw,'room-background-exact.png'))
const cabinet=read(path.join(v30Raw,'cabinet-run-v11-exact.png'))
const bodyFill=read(path.join(v22Raw,'join-body-backfill-template.png'))
const cap=read(path.join(v22Raw,'countertop-join-cap-template.png'))
if(background.width!==772||background.height!==224||cabinet.width!==176||cabinet.height!==82||bodyFill.width!==14||bodyFill.height!==63||cap.width!==24||cap.height!==12)throw new Error('Approved room or V22 join geometry drifted')

const healed={}
for(const name of roomStates){
  const oven=read(path.join(v30Raw,`oven-${name}.png`))
  healed[name]=composeRoom(background,cabinet,oven,bodyFill,cap)
  outputs.push(write(healed[name],`oven-${name}-native-room.png`))
}
const v30Room=read(path.join(v30Raw,'oven-broken-native-room.png'))
outputs.push(write(crop(v30Room,316,126,124,90),'oven-v30-underlay-join-focus.png'))
outputs.push(write(crop(healed.broken,316,126,124,90),'oven-v31-layered-join-focus.png'))

const publishedAssets=Object.fromEntries(outputs.map(file=>[path.basename(file),sha(file)]))
const catalogue={
  schema:'lighthouse-keeper/kitchen-standalone-state-family@1',set,version:31,status:'reversible-unapproved-unpromoted',
  authorities:{
    v30Catalogue:{file:path.relative(root,v30Catalogue),sha256:sha(v30Catalogue)},
    approvedBodyBackfill:{file:path.relative(root,path.join(v22Raw,'join-body-backfill-template.png')),sha256:sha(path.join(v22Raw,'join-body-backfill-template.png'))},
    approvedCountertopCap:{file:path.relative(root,path.join(v22Raw,'countertop-join-cap-template.png')),sha256:sha(path.join(v22Raw,'countertop-join-cap-template.png'))},
    joinApproval:{file:path.relative(root,v22Approval),sha256:sha(v22Approval)},
    roomBackground:v30.authorities.roomBackground,
    approvedCabinet:v30.authorities.approvedCabinet,
  },
  sources:{generationMode:'deterministic-existing-pixel-layered-compositing',v30AssetHashes:Object.fromEntries([...states,...loops].map(name=>[name,sha(path.join(v30Raw,name))]))},
  geometry:v30.geometry,
  foregroundProtection:v30.foregroundProtection,
  joinHealing:{
    method:'approved-v22-two-layer-seamless-join',sharedEdgeX:edges,
    activation:'exact snapped adjacency on the corresponding oven edge',leftAndRightIndependent:true,
    bodyBackfill:{template:'join-body-backfill-template.png',templatePixels:[14,63],sourceCrop:[0,0,6,63],destinationOrigins:[[333,145],[417,145]],placement:'behind assets'},
    countertopCap:{template:'countertop-seamless-cap-template.png',templatePixels:[24,12],sourceCrop:[0,0,16,12],destinationOrigins:[[328,134],[412,134]],placement:'in front of assets',seamVisible:false},
    drawOrder:['room background','active blue body backfills','cabinet neighbours','standalone oven','active seamless countertop caps'],
    embeddedInOvenSprite:false,embeddedInCabinetSprite:false,
  },
  states:v30.states,lighting:v30.lighting,sfxPlaceholders:v30.sfxPlaceholders,publishedAssets,
  boundaries:{v30Changed:false,ovenSpritesChanged:false,cabinetChanged:false,v22JoinAuthorityChanged:false,roomBackgroundChanged:false,finalChanged:false,runtimeChanged:false,promotionPerformed:false,nextAssetStarted:false},
}
const catalogueFile=path.join(draft,'candidate-catalogue.json')
fs.writeFileSync(catalogueFile,JSON.stringify(catalogue,null,2)+'\n')
const html=fs.readFileSync(template,'utf8').replace('__DATA__',JSON.stringify(catalogue))
const shell=path.join(review,'index.html');fs.writeFileSync(shell,html)
const register={
  schema:'lighthouse-keeper/reversible-review-batch@1',set,status:'reversible-unapproved-unpromoted',
  candidate:{catalogue:{file:path.relative(root,catalogueFile),sha256:sha(catalogueFile)},publicShell:{file:path.relative(root,shell),sha256:sha(shell)}},
  sources:[v30Catalogue,v22Approval,path.join(v22Raw,'join-body-backfill-template.png'),path.join(v22Raw,'countertop-join-cap-template.png')].map(file=>({file:path.relative(root,file),sha256:sha(file)})),
  publishedAssets:outputs.map(file=>({source:path.relative(root,file),sourceSha256:sha(file),publicAssemblyPath:path.posix.join('public/keeper-review',set,'assets',path.basename(file))})),
}
fs.writeFileSync(path.join(draft,'batch-register.json'),JSON.stringify(register,null,2)+'\n')
console.log('Built Kitchen Oven V31: seamless foreground countertop caps plus blue body backfills on both exact snapped edges')

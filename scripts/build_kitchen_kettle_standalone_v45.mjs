#!/usr/bin/env node
/** Build V45: concept-quality production masters with independent logical scale. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd(), set = 'kitchen-kettle-standalone-v45', batch = 'kitchen-kettle-standalone-2026-10-21-v45'
const source = path.join(root,'art/source',batch), raw = path.join(root,'art/raw',batch), draft = path.join(root,'art/drafts',batch)
const review = path.join(root,'public/keeper-review',set), reviewAssets = path.join(review,'assets')
const template = path.join(root,'scripts/templates/kitchen_kettle_standalone_v45.html')
const v41Raw = path.join(root,'art/raw/kitchen-dishwasher-workbench-2026-10-20-v41')
const v41Catalogue = path.join(root,'art/drafts/kitchen-dishwasher-workbench-2026-10-20-v41/candidate-catalogue.json')
const v43Source = path.join(root,'art/source/kitchen-kettle-standalone-2026-10-20-v43/generated')
const stateSource = path.join(v43Source,'kettle-state-family-source.png'), brokenSource = path.join(v43Source,'kettle-broken-source.png')
const steamSource = path.join(v43Source,'kettle-steam-keyframes-source.png'), generationProvenance = path.join(v43Source,'generation-provenance.json')
const stateNames = ['off','on','broken'], models = ['compact','regular','emphatic'], compatibleOrigins = [84,168,336,504]
const supportSurfaceSlots = [
  {origin:84,supportAssetId:'fridge',surfaceSlotId:'fridge-worktop'},
  {origin:168,supportAssetId:'cabinetA',surfaceSlotId:'cabinet-a-worktop'},
  {origin:336,supportAssetId:'cabinetB',surfaceSlotId:'cabinet-b-worktop'},
  {origin:504,supportAssetId:'dishwasher',surfaceSlotId:'dishwasher-worktop'},
]
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const read = file => PNG.sync.read(fs.readFileSync(file))
for (const file of [template,v41Catalogue,stateSource,brokenSource,steamSource,generationProvenance,path.join(v41Raw,'dishwasher-off-native-room.png'),path.join(v41Raw,'cabinet-a-le-re.png')]) if (!fs.existsSync(file)) throw new Error(`Missing authority: ${file}`)
for (const dir of [source,raw,draft,review]) { fs.mkdirSync(dir,{recursive:true}); for (const item of fs.readdirSync(dir)) fs.rmSync(path.join(dir,item),{recursive:true,force:true}) }

function composite(dst,src,dx,dy,sx=0,sy=0,width=src.width,height=src.height,opacity=1){
  for(let y=0;y<height;y++)for(let x=0;x<width;x++){const xx=dx+x,yy=dy+y;if(xx<0||yy<0||xx>=dst.width||yy>=dst.height)continue
    const si=((sy+y)*src.width+sx+x)*4,di=(yy*dst.width+xx)*4,a=src.data[si+3]/255*opacity,da=dst.data[di+3]/255,oa=a+da*(1-a);if(!oa)continue
    for(let c=0;c<3;c++)dst.data[di+c]=Math.round((src.data[si+c]*a+dst.data[di+c]*da*(1-a))/oa);dst.data[di+3]=Math.round(oa*255)}
}
function crop(src,x,y,width,height){const out=new PNG({width,height});composite(out,src,0,0,x,y,width,height);return out}
function resize(src,width,height){const out=new PNG({width,height});for(let y=0;y<height;y++)for(let x=0;x<width;x++){
  const fx=(x+.5)*src.width/width-.5,fy=(y+.5)*src.height/height-.5,x0=Math.max(0,Math.floor(fx)),y0=Math.max(0,Math.floor(fy)),x1=Math.min(src.width-1,x0+1),y1=Math.min(src.height-1,y0+1),tx=Math.max(0,fx-x0),ty=Math.max(0,fy-y0);let pa=0,pr=0,pg=0,pb=0
  for(const[xx,yy,w]of[[x0,y0,(1-tx)*(1-ty)],[x1,y0,tx*(1-ty)],[x0,y1,(1-tx)*ty],[x1,y1,tx*ty]]){const i=(yy*src.width+xx)*4,a=src.data[i+3]/255;pa+=a*w;pr+=src.data[i]*a*w;pg+=src.data[i+1]*a*w;pb+=src.data[i+2]*a*w}
  const o=(y*width+x)*4;if(pa){out.data[o]=Math.round(pr/pa);out.data[o+1]=Math.round(pg/pa);out.data[o+2]=Math.round(pb/pa);out.data[o+3]=Math.round(pa*255)}}return out}
function resizeNearest(src,width,height){const out=new PNG({width,height});for(let y=0;y<height;y++)for(let x=0;x<width;x++){const sx=Math.min(src.width-1,Math.floor(x*src.width/width)),sy=Math.min(src.height-1,Math.floor(y*src.height/height)),si=(sy*src.width+sx)*4,di=(y*width+x)*4;for(let c=0;c<4;c++)out.data[di+c]=src.data[si+c]}return out}
function thresholdAlpha(image,threshold=18){for(let i=3;i<image.data.length;i+=4)if(image.data[i]<threshold)image.data[i-3]=image.data[i-2]=image.data[i-1]=image.data[i]=0;return image}
function largestComponentBox(image,x0,x1,threshold=24){const width=x1-x0,height=image.height,seen=new Uint8Array(width*height);let best=null
  for(let y=0;y<height;y++)for(let x=0;x<width;x++){const q=y*width+x;if(seen[q]||image.data[(y*image.width+x0+x)*4+3]<threshold)continue
    const stack=[q];seen[q]=1;let count=0,minX=x,maxX=x,minY=y,maxY=y
    while(stack.length){const z=stack.pop(),xx=z%width,yy=(z-xx)/width;count++;minX=Math.min(minX,xx);maxX=Math.max(maxX,xx);minY=Math.min(minY,yy);maxY=Math.max(maxY,yy)
      for(const[dx,dy]of[[1,0],[-1,0],[0,1],[0,-1]]){const nx=xx+dx,ny=yy+dy,ni=ny*width+nx;if(nx>=0&&nx<width&&ny>=0&&ny<height&&!seen[ni]&&image.data[(ny*image.width+x0+nx)*4+3]>=threshold){seen[ni]=1;stack.push(ni)}}}
    if(!best||count>best.count)best={count,x:x0+minX,y:minY,width:maxX-minX+1,height:maxY-minY+1}}
  if(!best)throw new Error(`No source component in x=${x0}..${x1}`);return best}
function isolateMaster(image,box,gutter=32){const item=thresholdAlpha(crop(image,box.x,box.y,box.width,box.height)),out=new PNG({width:item.width+gutter*2,height:item.height+gutter*2});composite(out,item,gutter,gutter);return{image:out,sourceRect:[gutter,gutter,item.width,item.height],sourceComponent:box}}
function fitInto(src,width,height){const scale=Math.min(width/src.width,height/src.height);return thresholdAlpha(resize(src,Math.max(1,Math.round(src.width*scale)),Math.max(1,Math.round(src.height*scale))))}
function setPixel(image,x,y,rgba){if(x<0||y<0||x>=image.width||y>=image.height)return;const i=(y*image.width+x)*4;for(let c=0;c<4;c++)image.data[i+c]=rgba[c]}
function write(image,name){const file=path.join(raw,name);fs.writeFileSync(file,PNG.sync.write(image));return file}
function copy(sourceFile,name){const file=path.join(raw,name);fs.copyFileSync(sourceFile,file);return file}

const outputs=[]
outputs.push(copy(path.join(v41Raw,'dishwasher-off-native-room.png'),'approved-kitchen-counter-room.png'))
outputs.push(copy(path.join(v41Raw,'cabinet-a-le-re.png'),'approved-counter-bay.png'))

// Promote the approved concept pixels. Runtime scale is metadata, never a 48px source redraw.
const family=read(stateSource),intactBox=largestComponentBox(family,0,Math.floor(family.width/3))
const brokenPainting=read(brokenSource),brokenBox=largestComponentBox(brokenPainting,0,brokenPainting.width)
const intactMaster=isolateMaster(family,intactBox),brokenMaster=isolateMaster(brokenPainting,brokenBox)
outputs.push(write(intactMaster.image,'kettle-off.png'))
outputs.push(copy(path.join(raw,'kettle-off.png'),'kettle-on.png'))
outputs.push(write(brokenMaster.image,'kettle-broken.png'))
const stateRender={
  off:{sourceRect:intactMaster.sourceRect,renderPixels:[56,51],offset:[14,-51]},
  on:{sourceRect:intactMaster.sourceRect,renderPixels:[56,51],offset:[14,-51]},
  broken:{sourceRect:brokenMaster.sourceRect,renderPixels:[62,59],offset:[11,-59]},
}

const steam=read(steamSource),steamComponents=[]
for(let i=0;i<5;i++){const a=Math.floor(i*steam.width/5),b=Math.floor((i+1)*steam.width/5),box=largestComponentBox(steam,a,b);steamComponents.push(crop(steam,box.x,box.y,box.width,box.height))}
const pathFrames=[0,1,2,3,4,3,2,1,0]
const effectSpecs={
  on:{cell:[128,176],sourceSizes:{compact:[54,112],regular:[68,132],emphatic:[82,148]},logicalSizes:{compact:[16,30],regular:[20,36],emphatic:[24,42]},opacity:{compact:.64,regular:.76,emphatic:.86}},
  broken:{cell:[144,192],sourceSizes:{compact:[70,126],regular:[84,146],emphatic:[98,162]},logicalSizes:{compact:[22,36],regular:[27,42],emphatic:[32,46]},opacity:{compact:.72,regular:.84,emphatic:.94}},
}
function effectStrip(state,model){const spec=effectSpecs[state],[cellW,cellH]=spec.cell,[targetW,targetH]=spec.sourceSizes[model],keys=steamComponents.map(component=>fitInto(component,targetW,targetH)),strip=new PNG({width:cellW*40,height:cellH})
  for(let frame=0;frame<40;frame++){const segment=Math.floor(frame/5),t=(frame%5)/5,a=keys[pathFrames[segment]],b=keys[pathFrames[segment+1]],place=(image,amount)=>composite(strip,image,frame*cellW+Math.round((cellW-image.width)/2),cellH-12-image.height,0,0,image.width,image.height,amount*spec.opacity[model]);place(a,1-t);place(b,t)
    if(state==='broken'){const phase=frame%8,ox=frame*cellW,sparks=[[22+phase*2,138-phase*5],[116-phase*3,112+phase*2],[34+phase*5,72+phase*3],[102-phase*4,52+phase]]
      for(let index=0;index<sparks.length;index++){const[x,y]=sparks[index],color=index%2?[255,116,38,245]:[255,218,88,255];for(const[px,py]of[[x,y],[x+1,y],[x,y+1],[x+1,y+1]])setPixel(strip,ox+px,py,color)}
      if(phase===2||phase===6)for(const[x,y]of[[118,154],[119,155],[120,156],[29,161]])setPixel(strip,ox+x,y,[156,211,214,235])}}
  return strip}
for(const state of ['on','broken'])for(const model of models)outputs.push(write(effectStrip(state,model),`fx-kettle-${state}-steam--${model}-f40.png`))

const KETTLE_ORIGIN=168,WORKTOP_Y=134,SUPPORT_Y=141,PROOF_SCALE=2
const effectDefaults={on:{dx:54,dy:-72,model:'regular'},broken:{dx:54,dy:-78,model:'regular'}}
function renderState(room,state,placedOrigin){const spec=stateRender[state],master=state==='broken'?brokenMaster.image:intactMaster.image,[sx,sy,sw,sh]=spec.sourceRect,[logicalW,logicalH]=spec.renderPixels,scaled=resize(crop(master,sx,sy,sw,sh),logicalW*PROOF_SCALE,logicalH*PROOF_SCALE);composite(room,scaled,(placedOrigin+spec.offset[0])*PROOF_SCALE,(SUPPORT_Y+spec.offset[1])*PROOF_SCALE)}
function renderEffect(room,state,placedOrigin,frame){const model='regular',spec=effectSpecs[state],meta=effectDefaults[state],strip=read(path.join(raw,`fx-kettle-${state}-steam--${model}-f40.png`)),[cw,ch]=spec.cell,[logicalW,logicalH]=spec.logicalSizes[model],scaled=resize(crop(strip,frame*cw,0,cw,ch),logicalW*PROOF_SCALE,logicalH*PROOF_SCALE);composite(room,scaled,(placedOrigin+meta.dx)*PROOF_SCALE,(SUPPORT_Y+meta.dy)*PROOF_SCALE)}
function proof(state,placedOrigin=KETTLE_ORIGIN){const room=resizeNearest(read(path.join(raw,'approved-kitchen-counter-room.png')),772*PROOF_SCALE,224*PROOF_SCALE);renderState(room,state,placedOrigin);if(state!=='off')renderEffect(room,state,placedOrigin,state==='on'?13:22);return room}
for(const state of stateNames)outputs.push(write(proof(state),`kettle-${state}-retina-room.png`))
outputs.push(write(proof('off',84),'kettle-off-fridge-retina-room.png'))

const effects={}
for(const state of ['on','broken'])for(const model of models){const spec=effectSpecs[state],logical=spec.logicalSizes[model],defaults=effectDefaults[state],id=`kettle-${state}-steam-${model}`;effects[id]={file:`fx-kettle-${state}-steam--${model}-f40.png`,asset:'kettle',anchorAssetId:'kettle',transformSpace:'asset-local',appliesToState:state,remainsAttachedWhileBroken:true,model,baseFps:4,frameCount:40,durationSeconds:10,rasterCellPixels:spec.cell,logicalRenderPixels:logical,defaultTransform:{dx:defaults.dx,dy:defaults.dy,width:logical[0],height:logical[1],crop:[0,0,0,0],speed:1}}}
const brokenKeyframes=[{dx:0,angle:0},{dx:2.2,angle:2.8},{dx:-2.4,angle:-3.4},{dx:3,angle:3.8},{dx:-3,angle:-4.1},{dx:2.4,angle:3.2},{dx:-1.8,angle:-2.5},{dx:0,angle:0}]
const v41=JSON.parse(fs.readFileSync(v41Catalogue,'utf8'))
const publishedAssets=Object.fromEntries(outputs.map(file=>[path.basename(file),sha(file)]))
fs.mkdirSync(reviewAssets,{recursive:true});for(const file of outputs)fs.copyFileSync(file,path.join(reviewAssets,path.basename(file)))
const catalogue={
  schema:'lighthouse-keeper/kitchen-kettle-standalone@1',set,version:45,status:'reversible-unapproved-unpromoted',
  authorities:{dishwasherV41Catalogue:{file:path.relative(root,v41Catalogue),sha256:sha(v41Catalogue)},modularStandard:{file:'docs/KITCHEN_MODULAR_ASSET_AND_JOIN_STANDARD_2026-10-20.md',sha256:sha(path.join(root,'docs/KITCHEN_MODULAR_ASSET_AND_JOIN_STANDARD_2026-10-20.md'))}},
  sourceProvenance:{mode:'approved high-resolution concept pixels promoted directly to production masters; deterministic crop/pad only; logical scale stored separately',stateFamily:{file:path.relative(root,stateSource),sha256:sha(stateSource),selectedComponent:intactBox},brokenState:{file:path.relative(root,brokenSource),sha256:sha(brokenSource),selectedComponent:brokenBox},steamKeyframes:{file:path.relative(root,steamSource),sha256:sha(steamSource)},generationProvenance:{file:path.relative(root,generationProvenance),sha256:sha(generationProvenance)},generatedSourcesUsedAsProductionSprites:true,productionResizeAppliedToKettleMasters:false},
  geometry:{roomPixels:[772,224],reviewBackingScale:PROOF_SCALE,bayWidthPixels:84,worktopY:WORKTOP_Y,footLineY:208,primeStopTurnY:218,logicalFootprintPixels:[84,74],defaultOrigin:KETTLE_ORIGIN,compatibleCounterOrigins:compatibleOrigins,supportSurfaceSlots,primeAnchor:[KETTLE_ORIGIN+42,218],supportPlaneY:SUPPORT_Y,contactBottomExclusive:SUPPORT_Y,stateRender,scaleRationale:'The high-resolution masters retain 588 x 540 and 976 x 928 source pixels. Runtime draws them at 56 x 51 and 62 x 59 logical pixels inside one 84 px / 60 cm bay; raster quality is independent of countertop footprint.'},
  states:{off:{file:'kettle-off.png',effect:null},on:{file:'kettle-on.png',casingSha256:sha(path.join(raw,'kettle-on.png')),identicalToOff:sha(path.join(raw,'kettle-on.png'))===sha(path.join(raw,'kettle-off.png')),effectFamily:'kettle-on-steam'},broken:{file:'kettle-broken.png',bodyAnimation:{type:'asset-local-transform',frameCount:brokenKeyframes.length,fps:7,pivot:'bottom-centre-support-contact',basePinnedToSupportY:SUPPORT_Y,keyframes:brokenKeyframes},staticDamage:['handle torn from left mount and twisted across lid','lid forced wide open','spout cap displaced','deep crushed body panel','large jagged enamel rupture exposing dark metal','fractures and scorching'],effectFamily:'kettle-broken-steam',movementLocked:true}},
  effects,brokenAssetLock:v41.brokenAssetLock,
  countertopOccupancy:{layer:'countertop-appliance',compatibleOrigins,supportSurfaceSlots,placementPersistence:'store supportAssetId, surfaceSlotId and asset-local placement; derive room origin and Keeper stop point from the current supporting bay',moveRule:'Off/On commits only exact compatible counter origins, including the fridge worktop; Broken rejects direct move, bay-button movement and movement of its supporting asset',supportMoveRule:'a support asset carrying a Broken kettle cannot move until the kettle is repaired or removed',movingKettleMovesSupportAsset:false,movingSupportMovesKettle:true,cabinetryMovesWithKettle:false,joinsRecomputed:false},
  teaInteraction:{actionId:'make-cup-of-tea',dynamicPlace:true,keeperStopTurnY:218,keeperStopTurnXRule:'support bay origin + 42',facing:'rear',resolvesFrom:['supportAssetId','surfaceSlotId'],availableStates:['off','on'],blockedState:'broken'},
  soundPlaceholders:['kitchen_kettle_heating_hiss_loop','kitchen_kettle_broken_handle_rattle','kitchen_kettle_broken_pressure_hiss_loop'],reviewProofs:[...stateNames.map(state=>`kettle-${state}-retina-room.png`),'kettle-off-fridge-retina-room.png'],
  boundaries:{dishwasherV41Changed:false,approvedCabinetryChanged:false,toasterStarted:false,mixingBowlStarted:false,runtimeControllerImplemented:false,finalChanged:false},publishedAssets,
}
const catalogueFile=path.join(draft,'candidate-catalogue.json');fs.writeFileSync(catalogueFile,`${JSON.stringify(catalogue,null,2)}\n`)
const shell=path.join(review,'index.html');fs.writeFileSync(shell,fs.readFileSync(template,'utf8').replace('__DATA__',JSON.stringify(catalogue)))
fs.writeFileSync(path.join(source,'source-manifest.json'),`${JSON.stringify({set,status:'source-only-unapproved',generationMode:'existing built-in image-generation sources promoted without regeneration',files:{'v43/kettle-state-family-source.png':sha(stateSource),'v43/kettle-broken-source.png':sha(brokenSource),'v43/kettle-steam-keyframes-source.png':sha(steamSource),'v43/generation-provenance.json':sha(generationProvenance)},normalization:'Deterministic component isolation, 32 source-pixel transparent gutter and alpha cleanup below 18/255. Kettle master components are not resized; logical render dimensions live only in catalogue metadata.'},null,2)}\n`)
const register={schema:'lighthouse-keeper/reversible-review-batch@1',set,status:catalogue.status,candidate:{catalogue:{file:path.relative(root,catalogueFile),sha256:sha(catalogueFile)},publicShell:{file:path.relative(root,shell),sha256:sha(shell)}},sources:[v41Catalogue,stateSource,brokenSource,steamSource,generationProvenance].map(file=>({file:path.relative(root,file),sha256:sha(file)})),publishedAssets:outputs.map(file=>({source:path.relative(root,file),sourceSha256:sha(file),publicAssemblyPath:path.posix.join('public/keeper-review',set,'assets',path.basename(file))}))}
fs.writeFileSync(path.join(draft,'batch-register.json'),`${JSON.stringify(register,null,2)}\n`)
console.log(`Built Kitchen Kettle Standalone V45: ${outputs.length} assets; concept-quality masters render at one-bay logical scale with 2x review backing.`)

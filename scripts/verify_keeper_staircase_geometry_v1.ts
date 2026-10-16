import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const pack = path.join(root,'art/drafts/keeper-staircase-geometry-2026-10-16-v1')
const geometryFile = path.join(pack,'staircase-geometry-v1.json')
const svgFile = path.join(pack,'evidence/staircase-test-profile-v1.svg')
const handoffFile = path.join(pack,'HANDOFF.md')
const registerFile = path.join(pack,'batch-register.json')
const rigFile = path.join(root,'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16/stair-contact-rig-v16.json')
const approvalFile = path.join(root,'art/drafts/keeper-prime-stair-ascent-2026-10-15-v17/batch-register.json')
const descentFile = path.join(root,'art/drafts/keeper-prime-stair-descent-2026-10-16-v1/keeper-prime-stair-descent-v1.json')
const read = (file:string)=>JSON.parse(fs.readFileSync(file,'utf8'))
const sha = (file:string)=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message:string):never=>{throw new Error(`[keeper-staircase-geometry-v1] ${message}`)}
const near = (a:number,b:number,epsilon=1e-9)=>Math.abs(a-b)<=epsilon
for(const file of [geometryFile,svgFile,handoffFile,registerFile,rigFile,approvalFile,descentFile]) if(!fs.existsSync(file)) fail(`missing ${path.relative(root,file)}`)
const geometry=read(geometryFile), register=read(registerFile), rig=read(rigFile), approval=read(approvalFile), descent=read(descentFile)
if(geometry.schema!=='lighthouse-keeper/staircase-geometry@1'||geometry.status!=='approved-geometry-only-scenery-art-pending') fail('identity changed')
const flight=geometry.flight
if(flight.risers!==14||flight.treadRunLp!==7||!near(flight.riserRise.decimalLp,30/7)||flight.flightRunLp!==98||flight.flightRiseLp!==60||flight.reservedCoreRunLp!==105) fail('locked staircase dimensions changed')
if(geometry.floorPitch.lowerFinishedFloorYLp!==20||geometry.floorPitch.upperFinishedFloorYLp!==80||geometry.floorPitch.finishedFloorPitchLp!==60) fail('floor pitch changed')
if(geometry.treads.length!==14) fail('tread count changed')
for(let index=0;index<14;index++){
  const tread=geometry.treads[index], number=index+1
  const expectedRight=116-index*7, expectedLeft=expectedRight-7, expectedTop=20+number*(30/7)
  if(tread.number!==number||!near(tread.leftXLp,expectedLeft)||!near(tread.rightXLp,expectedRight)||!near(tread.topYLp,expectedTop)||!near(tread.contactCentreXLp,expectedLeft+3.5)) fail(`tread ${number} geometry changed`)
  if(index&& !near(tread.rightXLp,geometry.treads[index-1].leftXLp)) fail(`tread ${number} no longer contiguous`)
}
if(!near(geometry.treads.at(-1).topYLp,80)||geometry.treads[0].rightXLp-geometry.treads.at(-1).leftXLp!==98) fail('flight closure changed')
for(const key of ['floorTopLp','stairBaseRightLp','floorSupportCentreLp','flightRunLp','flightRiseLp','risers','treadRunLp','riserRiseLp','reservedCoreRunLp']){
  const mapped:any={floorTopLp:20,stairBaseRightLp:116,floorSupportCentreLp:119.5,flightRunLp:98,flightRiseLp:60,risers:14,treadRunLp:7,riserRiseLp:30/7,reservedCoreRunLp:105}
  if(!near(rig.geometry[key],mapped[key])) fail(`approved contact rig disagrees on ${key}`)
}
if(!approval.staircaseVisualContract?.geometryRule?.includes('fourteen-riser, 7-lp-tread, 98-by-60-lp')) fail('approved scenery contract changed')
if(descent.geometry.stair.risers!==14||descent.geometry.stair.treadRunLp!==7||descent.geometry.stair.flightRunLp!==98||descent.geometry.stair.flightRiseLp!==60) fail('descent review geometry disagrees')
for(const [entry,file] of [[register.geometry,geometryFile],[register.testProfileEvidence,svgFile],[register.handoff,handoffFile],[register.authorities.approvedContactRig,rigFile],[register.authorities.approvalPack,approvalFile]] as any) if(entry.sha256!==sha(file)) fail(`stale hash for ${entry.file}`)
const svg=fs.readFileSync(svgFile,'utf8')
if((svg.match(/<rect\b/g)||[]).length!==17||!svg.includes('id="future-foreground-scenery-envelope"')||!svg.includes('14 risers · 7 lp tread · 30/7 lp rise · 98 × 60 lp flight · 105 lp reserved core')) fail('stored test profile changed')
if(geometry.futureSceneryEnvelope.geometryMayChange!==false||geometry.futureSceneryEnvelope.requiredNewelPosts!==2||!geometry.futureSceneryEnvelope.requiredBalustrade.includes('foreground')||!geometry.futureSceneryEnvelope.requiredHandrail.includes('continuous')) fail('future scenery boundary changed')
if(register.visualBoundary.testRenderingApprovedAsFinalScenery!==false||register.visualBoundary.futureSceneryMayChangeLockedMeasurements!==false||register.visualBoundary.runtimeChanged!==false||register.visualBoundary.productionChanged!==false) fail('approval boundary changed')
console.log(JSON.stringify({ok:true,risers:14,treadRunLp:7,riserRiseLp:30/7,flight:[98,60],reservedCoreRunLp:105,testProfileStored:true,finalSceneryApproved:false},null,2))

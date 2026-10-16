import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const pack = path.join(root, 'art/drafts/keeper-prime-stair-descent-2026-10-16-v2')
const specFile = path.join(pack, 'keeper-prime-stair-descent-v2.json')
const registerFile = path.join(pack, 'batch-register.json')
const pageFile = path.join(root, 'public/keeper-review/keeper-prime-stair-descent-v2/index.html')
const read = (file:string) => JSON.parse(fs.readFileSync(file,'utf8'))
const sha = (file:string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message:string):never => { throw new Error(`[keeper-prime-stair-descent-v2] ${message}`) }
const alphaBounds = (png:PNG, threshold=16) => {
  let minX=png.width,minY=png.height,maxX=-1,maxY=-1
  for (let y=0;y<png.height;y++) for (let x=0;x<png.width;x++) if (png.data[(y*png.width+x)*4+3]>=threshold) {
    minX=Math.min(minX,x); minY=Math.min(minY,y); maxX=Math.max(maxX,x); maxY=Math.max(maxY,y)
  }
  return [minX,minY,maxX,maxY]
}
for (const file of [specFile,registerFile,pageFile]) if (!fs.existsSync(file)) fail(`missing ${path.relative(root,file)}`)
const spec = read(specFile)
const register = read(registerFile)
if (spec.schema !== 'lighthouse-keeper/stair-descent@2' || spec.status !== 'draft-stair-descent-v2-awaiting-frank') fail('identity changed')
if (spec.geometry.stair.risers !== 14 || spec.geometry.stair.flightRunLp !== 98 || spec.geometry.stair.flightRiseLp !== 60) fail('approved stair geometry changed')
if (!spec.direction.mechanics.startsWith('four descent-specific drawings alternate')) fail('alternating descent mechanics contract changed')
if (spec.boundaries.staircaseGeometryChanged !== false || spec.boundaries.newKeeperArtworkPresent !== true) fail('art/geometry boundary changed')

const routes = spec.routes
for (const key of ['turnMount','descentOnly','lowerExit','fullFlow']) if (!routes[key]?.frames?.length) fail(`route missing ${key}`)
const full = routes.fullFlow.frames
const descent = full.filter((frame:any)=>/^descent:\d+$/.test(frame.sourceFrame))
if (descent.length !== 27) fail(`expected 27 descending frames, found ${descent.length}`)
for (let index=0;index<27;index++) {
  const expected = `descent:${index+1}`
  if (descent[index].sourceFrame !== expected) fail(`descent frame ${index+1} is ${descent[index].sourceFrame}, expected ${expected}`)
  if (descent[index].flipX !== false) fail(`descent frame ${index+1} must use native side-right artwork`)
  if (index && (descent[index].xLp < descent[index-1].xLp || descent[index].bottomLp > descent[index-1].bottomLp)) fail(`descent root reverses at frame ${index+1}`)
  if (![0,0.25].includes(descent[index].descentRootCorrectionLp)) fail(`unexpected root correction at frame ${index+1}`)
}
const contacts = descent.filter((frame:any)=>frame.kind==='contact')
if (contacts.length !== 14) fail(`expected 14 contacts, found ${contacts.length}`)
for (let index=1;index<contacts.length;index++) if (contacts[index].leg === contacts[index-1].leg) fail(`contact legs do not alternate at ${index+1}`)
if (contacts.filter((frame:any)=>frame.leg==='right').length !== 7 || contacts.filter((frame:any)=>frame.leg==='left').length !== 7) fail('contacts are not exactly 7/7')
const expectedGait = ['right:contact','left:passing','left:contact','right:passing']
for (let index=0;index<descent.length;index++) {
  const actual = `${descent[index].leg}:${descent[index].kind}`
  if (actual !== expectedGait[index % 4]) fail(`gait phase ${index+1} is ${actual}`)
}
if (full[0].xLp !== 158.875 || full[0].upperDoorOpen !== 1) fail('route no longer begins walking under upper-door cover')
if (full.at(-1).xLp !== 161.5 || full.at(-1).lowerDoorOpen !== 1) fail('route no longer ends fully hidden behind lower door')
const turn = full.filter((frame:any)=>frame.sourceFrame?.startsWith('front-side:'))
if (turn.length !== 14 || turn[6].sourceFrame !== 'front-side:1' || turn[7].sourceFrame !== 'front-side:2') fail('side-left → front → side-right turn changed')
if (new Set(turn.map((frame:any)=>`${frame.xLp},${frame.bottomLp}`)).size !== 1) fail('turn root drifts')

const sourceHashes = new Set<string>()
for (const asset of register.publishedAssets) {
  const file = path.join(root,asset.source)
  if (!fs.existsSync(file) || sha(file)!==asset.sourceSha256) fail(`source hash changed ${asset.source}`)
  if (sourceHashes.has(asset.sourceSha256)) fail(`duplicate published object ${asset.sourceSha256}`)
  sourceHashes.add(asset.sourceSha256)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width!==256 || png.height!==320) fail(`cell changed ${asset.source}`)
  for (let x=0;x<png.width;x++) if (png.data[x*4+3] || png.data[((png.height-1)*png.width+x)*4+3]) fail(`horizontal gutter touched ${asset.source}`)
  for (let y=1;y<png.height-1;y++) if (png.data[(y*png.width)*4+3] || png.data[(y*png.width+png.width-1)*4+3]) fail(`vertical gutter touched ${asset.source}`)
}
for (const [name,record] of Object.entries(register.artwork) as any) {
  for (const lane of ['raw','draft']) {
    const file = path.join(root,record[lane].file)
    if (!fs.existsSync(file) || sha(file)!==record[lane].sha256) fail(`${name} ${lane} hash changed`)
    const png = PNG.sync.read(fs.readFileSync(file))
    if (png.width!==record[lane].dimensions[0] || png.height!==record[lane].dimensions[1]) fail(`${name} ${lane} dimensions changed`)
    if (lane==='draft') {
      const bounds=alphaBounds(png)
      if (JSON.stringify(bounds)!==JSON.stringify(record[lane].alphaBounds16)) fail(`${name} registered alpha bounds changed`)
      if (bounds[1]!==30 || bounds[3]!==315) fail(`${name} head/floor registration changed`)
      if (Math.abs(((bounds[0]+bounds[2])/2)-127.5)>0.5) fail(`${name} horizontal centre changed`)
    }
  }
}
const registeredUrls = new Set(register.publishedAssets.map((asset:any)=>asset.url))
for (const [key,route] of Object.entries(routes) as any) for (const [index,frame] of route.frames.entries()) if (!registeredUrls.has(frame.src)) fail(`${key} frame ${index+1} has unregistered asset`)
if (register.spec.sha256!==sha(specFile) || register.handoff.sha256!==sha(path.join(pack,'HANDOFF.md')) || register.reviewPage.sha256!==sha(pageFile)) fail('register hashes stale')
if (register.validation.rightContacts!==7 || register.validation.leftContacts!==7 || register.validation.staircaseGeometryChanged!==false) fail('descent validation changed')
if (register.validation.finalChanged!==false || register.validation.runtimeChanged!==false || register.validation.productionChanged!==false) fail('promotion boundary changed')
const html = fs.readFileSync(pageFile,'utf8')
for (const required of ['Previous frame','Next frame','data-scale="4"','Promise.all(unique.map(preload))','const routes={turn:SPEC.routes.turnMount','let routeId=\'turn\'']) if (!html.includes(required)) fail(`review contract missing ${required}`)
if (html.includes(`/keeper-review/keeper-prime-stair-transitions-v6/assets/`)) fail('stale source review URL leaked')
console.log(JSON.stringify({ok:true,routes:Object.fromEntries(Object.entries(routes).map(([key,route]:any)=>[key,route.frames.length])),descendingFrames:descent.length,contacts:contacts.length,rightContacts:7,leftContacts:7,publishedAssets:register.publishedAssets.length},null,2))

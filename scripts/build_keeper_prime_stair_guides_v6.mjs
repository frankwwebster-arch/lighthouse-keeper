#!/usr/bin/env node
/** Build the two six-pose, one-riser-per-leg V6 authoring guides as SVG. */
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const out = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v6/guides')
fs.mkdirSync(out, { recursive: true })
const width = 768
const height = 640
const red = '#ff5264'
const cyan = '#45d3ff'
const gold = '#ffe06a'
const poses = [
  { lead:[[130,215],[116,250],[111,287],[132,301]], support:[[126,215],[108,258],[103,289],[104,316]], root:[0,0], phase:'lift' },
  { lead:[[130,215],[145,244],[154,270],[174,282]], support:[[126,215],[108,258],[103,289],[104,316]], root:[1,0], phase:'swing' },
  { lead:[[130,215],[157,239],[170,258],[192,270]], support:[[126,215],[108,258],[103,289],[104,316]], root:[2,0], phase:'high pass' },
  { lead:[[130,215],[160,247],[175,270],[196,282]], support:[[126,215],[108,258],[103,289],[104,316]], root:[3.5,0], phase:'upper contact' },
  { lead:[[130,215],[154,251],[168,282],[190,299]], support:[[126,215],[108,260],[99,298],[112,318]], root:[4.75,2.142857], phase:'weight transfer' },
  { lead:[[130,215],[145,256],[145,291],[166,316]], support:[[126,215],[111,252],[101,278],[122,296]], root:[6,4.285714], phase:'plant / other toe-off' },
]

const line = (points, colour, opacity=1) => `<polyline points="${points.map(([x,y])=>`${x},${y}`).join(' ')}" fill="none" stroke="${colour}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" opacity="${opacity}"/>`
const foot = ([x,y], colour) => `<line x1="${x-15}" y1="${y}" x2="${x+17}" y2="${y}" stroke="${colour}" stroke-width="12" stroke-linecap="round"/>`
const panel = (pose, index, leadColour, supportColour, title) => {
  const col = index % 3
  const row = Math.floor(index / 3)
  const ox = col * 256
  const oy = row * 320
  const upperY = 282
  return `<g transform="translate(${ox} ${oy})">
    <rect width="256" height="320" fill="#0a1117"/>
    <path d="M18 316H118V282H238" fill="none" stroke="#aebbc4" stroke-width="3"/>
    <path d="M18 316H118V282H238V316Z" fill="#552022" opacity=".38"/>
    <circle cx="128" cy="72" r="44" fill="#26343e" stroke="#71818c" stroke-width="3"/>
    <line x1="128" y1="116" x2="128" y2="215" stroke="#71818c" stroke-width="16" stroke-linecap="round"/>
    <line x1="128" y1="135" x2="91" y2="202" stroke="#d8e1e6" stroke-width="12" stroke-linecap="round"/>
    <line x1="128" y1="135" x2="165" y2="202" stroke="#d8e1e6" stroke-width="12" stroke-linecap="round"/>
    ${line(pose.support, supportColour, .9)}${foot(pose.support.at(-1), supportColour)}
    ${line(pose.lead, leadColour)}${foot(pose.lead.at(-1), leadColour)}
    <circle cx="128" cy="215" r="7" fill="${gold}"/>
    <line x1="18" y1="${upperY}" x2="238" y2="${upperY}" stroke="${gold}" stroke-width="2" stroke-dasharray="6 5" opacity=".8"/>
    <text x="12" y="20" fill="#fff" font-family="system-ui,sans-serif" font-size="13" font-weight="700">${title} ${index+1}/6 · ${pose.phase}</text>
    <text x="12" y="308" fill="#a8bdc8" font-family="ui-monospace,monospace" font-size="11">root ${pose.root[0]} run · ${pose.root[1]} rise</text>
  </g>`
}

const build = (name, leadColour, supportColour, title) => {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">${poses.map((pose,index)=>panel(pose,index,leadColour,supportColour,title)).join('')}</svg>`
  fs.writeFileSync(path.join(out, name), svg)
}

build('left-leg-step-guide-v6.svg', red, cyan, 'LEFT LEG')
build('right-leg-step-guide-v6.svg', cyan, red, 'RIGHT LEG')

const rgba = (hex, alpha=255) => [parseInt(hex.slice(1,3),16),parseInt(hex.slice(3,5),16),parseInt(hex.slice(5,7),16),alpha]
const setPixel = (png,x,y,colour) => {
  x=Math.round(x);y=Math.round(y)
  if(x<0||x>=png.width||y<0||y>=png.height)return
  const offset=(png.width*y+x)*4
  png.data[offset]=colour[0];png.data[offset+1]=colour[1];png.data[offset+2]=colour[2];png.data[offset+3]=colour[3]
}
const circle = (png,cx,cy,r,colour) => { for(let y=Math.floor(cy-r);y<=Math.ceil(cy+r);y++)for(let x=Math.floor(cx-r);x<=Math.ceil(cx+r);x++)if((x-cx)**2+(y-cy)**2<=r*r)setPixel(png,x,y,colour) }
const thickLine = (png,a,b,width,colour) => {
  const dx=b[0]-a[0],dy=b[1]-a[1],steps=Math.max(Math.abs(dx),Math.abs(dy))*2
  for(let i=0;i<=steps;i++){const t=steps?i/steps:0;circle(png,a[0]+dx*t,a[1]+dy*t,width/2,colour)}
}
const rect = (png,x,y,w,h,colour) => { for(let yy=y;yy<y+h;yy++)for(let xx=x;xx<x+w;xx++)setPixel(png,xx,yy,colour) }
const rasterSheet = (filename,leadHex,supportHex) => {
  const png=new PNG({width,height})
  const lead=rgba(leadHex),support=rgba(supportHex),body=rgba('#71818c'),arms=rgba('#d8e1e6'),tread=rgba('#aebbc4'),joint=rgba(gold)
  poses.forEach((pose,index)=>{
    const ox=(index%3)*256,oy=Math.floor(index/3)*320
    rect(png,ox,oy,256,320,rgba('#0a1117'))
    thickLine(png,[ox+18,oy+316],[ox+118,oy+316],3,tread);thickLine(png,[ox+118,oy+316],[ox+118,oy+282],3,tread);thickLine(png,[ox+118,oy+282],[ox+238,oy+282],3,tread)
    circle(png,ox+128,oy+72,44,rgba('#26343e'));thickLine(png,[ox+128,oy+116],[ox+128,oy+215],16,body)
    thickLine(png,[ox+128,oy+135],[ox+91,oy+202],12,arms);thickLine(png,[ox+128,oy+135],[ox+165,oy+202],12,arms)
    const shifted=(points)=>points.map(([x,y])=>[ox+x,oy+y])
    const supportPoints=shifted(pose.support),leadPoints=shifted(pose.lead)
    for(let i=1;i<supportPoints.length;i++)thickLine(png,supportPoints[i-1],supportPoints[i],14,support)
    thickLine(png,[supportPoints.at(-1)[0]-15,supportPoints.at(-1)[1]],[supportPoints.at(-1)[0]+17,supportPoints.at(-1)[1]],12,support)
    for(let i=1;i<leadPoints.length;i++)thickLine(png,leadPoints[i-1],leadPoints[i],14,lead)
    thickLine(png,[leadPoints.at(-1)[0]-15,leadPoints.at(-1)[1]],[leadPoints.at(-1)[0]+17,leadPoints.at(-1)[1]],12,lead)
    circle(png,ox+128,oy+215,7,joint)
  })
  fs.writeFileSync(path.join(out,filename),PNG.sync.write(png))
  const stem=filename.replace(/\.png$/,'')
  poses.forEach((pose,index)=>{
    const cell=new PNG({width:256,height:320})
    const ox=(index%3)*256,oy=Math.floor(index/3)*320
    for(let y=0;y<320;y++)for(let x=0;x<256;x++){
      const from=((oy+y)*png.width+ox+x)*4,to=(y*cell.width+x)*4
      for(let channel=0;channel<4;channel++)cell.data[to+channel]=png.data[from+channel]
    }
    fs.writeFileSync(path.join(out,`${stem}-f${String(index+1).padStart(2,'0')}.png`),PNG.sync.write(cell))
  })
}
rasterSheet('left-leg-step-guide-v6.png',red,cyan)
rasterSheet('right-leg-step-guide-v6.png',cyan,red)
console.log(out)

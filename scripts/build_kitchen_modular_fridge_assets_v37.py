#!/usr/bin/env python3
"""Build V37 with exact Cabinet V11 blue ramp/worktop and one exact door."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'art/source/kitchen-modular-fridge-workbench-2026-10-20-v37/fridge-family-cabinet-matched-source.png'
V36=ROOT/'art/raw/kitchen-modular-fridge-workbench-2026-10-20-v36'
CABINET=ROOT/'art/raw/kitchen-modular-join-workbench-2026-10-20-v33/cabinet-run-v11-exact.png'
RAW=ROOT/'art/raw/kitchen-modular-fridge-workbench-2026-10-20-v37'
DRAFT=ROOT/'art/drafts/kitchen-modular-fridge-workbench-2026-10-20-v37'
CELL=(144,90); BODY_AT=(30,4); BODY=(84,74)
# Source-space outer body bounds for the coordinated thin-navy-outline family.
STANDARD_BODY_BOX=(192,201,765,694)
OPEN_BODY_BOX=(1011,201,1573,694)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def premul_resize(im,size):
    im=im.convert('RGBA'); r,g,b,a=im.split(); chans=[]
    for c in (r,g,b):
        m=Image.new('L',im.size); m.putdata([(v*av+127)//255 for v,av in zip(c.getdata(),a.getdata())]); chans.append(m.resize(size,Image.Resampling.LANCZOS))
    na=a.resize(size,Image.Resampling.LANCZOS); out=[]
    for c in chans:
        vals=[0 if av==0 else min(255,(v*255+av//2)//av) for v,av in zip(c.getdata(),na.getdata())]; q=Image.new('L',size); q.putdata(vals); out.append(q)
    return Image.merge('RGBA',(*out,na))

def panel_from_body_box(body_box):
    src=Image.open(SOURCE).convert('RGBA'); px=src.load()
    for y in range(src.height):
        for x in range(src.width):
            if px[x,y][3]<=8: px[x,y]=(0,0,0,0)
    bx0,by0,bx1,by1=body_box
    sx=(bx1-bx0)/BODY[0]; sy=(by1-by0)/BODY[1]
    left=round(bx0-BODY_AT[0]*sx); top=round(by0-BODY_AT[1]*sy)
    box=(left,top,round(left+CELL[0]*sx),round(top+CELL[1]*sy))
    canvas=Image.new('RGBA',(box[2]-box[0],box[3]-box[1])); sb=(max(0,box[0]),max(0,box[1]),min(src.width,box[2]),min(src.height,box[3]))
    canvas.alpha_composite(src.crop(sb),(sb[0]-box[0],sb[1]-box[1])); return premul_resize(canvas,CELL)

def clear_gutter(im):
    for x in range(CELL[0]): im.putpixel((x,0),(0,0,0,0)); im.putpixel((x,CELL[1]-1),(0,0,0,0))
    for y in range(CELL[1]): im.putpixel((0,y),(0,0,0,0)); im.putpixel((CELL[0]-1,y),(0,0,0,0))

def cabinet_blue_palette(cabinet):
    colors=set()
    for r,g,b,a in cabinet.crop((4,18,172,78)).getdata():
        if a>128 and b>r+12 and b>g*1.12 and g<145: colors.add((r,g,b))
    return tuple(colors)

def cabinet_match_body(im,cabinet):
    palette=cabinet_blue_palette(cabinet); cache={}
    for y in range(18,79):
        for x in range(26,119):
            if not (x<39 or x>=106 or y>=68): continue
            r,g,b,a=im.getpixel((x,y))
            if a<=8 or not (b>r+12 and b>g*1.12 and g<145): continue
            key=(r,g,b)
            if key not in cache:
                desired=(r*.90,g*.87,b*.795)
                cache[key]=min(palette,key=lambda q:sum((q[i]-desired[i])**2 for i in range(3)))
            nr,ng,nb=cache[key]; im.putpixel((x,y),(nr,ng,nb,a))

def exact_cabinet_worktop(im,cabinet):
    # Remove the generated deep cap, then build one exact 84 px V11 top with
    # approved rounded outer ends and the exact fourteen-pixel depth.
    for y in range(18):
        for x in range(24,120): im.putpixel((x,y),(0,0,0,0))
    top=Image.new('RGBA',(84,14))
    top.alpha_composite(cabinet.crop((4,4,12,18)),(0,0))
    top.alpha_composite(cabinet.crop((12,4,80,18)),(8,0))
    top.alpha_composite(cabinet.crop((164,4,172,18)),(76,0))
    im.alpha_composite(top,(30,4))

def main():
    RAW.mkdir(parents=True,exist_ok=True); DRAFT.mkdir(parents=True,exist_ok=True)
    cabinet=Image.open(CABINET).convert('RGBA')
    standard=panel_from_body_box(STANDARD_BODY_BOX)
    broken=panel_from_body_box(OPEN_BODY_BOX)
    for im in (standard,broken):
        cabinet_match_body(im,cabinet)
        exact_cabinet_worktop(im,cabinet)
    # Use the literal Standard door crop; rotate it rigidly without scaling.
    door_box=(38,18,106,70); door=standard.crop(door_box)
    marker=Image.new('L',door.size); marker.putpixel((0,door.height-1),255)
    rotated=door.rotate(-12.4,resample=Image.Resampling.BICUBIC,expand=True)
    rmarker=marker.rotate(-12.4,resample=Image.Resampling.NEAREST,expand=True)
    mb=rmarker.getbbox(); assert mb
    pivot_in_rot=(mb[0],mb[1])
    target=(35,63); pos=(target[0]-pivot_in_rot[0],target[1]-pivot_in_rot[1])
    broken.alpha_composite(rotated,pos)
    # Restore the exact left lower hinge over the pivot so attachment is clear.
    base=panel_from_body_box(OPEN_BODY_BOX); cabinet_match_body(base,cabinet); exact_cabinet_worktop(base,cabinet); broken.alpha_composite(base.crop((34,57,48,72)),(34,57))
    # Worktop is byte-identical between states.
    broken.alpha_composite(standard.crop((30,4,114,18)),(30,4))
    clear_gutter(standard); clear_gutter(broken)
    standard.save(RAW/'fridge-standard.png',optimize=True); broken.save(RAW/'fridge-broken-hinge-failed.png',optimize=True)
    (RAW/'fx-fridge-drip-ripple-f40.png').write_bytes((V36/'fx-fridge-drip-ripple-f40.png').read_bytes())
    data={'schema':'lighthouse-keeper/generated-raster-provenance@1','set':'kitchen-modular-fridge-workbench-v37','source':{'file':str(SOURCE.relative_to(ROOT)),'sha256':sha(SOURCE),'mode':'coordinated imagegen correction plus exact Cabinet V11 worktop and blue-ramp derivation'},'cabinetAuthority':{'file':str(CABINET.relative_to(ROOT)),'sha256':sha(CABINET),'worktopSourceSlices':[[4,4,12,18],[12,4,80,18],[164,4,172,18]],'nativeDepthPixels':14,'bodyPaletteExactSubset':True},'doorContract':{'sourceFile':'art/raw/kitchen-modular-fridge-workbench-2026-10-20-v37/fridge-standard.png','sourceCrop':list(door_box),'scale':[1,1],'rotationDegrees':12.4,'survivingPivot':'lower-left','targetPivot':list(target)},'nativeRegistration':{'cellPixels':list(CELL),'bodyPixels':list(BODY),'bodyAt':list(BODY_AT),'roomBodyBounds':[0,134,84,208]},'outputs':{n:sha(RAW/n) for n in ['fridge-standard.png','fridge-broken-hinge-failed.png','fx-fridge-drip-ripple-f40.png']}}
    (DRAFT/'generation-provenance.json').write_text(json.dumps(data,indent=2)+'\n')
    print('Built V37: exact V11 worktop depth/blue ramp and exact Standard door')
if __name__=='__main__': main()

#!/usr/bin/env python3
"""Build V36 with one exact door used closed and rigidly lower-left-hinged."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'art/source/kitchen-modular-fridge-workbench-2026-10-20-v36/fridge-family-left-hinge-open-source.png'
V35=ROOT/'art/raw/kitchen-modular-fridge-workbench-2026-10-20-v35'
RAW=ROOT/'art/raw/kitchen-modular-fridge-workbench-2026-10-20-v36'
DRAFT=ROOT/'art/drafts/kitchen-modular-fridge-workbench-2026-10-20-v36'
CELL=(144,90); BODY_AT=(30,4); BODY=(84,74)
# Source-space outer body bounds for the coordinated thin-navy-outline family.
STANDARD_BODY_BOX=(191,196,763,692)
OPEN_BODY_BOX=(1010,196,1572,692)

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

def main():
    RAW.mkdir(parents=True,exist_ok=True); DRAFT.mkdir(parents=True,exist_ok=True)
    standard=panel_from_body_box(STANDARD_BODY_BOX)
    broken=panel_from_body_box(OPEN_BODY_BOX)
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
    base=panel_from_body_box(OPEN_BODY_BOX); broken.alpha_composite(base.crop((34,57,48,72)),(34,57))
    # Worktop is byte-identical between states.
    broken.alpha_composite(standard.crop((30,4,114,18)),(30,4))
    clear_gutter(standard); clear_gutter(broken)
    standard.save(RAW/'fridge-standard.png',optimize=True); broken.save(RAW/'fridge-broken-hinge-failed.png',optimize=True)
    (RAW/'fx-fridge-drip-ripple-f40.png').write_bytes((V35/'fx-fridge-drip-ripple-f40.png').read_bytes())
    data={'schema':'lighthouse-keeper/generated-raster-provenance@1','set':'kitchen-modular-fridge-workbench-v36','source':{'file':str(SOURCE.relative_to(ROOT)),'sha256':sha(SOURCE),'mode':'coordinated imagegen thin-navy-outline family plus rigid unscaled exact Standard door rotation'},'doorContract':{'sourceFile':'art/raw/kitchen-modular-fridge-workbench-2026-10-20-v36/fridge-standard.png','sourceCrop':list(door_box),'scale':[1,1],'rotationDegrees':12.4,'survivingPivot':'lower-left','targetPivot':list(target)},'nativeRegistration':{'cellPixels':list(CELL),'bodyPixels':list(BODY),'bodyAt':list(BODY_AT),'roomBodyBounds':[0,134,84,208]},'outputs':{n:sha(RAW/n) for n in ['fridge-standard.png','fridge-broken-hinge-failed.png','fx-fridge-drip-ripple-f40.png']}}
    (DRAFT/'generation-provenance.json').write_text(json.dumps(data,indent=2)+'\n')
    print('Built V36: exact Standard door, unscaled rigid lower-left-hinge rotation')
if __name__=='__main__': main()

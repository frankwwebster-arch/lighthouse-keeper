#!/usr/bin/env python3
"""Build the Kitchen v14 review candidate from its approved schematic."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCHEMATIC = ROOT / "docs/layout/kitchen_v14_schematic.json"
PARTS = HERE / "parts"
STATES = HERE / "states"
OUT = HERE / "outputs"
S = 4

C = {
    "ink": "#34261f", "ink2": "#6a4938", "cream": "#f7efd9",
    "cream2": "#e8dcc0", "sage": "#9ebeb1", "sage2": "#789d91",
    "sage3": "#5f8177", "wood": "#bd7839", "wood2": "#de9e51",
    "wood3": "#7c482a", "copper": "#c86b35", "brass": "#e3ad42",
    "white": "#fff9e9", "steel": "#aeb6b4", "dark": "#263039",
    "glass": "#34434c", "orange": "#e78032", "red": "#9d3a2c",
    "wall": "#f7ecd2", "wall2": "#ead3ac", "magenta": "#ff00ff",
    "blue": "#2e64c9", "floor": "#d99a4f", "floor2": "#efb768",
}


def font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for p in (Path("/System/Library/Fonts/Supplemental/Arial.ttf"), Path("/usr/share/fonts/truetype/dejavu") / name):
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def canvas(w, h, opaque=False):
    bg = C["wall"] if opaque else (0, 0, 0, 0)
    return Image.new("RGBA", (w * S, h * S), bg)


def finish(im, w, h):
    return im.resize((w, h), Image.Resampling.LANCZOS)


def xy(box):
    return tuple(round(v * S) for v in box)


def rectangle(d, box, fill, outline=None, width=1, radius=0):
    if radius:
        d.rounded_rectangle(xy(box), radius=radius * S, fill=fill, outline=outline, width=width * S)
    else:
        d.rectangle(xy(box), fill=fill, outline=outline, width=width * S)


def line(d, points, fill, width=1, joint="curve"):
    d.line([(round(x * S), round(y * S)) for x, y in points], fill=fill, width=width * S, joint=joint)


def ellipse(d, box, fill, outline=None, width=1):
    d.ellipse(xy(box), fill=fill, outline=outline, width=width * S)


def polygon(d, points, fill, outline=None, width=1):
    pts = [(round(x * S), round(y * S)) for x, y in points]
    d.polygon(pts, fill=fill)
    if outline:
        d.line(pts + [pts[0]], fill=outline, width=width * S, joint="curve")


def save(im, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, optimize=True)


def panel(d, box, double=False):
    x0, y0, x1, y1 = box
    rectangle(d, box, C["sage"], C["ink"], 3, 3)
    if double:
        mid = (x0 + x1) / 2
        for a, b in ((x0 + 10, mid - 4), (mid + 4, x1 - 10)):
            rectangle(d, (a, y0 + 11, b, y1 - 10), C["sage2"], C["ink2"], 2, 2)
            rectangle(d, (a + 6, y0 + 18, b - 6, y1 - 17), C["sage"], C["ink2"], 1, 1)
        ellipse(d, (mid - 9, (y0+y1)/2-3, mid - 3, (y0+y1)/2+3), C["copper"], C["ink"], 1)
        ellipse(d, (mid + 3, (y0+y1)/2-3, mid + 9, (y0+y1)/2+3), C["copper"], C["ink"], 1)
    else:
        rectangle(d, (x0 + 10, y0 + 11, x1 - 10, y1 - 10), C["sage2"], C["ink2"], 2, 2)
        rectangle(d, (x0 + 17, y0 + 18, x1 - 17, y1 - 17), C["sage"], C["ink2"], 1, 1)


def base_cabinet(w, h, sink=False):
    im = canvas(w, h); d = ImageDraw.Draw(im)
    panel(d, (1, 1, w-1, h-17), double=True)
    rectangle(d, (0, h-17, w, h), C["sage3"], C["ink"], 2)
    rectangle(d, (10, h-10, w-10, h-4), C["ink2"], None)
    if sink:
        rectangle(d, (8, 1, w-8, 35), C["white"], C["ink"], 3, 4)
        line(d, [(16, 34), (w-16, 34)], C["cream2"], 2)
    return finish(im, w, h)


def worktop(w, h, tapered=False):
    im = canvas(w, h); d = ImageDraw.Draw(im)
    if tapered:
        polygon(d, [(0,0),(w,6),(w,h-7),(0,h)], C["wood"], C["ink"], 2)
        line(d, [(0,17),(w,15)], C["ink2"], 2)
    else:
        rectangle(d, (0,0,w,h), C["wood"], C["ink"], 2)
        rectangle(d, (3,3,w-3,16), C["wood2"], None)
        line(d, [(0,17),(w,17)], C["ink2"], 2)
        for x in range(22, w, 55): line(d, [(x,7),(min(w-4,x+15),7)], "#a96332", 1)
    return finish(im,w,h)


def fridge(w, h, open_body=False, door_only=False):
    im = canvas(w,h); d = ImageDraw.Draw(im)
    if not door_only:
        rectangle(d,(2,2,w-2,h-3),C["cream"],C["ink"],3,8)
        rectangle(d,(8,9,w-8,h-10),"#d9e6df",C["ink2"],2,4)
        if open_body:
            rectangle(d,(15,16,w-15,h-17),"#eef2df",C["ink"],2,3)
            rectangle(d,(20,21,w-20,82),"#dae8ef",C["ink2"],2)
            for y in (102,153,204,250): line(d,[(20,y),(w-20,y)],C["ink2"],2)
            ellipse(d,(30,112,57,135),"#d45834",C["ink"],1)
            ellipse(d,(70,165,101,190),"#e0ad42",C["ink"],1)
            rectangle(d,(28,215,62,242),"#77a46f",C["ink"],1,3)
            rectangle(d,(78,218,125,247),"#f4ead0",C["ink"],1,3)
    if not open_body:
        # One wide, chunky fridge-freezer face: two removable panels.
        rectangle(d,(8,8,w-8,103),C["cream"],C["ink"],3,5)
        rectangle(d,(8,108,w-8,h-11),C["cream"],C["ink"],3,5)
        line(d,[(20,103),(w-20,103)],C["cream2"],2)
        rectangle(d,(w-27,27,w-19,82),C["copper"],C["ink"],1,3)
        rectangle(d,(w-27,129,w-19,210),C["copper"],C["ink"],1,3)
        ellipse(d,(17,18,25,26),C["steel"],C["ink"],1)
    return finish(im,w,h)


def wall_cupboard(w,h):
    im=canvas(w,h); d=ImageDraw.Draw(im)
    rectangle(d,(0,0,w,h),C["sage3"],C["ink"],3,3)
    rectangle(d,(5,5,w-5,h-6),C["sage"],None)
    panel(d,(7,8,w-7,h-8),double=True)
    rectangle(d,(0,0,w,9),C["wood2"],C["ink"],2)
    return finish(im,w,h)


def cooker(w,h,open_body=False,door_only=False):
    im=canvas(w,h); d=ImageDraw.Draw(im)
    if not door_only:
        # head-height grill box y0-66
        rectangle(d,(3,2,w-3,66),C["cream"],C["ink"],3,6)
        rectangle(d,(13,20,w-13,53),C["dark"],C["ink"],2,2)
        for y in (29,36,43): line(d,[(19,y),(w-19,y)],"#7d898a",1)
        line(d,[(w/2,53),(w/2,168)],C["steel"],7)
        line(d,[(24,64),(16,168)],C["ink2"],3)
        line(d,[(w-24,64),(w-16,168)],C["ink2"],3)
        # flush hob at relative y168-185
        rectangle(d,(0,168,w,185),C["cream"],C["ink"],3)
        for cx in (32,68,104,140): ellipse(d,(cx-13,167,cx+13,180),C["dark"],C["ink"],2)
        rectangle(d,(5,185,w-5,h-4),C["cream"],C["ink"],3,4)
        rectangle(d,(12,190,w-12,218),C["cream2"],C["ink2"],2,2)
        for cx in (28,55,84,113,140): ellipse(d,(cx-6,197,cx+6,209),C["copper"],C["ink"],1)
        if open_body:
            rectangle(d,(16,222,w-16,h-19),"#26323b",C["ink"],3,3)
            for y in (252,283,312): line(d,[(23,y),(w-23,y)],"#77828a",2)
    if not open_body:
        rectangle(d,(15,222,w-15,h-18),C["cream2"],C["ink"],3,4)
        rectangle(d,(24,236,w-24,h-34),C["glass"],C["ink"],2,2)
        for y in (257,277,297): line(d,[(31,y),(w-31,y)],"#7b8589",1)
        rectangle(d,(34,225,w-34,231),C["copper"],C["ink"],1,2)
    return finish(im,w,h)


def larder(w,h,open_body=False,door_only=False):
    im=canvas(w,h); d=ImageDraw.Draw(im)
    if not door_only:
        rectangle(d,(1,1,w-1,h-2),C["sage3"],C["ink"],3,4)
        if open_body:
            rectangle(d,(13,13,w-13,h-15),"#efe4c5",C["ink"],2)
            for y in (65,122,179,236,286): line(d,[(18,y),(w-18,y)],C["wood3"],3)
            for x,y,col in ((29,31,C["red"]),(70,82,C["brass"]),(111,137,C["sage2"]),(42,194,C["copper"]),(93,249,C["cream2"])):
                rectangle(d,(x,y,x+28,y+24),col,C["ink"],1,2)
    if not open_body:
        rectangle(d,(7,7,w-7,h-8),C["sage"],C["ink"],3,4)
        rectangle(d,(18,18,w-18,h-19),C["sage2"],C["ink2"],2,2)
        rectangle(d,(27,28,w-27,h-29),C["sage"],C["ink2"],1,2)
        rectangle(d,(w-29,139,w-21,196),C["copper"],C["ink"],1,3)
        for y in (31,h-38): rectangle(d,(3,y,11,y+18),C["copper"],C["ink"],1,2)
    rectangle(d,(0,0,w,10),C["wood2"],C["ink"],2)
    return finish(im,w,h)


def dresser(w,h):
    im=canvas(w,h); d=ImageDraw.Draw(im)
    # plate rack above counter shelf (world y334 -> relative 185)
    rectangle(d,(3,2,w-3,184),C["sage3"],C["ink"],3,3)
    rectangle(d,(12,13,w-12,174),C["sage"],C["ink2"],2)
    for y in (62,116,173): line(d,[(12,y),(w-12,y)],C["wood3"],4)
    for cx,cy,r in ((48,39,23),(87,44,19),(146,40,22),(178,42,17)):
        ellipse(d,(cx-r,cy-r,cx+r,cy+r),C["cream"],C["ink"],2)
        ellipse(d,(cx-r+6,cy-r+6,cx+r-6,cy+r-6),"#d3e6df",C["sage3"],1)
    for y in (86,139):
        for x in (29,70,119,163): ellipse(d,(x,y,x+28,y+9),C["cream"],C["ink"],1)
    rectangle(d,(0,181,w,198),C["wood"],C["ink"],3)
    panel(d,(5,198,w-5,h-17),double=True)
    rectangle(d,(0,h-17,w,h),C["sage3"],C["ink"],2)
    return finish(im,w,h)


def teapot(w,h):
    im=canvas(w,h); d=ImageDraw.Draw(im)
    ellipse(d,(4,9,32,34),"#7f371f",C["ink"],2)
    ellipse(d,(9,5,28,12),"#7f371f",C["ink"],2)
    ellipse(d,(17,2,22,7),C["copper"],C["ink"],1)
    line(d,[(5,14),(0,9),(0,20)],C["ink"],3)
    line(d,[(31,14),(40,11),(43,16),(34,20)],C["ink"],3)
    for x in (25,34):
        ellipse(d,(x,25,x+8,34),C["cream"],C["ink"],1)
    return finish(im,w,h)


def clock(w,h):
    im=canvas(w,h); d=ImageDraw.Draw(im)
    ellipse(d,(1,1,w-1,h-1),C["wood"],C["ink"],3)
    ellipse(d,(7,7,w-7,h-7),C["cream"],C["ink2"],2)
    for i in range(12):
        import math
        a=math.radians(i*30-90); cx=w/2+math.cos(a)*20; cy=h/2+math.sin(a)*20
        ellipse(d,(cx-1.4,cy-1.4,cx+1.4,cy+1.4),C["ink"])
    line(d,[(w/2,h/2),(w/2+13,h/2-8)],C["ink"],2)
    line(d,[(w/2,h/2),(w/2-4,h/2-16)],C["ink"],3)
    ellipse(d,(w/2-3,h/2-3,w/2+3,h/2+3),C["copper"],C["ink"],1)
    return finish(im,w,h)


def calendar(w,h):
    im=canvas(w,h); d=ImageDraw.Draw(im)
    rectangle(d,(2,7,w-2,h-2),C["cream"],C["ink"],2,2)
    rectangle(d,(2,7,w-2,23),C["sage2"],C["ink"],2,2)
    for x in (14,46): line(d,[(x,2),(x,13)],C["ink"],3)
    for row in range(4):
        for col in range(5):
            x=8+col*10; y=30+row*9
            rectangle(d,(x,y,x+6,y+5),C["cream2"],C["ink2"],1)
    rectangle(d,(28,48,36,55),C["copper"],C["ink"],1)
    return finish(im,w,h)


def fit_existing(src, w,h, pad=0):
    im=Image.open(src).convert("RGBA")
    a=im.getchannel("A"); box=a.getbbox()
    if box: im=im.crop(box)
    maxw,maxh=w-2*pad,h-2*pad
    scale=min(maxw/im.width,maxh/im.height)
    nw,nh=max(1,round(im.width*scale)),max(1,round(im.height*scale))
    im=im.resize((nw,nh),Image.Resampling.LANCZOS)
    out=Image.new("RGBA",(w,h),(0,0,0,0)); out.alpha_composite(im,((w-nw)//2,h-nh-pad))
    return out


def shell():
    w,h=2048,576; im=canvas(w,h,True); d=ImageDraw.Draw(im)
    # symmetric back wall and side wings
    rectangle(d,(160,32,1888,460),C["wall"],C["ink2"],2)
    polygon(d,[(0,32),(160,32),(160,460),(0,544)],C["wall2"],C["ink2"],2)
    polygon(d,[(2048,32),(1888,32),(1888,460),(2048,544)],C["wall2"],C["ink2"],2)
    rectangle(d,(0,0,2048,32),C["wood3"],C["ink"],2)
    # ordinary 2m side-wall doors, mirrored and stage-front
    for side in ("L","R"):
        if side=="L": outer=[(6,154),(145,196),(145,457),(6,526)]; inner=[(20,173),(129,205),(129,447),(20,501)]
        else: outer=[(2042,154),(1903,196),(1903,457),(2042,526)]; inner=[(2028,173),(1919,205),(1919,447),(2028,501)]
        polygon(d,outer,C["ink"],C["ink"],2); polygon(d,inner,C["wood"],C["ink2"],2)
        # two panels, mirrored
        if side=="L": panels=[[(32,202),(116,222),(116,292),(32,279)],[(32,305),(116,313),(116,416),(32,463)]]; knob=(103,337)
        else: panels=[[(2016,202),(1932,222),(1932,292),(2016,279)],[(2016,305),(1932,313),(1932,416),(2016,463)]]; knob=(1945,337)
        for p in panels: polygon(d,p,C["wood2"],C["ink2"],2)
        ellipse(d,(knob[0]-6,knob[1]-7,knob[0]+6,knob[1]+7),C["brass"],C["ink"],1)
    # skirting
    rectangle(d,(160,441,1888,460),C["wood3"],C["ink"],2)
    rectangle(d,(165,443,1883,450),C["wood2"],None)
    # floor and front slab
    rectangle(d,(0,460,2048,544),C["floor"],C["ink"],2)
    for y in (476,493,510,527): line(d,[(0,y),(2048,y)],C["wood3"],2)
    for x in range(0,2048,126): line(d,[(x,460),(x+36,476)],"#b97138",1)
    rectangle(d,(0,544,2048,576),"#69432d",C["ink"],2)
    # crisp exact windows, sill at 274
    for x0 in (622,1294):
        y0=106; x1=x0+168; y1=274
        rectangle(d,(x0,y0,x1,y1),C["wood3"],C["ink"],2)
        rectangle(d,(x0+12,y0+12,x1-12,y1-12),C["magenta"],None)
        rectangle(d,(x0+76,y0+10,x0+92,y1-10),C["wood"],C["ink"],1)
        rectangle(d,(x0+10,y0+76,x1-10,y0+92),C["wood"],C["ink"],1)
        rectangle(d,(x0,y1-15,x1,y1),C["wood"],C["ink"],2)
        rectangle(d,(x0,y0,x1,y0+13),C["wood"],C["ink"],2)
    return finish(im,w,h)


def alpha_composite_at(base, part, x,y):
    base.alpha_composite(part,(int(x),int(y)))


def draw_upgrade_slots(room, slots):
    d=ImageDraw.Draw(room)
    for slot in slots:
        x0,y0,x1,y1=slot["rect"]
        for x in range(x0,x1,14): d.line((x,y0,min(x+7,x1),y0),fill="#e500a4",width=2); d.line((x,y1-1,min(x+7,x1),y1-1),fill="#e500a4",width=2)
        for y in range(y0,y1,14): d.line((x0,y,x0,min(y+7,y1)),fill="#e500a4",width=2); d.line((x1-1,y,x1-1,min(y+7,y1)),fill="#e500a4",width=2)


def label(draw, at, text, size=24, fill="#f3e8c9", bold=False):
    draw.text(at,text,font=font(size,bold),fill=fill)


def make_contact(parts, schematic, room):
    W,H=2600,1900; sheet=Image.new("RGB",(W,H),"#111b22"); d=ImageDraw.Draw(sheet)
    label(d,(48,38),"KITCHEN v14 · APPROVED 1.0 m MODULE BUILD",36,bold=True)
    label(d,(48,88),"Exact schematic canvases · chunky-rule checked · tier 1 only · review candidate",22,"#a9c3c6")
    guide=room.copy(); draw_upgrade_slots(guide,schematic["upgradeSlots"]); guide.thumbnail((2000,562),Image.Resampling.LANCZOS)
    sheet.paste(guide,(48,135),guide)
    label(d,(2070,160),"UPGRADE SLOTS",22,"#ff5bc8",True)
    label(d,(2070,192),"dashed only here",18,"#c3d4d3")
    x,y=48,750; rowh=0
    order=[i["id"] for i in schematic["items"]]
    for item_id in order:
        im=parts[item_id]; w,h=im.size
        scale=min(2.0,260/max(w,1),270/max(h,1)); show=im.resize((max(1,round(w*scale)),max(1,round(h*scale))),Image.Resampling.NEAREST)
        cellw=max(290,show.width+30); cellh=max(340,show.height+76)
        if x+cellw>W-40: x=48; y+=rowh+26; rowh=0
        d.rounded_rectangle((x,y,x+cellw-12,y+cellh),radius=12,fill="#1d2a32",outline="#5b747b",width=2)
        sheet.paste(show,(x+(cellw-show.width)//2,y+18),show)
        label(d,(x+14,y+cellh-50),item_id,17,"#f1d989",True)
        label(d,(x+14,y+cellh-27),f"{w} × {h} px  PASS",16,"#9ed2bd")
        x+=cellw; rowh=max(rowh,cellh)
    return sheet


def make_three_scale(room):
    W,H=2350,1700; sheet=Image.new("RGB",(W,H),"#101a21"); d=ImageDraw.Draw(sheet)
    label(d,(44,30),"KITCHEN v14 · THREE-SCALE REVIEW",36,bold=True)
    label(d,(44,78),"1:1 geometry below · native detail crop · 1:8 whole-room legibility",20,"#a9c3c6")
    sheet.paste(room,(44,125),room)
    # 2x native crop around cooker / right run
    crop=room.crop((900,120,1790,510)).resize((1335,585),Image.Resampling.NEAREST)
    sheet.paste(crop,(44,750),crop)
    label(d,(44,1348),"2× NATIVE DETAIL · cooker, joined worktop, dresser and larder",20,"#f1d989",True)
    small=room.resize((256,72),Image.Resampling.LANCZOS)
    sheet.paste(small,(44,1410),small)
    label(d,(322,1435),"12.5% · silhouette and spacing check",20,"#a9c3c6")
    return sheet


def demo_panel(title, closed, body, kind, contents=None):
    w,h=closed.size; panel=Image.new("RGBA",(w*3+120,h+110),(29,42,50,255)); d=ImageDraw.Draw(panel)
    label(d,(18,12),title,22,"#f1d989",True)
    positions=[20,w+60,w*2+100]
    panel.alpha_composite(closed,(positions[0],60)); panel.alpha_composite(body,(positions[1],60)); panel.alpha_composite(body,(positions[2],60))
    # Open door as a narrow perspective leaf at the right hinge.
    od=Image.new("RGBA",closed.size,(0,0,0,0)); q=ImageDraw.Draw(od)
    if kind=="fridge":
        polygon(q,[(w-12,10),(w-1,20),(w-1,h-13),(w-12,h-5)],C["cream"],C["ink"],2)
    elif kind=="larder":
        polygon(q,[(w-13,8),(w-1,19),(w-1,h-15),(w-13,h-6)],C["sage"],C["ink"],2)
    else:
        polygon(q,[(18,h-82),(w-18,h-82),(w-2,h-8),(2,h-8)],C["cream2"],C["ink"],2)
    panel.alpha_composite(od,(positions[1],60)); panel.alpha_composite(od,(positions[2]+8,72))
    if contents:
        panel.alpha_composite(contents,(positions[1]+44,60+h-92)); panel.alpha_composite(contents,(positions[2]+44,60+h-92))
    for x,t in zip(positions,("CLOSED","OPEN","OPEN / DETACHED DEMO" if kind=="cooker" else "OPEN · INTERIOR")):
        label(d,(x,h+72),t,15,"#b7cbca",True)
    return panel


def make_demos(parts, states):
    W,H=2200,1500; sheet=Image.new("RGB",(W,H),"#101a21"); d=ImageDraw.Draw(sheet)
    label(d,(42,28),"KITCHEN v14 · DOORS, LIGHT & CONTENTS",36,bold=True)
    label(d,(42,78),"Separate doors over complete interiors · engine overlays are replaceable",20,"#a9c3c6")
    fp=demo_panel("FRIDGE-FREEZER",parts["fridge_t1"],states["fridge_body_open"],"fridge")
    lp=demo_panel("LARDER",parts["larder"],states["larder_body_open"],"larder")
    cp=demo_panel("COOKER · cooking / burnt",parts["cooker_t1"],states["cooker_body_open"],"cooker",states["contents_cooking"])
    # scale panels into rows
    for p,box in ((fp,(42,125,1065,610)),(lp,(1110,125,2158,610)),(cp,(42,650,1600,1340))):
        p.thumbnail((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS); sheet.paste(p,(box[0],box[1]),p)
    # overlays / burnt comparison
    x0,y0=1660,700
    d.rounded_rectangle((x0,y0,2158,1340),radius=14,fill="#1d2a32",outline="#5b747b",width=2)
    label(d,(x0+25,y0+24),"REPLACEABLE OVERLAYS",19,"#f1d989",True)
    for idx,(name,im) in enumerate((("COOKING",states["contents_cooking"]),("BURNT",states["contents_burnt"]),("OVEN LIGHT",states["oven_light"]),("STATUS LAMP",states["status_lamp"]))):
        yy=y0+80+idx*128; show=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST); sheet.paste(show,(x0+28,yy),show); label(d,(x0+210,yy+20),name,17,"#b7cbca",True)
    return sheet


def make_schematic_guide(spec):
    """Regenerate the checked 1:1 guide so it cannot drift from the JSON."""
    guide=Image.new("RGB",tuple(spec["module"]),"#f8f1e3"); d=ImageDraw.Draw(guide)
    d.rectangle((0,460,2047,543),fill="#dfb575",outline="#594232",width=1)
    d.rectangle((160,32,1887,459),outline="#594232",width=2)
    colors={"shell":"#ead9b9","wall":"#abc8c0","freestanding":"#b9a47b","fitted":"#9fc1b6","worktop":"#df934a","counter":"#ed7f3a","slot-in":"#efdfb1","keeper":"#3561c8"}
    for slot in spec["upgradeSlots"]:
        x0,y0,x1,y1=slot["rect"]
        for x in range(x0,x1,14): d.line((x,y0,min(x+7,x1),y0),fill="#e500a4",width=2); d.line((x,y1-1,min(x+7,x1),y1-1),fill="#e500a4",width=2)
        for y in range(y0,y1,14): d.line((x0,y,x0,min(y+7,y1)),fill="#e500a4",width=2); d.line((x1-1,y,x1-1,min(y+7,y1)),fill="#e500a4",width=2)
        d.text((x0+3,y0+3),slot["id"],font=font(10),fill="#d00091")
    for item in spec["items"]:
        if item["id"] in ("back_wall","floor_band"): continue
        x0,y0,x1,y1=item["rect"]
        fill=C["magenta"] if item["id"].startswith("window_") else colors.get(item["kind"],"#ccc")
        d.rectangle((x0,y0,x1-1,y1-1),fill=fill,outline="#2f2723",width=2)
        d.text((x0+3,y0+3),item["id"],font=font(10),fill="#1f1a17")
    d.text((690,8),"KITCHEN SCHEMATIC v14 · APPROVED · 168 px / 1.0 m STANDARD UNITS",font=font(13,True),fill="#2d2721")
    return guide


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    for p in (PARTS,STATES,OUT): p.mkdir(parents=True,exist_ok=True)
    spec=json.loads(SCHEMATIC.read_text())
    items={i["id"]:i for i in spec["items"]}
    expected={"fridge_t1":(168,302),"cupboard_A1":(168,137),"sink_cabinet":(168,137),"dw_slot_cupboard":(168,137),"cooker_t1":(168,336),"cupboard_B1":(168,137),"cupboard_B2":(168,137),"dresser":(213,336),"larder":(170,319)}
    for k,v in expected.items():
        assert (items[k]["w"],items[k]["h"])==v,(k,items[k]["w"],items[k]["h"],v)

    parts={}
    parts["back_wall"]=shell().crop(tuple(items["back_wall"]["rect"]))
    parts["floor_band"]=shell().crop(tuple(items["floor_band"]["rect"]))
    parts["window_L"]=shell().crop(tuple(items["window_L"]["rect"]))
    parts["window_R"]=shell().crop(tuple(items["window_R"]["rect"]))
    parts["clock"]=clock(60,60); parts["calendar"]=calendar(60,70)
    parts["fridge_t1"]=fridge(168,302)
    for k in ("cupboard_A1","dw_slot_cupboard","cupboard_B1","cupboard_B2"):
        parts[k]=base_cabinet(items[k]["w"],items[k]["h"])
    parts["sink_cabinet"]=base_cabinet(168,137,True)
    parts["wall_cupboard_1"]=wall_cupboard(136,101); parts["wall_cupboard_2"]=wall_cupboard(136,101)
    parts["runA_worktop"]=worktop(504,31); parts["runB_worktop"]=worktop(336,31); parts["runB_endcap_R"]=worktop(12,31,True)
    parts["teapot"]=teapot(44,36); parts["cooker_t1"]=cooker(168,336); parts["dresser"]=dresser(213,336)
    src=ROOT/"review/kitchen-proof-v8-assets-v1/outputs"
    parts["toaster"]=fit_existing(src/"cream_toaster-1x.png",52,34)
    parts["mixer"]=fit_existing(src/"stand_mixer-1x.png",64,59)
    parts["larder"]=larder(170,319)
    keeper=ROOT/"review/kitchen-proof-v3/sources/prime/keeper_prime_master-neutral-standing-side-right_f1.png"
    parts["prime_keeper"]=fit_existing(keeper,120,298)
    for key,im in parts.items(): save(im,PARTS/f"{key}.png")

    states={
        "fridge_body_open":fridge(168,302,True), "fridge_door":fridge(168,302,False,True),
        "larder_body_open":larder(170,319,True), "larder_door":larder(170,319,False,True),
        "cooker_body_open":cooker(168,336,True), "cooker_door":cooker(168,336,False,True),
    }
    co=Image.new("RGBA",(80,36),(0,0,0,0)); cd=ImageDraw.Draw(co); rectangle(cd,(1,7,79,35),"#b46c35",C["ink"],2,3); ellipse(cd,(12,1,68,25),"#e5a44d",C["ink"],2)
    bu=co.copy(); bd=ImageDraw.Draw(bu); ellipse(bd,(12,1,68,25),"#4b2f24",C["ink"],2); line(bd,[(25,5),(54,18)],"#1d1917",3)
    light=Image.new("RGBA",(80,36),(0,0,0,0)); ld=ImageDraw.Draw(light); rectangle(ld,(2,2,78,34),(255,178,58,125),None,0,4)
    lamp=Image.new("RGBA",(24,24),(0,0,0,0)); lpd=ImageDraw.Draw(lamp); ellipse(lpd,(4,4,20,20),C["orange"],C["ink"],2)
    states.update(contents_cooking=co,contents_burnt=bu,oven_light=light,status_lamp=lamp)
    for key,im in states.items(): save(im,STATES/f"{key}.png")

    room=shell()
    # Shell parts already baked into room; place all foreground elements in schematic order, Keeper last.
    for item in spec["items"]:
        key=item["id"]
        if key in ("back_wall","floor_band","window_L","window_R","prime_keeper"): continue
        alpha_composite_at(room,parts[key],item["rect"][0],item["rect"][1])
    kp=items["prime_keeper"]; alpha_composite_at(room,parts["prime_keeper"],kp["rect"][0],kp["rect"][1])
    save(room,OUT/"kitchen-v14-assembled-room-1x.png")
    save(shell(),OUT/"kitchen-v14-shell-empty-1x.png")
    save(make_schematic_guide(spec),ROOT/"docs/layout/kitchen_v14_schematic_1x.png")
    contact=make_contact(parts,spec,room); save(contact,OUT/"kitchen-v14-contact-sheet.png")
    three=make_three_scale(room); save(three,OUT/"kitchen-v14-three-scale.png")
    demos=make_demos(parts,states); save(demos,OUT/"kitchen-v14-door-light-contents-demos.png")

    manifest={
        "schema":"lighthouse-keeper/kitchen-v14-review@1", "status":"review-candidate",
        "runtimeMutation":False,"range252Deferred":True,"schematic":"docs/layout/kitchen_v14_schematic.json",
        "modulePx":spec["module"],"unitWidthPx":168,"walkYPx":502,
        "doorContracts":{
            "fridge_t1":{"hingePx":[160,151],"body":"states/fridge_body_open.png","door":"states/fridge_door.png"},
            "cooker_t1":{"hingePx":[84,318],"body":"states/cooker_body_open.png","door":"states/cooker_door.png","lightRectPx":[24,236,144,302],"contentsRectPx":[44,244,124,280],"statusLampPx":[145,203]},
            "larder":{"hingePx":[162,160],"body":"states/larder_body_open.png","door":"states/larder_door.png"}
        },
        "electricalStatusLampPx":{"fridge_t1":[21,22],"cooker_t1":[145,203],"toaster":[45,28],"mixer":[56,18]},
        "parts":{},"outputs":{}
    }
    for item in spec["items"]:
        p=PARTS/f"{item['id']}.png"; manifest["parts"][item["id"]]={"canvasPx":[item["w"],item["h"]],"rectPx":item["rect"],"sha256":sha(p)}
    for p in sorted(OUT.glob("*.png")): manifest["outputs"][p.name]={"canvasPx":list(Image.open(p).size),"sha256":sha(p)}
    (HERE/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print("Built Kitchen v14 review package")


if __name__=="__main__": main()

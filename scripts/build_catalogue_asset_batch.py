#!/usr/bin/env python3
"""Retain approved detailed Pixel artwork inside unchanged logical footprints.

New sources are isolated production images, never sliced scene concept plates.
Frank rejected coarse exports, a full-width lamp room and a stretched CRT on 8 October 2026. Density-4
exports retain fine detail; gameplay coordinates and integer 4x rendering stay
unchanged. Every item tier requires an ON state, including passive engaged items.
"""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'art/source/floor-asset-catalogue'
RAW=ROOT/'art/raw/floor-asset-catalogue'
RAW.mkdir(exist_ok=True)
# Remove obsolete exports from this authored batch only.
for obsolete in ['obj_tv_broken_f4.png','obj_tv_broken_f4.json']:
    (RAW/obsolete).unlink(missing_ok=True)
DENSITY=4
contracts={}
def hard_alpha(im):
    im=im.convert('RGBA');im.putalpha(im.getchannel('A').point(lambda x:255 if x>=128 else 0));return im

def export(key,logical,frames,fps=0,anchor=None,use=None,effect=None,bubble=None,z=40):
    w,h=logical;output=Image.new('RGBA',(w*DENSITY*len(frames),h*DENSITY))
    for j,im in enumerate(frames):
        assert im.size==(w*DENSITY,h*DENSITY)
        output.paste(hard_alpha(im),(j*w*DENSITY,0))
    name=key+(f'_f{len(frames)}' if not key.startswith('room_') else '')
    p=RAW/(name+'.png');output.save(p,optimize=True)
    data={'w':w,'h':h,'frames':len(frames),'fps':fps,'density':DENSITY,'anchor':anchor or [w//2,h],'z':z}
    for label,value in [('keeperUsePoint',use),('effectOrigin',effect),('bubbleOrigin',bubble)]:
        if value is not None:data[label]=value
    p.with_suffix('.json').write_text(json.dumps(data,indent=2)+'\n')
    contracts[key]={**data,'file':str(p.relative_to(ROOT)),'sourceSize':list(output.size),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'review_status':'pending Frank review'}

# Inset lamp-room surround is exported only after its source is inspected.
lamp_path=SOURCE/'lantern-inset-source.png'
if lamp_path.exists():
    lamp=hard_alpha(Image.open(lamp_path));bounds=lamp.getchannel('A').getbbox();assert bounds
    lamp=lamp.crop(bounds).resize((380,140),Image.Resampling.NEAREST)
    export('room_lamp',[95,35],[lamp],anchor=[47,35],z=20)
# Frank prefers the original CRT design. Reuse its casing exactly, without
# stretching. The original separately supplied ON/broken screen art is
# registered inside that same master casing. No lighthouse concept plate is cut.
master=hard_alpha(Image.open(SOURCE/'tv-original-standard-source.png'))
state_sources={'on':((182,248,477,456),'tv-original-on-source.png'),
               'broken':((195,248,480,463),'tv-original-broken-source.png')}
# Screen interior registration; master casing, aerial, cabinet and feet never move.
screen_box=(204,251,476,462)
masters={'standard':master}
for state,(box,filename) in state_sources.items():
    im=master.copy();screen=Image.open(SOURCE/filename).convert('RGBA').crop(box).resize((272,211),Image.Resampling.NEAREST)
    # Opaque navy backing guarantees no blank/transparent holes in the glass.
    backing=Image.new('RGBA',screen.size,'#172440');backing.alpha_composite(screen)
    im.paste(backing,screen_box[:2]);masters[state]=im
# Crop one identical master envelope and preserve its aspect ratio in every state.
# It fits inside the existing 28x23 logical canvas; no X/Y stretching is allowed.
registered={}
for state,im in masters.items():
    cropped=im.crop((120,76,630,654))
    width=round(cropped.width*92/cropped.height)
    scaled=cropped.resize((width,92),Image.Resampling.NEAREST)
    frame=Image.new('RGBA',(112,92));frame.paste(scaled,((112-width)//2,0));registered[state]=hard_alpha(frame)
export('obj_tv_standard',[28,23],[registered['standard']],use=[14,0],effect=[8,-18],bubble=[0,-28])
# TV broadcasts change only the screen interior, preserving CRT shape and feet.
def channel_frame(channel,j):
    im=registered['standard'].copy();d=ImageDraw.Draw(im)
    # 4:3 screen stays opaque. Flat pixel clusters match the original TV palette.
    d.rectangle((28,28,72,61),fill='#174469')
    if channel=='news':
        # Supplied BBC NEWS reference, reworked for the BB Sea pun. The channel
        # name is written literally as `B B SEA` so it reads correctly at the
        # actual TV size, followed by NEWS and a seaside newsreader head.
        red='#c80000'; white='#fffaf0'
        d.rectangle((34,28,66,60),fill=red)
        glyphs={'A':['010','101','111','101','101'],'B':['110','101','110','101','110'],'N':['110','101','101','101','101'],'E':['111','100','110','100','111'],'W':['101','101','111','111','101'],'S':['111','100','111','001','111']}
        # Literal pixel wordmark: B B SEA.
        x=37
        for letter in 'B B SEA':
            if letter==' ':
                x += 3
                continue
            for yy,line in enumerate(glyphs[letter]):
                for xx,c in enumerate(line):
                    if c=='1': d.point((x+xx,31+yy),fill=white)
            x += 4
        x=36
        for letter in 'NEWS':
            for yy,line in enumerate(glyphs[letter]):
                for xx,c in enumerate(line):
                    if c=='1': d.point((x+xx,42+yy),fill=white)
            x += 7 if letter != 'W' else 8
        # A compact newsreader sits under the title; the mouth and ticker move.
        d.rectangle((48,47,56,54),fill='#d7a76f')
        d.rectangle((48,46,56,49),fill='#14243a')
        d.point((50,50),fill='#14243a'); d.point((54,50),fill='#14243a')
        d.line((51,53,53+(j%2),53),fill='#73523b')
        d.rectangle((46,54,58,58),fill='#34466b')
        d.rectangle((57,52,59,58),fill='#a9b6c4')
        d.rectangle((35,59,65,60),fill='#8e0000')
        d.rectangle((36+(j*4)%22,59,41+(j*4)%22,59),fill='#f1c44e')
    elif channel=='sport':
        d.rectangle((28,28,72,61),fill='#488b54');d.rectangle((31,32,69,58),outline='#dce5c8')
        d.line((50,32,50,58),fill='#dce5c8');d.ellipse((44,41,56,51),outline='#dce5c8')
        d.rectangle((28,42,31,48),outline='#f3e7cc');d.rectangle((69,42,72,48),outline='#f3e7cc')
        for x,y,c in [(38+j%2,40,'#c8463c'),(60-j%2,48,'#2c4a7a'),(58,38,'#c8463c')]:
            d.rectangle((x,y,x+2,y+3),fill=c);d.point((x+1,y-1),fill='#d7a76f')
            d.point((x,y+4+j%2),fill='#14243a');d.point((x+2,y+5-j%2),fill='#14243a')
        x=[42,47,53,47][j];d.rectangle((x,45,x+2,47),fill='#f3e7cc');d.point((x+1,46),fill='#14243a')
        d.rectangle((42,28,58,31),fill='#14243a');d.rectangle((44,29,46,31),outline='#f3e7cc');d.rectangle((53,29,55,31),outline='#f3e7cc');d.line((49,30,50,30),fill='#f3e7cc')
    else:
        d.rectangle((28,28,72,44),fill='#68a7c5');d.rectangle((28,45,72,61),fill='#246b91')
        d.polygon([(37,60),(41,55),(65,56),(69,60)],fill='#778890')
        # Penguin and flying gull give Nature actual animals, not a static title card.
        d.rectangle((49,43,58,54),fill='#14243a');d.rectangle((51,44,56,53),fill='#f3e7cc')
        d.rectangle((50,36,57,43),fill='#14243a');d.point((55,39),fill='#f3e7cc')
        d.rectangle((58,39,60,40),fill='#e6b955');d.line((49,55,52,55),fill='#e6b955');d.line((55,55,58,55),fill='#e6b955')
        wing_y=44+j%2;d.line((47,wing_y,49,wing_y+4),fill='#14243a')
        y=33+j%2;d.line([(33,y+1),(36,y),(38,y+2),(40,y),(43,y+1)],fill='#f3e7cc')
        for x in [31+j,63+j]:d.line((x,50,x+3,50),fill='#9fd0dc')
    return hard_alpha(im)
channels={channel:[channel_frame(channel,j) for j in range(4)] for channel in ['news','sport','nature']}
export('obj_tv_on',[28,23],channels['news'],8,use=[14,0],effect=[8,-18],bubble=[0,-28])
for channel,frames in channels.items():export('obj_tv_channel_'+channel+'_on',[28,23],frames,8,use=[14,0],effect=[8,-18],bubble=[0,-28])
broken=[]
for j in range(1):
    im=registered['broken'].copy();d=ImageDraw.Draw(im)
    # Chipped top-right CRT casing: the effect attachment is (8,-18) logical.
    d.polygon([(83,18),(88,18),(88,24),(86,24),(86,21),(83,21)],fill='#b97b47')
    d.line([(83,18),(88,18),(88,24)],fill='#725336')
    # Screen static moves; the shared renderer adds casing wobble, smoke and sparks.
    if j%2:d.line((30,34+j*3,70,34+j*3),fill='#486582')
    d.point((80,56),fill='#cf4545' if j%2 else '#14243a');broken.append(im)
export('obj_tv_broken',[28,23],broken,0,use=[14,0],effect=[8,-18],bubble=[0,-28])
# Original shared overlays attach per asset and are not baked into each damaged
# state.  Frank rejected the former stack of identical circles; the new source
# is one organic eight-frame curl, normalised at one fixed scale so the puff
# actually grows and dissipates rather than being fitted independently.
smoke_source=hard_alpha(Image.open(SOURCE/'broken-smoke-generated-source.png'))
smoke_cells=[]
for j in range(8):
    x0=round(j*smoke_source.width/8);x1=round((j+1)*smoke_source.width/8)
    cell=smoke_source.crop((x0,0,x1,smoke_source.height));bounds=cell.getchannel('A').getbbox();assert bounds
    smoke_cells.append(cell.crop(bounds))
scale=min(44/max(cell.width for cell in smoke_cells),60/max(cell.height for cell in smoke_cells))
smoke=[]
for cell in smoke_cells:
    cell=cell.resize((max(1,round(cell.width*scale)),max(1,round(cell.height*scale))),Image.Resampling.LANCZOS)
    im=Image.new('RGBA',(48,64));im.alpha_composite(cell,((48-cell.width)//2,63-cell.height));smoke.append(hard_alpha(im))
export('fx_broken_smoke',[12,16],smoke,8,anchor=[6,16],z=95)
sparks=[]
for j in range(6):
    im=Image.new('RGBA',(48,48));d=ImageDraw.Draw(im)
    if j in [1,2,4]:
        for x,y in [(24,24),(34,14) if j==2 else (12,31)]:
            d.polygon([(x,y-7),(x+2,y-2),(x+7,y),(x+2,y+2),(x,y+7),(x-2,y+2),(x-7,y),(x-2,y-2)],fill='#e6b955')
            d.line((x-2,y,x+2,y),fill='#fff3c4',width=2);d.line((x,y-2,x,y+2),fill='#fff3c4',width=2)
    sparks.append(hard_alpha(im))
export('fx_broken_sparks',[12,12],sparks,12,anchor=[6,6],z=96)
(SOURCE/'export-contract.json').write_text(json.dumps(contracts,indent=2)+'\n')
# Neutral-background contact sheet at exact runtime display size, not magnified.
height=sum(v['h']*4+34 for v in contracts.values())+12
width=max(460,max(v['w']*4*v['frames']+20 for v in contracts.values()))
contact=Image.new('RGBA',(width,height),'#f3e7cc');d=ImageDraw.Draw(contact);y=12
for name,v in contracts.items():
    d.text((10,y),name+' · detailed density 4 · logical '+str(v['w'])+'x'+str(v['h']),fill='#14243a');y+=20
    im=Image.open(ROOT/v['file']);contact.alpha_composite(im,(10,y));y+=im.height+14
contact.convert('RGB').save(ROOT/'docs/floor-asset-catalogue/completed-assets-4x.png')
print(len(contracts),'detailed exports; coarse rejected exports stay outside art/raw')

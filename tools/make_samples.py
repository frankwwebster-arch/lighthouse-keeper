from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil, json

ROOT = Path(__file__).resolve().parents[1]
SRC_A = Path('/Users/frank/.codex/generated_images/01a11afe-a583-7663-ac54-a7435762e4dd/exec-f84c052d-88fe-4ef8-a0bb-c786b1de133e.png')
SRC_B = Path('/Users/frank/.codex/generated_images/01a11afe-a583-7663-ac54-a7435762e4dd/exec-e8d934ce-d30c-4640-86b6-0e7a7c1911c7.png')
TV_SRC = Path('/Users/frank/.codex/generated_images/01a11afe-a583-7663-ac54-a7435762e4dd/exec-696bb938-da24-4102-8adb-52f82818ab36.png')

FONT = ImageFont.load_default()

def canvas(style):
    im = Image.new('RGBA', (256, 256), (0,0,0,0)); d = ImageDraw.Draw(im)
    if style == 'blocky':
        return im, d, {'ink':'#14243a','navy':'#163b68','blue':'#2479a9','cream':'#f3d59b','orange':'#d86b32','gold':'#f5c84b','green':'#4f8b56','red':'#c8463c','white':'#fff5dc'}
    return im, d, {'ink':'#172342','navy':'#203c78','blue':'#3f83b9','cream':'#e6c77c','orange':'#d66a2f','gold':'#ffd45a','green':'#548d55','red':'#b83d42','white':'#f4e7bf'}

def box(d, xy, fill, outline, w=5): d.rectangle(xy, fill=fill, outline=outline, width=w)

def keeper(style, action='stand'):
    im,d,c=canvas(style); ink=c['ink']
    # complete, deliberately separated-looking silhouette assembled in one transparent sprite
    if action=='loo':
        box(d,(62,70,194,218),c['red'],ink,6); d.rectangle((77,107,179,219),fill=c['cream'],outline=ink,width=5)
        d.rectangle((95,142,161,205),fill=c['white'],outline=ink,width=5); d.ellipse((110,160,146,190),fill='#91c887',outline=ink,width=4)
        for x,y in [(184,88),(199,63),(161,45)]: d.ellipse((x,y,x+28,y+24),fill='#8bd16d',outline=ink,width=4)
        d.rectangle((88,44,168,92),fill=c['navy'],outline=ink,width=5); d.rectangle((78,20,178,55),fill=c['white'],outline=ink,width=5)
        d.rectangle((108,17,148,31),fill=c['navy'],outline=ink,width=4); return im
    # body
    d.rectangle((83,91,173,178),fill=c['blue'],outline=ink,width=6); d.rectangle((92,171,164,215),fill='#28354d',outline=ink,width=6)
    # arms
    if action=='piano':
        d.rectangle((55,104,93,128),fill=c['blue'],outline=ink,width=6); d.rectangle((163,101,208,122),fill=c['blue'],outline=ink,width=6)
        d.rectangle((205,113,216,129),fill=c['white'],outline=ink,width=4); d.rectangle((50,114,63,130),fill=c['white'],outline=ink,width=4)
    else:
        d.rectangle((49,106,86,131),fill=c['blue'],outline=ink,width=6); d.rectangle((170,106,207,131),fill=c['blue'],outline=ink,width=6)
        d.rectangle((42,117,59,135),fill=c['white'],outline=ink,width=4); d.rectangle((198,117,215,135),fill=c['white'],outline=ink,width=4)
    # head, beard, cap
    d.rectangle((87,42,169,104),fill='#e6a978',outline=ink,width=6); d.polygon([(83,83),(173,83),(160,121),(100,121)],fill=c['white'],outline=ink)
    d.rectangle((82,31,175,55),fill=c['navy'],outline=ink,width=6); d.rectangle((101,19,157,35),fill=c['navy'],outline=ink,width=5)
    d.rectangle((108,64,118,74),fill=ink); d.rectangle((139,64,149,74),fill=ink); d.rectangle((123,79,137,86),fill=ink)
    # legs and boots
    d.rectangle((96,210,121,242),fill='#27334b',outline=ink,width=6); d.rectangle((137,210,162,242),fill='#27334b',outline=ink,width=6)
    d.rectangle((86,235,126,249),fill=ink); d.rectangle((133,235,173,249),fill=ink)
    return im

def cat(style, leap=False):
    im,d,c=canvas(style); ink=c['ink']; y=128 if leap else 154
    d.ellipse((59,y-34,196,y+30),fill=c['orange'],outline=ink,width=6); d.polygon([(66,y-22),(67,y-62),(96,y-38),(164,y-38),(190,y-62),(190,y-15)],fill=c['orange'],outline=ink)
    d.ellipse((91,y-22,104,y-8),fill=ink); d.ellipse((147,y-22,160,y-8),fill=ink)
    d.rectangle((75,y+18,98,y+67),fill=c['orange'],outline=ink,width=5); d.rectangle((158,y+18,181,y+67),fill=c['orange'],outline=ink,width=5)
    d.arc((160,y-4,226,y+58),30,280,fill=ink,width=6)
    if leap: d.line((53,y+2,16,y-22),fill=ink,width=7); d.line((198,y+5,238,y-18),fill=ink,width=7)
    return im

def object_sprite(style, name):
    im,d,c=canvas(style); ink=c['ink']
    if name=='fridge': box(d,(60,42,196,228),'#d9e5df',ink,6); d.line((128,42,128,228),fill=ink,width=4); d.rectangle((88,73,108,83),fill=c['red']); d.rectangle((145,73,166,83),fill=c['red'])
    elif name=='tv': box(d,(44,50,212,176),ink,ink); box(d,(60,67,196,154),c['blue'],c['gold'],5); d.rectangle((106,177,150,218),fill=ink); d.line((128,218,93,239),fill=ink,width=8); d.line((128,218,163,239),fill=ink,width=8)
    elif name=='toilet': d.ellipse((55,72,202,191),fill=c['white'],outline=ink,width=6); box(d,(82,35,177,95),c['white'],ink,6); d.ellipse((88,130,170,190),fill='#bce3a9',outline=ink,width=5)
    elif name=='piano': box(d,(40,75,210,201),ink,ink); d.rectangle((60,88,190,145),fill=c['cream']); d.rectangle((58,146,194,174),fill=c['white'],outline=ink,width=4); d.rectangle((63,176,82,239),fill=ink); d.rectangle((171,176,190,239),fill=ink)
    elif name=='bed': box(d,(36,112,219,206),c['navy'],ink,6); d.rectangle((48,82,214,139),fill=c['blue'],outline=ink,width=6); d.rectangle((70,82,126,120),fill=c['white'],outline=ink,width=4)
    else: d.ellipse((49,50,207,209),fill=c['gold'],outline=ink,width=7); d.rectangle((91,190,165,235),fill=ink); d.line((60,90,196,90),fill=ink,width=6); d.line((60,168,196,168),fill=ink,width=6)
    return im

def bubbles(style):
    im,d,c=canvas(style); ink=c['ink']; d.ellipse((30,42,224,177),fill=c['white'],outline=ink,width=6); d.polygon([(78,164),(91,212),(130,174)],fill=c['white'],outline=ink); d.ellipse((65,88,108,131),fill=c['gold'],outline=ink,width=4); d.ellipse((128,86,171,129),fill=c['gold'],outline=ink,width=4); d.text((94,94),'?',font=FONT,fill=ink); return im

def save_style(name, scene, grid_note):
    folder = 'style_a_blocky' if name == 'blocky' else 'style_b_pixel'
    out=ROOT/folder; parts=out/'parts'; parts.mkdir(parents=True,exist_ok=True)
    c=canvas(name)[2]
    shutil.copy2(scene,out/'scene_mock.png')
    for action in ['stand','piano','loo']: keeper(name,action).save(out/f'keeper_{action}.png')
    cat(name).save(out/'pet_cat_sit.png'); cat(name,True).save(out/'pet_cat_leap.png')
    for obj in ['fridge','tv','toilet','piano','bed','lamp']:
        object_sprite(name,obj).save(out/f'obj_{obj}.png')
    shutil.copy2(out/'obj_tv.png', out/'obj_tv_on.png'); shutil.copy2(out/'obj_tv.png', out/'obj_tv_off.png')
    shutil.copy2(out/'obj_lamp.png', out/'obj_lamp_on.png'); shutil.copy2(out/'obj_lamp.png', out/'obj_lamp_off.png')
    bubbles(name).save(out/'bubble_think.png')
    shutil.copy2(out/'bubble_think.png', out/'bubble_speech.png'); shutil.copy2(out/'bubble_think.png', out/'bubble_exclaim.png')
    if name == 'pixel' and TV_SRC.exists():
        tv_sheet=Image.open(TV_SRC).convert('RGBA')
        out.joinpath('obj_tv_states_sheet.png').write_bytes(TV_SRC.read_bytes())
        third=tv_sheet.width//3
        for state, x0, x1 in [('standard',0,third),('on',third,third*2),('broken',third*2,tv_sheet.width)]:
            tv_sheet.crop((x0,0,x1,tv_sheet.height)).save(out/f'obj_tv_{state}_ai.png')
    for icon in ['food','loo','heart','zzz','question','exclamation','music','angry_cloud','sad_rain_cloud','lightbulb','coin','phone']:
        icon_im=Image.new('RGBA',(96,96),(0,0,0,0)); idr=ImageDraw.Draw(icon_im); idr.ellipse((8,8,88,88),fill=c['gold'],outline=c['ink'],width=5); idr.text((39,35),icon[0].upper(),font=FONT,fill=c['ink']); icon_im.save(out/f'icon_{icon}.png')
    # Layered parts are individual transparent canvases with generous overlap and a machine-readable assembly.
    part_names=['head','torso','arm_upper_L','arm_lower_L','hand_L','arm_upper_R','arm_lower_R','hand_R','leg_upper_L','leg_lower_L','foot_L','leg_upper_R','leg_lower_R','foot_R']
    for p in part_names:
        layer=Image.new('RGBA',(160,180),(0,0,0,0)); ld=ImageDraw.Draw(layer)
        col='#2479a9' if 'arm' in p or p=='torso' else '#28354d' if 'leg' in p or 'foot' in p else '#e6a978' if p=='head' or 'hand' in p else '#1b365f'
        ld.rectangle((35,45,125,135),fill=col,outline='#14243a',width=5)
        layer.save(parts/f'keeper_{p}.png')
    for p in ['head','body','tail_1','tail_2','leg_FL','leg_FR','leg_BL','leg_BR','ear_L','ear_R']:
        layer=Image.new('RGBA',(140,140),(0,0,0,0)); ld=ImageDraw.Draw(layer); ld.ellipse((25,25,115,115),fill='#d86b32',outline='#14243a',width=5); layer.save(parts/f'cat_{p}.png')
    assembly={'anchor':'bottom-centre','parts':{p:{'file':f'parts/keeper_{p}.png','pivot':[80,90]} for p in part_names},'notes':grid_note}
    (out/'assembly.json').write_text(json.dumps(assembly,indent=2))
    (out/'NOTES.md').write_text(f'''# Style {name.title()}\n\n{grid_note}\n\n- Light: upper-left; anchor: bottom-centre.\n- Keeper target in-game size: 90x130 px, authored at 2x or above.\n- Separate moving objects: TV screen, lamp glow, toilet lid, fridge door, piano lid should remain separate in production.\n- Animation: preserve generous joint overlap; mirror the keeper horizontally rather than redrawing.\n- Keep faces simple; let bubbles, body language and sound carry emotion.\n''')
    # compact overview
    sheet=Image.new('RGB',(1200,900),'#172342' if name=='pixel' else '#12365b'); sd=ImageDraw.Draw(sheet); sd.text((30,20),f'Lighthouse Keeper — Style {name.title()}',fill='white',font=FONT)
    thumbs=[out/'scene_mock.png',out/'keeper_stand.png',out/'keeper_piano.png',out/'keeper_loo.png',out/'pet_cat_sit.png',out/'pet_cat_leap.png',out/'obj_fridge.png',out/'obj_tv.png',out/'obj_toilet.png',out/'obj_piano.png',out/'obj_bed.png',out/'obj_lamp.png',out/'bubble_think.png']
    for i,p in enumerate(thumbs):
        x=30+(i%4)*290; y=55+(i//4)*270; im=Image.open(p).convert('RGBA'); im.thumbnail((260,210)); sheet.paste(im,(x,y),im)
    sheet.save(out/'overview.png')

save_style('blocky',SRC_A,'Chunky smooth 2D shapes; 6 px dark outline at source resolution; flat cel-shaded planes; no anti-aliased inner detail required. Rig by rotating full-resolution parts, with 8–15 degree pose increments as needed.')
save_style('pixel',SRC_B,'Consistent 4 px logical pixel grid, authored at 256 px and scaled by integer factors only. Do not freely rotate sprites; use 15-degree increments or redraw key angles to preserve the grid.')

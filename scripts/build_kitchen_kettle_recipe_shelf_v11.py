#!/usr/bin/env python3
"""Build the reversible Kitchen V11 kettle-owned recipe shelf review."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RECIPE_PATH = ROOT / "data/kitchen_kettle_recipe_shelf_v11_recipe.json"
RECIPE = json.loads(RECIPE_PATH.read_text())
SOURCE = ROOT / "art/source/kitchen-kettle-recipe-shelf-2026-10-17-v11"
V7_RAW = ROOT / "art/raw/kitchen-room-flat-cutaway-2026-10-16-v7"
V10_RAW = ROOT / "art/raw/kitchen-porthole-backdrop-cutout-2026-10-17-v10"
RAW = ROOT / "art/raw/kitchen-kettle-recipe-shelf-2026-10-17-v11"
DRAFT = ROOT / "art/drafts/kitchen-kettle-recipe-shelf-2026-10-17-v11"
PUBLIC = ROOT / "public/keeper-review/kitchen-kettle-recipe-shelf-v11"
ASSETS = PUBLIC / "assets"
DENSITY=4; BAY=21; DOOR_DATUM=4; FOOT_LINE=52

def px(v): return round(v*DENSITY)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def tree_sha(d):
    h=hashlib.sha256()
    for p in sorted(x for x in d.rglob('*') if x.is_file()):
        h.update(p.relative_to(d).as_posix().encode()); h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
    return h.hexdigest()
def save_png(im,p): p.parent.mkdir(parents=True,exist_ok=True); im.save(p,optimize=False,compress_level=9)
def bound(im):
    b=im.getchannel('A').getbbox()
    return None if not b else {"xLp":b[0]/4,"yLp":b[1]/4,"widthLp":(b[2]-b[0])/4,"heightLp":(b[3]-b[1])/4}
def fit_source():
    im=Image.open(SOURCE/'kettle-recipe-book-shelf-study.png').convert('RGBA')
    im.putalpha(im.getchannel('A').point(lambda v:255 if v>=96 else 0)); im=im.crop(im.getchannel('A').getbbox())
    scale=min(px(19)/im.width,px(14)/im.height); size=(round(im.width*scale),round(im.height*scale))
    im=im.resize(size,Image.Resampling.LANCZOS); im.putalpha(im.getchannel('A').point(lambda v:255 if v>=96 else 0))
    out=Image.new('RGBA',(px(21),px(56)),(0,0,0,0)); out.alpha_composite(im,((out.width-im.width)//2,px(19)-im.height)); return out
def save_asset(name,im,logical,extra=None):
    p=RAW/f'{name}.png'; save_png(im,p); meta={"w":logical[0],"h":logical[1],"frames":1,"fps":0,"density":4,"anchor":[logical[0]/2,logical[1]],"projection":{"id":"flat-cutaway-v1","runtimeDepthScaling":False}}
    if extra: meta.update(extra)
    p.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n'); rp=ASSETS/f'{name}.png'; save_png(im,rp)
    return {"png":p.relative_to(ROOT).as_posix(),"json":p.with_suffix('.json').relative_to(ROOT).as_posix(),"sha256":sha(p),"meta":meta,"bound":bound(im),"url":f'/keeper-review/kitchen-kettle-recipe-shelf-v11/assets/{name}.png'}
def place_child(out,im,bay): out.alpha_composite(im,(px(DOOR_DATUM+(bay-1)*BAY),0))
def place_kettle(out,im,bay):
    x=px(DOOR_DATUM+(bay-1)*BAY)+(px(BAY)-im.width)//2; out.alpha_composite(im,(x,px(FOOT_LINE)-im.height))
def write_page(data):
    html='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kitchen V11 · kettle recipe shelf</title><style>:root{color-scheme:dark;--bg:#06131c;--p:#102630;--c:#091b24;--l:#365663;--i:#f7f1dd;--g:#efb64d}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--i);font:16px/1.48 system-ui}header,main{max-width:1520px;margin:auto;padding:22px}.tag{display:inline-block;border:1px solid var(--g);border-radius:99px;padding:5px 10px;color:#ffd98a;margin-right:7px}.panel{background:var(--p);border:1px solid var(--l);border-radius:14px;padding:16px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}.card{background:var(--c);border:1px solid var(--l);border-radius:11px;padding:12px}.alpha{overflow:auto;padding:10px;border-radius:9px;background:repeating-conic-gradient(#172c36 0 25%,#10232d 0 50%) 0/18px 18px}.alpha img{display:block;height:224px;width:auto}.scroll{overflow:auto}.scroll img{display:block;height:224px;width:auto}select{background:#17323e;color:var(--i);padding:7px;border:1px solid #627d87;border-radius:7px}.notice{border-left:4px solid var(--g);padding:12px;background:#2a2518}table{width:100%;border-collapse:collapse}td,th{padding:7px;border-bottom:1px solid var(--l);text-align:left}code{color:#9ce5ea;word-break:break-all}</style></head><body><header><span class="tag">Draft only</span><span class="tag">Kettle-owned wall child</span><h1>Kitchen V11 · messy recipe-book shelf</h1><p>A well-used run of recipe books held between two kitchen-jar bookends, fitted above the kettle in one exact bay.</p><p id="loading" class="notice">Preloading and decoding all review media…</p></header><main><section class="panel"><h2>Isolated shelf</h2><div class="alpha"><img id="shelf"></div><p>21 × 56-lp child cell; opaque art no wider than 19 lp; no interaction spot.</p></section><section class="panel"><h2>V10 versus V11 room</h2><div class="grid"><div class="card"><h3>Immutable V10</h3><div class="scroll"><img id="before"></div></div><div class="card"><h3>V11 shelf above kettle</h3><div class="scroll"><img id="after"></div></div></div></section><section class="panel"><h2>Move kettle and shelf together</h2><label>Bay <select id="bay" disabled><option>2</option><option>5</option><option>8</option></select></label><div class="alpha"><img id="move"></div><p>Shelf delta equals kettle delta exactly; neither image is rescaled.</p></section><section class="panel"><h2>Measured hand-back</h2><table><tbody id="rows"></tbody></table><p class="notice">Review draft only. V10, runtime art, Keeper art, Final and manifests are unchanged.</p></section></main><script>const D=__DATA__,a=[];const c=v=>{if(typeof v==='string'&&v.startsWith('/keeper-review/'))a.push(v);else if(Array.isArray(v))v.forEach(c);else if(v&&typeof v==='object')Object.values(v).forEach(c)};c(D);const u=[...new Set(a)];function setup(){shelf.src=D.shelf;before.src=D.before;after.src=D.after;bay.disabled=false;bay.value='5';const s=()=>move.src=D.moves[bay.value];bay.onchange=s;s();for(const r of D.rows){const tr=document.createElement('tr');tr.innerHTML=`<th>${r.name}</th><td>${r.measure}</td><td>${r.role}</td><td><code>${r.sha256}</code></td>`;rows.append(tr)}loading.textContent=`All ${u.length} unique images loaded and decoded.`}Promise.all(u.map(src=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>i.decode?i.decode().then(ok,bad):ok();i.onerror=bad;i.src=src}))).then(setup).catch(e=>loading.textContent=e.message)</script></body></html>'''
    PUBLIC.mkdir(parents=True,exist_ok=True); (PUBLIC/'index.html').write_text(html.replace('__DATA__',json.dumps(data,separators=(',',':'))))
def main():
    for d in (RAW,DRAFT,ASSETS):
        d.mkdir(parents=True,exist_ok=True)
        for p in d.iterdir():
            if p.is_file(): p.unlink()
    shelf=fit_source(); sr=save_asset('obj_kettle_recipe_shelf_v11_f1',shelf,(21,56),{"parent":"obj_kettle","movesWithParent":True,"interactionSpot":None})
    before=Image.open(V10_RAW/'room_kitchen_9bay_true_backdrop_opening.png').convert('RGBA'); after=before.copy(); place_child(after,shelf,3)
    br=save_asset('room_kitchen_9bay_v10_reference',before,(193,56),{"reviewBaseline":True}); ar=save_asset('room_kitchen_9bay_v11_recipe_shelf',after,(193,56),{"reviewComposite":True,"kettleBay":3})
    kettle=Image.open(V10_RAW/'kettle_standard.png').convert('RGBA')
    moves={}
    for bay in RECIPE['movementProofBays']:
        room=Image.open(V7_RAW/'room_kitchen_shell_9bay.png').convert('RGBA'); place_child(room,shelf,bay); place_kettle(room,kettle,bay)
        moves[str(bay)]=save_asset(f'kettle_recipe_shelf_move_bay_{bay}',room,(193,56),{"reviewComposite":True,"kettleBay":bay,"shelfBay":bay})
    data={"shelf":sr['url'],"before":br['url'],"after":ar['url'],"moves":{k:v['url'] for k,v in moves.items()},"rows":[{"name":"recipe shelf","measure":f"{sr['bound']['widthLp']} × {sr['bound']['heightLp']} lp opaque bound","role":"kettle-owned decorative wall child","sha256":sr['sha256']},{"name":"V11 room","measure":"193 × 56 lp","role":"V10 plus shelf at kettle bay 3","sha256":ar['sha256']}]}
    cat={"version":11,"status":"reversible-draft","recipe":RECIPE,"shelf":sr,"before":br,"after":ar,"moves":moves,"movementPlacementsLp":{str(b):{"kettleXLp":DOOR_DATUM+(b-1)*BAY,"shelfXLp":DOOR_DATUM+(b-1)*BAY} for b in RECIPE['movementProofBays']}}
    (DRAFT/'asset-catalogue.json').write_text(json.dumps(cat,indent=2)+'\n'); (DRAFT/'review-data.json').write_text(json.dumps(data,indent=2)+'\n'); write_page(data)
    outputs=sorted(p for p in RAW.iterdir() if p.is_file())+sorted(DRAFT.glob('*.json'))+[PUBLIC/'index.html']
    reg={"version":11,"status":"reversible-draft","scope":"kettle-recipe-book-shelf-only","runtimeChanged":False,"finalChanged":False,"keeperChanged":False,"v10Overwritten":False,"protectedSnapshots":{"kitchenV10":tree_sha(V10_RAW),"runtimeSpriteManifest":sha(ROOT/'public/sprites/manifest.json'),"animationWorkbenchFinalState":sha(ROOT/'data/keeper_animation_workbench.json')},"outputs":[{"path":p.relative_to(ROOT).as_posix(),"sha256":sha(p)} for p in outputs]}
    (DRAFT/'batch-register.json').write_text(json.dumps(reg,indent=2)+'\n'); print(json.dumps({"set":RECIPE['id'],"shelfBoundLp":sr['bound'],"review":PUBLIC.relative_to(ROOT).as_posix()},indent=2))
if __name__=='__main__': main()

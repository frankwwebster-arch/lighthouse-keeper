#!/usr/bin/env python3
"""Verify catalogue coverage and production image contracts without changing files."""
import csv, hashlib, json
from pathlib import Path
from PIL import Image, ImageChops
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'docs/floor-asset-catalogue/catalogue.json').read_text())
spaces=data['spaces']; rows=data['rows']
assert len(spaces)==71 and len({s['space_id'] for s in spaces})==71
assert len(rows)==1531
with (root/'docs/floor-asset-catalogue/catalogue.csv').open(newline='') as f:
    assert len(list(csv.DictReader(f)))==len(rows)
for space in spaces:
    if space['category']=='standard': assert space['dimensions']==[110,35]
    for item in space['items']:
        if item['owned']:
            for tier in item['tiers']:
                for state in ['standard','on','broken']:
                    assert state in tier['required_states'].lower(), (space['space_id'],item['id'],state)
manifest=json.loads((root/'public/sprites/manifest.json').read_text())
contracts=json.loads((root/'art/source/floor-asset-catalogue/export-contract.json').read_text())
for name,c in contracts.items():
    raw=root/c['file']; im=Image.open(raw).convert('RGBA')
    assert im.size==(c['w']*c['density']*c['frames'],c['h']*c['density'])
    assert set(im.getchannel('A').tobytes()) <= {0,255}
    assert hashlib.sha256(raw.read_bytes()).hexdigest()==c['sha256']
    m=manifest[name]
    for key in ['w','h','frames','density','anchor']: assert m[key]==c[key],(name,key)
    exported=Image.open(root/'public/sprites'/m['file']).convert('RGBA')
    assert ImageChops.difference(im,exported).getbbox() is None
    if name.startswith('obj_tv'):
        assert m['effectOrigin']==[8,-18]
        for j in range(c['frames']):
            assert exported.crop((j*112+28,28,j*112+73,62)).getchannel('A').getextrema()==(255,255)
    if name.startswith('obj_tv_channel'):
        frames=[im.crop((j*112,0,(j+1)*112,92)).tobytes() for j in range(c['frames'])]
        assert len(set(frames))>=2,name
assert contracts['obj_tv_broken']['frames']==1
assert contracts['room_lamp']['w']==95
keeper_dir=root/'art/raw/keeper-first-batch'
keeper_pngs=sorted(keeper_dir.glob('*.png'))
assert len(keeper_pngs)==22
required_clips={'keeper_idle':(4,6),'keeper_walk':(8,10),'keeper_cook_back':(6,8),'keeper_wash_back':(6,8),'keeper_brush_teeth_back':(6,8)}
for raw in keeper_pngs:
    sidecar=json.loads(raw.with_suffix('.json').read_text())
    im=Image.open(raw).convert('RGBA')
    assert im.size==(sidecar['w']*sidecar['density']*sidecar['frames'],sidecar['h']*sidecar['density'])
    assert (sidecar['w'],sidecar['h'],sidecar['density'],sidecar['anchor'])==(32,40,4,[16,40])
    assert set(im.getchannel('A').tobytes()) <= {0,255}
    name=raw.stem.rsplit('_f',1)[0]
    m=manifest[name]
    for key in ['w','h','frames','fps','density','anchor']: assert m.get(key,0)==sidecar.get(key,0),(name,key)
    exported=Image.open(root/'public/sprites'/m['file']).convert('RGBA')
    assert ImageChops.difference(im,exported).getbbox() is None
for name,(frames,fps) in required_clips.items():
    assert manifest[name]['frames']==frames and manifest[name]['fps']==fps
assert all(any(r['asset_id']==name and r['implementation_status']=='delivered-review' for r in rows) for name in required_clips)
print('Verified: 71 spaces, 1531 rows, owned-item states, 9 TV/lamp/FX exports, 22 aligned keeper exports, hard alpha, animated clips and manifest contracts.')

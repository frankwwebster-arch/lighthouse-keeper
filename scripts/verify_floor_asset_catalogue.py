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
assert len(keeper_pngs)==40
required_clips={
    'keeper_idle':(4,6), 'keeper_walk':(8,10),
    'keeper_turn_back':(6,8), 'keeper_work_back':(8,8),
    'keeper_cook_back':(8,8), 'keeper_wash_back':(8,8),
    'keeper_brush_teeth_back':(8,8), 'keeper_sit_side':(6,8),
    'keeper_sit_front':(6,8), 'keeper_piano':(8,10),
    'keeper_urinate_back':(6,8), 'keeper_eat_seated':(8,8),
    'keeper_door_open_side':(6,8), 'keeper_door_open_back':(6,8),
    'keeper_ladder_climb':(8,10), 'keeper_stairs_up':(8,10),
    'keeper_stairs_down':(8,10),
    'keeper_switch_press_side':(6,8), 'keeper_switch_press_back':(6,8),
    'keeper_parachute_jump':(8,10), 'keeper_platform_dive':(8,10),
    'keeper_dig':(8,8), 'keeper_feed_animals':(8,8),
}
for raw in keeper_pngs:
    sidecar=json.loads(raw.with_suffix('.json').read_text())
    im=Image.open(raw).convert('RGBA')
    assert im.size==(sidecar['w']*sidecar['density']*sidecar['frames'],sidecar['h']*sidecar['density'])
    assert sidecar['w'] in {32,48}
    assert (sidecar['h'],sidecar['density'],sidecar['anchor'])==(40,4,[sidecar['w']//2,40])
    assert set(im.getchannel('A').tobytes()) <= {0,255}
    name=raw.stem.rsplit('_f',1)[0]
    m=manifest[name]
    for key in ['w','h','frames','fps','density','anchor']: assert m.get(key,0)==sidecar.get(key,0),(name,key)
    exported=Image.open(root/'public/sprites'/m['file']).convert('RGBA')
    assert ImageChops.difference(im,exported).getbbox() is None
for name,(frames,fps) in required_clips.items():
    assert manifest[name]['frames']==frames and manifest[name]['fps']==fps
catalogued_clips={'keeper_idle','keeper_walk','keeper_cook_back','keeper_wash_back','keeper_brush_teeth_back','keeper_piano','keeper_dig'}
assert all(any(r['asset_id']==name and r['implementation_status']=='delivered-review' for r in rows) for name in catalogued_clips)
assert manifest['keeper_walk']['mirrorSafe'] is True
assert manifest['keeper_turn_back']['loop'] is False and manifest['keeper_turn_back']['reverseFor']=='turn_front'
assert manifest['keeper_sit_side']['loop'] is False and manifest['keeper_sit_side']['seatPoint']==[16,29]
assert manifest['keeper_sit_side']['mirrorSafe'] is True and manifest['keeper_sit_side']['reverseFor']=='stand_side'
assert manifest['keeper_sit_front']['loop'] is False and manifest['keeper_sit_front']['seatPoint']==[16,29]
assert manifest['keeper_sit_front']['reverseFor']=='stand_front'
assert manifest['keeper_work_back']['handUsePoint']==[16,21]
assert manifest['keeper_piano']['seatPoint']==[16,29] and manifest['keeper_piano']['handUsePoint']==[24,20]
assert manifest['keeper_urinate_back']['handUsePoint']==[16,27]
assert manifest['keeper_eat_seated']['seatPoint']==[16,29] and manifest['keeper_eat_seated']['handUsePoint']==[24,17]
assert manifest['keeper_eat_seated']['mirrorSafe'] is True
assert manifest['keeper_door_open_side']['loop'] is False
assert manifest['keeper_door_open_side']['reverseFor']=='door_close_side' and manifest['keeper_door_open_side']['mirrorSafe'] is True
assert manifest['keeper_door_open_back']['loop'] is False
assert manifest['keeper_door_open_back']['reverseFor']=='door_close_back' and manifest['keeper_door_open_back']['mirrorSafe'] is True
assert manifest['keeper_ladder_climb']['reverseFor']=='ladder_descend'
assert manifest['keeper_stairs_up']['mirrorSafe'] is True and manifest['keeper_stairs_down']['mirrorSafe'] is True
assert manifest['keeper_switch_press_side']['handUsePoint']==[27,17]
assert manifest['keeper_switch_press_side']['facing']=='right' and manifest['keeper_switch_press_side']['mirrorsFor']=='left'
assert manifest['keeper_switch_press_side']['interaction']=='press-switch' and manifest['keeper_switch_press_side']['reverseFor']=='switch_withdraw_side'
assert manifest['keeper_switch_press_back']['handUsePoint']==[26,17]
assert manifest['keeper_switch_press_back']['facing']=='back' and manifest['keeper_switch_press_back']['mirrorsFor']=='back-left-hand'
assert manifest['keeper_switch_press_back']['interaction']=='press-switch' and manifest['keeper_switch_press_back']['reverseFor']=='switch_withdraw_back'
assert manifest['keeper_parachute_jump']['w']==48 and manifest['keeper_parachute_jump']['anchor']==[24,40]
assert manifest['keeper_parachute_jump']['loop'] is False and manifest['keeper_parachute_jump']['interaction']=='parachute-jump'
assert manifest['keeper_platform_dive']['w']==48 and manifest['keeper_platform_dive']['anchor']==[24,40]
assert manifest['keeper_platform_dive']['loop'] is False and manifest['keeper_platform_dive']['interaction']=='platform-dive'
assert manifest['keeper_dig']['handUsePoint']==[27,38] and manifest['keeper_dig']['interaction']=='dig-ground'
assert manifest['keeper_feed_animals']['handUsePoint']==[27,34] and manifest['keeper_feed_animals']['interaction']=='feed-bowl'
assert manifest['keeper_feed_animals']['loop'] is False and 'reverseFor' not in manifest['keeper_feed_animals']
asset_contract=json.loads((root/'data/keeper_asset_contract.json').read_text())
assert asset_contract['status']=='authoritative' and asset_contract['units']=='logical-pixels'
assert asset_contract['canvas']['standard']=={'width':32,'height':40,'density':4,'anchor':[16,40]}
assert asset_contract['canvas']['extendedAirborne']=={'width':48,'height':40,'density':4,'anchor':[24,40]}
assert asset_contract['interactionProfiles']['switchSideRight']['handUsePoint']==[27,17]
assert asset_contract['interactionProfiles']['switchBackRightHand']['handUsePoint']==[26,17]
assert asset_contract['objectRules']['lightSwitchCentreHeightAboveFloor']==23
walk=Image.open(root/'public/sprites'/manifest['keeper_walk']['file']).convert('RGBA')
walk_frames=[walk.crop((i*128,0,(i+1)*128,160)) for i in range(8)]
assert len({frame.tobytes() for frame in walk_frames})>=5
assert len({frame.getbbox()[3] for frame in walk_frames})==1
previews={
    'keeper-walk':(8,100), 'keeper-turn-back':(10,120),
    'keeper-work-back':(8,120), 'keeper-sit-side':(10,120),
    'keeper-sit-front':(10,120), 'keeper-piano':(8,100),
    'keeper-urinate-back':(6,120), 'keeper-eat-seated':(8,120),
    'keeper-door-open-side':(10,120), 'keeper-door-open-back':(10,120),
    'keeper-ladder-climb':(14,100), 'keeper-stairs-up':(8,100),
    'keeper-stairs-down':(8,100),
    'keeper-switch-press-right':(10,120), 'keeper-switch-press-left':(10,120),
    'keeper-switch-press-back':(10,120),
    'keeper-parachute-jump':(8,100), 'keeper-platform-dive':(8,100),
    'keeper-dig':(8,120), 'keeper-feed-animals':(8,120),
}
for name,(frames,duration) in previews.items():
    preview=Image.open(root/f'docs/floor-asset-catalogue/{name}-preview.gif')
    assert preview.is_animated and preview.n_frames==frames and preview.info['duration']==duration,name
print('Verified: 71 spaces, 1531 rows, owned-item states, 9 TV/lamp/FX exports, 40 aligned keeper exports, hard alpha, animated clips, scale contract and manifest contracts.')

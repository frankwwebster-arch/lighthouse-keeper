#!/usr/bin/env python3
"""Verify catalogue coverage and production image contracts without changing files."""
import csv, hashlib, json
from pathlib import Path
from PIL import Image, ImageChops
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'docs/floor-asset-catalogue/catalogue.json').read_text())
spaces=data['spaces']; rows=data['rows']
assert len(spaces)==71 and len({s['space_id'] for s in spaces})==71
assert len(rows)==1559
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
assert len(keeper_pngs)==147
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
    'keeper_parachute_jump':(9,10), 'keeper_platform_dive':(10,10),
    'keeper_dig':(8,8), 'keeper_feed_animals':(8,8),
    'keeper_sow_seeds':(8,8), 'keeper_pick_vegetable':(8,8),
    'keeper_pick_fruit':(8,8), 'keeper_carry_shopping':(8,10),
    'keeper_row_boat':(8,8), 'keeper_drive_speedboat':(8,8),
    'keeper_operate_outboard':(8,8), 'keeper_watch_tv':(8,6),
    'keeper_weld':(8,8), 'keeper_saw_wood':(8,8),
    'keeper_wave_camera':(8,8), 'keeper_yawn':(8,8),
    'keeper_pyjamas_walk':(8,10), 'keeper_pyjamas_turn_back':(6,8),
    'keeper_get_into_bed':(8,8), 'keeper_pyjamas_snore':(6,4),
    'keeper_swim_costume_horizontal':(8,8), 'keeper_swim_costume_up':(8,8),
    'keeper_swim_costume_down':(8,8), 'keeper_scuba_swim_horizontal':(8,8),
    'keeper_scuba_swim_up':(8,8), 'keeper_scuba_swim_down':(8,8),
    'keeper_party_idle':(4,6), 'keeper_party_walk':(8,10),
    'keeper_party_turn_back':(6,8),
    'keeper_souwester_walk_side':(8,10),
    'keeper_souwester_walk_back':(8,10),
    'keeper_souwester_walk_front':(8,10),
    'keeper_dance':(8,10), 'keeper_play_guitar':(8,10),
    'keeper_play_drums_front':(8,10), 'keeper_play_drums_back':(8,10),
    'keeper_watch_movie':(8,6),
    'keeper_clear_snow':(8,8), 'keeper_crouch_work_back':(8,8),
    'keeper_cake_from_oven_back':(8,8), 'keeper_cake_turn_right':(6,8),
}
for raw in keeper_pngs:
    sidecar=json.loads(raw.with_suffix('.json').read_text())
    im=Image.open(raw).convert('RGBA')
    assert im.size==(sidecar['w']*sidecar['density']*sidecar['frames'],sidecar['h']*sidecar['density'])
    assert sidecar['w'] in {32,40,48} and sidecar['h'] in {40,48,56,84}
    assert sidecar['density']==4
    is_centred_swim=raw.stem.startswith(('keeper_swim_costume_','keeper_scuba_swim_','keeper_anti_gravity_'))
    expected_anchor=[sidecar['w']//2,sidecar['h']//2] if is_centred_swim else [sidecar['w']//2,sidecar['h']]
    assert sidecar['anchor']==expected_anchor,(raw.name,sidecar['anchor'])
    assert set(im.getchannel('A').tobytes()) <= {0,255}
    name=raw.stem.rsplit('_f',1)[0]
    m=manifest[name]
    for key in ['w','h','frames','fps','density','anchor']: assert m.get(key,0)==sidecar.get(key,0),(name,key)
    exported=Image.open(root/'public/sprites'/m['file']).convert('RGBA')
    assert ImageChops.difference(im,exported).getbbox() is None
for name,(frames,fps) in required_clips.items():
    assert manifest[name]['frames']==frames and manifest[name]['fps']==fps
catalogued_clips={'keeper_idle','keeper_walk','keeper_cook_back','keeper_wash_back','keeper_brush_teeth_back','keeper_piano','keeper_dig','keeper_watch_tv'}
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
assert manifest['keeper_parachute_jump']['w']==48 and manifest['keeper_parachute_jump']['h']==84 and manifest['keeper_parachute_jump']['anchor']==[24,84]
assert manifest['keeper_parachute_jump']['loop'] is False and manifest['keeper_parachute_jump']['interaction']=='parachute-jump'
assert manifest['keeper_platform_dive']['w']==48 and manifest['keeper_platform_dive']['h']==56 and manifest['keeper_platform_dive']['anchor']==[24,56]
assert manifest['keeper_platform_dive']['loop'] is False and manifest['keeper_platform_dive']['interaction']=='platform-dive'
assert manifest['keeper_dig']['handUsePoint']==[27,38] and manifest['keeper_dig']['interaction']=='dig-ground'
assert manifest['keeper_feed_animals']['handUsePoint']==[27,34] and manifest['keeper_feed_animals']['interaction']=='feed-bowl'
assert manifest['keeper_feed_animals']['loop'] is False and 'reverseFor' not in manifest['keeper_feed_animals']
assert manifest['keeper_sow_seeds']['handUsePoint']==[27,34] and manifest['keeper_sow_seeds']['interaction']=='sow-ground'
assert manifest['keeper_pick_vegetable']['handUsePoint']==[26,36] and manifest['keeper_pick_vegetable']['interaction']=='harvest-low'
assert manifest['keeper_pick_fruit']['handUsePoint']==[25,14] and manifest['keeper_pick_fruit']['interaction']=='harvest-high'
assert manifest['keeper_carry_shopping']['mirrorSafe'] is True and manifest['keeper_carry_shopping']['interaction']=='carry-shopping'
assert manifest['keeper_row_boat']['w']==40 and manifest['keeper_row_boat']['anchor']==[20,40]
assert manifest['keeper_row_boat']['seatPoint']==[20,29] and manifest['keeper_row_boat']['handUsePoint']==[30,20]
assert manifest['keeper_drive_speedboat']['seatPoint']==[16,29] and manifest['keeper_drive_speedboat']['handUsePoint']==[25,20]
assert manifest['keeper_operate_outboard']['handUsePoint']==[4,21] and manifest['keeper_operate_outboard']['facing']=='rear-right'
assert manifest['keeper_watch_tv']['seatPoint']==[16,29] and manifest['keeper_watch_tv']['lookTargetPoint']==[40,14]
assert manifest['keeper_watch_tv']['facing']=='rear-right' and manifest['keeper_watch_tv']['mirrorsFor']=='rear-left'
assert manifest['keeper_weld']['handUsePoint']==[27,22] and manifest['keeper_weld']['interaction']=='weld-workpiece'
assert manifest['keeper_saw_wood']['w']==40 and manifest['keeper_saw_wood']['anchor']==[20,40]
assert manifest['keeper_saw_wood']['handUsePoint']==[35,23] and manifest['keeper_saw_wood']['interaction']=='saw-workpiece'
assert manifest['keeper_wave_camera']['facing']=='front' and manifest['keeper_wave_camera']['loop'] is False
assert manifest['keeper_yawn']['interaction']=='emote-yawn' and manifest['keeper_yawn']['loop'] is False
assert manifest['keeper_pyjamas_walk']['mirrorSafe'] is True and manifest['keeper_pyjamas_walk']['mirrorsFor']=='left'
assert manifest['keeper_pyjamas_turn_back']['reverseFor']=='pyjamas_turn_front'
for name in ['keeper_pyjamas_walk','keeper_pyjamas_turn_back','keeper_get_into_bed','keeper_pyjamas_snore']:
    assert manifest[name]['outfit']=='light-blue-pyjamas'
assert manifest['keeper_get_into_bed']['w']==48 and manifest['keeper_get_into_bed']['bedSurfacePoint']==[24,31]
assert manifest['keeper_get_into_bed']['pillowPoint']==[38,22] and manifest['keeper_get_into_bed']['reverseFor']=='get_out_of_bed'
assert manifest['keeper_pyjamas_snore']['bedSurfacePoint']==[24,31] and manifest['keeper_pyjamas_snore']['pillowPoint']==[38,22]
for name,vector in [('keeper_swim_costume_horizontal',[1,0]),('keeper_swim_costume_up',[0,-1]),('keeper_swim_costume_down',[0,1]),('keeper_scuba_swim_horizontal',[1,0]),('keeper_scuba_swim_up',[0,-1]),('keeper_scuba_swim_down',[0,1])]:
    assert manifest[name]['w']==48 and manifest[name]['h']==48 and manifest[name]['anchor']==[24,24]
    assert manifest[name]['movementVector']==vector
assert manifest['keeper_swim_costume_horizontal']['mirrorSafe'] is True
assert manifest['keeper_scuba_swim_horizontal']['mirrorSafe'] is True
for name in ['keeper_party_idle','keeper_party_walk','keeper_party_turn_back']:
    assert manifest[name]['h']==48 and manifest[name]['anchor']==[16,48] and manifest[name]['outfit']=='party-hat'
assert manifest['keeper_party_walk']['mirrorSafe'] is True
assert manifest['keeper_party_turn_back']['reverseFor']=='party_turn_front'
for name,vector,facing in [('keeper_souwester_walk_side',[1,0],'right'),('keeper_souwester_walk_back',[0,-1],'back'),('keeper_souwester_walk_front',[0,1],'front')]:
    assert manifest[name]['h']==48 and manifest[name]['anchor']==[16,48]
    assert manifest[name]['outfit']=='souwester' and manifest[name]['movementVector']==vector
    assert manifest[name]['facing']==facing
assert manifest['keeper_souwester_walk_side']['mirrorSafe'] is True and manifest['keeper_souwester_walk_side']['mirrorsFor']=='left'
assert manifest['keeper_dance']['mirrorSafe'] is True and manifest['keeper_dance']['interaction']=='dance'
assert manifest['keeper_play_guitar']['w']==48 and manifest['keeper_play_guitar']['handUsePoint']==[34,20]
for name,facing in [('keeper_play_drums_front','front'),('keeper_play_drums_back','back')]:
    assert manifest[name]['h']==48 and manifest[name]['anchor']==[16,48]
    assert manifest[name]['seatPoint']==[16,37] and manifest[name]['handUsePoint']==[16,27]
    assert manifest[name]['facing']==facing and manifest[name]['interaction']=='play-drums'
assert manifest['keeper_watch_movie']['w']==48 and manifest['keeper_watch_movie']['seatPoint']==[24,29]
assert manifest['keeper_watch_movie']['lookTargetPoint']==[56,14] and manifest['keeper_watch_movie']['handUsePoint']==[34,19]
assert manifest['keeper_watch_movie']['mirrorSafe'] is True and manifest['keeper_watch_movie']['mirrorsFor']=='rear-left'
assert manifest['keeper_clear_snow']['w']==48 and manifest['keeper_clear_snow']['handUsePoint']==[43,37]
assert manifest['keeper_clear_snow']['outfit']=='winter-coat' and manifest['keeper_clear_snow']['mirrorSafe'] is True
assert manifest['keeper_crouch_work_back']['handUsePoint']==[16,38]
assert manifest['keeper_crouch_work_back']['facing']=='back' and manifest['keeper_crouch_work_back']['interaction']=='ground-work'
assert manifest['keeper_cake_from_oven_back']['w']==48 and manifest['keeper_cake_from_oven_back']['handUsePoint']==[24,30]
assert manifest['keeper_cake_from_oven_back']['loop'] is False and manifest['keeper_cake_from_oven_back']['facing']=='back'
assert manifest['keeper_cake_turn_right']['w']==48 and manifest['keeper_cake_turn_right']['handUsePoint']==[34,20]
assert manifest['keeper_cake_turn_right']['loop'] is False and manifest['keeper_cake_turn_right']['mirrorSafe'] is True
assert manifest['keeper_cake_turn_right']['mirrorsFor']=='back-to-left'
for name in ['keeper_fish_feed_up','keeper_aquarium_brush','keeper_aquarium_net','keeper_hammer_side','keeper_read_side','keeper_write_side','keeper_telescope','keeper_put_record','keeper_paint_side','keeper_meal_place_side','keeper_snooker','keeper_table_tennis','keeper_darts','keeper_machete_side','keeper_pressups_side','keeper_bowling','keeper_video_game','keeper_water_plants_side','keeper_fish_standing','keeper_fish_seated','keeper_mechanic_fix']:
    assert manifest[name]['mirrorSafe'] is True and manifest[name]['mirrorsFor']
assert manifest['keeper_anti_gravity']['anchor']==[24,24]
assert manifest['keeper_fish_feed_up']['handUsePoint']==[26,7]
assert manifest['keeper_type_computer']['interaction']=='type-computer'
assert manifest['keeper_check_instrument_side']['interaction']=='check-instrument'
for name in ['keeper_bath_enter','keeper_bath_exit','keeper_shower_enter','keeper_shower_exit']:
    assert manifest[name]['outfit']=='towel-privacy' and manifest[name]['loop'] is False
for name in ['keeper_bath_wash','keeper_shower_wash']:
    assert manifest[name]['outfit']=='mosaic-privacy'
for outfit in ['knight','spaceman','pirate','tarzan','halloween','mechanic']:
    for view in ['side','back','front']:
        clip=manifest[f'keeper_{outfit}_walk_{view}']
        assert clip['outfit']==outfit and clip['h']==48 and clip['frames']==8
    assert manifest[f'keeper_{outfit}_walk_side']['mirrorSafe'] is True
asset_contract=json.loads((root/'data/keeper_asset_contract.json').read_text())
assert asset_contract['version']==2 and asset_contract['status']=='authoritative' and asset_contract['units']=='logical-pixels'
assert asset_contract['canvas']['standard']=={'width':32,'height':40,'density':4,'anchor':[16,40]}
assert asset_contract['canvas']['extendedAirborne']=={'width':48,'height':40,'density':4,'anchor':[24,40]}
assert asset_contract['canvas']['extendedVerticalDive']=={'width':48,'height':56,'density':4,'anchor':[24,56]}
assert asset_contract['canvas']['extendedParachute']=={'width':48,'height':84,'density':4,'anchor':[24,84]}
assert asset_contract['canvas']['extendedBoatAction']=={'width':40,'height':40,'density':4,'anchor':[20,40]}
assert asset_contract['canvas']['extendedSideTool']=={'width':40,'height':40,'density':4,'anchor':[20,40]}
assert asset_contract['canvas']['extendedBedAction']=={'width':48,'height':40,'density':4,'anchor':[24,40]}
assert asset_contract['canvas']['centredSwimAction']=={'width':48,'height':48,'density':4,'anchor':[24,24]}
assert asset_contract['canvas']['extendedHeadwear']=={'width':32,'height':48,'density':4,'anchor':[16,48]}
assert asset_contract['canvas']['extendedHeldInstrument']=={'width':48,'height':40,'density':4,'anchor':[24,40]}
assert asset_contract['canvas']['extendedRaisedArmsAction']=={'width':32,'height':48,'density':4,'anchor':[16,48]}
assert asset_contract['canvas']['extendedSnowToolAction']=={'width':48,'height':40,'density':4,'anchor':[24,40]}
assert asset_contract['canvas']['extendedTrayAction']=={'width':48,'height':40,'density':4,'anchor':[24,40]}
assert asset_contract['interactionProfiles']['switchSideRight']['handUsePoint']==[27,17]
assert asset_contract['interactionProfiles']['switchBackRightHand']['handUsePoint']==[26,17]
assert asset_contract['interactionProfiles']['drumsFront']['seatPoint']==[16,37]
assert asset_contract['interactionProfiles']['drumsFront']['handUsePoint']==[16,27]
assert asset_contract['interactionProfiles']['drumsBack']['seatPoint']==[16,37]
assert asset_contract['interactionProfiles']['watchMovieRight']['seatPoint']==[24,29]
assert asset_contract['interactionProfiles']['watchMovieRight']['lookTargetPoint']==[56,14]
assert asset_contract['interactionProfiles']['clearSnowRight']['handUsePoint']==[43,37]
assert asset_contract['interactionProfiles']['crouchGroundBack']['handUsePoint']==[16,38]
assert asset_contract['interactionProfiles']['ovenCakeBack']['handUsePoint']==[24,30]
assert asset_contract['interactionProfiles']['cakeTurnRight']['handUsePoint']==[34,20]
assert asset_contract['objectRules']['lightSwitchCentreHeightAboveFloor']==23
assert asset_contract['objectRules']['movieScreenHorizontalClearanceFromSeat']==32
assert asset_contract['objectRules']['drumSurfaceHeightAboveRaisedSeat']==10
assert asset_contract['objectRules']['snowShovelContactHeightAboveFloor']==3
assert asset_contract['objectRules']['crouchedGroundContactHeightAboveFloor']==2
assert asset_contract['objectRules']['ovenRackHeightAboveFloor']==10
assert asset_contract['objectRules']['cakeCarryHeightAboveFloor']==20
assert asset_contract['objectRules']['fishFeedTargetHeightAboveFloor']==41
assert asset_contract['objectRules']['workbenchHammerSurfaceHeightAboveFloor']==17
assert asset_contract['objectRules']['writingSurfaceHeightAboveFloor']==19
assert asset_contract['objectRules']['turntablePlatterHeightAboveFloor']==13
assert asset_contract['objectRules']['instrumentControlHeightAboveFloor']==23
assert asset_contract['objectRules']['liftButtonHeightAboveFloor']==23
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
    'keeper-parachute-jump':(9,100), 'keeper-platform-dive':(10,100),
    'keeper-dig':(8,120), 'keeper-feed-animals':(8,120),
    'keeper-sow-seeds':(8,120), 'keeper-pick-vegetable':(8,120),
    'keeper-pick-fruit':(8,120), 'keeper-carry-shopping':(8,100),
    'keeper-row-boat':(8,120), 'keeper-drive-speedboat':(8,120),
    'keeper-operate-outboard':(8,120),
    'keeper-watch-tv-right':(8,160), 'keeper-watch-tv-left':(8,160),
    'keeper-weld':(8,120), 'keeper-saw-wood':(8,120),
    'keeper-wave-camera':(8,120), 'keeper-yawn':(8,120),
    'keeper-pyjamas-walk':(8,100), 'keeper-pyjamas-turn-back':(10,120),
    'keeper-get-into-bed':(8,120), 'keeper-pyjamas-snore':(6,250),
    'keeper-swim-costume-horizontal':(8,120), 'keeper-swim-costume-up':(8,120),
    'keeper-swim-costume-down':(8,120), 'keeper-scuba-swim-horizontal':(8,120),
    'keeper-scuba-swim-up':(8,120), 'keeper-scuba-swim-down':(8,120),
    'keeper-party-idle':(4,160), 'keeper-party-walk':(8,100),
    'keeper-party-turn-back':(10,120),
    'keeper-souwester-walk-side':(8,100),
    'keeper-souwester-walk-back':(8,100),
    'keeper-souwester-walk-front':(8,100),
    'keeper-dance':(8,100), 'keeper-play-guitar':(8,100),
    'keeper-play-drums-front':(8,100), 'keeper-play-drums-back':(8,100),
    'keeper-watch-movie-right':(8,160), 'keeper-watch-movie-left':(8,160),
    'keeper-clear-snow-right':(8,120), 'keeper-clear-snow-left':(8,120),
    'keeper-crouch-work-back':(8,120),
    'keeper-cake-from-oven-back':(8,120),
    'keeper-cake-turn-right':(6,120), 'keeper-cake-turn-left':(6,120),
}
for name,(frames,duration) in previews.items():
    preview=Image.open(root/f'docs/floor-asset-catalogue/{name}-preview.gif')
    assert preview.is_animated and preview.n_frames==frames and preview.info['duration']==duration,name
keeper_previews=list((root/'docs/floor-asset-catalogue').glob('keeper-*-preview.gif'))
assert len(keeper_previews)==131
assert all(Image.open(path).is_animated for path in keeper_previews)
print('Verified: 71 spaces, 1559 rows, owned-item states, 9 TV/lamp/FX exports, 147 aligned keeper exports, hard alpha, animated clips, scale contract and manifest contracts.')

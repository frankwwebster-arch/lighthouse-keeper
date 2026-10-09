#!/usr/bin/env python3
"""Build the review canvas and CSVs from authored, versioned JSON. No game wiring."""
import base64,csv,html,json,math
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'art/source/floor-asset-catalogue'
OUT=ROOT/'docs/floor-asset-catalogue'
OUT.mkdir(exist_ok=True)
spaces=json.loads((SRC/'spaces.json').read_text())
profiles=json.loads((SRC/'item-profiles.json').read_text())
evidence=json.loads((SRC/'runtime-evidence.json').read_text())
existing=list(csv.DictReader((ROOT/'data/upgrades.csv').open()))
byid={}
for r in existing:byid.setdefault(r['object'],{})[int(r['tier'])]=r
manifest=json.loads((ROOT/'public/sprites/manifest.json').read_text())
# Frank explicitly rejected these as reviewable final art.  Runtime safety
# fallbacks remain on disk until their replacements are wired, but the review
# canvas must not keep presenting them for approval.
REVIEW_IMAGE_EXCLUSIONS={
    'keeper_idle','keeper_reference','obj_tv_on',
    'room_bedroom','room_kitchen','room_living',
    'keeper_front_torso','keeper_front_arm_l','keeper_front_arm_r',
    'keeper_front_leg_l','keeper_front_leg_r','keeper_front_head_happy',
    'keeper_front_head_neutral','keeper_front_head_grumpy',
    'keeper_front_head_asleep','keeper_front_head_open',
    'keeper_back_torso','keeper_back_arm_l','keeper_back_arm_r',
    'keeper_back_leg_l','keeper_back_leg_r','keeper_back_head',
}
rows=[];items=[]
FIELDS='space_id,name,category,placement_rule,stack_eligible,dimensions,dependencies,activities,unlock_challenge,asset_id,asset_type,tier,measurable_benefit,required_states,frames,keeper_pose,anchor,reusable_source,breakdown_effect,priority,implementation_status,notes'.split(',')
OVERRIDES={
'battery':['20 energy units stored','40 units stored','60 units stored'],
'powerrouter':['route power to 3 circuits','6 circuits','9 circuits'],
'gravitycontrol':['10 game min float time per charge','20 min per charge','30 min per charge'],
'windturbine':['10 units per moderate-wind game day','20 units per moderate-wind day','30 units per moderate-wind day'],
'poolheater':['heat pool for 30 min per charge','60 min per charge','90 min per charge'],
'hottub':['10 fun and 10 energy per 20 min warm soak','13 fun and 13 energy per 17 min','15 fun and 15 energy per 14 min'],
'safe':['4 stored crates; money balance unlimited and unaffected','8 crates; money unaffected','12 crates; money unaffected'],
'seadoors':['one boat bay open/close in 8 min','one bay in 6 min','one bay in 4 min'],
'fuelpump':['1 tank fill / 10 min','1 tank / 8 min','1 tank / 6 min'],
'berth':['one rowing-size berth; 1 repair station','one tug-size berth; 2 repair stations','one speedboat-size berth; 3 repair stations'],
'suntracker':['30 energy units on clear day; manual alignment','36 units; tracks every 2 game hours','42 units; tracks hourly'],
'stairs':['ladder travel 8 min per band both ways','spiral stair 5 min up and 6 min down','stair with handrail 4 min up and 5 min down'],
'slide':['down one band in 5 min','down one band in 3 min','down one band in 2 min; every floor still has exit'],
'projector':['30 fun / 40 min screening','38 fun / 34 min','45 fun / 28 min'],
'pinsetter':['reset 10 pins / 3 min','10 pins / 2 min','10 pins / 1 min'],
'sampletank':['1 habitat group','2 separately filtered habitat groups','3 habitat groups'],
'microscope':['resolve 1 sample detail','2 sample details','3 details including small plankton'],
'waterkit':['one salinity reading / 10 min'],
'coinscales':['weigh one coin batch / 10 min'],
'raingauge':['one rain reading / 10 min'],
'windvane':['one wind direction / 10 min'],
'pressuregauge':['one pressure reading / 10 min'],
'stardial':['one moon/sky bearing reading / 10 min'],
}
POSES={'telescope':(4,6),'idle':(4,6),'walk':(8,10),'reach_use':(5,10),'eat':(6,8),'cook_back':(8,8),'brush_teeth_back':(8,8),'wash_back':(8,8),'read':(4,5),'piano':(8,10),'watch_tv':(8,6),'watch_movie':(8,6),'sleep':(4,4),'wave_camera':(8,8),'yawn':(8,8),'pyjamas_walk':(8,10),'pyjamas_turn_back':(6,8),'get_into_bed':(8,8),'pyjamas_snore':(6,4),'swim_costume_horizontal':(8,8),'swim_costume_up':(8,8),'swim_costume_down':(8,8),'scuba_swim_horizontal':(8,8),'scuba_swim_up':(8,8),'scuba_swim_down':(8,8),'party_idle':(4,6),'party_walk':(8,10),'party_turn_back':(6,8),'souwester_walk_side':(8,10),'souwester_walk_back':(8,10),'souwester_walk_front':(8,10),'play_guitar':(8,10),'play_drums_front':(8,10),'play_drums_back':(8,10),'clear_snow':(8,8),'crouch_work_back':(8,8),'cake_from_oven_back':(8,8),'cake_turn_right':(6,8),'fish':(8,8),'dig':(8,8),'weld':(8,8),'saw_wood':(8,8),'tidy':(6,8),'phone':(4,6),'greet':(5,8),'dance':(8,10),'jump':(6,12),'spin':(6,12),'shake':(4,12),'shrug':(4,8),'robot_walk':(8,8),'chicken_care':(6,8),'headstand':(6,10),'flex':(5,8),'cry':(4,6),'laugh':(4,8),'hide':(5,8),'loo_hide':(0,0),'bodily_gag':(3,12),'swim_idle':(6,8),'swim_lengths':(8,8),'swim_splash':(6,8),'swim_float':(4,4),'swim_exit':(6,8),'pool_rescue':(8,8),'row':(8,8),'float_spacesuit':(8,8),'change_to_dive':(0,0)}
POSES.update({'sad':(8,8),'hungry':(8,8),'bored':(8,8),'cross':(8,8),'vomit_loo_back':(8,8),'bathrobe_walk':(8,10),'shower_door_open_bathrobe':(8,8),'shower_enter_bathrobe':(8,8),'spiral_stairs_up':(8,8),'spiral_stairs_down':(8,8),'hot_drink_pour':(10,8),'hot_drink_stir':(8,8),'hot_drink_pickup':(8,8),'hot_drink_drink':(8,8),'hot_drink_put_down':(8,8),'boat_enter':(8,8),'boat_exit':(8,8)})
VISUAL=['Basic: simple manual mechanism and few visible controls','Mid: sturdier housing; second visible functional control and clear status indicator','Top: automatic mechanism; readable capacity/output gauge; same anchor and frame bounds']
PROFILE_VISUALS={
    'storage':['Small four-slot shelves or single chest','Divided eight-slot cabinet with double doors','Twelve-slot cabinet with labelled bays; same footprint'],
    'cook':['Manual single burner/range','Two clearly marked burner controls','Three marked cooking slots and recipe display'],
    'clean':['Broom and bristles','Hoover body with hose','Robot cleaner with wheels and automatic status light'],
    'pet':['Plain bowl or simple hand-fed coop','Sturdier vessel with visible larger feed measure','Automatic feed dispenser and timed indicator'],
    'sleep':['Single bed and blue blanket','Double-style padded headboard within same frame','Four-poster silhouette with energy crest; same footprint'],
    'wash':['Simple pedestal tap or basic shower','Added mixer/shower control','Rainfall head and warm-water status light'],
    'loo':['Cistern and plain seat','Quiet-flush cistern with handle indicator','Heated-seat switch and comfort indicator'],
    'spot':['Short brass telescope','Longer optic on same tripod','Larger lens and spotting finder; stable tripod feet'],
    'music':['Basic upright or small instrument casing','Improved keyboard/bellows and sound indicator','Performance-ready casing and concert cue; keep frame bounds'],
    'social':['Manual handset or small serving counter','Cordless/expanded service with readiness light','Video or group-service screen and visitor cue'],
    'growing':['Ground patch and three crop slots','Raised beds with irrigation line','Glass greenhouse and protected crop gauge'],
    'boat':['Rowboat and oars','Small tug with engine stack','Compact speedboat with engine hood; shared waterline'],
    'forecast':['One brass dial','Instrument cluster','Forecast terminal with clear lead-time indicator'],
    'signal':['Small crackling speaker/aerial','Ship-to-shore console and tuned indicator','Coastguard-style multi-signal console'],
    'power':['Small manual panel/battery/motor with one status lamp','Larger working surface and second capacity band','Automatic controller and three output bands'],
    'heat':['Pilot flame and one pressure band','Larger exchanger and two pressure bands','Three service circuits and efficiency gauge'],
    'water':['Single manual pump and pipe','Two-way pump with visible valve','Three-way pump with filtering gauge'],
    'travel':['Simple manual carrier or landing','Improved motor/brake and clear floor indicator','Fast automatic carrier with route and safety indicator'],
    'door':['Wooden entrance','Knocker and peephole','Doorbell camera and visitor-wait indicator'],
    'fun':['Charcoal CRT and wooden stand','Flat-screen with same stable stand and larger viewing area','Cinema-style screen and two compact speakers within fixed bounds'],
    'research':['Manual book, board or simple computer','Indexed storage or improved terminal','Search interface or clue display; no live internet'],
    'repair':['Hand tools and pegboard','Powered repair jig','Diagnostic display and efficient tool station; do not promise global fault reduction'],
    'craft':['Manual wheel, printer or assembly bench','Two-batch fixture or feed tray','Three-batch automated fixture; same anchor'],
    'game':['Manual game surface and basic score display','Timing/score assistance with visible control','Helpful practice/aiming display; skill still required'],
    'weatherproof':['Plain exposed fixture','Light-rain cover','Stronger rain seal and status tab; no storm safety bypass'],
    'fish':['Weathered dock and rod support','Reinforced dock and bait stand','Harbour dock with launch fittings'],
    'bank':['Manual coin tube and receipt slot','Twin-batch deposit mechanism','Triple-batch counter and balance display; no savings loss'],
    'fitness':['Manual resistance equipment','Adjustable resistance indicator','Progress display with efficient activity controls'],
}
# All coordinates are logical, x within the space, y up from its walking plane.
def placements(s):
    obj=s['items'];width=s['dimensions'][0]
    if not obj:return []
    if s['space_id']=='bedroom':return [(18,0),(54,-20),(54,0),(84,0),(101,0)]
    if s['space_id']=='ensuite':return [(10,0),(27,0)]
    if s['space_id'] in ['pool_changing','gym_changing']:return [(13,0),(34,0),(53,0)]
    if s['space_id'] in ['pub_wc','service_wc']:return [(12,0),(31,0)]
    if s['space_id']=='boathouse':return [(55,0),(87,-25),(98,0),(16,0),(55,-25)]
    if s['space_id']=='kitchen':return [(10,0),(30,0),(53,0),(76,0),(95,0)]
    if s['space_id']=='living':return [(23,0),(53,0),(85,0)]
    if s['space_id']=='lamp':return [(16,0),(52,0)]
    # Overfull facilities are activity-specific station variants, not overlapping props.
    total=sum(i['dimensions'][0]+4 for i in obj)
    if total>width-8:
        s['station_variants']=True
        return [(width//2,0) for _ in obj]
    x=4;out=[]
    for i in obj:x+=i['dimensions'][0]//2;out.append((x,0));x+=math.ceil(i['dimensions'][0]/2)+4
    return out

def row(s,asset,typ,tier,benefit,states,frames,pose,anchor,reuse,broken,status,notes,size=None):
    r={k:s.get(k,'') for k in FIELDS};r.update(asset_id=asset,asset_type=typ,tier=tier,dimensions='x'.join(map(str,size or s['dimensions'])),measurable_benefit=benefit,required_states=states,frames=frames,keeper_pose=pose,anchor=anchor,reusable_source=reuse,breakdown_effect=broken,implementation_status=status,notes=notes)
    rows.append(r);return r

def runtime_benefit(id,tier):
    matches=[r for r in evidence['interactions'] if r['object']==id and r['effects']]
    preferred={'tv':'tv_watch','bed':'bed_nap','cooker':'cooker_toast','basin':'wash_basin','toilet':'loo_wee','broom':'desk_tidy'}
    r=next((r for r in matches if r['id']==preferred.get(id)),matches[0] if matches else None)
    if id=='bed':return f"Runtime: morning energy {evidence['bedEnergy'][tier-1]} percent"
    if not r:return None
    t=math.floor(r['minutes']*(1-evidence['quicker'][tier-1]/100)+.5)
    effects={k:math.floor(v*(1+evidence['boost'][tier-1]/100)+.5) if v>0 else v for k,v in r['effects'].items()}
    return 'Runtime: '+r['label']+f'; {t} game min; '+', '.join(f'{k} {v:+}' for k,v in effects.items())+' (need caps apply)'
for s in spaces:
    s['placements']=placements(s)
    s['bathroom_rule']='Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.' if s['category']=='standard' else 'Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.'
    s['breakdown_design']='Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.'
    if s['space_id']=='shop':s['breakdown_design']='Proprietor-owned; never keeper repair queue. Weather may prevent travel.'
    if s['space_id']=='garage':
        row(s,'retired_garage','retired',0,'none','none','0','none','none','boathouse','none','retired','Historical record; garage replaced by boathouse.');continue
    plate='room_'+s['space_id'] if s['category'] in ['standard','theme','lantern_cap'] or s['space_id']=='lair' else 'facility_'+s['space_id']
    size=[95,35] if s['category']=='lantern_cap' else [105,35] if s['category'] in ['standard','theme'] or s['space_id']=='lair' else s['dimensions']
    row(s,plate,'room_plate',0,'Separate structure; enables activities below','standard','1','none',f'top-left (0,0); floor y={size[1]}','room timber/stone/tile palette; no furniture','structure faults use separate interactive components','delivered-existing' if plate in manifest else 'planned',s['layout']+'; '+s['decision']+'; source: '+s['source'],size)
    row(s,'seam_'+s['category'],'structural_kit',0,'Connect without resizing furniture','standard','1','none','integer parent seam; walking-plane y=0','shared wall/beam/pipe segments','none; parent component controls faults','planned','Core remains 110x35; 105x35 plate; world-Y stripes. Extensions consume no standard slot.',[5,35])
    for j,i in enumerate(s['items']):
        id=i['id'];p=profiles[i['profile']];benefits=OVERRIDES.get(id,p['benefits']);tiers=len(benefits)
        if id in byid:tiers=3
        # Door ON is required by Frank's latest instruction, superseding earlier n/a guidance.
        onframes=1 if id in ['shop','diveinner','diveouter'] else 4
        broken='none: proprietor-owned' if id=='shop' else 'shared wobble(1px), smoke, intermittent sparks + '+p['visual_cues'].split('/')[-1].strip()
        records=[]
        for tier in range(1,tiers+1):
            aid='obj_'+id+('' if tier==1 else f'_t{tier}')
            proposed=benefits[min(tier-1,len(benefits)-1)]
            benefit=runtime_benefit(id,tier) if id in byid and id!='boat' else None
            if benefit:benefit+='; proposed specialist perk: '+proposed
            else:benefit='PROPOSED, not coded: '+proposed
            name=byid.get(id,{}).get(tier,{}).get('name',('Basic','Mid-tier','Top-tier')[min(tier-1,2)]+' '+id.replace('_',' '))
            w,h=i['dimensions'];x,y=s['placements'][j]
            states='standard;on' if id=='shop' else 'standard;on;broken'
            delivered=[state for state in states.split(';') if aid+'_'+state in manifest]
            status='delivered-review' if len(delivered)==len(states.split(';')) else 'planned'
            if id in ['door','shop','diveinner','diveouter']:cue='ON: open doorway/engaged entrance, explicitly delivered at every tier'
            elif id=='tv':cue='ON: literal B B SEA wordmark from supplied BBC NEWS reference, NEWS title and newsreader head; Sport football match; Nature animals. Every tier needs all three channel strips; glass always opaque'
            else:cue='ON: '+p['visual_cues'].split('/')[1].strip()
            notes=f'{name}. {PROFILE_VISUALS.get(i['profile'],VISUAL)[min(tier-1,2)]}. {cue}. Proposed location ({x},{y}), logical frame {w}x{h}; stable usePoint(-8,0), effectOrigin(0,{-h}), bubbleOrigin(0,{-h-8}), z40. New tier mechanics and names require review; existing names preserved.'
            if id=='tv': notes=notes.replace(f'usePoint(-8,0), effectOrigin(0,{-h}), bubbleOrigin(0,{-h-8})','usePoint(14,0), effectOrigin(8,-18), bubbleOrigin(0,-28)')
            if s.get('station_variants'):notes+=' This station replaces the central activity bay when selected; never draw all stations simultaneously.'
            if s['category']=='theme':notes+=' Theme prop remains single-tier; unlock variety instead of cosmetic upgrades.'
            r=row(s,aid,'interactive_item',tier,benefit,states,f'standard 1; on {onframes}@8fps; broken 1 + shared FX' if id!='shop' else 'standard 1; on 1',p['keeper_pose'],f'bottom-centre ({w//2},{h}); keeper floor anchor (16,40)',f'obj_{id}; shared {i["profile"]} chassis/pose',broken,status,notes,[w,h]);records.append(r)
        i.update(tiers=records,position=[x,y],owned=id!='shop',on_frames=onframes)
        items.append({'space_id':s['space_id'],**i})
    if s['space_id']=='living':
        for tier in range(1,4):
            for channel,label,content,benefit in [('news','BB Sea','Fictional keeper news presenter, moving ticker, blinking mouth','watch TV: fun +30/+38/+45; 40/34/28 min'),('sport','Sport','Football pitch, moving ball and kicking players','watch TV: fun +30/+38/+45; 40/34/28 min'),('nature','Nature','Penguin on rocks, flapping wing, moving gull and waves','nature: fun +22/+28/+33 and social +6/+8/+9; 40/34/28 min')]:
                aid='obj_tv'+('' if tier==1 else f'_t{tier}')+'_channel_'+channel+'_on'
                row(s,aid,'channel_strip',tier,'Runtime action reuse: '+benefit,'on','4@8fps','watch_tv','frame bottom-centre (14,23); usePoint(14,0)', 'same CRT casing as corresponding tier','broken state uses common TV broken strip','delivered-review' if aid in manifest else 'planned',label+': '+content+'. Same gameplay action as existing tv_watch/tv_nature; no new floor/mission rules. Channel art required at every TV tier.',[28,23])
    for prop in s['props']:
        if prop.endswith('_backdrop'):size=[105,35]
        elif prop in ['water_surface','indoor_water']:size=[48,8]
        elif prop in ['pipe_set','glass_segments','rock_layers']:size=[16,35]
        elif prop=='helicopter':size=[55,30]
        else:size=[12,12]
        row(s,'prop_'+prop,'dressing_or_activity_prop',1,'Supports '+s['activities']+'; single tier','standard;on' if prop in ['chicken_idle','chicken_peck','sea_creatures','fish_variants','water_surface','indoor_water','helicopter','comic_ghost'] else 'standard','on 4@8fps; standard 1' if prop in ['chicken_idle','chicken_peck','sea_creatures','fish_variants','water_surface','indoor_water','helicopter','comic_ghost'] else '1','reach_use','bottom-centre; water surface top-left',f'shared prop_{prop}','not independently interactive; no repair tier','planned','Separate prop; do not bake interactive furniture into plates. Exact final appearance proposal.',size)
    # Full dependencies include required character clips and effects, shared across rooms.
    poses={profiles[i['profile']]['keeper_pose'] for i in s['items']}
    poses|={'idle','walk','reach_use','greet','shrug'}
    if s['space_id'] in ['pool','lido','dive','hot_tub']:poses|={'swim_idle','swim_lengths','swim_splash','swim_float','swim_exit','pool_rescue','change_to_dive'}
    if s['space_id']=='zero_gravity':poses|={'float_spacesuit'}
    for pose in sorted(poses):
        n,fps=POSES[pose]
        aid='keeper_'+pose
        clip=manifest.get(aid,{})
        size=[clip.get('w',32),clip.get('h',40)]
        anchor=clip.get('anchor',[16,40])
        row(s,aid,'keeper_clip',0,'Reusable task pose','on',f'{n}@{fps}fps',pose,f'anchor ({anchor[0]},{anchor[1]}); canonical rig scale',f'shared keeper_{pose}','not repairable','delivered-review' if aid in manifest else ('hidden sequence' if n==0 else 'planned'),f'{size[0]}x{size[1]} aligned frames; hand-drawn angles and integer translation; no arbitrary raster rotation.',size)
    for fx,size,n,fps,anchor in [('broken_smoke',[12,16],8,8,[6,16]),('broken_sparks',[12,12],6,12,[6,6]),('floor_arrival_smoke',[64,64],8,12,[32,64]),('shine',[16,16],4,8,[8,16])]:
        if s['space_id']=='shop' and fx.startswith('broken'):continue
        aid='fx_'+fx
        row(s,aid,'shared_effect',0,'Reusable fault/reveal feedback','on',f'{n}@{fps}fps','none',str(anchor),aid,'overlay; does not move anchors','delivered-review' if aid in manifest else 'planned','FX shared; casing/body motion is separately integer-safe.',size)
# Shared production inventory: keeper layers, props, world layers, effects, NPCs.
shared={'space_id':'shared','name':'Shared world / keeper kit','category':'shared','placement_rule':'world layers / explicit anchors','stack_eligible':False,'dependencies':'renderer','activities':'all spaces','unlock_challenge':'none','priority':'P0','dimensions':[32,40]}
for view in ['front','back']:
    for part in ['torso','arm_l','arm_r','leg_l','leg_r']+(['head_happy','head_neutral','head_grumpy','head_asleep','head_open'] if view=='front' else ['head']):
        aid='keeper_'+view+'_'+part
        row(shared,aid,'keeper_part',0,'Aligned reusable puppet','standard','1','idle','canvas 32x40; floor (16,40); pivots per production kit','keeper master silhouette','none','delivered-review' if aid in manifest else 'planned','Front/back same canvas; layered z10/20/30/40/50/80; cap/beard included in head.',[32,40])
for asset,size,n,fps in [('fx_steam',[16,20],8,8),('fx_water_bubbles',[16,16],6,8),('fx_music_notes',[20,20],8,8),('fx_zzz',[20,20],8,4),('fx_splash',[48,32],8,12),('fx_rain',[8,16],4,10),('fx_snow',[8,16],4,8),('fx_lightning',[16,16],4,12),('fx_dust',[16,16],6,8),('fx_stink',[16,16],6,8),('fx_heart',[12,12],4,8),('fx_coin',[12,12],4,8),('fx_lamp_beam',[64,35],4,6),('bubble_speech',[36,20],4,6),('bubble_thought',[36,20],4,6),('bubble_alert',[20,20],4,8)]:
    row(shared,asset,'shared_effect',0,'Activity/reaction feedback','on',f'{n}@{fps}fps','none',f'bottom-centre ({size[0]//2},{size[1]})','shared world kit','none','planned','Separate layers; render at integer 4x; z95 effects, z110 bubbles.',size)
for asset,size in [('tower_base',[110,35]),('tower_lamproom',[110,35]),('tower_roof',[110,20]),('ground_strip',[300,30]),('tower_stripe_red',[110,8]),('tower_stripe_white',[110,8]),('bg_sky',[300,190]),('bg_clouds',[300,190]),('bg_distant_village',[300,50]),('bg_sea',[300,80]),('bg_island_back',[300,70]),('bg_lighthouse_shell',[110,35]),('bg_terrain',[300,70]),('bg_foreground',[300,30]),('facade_left',[55,35]),('facade_right',[55,35]),('island_heal_soil',[32,16]),('island_split_rock',[32,32])]:
    row(shared,asset,'world_layer',0,'Reusable modular world layer','standard;on' if asset.startswith('facade') or asset.startswith('island') else 'standard','4@8fps' if asset.startswith('facade') or asset.startswith('island') else '1','none','top-left; façade seam aligns band','world palette; stripes from world Y','none','delivered-existing' if asset in manifest else 'planned','No concept slicing; no cave cues in day-one ground; retain day/night tint layers.',size)
for prop in ['pan','toothbrush','book','phone','rod','cup','repair_tool','oilskins','warmcoat','rescuegear','diveoutfit','spacesuit','parachute']:
    row(shared,'prop_'+prop,'keeper_prop_or_outfit',1,'One functional held prop/outfit; no cosmetic tiers','standard;on','1; on 4@8fps if moving','reach_use','explicit wrist pivot; outfits on 32x40 master','shared keeper','not item machinery; no random fault','planned','Oilskins expand comfort, rescue gear expands safe emergency actions; cannot override hard lightning/sea restrictions.',[32,40] if prop.endswith('outfit') or prop in ['spacesuit','oilskins','warmcoat'] else [12,12])
for npc,size,n in [('cat_idle',[24,16],4),('cat_walk',[24,16],8),('visitor',[22,32],4),('seagull',[16,12],4),('ship',[48,24],4),('whale',[32,16],4),('pirate_ship',[48,24],4)]:
    row(shared,'npc_'+npc,'npc_or_spotting_target',0,'Activity/spotting/visitor content','standard;on',f'1; on {n}@8fps','none',f'bottom-centre ({size[0]//2},{size[1]})','shared NPC family','not keeper machinery','planned','Separate originals; do not reuse rejected style_a blocky art.',size)
for pose,(n,fps) in POSES.items():
    aid='keeper_'+pose
    if not any(r['asset_id']==aid for r in rows):
        clip=manifest.get(aid,{})
        size=[clip.get('w',32),clip.get('h',40)]
        anchor=clip.get('anchor',[16,40])
        row(shared,aid,'keeper_clip',0,'Reusable reaction or activity','on',f'{n}@{fps}fps',pose,f'anchor ({anchor[0]},{anchor[1]})','shared keeper','none','delivered-review' if aid in manifest else ('planned' if n else 'hidden sequence'),f'Aligned {size[0]}x{size[1]} frames; hand-drawn rotations only.',size)
with (OUT/'catalogue.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerows(rows)
with (OUT/'spaces.csv').open('w',newline='') as f:
    fields=['space_id','name','category','placement_rule','stack_eligible','dimensions','dependencies','activities','unlock_challenge','layout','bathroom_rule','breakdown_design','decision','source','priority']
    w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows({k:('x'.join(map(str,s[k])) if k=='dimensions' else s[k]) for k in fields} for s in spaces)
# Asset status is editable annotation data, not a change to runtime mechanics.
summary=Counter(r['implementation_status'] for r in rows)
payload={'base_commit':evidence['baseCommit'],'spaces':spaces,'rows':rows,'summary':dict(summary),'native_canvas_published':False,'revision':'2026-10-09 keeper interaction expansion; ON required for operating devices; passive furniture uses standard/occupied states'}
(OUT/'catalogue.json').write_text(json.dumps(payload,indent=2)+'\n')
# A self-contained HTML file is produced from a template, with embedded JSON and sprite images.
images={}
for key,e in manifest.items():
    if key in REVIEW_IMAGE_EXCLUSIONS:
        continue
    p=ROOT/'public/sprites'/e['file'];images[key]={'src':'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode(),'w':e['w'],'h':e['h'],'frames':e['frames'],'fps':e.get('fps',0)}
payload['images']=images
payload['references']={}
for label,p in [('Keeper turnaround — new review source',ROOT/'art/source/keeper-first-batch/keeper-turnaround-source.png'),('Keeper aligned contact sheet — new review batch',ROOT/'art/source/keeper-first-batch/keeper-contact-sheet.png'),('Inset lantern surround — new review source',SRC/'lantern-inset-source.png'),('Original CRT — preferred style and production master',SRC/'tv-original-standard-source.png'),('Original TV ON reference',SRC/'tv-original-on-source.png'),('Rejected full-width room — sharpness reference only',SRC/'room-lamp-source.png')]:
    if p.exists():payload['references'][label]='data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
TEMPLATE=(SRC/'review-template.html').read_text()
# Keep the source template compact, while injecting the review-only broadcast
# controls into the generated standalone canvas. These settings are annotations
# and never alter runtime sprites or game mechanics.
TEMPLATE=TEMPLATE.replace('</style>', '<style>.channel-stage{position:relative;display:inline-block;overflow:hidden;image-rendering:pixelated;background:#14243a}.shimmer-overlay{position:absolute;left:0;right:0;height:4px;background:rgba(255,244,190,.9);mix-blend-mode:screen;pointer-events:none;opacity:.65}</style>')
TEMPLATE=TEMPLATE.replace('Frank’s working review · 8 October 2026', 'Frank’s working review · 9 October 2026')
TEMPLATE=TEMPLATE.replace('Native Codex Canvas publication is unavailable in this session. Frank’s corrections: use the inset glazed lantern cap from the full lighthouse reference, with wraparound walkway; preserve the original CRT box proportions. Coarse exports, the full-width room and stretched TV are rejected. Logical footprints stay fixed; new PNGs retain 4 source pixels per logical pixel.', 'The new keeper batch follows the approved CRT detail, palette and hard-alpha rules while preserving the familiar navy cap, blue jumper and cream beard. Frank’s earlier corrections remain locked: inset glazed lantern cap with wraparound walkway; original CRT box proportions; fixed logical footprints and density-4 production sources.')
TEMPLATE=TEMPLATE.replace('The lamp room is the narrow glazed lantern chamber on a wraparound outside walkway, matching the top of the full lighthouse reference. The original CRT is the production master, with its aspect ratio preserved. Rejected studies remain clearly labelled for review history.', 'The keeper turnaround and aligned contact sheet are the newest review sources. The original CRT remains the object-style master; the inset glazed lantern chamber remains the top-floor reference. Rejected studies stay labelled for review history.')
TEMPLATE=TEMPLATE.replace("k.startsWith('obj_tv')||k.startsWith('fx_broken')||k==='room_lamp'", "k.startsWith('keeper_')||k.startsWith('obj_tv')||k.startsWith('fx_broken')||k==='room_lamp'")
TEMPLATE=TEMPLATE.replace(' · isolated branch: codex/floor-asset-catalogue.', '.')
TEMPLATE=TEMPLATE.replace('Every interactive item tier requires <b>standard + ON + broken</b>; proprietor-owned shop has no broken state.', 'Operating devices require <b>standard + ON + broken</b>; passive furniture uses standard/occupied states; proprietor-owned shop has no broken state.')
TEMPLATE=TEMPLATE.replace('one opaque ON/engaged state for every interactive item tier.', 'opaque ON/engaged states for operating devices; passive furniture uses actor-layer occupied poses.')
TEMPLATE=TEMPLATE.replace('<div id="channelpreview"></div>', '<div id="channelpreview"></div><div id="shimmer-controls" class="toolbar"><label>Shimmer strength <input id="shimmerstrength" type="range" min="0" max="100" value="80"><output id="shimmerstrengthvalue">80%</output></label><label>Shimmer speed <input id="shimmerspeed" type="range" min="25" max="200" value="100"><output id="shimmerspeedvalue">100%</output></label><span class="muted compact">Tune the animated broadcast highlight; settings save and export with your review.</span></div>')
TEMPLATE=TEMPLATE.replace("let reviewChannel='news';let tab='spaces',page=0;edits.pixelEdits??={};", "let reviewChannel='news';let tab='spaces',page=0;edits.pixelEdits??={};edits.animation??={shimmer:80,speed:100};")
TEMPLATE=TEMPLATE.replace("additions:[...edits.additions,...x.additions],pixelEdits:", "additions:[...edits.additions,...x.additions],animation:{...edits.animation,...(x.animation||{})},pixelEdits:")
TEMPLATE=TEMPLATE.replace("function renderChannelPreview(){const key='obj_tv_channel_'+reviewChannel+'_on',i=DATA.images[key];if(!i){$('channelpreview').textContent='Channel export pending';return}$('channelpreview').innerHTML=`<div class=\"stripframe\" data-animation=\"${key}\" data-scale=\"3\" style=\"width:${i.w*12}px;height:${i.h*12}px\"><img alt=\"Animated ${esc(reviewChannel)} broadcast\" src=\"${i.src}\" width=\"${i.w*i.frames*12}\" height=\"${i.h*12}\"></div>`;}", "function applyShimmerControls(){const a=edits.animation??={shimmer:65,speed:100};$('shimmerstrength').value=a.shimmer;$('shimmerstrengthvalue').textContent=a.shimmer+'%';$('shimmerspeed').value=a.speed;$('shimmerspeedvalue').textContent=a.speed+'%';document.querySelectorAll('[data-shimmer-overlay]').forEach(x=>x.style.opacity=(a.shimmer/100).toFixed(2))}function renderChannelPreview(){const key='obj_tv_channel_'+reviewChannel+'_on',i=DATA.images[key];if(!i){$('channelpreview').textContent='Channel export pending';return}$('channelpreview').innerHTML=`<div class=\"channel-stage\" data-channel-stage><div class=\"stripframe\" data-animation=\"${key}\" data-scale=\"3\" style=\"width:${i.w*12}px;height:${i.h*12}px\"><img alt=\"Animated ${esc(reviewChannel)} broadcast\" src=\"${i.src}\" width=\"${i.w*i.frames*12}\" height=\"${i.h*12}\"></div><div class=\"shimmer-overlay\" data-shimmer-overlay></div></div>`;applyShimmerControls();}")
TEMPLATE=TEMPLATE.replace("function animate(now){if(tab==='assets')document.querySelectorAll('[data-animation]').forEach(el=>{const i=DATA.images[el.dataset.animation];const f=i.fps?Math.floor(now/1000*i.fps)%i.frames:0;el.firstElementChild.style.left=(-f*i.w*4*(Number(el.dataset.scale)||1))+'px'});requestAnimationFrame(animate)}", "function animate(now){if(tab==='assets'){const a=edits.animation??={shimmer:65,speed:100};document.querySelectorAll('[data-animation]').forEach(el=>{const i=DATA.images[el.dataset.animation];const f=i.fps?Math.floor(now/1000*i.fps*(a.speed/100))%i.frames:0;el.firstElementChild.style.left=(-f*i.w*4*(Number(el.dataset.scale)||1))+'px'});document.querySelectorAll('[data-shimmer-overlay]').forEach(el=>{const stage=el.closest('[data-channel-stage]');el.style.opacity=(a.shimmer/100).toFixed(2);el.style.transform=`translateY(${(now/1000*(a.speed/100)*stage.clientHeight)%stage.clientHeight}px)`})}requestAnimationFrame(animate)}")
TEMPLATE=TEMPLATE.replace("['search','category','state'].forEach(id=>", "['shimmerstrength','shimmerspeed'].forEach(id=>$(id).addEventListener('input',()=>{edits.animation={shimmer:Number($('shimmerstrength').value),speed:Number($('shimmerspeed').value)};applyShimmerControls();save()}));applyShimmerControls();['search','category','state'].forEach(id=>")
TEMPLATE=TEMPLATE.replace('shimmer:65','shimmer:80').replace('value="65"','value="80"').replace('>65%</output>','>80%</output>')
(OUT/'review.html').write_text(TEMPLATE.replace('/*CATALOGUE_DATA*/',json.dumps(payload).replace('</','<\\/')))
# Durable plain-text per-space design, convenient for annotations in pull request review.
lines=['# Floor and facility design review','',f"Base: `{evidence['baseCommit']}`. 71 discussed spaces/variants, including retired garage. All non-runtime numbers are proposals. Frank selected sharp detailed artwork and the original CRT style; coarse exports, the full-width lamp room and stretched TV are rejected. The top lantern cap is inset (95x35 logical), with a wraparound walkway, rather than an ordinary 110-wide floor. Density-4 source images preserve footprints and TV proportions. ON is required for operating devices; passive furniture uses standard art plus actor-layer occupied/seated poses. No progression code changed.",'','Standard bands: 110 × 35. Plates: 105 × 35. Kitchen base, lamp top, bedroom beneath lamp, other standard floors saved random middle position. Nonstandard previews show their separate proposed footprints. No fixed-height dependency.', '', '## Decision register', '', '- Marine lab: separate floor or aquarium specialization.', '- Radio room: separate floor or weather-room expansion; migrate radio without removing activity.', '- Greenhouse: garden tier 3 and/or separate facility; avoid double rewards.', '- Lift: rear versus side core; current mission at five floors takes precedence over older seven-floor guidance.', '- Transport: exact slide clearance and funicular route; no final shafts yet.', '- Power: unit budget and zero-gravity costume; numbers are review proposals.', '- Bank: capped modest interest rate, interval and grown-up controls undecided; balances never break.', '- Bowling/gaming/hot-tub/roof bays: attachment and safe geometry still require review.', '- Solar tracker: optional fourth tier discussed; held as separate candidate module.', '- Native Codex Canvas tool unavailable; standalone review canvas is delivered, native publication remains outstanding.', '']
for s in spaces:
    lines+=['## '+s['name']+' (`'+s['space_id']+'`)','',f"**{s['category']} · {s['dimensions'][0]} × {s['dimensions'][1]} logical pixels · {s['placement_rule']}**",'', '**Layout:** '+s['layout']+(' Stations alternate in one central bay; not all displayed at once.' if s.get('station_variants') else ''),'','**Activities:** '+s['activities'],'','**Dependencies:** '+s['dependencies'],'','**Unlock challenge:** '+s['unlock_challenge'],'','**Breakdowns:** '+s['breakdown_design'],'','**Bathroom access:** '+s['bathroom_rule'],'','**Decision/status:** '+s['decision'],'','**Source:** '+s['source'],'','**Asset inventory:** plate + structural kit; '+', '.join(s['props'])+'; shared keeper poses and fault/reveal effects are itemized in CSV.','']
    for i in s['items']:
        lines+=['### '+i['id'], '']
        for r in i['tiers']:lines+=['- '+r['asset_id']+': '+r['measurable_benefit']+'. '+r['notes']+' States: '+r['required_states']+'; '+r['frames']+'.']
        lines+=['']
    lines+=['**Frank’s changes / additions:**','', '- [ ] Reviewed','- Notes:','']
(OUT/'DESIGNS.md').write_text('\n'.join(lines)+'\n')
print(f'{len(spaces)} spaces; {len(rows)} catalogue rows; {len({r["asset_id"] for r in rows})} unique asset/tier keys')

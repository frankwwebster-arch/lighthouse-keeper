#!/usr/bin/env python3
"""Build immutable Activity Cloud Composer V4 with deterministic music notation."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

import build_activity_cloud_composer_v1 as base


ROOT = Path(__file__).resolve().parents[1]
SET = "activity-cloud-composer-v4"
PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-19-v4"
SOURCE = PACK / "source/music-notation-source-sheet.png"
ACCENTS = PACK / "drafts/accents"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
PAGE = PUBLIC / "index.html"
CATALOGUE = PUBLIC / "catalogue.json"
V3_PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-19-v3"
V3_REGISTER = V3_PACK / "batch-register.json"
V3_CATALOGUE = ROOT / "public/keeper-review/activity-cloud-composer-v3/catalogue.json"
V3_PAGE = ROOT / "public/keeper-review/activity-cloud-composer-v3/index.html"

ACCENT_CELLS = (
    ("music-notation-quaver", (0, 0, 512, 512)),
    ("music-notation-beamed-quavers", (512, 0, 1024, 512)),
    ("music-notation-treble-clef", (1024, 0, 1536, 512)),
    ("music-notation-bass-clef", (0, 512, 512, 1024)),
    ("music-notation-sharp-note", (512, 512, 1024, 1024)),
    ("music-notation-rising-stave", (1024, 512, 1536, 1024)),
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    separators = (",", ":") if compact else None
    path.write_text(json.dumps(value, indent=None if compact else 2, separators=separators) + "\n")


def replace_once(page: str, old: str, new: str) -> str:
    if page.count(old) != 1:
        raise RuntimeError(f"V3 page contract changed; expected one occurrence: {old[:100]}")
    return page.replace(old, new)


def page_v4() -> str:
    page = V3_PAGE.read_text()
    page = page.replace("Activity Cloud Composer V3", "Activity Cloud Composer V4")
    page = replace_once(
        page,
        'href="/keeper-review/activity-cloud-composer-v2/index.html">\u2190 Immutable Composer V2',
        'href="/keeper-review/activity-cloud-composer-v3/index.html">\u2190 Immutable Composer V3',
    )
    page = replace_once(
        page,
        '<span class="tag">V2 exact + 12 album homages</span>',
        '<span class="tag">V3 exact + deterministic music notation</span>',
    )
    page = replace_once(
        page,
        "const SET='activity-cloud-composer-v3',STORAGE='lighthouse-keeper.activity-cloud-composer-v3'",
        "const SET='activity-cloud-composer-v4',STORAGE='lighthouse-keeper.activity-cloud-composer-v4'",
    )
    page = replace_once(
        page,
        '.piece{position:absolute;width:104px;height:104px;left:50%;top:50%;object-fit:contain;transform-origin:center}',
        '.piece{position:absolute;width:104px;height:104px;left:50%;top:50%;object-fit:contain;transform-origin:center}.piece.notation-piece{width:62px;height:62px;z-index:3}',
    )
    page = replace_once(
        page,
        '<label><input id="reducedMotion" type="checkbox"> Reduced motion</label>',
        '<label><input id="reducedMotion" type="checkbox"> Reduced motion</label><label><input id="showNotation" type="checkbox" checked> Musical notation</label>',
    )
    page = replace_once(
        page,
        "function slug(v){return v.toLowerCase().trim().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,64)}function valid(){return selection.length>=data.composer.minimumElements&&selection.length<=data.composer.maximumElements&&$('activityLabel').value.trim()&&$('recipeKey').value.trim()&&$('targetLabel').value.trim()&&$('targetId').value.trim()}",
        "function slug(v){return v.toLowerCase().trim().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,64)}function valid(){return selection.length>=data.composer.minimumElements&&selection.length<=data.composer.maximumElements&&$('activityLabel').value.trim()&&$('recipeKey').value.trim()&&$('targetLabel').value.trim()&&$('targetId').value.trim()}function musicSelection(){return selection.filter(key=>data.components[key].family==='music')}function notationEnabled(){return $('showNotation').checked&&musicSelection().length>0}function seed32(value){let h=2166136261;for(let i=0;i<value.length;i++){h^=value.charCodeAt(i);h=Math.imul(h,16777619)}return h>>>0}function notationSeed(){return seed32(`${$('recipeKey').value.trim()}|${musicSelection().join('|')}`)}function notationContract(){const enabled=notationEnabled();return{enabled,triggerFamily:'music',seedAlgorithm:data.notationAccents.seedAlgorithm,seed:enabled?notationSeed():null,sequenceLengthFrames:data.notationAccents.sequenceLengthFrames,visibleNotes:data.notationAccents.visibleNotes,components:Object.entries(data.notationAccents.components).map(([asset,item])=>({asset,sha256:item.sha256,sourceSet:item.sourceSet}))}}",
    )
    old_recipe = "function baseRecipe(){return{schema:'lighthouse-keeper/activity-cloud-recipe@1',sourceSet:SET,activity:{key:$('recipeKey').value.trim(),label:$('activityLabel').value.trim(),notes:$('notes').value.trim()},appliesTo:{assetId:$('targetId').value.trim(),label:$('targetLabel').value.trim()},bodyCompatibility:$('compatibility').value,elements:selection.map((key,index)=>({asset:key,role:index===0?'primary':'support',order:index,sha256:data.components[key].sha256,sourceSet:data.components[key].sourceSet})),timing:{frames:42,fps:8,quietTailFrames:5},treatments:['orbit','bustle'],sfx:$('sfx').value.trim()?[{cue:$('sfx').value.trim(),kind:'activity-beat'}]:[],ownership:{componentOwnerCount:1,contextBakedIntoKeeper:false}}}"
    new_recipe = "function baseRecipe(){return{schema:'lighthouse-keeper/activity-cloud-recipe@1',sourceSet:SET,activity:{key:$('recipeKey').value.trim(),label:$('activityLabel').value.trim(),notes:$('notes').value.trim()},appliesTo:{assetId:$('targetId').value.trim(),label:$('targetLabel').value.trim()},bodyCompatibility:$('compatibility').value,elements:selection.map((key,index)=>({asset:key,role:index===0?'primary':'support',order:index,sha256:data.components[key].sha256,sourceSet:data.components[key].sourceSet})),notationAccents:notationContract(),timing:{frames:42,fps:8,quietTailFrames:5},treatments:['orbit','bustle'],sfx:$('sfx').value.trim()?[{cue:$('sfx').value.trim(),kind:'activity-beat'}]:[],ownership:{componentOwnerCount:1,contextBakedIntoKeeper:false,notationBakedIntoComponents:false}}}"
    page = replace_once(page, old_recipe, new_recipe)
    old_draw = "function draw(host,treatment){host.innerHTML='';for(const p of parts(treatment)){const img=document.createElement('img');img.className='piece';img.src=data.components[p.asset].src;img.alt=p.asset;img.style.opacity=p.opacity;img.style.transform=`translate(calc(-50% + ${p.x}px),calc(-50% + ${p.y}px)) rotate(${p.rotate}deg) scale(${p.scale})`;host.appendChild(img)}}"
    new_draw = "function notationParts(treatment){if(!notationEnabled())return[];const f=$('reducedMotion').checked?18:frame;if(f<3||f>35)return[];const keys=Object.keys(data.notationAccents.components),seed=notationSeed(),cycle=Math.floor(f/data.notationAccents.sequenceLengthFrames),bases=[[-98,-43],[98,-38],[0,-62]];return bases.map(([bx,by],i)=>{const n=seed32(`${seed}|${cycle}|${i}`),asset=keys[n%keys.length],jitterX=((n>>>8)%15)-7,jitterY=((n>>>16)%11)-5,rotate=((n>>>23)%31)-15;let x=bx+jitterX,y=by+jitterY;if(treatment==='bustle'){x=Math.round(x*.76);y=Math.round(y*.7+2)}const phase=f%data.notationAccents.sequenceLengthFrames,opacity=phase===0?.45:phase===data.notationAccents.sequenceLengthFrames-1?.6:1;return{asset,x,y,rotate,scale:treatment==='orbit'?.48:.4,opacity}})}function appendPiece(host,p,notation=false){const img=document.createElement('img');img.className=notation?'piece notation-piece':'piece';const source=notation?data.notationAccents.components[p.asset]:data.components[p.asset];img.src=source.src;img.alt=p.asset;img.style.opacity=p.opacity;img.style.transform=`translate(calc(-50% + ${p.x}px),calc(-50% + ${p.y}px)) rotate(${p.rotate}deg) scale(${p.scale})`;host.appendChild(img)}function draw(host,treatment){host.innerHTML='';for(const p of parts(treatment))appendPiece(host,p);for(const p of notationParts(treatment))appendPiece(host,p,true)}"
    page = replace_once(page, old_draw, new_draw)
    page = replace_once(
        page,
        "$('frameReadout').textContent=`Callout ${frame+1}/42 at 8 fps · Prime body ${bodyFrame+1}/24 at 4 fps`",
        "$('frameReadout').textContent=`Callout ${frame+1}/42 at 8 fps · Prime body ${bodyFrame+1}/24 at 4 fps · notation ${notationEnabled()?'on':'off'}`",
    )
    page = replace_once(
        page,
        "$('sfx').value=r.sfx?.[0]?.cue||'';selection=(r.elements||[]).map(e=>e.asset).filter(k=>data.components[k]).slice(0,data.composer.maximumElements);updateAll()",
        "$('sfx').value=r.sfx?.[0]?.cue||'';selection=(r.elements||[]).map(e=>e.asset).filter(k=>data.components[k]).slice(0,data.composer.maximumElements);$('showNotation').checked=r.notationAccents?.enabled!==false;updateAll()",
    )
    page = replace_once(
        page,
        "[...Object.values(d.components).map(v=>v.src),...d.body.frames.map(v=>v.src)]",
        "[...Object.values(d.components).map(v=>v.src),...Object.values(d.notationAccents.components).map(v=>v.src),...d.body.frames.map(v=>v.src)]",
    )
    page = replace_once(
        page,
        "['targetLabel','targetId','compatibility','sfx','notes','showBody','reducedMotion']",
        "['targetLabel','targetId','compatibility','sfx','notes','showBody','reducedMotion','showNotation']",
    )
    page = replace_once(
        page,
        "$('notes').value='';frame=18;bodyFrame=0;updateAll()",
        "$('notes').value='';$('showNotation').checked=true;frame=18;bodyFrame=0;updateAll()",
    )
    page = replace_once(
        page,
        'Both treatments are generated from the same ordered component package.',
        'Both treatments are generated from the same ordered component package. Music selections receive a separately switchable, deterministic notation layer.',
    )
    return page


def main() -> None:
    for required in (SOURCE, V3_REGISTER, V3_CATALOGUE, V3_PAGE):
        if not required.exists():
            raise RuntimeError(f"missing dependency: {rel(required)}")

    source = Image.open(SOURCE).convert("RGBA")
    if source.size != (1536, 1024):
        raise RuntimeError(f"unexpected notation source geometry: {source.size}")
    boundary = {
        "verticalBoundaryX512AlphaPixels": base.boundary_count(source, "x", 512),
        "verticalBoundaryX1024AlphaPixels": base.boundary_count(source, "x", 1024),
        "horizontalBoundaryY512AlphaPixels": base.boundary_count(source, "y", 512),
    }
    if base.edge_alpha(source) or any(boundary.values()):
        raise RuntimeError(f"notation source ownership failed: edge={base.edge_alpha(source)}, {boundary}")

    v3 = json.loads(V3_CATALOGUE.read_text())
    v3_register = json.loads(V3_REGISTER.read_text())
    records: dict[str, dict] = {}
    published: list[dict] = []
    ACCENTS.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    for name, crop in ACCENT_CELLS:
        component, evidence = base.isolate(source, crop)
        if base.edge_alpha(component) or base.gutter(component) < 16:
            raise RuntimeError(f"unsafe notation component gutter: {name}")
        component_path = ACCENTS / f"{name}.png"
        component.save(component_path)
        digest = sha(component_path)
        public_asset = ASSETS / f"{name}-{digest[:16]}.png"
        shutil.copyfile(component_path, public_asset)
        record = {
            **evidence,
            "file": rel(component_path),
            "sha256": digest,
            "family": "music-notation",
            "cellPixels": [base.CELL, base.CELL],
            "sourceSet": SET,
            "src": f"/keeper-review/{SET}/assets/{public_asset.name}",
        }
        records[name] = record
        published.append({
            "source": rel(component_path),
            "sourceSha256": digest,
            "public": rel(public_asset),
            "publicAssemblyPath": rel(public_asset),
            "publicSha256": sha(public_asset),
            "url": record["src"],
        })

    composer = dict(v3["composer"])
    composer["localStorageKey"] = "lighthouse-keeper.activity-cloud-composer-v4"
    source_vocabulary = {
        "set": v3["set"],
        "catalogue": rel(V3_CATALOGUE),
        "catalogueSha256": sha(V3_CATALOGUE),
        "register": rel(V3_REGISTER),
        "registerSha256": sha(V3_REGISTER),
        "inheritedComponents": len(v3["components"]),
    }
    notation = {
        "triggerFamily": "music",
        "defaultEnabled": True,
        "seedAlgorithm": "fnv1a32-v1",
        "sequenceLengthFrames": 6,
        "visibleNotes": 3,
        "components": {
            name: {key: record[key] for key in ("sha256", "family", "cellPixels", "sourceSet", "src")}
            for name, record in records.items()
        },
    }
    catalogue = {
        **v3,
        "set": SET,
        "sourceVocabulary": source_vocabulary,
        "components": v3["components"],
        "composer": composer,
        "notationAccents": notation,
    }
    write_json(CATALOGUE, catalogue, compact=True)
    PAGE.write_text(page_v4())

    register = {
        "schema": "lighthouse-keeper/activity-cloud-composer-register@4",
        "set": SET,
        "status": catalogue["status"],
        "sourceVocabulary": source_vocabulary,
        "generatedSource": {
            "file": rel(SOURCE),
            "sha256": sha(SOURCE),
            "pixels": list(source.size),
            "edgeAlphaPixels": base.edge_alpha(source),
            "cellBoundaryAlphaPixels": boundary,
        },
        "newAccentComponents": records,
        "notationAccents": notation,
        "catalogue": {"file": rel(CATALOGUE), "sha256": sha(CATALOGUE), "components": len(v3["components"]), "newAccentComponents": len(records)},
        "page": {"file": rel(PAGE), "sha256": sha(PAGE)},
        "candidate": {"publicShell": {"file": rel(PAGE), "sha256": sha(PAGE)}},
        "publishedAssets": published,
        "checks": {
            "sourceEdgesClear": True,
            "sourceCellBoundariesClear": True,
            "componentGuttersClear": True,
            "componentOwnershipUnambiguous": True,
            "v3ComposerUnchanged": sha(V3_PAGE) == v3_register["page"]["sha256"],
            "primeBodyUnchanged": True,
            "runtimeChanged": False,
            "kitchenChanged": False,
            "deployed": False,
        },
        "approvalBoundary": {
            "notationVocabularyApproved": False,
            "composerApproved": False,
            "recipeApproved": False,
            "runtimePromoted": False,
        },
    }
    write_json(PACK / "batch-register.json", register)
    print(json.dumps({"set": SET, "components": len(v3["components"]), "newAccentComponents": len(records), "page": rel(PAGE)}, indent=2))


if __name__ == "__main__":
    main()

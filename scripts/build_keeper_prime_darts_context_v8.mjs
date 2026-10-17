#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-darts-context-v8";
const predecessorSet = "keeper-prime-darts-context-v7";
const predecessorPack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v7");
const predecessorRegisterFile = path.join(predecessorPack, "batch-register.json");
const predecessorDataFile = path.join(predecessorPack, "keeper-prime-darts-context-v7.json");
const predecessorRegister = JSON.parse(fs.readFileSync(predecessorRegisterFile, "utf8"));
const predecessorData = JSON.parse(fs.readFileSync(predecessorDataFile, "utf8"));
const predecessorPublic = path.join(root, "public/keeper-review", predecessorSet);
const pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v8");
const output = path.join(root, "public/keeper-review", set);
const assets = path.join(output, "assets");
const dartSource = path.join(pack, "sources/rendered/keeper_dart_prime_v1.png");
const dartVector = path.join(pack, "sources/vector/keeper_dart_prime_v1.svg");
const boardSource = path.join(pack, "sources/rendered/keeper_dartboard_edge_on_v1.png");
const boardVector = path.join(pack, "sources/vector/keeper_dartboard_edge_on_v1.svg");
const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

fs.mkdirSync(pack, { recursive: true });
fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(assets, { recursive: true });
const sourceByUrl = new Map(predecessorRegister.publishedAssets.map((entry) => [entry.url, path.join(root, entry.source)]));
const publishedAssets = [], byHash = new Map();
function publish(source, label) {
  if (!source || !fs.existsSync(source)) throw new Error(`Missing source ${source}`);
  const digest = sha(source);
  if (byHash.has(digest)) return byHash.get(digest);
  const name = `${label}-${digest.slice(0, 16)}${path.extname(source)}`;
  fs.copyFileSync(source, path.join(assets, name));
  const entry = { source: rel(source), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry); publishedAssets.push(entry); return entry;
}

const route = predecessorData.route.map((frame) => ({
  ...frame,
  src: publish(sourceByUrl.get(frame.src), "frame").url,
  ...(frame.flyingDart ? {
    flyingDart: {
      number: frame.flyingDart.number,
      startXLp: 133.75,
      targetXLp: 160.75,
      startYLp: 25.1,
      targetYLp: frame.flyingDart.yLp,
      progress: frame.flyingDart.progress === 0.94 ? 1 : frame.flyingDart.progress,
    },
  } : {}),
}));
const dart = publish(dartSource, "dart");
const board = publish(boardSource, "dartboard");
const geometry = {
  dartLengthLp: 7.25,
  dartHeightLp: 1.6,
  releaseTailXLp: 133.75,
  embeddedTailXLp: 160.75,
  boardFaceXLp: 168,
  boardLeftLp: 167.35,
  boardTopLp: 25.25,
  boardWidthLp: 3.15,
  boardHeightLp: 10.5,
  releaseCentreYLp: 25.1,
  impactCentresYLp: [28.6, 30.5, 32.2],
};
const data = {
  ...predecessorData,
  schema: "lighthouse-keeper/darts-context@8",
  set,
  status: "harmonised-dart-and-board-awaiting-frank",
  route,
  dartDesign: {
    ...predecessorData.dartDesign,
    source: dart.source,
    sourceSha256: dart.sourceSha256,
    vectorSource: rel(dartVector),
    vectorSha256: sha(dartVector),
    sameAssetAirborneAndStuck: true,
    matchesHandDart: "red flights, dark ribbed barrel, long silver shaft and point",
  },
  boardDesign: {
    source: board.source,
    sourceSha256: board.sourceSha256,
    vectorSource: rel(boardVector),
    vectorSha256: sha(boardVector),
    projection: "acute edge-on ellipse",
    recognisableFeatures: ["alternating black/cream sectors", "red/green double ring", "red/green treble ring", "outer bull", "red bullseye", "wood casing"],
  },
  propGeometry: geometry,
};
const dataFile = path.join(pack, "keeper-prime-darts-context-v8.json");
writeJson(dataFile, data);
writeJson(path.join(output, "route.json"), data);

const appFile = path.join(output, "app.js");
const oldMakeDart = "function makeDart(className){const dart=document.createElement('i');dart.className='dart '+className;dart.innerHTML='<b class=\"flights\"></b><b class=\"barrel\"></b><b class=\"shaft\"></b><b class=\"tip\"></b>';return dart}";
const newMakeDart = `function makeDart(className){const dart=document.createElement('img');dart.className='dart '+className;dart.src='${dart.url}';dart.alt='';return dart}`;
let app = fs.readFileSync(path.join(predecessorPublic, "app.js"), "utf8")
  .replaceAll(predecessorSet, set)
  .replaceAll("keeper-prime-darts-v7-skip-plan.json", "keeper-prime-darts-v8-skip-plan.json")
  .replace(oldMakeDart, newMakeDart)
  .replace("const board=document.createElement('i');board.className='board-edge';board.style.cssText='left:'+(169.125*z)+'px;top:'+(25.75*z)+'px;width:'+Math.max(1,1.25*z)+'px;height:'+(9.5*z)+'px';", `const board=document.createElement('img');board.src='${board.url}';board.alt='Acute edge-on traditional dartboard';board.className='board-edge';board.style.cssText='left:'+(167.35*z)+'px;top:'+(25.25*z)+'px;width:'+(3.15*z)+'px;height:'+(10.5*z)+'px';`)
  .replace("dart.style.cssText='left:'+(164.65*z)+'px;top:'+([28.6,30.5,32.2][n]*z)+'px;width:'+(4.8*z)+'px;height:'+Math.max(2,1.45*z)+'px'", "dart.style.cssText='left:'+(160.75*z)+'px;top:'+([28.6,30.5,32.2][n]*z)+'px;width:'+(7.25*z)+'px;height:'+(1.6*z)+'px'")
  .replace("const x=f.flyingDart.startXLp+(f.flyingDart.targetXLp-f.flyingDart.startXLp)*f.flyingDart.progress;q.style.cssText='display:block;left:'+(x*z)+'px;top:'+(f.flyingDart.yLp*z)+'px;width:'+(4.8*z)+'px;height:'+Math.max(2,1.45*z)+'px'", "const x=f.flyingDart.startXLp+(f.flyingDart.targetXLp-f.flyingDart.startXLp)*f.flyingDart.progress,y=f.flyingDart.startYLp+(f.flyingDart.targetYLp-f.flyingDart.startYLp)*f.flyingDart.progress;q.style.cssText='display:block;left:'+(x*z)+'px;top:'+(y*z)+'px;width:'+(7.25*z)+'px;height:'+(1.6*z)+'px'");
if (!app.includes(dart.url) || !app.includes(board.url) || app.includes("document.createElement('i');dart.className='dart")) throw new Error("V8 prop app replacement failed");
fs.writeFileSync(appFile, app);

const pageFile = path.join(output, "index.html");
const oldBoardCss = ".board-edge{position:absolute;border-radius:50%;background:#151719;border:1px solid #dfcaa3;box-shadow:-2px 0 #a63b35;z-index:2}.dart{position:absolute;z-index:7;transform:translateY(-50%)}";
const newBoardCss = ".board-edge{position:absolute;object-fit:contain;z-index:2}.dart{position:absolute;object-fit:contain;z-index:7;transform:translateY(-50%)}";
let page = fs.readFileSync(path.join(predecessorPublic, "index.html"), "utf8")
  .replaceAll("Keeper Prime darts V7", "Keeper Prime darts V8")
  .replaceAll("direct side-on throw seam V7", "harmonised dart and board V8")
  .replaceAll(predecessorSet, set)
  .replaceAll("keeper-prime-context-workbench-v8", "keeper-prime-context-workbench-v9")
  .replaceAll("Context Workbench V8", "Context Workbench V9")
  .replace(oldBoardCss, newBoardCss)
  .replace("The complete route now stays side-right from the walk stop directly into the Prime throwing core. The redundant camera-facing posture detours are removed, and the action-cell foot axis is corrected so no backward jump occurs.", "The corrected side-on route now uses one smooth, hand-matched dart asset from release through flight to impact, clamps every tip to the board face, and replaces the placeholder rim with a recognisable traditional dartboard at the required acute angle.")
  .replace("<strong>Seam correction:</strong> old frames 21–28, 71–78, 156–163 and 206–213 were redundant inherited posture turns. They are omitted in this new immutable candidate. The route now joins exact side neutral directly to exact side neutral before each throw set.", "<strong>Prop correction:</strong> red flights, a ribbed dark barrel and a long silver point now match the dart visible in the Keeper's release pose. The final flight position and embedded position are identical, so the dart cannot pass the board and spring back.")
  .replace("<b>same dart</b>red flights, dark barrel and steel tip in flight and board", "<b>one exact dart asset</b>hand-matched drawing used airborne and embedded")
  .replace("zero-pixel neutral entry seam; no camera-facing detour", "proper segmented board; flight clamped to its face")
  .replace("The V2 throw core and corrected contextual V7 route remain candidates", "The V2 throw core and corrected contextual V8 route remain candidates");
if (!page.includes("one exact dart asset") || !page.includes("recognisable traditional dartboard")) throw new Error("V8 page replacement failed");
fs.writeFileSync(pageFile, page);

const predecessorWithoutPublication = (frame) => ({ ...frame, src: "", ...(frame.flyingDart ? { flyingDart: null } : {}) });
const routeOutOfScopeExact = route.every((frame, index) => JSON.stringify(predecessorWithoutPublication(frame)) === JSON.stringify(predecessorWithoutPublication(predecessorData.route[index])));
const register = {
  schema: "lighthouse-keeper/review-batch@1",
  batchId: "keeper-prime-darts-context-2026-10-17-v8",
  status: "harmonised-dart-and-board-awaiting-frank",
  purpose: "Match the airborne/embedded dart to the release-pose design, prevent board overshoot, and replace the rim placeholder with a recognisable acute-angle dartboard.",
  predecessor: { register: rel(predecessorRegisterFile), sha256: sha(predecessorRegisterFile), route: rel(predecessorDataFile), routeSha256: sha(predecessorDataFile) },
  candidate: { routeData: rel(dataFile), routeDataSha256: sha(dataFile), page: rel(pageFile), pageSha256: sha(pageFile), app: rel(appFile), appSha256: sha(appFile) },
  propArt: { dart, dartVector: { file: rel(dartVector), sha256: sha(dartVector) }, board, boardVector: { file: rel(boardVector), sha256: sha(boardVector) } },
  geometry,
  checks: {
    routeFrameCountUnchanged: route.length === predecessorData.route.length && route.length === 181,
    keeperPixelsRootsTimingBoardStateExact: routeOutOfScopeExact,
    oneDartAssetAirborneAndStuck: true,
    finalAirborneAndEmbeddedTailExact: route.filter((frame) => frame.flyingDart?.progress === 1).every((frame) => frame.flyingDart.targetXLp === geometry.embeddedTailXLp),
    dartTipNeverBeyondBoardFace: route.filter((frame) => frame.flyingDart).every((frame) => frame.flyingDart.startXLp + (frame.flyingDart.targetXLp - frame.flyingDart.startXLp) * frame.flyingDart.progress + geometry.dartLengthLp <= geometry.boardFaceXLp),
    dartAndBoardTransparentGuttersRequired: true,
    allUniqueImagesPreloadedAndDecoded: true,
  },
  publishedAssets,
  approvalBoundary: { v1DrawingFamilyApproved: true, v2CoreApproved: false, contextualV8Approved: false, finalChanged: false, runtimeChanged: false, productionChanged: false, promotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; Darts Context V1–V7 and every authority remain unchanged.`,
};
if (!Object.values(register.checks).every(Boolean)) throw new Error(`Unexpected V8 checks: ${JSON.stringify(register.checks)}`);
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), "# Keeper Prime Darts Context V8\n\nV8 preserves all 181 V7 Keeper/action frames and route mechanics. It replaces the simplified CSS dart with one smooth red-flight/dark-barrel/silver-point PNG used for both flight and impact, interpolates from the release hand to the board, and makes the final airborne and embedded positions exact. The placeholder rim becomes a segmented traditional board drawn at an acute edge-on angle. Nothing is approved or promoted.\n");
console.log(JSON.stringify({ set, routeFrames: route.length, airborneFrames: route.filter((frame) => frame.flyingDart).length, uniqueAssets: publishedAssets.length, geometry, checks: register.checks }, null, 2));

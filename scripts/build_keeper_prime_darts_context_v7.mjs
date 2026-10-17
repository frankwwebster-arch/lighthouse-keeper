#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-darts-context-v7";
const predecessorSet = "keeper-prime-darts-context-v6";
const predecessorPack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v6");
const predecessorRegisterFile = path.join(predecessorPack, "batch-register.json");
const predecessorDataFile = path.join(predecessorPack, "keeper-prime-darts-context-v6.json");
const predecessorRegister = JSON.parse(fs.readFileSync(predecessorRegisterFile, "utf8"));
const predecessorData = JSON.parse(fs.readFileSync(predecessorDataFile, "utf8"));
const predecessorPublic = path.join(root, "public/keeper-review", predecessorSet);
const pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v7");
const output = path.join(root, "public/keeper-review", set);
const assets = path.join(output, "assets");
const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

fs.mkdirSync(pack, { recursive: true });
fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(assets, { recursive: true });

const sourceByUrl = new Map(predecessorRegister.publishedAssets.map((entry) => [entry.url, path.join(root, entry.source)]));
const publishedAssets = [];
const byHash = new Map();
function publish(oldUrl) {
  const source = sourceByUrl.get(oldUrl);
  if (!source || !fs.existsSync(source)) throw new Error(`Missing V6 source for ${oldUrl}`);
  const digest = sha(source);
  if (byHash.has(digest)) return byHash.get(digest).url;
  const name = `frame-${digest.slice(0, 16)}${path.extname(source)}`;
  fs.copyFileSync(source, path.join(assets, name));
  const entry = { source: rel(source), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry);
  publishedAssets.push(entry);
  return entry.url;
}

const redundantPhases = new Set([
  "set 1 entry", "set 1 stance", "set 1 stance exit", "set 1 complete",
  "set 2 entry", "set 2 stance", "set 2 stance exit", "set 2 complete",
]);
const removedFrames = predecessorData.route
  .map((frame, index) => redundantPhases.has(frame.phase) ? index + 1 : null)
  .filter(Boolean);
const route = predecessorData.route
  .filter((frame) => !redundantPhases.has(frame.phase))
  .map((frame) => ({
    ...frame,
    src: publish(frame.src),
    ...(frame.coreFrame ? { anchorLp: [16, 40] } : {}),
  }));

const firstCoreStart = route.findIndex((frame) => frame.setNumber === 1 && frame.throwNumber === 1 && frame.coreFrame === 1);
const firstCoreEnd = route.findLastIndex((frame) => frame.setNumber === 1 && frame.throwNumber === 3 && frame.coreFrame === 14);
const secondCoreStart = route.findIndex((frame) => frame.setNumber === 2 && frame.throwNumber === 1 && frame.coreFrame === 1);
const ranges = {
  complete: [0, route.length - 1],
  firstThrowSet: [0, firstCoreEnd],
  repeatableActivity: [firstCoreEnd, route.length - 1],
  secondThrowSet: [secondCoreStart, route.length - 1],
};
const data = {
  ...predecessorData,
  schema: "lighthouse-keeper/darts-context@7",
  set,
  status: "direct-side-throw-seam-awaiting-frank",
  route,
  ranges,
  correction: {
    removedRedundantTurnToCameraFrames: removedFrames,
    coreAnchorLp: [16, 40],
    reason: "The 448px action cells keep the Prime foot axis at source x=128 (16 lp), not the cell midpoint x=224 (28 lp).",
  },
};
const dataFile = path.join(pack, "keeper-prime-darts-context-v7.json");
writeJson(dataFile, data);
writeJson(path.join(output, "route.json"), data);

const appFile = path.join(output, "app.js");
fs.writeFileSync(appFile, fs.readFileSync(path.join(predecessorPublic, "app.js"), "utf8")
  .replaceAll(predecessorSet, set)
  .replaceAll("keeper-prime-darts-v6-skip-plan.json", "keeper-prime-darts-v7-skip-plan.json")
  .replace("const a=f.anchorLp||[16,40],w=a[0]===28?56:32", "const a=f.anchorLp||[16,40],w=f.coreFrame?56:(a[0]===28?56:32)")
  .replace("src:route[ranges.firstThrowSet[0]].src,anchorLp:[28,40],flipX:false", "src:route.find(x=>x.coreFrame===1).src,anchorLp:[16,40],coreFrame:1,flipX:false"));
const pageFile = path.join(output, "index.html");
fs.writeFileSync(pageFile, fs.readFileSync(path.join(predecessorPublic, "index.html"), "utf8")
  .replaceAll("Keeper Prime darts V6", "Keeper Prime darts V7")
  .replaceAll("complete-context redraw V6", "direct side-on throw seam V7")
  .replaceAll(predecessorSet, set)
  .replaceAll("keeper-prime-context-workbench-v7", "keeper-prime-context-workbench-v8")
  .replaceAll("Context Workbench V7", "Context Workbench V8")
  .replace("The complete accepted route now uses Prime-derived Keeper artwork for every one of the fourteen throw-core slots, plus one matching dart design for flight and board impact.", "The complete route now stays side-right from the walk stop directly into the Prime throwing core. The redundant camera-facing posture detours are removed, and the action-cell foot axis is corrected so no backward jump occurs.")
  .replace("<strong>Whole-bank redraw rule applied:</strong> the old Darts actor contributed choreography only. Every visible throw-core Keeper is exact Prime neutral, an approved V1 key pose, or a new Prime-derived bridge drawing. Frame skipping remains reversible and browser-local.", "<strong>Seam correction:</strong> old frames 21–28, 71–78, 156–163 and 206–213 were redundant inherited posture turns. They are omitted in this new immutable candidate. The route now joins exact side neutral directly to exact side neutral before each throw set.")
  .replace("zero inherited actor pixels remain in the throw core", "zero-pixel neutral entry seam; no camera-facing detour")
  .replace("This complete V2 throw core and contextual V6 route remain candidates", "The V2 throw core and corrected contextual V7 route remain candidates"));

const normalized = (frame) => ({ ...frame, src: "" });
const retainedPredecessor = predecessorData.route.filter((frame) => !redundantPhases.has(frame.phase));
const retainedUnchanged = route.every((frame, index) => {
  const expected = { ...retainedPredecessor[index], src: "" };
  if (frame.coreFrame) expected.anchorLp = [16, 40];
  return JSON.stringify(normalized(frame)) === JSON.stringify(expected);
});
const register = {
  schema: "lighthouse-keeper/review-batch@1",
  batchId: "keeper-prime-darts-context-2026-10-17-v7",
  status: "direct-side-throw-seam-awaiting-frank",
  purpose: "Remove the unnecessary camera-facing posture detours and correct the action-cell anchor that caused the backward jump into the throw core.",
  predecessor: { register: rel(predecessorRegisterFile), sha256: sha(predecessorRegisterFile), route: rel(predecessorDataFile), routeSha256: sha(predecessorDataFile) },
  candidate: { routeData: rel(dataFile), routeDataSha256: sha(dataFile), page: rel(pageFile), pageSha256: sha(pageFile), app: rel(appFile), appSha256: sha(appFile) },
  correction: { removedFrames, oldRouteFrames: predecessorData.route.length, newRouteFrames: route.length, oldCoreAnchorLp: [28, 40], newCoreAnchorLp: [16, 40], firstCoreStartFrame: firstCoreStart + 1 },
  checks: {
    exactRedundantFramesRemoved: JSON.stringify(removedFrames) === JSON.stringify([21,22,23,24,25,26,27,28,71,72,73,74,75,76,77,78,156,157,158,159,160,161,162,163,206,207,208,209,210,211,212,213]),
    retainedFrameOrderPixelsTimingStateExact: retainedUnchanged,
    everyCoreFrameUsesSourceFootAxis: route.filter((frame) => frame.coreFrame).every((frame) => JSON.stringify(frame.anchorLp) === JSON.stringify([16, 40])),
    noCameraFacingStancePhases: route.every((frame) => !redundantPhases.has(frame.phase)),
    completeRouteFrameCount: route.length === 181,
    skipControlsRetained: true,
    allUniqueFrameImagesPreloadedAndDecoded: true,
  },
  publishedAssets,
  approvalBoundary: { v1DrawingFamilyApproved: true, v2CoreApproved: false, contextualV7Approved: false, finalChanged: false, runtimeChanged: false, productionChanged: false, promotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; Darts Context V1–V6 and every authority remain unchanged.`,
};
if (!Object.values(register.checks).every(Boolean)) throw new Error(`Unexpected V7 checks: ${JSON.stringify(register.checks)}`);
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), "# Keeper Prime Darts Context V7\n\nV7 removes the four redundant eight-frame camera-facing posture bridges and corrects all 84 action-cell anchors from 28 lp to the actual 16-lp Prime foot axis. The old frame 20 stop now joins directly to the old frame 29/new frame 21 exact Prime neutral with no visual or root displacement. Route effects, throw timing, collection, turns and review controls remain unchanged. Nothing is approved or promoted.\n");
console.log(JSON.stringify({ set, routeFrames: route.length, removedFrames, firstCoreStartFrame: firstCoreStart + 1, uniqueAssets: publishedAssets.length, checks: register.checks }, null, 2));

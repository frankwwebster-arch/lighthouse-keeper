import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { PNG } from "pngjs";

const root = path.resolve(import.meta.dirname, "..");
const pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v7");
const register = JSON.parse(fs.readFileSync(path.join(pack, "batch-register.json"), "utf8"));
const data = JSON.parse(fs.readFileSync(path.join(root, register.candidate.routeData), "utf8"));
const predecessor = JSON.parse(fs.readFileSync(path.join(root, register.predecessor.route), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };

if (data.schema !== "lighthouse-keeper/darts-context@7" || data.route.length !== 181) fail("Wrong Darts Context V7 identity/count");
const expectedRemoved = [21,22,23,24,25,26,27,28,71,72,73,74,75,76,77,78,156,157,158,159,160,161,162,163,206,207,208,209,210,211,212,213];
if (JSON.stringify(register.correction.removedFrames) !== JSON.stringify(expectedRemoved)) fail("Wrong redundant frames removed");
if (data.route.some((frame: any) => /^(set [12] (entry|stance|stance exit|complete))$/.test(frame.phase))) fail("Camera-facing posture detour remains");
const core = data.route.filter((frame: any) => frame.coreFrame);
if (core.length !== 84 || core.some((frame: any) => frame.anchorLp[0] !== 16 || frame.anchorLp[1] !== 40)) fail("Action-cell foot axis is not 16 lp");

const sourceByUrl = new Map(register.publishedAssets.map((entry: any) => [entry.url, path.join(root, entry.source)]));
const stop = data.route[19];
const firstCore = data.route[20];
if (stop.rootXLp !== firstCore.rootXLp || stop.bottomLp !== firstCore.bottomLp || stop.anchorLp[0] !== firstCore.anchorLp[0]) fail("F20→F21 root/anchor seam moves");
const stopPng = PNG.sync.read(fs.readFileSync(sourceByUrl.get(stop.src)));
const corePng = PNG.sync.read(fs.readFileSync(sourceByUrl.get(firstCore.src)));
if (stopPng.width !== 256 || corePng.width !== 448 || stopPng.height !== corePng.height) fail("Unexpected neutral seam geometry");
for (let y = 0; y < stopPng.height; y++) for (let x = 0; x < corePng.width; x++) {
  const ci = (y * corePng.width + x) * 4;
  if (x < stopPng.width) {
    const si = (y * stopPng.width + x) * 4;
    for (let c = 0; c < 4; c++) if (stopPng.data[si + c] !== corePng.data[ci + c]) fail(`Neutral seam differs at ${x},${y}`);
  } else if (corePng.data[ci + 3] !== 0) fail(`Extended action-cell area is not transparent at ${x},${y}`);
}

const removed = new Set(expectedRemoved.map((frame) => frame - 1));
const retained = predecessor.route.filter((_: any, index: number) => !removed.has(index));
if (retained.length !== data.route.length) fail("Retained route length mismatch");
for (let i = 0; i < retained.length; i++) {
  const expected = { ...retained[i], src: "" };
  const actual = { ...data.route[i], src: "" };
  if (actual.coreFrame) expected.anchorLp = [16, 40];
  if (JSON.stringify(actual) !== JSON.stringify(expected)) fail(`Out-of-scope route change at candidate frame ${i + 1}`);
}
for (const field of ["routeData", "page", "app"]) if (sha(path.join(root, register.candidate[field])) !== register.candidate[`${field}Sha256`]) fail(`V7 ${field} hash drift`);
if (!Object.values(register.checks).every(Boolean)) fail("Recorded V7 checks failed");
if (register.approvalBoundary.contextualV7Approved || register.approvalBoundary.finalChanged || register.approvalBoundary.runtimeChanged || register.approvalBoundary.productionChanged || register.approvalBoundary.promotionAllowed) fail("Context V7 approval boundary breached");
console.log("Keeper Prime Darts Context V7 verified: four redundant camera-facing bridges removed, exact zero-pixel F20→F21 neutral seam, all 84 core anchors corrected to 16 lp, and 181 retained route frames remain deterministic; nothing promoted.");

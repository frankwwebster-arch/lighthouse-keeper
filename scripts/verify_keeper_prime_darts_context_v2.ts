#!/usr/bin/env node

import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { PNG } from "pngjs";

const root = path.resolve(import.meta.dirname, "..");
const pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v2");
const register = JSON.parse(fs.readFileSync(path.join(pack, "batch-register.json"), "utf8"));
const data = JSON.parse(fs.readFileSync(path.join(pack, "keeper-prime-darts-context-v2.json"), "utf8"));
const sidecarPath = path.join(root, register.candidate.sidecar);
const sidecar = JSON.parse(fs.readFileSync(sidecarPath, "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");

assert.equal(register.batchId, "keeper-prime-darts-context-2026-10-17-v2");
assert.equal(register.approvalBoundary.promotionAllowed, false);
assert.equal(register.approvalBoundary.productionChanged, false);
assert.equal(sidecar.frames, 30, "exact endpoint + 7-frame posture bridge + 14-frame throw + reverse bridge + endpoint");
assert.deepEqual(sidecar.repeatableCoreFrameRange, [9, 22]);
assert.deepEqual(sidecar.anchor, [28, 40]);
assert.equal(sidecar.startPose, "standing-side-right");
assert.equal(sidecar.endPose, "standing-side-right");

const strip = PNG.sync.read(fs.readFileSync(path.join(root, register.candidate.strip)));
assert.equal(strip.width, 448 * sidecar.frames);
assert.equal(strip.height, 320);
assert.equal(register.candidate.stripSha256, sha(path.join(root, register.candidate.strip)));
assert.equal(register.candidate.sidecarSha256, sha(sidecarPath));

assert.equal(register.candidate.frames.length, sidecar.frames);
assert.equal(register.candidate.frames[0].sha256, register.candidate.frames.at(-1).sha256, "entry and exit cells must be byte-identical");
assert(register.candidate.frames.every((entry: any) => entry.edgeAlphaPixels === 0), "every action cell must retain transparent edge alpha");
assert(register.checks.maximumAbsoluteGeneratedActorHeightDeltaPercent <= 1.1, "generated height drift exceeds the V2 measured gate");
assert.equal(register.checks.threeIdenticalCoreRepeats, true);
assert.equal(register.checks.fullStrideWalkToCollection, true);
assert.equal(register.checks.ghostOverlaysRequired, true);

const throwGroups = [1, 2, 3].map((number) => data.route.filter((entry: any) => entry.throwNumber === number));
assert(throwGroups.every((group: any[]) => group.length === 14), "each of the three darts must use all fourteen core poses");
assert.deepEqual(throwGroups[0].map((entry: any) => entry.src), throwGroups[1].map((entry: any) => entry.src));
assert.deepEqual(throwGroups[1].map((entry: any) => entry.src), throwGroups[2].map((entry: any) => entry.src));
assert.equal(Math.max(...data.route.map((entry: any) => entry.boardDarts)), 3);
assert.equal(data.route.at(-1).boardDarts, 0);
assert.equal(data.route.filter((entry: any) => entry.phase === "collect darts" && entry.label.includes("removed from board")).length, 3);
const collectionExit = data.route.findLastIndex((entry: any) => entry.phase === "collection exit");
assert.equal(data.actionRange[1], collectionExit, "action-only review must include walking to and collecting the darts");
const throwRoot = data.route.find((entry: any) => entry.phase === "action entry").rootXLp;
const collectionRoot = data.route.find((entry: any) => entry.phase === "collect darts").rootXLp;
assert.equal(collectionRoot - throwRoot, 30.5, "collection approach must use a complete approved stop-to-stop stride distance");

const page = fs.readFileSync(path.join(root, register.review.page), "utf8");
for (const required of ["Exact Prime ghost", "Previous-frame ghost", "Loop action + collection", "Promise.all(unique.map(preload))", "data-scale=\"8\"", "data-scale=\"4\"", "data-scale=\"1\""]) assert(page.includes(required), `review page missing ${required}`);
for (const entry of register.publishedAssets) assert.equal(entry.sourceSha256, sha(path.join(root, entry.source)), `published source hash drift: ${entry.source}`);

console.log(`Keeper Prime Darts Context V2 verified: ${data.route.length} route frames, three identical 14-frame throws, full-stride collection, exact endpoints and ghost controls.`);

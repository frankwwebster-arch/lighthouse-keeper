#!/usr/bin/env node

import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v3");
const register = JSON.parse(fs.readFileSync(path.join(pack, "batch-register.json"), "utf8"));
const data = JSON.parse(fs.readFileSync(path.join(pack, "keeper-prime-darts-context-v3.json"), "utf8"));
const v2 = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v2/batch-register.json"), "utf8"));
const page = fs.readFileSync(path.join(root, register.candidate.page), "utf8");
const app = fs.readFileSync(path.join(root, "public/keeper-review/keeper-prime-darts-context-v3/app.js"), "utf8");
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");

assert.equal(register.batchId, "keeper-prime-darts-context-2026-10-17-v3");
assert.equal(data.schema, "lighthouse-keeper/darts-context@3");
assert.equal(register.approvalBoundary.promotionAllowed, false);
assert.equal(register.approvalBoundary.productionChanged, false);
assert.equal(data.stage.cupboardDoor.state, "closed");
assert.equal(data.stage.cupboardDoor.presentation, "edge-on");
assert.equal(data.stage.dartboard.presentation, "edge-on outer rim only");
assert.equal(data.stage.dartboard.centreYLp, 30.5);
assert.equal(data.stage.collectionRootXLp - data.stage.ocheRootXLp, 30.5);

assert.equal(v2.candidate.frames.length, 30);
assert.equal(register.checks.v2ActionPixelsReusedByteForByte, true);
for (const frame of v2.candidate.frames) assert.equal(frame.sha256, sha(path.join(root, frame.file)), `V2 action pixel drift: ${frame.file}`);

const sets = [1, 2].map((setNumber) => data.route.filter((entry: any) => entry.setNumber === setNumber && entry.throwNumber));
assert.deepEqual(sets.map((set: any[]) => set.length), [42, 42], "each set must contain three complete fourteen-frame throws");
for (const set of sets) {
  const throws = [1, 2, 3].map((number) => set.filter((entry: any) => entry.throwNumber === number));
  assert(throws.every((group: any[]) => group.length === 14));
  assert.deepEqual(throws[0].map((entry: any) => entry.src), throws[1].map((entry: any) => entry.src));
  assert.deepEqual(throws[1].map((entry: any) => entry.src), throws[2].map((entry: any) => entry.src));
  assert.deepEqual(throws.map((group: any[]) => group.filter((entry: any) => entry.flyingDart).length), [5, 5, 5]);
}
assert.equal(data.route.filter((entry: any) => entry.flyingDart).length, 30, "six darts need five visible flight positions apiece");
for (const frame of data.route.filter((entry: any) => entry.flyingDart)) {
  assert.equal(frame.flyingDart.targetXLp, data.stage.dartboard.planeXLp);
  assert(frame.flyingDart.progress > 0 && frame.flyingDart.progress < 1);
}

assert.equal(data.route.filter((entry: any) => entry.phase === "collect darts" && entry.label.includes("removed")).length, 3);
assert.equal(data.route.filter((entry: any) => entry.phase === "turn at board").length, 16);
assert.equal(data.route.filter((entry: any) => entry.phase === "turn at oche").length, 16);
assert.equal(data.route.filter((entry: any) => entry.phase.includes("turn") && !["turn at board", "turn at oche"].includes(entry.phase)).length, 0, "no unnecessary turn phases permitted");

const [loopStart, loopEnd] = data.ranges.repeatableActivity;
const start = data.route[loopStart], end = data.route[loopEnd];
assert.equal(start.src, end.src, "activity loop must close on byte-identical Prime pixels");
assert.equal(start.rootXLp, end.rootXLp);
assert.equal(start.bottomLp, end.bottomLp);
assert.equal(start.flipX, end.flipX);
assert.equal(start.boardDarts, 3);
assert.equal(end.boardDarts, 3);
assert.equal(start.rootXLp, data.stage.ocheRootXLp);
assert.equal(data.route.find((entry: any) => entry.phase === "collect darts").rootXLp, data.stage.collectionRootXLp);
assert.equal(data.route.at(-1).phase, "set 2 complete");

for (const required of ["closed and seen edge-on", "6 flights", "2 necessary turns", "30.5 lp", "Exact Prime ghost", "Previous-frame ghost", "data-scale=\"8\"", "data-scale=\"4\"", "data-scale=\"1\""]) assert(page.includes(required), `review page missing ${required}`);
for (const required of ["/keeper-review/keeper-prime-darts-context-v3/route.json", "Promise.all", "f.flyingDart", "ranges.repeatableActivity"]) assert(app.includes(required), `review app missing ${required}`);
assert(!app.includes("fetch('./"), "deployed review fetches must not depend on a trailing slash");
for (const asset of register.publishedAssets) assert.equal(asset.sourceSha256, sha(path.join(root, asset.source)), `published source hash drift: ${asset.source}`);

console.log(`Keeper Prime Darts Context V3 verified: ${data.route.length} frames, six visible dart flights, two necessary turns, exact 30.5 lp return and a closed-door edge-on board.`);

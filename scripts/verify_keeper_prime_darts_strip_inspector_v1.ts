#!/usr/bin/env node

import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-darts-strip-inspector-v1";
const pack = path.join(root, "art/drafts/keeper-prime-darts-strip-inspector-2026-10-17-v1");
const output = path.join(root, "public/keeper-review", set);
const register = JSON.parse(fs.readFileSync(path.join(pack, "batch-register.json"), "utf8"));
const manifest = JSON.parse(fs.readFileSync(path.join(output, "manifest.json"), "utf8"));
const page = fs.readFileSync(path.join(output, "index.html"), "utf8");
const app = fs.readFileSync(path.join(output, "app.js"), "utf8");
const v2 = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v2/batch-register.json"), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");

assert.equal(register.batchId, "keeper-prime-darts-strip-inspector-2026-10-17-v1");
assert.equal(register.status, "inspection-only-no-art-change");
assert.equal(register.approvalBoundary.promotionAllowed, false);
assert.equal(register.checks.artPixelsChanged, false);
assert.equal(manifest.schema, "lighthouse-keeper/darts-strip-inspector@1");
assert.equal(manifest.frames.length, 30);
assert.deepEqual(manifest.sourceStrip.logicalFrameSize, [56, 40]);
assert.equal(manifest.sourceStrip.density, 8);
assert.equal(manifest.sourceStrip.frameCount, 30);
assert.equal(manifest.frames[0].sourceSha256, manifest.frames.at(-1).sourceSha256);
assert.equal(manifest.frames[0].exactEndpoint, true);
assert.equal(manifest.frames.at(-1).exactEndpoint, true);
assert(manifest.frames.slice(8, 22).every((frame: any) => frame.role === "new registered darts core"));

for (const [index, frame] of manifest.frames.entries()) {
  assert.equal(frame.sourceSha256, v2.candidate.frames[index].sha256, `V2 frame hash mismatch at F${index + 1}`);
  assert.equal(frame.sourceSha256, sha(path.join(root, frame.source)), `source bytes drifted at F${index + 1}`);
  for (const key of ["blue", "navy", "cream"]) {
    assert.equal(frame.palette[key].medianRgb.length, 3);
    assert(frame.palette[key].classifiedPixels > 1000, `${key} class too small at F${index + 1}`);
    assert(Number.isFinite(frame.paletteDistanceFromPrime[key]));
  }
}
assert(manifest.frames.slice(8, 22).some((frame: any) => frame.paletteDistanceFromPrime.blue > 20), "inspector should expose the suspected throw-core blue drift");
assert.equal(manifest.frames[0].paletteDistanceFromPrime.blue, 0);
assert.equal(manifest.frames.at(-1).paletteDistanceFromPrime.blue, 0);

for (const required of ["Exact source pixels · 448×320", "2× source · 896×640", "Prime overlay", "Previous-frame overlay", "Difference blend", "Deterministic colour classes", "All 30 frames", "Whole registered V2 strip"]) assert(page.includes(required), `inspector page missing ${required}`);
for (const required of ["/keeper-review/keeper-prime-darts-strip-inspector-v1/manifest.json", "Promise.all", "ArrowLeft", "paletteDistanceFromPrime"]) assert(app.includes(required), `inspector app missing ${required}`);
assert(!app.includes("fetch('./"), "inspector manifest fetch must be root-absolute");
assert.equal(register.publishedAssets.length, 23, "reversible duplicated cells should be content-deduplicated");
for (const asset of register.publishedAssets) assert.equal(asset.sourceSha256, sha(path.join(root, asset.source)), `published source hash drift: ${asset.source}`);

console.log(`Darts V2 strip inspector verified: 30 cells, 23 unique immutable images, exact-source zoom, overlays and deterministic three-class palette comparison.`);

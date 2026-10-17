#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const publicDir = path.join(root, "public/keeper-review/keeper-prime-context-workbench-v1");
const catalog = JSON.parse(fs.readFileSync(path.join(publicDir, "catalog.json"), "utf8"));
const page = fs.readFileSync(path.join(publicDir, "index.html"), "utf8");
const register = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v1/batch-register.json"), "utf8"));

assert.equal(catalog.schema, "lighthouse-keeper/context-workbench@1");
assert.equal(catalog.status, "review-only");
assert.equal(catalog.boundaries.productionChanged, false);
assert.equal(catalog.boundaries.approvalsChanged, false);
assert.equal(catalog.sequences.length, 7);
assert.equal(catalog.sequences.filter((entry: any) => entry.kind === "native").length, 3);
assert.equal(catalog.sequences.filter((entry: any) => entry.kind === "external").length, 4);
assert.equal(catalog.inventorySummary.totalRows, 308);
assert.equal(catalog.inventoryUrl, "./inventory.json");
const inventory = JSON.parse(fs.readFileSync(path.join(publicDir, "inventory.json"), "utf8"));
assert.equal(inventory.rows.length, 308);
for (const sequence of catalog.sequences) {
  assert(sequence.status && sequence.summary, `${sequence.id} lacks explicit review status`);
  if (sequence.kind === "native") {
    assert(sequence.frames.length > 0, `${sequence.id} has no frames`);
    assert(sequence.coreRange[0] >= 0 && sequence.coreRange[1] < sequence.frames.length && sequence.coreRange[0] <= sequence.coreRange[1], `${sequence.id} has invalid core range`);
    assert(sequence.frames.every((frame: any) => frame.src && frame.phase && frame.durationMs > 0 && Number.isFinite(frame.rootXLp)), `${sequence.id} has an incomplete route frame`);
  } else {
    assert(sequence.url.startsWith("/keeper-review/"), `${sequence.id} external route is not a review URL`);
  }
}
const darts = catalog.sequences.find((entry: any) => entry.id === "darts-v2");
assert.equal(darts.status, "new candidate awaiting Frank");
assert.equal(Math.max(...darts.frames.map((frame: any) => frame.boardDarts ?? 0)), 3);
for (const required of ["preceding transition", "finishing transition", "Prime ghost", "previous-frame ghost", "data-scale=\"8\"", "data-scale=\"4\"", "data-scale=\"1\"", "Promise.all(unique.map(preload))", "iframe", "all 308 production animations", "./inventory.json"]) assert(page.includes(required), `workbench missing ${required}`);
assert(register.features.includes("animation selector"));
assert(register.features.includes("whole/core looping"));
assert(register.features.includes("complete 308-row inventory"));
assert.equal(register.boundaries.productionChanged, false);

console.log(`Prime Context Workbench V1 verified: ${catalog.sequences.length} selections, optional pre/post transitions, frame stepping, speed, looping and ghost overlays.`);

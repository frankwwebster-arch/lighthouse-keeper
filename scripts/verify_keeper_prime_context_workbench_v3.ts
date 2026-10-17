#!/usr/bin/env node

import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-context-workbench-v3";
const output = path.join(root, "public/keeper-review", set);
const pack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v3");
const catalog = JSON.parse(fs.readFileSync(path.join(output, "catalog.json"), "utf8"));
const inventory = JSON.parse(fs.readFileSync(path.join(output, "inventory.json"), "utf8"));
const page = fs.readFileSync(path.join(output, "index.html"), "utf8");
const app = fs.readFileSync(path.join(output, "app.js"), "utf8");
const register = JSON.parse(fs.readFileSync(path.join(pack, "batch-register.json"), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");

assert.equal(catalog.schema, "lighthouse-keeper/context-workbench@3");
assert.equal(catalog.set, set);
assert.equal(catalog.sequences.length, 8);
assert.equal(catalog.sequences.filter((entry: any) => entry.kind === "native").length, 2);
assert.equal(catalog.sequences.filter((entry: any) => entry.kind === "external").length, 6);
assert.equal(catalog.inventoryUrl, `/keeper-review/${set}/inventory.json`);
assert.equal(inventory.rows.length, 308);
assert.equal(catalog.boundaries.productionChanged, false);
assert.equal(catalog.boundaries.approvalsChanged, false);

const inspector = catalog.sequences.find((entry: any) => entry.id === "darts-v2-strip-inspector");
assert(inspector);
assert.equal(inspector.kind, "external");
assert.equal(inspector.url, "/keeper-review/keeper-prime-darts-strip-inspector-v1/");
assert.equal(inspector.status, "inspection only; no art changed");
assert(catalog.sequences.some((entry: any) => entry.id === "darts-v3"), "corrected Darts V3 route must remain available");

for (const sequence of catalog.sequences.filter((entry: any) => entry.kind === "native")) {
  assert(sequence.frames.length > 0);
  assert(sequence.frames.every((frame: any) => frame.src.startsWith(`/keeper-review/${set}/assets/`)));
}
for (const required of ["Prime Keeper contextual animation workbench V3", "detailed frame-by-frame inspection", "Eight current authorities, candidates or inspection views", "Preceding transition", "Finishing transition", "Exact Prime ghost", "Previous-frame ghost"]) assert(page.includes(required), `V3 workbench page missing ${required}`);
for (const required of [`/keeper-review/${set}/catalog.json`, "Promise.all", "dedicated contextual reviewer"]) assert(app.includes(required), `V3 workbench app missing ${required}`);
assert(!app.includes("fetch('./"));
assert(register.features.includes("Darts V2 30-frame registered-strip inspector"));
assert(register.features.includes("per-frame deterministic palette measurements"));
assert.equal(register.publishedAssets.length, 22);
for (const asset of register.publishedAssets) assert.equal(asset.sourceSha256, sha(path.join(root, asset.source)), `published source drift: ${asset.source}`);

console.log(`Prime Context Workbench V3 verified: ${catalog.sequences.length} choices including the detailed 30-frame Darts V2 strip inspector.`);

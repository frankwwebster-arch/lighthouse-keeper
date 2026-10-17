#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const publicDir = path.join(root, "public/keeper-review/keeper-prime-context-workbench-v2");
const catalog = JSON.parse(fs.readFileSync(path.join(publicDir, "catalog.json"), "utf8"));
const inventory = JSON.parse(fs.readFileSync(path.join(publicDir, "inventory.json"), "utf8"));
const page = fs.readFileSync(path.join(publicDir, "index.html"), "utf8");
const app = fs.readFileSync(path.join(publicDir, "app.js"), "utf8");
const register = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v2/batch-register.json"), "utf8"));

assert.equal(catalog.schema, "lighthouse-keeper/context-workbench@2");
assert.equal(catalog.status, "review-only");
assert.equal(catalog.boundaries.productionChanged, false);
assert.equal(catalog.boundaries.approvalsChanged, false);
assert.equal(catalog.sequences.length, 7);
assert.equal(catalog.sequences.filter((entry: any) => entry.kind === "native").length, 2);
assert.equal(catalog.sequences.filter((entry: any) => entry.kind === "external").length, 5);
assert.equal(catalog.inventorySummary.totalRows, 308);
assert.equal(inventory.rows.length, 308);
assert.equal(catalog.inventoryUrl, "/keeper-review/keeper-prime-context-workbench-v2/inventory.json");

for (const sequence of catalog.sequences) {
  assert(sequence.status && sequence.summary, `${sequence.id} lacks explicit status or summary`);
  if (sequence.kind === "native") {
    assert(sequence.frames.length > 0, `${sequence.id} has no frames`);
    assert(sequence.coreRange[0] >= 0 && sequence.coreRange[1] < sequence.frames.length);
    assert(sequence.frames.every((frame: any) => frame.src && frame.phase && frame.durationMs > 0 && Number.isFinite(frame.rootXLp)));
  } else assert(sequence.url.startsWith("/keeper-review/"), `${sequence.id} is not root-absolute`);
}
const darts = catalog.sequences.find((entry: any) => entry.id === "darts-v3");
assert(darts);
assert.equal(darts.url, "/keeper-review/keeper-prime-darts-context-v3/");
assert.equal(darts.status, "corrected candidate awaiting Frank");
assert(!catalog.sequences.some((entry: any) => entry.id === "darts-v2"));

for (const required of ["all 308 production animations", "Preceding transition", "Finishing transition", "Exact Prime ghost", "Previous-frame ghost", "data-scale=\"8\"", "data-scale=\"4\"", "data-scale=\"1\"", "full browser width", "/keeper-review/keeper-prime-context-workbench-v2/app.js"]) assert(page.includes(required), `workbench page missing ${required}`);
for (const required of ["/keeper-review/keeper-prime-context-workbench-v2/catalog.json", "Promise.all", "dedicated contextual reviewer"]) assert(app.includes(required), `workbench app missing ${required}`);
assert(page.includes("iframe"), "workbench page must embed dedicated contextual reviewers");
assert(!app.includes("fetch('./"), "catalogue loading must not rely on a trailing slash");
assert(!page.includes("./inventory.json"), "inventory link must not rely on a trailing slash");
assert(register.features.includes("root-absolute deployment-safe data loading"));
assert(register.features.includes("complete 308-row inventory"));
assert.equal(register.boundaries.productionChanged, false);

console.log(`Prime Context Workbench V2 verified: deployment-safe absolute loading, ${catalog.sequences.length} review choices and the complete ${inventory.rows.length}-row inventory.`);

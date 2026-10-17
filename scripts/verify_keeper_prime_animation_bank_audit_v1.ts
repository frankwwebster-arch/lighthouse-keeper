#!/usr/bin/env node

import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const audit = JSON.parse(fs.readFileSync(path.join(root, "data/keeper-prime-animation-bank-audit-v1.json"), "utf8"));
const hash = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");

assert.equal(audit.schemaVersion, 1);
assert.equal(audit.summary.totalRows, 308);
assert.equal(audit.rows.length, 308);
assert.equal(new Set(audit.rows.map((row: any) => row.id)).size, 308);
assert.equal(audit.summary.geometryMismatchCount, 0);
assert.equal(audit.summary.explicitlyRejectedOrExcludedCount, 28);
assert.equal(audit.summary.byTreatment["excluded-deleted-amendment"], 1);
assert(audit.explicitlyRejectedOrExcluded.includes("keeper_count_money"));

for (const row of audit.rows) {
  assert.deepEqual(row.frameRange, [1, row.frames], `${row.id}: incomplete frame range`);
  assert.equal(row.geometryMatchesSidecar, true, `${row.id}: strip/sidecar mismatch`);
  assert(row.currentFaceAndBodyFamily && row.historicalMotionTreatment, `${row.id}: authority/treatment missing`);
  assert(typeof row.requiredContextRoute === "string" && row.requiredContextRoute.length > 20, `${row.id}: contextual route missing`);
  const runtime = path.join(root, row.runtimeFile);
  assert(fs.existsSync(runtime), `${row.id}: missing runtime evidence`);
  assert.equal(hash(runtime), row.sha256, `${row.id}: runtime evidence changed since audit`);
}

console.log("Prime animation-bank audit V1 verified: 308 unique rows, current hashes, zero geometry mismatches and 28 explicit rejected/excluded entries.");

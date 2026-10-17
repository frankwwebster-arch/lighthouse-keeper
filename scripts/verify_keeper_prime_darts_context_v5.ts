import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const registerFile = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v5/batch-register.json");
const register = JSON.parse(fs.readFileSync(registerFile, "utf8"));
const dataFile = path.join(root, register.candidate.routeData);
const data = JSON.parse(fs.readFileSync(dataFile, "utf8"));
const predecessor = JSON.parse(fs.readFileSync(path.join(root, register.predecessor.route), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };
const geometryKey = (frame: any) => JSON.stringify({ ...frame, src: "" });

if (register.batchId !== "keeper-prime-darts-context-2026-10-17-v5" || data.schema !== "lighthouse-keeper/darts-context@5") fail("Wrong Darts V5 identity");
if (data.route.length !== 213 || predecessor.route.length !== data.route.length) fail("Darts route frame count changed");
if (!data.route.every((frame: any, index: number) => geometryKey(frame) === geometryKey(predecessor.route[index]))) fail("Darts V4 route geometry, timing or state changed");
if (!Object.values(register.checks).every(Boolean)) fail("A recorded Darts V5 check failed");
if (sha(dataFile) !== register.candidate.routeDataSha256) fail("Darts V5 route hash mismatch");
for (const field of ["page", "app"]) if (sha(path.join(root, register.candidate[field])) !== register.candidate[`${field}Sha256`]) fail(`Darts V5 ${field} hash mismatch`);

const page = fs.readFileSync(path.join(root, register.candidate.page), "utf8");
const app = fs.readFileSync(path.join(root, register.candidate.app), "utf8");
for (const id of ["skipOccurrence", "skipAsset", "restore", "exportPlan", "inspectSkipped"]) if (!page.includes(`id="${id}"`)) fail(`Darts V5 page missing ${id}`);
for (const required of ["localStorage.setItem", "localStorage.getItem", "skippedOccurrences", "skippedAssets", "makeDart", "Promise.all"]) if (!app.includes(required)) fail(`Darts V5 app missing ${required}`);
if ((app.match(/makeDart\('/g) ?? []).length < 2 || !page.includes(".dart .flights") || !page.includes(".dart .barrel") || !page.includes(".dart .tip")) fail("One shared detailed dart component is not used for both flight and board states");
if (!page.includes("Prime Darts redraw calibration V1") || !page.includes("Skip this pose everywhere") || !page.includes("Restore all frames")) fail("Darts V5 review copy or controls missing");
for (const entry of register.publishedAssets) {
  const source = path.join(root, entry.source);
  if (!fs.existsSync(source) || sha(source) !== entry.sourceSha256) fail(`Darts V5 published provenance mismatch ${entry.source}`);
}
if (register.approvalBoundary.candidateApproved || register.approvalBoundary.redrawApplied || register.approvalBoundary.finalChanged || register.approvalBoundary.runtimeChanged || register.approvalBoundary.productionChanged || register.approvalBoundary.promotionAllowed) fail("Darts V5 approval boundary breached");
console.log("Keeper Prime Darts Context V5 verified: V4 route unchanged, reversible occurrence/pose skipping retained, and one dart component drives airborne and stuck states.");

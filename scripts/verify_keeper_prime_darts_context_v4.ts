import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const registerFile = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v4/batch-register.json");
const register = JSON.parse(fs.readFileSync(registerFile, "utf8"));
const routeFile = path.join(root, register.candidate.routeData);
const data = JSON.parse(fs.readFileSync(routeFile, "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };

if (register.batchId !== "keeper-prime-darts-context-2026-10-17-v4" || data.schema !== "lighthouse-keeper/darts-context@4") fail("Wrong Darts V4 identity");
if (data.route.length !== 213 || !register.checks.routeFrameCountUnchanged || !register.checks.routeGeometryAndTimingUnchanged) fail("V3 route choreography changed");
if (register.checks.correctedCoreUniqueAssets !== 14 || register.checks.correctedCoreRouteUses !== 84) fail("Corrected core is not used for all six fourteen-frame throws");
if (data.route.filter((frame: any) => frame.flyingDart).length !== 30 || register.checks.projectileFlights !== 30) fail("Visible projectile flight sequence changed");
if (data.route.filter((frame: any) => frame.phase.startsWith("turn at ")).length === 0 || register.checks.turnEvents !== 2) fail("Turn contract changed");
if (!register.checks.controlsAndFullRoutePlaybackRetained) fail("Full-route controls were not retained");
if (sha(routeFile) !== register.candidate.routeDataSha256) fail("Route hash mismatch");
const pageFile = path.join(root, register.candidate.page);
if (sha(pageFile) !== register.candidate.pageSha256) fail("Page hash mismatch");
const html = fs.readFileSync(pageFile, "utf8");
if (!html.includes("complete-context V4") || !html.includes("cell-isolated fourteen-frame throw core") || !html.includes("Loop complete route")) fail("V4 full-animation reviewer copy or controls missing");
for (const entry of register.publishedAssets) {
  const file = path.join(root, entry.source);
  if (!fs.existsSync(file) || sha(file) !== entry.sourceSha256) fail(`Published provenance mismatch ${entry.source}`);
}
if (register.approvalBoundary.candidateApproved || register.approvalBoundary.paletteCorrected || register.approvalBoundary.finalChanged || register.approvalBoundary.runtimeChanged || register.approvalBoundary.productionChanged || register.approvalBoundary.promotionAllowed) fail("Approval boundary breached");
console.log("Keeper Prime Darts Context V4 verified: full 213-frame route retained with 84 isolated-core uses, six visible flights, frame stepping, looping and speed controls.");

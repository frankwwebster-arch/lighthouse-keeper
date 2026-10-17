import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { PNG } from "pngjs";

const root = path.resolve(import.meta.dirname, "..");
const registerFile = path.join(root, "art/drafts/keeper-prime-darts-redraw-2026-10-17-v1/batch-register.json");
const register = JSON.parse(fs.readFileSync(registerFile, "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };

if (register.batchId !== "keeper-prime-darts-redraw-2026-10-17-v1" || register.status !== "three-pose-calibration-awaiting-frank") fail("Wrong redraw calibration identity or status");
if (register.candidate.poses.length !== 3 || register.checks.poseCount !== 3) fail("Redraw calibration must contain exactly three key poses");
if (!register.checks.allSourceCanvases1122x1402 || !register.checks.allRegisteredCanvases448x320 || !register.checks.allCapTopsExact || !register.checks.allFloorRowsExact || !register.checks.allEdgeAlphaZero || !register.checks.uniformWholeCharacterScalingOnly) fail("Recorded redraw checks are incomplete");

for (const pose of register.candidate.poses) {
  const sourceFile = path.join(root, pose.source);
  const draftFile = path.join(root, pose.draft);
  if (sha(sourceFile) !== pose.sourceSha256 || sha(draftFile) !== pose.draftSha256) fail(`${pose.id} source/draft hash drift`);
  const source = PNG.sync.read(fs.readFileSync(sourceFile));
  const draft = PNG.sync.read(fs.readFileSync(draftFile));
  if (source.width !== 1122 || source.height !== 1402) fail(`${pose.id} source geometry drift`);
  if (draft.width !== 448 || draft.height !== 320) fail(`${pose.id} registered geometry drift`);
  let minY = draft.height;
  let maxY = -1;
  let edgeAlpha = 0;
  for (let y = 0; y < draft.height; y++) for (let x = 0; x < draft.width; x++) {
    const alpha = draft.data[(y * draft.width + x) * 4 + 3];
    if (!alpha) continue;
    minY = Math.min(minY, y);
    maxY = Math.max(maxY, y);
    if (x === 0 || y === 0 || x === draft.width - 1 || y === draft.height - 1) edgeAlpha++;
  }
  if (minY !== 18 || maxY !== 315 || edgeAlpha !== 0) fail(`${pose.id} cap/floor/gutter contract drift (${minY}, ${maxY}, ${edgeAlpha})`);
  if (pose.geometry.creativePixelWarp || pose.geometry.registeredFootAxisX !== 128) fail(`${pose.id} registration is no longer whole-character/anchor locked`);
}

const contactFile = path.join(root, register.candidate.contactSheet.file);
if (sha(contactFile) !== register.candidate.contactSheet.sha256) fail("Contact-sheet hash drift");
const page = fs.readFileSync(path.join(root, "public/keeper-review/keeper-prime-darts-redraw-v1/index.html"), "utf8");
for (const required of ["Three-pose drawing-family gate", "Exact Prime ghost", "448 × 320", "do not replace the fourteen-frame throw core"]) if (!page.includes(required)) fail(`Redraw page missing ${required}`);
if (register.approvalBoundary.candidateApproved || register.approvalBoundary.completeThrowCoreBuilt || register.approvalBoundary.finalChanged || register.approvalBoundary.runtimeChanged || register.approvalBoundary.productionChanged || register.approvalBoundary.promotionAllowed) fail("Redraw approval boundary breached");
console.log("Keeper Prime Darts redraw V1 verified: three Prime-derived key poses, exact cap/floor registration, 448×320 action cells and zero edge alpha; no route or production promotion.");

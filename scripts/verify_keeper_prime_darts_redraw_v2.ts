import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { PNG } from "pngjs";

const root = path.resolve(import.meta.dirname, "..");
const register = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-darts-redraw-2026-10-17-v2/batch-register.json"), "utf8"));
const approval = JSON.parse(fs.readFileSync(path.join(root, "docs/review/keeper-prime-darts-redraw-v1-approval-2026-10-17.json"), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };

if (approval.decision !== "approved-as-drawing-family-authority" || !approval.approvalBoundary.threeRegisteredKeyPosesApproved) fail("V1 drawing-family approval is not pinned");
if (register.batchId !== "keeper-prime-darts-redraw-2026-10-17-v2" || register.status !== "complete-prime-core-awaiting-frank") fail("Wrong redraw V2 identity/status");
if (register.coreSlots.length !== 14 || register.newBridgePoses.length !== 5) fail("Redraw V2 must have fourteen slots and five new bridges");
if (!Object.values(register.checks).every(Boolean)) fail("Recorded redraw V2 checks failed");
for (const pose of register.newBridgePoses) {
  if (sha(path.join(root, pose.source)) !== pose.sourceSha256 || sha(path.join(root, pose.draft)) !== pose.draftSha256) fail(`${pose.id} hash drift`);
}
for (const slot of register.coreSlots) {
  const file = path.join(root, slot.file);
  if (sha(file) !== slot.sha256) fail(`F${slot.frame} hash drift`);
  const png = PNG.sync.read(fs.readFileSync(file));
  if (png.width !== 448 || png.height !== 320) fail(`F${slot.frame} geometry drift`);
  let edge = 0;
  for (let x = 0; x < png.width; x++) edge += +(png.data[(x * 4) + 3] > 0) + +(png.data[(((png.height - 1) * png.width + x) * 4) + 3] > 0);
  for (let y = 0; y < png.height; y++) edge += +(png.data[((y * png.width) * 4) + 3] > 0) + +(png.data[((y * png.width + png.width - 1) * 4) + 3] > 0);
  if (edge) fail(`F${slot.frame} touches a cell edge`);
}
if (register.coreSlots[3].sha256 !== approval.approvedPoseHashes.windup || register.coreSlots[5].sha256 !== approval.approvedPoseHashes.release || register.coreSlots[7].sha256 !== approval.approvedPoseHashes.recovery) fail("Approved V1 poses are not exact in V2");
if (new Set(register.coreSlots.map((slot: any) => slot.sha256)).size !== 9) fail("Unexpected V2 unique-pose count");
const page = fs.readFileSync(path.join(root, register.page.file), "utf8");
for (const required of ["14-slot Prime redraw candidate", "Previous-frame ghost", "Fixed-scale unique-pose lineup", "nothing promoted"]) if (!page.includes(required)) fail(`Redraw V2 page missing ${required}`);
if (register.approvalBoundary.v2CoreApproved || register.approvalBoundary.finalChanged || register.approvalBoundary.runtimeChanged || register.approvalBoundary.productionChanged || register.approvalBoundary.promotionAllowed) fail("Redraw V2 approval boundary breached");
console.log("Keeper Prime Darts redraw V2 verified: 14 slots, nine Prime-derived poses, exact approved V1 authorities, clear 448×320 cells and no promotion.");

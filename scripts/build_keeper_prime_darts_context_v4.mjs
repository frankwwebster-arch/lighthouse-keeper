#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-darts-context-v4";
const pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v4");
const output = path.join(root, "public/keeper-review", set);
const assets = path.join(output, "assets");
const v3Pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v3");
const v3RegisterFile = path.join(v3Pack, "batch-register.json");
const v3DataFile = path.join(v3Pack, "keeper-prime-darts-context-v3.json");
const v3Register = JSON.parse(fs.readFileSync(v3RegisterFile, "utf8"));
const v3Data = JSON.parse(fs.readFileSync(v3DataFile, "utf8"));
const isolationRegisterFile = path.join(root, "art/drafts/keeper-prime-darts-isolation-2026-10-17-v1/batch-register.json");
const isolation = JSON.parse(fs.readFileSync(isolationRegisterFile, "utf8"));
const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

fs.mkdirSync(pack, { recursive: true });
fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(assets, { recursive: true });

const correctedCoreFiles = isolation.candidate.frames.slice(8, 22).map((entry) => path.join(root, entry.file));
if (correctedCoreFiles.length !== 14) throw new Error("Isolation register does not expose fourteen corrected core frames");
const oldCoreFiles = Array.from({ length: 14 }, (_, index) => path.join(root, `art/drafts/keeper-prime-darts-context-2026-10-17-v2/drafts/frames/keeper_prime_darts-core-right_f${String(index + 1).padStart(2, "0")}.png`));
const replacementBySource = new Map(oldCoreFiles.map((file, index) => [rel(file), correctedCoreFiles[index]]));
const byHash = new Map(), publishedAssets = [];
function publish(file, label) {
  const digest = sha(file);
  if (byHash.has(digest)) return byHash.get(digest);
  const name = `${label}-${digest.slice(0, 16)}${path.extname(file)}`;
  fs.copyFileSync(file, path.join(assets, name));
  const entry = { source: rel(file), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry); publishedAssets.push(entry); return entry;
}

const urlMap = new Map();
for (const entry of v3Register.publishedAssets) {
  const replacement = replacementBySource.get(entry.source);
  const sourceFile = replacement ?? path.join(root, entry.source);
  urlMap.set(entry.url, publish(sourceFile, replacement ? "isolated-dart" : path.basename(entry.url).split("-")[0]).url);
}
const route = v3Data.route.map((frame) => {
  const src = urlMap.get(frame.src);
  if (!src) throw new Error(`No V4 asset mapping for ${frame.src}`);
  return { ...frame, src, label: frame.label.replace("identical V2 throw core", "cell-isolated throw core") };
});
const data = { ...v3Data, schema: "lighthouse-keeper/darts-context@4", set, status: "corrective-draft-awaiting-frank", route };
const dataFile = path.join(pack, "keeper-prime-darts-context-v4.json");
writeJson(dataFile, data);
writeJson(path.join(output, "route.json"), data);

const app = fs.readFileSync(path.join(root, "public/keeper-review/keeper-prime-darts-context-v3/app.js"), "utf8")
  .replaceAll("/keeper-review/keeper-prime-darts-context-v3/", `/keeper-review/${set}/`);
fs.writeFileSync(path.join(output, "app.js"), app);
const pageFile = path.join(output, "index.html");
const html = fs.readFileSync(path.join(root, "public/keeper-review/keeper-prime-darts-context-v3/index.html"), "utf8")
  .replaceAll("Keeper Prime darts V3", "Keeper Prime darts V4")
  .replaceAll("Context workbench V2", "Context Workbench V5")
  .replaceAll("/keeper-review/keeper-prime-context-workbench-v2/", "/keeper-review/keeper-prime-context-workbench-v5/")
  .replaceAll("/keeper-review/keeper-prime-darts-context-v3/", `/keeper-review/${set}/`)
  .replace("Keeper Prime darts · complete-context V3", "Keeper Prime darts · complete-context V4")
  .replace("Walk to the oche, throw three visible darts, collect all three, turn once, walk back, turn once, and throw the same three again.", "The complete playable route, now using the cell-isolated fourteen-frame throw core: walk to the oche, throw three visible darts, collect all three, turn once, walk back, turn once, and throw the same three again.")
  .replace("<strong>Approval boundary:</strong> this is a new V3 route and measured scenery proposal. It reuses the V2 character pixels byte-for-byte, changes no approved art, and promotes nothing.", "<strong>Approval boundary:</strong> this is a new V4 corrective route. It changes only the fourteen unapproved throw-core cells to the isolated V1 candidate, preserves every approved transition asset, changes no Final/runtime/production art, and promotes nothing.");
fs.writeFileSync(pageFile, html);

const correctedHashes = new Set(correctedCoreFiles.map(sha));
const correctedUrls = new Set(publishedAssets.filter((entry) => correctedHashes.has(entry.sourceSha256)).map((entry) => entry.url));
const register = {
  schema: "lighthouse-keeper/review-batch@1", batchId: "keeper-prime-darts-context-2026-10-17-v4", status: "corrective-draft-awaiting-frank",
  purpose: "Complete playable Darts V3 choreography with the fourteen cell-isolated throw-core frames substituted in place of unsafe V2 rectangular crops.",
  predecessor: { register: rel(v3RegisterFile), sha256: sha(v3RegisterFile), route: rel(v3DataFile), routeSha256: sha(v3DataFile) },
  correctiveArt: { register: rel(isolationRegisterFile), sha256: sha(isolationRegisterFile) },
  candidate: { routeData: rel(dataFile), routeDataSha256: sha(dataFile), page: rel(pageFile), pageSha256: sha(pageFile) },
  checks: {
    routeFrameCountUnchanged: route.length === v3Data.route.length,
    routeGeometryAndTimingUnchanged: route.every((frame, index) => JSON.stringify({ ...frame, src: "", label: "" }) === JSON.stringify({ ...v3Data.route[index], src: "", label: "" })),
    correctedCoreUniqueAssets: correctedUrls.size,
    correctedCoreRouteUses: route.filter((frame) => correctedUrls.has(frame.src)).length,
    projectileFlights: route.filter((frame) => frame.flyingDart).length,
    turnEvents: 2,
    fullStrideCollectionAndReturnLp: 30.5,
    controlsAndFullRoutePlaybackRetained: true,
  },
  publishedAssets,
  approvalBoundary: { candidateApproved: false, paletteCorrected: false, finalChanged: false, runtimeChanged: false, productionChanged: false, promotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; V2, V3, isolation V1 and all authorities remain unchanged.`,
};
if (!register.checks.routeFrameCountUnchanged || !register.checks.routeGeometryAndTimingUnchanged || register.checks.correctedCoreUniqueAssets !== 14 || register.checks.correctedCoreRouteUses !== 84 || register.checks.projectileFlights !== 30) throw new Error(`Unexpected V4 route checks: ${JSON.stringify(register.checks)}`);
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), "# Keeper Prime Darts Context V4\n\nV4 restores full playable-route review while substituting the fourteen Darts Isolation V1 core cells for the unsafe V2 rectangular crops. Route order, timing, roots, scenery state, six throws, collection and two turns are unchanged from V3. Palette correction remains pending. Nothing is approved or promoted.\n");
console.log(JSON.stringify({ set, routeFrames: route.length, correctedCoreRouteUses: register.checks.correctedCoreRouteUses, projectileFlights: register.checks.projectileFlights, page: rel(pageFile) }, null, 2));

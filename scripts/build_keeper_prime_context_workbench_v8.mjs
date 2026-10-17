#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-context-workbench-v8";
const predecessorSet = "keeper-prime-context-workbench-v7";
const predecessorDir = path.join(root, "public/keeper-review", predecessorSet);
const predecessorRegisterFile = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v7/batch-register.json");
const predecessorRegister = JSON.parse(fs.readFileSync(predecessorRegisterFile, "utf8"));
const predecessorCatalog = JSON.parse(fs.readFileSync(path.join(predecessorDir, "catalog.json"), "utf8"));
const predecessorInventoryFile = path.join(predecessorDir, "inventory.json");
const dartsV7RegisterFile = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v7/batch-register.json");
const output = path.join(root, "public/keeper-review", set);
const assets = path.join(output, "assets");
const pack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v8");
const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

fs.mkdirSync(pack, { recursive: true });
fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(assets, { recursive: true });
const sourceByUrl = new Map(predecessorRegister.publishedAssets.map((entry) => [entry.url, path.join(root, entry.source)]));
const publishedAssets = [], byHash = new Map();
function localise(url) {
  const source = sourceByUrl.get(url);
  if (!source) throw new Error(`Missing Workbench V7 source provenance for ${url}`);
  const digest = sha(source);
  if (byHash.has(digest)) return byHash.get(digest).url;
  const name = `frame-${digest.slice(0, 16)}${path.extname(source)}`;
  fs.copyFileSync(source, path.join(assets, name));
  const entry = { source: rel(source), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry); publishedAssets.push(entry); return entry.url;
}

const sequences = predecessorCatalog.sequences.map((sequence) => {
  if (sequence.kind === "native") return { ...sequence, frames: sequence.frames.map((frame) => ({ ...frame, src: localise(frame.src) })) };
  if (sequence.id === "darts-v6") return {
    ...sequence,
    id: "darts-v7",
    title: "Candidate · direct side-on Prime Darts V7 animation",
    status: "redundant camera-facing detours removed; action-cell foot axis corrected; nothing promoted",
    summary: "Complete approach, six Prime-redrawn throws, collection and return with a zero-pixel neutral entry seam and reversible frame skipping.",
    url: "/keeper-review/keeper-prime-darts-context-v7/",
  };
  return sequence;
});
if (!sequences.some((entry) => entry.id === "darts-v7") || sequences.some((entry) => entry.id === "darts-v6") || sequences.length !== 10) throw new Error("Workbench V8 Darts choice is incomplete");
const catalog = {
  ...predecessorCatalog,
  schema: "lighthouse-keeper/context-workbench@8",
  set,
  exactPrimeGhost: localise(predecessorCatalog.exactPrimeGhost),
  inventoryUrl: `/keeper-review/${predecessorSet}/inventory.json`,
  sequences,
  addedInV8: "Darts Context V7 removes redundant camera-facing bridges and corrects the 448px action-cell foot axis.",
};
const catalogFile = path.join(output, "catalog.json");
writeJson(catalogFile, catalog);
const appFile = path.join(output, "app.js");
fs.writeFileSync(appFile, fs.readFileSync(path.join(predecessorDir, "app.js"), "utf8").replaceAll(predecessorSet, set));
const pageFile = path.join(output, "index.html");
fs.writeFileSync(pageFile, fs.readFileSync(path.join(predecessorDir, "index.html"), "utf8")
  .replaceAll("Prime Keeper contextual animation workbench V7", "Prime Keeper contextual animation workbench V8")
  .replaceAll("Context Workbench V7", "Context Workbench V8")
  .replaceAll(predecessorSet, set)
  .replace("V7 retains every prior route and diagnostic view, replaces the inherited Darts actor core with the complete Prime-derived V2 redraw, and keeps the full contextual route tunable.", "V8 retains every prior route and diagnostic view, and replaces Darts V6 with the corrected V7 route: no unnecessary camera-facing stance detour and no backward anchor jump into the throw core."));

const register = {
  schema: "lighthouse-keeper/review-batch@1",
  batchId: "keeper-prime-context-workbench-2026-10-17-v8",
  status: "review-tool-awaiting-frank",
  purpose: predecessorCatalog.purpose,
  predecessor: { register: rel(predecessorRegisterFile), sha256: sha(predecessorRegisterFile), role: "immutable Workbench V7" },
  playableDartsCandidate: { register: rel(dartsV7RegisterFile), sha256: sha(dartsV7RegisterFile) },
  inventory: { file: rel(predecessorInventoryFile), sha256: sha(predecessorInventoryFile), reusedWithoutDuplication: true },
  catalog: { file: rel(catalogFile), sha256: sha(catalogFile) },
  page: { file: rel(pageFile), sha256: sha(pageFile) },
  app: { file: rel(appFile), sha256: sha(appFile) },
  coverage: sequences.map(({ id, title, status, kind }) => ({ id, title, status, kind })),
  features: [...new Set([...predecessorRegister.features, "zero-pixel Darts neutral entry seam", "correct 16-lp action-cell foot axis"])],
  publishedAssets,
  boundaries: predecessorCatalog.boundaries,
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; Workbench V1–V7 and Darts V1–V7 remain unchanged.`,
};
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), "# Prime Keeper Context Workbench V8\n\nV8 retains all ten V7 choices and points the playable Darts choice to corrected Context V7. The V2 core inspector and every earlier diagnostic remain available. Nothing is approved or promoted.\n");
console.log(JSON.stringify({ set, sequences: sequences.length, playableDarts: sequences.find((entry) => entry.id === "darts-v7")?.url, uniqueAssets: publishedAssets.length }, null, 2));

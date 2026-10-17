#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-context-workbench-v4";
const predecessorSet = "keeper-prime-context-workbench-v3";
const predecessorDir = path.join(root, "public/keeper-review", predecessorSet);
const predecessorPack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v3");
const predecessorRegister = JSON.parse(fs.readFileSync(path.join(predecessorPack, "batch-register.json"), "utf8"));
const predecessorCatalog = JSON.parse(fs.readFileSync(path.join(predecessorDir, "catalog.json"), "utf8"));
const inventory = JSON.parse(fs.readFileSync(path.join(predecessorDir, "inventory.json"), "utf8"));
const isolationRegisterFile = path.join(root, "art/drafts/keeper-prime-darts-isolation-2026-10-17-v1/batch-register.json");
const output = path.join(root, "public/keeper-review", set);
const assets = path.join(output, "assets");
const pack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v4");
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
  if (!source) throw new Error(`Missing V3 source provenance for ${url}`);
  const digest = sha(source);
  if (byHash.has(digest)) return byHash.get(digest).url;
  const name = `frame-${digest.slice(0, 16)}${path.extname(source)}`;
  fs.copyFileSync(source, path.join(assets, name));
  const entry = { source: rel(source), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry); publishedAssets.push(entry); return entry.url;
}

const sequences = predecessorCatalog.sequences.map((sequence) => sequence.kind === "native" ? { ...sequence, frames: sequence.frames.map((frame) => ({ ...frame, src: localise(frame.src) })) } : sequence);
sequences.push({
  id: "darts-cell-isolation-v1",
  title: "Corrective draft · Darts cell isolation V1",
  status: "awaiting review; nothing promoted",
  summary: "Side-by-side evidence for the 14 corrected throw-core cells: whole-component actor ownership, no neighbouring-frame fragments, and detached darts kept as separate effects.",
  kind: "external",
  url: "/keeper-review/keeper-prime-darts-isolation-v1/",
});
const catalog = { ...predecessorCatalog, schema: "lighthouse-keeper/context-workbench@4", set, exactPrimeGhost: localise(predecessorCatalog.exactPrimeGhost), inventoryUrl: `/keeper-review/${set}/inventory.json`, sequences, addedInV4: "Versioned Darts cell-isolation corrective draft with old/new/overlay inspection." };
const catalogFile = path.join(output, "catalog.json");
writeJson(catalogFile, catalog);
writeJson(path.join(output, "inventory.json"), inventory);
fs.writeFileSync(path.join(output, "app.js"), fs.readFileSync(path.join(predecessorDir, "app.js"), "utf8").replaceAll(`/keeper-review/${predecessorSet}/`, `/keeper-review/${set}/`));
const pageFile = path.join(output, "index.html");
fs.writeFileSync(pageFile, fs.readFileSync(path.join(predecessorDir, "index.html"), "utf8")
  .replaceAll("Prime Keeper contextual animation workbench V3", "Prime Keeper contextual animation workbench V4")
  .replaceAll("Context Workbench V3", "Context Workbench V4")
  .replaceAll(`/keeper-review/${predecessorSet}/`, `/keeper-review/${set}/`)
  .replace("V3 retains the deployment-safe full-width viewer and adds detailed frame-by-frame inspection of the inherited Darts V2 strip.", "V4 retains every prior view and adds the reversible Darts cell-isolation correction for side-by-side inspection.")
  .replace("Eight current authorities, candidates or inspection views", "Nine current authorities, candidates or inspection views"));

const register = {
  schema: "lighthouse-keeper/review-batch@1", batchId: "keeper-prime-context-workbench-2026-10-17-v4", status: "review-tool-awaiting-frank", purpose: predecessorCatalog.purpose,
  predecessor: { register: rel(path.join(predecessorPack, "batch-register.json")), sha256: sha(path.join(predecessorPack, "batch-register.json")), role: "immutable Workbench V3" },
  correctiveDraft: { register: rel(isolationRegisterFile), sha256: sha(isolationRegisterFile) },
  catalog: { file: rel(catalogFile), sha256: sha(catalogFile) }, page: { file: rel(pageFile), sha256: sha(pageFile) },
  coverage: sequences.map(({ id, title, status, kind }) => ({ id, title, status, kind })),
  features: [...predecessorRegister.features, "Darts cell-isolation old/new/overlay review"], publishedAssets, boundaries: predecessorCatalog.boundaries,
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; all earlier workbenches and animation evidence remain unchanged.`,
};
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), "# Prime Keeper Context Workbench V4\n\nV4 retains all eight Workbench V3 choices and adds the Darts cell-isolation corrective review as a ninth external choice. No animation has been approved or promoted.\n");
console.log(JSON.stringify({ set, sequences: sequences.length, native: sequences.filter((entry) => entry.kind === "native").length, external: sequences.filter((entry) => entry.kind === "external").length, uniqueAssets: publishedAssets.length }, null, 2));

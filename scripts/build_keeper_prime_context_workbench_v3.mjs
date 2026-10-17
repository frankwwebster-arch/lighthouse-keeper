#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-context-workbench-v3";
const predecessorSet = "keeper-prime-context-workbench-v2";
const predecessorDir = path.join(root, "public/keeper-review", predecessorSet);
const predecessorPack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v2");
const predecessorRegister = JSON.parse(fs.readFileSync(path.join(predecessorPack, "batch-register.json"), "utf8"));
const predecessorCatalog = JSON.parse(fs.readFileSync(path.join(predecessorDir, "catalog.json"), "utf8"));
const inventory = JSON.parse(fs.readFileSync(path.join(predecessorDir, "inventory.json"), "utf8"));
const output = path.join(root, "public/keeper-review", set);
const assets = path.join(output, "assets");
const pack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v3");
const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

fs.mkdirSync(pack, { recursive: true });
fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(assets, { recursive: true });
const sourceByUrl = new Map(predecessorRegister.publishedAssets.map((entry) => [entry.url, path.join(root, entry.source)]));
const publishedAssets = [];
const byHash = new Map();
function localise(url) {
  const source = sourceByUrl.get(url);
  if (!source) throw new Error(`Missing V2 source provenance for ${url}`);
  const digest = sha(source);
  if (byHash.has(digest)) return byHash.get(digest).url;
  const name = `frame-${digest.slice(0, 16)}${path.extname(source)}`;
  fs.copyFileSync(source, path.join(assets, name));
  const entry = { source: rel(source), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry);
  publishedAssets.push(entry);
  return entry.url;
}

const sequences = predecessorCatalog.sequences.map((sequence) => sequence.kind === "native" ? {
  ...sequence,
  frames: sequence.frames.map((frame) => ({ ...frame, src: localise(frame.src) })),
} : sequence);
sequences.push({
  id: "darts-v2-strip-inspector",
  title: "Inspect · Darts V2 registered strip · all 30 frames",
  status: "inspection only; no art changed",
  summary: "Exact-source zoom, frame stepping, Prime/adjacent overlays and deterministic blue/navy/cream comparisons for every inherited V2 cell.",
  kind: "external",
  url: "/keeper-review/keeper-prime-darts-strip-inspector-v1/",
});
const catalog = {
  ...predecessorCatalog,
  schema: "lighthouse-keeper/context-workbench@3",
  set,
  exactPrimeGhost: localise(predecessorCatalog.exactPrimeGhost),
  inventoryUrl: `/keeper-review/${set}/inventory.json`,
  sequences,
  addedInV3: "Dedicated frame-by-frame and palette inspector for the immutable Darts V2 registered strip.",
};
const catalogFile = path.join(output, "catalog.json");
writeJson(catalogFile, catalog);
writeJson(path.join(output, "inventory.json"), inventory);

const predecessorApp = fs.readFileSync(path.join(predecessorDir, "app.js"), "utf8");
const app = predecessorApp.replaceAll(`/keeper-review/${predecessorSet}/`, `/keeper-review/${set}/`);
fs.writeFileSync(path.join(output, "app.js"), app);
const predecessorHtml = fs.readFileSync(path.join(predecessorDir, "index.html"), "utf8");
const html = predecessorHtml
  .replaceAll("Prime Keeper contextual animation workbench V2", "Prime Keeper contextual animation workbench V3")
  .replaceAll("Context Workbench V2", "Context Workbench V3")
  .replaceAll(`/keeper-review/${predecessorSet}/`, `/keeper-review/${set}/`)
  .replace("V2 fixes the deployed catalogue-loading fault and gives the large inspection pane the full browser width.", "V3 retains the deployment-safe full-width viewer and adds detailed frame-by-frame inspection of the inherited Darts V2 strip.")
  .replace("Seven current authorities or candidates", "Eight current authorities, candidates or inspection views");
const pageFile = path.join(output, "index.html");
fs.writeFileSync(pageFile, html);

const register = {
  schema: "lighthouse-keeper/review-batch@1",
  batchId: "keeper-prime-context-workbench-2026-10-17-v3",
  status: "review-tool-awaiting-frank",
  purpose: predecessorCatalog.purpose,
  predecessor: { register: rel(path.join(predecessorPack, "batch-register.json")), sha256: sha(path.join(predecessorPack, "batch-register.json")), role: "immutable deployment-safe V2 viewer" },
  catalog: { file: rel(catalogFile), sha256: sha(catalogFile) },
  page: { file: rel(pageFile), sha256: sha(pageFile) },
  coverage: sequences.map(({ id, title, status, kind }) => ({ id, title, status, kind })),
  features: [...predecessorRegister.features, "Darts V2 30-frame registered-strip inspector", "per-frame deterministic palette measurements"],
  publishedAssets,
  boundaries: predecessorCatalog.boundaries,
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; V1, V2 and all animation evidence remain unchanged.`,
};
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), `# Prime Keeper Context Workbench V3\n\nV3 keeps V2's deployment-safe full-width viewer and all seven existing choices, then adds the Darts V2 registered-strip inspector as an eighth external review choice. No animation or approval changed.\n`);
console.log(JSON.stringify({ set, sequences: sequences.length, native: sequences.filter((entry) => entry.kind === "native").length, external: sequences.filter((entry) => entry.kind === "external").length, uniqueAssets: publishedAssets.length }, null, 2));

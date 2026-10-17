#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-context-workbench-v5";
const predecessorSet = "keeper-prime-context-workbench-v4";
const predecessorDir = path.join(root, "public/keeper-review", predecessorSet);
const predecessorPack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v4");
const predecessorRegisterFile = path.join(predecessorPack, "batch-register.json");
const predecessorRegister = JSON.parse(fs.readFileSync(predecessorRegisterFile, "utf8"));
const predecessorCatalog = JSON.parse(fs.readFileSync(path.join(predecessorDir, "catalog.json"), "utf8"));
const inventory = JSON.parse(fs.readFileSync(path.join(predecessorDir, "inventory.json"), "utf8"));
const dartsV4RegisterFile = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v4/batch-register.json");
const output = path.join(root, "public/keeper-review", set);
const assets = path.join(output, "assets");
const pack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v5");
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
  if (!source) throw new Error(`Missing V4 source provenance for ${url}`);
  const digest = sha(source);
  if (byHash.has(digest)) return byHash.get(digest).url;
  const name = `frame-${digest.slice(0, 16)}${path.extname(source)}`;
  fs.copyFileSync(source, path.join(assets, name));
  const entry = { source: rel(source), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry); publishedAssets.push(entry); return entry.url;
}

const sequences = predecessorCatalog.sequences.map((sequence) => {
  if (sequence.kind === "native") return { ...sequence, frames: sequence.frames.map((frame) => ({ ...frame, src: localise(frame.src) })) };
  if (sequence.id === "darts-v3") return { ...sequence, id: "darts-v4", title: "Corrective candidate · full Darts V4 animation", status: "cell-isolated core; palette pending; nothing promoted", summary: "Complete playable approach, six throws, collection, two necessary turns and return, now using the isolated fourteen-frame core.", url: "/keeper-review/keeper-prime-darts-context-v4/" };
  return sequence;
});
if (!sequences.some((entry) => entry.id === "darts-v4") || sequences.some((entry) => entry.id === "darts-v3")) throw new Error("Darts V4 did not replace Darts V3 in the selector");
const catalog = { ...predecessorCatalog, schema: "lighthouse-keeper/context-workbench@5", set, exactPrimeGhost: localise(predecessorCatalog.exactPrimeGhost), inventoryUrl: `/keeper-review/${set}/inventory.json`, sequences, addedInV5: "Restored complete playable Darts review using the cell-isolated core." };
const catalogFile = path.join(output, "catalog.json");
writeJson(catalogFile, catalog);
writeJson(path.join(output, "inventory.json"), inventory);
fs.writeFileSync(path.join(output, "app.js"), fs.readFileSync(path.join(predecessorDir, "app.js"), "utf8").replaceAll(`/keeper-review/${predecessorSet}/`, `/keeper-review/${set}/`));
const pageFile = path.join(output, "index.html");
fs.writeFileSync(pageFile, fs.readFileSync(path.join(predecessorDir, "index.html"), "utf8")
  .replaceAll("Prime Keeper contextual animation workbench V4", "Prime Keeper contextual animation workbench V5")
  .replaceAll("Context Workbench V4", "Context Workbench V5")
  .replaceAll(`/keeper-review/${predecessorSet}/`, `/keeper-review/${set}/`)
  .replace("V4 retains every prior view and adds the reversible Darts cell-isolation correction for side-by-side inspection.", "V5 keeps the cell-isolation comparison and restores the complete playable Darts route with those corrected cells."));

const register = {
  schema: "lighthouse-keeper/review-batch@1", batchId: "keeper-prime-context-workbench-2026-10-17-v5", status: "review-tool-awaiting-frank", purpose: predecessorCatalog.purpose,
  predecessor: { register: rel(predecessorRegisterFile), sha256: sha(predecessorRegisterFile), role: "immutable Workbench V4" },
  playableDartsCandidate: { register: rel(dartsV4RegisterFile), sha256: sha(dartsV4RegisterFile) },
  catalog: { file: rel(catalogFile), sha256: sha(catalogFile) }, page: { file: rel(pageFile), sha256: sha(pageFile) },
  coverage: sequences.map(({ id, title, status, kind }) => ({ id, title, status, kind })),
  features: [...predecessorRegister.features, "complete playable Darts V4 route with isolated cells"], publishedAssets, boundaries: predecessorCatalog.boundaries,
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; Workbench V4, Darts V3/V4 and all evidence remain unchanged.`,
};
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), "# Prime Keeper Context Workbench V5\n\nV5 retains all nine Workbench V4 choices but replaces the old playable Darts V3 link with Darts V4, whose complete 213-frame route uses the isolated fourteen-frame core. The frame-isolation comparison and immutable V2 inspector remain separately available. Nothing is approved or promoted.\n");
console.log(JSON.stringify({ set, sequences: sequences.length, playableDarts: sequences.find((entry) => entry.id === "darts-v4")?.url, uniqueAssets: publishedAssets.length }, null, 2));

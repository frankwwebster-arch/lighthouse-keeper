#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-context-workbench-v6";
const predecessorSet = "keeper-prime-context-workbench-v5";
const predecessorDir = path.join(root, "public/keeper-review", predecessorSet);
const predecessorPack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v5");
const predecessorRegisterFile = path.join(predecessorPack, "batch-register.json");
const predecessorRegister = JSON.parse(fs.readFileSync(predecessorRegisterFile, "utf8"));
const predecessorCatalog = JSON.parse(fs.readFileSync(path.join(predecessorDir, "catalog.json"), "utf8"));
const inventory = JSON.parse(fs.readFileSync(path.join(predecessorDir, "inventory.json"), "utf8"));
const dartsV5RegisterFile = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v5/batch-register.json");
const redrawV1RegisterFile = path.join(root, "art/drafts/keeper-prime-darts-redraw-2026-10-17-v1/batch-register.json");
const output = path.join(root, "public/keeper-review", set);
const assets = path.join(output, "assets");
const pack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v6");
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
  if (!source) throw new Error(`Missing Workbench V5 source provenance for ${url}`);
  const digest = sha(source);
  if (byHash.has(digest)) return byHash.get(digest).url;
  const name = `frame-${digest.slice(0, 16)}${path.extname(source)}`;
  fs.copyFileSync(source, path.join(assets, name));
  const entry = { source: rel(source), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry); publishedAssets.push(entry); return entry.url;
}

const sequences = predecessorCatalog.sequences.map((sequence) => {
  if (sequence.kind === "native") return { ...sequence, frames: sequence.frames.map((frame) => ({ ...frame, src: localise(frame.src) })) };
  if (sequence.id === "darts-v4") return {
    ...sequence,
    id: "darts-v5",
    title: "Tunable candidate · full Darts V5 animation",
    status: "frame skipping + matching dart effect; Prime redraw pending; nothing promoted",
    summary: "Complete approach, six throws, collection and return with reversible occurrence/pose skipping and one shared airborne/stuck dart design.",
    url: "/keeper-review/keeper-prime-darts-context-v5/",
  };
  return sequence;
});
sequences.push({
  id: "darts-prime-redraw-v1",
  title: "Drawing-family gate · Prime Darts redraw V1",
  status: "three Prime-derived key poses; not a complete animation",
  summary: "Compare exact Prime with the new wind-up, release and recovery drawings before the full throw core is commissioned.",
  kind: "external",
  url: "/keeper-review/keeper-prime-darts-redraw-v1/",
});
if (!sequences.some((entry) => entry.id === "darts-v5") || sequences.some((entry) => entry.id === "darts-v4") || !sequences.some((entry) => entry.id === "darts-prime-redraw-v1")) throw new Error("Workbench V6 Darts choices are incomplete");

const catalog = {
  ...predecessorCatalog,
  schema: "lighthouse-keeper/context-workbench@6",
  set,
  exactPrimeGhost: localise(predecessorCatalog.exactPrimeGhost),
  inventoryUrl: `/keeper-review/${set}/inventory.json`,
  sequences,
  addedInV6: "Tunable full-route Darts V5 plus a separate three-pose Prime redraw calibration gate.",
};
const catalogFile = path.join(output, "catalog.json");
writeJson(catalogFile, catalog);
writeJson(path.join(output, "inventory.json"), inventory);
fs.writeFileSync(path.join(output, "app.js"), fs.readFileSync(path.join(predecessorDir, "app.js"), "utf8").replaceAll(`/keeper-review/${predecessorSet}/`, `/keeper-review/${set}/`));
const pageFile = path.join(output, "index.html");
fs.writeFileSync(pageFile, fs.readFileSync(path.join(predecessorDir, "index.html"), "utf8")
  .replaceAll("Prime Keeper contextual animation workbench V5", "Prime Keeper contextual animation workbench V6")
  .replaceAll("Context Workbench V5", "Context Workbench V6")
  .replaceAll(`/keeper-review/${predecessorSet}/`, `/keeper-review/${set}/`)
  .replace("Nine current authorities, candidates or inspection views", "Ten current authorities, candidates or inspection views")
  .replace("V5 keeps the cell-isolation comparison and restores the complete playable Darts route with those corrected cells.", "V6 retains every prior route and diagnostic view, upgrades Darts to the tunable V5 route, and adds the separate Prime redraw calibration gate."));

const register = {
  schema: "lighthouse-keeper/review-batch@1",
  batchId: "keeper-prime-context-workbench-2026-10-17-v6",
  status: "review-tool-awaiting-frank",
  purpose: predecessorCatalog.purpose,
  predecessor: { register: rel(predecessorRegisterFile), sha256: sha(predecessorRegisterFile), role: "immutable Workbench V5" },
  playableDartsCandidate: { register: rel(dartsV5RegisterFile), sha256: sha(dartsV5RegisterFile) },
  dartsRedrawCalibration: { register: rel(redrawV1RegisterFile), sha256: sha(redrawV1RegisterFile) },
  catalog: { file: rel(catalogFile), sha256: sha(catalogFile) },
  page: { file: rel(pageFile), sha256: sha(pageFile) },
  coverage: sequences.map(({ id, title, status, kind }) => ({ id, title, status, kind })),
  features: [...predecessorRegister.features, "browser-local Darts occurrence/pose skipping with JSON export", "three-pose Prime Darts redraw calibration"],
  publishedAssets,
  boundaries: predecessorCatalog.boundaries,
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; Workbench V5, Darts V1-V5 and redraw V1 remain unchanged.`,
};
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), "# Prime Keeper Context Workbench V6\n\nV6 retains all nine V5 choices, replaces the playable Darts V4 link with tunable V5, and adds the three-pose Prime redraw calibration as a tenth choice. Nothing is approved or promoted.\n");
console.log(JSON.stringify({ set, sequences: sequences.length, playableDarts: sequences.find((entry) => entry.id === "darts-v5")?.url, redraw: sequences.find((entry) => entry.id === "darts-prime-redraw-v1")?.url, uniqueAssets: publishedAssets.length }, null, 2));

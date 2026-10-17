#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-context-workbench-v7";
const predecessorSet = "keeper-prime-context-workbench-v6";
const predecessorDir = path.join(root, "public/keeper-review", predecessorSet);
const predecessorPack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v6");
const predecessorRegisterFile = path.join(predecessorPack, "batch-register.json");
const predecessorRegister = JSON.parse(fs.readFileSync(predecessorRegisterFile, "utf8"));
const predecessorCatalog = JSON.parse(fs.readFileSync(path.join(predecessorDir, "catalog.json"), "utf8"));
const inventory = JSON.parse(fs.readFileSync(path.join(predecessorDir, "inventory.json"), "utf8"));
const dartsV6RegisterFile = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v6/batch-register.json");
const redrawV2RegisterFile = path.join(root, "art/drafts/keeper-prime-darts-redraw-2026-10-17-v2/batch-register.json");
const output = path.join(root, "public/keeper-review", set);
const assets = path.join(output, "assets");
const pack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v7");
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
  if (!source) throw new Error(`Missing Workbench V6 source provenance for ${url}`);
  const digest = sha(source);
  if (byHash.has(digest)) return byHash.get(digest).url;
  const name = `frame-${digest.slice(0, 16)}${path.extname(source)}`;
  fs.copyFileSync(source, path.join(assets, name));
  const entry = { source: rel(source), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry); publishedAssets.push(entry); return entry.url;
}

const sequences = predecessorCatalog.sequences.map((sequence) => {
  if (sequence.kind === "native") return { ...sequence, frames: sequence.frames.map((frame) => ({ ...frame, src: localise(frame.src) })) };
  if (sequence.id === "darts-v5") return {
    ...sequence,
    id: "darts-v6",
    title: "Candidate · complete Prime-redrawn Darts V6 animation",
    status: "all throw-core actor pixels Prime-derived; route mechanics unchanged; nothing promoted",
    summary: "Complete approach, six Prime-redrawn throws, collection and return with reversible frame skipping and one matching dart design.",
    url: "/keeper-review/keeper-prime-darts-context-v6/",
  };
  if (sequence.id === "darts-prime-redraw-v1") return {
    ...sequence,
    id: "darts-prime-redraw-v2",
    title: "Candidate · registered 14-slot Prime Darts core V2",
    status: "approved V1 keyframes plus five new Prime-derived bridges; nothing promoted",
    summary: "Inspect every throw-core slot and all nine unique registered poses before approving the complete action family.",
    url: "/keeper-review/keeper-prime-darts-redraw-v2/",
  };
  return sequence;
});
if (!sequences.some((entry) => entry.id === "darts-v6") || sequences.some((entry) => entry.id === "darts-v5") || !sequences.some((entry) => entry.id === "darts-prime-redraw-v2") || sequences.length !== 10) throw new Error("Workbench V7 Darts choices are incomplete");

const catalog = {
  ...predecessorCatalog,
  schema: "lighthouse-keeper/context-workbench@7",
  set,
  exactPrimeGhost: localise(predecessorCatalog.exactPrimeGhost),
  inventoryUrl: `/keeper-review/${set}/inventory.json`,
  sequences,
  addedInV7: "Complete-context Darts V6 with the full Prime-derived core, plus its registered 14-slot redraw inspector V2.",
};
const catalogFile = path.join(output, "catalog.json");
writeJson(catalogFile, catalog);
writeJson(path.join(output, "inventory.json"), inventory);
fs.writeFileSync(path.join(output, "app.js"), fs.readFileSync(path.join(predecessorDir, "app.js"), "utf8").replaceAll(`/keeper-review/${predecessorSet}/`, `/keeper-review/${set}/`));
const pageFile = path.join(output, "index.html");
fs.writeFileSync(pageFile, fs.readFileSync(path.join(predecessorDir, "index.html"), "utf8")
  .replaceAll("Prime Keeper contextual animation workbench V6", "Prime Keeper contextual animation workbench V7")
  .replaceAll("Context Workbench V6", "Context Workbench V7")
  .replaceAll(`/keeper-review/${predecessorSet}/`, `/keeper-review/${set}/`)
  .replace("V6 retains every prior route and diagnostic view, upgrades Darts to the tunable V5 route, and adds the separate Prime redraw calibration gate.", "V7 retains every prior route and diagnostic view, replaces the inherited Darts actor core with the complete Prime-derived V2 redraw, and keeps the full contextual route tunable."));

const register = {
  schema: "lighthouse-keeper/review-batch@1",
  batchId: "keeper-prime-context-workbench-2026-10-17-v7",
  status: "review-tool-awaiting-frank",
  purpose: predecessorCatalog.purpose,
  predecessor: { register: rel(predecessorRegisterFile), sha256: sha(predecessorRegisterFile), role: "immutable Workbench V6" },
  playableDartsCandidate: { register: rel(dartsV6RegisterFile), sha256: sha(dartsV6RegisterFile) },
  dartsRedrawCore: { register: rel(redrawV2RegisterFile), sha256: sha(redrawV2RegisterFile) },
  catalog: { file: rel(catalogFile), sha256: sha(catalogFile) },
  page: { file: rel(pageFile), sha256: sha(pageFile) },
  coverage: sequences.map(({ id, title, status, kind }) => ({ id, title, status, kind })),
  features: [...new Set([...predecessorRegister.features, "complete Prime-derived Darts throw core", "registered fourteen-slot Darts core inspector"])],
  publishedAssets,
  boundaries: predecessorCatalog.boundaries,
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; Workbench V1-V6, Darts V1-V6 and redraw V1-V2 remain unchanged.`,
};
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), "# Prime Keeper Context Workbench V7\n\nV7 retains all ten V6 choices, replaces the inherited-core Darts route with complete Prime-redrawn Darts V6, and replaces the three-pose calibration link with the registered fourteen-slot V2 core inspector. Nothing is approved or promoted.\n");
console.log(JSON.stringify({ set, sequences: sequences.length, playableDarts: sequences.find((entry) => entry.id === "darts-v6")?.url, redraw: sequences.find((entry) => entry.id === "darts-prime-redraw-v2")?.url, uniqueAssets: publishedAssets.length }, null, 2));

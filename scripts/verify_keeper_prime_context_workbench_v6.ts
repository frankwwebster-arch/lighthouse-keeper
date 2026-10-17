import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const publicDir = path.join(root, "public/keeper-review/keeper-prime-context-workbench-v6");
const register = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v6/batch-register.json"), "utf8"));
const catalog = JSON.parse(fs.readFileSync(path.join(publicDir, "catalog.json"), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };

if (catalog.schema !== "lighthouse-keeper/context-workbench@6" || catalog.sequences.length !== 10) fail("Wrong Workbench V6 identity or choice count");
const darts = catalog.sequences.find((entry: any) => entry.id === "darts-v5");
const redraw = catalog.sequences.find((entry: any) => entry.id === "darts-prime-redraw-v1");
if (!darts || darts.url !== "/keeper-review/keeper-prime-darts-context-v5/" || darts.kind !== "external") fail("Tunable Darts V5 choice missing");
if (!redraw || redraw.url !== "/keeper-review/keeper-prime-darts-redraw-v1/" || redraw.kind !== "external") fail("Prime Darts redraw calibration choice missing");
if (catalog.sequences.some((entry: any) => entry.id === "darts-v4")) fail("Superseded playable Darts V4 choice remains");
if (!catalog.sequences.some((entry: any) => entry.id === "darts-cell-isolation-v1") || !catalog.sequences.some((entry: any) => entry.id === "darts-v2-strip-inspector")) fail("Darts diagnostic views were lost");
if (!fs.existsSync(path.join(root, "public/keeper-review/keeper-prime-darts-context-v5/index.html")) || !fs.existsSync(path.join(root, "public/keeper-review/keeper-prime-darts-redraw-v1/index.html"))) fail("Darts V5 or redraw page missing");
if (sha(path.join(publicDir, "catalog.json")) !== register.catalog.sha256 || sha(path.join(publicDir, "index.html")) !== register.page.sha256) fail("Workbench V6 page/catalog hashes mismatch");
if (!fs.readFileSync(path.join(publicDir, "index.html"), "utf8").includes("adds the separate Prime redraw calibration gate")) fail("Workbench V6 copy does not explain the new split review");
for (const entry of register.publishedAssets) {
  const file = path.join(root, entry.source);
  if (!fs.existsSync(file) || sha(file) !== entry.sourceSha256) fail(`Published provenance mismatch ${entry.source}`);
}
console.log("Prime Context Workbench V6 verified: 10 choices, tunable Darts V5 and separate Prime redraw calibration added without losing prior routes or diagnostics.");

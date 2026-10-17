import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const publicDir = path.join(root, "public/keeper-review/keeper-prime-context-workbench-v4");
const registerFile = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v4/batch-register.json");
const register = JSON.parse(fs.readFileSync(registerFile, "utf8"));
const catalog = JSON.parse(fs.readFileSync(path.join(publicDir, "catalog.json"), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };

if (catalog.schema !== "lighthouse-keeper/context-workbench@4" || catalog.set !== "keeper-prime-context-workbench-v4") fail("Wrong Workbench V4 catalogue identity");
if (catalog.sequences.length !== 9) fail(`Expected 9 choices, found ${catalog.sequences.length}`);
const isolation = catalog.sequences.find((entry: any) => entry.id === "darts-cell-isolation-v1");
if (!isolation || isolation.kind !== "external" || isolation.url !== "/keeper-review/keeper-prime-darts-isolation-v1/") fail("Darts isolation choice is missing or wrong");
if (!fs.existsSync(path.join(root, "public/keeper-review/keeper-prime-darts-isolation-v1/index.html"))) fail("Isolation page is missing");
if (sha(path.join(publicDir, "catalog.json")) !== register.catalog.sha256) fail("Catalogue hash mismatch");
if (sha(path.join(publicDir, "index.html")) !== register.page.sha256) fail("Page hash mismatch");
if (!fs.readFileSync(path.join(publicDir, "index.html"), "utf8").includes("Nine current authorities, candidates or inspection views")) fail("Workbench V4 copy is stale");
for (const entry of register.publishedAssets) {
  const source = path.join(root, entry.source);
  if (!fs.existsSync(source) || sha(source) !== entry.sourceSha256) fail(`Published provenance mismatch ${entry.source}`);
}
console.log("Prime Context Workbench V4 verified: 9 choices including the reversible Darts cell-isolation corrective draft.");

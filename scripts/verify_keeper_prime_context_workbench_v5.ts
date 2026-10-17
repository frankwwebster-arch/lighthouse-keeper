import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const publicDir = path.join(root, "public/keeper-review/keeper-prime-context-workbench-v5");
const register = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v5/batch-register.json"), "utf8"));
const catalog = JSON.parse(fs.readFileSync(path.join(publicDir, "catalog.json"), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };

if (catalog.schema !== "lighthouse-keeper/context-workbench@5" || catalog.sequences.length !== 9) fail("Wrong Workbench V5 identity or choice count");
const darts = catalog.sequences.find((entry: any) => entry.id === "darts-v4");
if (!darts || darts.url !== "/keeper-review/keeper-prime-darts-context-v4/" || darts.kind !== "external") fail("Playable Darts V4 choice missing");
if (catalog.sequences.some((entry: any) => entry.id === "darts-v3")) fail("Obsolete playable Darts V3 choice remains");
if (!catalog.sequences.some((entry: any) => entry.id === "darts-cell-isolation-v1") || !catalog.sequences.some((entry: any) => entry.id === "darts-v2-strip-inspector")) fail("Darts diagnostic views were lost");
if (!fs.existsSync(path.join(root, "public/keeper-review/keeper-prime-darts-context-v4/index.html"))) fail("Darts V4 page missing");
if (sha(path.join(publicDir, "catalog.json")) !== register.catalog.sha256 || sha(path.join(publicDir, "index.html")) !== register.page.sha256) fail("Workbench V5 page/catalog hashes mismatch");
if (!fs.readFileSync(path.join(publicDir, "index.html"), "utf8").includes("restores the complete playable Darts route")) fail("Workbench V5 copy does not explain restored playback");
for (const entry of register.publishedAssets) {
  const file = path.join(root, entry.source);
  if (!fs.existsSync(file) || sha(file) !== entry.sourceSha256) fail(`Published provenance mismatch ${entry.source}`);
}
console.log("Prime Context Workbench V5 verified: 9 choices, complete playable Darts V4 restored, isolation comparison and V2 strip inspector retained.");

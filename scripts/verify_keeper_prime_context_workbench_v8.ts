import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const publicDir = path.join(root, "public/keeper-review/keeper-prime-context-workbench-v8");
const register = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v8/batch-register.json"), "utf8"));
const catalog = JSON.parse(fs.readFileSync(path.join(publicDir, "catalog.json"), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };

if (catalog.schema !== "lighthouse-keeper/context-workbench@8" || catalog.sequences.length !== 10) fail("Wrong Workbench V8 identity/count");
if (catalog.inventoryUrl !== "/keeper-review/keeper-prime-context-workbench-v7/inventory.json" || fs.existsSync(path.join(publicDir, "inventory.json"))) fail("Workbench V8 duplicated the unchanged inventory");
const darts = catalog.sequences.find((entry: any) => entry.id === "darts-v7");
if (!darts || darts.url !== "/keeper-review/keeper-prime-darts-context-v7/" || darts.kind !== "external") fail("Darts V7 choice missing");
if (catalog.sequences.some((entry: any) => entry.id === "darts-v6")) fail("Superseded playable Darts V6 choice remains");
for (const id of ["darts-prime-redraw-v2", "darts-cell-isolation-v1", "darts-v2-strip-inspector"]) if (!catalog.sequences.some((entry: any) => entry.id === id)) fail(`${id} diagnostic was lost`);
for (const field of ["catalog", "page", "app"]) if (sha(path.join(root, register[field].file)) !== register[field].sha256) fail(`Workbench V8 ${field} hash drift`);
if (!fs.readFileSync(path.join(publicDir, "index.html"), "utf8").includes("no backward anchor jump")) fail("Workbench V8 copy missing seam correction");
console.log("Prime Context Workbench V8 verified: ten choices, corrected Darts V7 selected, and all prior diagnostics retained.");

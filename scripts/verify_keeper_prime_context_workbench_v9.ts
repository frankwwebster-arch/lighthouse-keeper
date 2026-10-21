import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const publicDir = path.join(root, "public/keeper-review/keeper-prime-context-workbench-v9");
const register = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v9/batch-register.json"), "utf8"));
const catalog = JSON.parse(fs.readFileSync(path.join(publicDir, "catalog.json"), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };
const physicallyExists = (file: string): boolean => {
  try { fs.lstatSync(file); return true; }
  catch (error: any) { if (error.code === "ENOENT") return false; throw error; }
};

if (catalog.schema !== "lighthouse-keeper/context-workbench@9" || catalog.sequences.length !== 10) fail("Wrong Workbench V9 identity/count");
const darts = catalog.sequences.find((entry: any) => entry.id === "darts-v8");
if (!darts || darts.url !== "/keeper-review/keeper-prime-darts-context-v8/" || darts.kind !== "external") fail("Darts V8 choice missing");
if (catalog.sequences.some((entry: any) => entry.id === "darts-v7")) fail("Superseded playable Darts V7 choice remains");
for (const id of ["darts-prime-redraw-v2", "darts-cell-isolation-v1", "darts-v2-strip-inspector"]) if (!catalog.sequences.some((entry: any) => entry.id === id)) fail(`${id} diagnostic was lost`);
if (catalog.inventoryUrl !== "/keeper-review/keeper-prime-context-workbench-v7/inventory.json" || physicallyExists(path.join(publicDir, "inventory.json"))) fail("Workbench V9 duplicated the unchanged inventory");
for (const field of ["catalog", "page", "app"]) if (sha(path.join(root, register[field].file)) !== register[field].sha256) fail(`Workbench V9 ${field} hash drift`);
if (!fs.readFileSync(path.join(publicDir, "index.html"), "utf8").includes("one hand-matched dart asset")) fail("Workbench V9 copy missing prop correction");
console.log("Prime Context Workbench V9 verified: ten choices, harmonised Darts V8 selected, unchanged inventory reused and all prior diagnostics retained.");

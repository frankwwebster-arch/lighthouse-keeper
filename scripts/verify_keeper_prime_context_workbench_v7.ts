import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const publicDir = path.join(root, "public/keeper-review/keeper-prime-context-workbench-v7");
const register = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v7/batch-register.json"), "utf8"));
const catalog = JSON.parse(fs.readFileSync(path.join(publicDir, "catalog.json"), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };

if (catalog.schema !== "lighthouse-keeper/context-workbench@7" || catalog.sequences.length !== 10) fail("Wrong Workbench V7 identity/count");
const darts = catalog.sequences.find((entry: any) => entry.id === "darts-v6");
const redraw = catalog.sequences.find((entry: any) => entry.id === "darts-prime-redraw-v2");
if (!darts || darts.url !== "/keeper-review/keeper-prime-darts-context-v6/" || darts.kind !== "external") fail("Darts V6 choice missing");
if (!redraw || redraw.url !== "/keeper-review/keeper-prime-darts-redraw-v2/" || redraw.kind !== "external") fail("Redraw V2 choice missing");
if (catalog.sequences.some((entry: any) => entry.id === "darts-v5" || entry.id === "darts-prime-redraw-v1")) fail("Superseded Darts choices remain");
for (const id of ["darts-cell-isolation-v1", "darts-v2-strip-inspector"]) if (!catalog.sequences.some((entry: any) => entry.id === id)) fail(`${id} diagnostic was lost`);
if (sha(path.join(publicDir, "catalog.json")) !== register.catalog.sha256 || sha(path.join(publicDir, "index.html")) !== register.page.sha256) fail("Workbench V7 hashes drifted");
if (!fs.readFileSync(path.join(publicDir, "index.html"), "utf8").includes("complete Prime-derived V2 redraw")) fail("Workbench V7 copy missing redraw decision");
console.log("Prime Context Workbench V7 verified: ten choices, complete-context Darts V6 and registered redraw V2 added without losing prior authorities or diagnostics.");

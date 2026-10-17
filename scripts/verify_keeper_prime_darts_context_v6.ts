import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const register = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v6/batch-register.json"), "utf8"));
const data = JSON.parse(fs.readFileSync(path.join(root, register.candidate.routeData), "utf8"));
const predecessor = JSON.parse(fs.readFileSync(path.join(root, register.predecessor.route), "utf8"));
const redraw = JSON.parse(fs.readFileSync(path.join(root, register.primeRedrawCore.register), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };
const mechanics = (frame: any) => JSON.stringify({ ...frame, src: "", label: "" });

if (register.batchId !== "keeper-prime-darts-context-2026-10-17-v6" || data.schema !== "lighthouse-keeper/darts-context@6") fail("Wrong Darts Context V6 identity");
if (data.route.length !== 213 || !data.route.every((frame: any, i: number) => mechanics(frame) === mechanics(predecessor.route[i]))) fail("V5 route mechanics changed");
const coreHashes = new Map(redraw.coreSlots.map((slot: any) => [slot.frame, slot.sha256]));
const publishedHashByUrl = new Map(register.publishedAssets.map((entry: any) => [entry.url, entry.sourceSha256]));
const core = data.route.filter((frame: any) => frame.coreFrame);
if (core.length !== 84 || !core.every((frame: any) => publishedHashByUrl.get(frame.src) === coreHashes.get(frame.coreFrame))) fail("Not every throw-core occurrence uses exact redraw V2 bytes");
if (register.checks.inheritedActorCorePixelsRetained !== false || !Object.entries(register.checks).every(([key, value]) => key === "inheritedActorCorePixelsRetained" ? value === false : Boolean(value))) fail("Recorded V6 checks failed");
for (const field of ["routeData", "page", "app"]) if (sha(path.join(root, register.candidate[field])) !== register.candidate[`${field}Sha256`]) fail(`V6 ${field} hash drift`);
const page = fs.readFileSync(path.join(root, register.candidate.page), "utf8");
const app = fs.readFileSync(path.join(root, register.candidate.app), "utf8");
for (const required of ["Whole-bank redraw rule applied", "Prime throughout", "registered 14-slot Prime throw core V2", "Skip this occurrence"]) if (!page.includes(required)) fail(`V6 page missing ${required}`);
for (const required of ["Promise.all", "makeDart", "keeper-prime-darts-context-v6-skip-plan"]) if (!app.includes(required)) fail(`V6 app missing ${required}`);
if (register.approvalBoundary.v2CoreApproved || register.approvalBoundary.contextualV6Approved || register.approvalBoundary.finalChanged || register.approvalBoundary.runtimeChanged || register.approvalBoundary.productionChanged || register.approvalBoundary.promotionAllowed) fail("Context V6 approval boundary breached");
console.log("Keeper Prime Darts Context V6 verified: all 84 core occurrences use redraw V2 while all 213 route mechanics remain exact; nothing promoted.");

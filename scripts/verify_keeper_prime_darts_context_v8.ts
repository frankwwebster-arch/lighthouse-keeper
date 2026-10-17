import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { PNG } from "pngjs";

const root = path.resolve(import.meta.dirname, "..");
const pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v8");
const register = JSON.parse(fs.readFileSync(path.join(pack, "batch-register.json"), "utf8"));
const data = JSON.parse(fs.readFileSync(path.join(root, register.candidate.routeData), "utf8"));
const predecessor = JSON.parse(fs.readFileSync(path.join(root, register.predecessor.route), "utf8"));
const sha = (file: string) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const fail = (message: string): never => { throw new Error(message); };
const edgeAlpha = (file: string) => {
  const png = PNG.sync.read(fs.readFileSync(file)); let edges = 0;
  for (let x = 0; x < png.width; x++) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) edges++;
  for (let y = 1; y < png.height - 1; y++) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) edges++;
  return { png, edges };
};

if (data.schema !== "lighthouse-keeper/darts-context@8" || data.route.length !== 181) fail("Wrong Darts Context V8 identity/count");
const flights = data.route.filter((frame: any) => frame.flyingDart);
if (flights.length !== 30) fail("Wrong flight-frame count");
for (const flight of flights) {
  const dart = flight.flyingDart;
  const tail = dart.startXLp + (dart.targetXLp - dart.startXLp) * dart.progress;
  if (tail + data.propGeometry.dartLengthLp > data.propGeometry.boardFaceXLp) fail("Dart tip passes board face");
  if (dart.startYLp !== 25.1 || !data.propGeometry.impactCentresYLp.includes(dart.targetYLp)) fail("Flight y interpolation drift");
}
const groups = [];
for (let i = 0; i < flights.length; i += 5) groups.push(flights.slice(i, i + 5));
if (groups.length !== 6 || groups.some((group: any[]) => group.at(-1).flyingDart.progress !== 1 || group.at(-1).flyingDart.targetXLp !== data.propGeometry.embeddedTailXLp)) fail("Final flight does not equal embedded position");

for (let i = 0; i < data.route.length; i++) {
  const before = { ...predecessor.route[i], src: "", flyingDart: null };
  const after = { ...data.route[i], src: "", flyingDart: null };
  if (JSON.stringify(before) !== JSON.stringify(after)) fail(`Keeper/timing/state changed at frame ${i + 1}`);
}
for (const prop of [register.propArt.dart, register.propArt.board]) {
  const file = path.join(root, prop.source);
  if (sha(file) !== prop.sourceSha256) fail(`${prop.source} hash drift`);
  const { png, edges } = edgeAlpha(file);
  if (png.colorType !== 6 || edges !== 0) fail(`${prop.source} lacks transparent safety gutter`);
}
const dartPng = PNG.sync.read(fs.readFileSync(path.join(root, register.propArt.dart.source)));
const boardPng = PNG.sync.read(fs.readFileSync(path.join(root, register.propArt.board.source)));
if (dartPng.width !== 620 || dartPng.height !== 160 || boardPng.width !== 320 || boardPng.height !== 856) fail("Prop source geometry drift");
const app = fs.readFileSync(path.join(root, register.candidate.app), "utf8");
for (const required of [register.propArt.dart.url, register.propArt.board.url, "startYLp", "targetYLp", "7.25", "160.75"]) if (!app.includes(required)) fail(`V8 app missing ${required}`);
if (app.includes("document.createElement('i');dart.className='dart")) fail("Simplified CSS dart remains");
for (const field of ["routeData", "page", "app"]) if (sha(path.join(root, register.candidate[field])) !== register.candidate[`${field}Sha256`]) fail(`V8 ${field} hash drift`);
if (!Object.values(register.checks).every(Boolean)) fail("Recorded V8 checks failed");
if (register.approvalBoundary.contextualV8Approved || register.approvalBoundary.finalChanged || register.approvalBoundary.runtimeChanged || register.approvalBoundary.productionChanged || register.approvalBoundary.promotionAllowed) fail("Context V8 approval boundary breached");
console.log("Keeper Prime Darts Context V8 verified: one gutter-safe hand-matched dart drives all 30 airborne frames and every impact; six flights finish exactly at the board face; segmented acute-angle board installed; all 181 Keeper/timing/state frames unchanged.");

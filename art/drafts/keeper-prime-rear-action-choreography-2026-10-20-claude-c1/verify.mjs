#!/usr/bin/env node
// Check the C1 draft against Codex's model-test brief. Run: node verify.mjs
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { FRAMES, FPS, QUIET_START, ORIGIN, measureTimeline } from './metrics.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../../..');
const PACK_REPO = 'art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v2/claude-code-model-test-pack';
const sha256 = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));

const failures = [];
let checks = 0;
function check(ok, message) { checks++; if (!ok) failures.push(message); }

// 1. Nothing outside this directory changed: the pack, V1, V2, runtime, Final, Kitchen, deploy config.
const protectedPaths = [
  'art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v2',
  'art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v1',
  'public', 'src', 'data', 'review-archive', 'scripts', 'package.json', 'vercel.json', 'next.config.js', 'next.config.mjs',
];
const dirty = execFileSync('git', ['status', '--porcelain', '--', ...protectedPaths], { cwd: ROOT, encoding: 'utf8' }).trim();
check(dirty === '', `Protected paths changed:\n${dirty}`);
const manifest = readJson(path.join(HERE, 'pack/asset-manifest.json'));
for (const asset of manifest.assets) {
  const file = path.join(ROOT, asset.file);
  check(fs.existsSync(file) && sha256(file) === asset.sha256, `Pack asset changed: ${asset.file}`);
}

// 2. Only pack pictures, and every Prime body byte for byte.
const catalogue = readJson(path.join(HERE, 'catalogue.json'));
const v2 = readJson(path.join(HERE, 'pack/metadata/v2-catalogue.json'));
const packSha = new Map(manifest.assets.map((a) => ['pack/' + path.posix.relative(PACK_REPO, a.file), a.sha256]));
check(catalogue.sequence.length === v2.sequence.length, 'Sequence length differs from the approved Prime sequence');
catalogue.sequence.forEach((frame, i) => {
  const expected = v2.sequence[i].authoritySha256 || v2.sequence[i].candidateSha256;
  check(frame.src.startsWith('pack/assets/body/') && packSha.get(frame.src) === expected && sha256(path.join(HERE, frame.src)) === expected,
    `Body frame ${i} is not the byte-exact approved Prime image`);
  check(frame.durationMs === v2.sequence[i].durationMs && frame.x === v2.sequence[i].x, `Body frame ${i} timing or position changed`);
});
for (const [id, c] of Object.entries(catalogue.components)) {
  check(packSha.has(c.src) && sha256(path.join(HERE, c.src)) === c.sha256 && packSha.get(c.src) === c.sha256, `Component ${id} is not a pack asset`);
}

// 3–9. Each story, both motion modes.
const visibleKey = (frame) => JSON.stringify(frame.objects.filter((o) => o.opacity > 0).map(({ instance, x, y, scale, rotation, opacity }) => [instance, x, y, scale, rotation, opacity]));
const report = {};
for (const [key, story] of Object.entries(catalogue.stories)) {
  const full = story.timelines.bubble.full;
  const reduced = story.timelines.bubble.reduced;
  for (const [mode, frames] of [['full', full], ['reduced', reduced]]) {
    const where = `${key}/${mode}`;
    check(frames.length === FRAMES, `${where}: ${frames.length} frames, expected ${FRAMES}`);
    frames.forEach((frame, f) => {
      check(frame.timeMs === (f * 1000) / FPS, `${where} f${f}: wrong time`);
      check(frame.quietTail === f >= QUIET_START, `${where} f${f}: quiet-tail flag wrong`);
      const roles = frame.objects.map((o) => o.role).sort().join(',');
      check(roles === 'hero,resolved,support,support,support', `${where} f${f}: layers are ${roles}`);
      check(frame.symbols.every((s) => ['momentum', 'interaction', 'punctuation'].includes(s.role)), `${where} f${f}: unknown symbol role`);
      check(frame.symbols.every((s) => s.component.startsWith('symbol-')) && frame.objects.every((o) => !o.component.startsWith('symbol-')), `${where} f${f}: symbol and object layers mixed`);
      check(frame.treatment && frame.treatment.trail.length === 3, `${where} f${f}: treatment marks missing`);
    });
    const m = measureTimeline(frames, catalogue.components, story.contacts);
    check(m.tailStatic && m.tailSymbolsSilent, `${where}: quiet tail is not still and silent`);
    check(m.objectFramesOutsideBubble === 0, `${where}: ${m.objectFramesOutsideBubble} picture-frames leave the bubble`);
    check(m.maxUndeclaredOverlap <= 0.1, `${where}: pictures cover each other by ${Math.round(m.maxUndeclaredOverlap * 100)}% outside a touch`);
    report[where] = m;
  }
  check(visibleKey(full[FRAMES - 1]) === visibleKey(reduced[FRAMES - 1]), `${key}: reduced motion ends on a different picture`);
  check(story.sfx.every((cue) => cue.frame < QUIET_START), `${key}: a sound is declared inside the quiet tail`);

  // Head-to-bubble origin and mobile objects (full motion).
  const mf = report[`${key}/full`];
  for (const id of ['hero', ...Object.keys(story.supports)]) {
    check(mf.firstVisibleDistanceFromOrigin[id] <= 20, `${key}: ${id} is not born at the head connector (${mf.firstVisibleDistanceFromOrigin[id]}px away)`);
  }
  for (const id of Object.keys(story.supports)) check(mf.pathLength[id] >= 150, `${key}: ${id} barely moves (${mf.pathLength[id]}px)`);
  check(mf.symbolInstancesUsed >= 15, `${key}: only ${mf.symbolInstancesUsed} separate ticks and stars`);
  check((mf.symbolInstancesByComponent['symbol-motion-ticks'] || 0) >= 4, `${key}: too few speed ticks`);
  check((mf.symbolInstancesByComponent['symbol-impact-star'] || 0) >= 5, `${key}: too few stars`);
  check(full.slice(0, 3).some((f, i) => f.treatment.trail[0] > 0 && f.treatment.bubbleScale < 1), `${key}: the bubble does not grow from the head`);

  // Reduced motion: nothing travels, spins or scales while visible; no speed ticks.
  for (let f = 1; f < FRAMES; f++) {
    for (const o of reduced[f].objects) {
      const p = reduced[f - 1].objects.find((x) => x.instance === o.instance);
      if (Math.min(o.opacity, p.opacity) > 0.05) {
        check(o.x === p.x && o.y === p.y && o.rotation === p.rotation && o.scale === p.scale, `${key}/reduced f${f}: ${o.instance} moves while visible`);
      }
    }
    check(reduced[f].symbols.every((s) => s.role !== 'momentum' || s.opacity === 0), `${key}/reduced f${f}: speed ticks shown`);
    check(reduced[f].treatment.bubbleScale === 1, `${key}/reduced f${f}: the bubble scales`);
  }
}

const rows = Object.entries(report).map(([k, m]) => `${k.padEnd(24)} covering outside touches ${String(Math.round(m.maxUndeclaredOverlap * 100)).padStart(2)}% · ticks/stars ${m.symbolInstancesUsed} · max on one frame ${m.maxSymbolsOnOneFrame}`);
console.log(rows.join('\n'));
if (failures.length) {
  console.error(`\n${failures.length} of ${checks} checks failed:\n- ${failures.join('\n- ')}`);
  process.exit(1);
}
console.log(`\nAll ${checks} checks passed. Origin ${ORIGIN.x},${ORIGIN.y}; quiet tail ${QUIET_START}–${FRAMES - 1}.`);

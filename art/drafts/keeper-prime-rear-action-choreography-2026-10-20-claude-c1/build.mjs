#!/usr/bin/env node
// Build Claude's C1 bubble choreography from Codex's model-test pack.
// The pack (reached through the `pack` link) is read only; every output is
// written next to this script. Run: node build.mjs
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { FRAMES, FPS, QUIET_START, ORIGIN, OBJECT_BOX, measureTimeline } from './metrics.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../../..');
const PACK = path.join(HERE, 'pack');
const PACK_REPO = 'art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v2/claude-code-model-test-pack';
const SET = 'keeper-prime-rear-action-choreography-claude-c1';
const require = createRequire(path.join(ROOT, 'package.json'));
const { PNG } = require('pngjs');

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const sha256 = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const local = (repoFile) => 'pack/' + path.posix.relative(PACK_REPO, repoFile);
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
const r2 = (v) => Math.round(v * 100) / 100;
const r3 = (v) => Math.round(v * 1000) / 1000;

const manifest = readJson(path.join(PACK, 'asset-manifest.json'));
const v2 = readJson(path.join(PACK, 'metadata/v2-catalogue.json'));

// ---------------------------------------------------------------- assets
function alphaBox(file) {
  const png = PNG.sync.read(fs.readFileSync(file));
  let x0 = png.width, y0 = png.height, x1 = -1, y1 = -1;
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) {
    if (png.data[(y * png.width + x) * 4 + 3] > 8) {
      x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y);
    }
  }
  return [x0, y0, x1, y1];
}

const components = {};
const bodyByFrame = {};
for (const asset of manifest.assets) {
  const file = path.join(PACK, path.posix.relative(PACK_REPO, asset.file));
  const actual = sha256(file);
  if (actual !== asset.sha256) throw new Error(`Pack asset changed: ${asset.file}`);
  if (asset.kind === 'approved-prime-body') {
    for (const frame of asset.usedBySequenceFrames) bodyByFrame[frame] = { src: local(asset.file), sha256: actual };
  } else if (asset.kind === 'activity-object' || asset.kind === 'comic-symbol') {
    components[asset.id] = { kind: asset.kind, family: asset.family, src: local(asset.file), sha256: actual, bbox: alphaBox(file) };
  }
}

const sequence = v2.sequence.map((frame, index) => {
  const body = bodyByFrame[index];
  const expected = frame.authoritySha256 || frame.candidateSha256;
  if (!body || body.sha256 !== expected) throw new Error(`No byte-exact Prime body for sequence frame ${index}`);
  return { src: body.src, sha256: body.sha256, phase: frame.phase, pose: frame.pose, x: frame.x, dx: frame.dx, durationMs: frame.durationMs };
});

// ---------------------------------------------------------------- motion
const EASE = {
  lin: (t) => t,
  inOut: (t) => (t < 0.5 ? 4 * t ** 3 : 1 - (-2 * t + 2) ** 3 / 2),
  out: (t) => 1 - (1 - t) ** 3,
  in: (t) => t ** 3,
  back: (t) => 1 + 2.70158 * (t - 1) ** 3 + 1.70158 * (t - 1) ** 2,
  soft: (t) => 1 + 1.8 * (t - 1) ** 3 + 0.8 * (t - 1) ** 2,
};

// rows: [frame, changes, ease, bend]; unspecified values carry over. `bend`
// offsets the midpoint of a segment to make a curved (quadratic) path.
function keys(rows) {
  let prev = { x: 0, y: 0, s: 1, r: 0, o: 1 };
  return rows.map(([f, change = {}, ease = 'inOut', bend = null]) => {
    prev = { ...prev, ...change };
    return { f, ...prev, ease, bend };
  });
}

function sample(track, f) {
  if (f <= track[0].f) return { ...track[0] };
  for (let i = 0; i < track.length - 1; i++) {
    const a = track[i], b = track[i + 1];
    if (f >= a.f && f < b.f) {
      const t = (f - a.f) / (b.f - a.f);
      const e = EASE[b.ease](t);
      let x = a.x + (b.x - a.x) * e, y = a.y + (b.y - a.y) * e;
      if (b.bend) {
        const cx = (a.x + b.x) / 2 + b.bend[0], cy = (a.y + b.y) / 2 + b.bend[1];
        x = (1 - e) ** 2 * a.x + 2 * (1 - e) * e * cx + e * e * b.x;
        y = (1 - e) ** 2 * a.y + 2 * (1 - e) * e * cy + e * e * b.y;
      }
      return { x, y, s: a.s + (b.s - a.s) * e, r: a.r + (b.r - a.r) * e, o: a.o + (b.o - a.o) * t };
    }
  }
  return { ...track[track.length - 1] };
}

// ---------------------------------------------------------------- staging
const O = ORIGIN;
const HERO = { x: 0, y: 16, s: 0.7 };
const HERO_END = { x: -44, y: 16, s: 0.62 };
const RESULT_END = { x: 48, y: 6, s: 0.64 };
const SUP = 0.42;
const LANE = { A: { x: -84, y: -26 }, B: { x: 84, y: -28 }, C: { x: 86, y: 34 } };
const BIRTH = { A: [4, 8], B: [6, 10], C: [8, 12] };
const BIRTH_BEND = { A: [-30, 10], B: [30, 10], C: [10, 22] };
const ZS = { A: 5, B: 6, C: 7 };

const heroRows = [
  [0, { x: O.x, y: O.y, s: 0.1, r: 0, o: 0 }],
  [1, { y: 72, s: 0.18, o: 1 }, 'lin'],
  [5, { x: HERO.x, y: HERO.y, s: HERO.s }, 'back'],
  [31, {}],
  [32, { y: 18, s: 0.74 }, 'out'],
  [35, { x: HERO_END.x, y: HERO_END.y, s: HERO_END.s }, 'back', [0, -14]],
];
const resultRows = [
  [0, { x: 0, y: 16, s: 0.12, r: 0, o: 0 }],
  [31, {}],
  [32, { x: 4, y: 8, s: 0.34, o: 1 }, 'lin'],
  [35, { x: RESULT_END.x, y: RESULT_END.y, s: RESULT_END.s }, 'back', [0, -22]],
];
const birthRows = (lane) => {
  const [f0, f1] = BIRTH[lane];
  const at = LANE[lane];
  return [
    [0, { x: O.x, y: O.y, s: 0.1, r: 0, o: 0 }],
    [f0, {}],
    [f0 + 1, { y: O.y - 4, s: 0.16, o: 1 }, 'lin'],
    [f1, { x: at.x, y: at.y, s: SUP }, 'soft', BIRTH_BEND[lane]],
  ];
};
const fold = (f0, f1, to = { x: 0, y: 12 }, bend = null, extra = {}) => [[f0, {}], [f1, { ...to, s: 0.1, o: 0, ...extra }, 'in', bend]];
const home = (lane) => ({ x: LANE[lane].x, y: LANE[lane].y });

// Each story: hero/result, three supports in lanes A, B and C, the frames
// where touching is the point (declared contacts) and the punctuation.
const STORIES = {
  'garden-bbq': {
    beats: ['the grill rises out of his head', 'charcoal tips in and the heat starts', 'sausages, then hot dogs, flip onto the bars', 'everything cooks down into burgers'],
    sfx: { 'charcoal-rattle': 16, 'bbq-sizzle': 22, 'food-ready': 32 },
    supports: {
      charcoal: { lane: 'A', rows: [[13, {}], [14, { x: -84, y: -30, r: -8 }, 'out'], [16, { x: -34, y: -20, r: -40 }, 'inOut', [0, -26]], [17, { x: -31, y: -17, r: -46 }, 'lin'], [18, { x: -35, y: -20, r: -36 }, 'lin'], [20, { ...home('A'), r: 0 }, 'inOut', [0, -20]], ...fold(29, 32, { x: -2, y: 12 }, [-10, -20], { r: -80 })],
        idle: [[8, 13], [20, 29]], contact: { x: -34, y: -20, r: -40 }, reduced: { go: 14, at: 16, leave: 18, end: [29, 31] } },
      sausages: { lane: 'B', rows: [[18, {}], [19, { x: 84, y: -32 }, 'out'], [22, { x: 20, y: -18, r: 180 }, 'inOut', [0, -24]], [23, { x: 18, y: -16, r: 186 }, 'lin'], [26, { ...home('B'), r: 360 }, 'inOut', [0, -12]], ...fold(29, 32, { x: 2, y: 12 }, [10, -20], { r: 420 })],
        idle: [[10, 18], [26, 29]], contact: { x: 20, y: -18, r: 180 }, reduced: { go: 19, at: 22, leave: 24, end: [29, 31] } },
      hotdogs: { lane: 'C', rows: [[23, {}], [24, { x: 90, y: 38 }, 'out'], [27, { x: 26, y: -6, r: -180 }, 'inOut', [-14, -10]], [28, { x: 28, y: -4, r: -186 }, 'lin'], [30, { x: 24, y: -2, r: -180 }, 'lin'], ...fold(30, 32, { x: 2, y: 14 }, null, { r: -200 })],
        idle: [[12, 23]], contact: { x: 26, y: -6, r: -180 }, reduced: { go: 24, at: 27, leave: null, end: [30, 32] } },
    },
    contacts: [['charcoal', 'hero', 15, 19], ['sausages', 'hero', 21, 24], ['hotdogs', 'hero', 26, 32]],
    punctuation: [
      { id: 'contact-charcoal', c: 'symbol-impact-star', role: 'interaction', anchor: 'charcoal', with: 'hero', f: 16, x: -44, y: -26, s: 0.34, spin: 30 },
      { id: 'contact-sausages', c: 'symbol-impact-star', role: 'interaction', anchor: 'sausages', with: 'hero', f: 22, x: 38, y: -24, s: 0.34, spin: -30 },
      { id: 'contact-hotdogs', c: 'symbol-impact-star', role: 'interaction', anchor: 'hotdogs', with: 'hero', f: 27, x: 44, y: -10, s: 0.34, spin: 30 },
      { id: 'sizzle-sausages', c: 'symbol-sizzle-spark', role: 'punctuation', anchor: 'sausages', f: 22, x: 14, y: -38, s: 0.3, dir: -90, dur: 3 },
      { id: 'sizzle-hotdogs', c: 'symbol-sizzle-spark', role: 'punctuation', anchor: 'hotdogs', f: 27, x: 24, y: -26, s: 0.3, dir: -80, dur: 3 },
      { id: 'heat-left', c: 'symbol-heat-curls', role: 'punctuation', anchor: 'hero', loop: [17, 31], x: -12, y: -18, rise: 30, period: 6, s: 0.3 },
      { id: 'heat-right', c: 'symbol-heat-curls', role: 'punctuation', anchor: 'hero', loop: [19, 31], x: 14, y: -20, rise: 30, period: 6, s: 0.26 },
    ],
  },
  'make-sandwich': {
    beats: ['the bread rises out of his head', 'ham drops on', 'lettuce, then tomato, stack up', 'the stack presses into a finished sandwich'],
    sfx: { 'bread-set-down': 5, 'ingredients-stack': 21, 'sandwich-finished': 32 },
    supports: {
      ham: { lane: 'A', rows: [[13, {}], [14, { x: -84, y: -32 }, 'out'], [16, { x: 0, y: 4 }, 'inOut', [-6, -36]], [17, { y: 7 }, 'lin'], [18, { y: 4 }], [29, {}], [30, { y: 9 }, 'out'], ...fold(30, 32, { x: 2, y: 12 })],
        idle: [[8, 13]], contact: { x: 0, y: 4, r: 0 }, reduced: { go: 14, at: 16, leave: null, end: [30, 32] } },
      lettuce: { lane: 'B', rows: [[18, {}], [19, { x: 84, y: -34 }, 'out'], [21, { x: 2, y: -4 }, 'inOut', [6, -36]], [22, { y: -1 }, 'lin'], [23, { y: -4 }], [29, {}], [30, { y: 4 }, 'out'], ...fold(30, 32, { x: 2, y: 12 })],
        idle: [[10, 18]], contact: { x: 2, y: -4, r: 0 }, reduced: { go: 19, at: 21, leave: null, end: [30, 32] } },
      tomato: { lane: 'C', rows: [[23, {}], [24, { x: 92, y: 42 }, 'out'], [26, { x: -2, y: -12, s: 0.32 }, 'inOut', [10, -48]], [27, { y: -9 }, 'lin'], [28, { y: -12 }], [29, {}], [30, { y: -2 }, 'out'], ...fold(30, 32, { x: 2, y: 12 })],
        idle: [[12, 23]], contact: { x: -2, y: -12, r: 0, s: 0.32 }, reduced: { go: 24, at: 26, leave: null, end: [30, 32] } },
    },
    contacts: [['ham', 'hero', 15, 32], ['lettuce', 'hero', 20, 32], ['tomato', 'hero', 25, 32], ['ham', 'lettuce', 20, 32], ['ham', 'tomato', 25, 32], ['lettuce', 'tomato', 25, 32]],
    punctuation: [
      { id: 'contact-ham', c: 'symbol-impact-star', role: 'interaction', anchor: 'ham', with: 'hero', f: 16, x: -40, y: -10, s: 0.32, spin: 30 },
      { id: 'contact-lettuce', c: 'symbol-impact-star', role: 'interaction', anchor: 'lettuce', with: 'ham', f: 21, x: 42, y: -16, s: 0.32, spin: -30 },
      { id: 'contact-tomato', c: 'symbol-impact-star', role: 'interaction', anchor: 'tomato', with: 'lettuce', f: 26, x: -38, y: -26, s: 0.32, spin: 30 },
      { id: 'press-left', c: 'symbol-motion-ticks', role: 'punctuation', anchor: 'hero', f: 29, x: -40, y: -22, s: 0.26, dir: 90, dur: 3 },
      { id: 'press-right', c: 'symbol-motion-ticks', role: 'punctuation', anchor: 'hero', f: 29, x: 40, y: -22, s: 0.26, dir: 90, dur: 3 },
      { id: 'press-star', c: 'symbol-sizzle-spark', role: 'punctuation', anchor: 'hero', f: 30, x: 0, y: -40, s: 0.28, dir: -90, dur: 2 },
    ],
  },
  'washing-up': {
    beats: ['the dirty plate rises out of his head', 'washing-up liquid squeezes, bubbles rise', 'water drops in, the sponge scrubs', 'clean cutlery glints beside the plate'],
    sfx: { 'tap-water': 21, 'sponge-scrub': 25, 'clean-clink': 33 },
    supports: {
      liquid: { lane: 'A', rows: [[13, {}], [15, { x: -34, y: -34, r: -24 }, 'inOut', [0, -12]], [17, { x: -30, y: -30, r: -72 }, 'out'], [18, { x: -31, y: -31, r: -64 }, 'lin'], [20, { ...home('A'), r: 0 }, 'inOut', [-6, -14]], ...fold(29, 32, { x: O.x, y: O.y }, [-34, 12])],
        idle: [[8, 13], [20, 29]], contact: { x: -30, y: -30, r: -72 }, reduced: { go: 14, at: 16, leave: 18, end: [29, 31] } },
      droplets: { lane: 'B', rows: [[17, {}], [19, { x: 8, y: -36 }, 'inOut', [0, -24]], [21, { x: 6, y: 4, s: 0.32 }, 'in'], [23, { x: 6, y: 10, s: 0.18, o: 0 }, 'out']],
        idle: [[10, 17]], contact: { x: 6, y: 4, r: 0, s: 0.32 }, reduced: { go: 18, at: 20, leave: null, end: [22, 23] } },
      sponge: { lane: 'C', rows: [[22, {}], [24, { x: -18, y: 6, r: -8 }, 'inOut', [0, -30]], [25, { x: 20, r: 8 }], [26, { x: -20, y: 8, r: -8 }], [27, { x: 20, y: 6, r: 8 }], [28, { x: -14, y: 8, r: -6 }], [29, { x: 0, y: 4, r: 0 }], ...fold(29, 32, { x: O.x, y: O.y }, [30, 6])],
        idle: [[12, 22]], contact: { x: 0, y: 6, r: 0 }, reduced: { go: 23, at: 25, leave: null, end: [29, 31] } },
    },
    contacts: [['liquid', 'hero', 14, 19], ['droplets', 'hero', 20, 23], ['sponge', 'hero', 23, 30]],
    punctuation: [
      { id: 'contact-liquid', c: 'symbol-impact-star', role: 'interaction', anchor: 'liquid', with: 'hero', f: 17, x: -56, y: -50, s: 0.28, spin: 30 },
      { id: 'soap-left', c: 'symbol-soap-bubbles', role: 'punctuation', anchor: 'hero', loop: [17, 31], x: -14, y: -10, rise: 34, period: 7, s: 0.3 },
      { id: 'soap-right', c: 'symbol-soap-bubbles', role: 'punctuation', anchor: 'hero', loop: [19, 31], x: 20, y: -8, rise: 34, period: 7, s: 0.26 },
      { id: 'splash', c: 'symbol-water-droplets', role: 'interaction', anchor: 'droplets', with: 'hero', f: 21, x: 8, y: -20, s: 0.36, spin: 0, dur: 3 },
      { id: 'contact-droplets', c: 'symbol-impact-star', role: 'interaction', anchor: 'droplets', with: 'hero', f: 21, x: 40, y: -6, s: 0.28, spin: -30 },
      { id: 'contact-sponge', c: 'symbol-impact-star', role: 'interaction', anchor: 'sponge', with: 'hero', f: 24, x: -46, y: -4, s: 0.28, spin: 30 },
      { id: 'scrub-right', c: 'symbol-soap-bubbles', role: 'punctuation', anchor: 'sponge', f: 25, x: 46, y: -4, s: 0.28, spin: 0, dur: 2 },
      { id: 'scrub-left', c: 'symbol-soap-bubbles', role: 'punctuation', anchor: 'sponge', f: 27, x: -46, y: -2, s: 0.28, spin: 0, dur: 2 },
    ],
  },
  'general-repair': {
    beats: ['the toolbox rises out of his head', 'the hull patch is set against the job', 'the hammer strikes three times, the wrench spins tight', 'the tools pack away and a tied rope knot resolves'],
    sfx: { 'toolbox-open': 5, 'hammer-tap-wrench-click': 19, 'repair-secured': 32 },
    supports: {
      patch: { lane: 'A', rows: [[12, {}], [15, { x: -52, y: -8, r: -6 }, 'inOut', [-10, -18]], [16, { x: -50, y: -6, r: -4 }, 'lin'], [30, {}], ...fold(30, 32, { x: 0, y: 12 })],
        idle: [[8, 12]], contact: { x: -52, y: -8, r: -6 }, reduced: { go: 13, at: 15, leave: null, end: [30, 32] } },
      hammer: { lane: 'B', rows: [[15, {}], [18, { x: -10, y: -40, r: 34 }, 'inOut', [0, -20]], [19, { x: -14, y: -32, r: -22 }, 'in'], [20, { x: -10, y: -40, r: 34 }, 'out'], [21, { x: -14, y: -32, r: -22 }, 'in'], [22, { x: -10, y: -40, r: 34 }, 'out'], [23, { x: -14, y: -32, r: -22 }, 'in'], [24, { x: -10, y: -40, r: 10 }, 'out'], [26, { ...home('B'), r: 0 }, 'inOut', [0, -24]], ...fold(30, 32, { x: 0, y: 12 }, [0, -20])],
        idle: [[10, 15], [26, 30]], contact: { x: -14, y: -32, r: -22 }, reduced: { go: 16, at: 18, leave: 24, end: [30, 32] } },
      wrench: { lane: 'C', rows: [[25, {}], [27, { x: 50, y: 26, r: 0 }, 'inOut', [-4, 10]], [28, { r: -180 }, 'lin'], [29, { r: -360 }, 'lin'], [30, { r: -480 }, 'out'], ...fold(30, 32, { x: 0, y: 12 }, null, { r: -540 })],
        idle: [[12, 25]], contact: { x: 50, y: 26, r: 0 }, reduced: { go: 25, at: 27, leave: null, end: [30, 32] } },
    },
    contacts: [['patch', 'hero', 14, 32], ['hammer', 'patch', 17, 25], ['hammer', 'hero', 17, 25], ['wrench', 'hero', 26, 32]],
    punctuation: [
      { id: 'contact-patch', c: 'symbol-impact-star', role: 'interaction', anchor: 'patch', with: 'hero', f: 15, x: -70, y: -26, s: 0.3, spin: 30 },
      { id: 'strike-1', c: 'symbol-impact-star', role: 'interaction', anchor: 'hammer', with: 'patch', f: 19, x: -40, y: -20, s: 0.34, spin: 40 },
      { id: 'strike-2', c: 'symbol-impact-star', role: 'interaction', anchor: 'hammer', with: 'patch', f: 21, x: -36, y: -26, s: 0.3, spin: -40 },
      { id: 'strike-3', c: 'symbol-impact-star', role: 'interaction', anchor: 'hammer', with: 'patch', f: 23, x: -44, y: -14, s: 0.38, spin: 40 },
      { id: 'spin-upper', c: 'symbol-motion-ticks', role: 'momentum', anchor: 'wrench', orbit: { f: [27, 30], x: 50, y: 26, radius: 40, start: -90, sweep: -270 }, s: 0.24 },
      { id: 'spin-lower', c: 'symbol-motion-ticks', role: 'momentum', anchor: 'wrench', orbit: { f: [27, 30], x: 50, y: 26, radius: 40, start: 90, sweep: -270 }, s: 0.24 },
      { id: 'click', c: 'symbol-impact-star', role: 'interaction', anchor: 'wrench', with: 'hero', f: 30, x: 86, y: 4, s: 0.3, spin: -30 },
    ],
  },
};

// Shared punctuation: landings, the hero's arrival, the burst and the glints.
const SHARED_PUNCTUATION = [
  { id: 'arrive-hero', c: 'symbol-impact-star', role: 'punctuation', anchor: 'hero', f: 5, x: -38, y: -14, s: 0.24, spin: 30 },
  { id: 'land-A', c: 'symbol-sizzle-spark', role: 'punctuation', anchorLane: 'A', f: 8, x: -86, y: -54, s: 0.2, dir: -90, dur: 2 },
  { id: 'land-B', c: 'symbol-sizzle-spark', role: 'punctuation', anchorLane: 'B', f: 10, x: 86, y: -56, s: 0.2, dir: -90, dur: 2 },
  { id: 'land-C', c: 'symbol-sizzle-spark', role: 'punctuation', anchorLane: 'C', f: 12, x: 112, y: 22, s: 0.2, dir: -30, dur: 2 },
  { id: 'burst-star', c: 'symbol-impact-star', role: 'interaction', anchor: 'result', with: 'hero', f: 32, x: 6, y: -8, s: 0.46, spin: 40, dur: 3 },
  { id: 'burst-spark', c: 'symbol-sizzle-spark', role: 'punctuation', anchor: 'result', f: 32, x: 8, y: -34, s: 0.3, dir: -90, dur: 3 },
  { id: 'glint-1', c: 'symbol-impact-star', role: 'punctuation', anchor: 'result', f: 34, x: 74, y: -18, s: 0.22, spin: 45, dur: 2 },
  { id: 'glint-2', c: 'symbol-impact-star', role: 'punctuation', anchor: 'result', f: 35, x: 22, y: -22, s: 0.18, spin: -45, dur: 2 },
  { id: 'glint-3', c: 'symbol-impact-star', role: 'punctuation', anchor: 'result', f: 35, x: 70, y: 32, s: 0.2, spin: 45, dur: 2 },
];

const STORY_PHASE = (f) => (f >= QUIET_START ? 'quiet-tail' : f >= 32 ? 'resolution' : f >= 13 ? 'working' : 'beginning');

// ---------------------------------------------------------------- full mode
function bob(windows, f, phase) {
  let dy = 0, dr = 0;
  for (const [a, b] of windows) {
    if (f <= a || f >= b) continue;
    const env = Math.sin((Math.PI * (f - a)) / (b - a));
    dy += 2.6 * Math.sin((f - a) * 1.05 + phase) * env;
    dr += 3.2 * Math.sin((f - a) * 0.8 + phase) * env;
  }
  return { dy, dr };
}

function objectState(instance, component, role, z, s) {
  return { instance, component, role, x: r2(s.x), y: r2(s.y), scale: r3(s.s), rotation: r2(s.r), opacity: r3(clamp(s.o, 0, 1)), z };
}

function fullObjects(story) {
  const contactFrames = story.punctuation.filter((p) => p.role === 'interaction' && p.f).map((p) => p.f).concat([32]);
  const heroTrack = keys(heroRows), resultTrack = keys(resultRows);
  const supportTracks = Object.entries(story.supports).map(([id, sp], i) => ({ id, sp, i, track: keys([...birthRows(sp.lane), ...sp.rows]) }));
  const frames = [];
  for (let f = 0; f < FRAMES; f++) {
    const hero = sample(heroTrack, Math.min(f, QUIET_START));
    // The hero gives a small squash on every contact.
    const squash = contactFrames.reduce((m, c) => Math.max(m, Math.exp(-(((f - c) / 0.7) ** 2))), 0);
    if (f < 31) { hero.s *= 1 + 0.05 * squash; hero.y += 2 * squash; }
    const objects = [objectState('hero', story.hero, 'hero', 4, hero)];
    for (const { id, sp, i, track } of supportTracks) {
      const s = sample(track, Math.min(f, QUIET_START));
      const { dy, dr } = bob(sp.idle, f, i * 1.9);
      s.y += dy; s.r += dr;
      objects.push(objectState(id, sp.component, 'support', ZS[sp.lane], s));
    }
    objects.push(objectState('result', story.resolved, 'resolved', 9, sample(resultTrack, Math.min(f, QUIET_START))));
    frames.push(objects);
  }
  return frames;
}

// ---------------------------------------------------------------- reduced mode
// No travel: things fade in where they live, swap to their contact pose
// while invisible, and fade back. The hero swaps to its end place the same way.
function reducedObjects(story) {
  const frames = [];
  for (let f = 0; f < FRAMES; f++) {
    const objects = [];
    const heroO = f < 31 ? clamp((f - 2) / 2, 0, 1) : f < 33 ? clamp(1 - (f - 31), 0, 1) : clamp((f - 32) / 2, 0, 1);
    objects.push(objectState('hero', story.hero, 'hero', 4, { ...(f < 32 ? HERO : HERO_END), r: 0, o: heroO }));
    for (const [id, sp] of Object.entries(story.supports)) {
      const lane = LANE[sp.lane];
      const contact = { x: sp.contact.x, y: sp.contact.y, s: sp.contact.s || SUP, r: sp.contact.r % 360 };
      const { go, at, leave, end } = sp.reduced;
      const born = BIRTH[sp.lane][1];
      let pose = { ...lane, s: SUP, r: 0 }, o = clamp((f - (born - 2)) / 2, 0, 1);
      if (f > go) o = 0;
      if (f >= at - 1) { pose = contact; o = clamp(f - at + 1, 0, 1); }
      if (leave !== null && f > leave) { pose = { ...lane, s: SUP, r: 0 }; o = clamp(f - leave - 1, 0, 1); }
      if (f >= end[0]) o = Math.min(o, clamp(1 - (f - end[0]) / (end[1] - end[0]), 0, 1));
      objects.push(objectState(id, sp.component, 'support', ZS[sp.lane], { ...pose, o }));
    }
    objects.push(objectState('result', story.resolved, 'resolved', 9, { ...RESULT_END, r: 0, o: clamp((f - 32) / 2, 0, 1) }));
    frames.push(objects);
  }
  return frames;
}

// ---------------------------------------------------------------- symbols
const TICK_BASE = 35.5; // the drawn streaks point up-right; rotate them onto the travel direction
const SPARK_BASE = 90; // the drawn spark fans upwards

function symbolState(p, z, x, y, s, r, o) {
  const item = { instance: p.id, component: p.c, role: p.role, x: r2(x), y: r2(y), scale: r3(s), rotation: r2(r), opacity: r3(clamp(o, 0, 1)), z };
  if (p.motionFunction) item.motionFunction = p.motionFunction;
  if (p.anchor) item.anchorInstance = p.anchor;
  if (p.with) item.interactionWith = p.with;
  return item;
}

function momentumTicks(objectFrames, reduced) {
  const ids = objectFrames[0].map((o) => o.instance);
  return ids.map((id, n) => {
    const def = { id: `momentum-${id}`, c: 'symbol-motion-ticks', role: 'momentum', motionFunction: 'directional-trail', anchor: id };
    let lastPose = null;
    return objectFrames.map((objects, f) => {
      const now = objects.find((o) => o.instance === id);
      const before = f ? objectFrames[f - 1].find((o) => o.instance === id) : now;
      const dx = now.x - before.x, dy = now.y - before.y, speed = Math.hypot(dx, dy);
      let o = 0;
      if (!reduced && f < QUIET_START && speed > 3 && Math.min(now.opacity, before.opacity) > 0.3) {
        const reach = (OBJECT_BOX * now.scale) / 2.4 + 6;
        lastPose = { x: now.x - (dx / speed) * reach, y: now.y - (dy / speed) * reach, s: 0.22 + Math.min(0.12, speed / 80), r: (Math.atan2(dy, dx) * 180) / Math.PI + TICK_BASE };
        o = clamp((speed - 3) / 6, 0, 1) * Math.min(1, now.opacity);
      }
      const pose = lastPose || { x: now.x, y: now.y, s: 0.22, r: TICK_BASE };
      return symbolState(def, 20 + n, pose.x, pose.y, pose.s, pose.r, o);
    });
  });
}

function punctuationTrack(p, n, reduced) {
  const shift = { x: 0, y: 0 };
  const z = 12 + n;
  const out = [];
  for (let f = 0; f < FRAMES; f++) {
    let x = p.x + shift.x, y = p.y + shift.y, s = p.s, r = 0, o = 0;
    if (p.loop) {
      const [a, b] = p.loop;
      const mid = { x, y: y - p.rise / 2 };
      if (reduced) {
        o = f >= a && f <= b && f < QUIET_START ? 0.7 * Math.min(1, (f - a + 1) / 2, (b - f + 1) / 2) : 0;
        x = mid.x; y = mid.y;
      } else {
        const ph = (((f - a) % p.period) + p.period) % p.period / p.period;
        if (f >= a && f <= b) { o = Math.sin(Math.PI * ph) * Math.min(1, (b - f + 1) / 3); y -= p.rise * ph; x += 4 * Math.sin(ph * Math.PI * 2); s *= 0.9 + 0.2 * ph; }
        else { y = mid.y; }
      }
    } else if (p.orbit) {
      const [a, b] = p.orbit.f;
      const t = clamp((f - a) / (b - a), 0, 1);
      const ang = ((p.orbit.start + p.orbit.sweep * t) * Math.PI) / 180;
      x = p.orbit.x + shift.x + Math.cos(ang) * p.orbit.radius;
      y = p.orbit.y + shift.y + Math.sin(ang) * p.orbit.radius;
      const travel = (ang * 180) / Math.PI + (p.orbit.sweep < 0 ? -90 : 90);
      r = travel + TICK_BASE;
      o = !reduced && f >= a && f <= b ? 0.95 : 0;
    } else {
      const dur = p.dur || 3;
      const k = f - p.f;
      if (p.dir !== undefined) r = p.dir + SPARK_BASE;
      if (k >= 0 && k < dur && f < QUIET_START) {
        if (reduced) o = 0.85;
        else {
          const pop = [0.6, 1.12, 1, 0.9, 0.82][Math.min(k, 4)];
          s = p.s * pop;
          r += (p.spin || 0) * k;
          o = k === dur - 1 && dur > 1 ? 0.55 : 1;
          if (p.dir !== undefined) { const rad = (p.dir * Math.PI) / 180; x += Math.cos(rad) * 4 * k; y += Math.sin(rad) * 4 * k; }
        }
      }
    }
    out.push(symbolState(p, z, x, y, s, r, o));
  }
  return out;
}

// ---------------------------------------------------------------- treatment marks
function treatmentFrames(reduced, contactFrames) {
  const bubbleScale = [0.5, 0.72, 0.94, 1.05, 1.0];
  const bubbleOpacity = [0.15, 0.6, 0.9, 1, 1];
  return Array.from({ length: FRAMES }, (_, f) => {
    const trail = [0, 1, 2].map((k) => r3(clamp(reduced ? (f - k + 1) / 2 : f - k + 1, 0, 1)));
    const trailScale = [0, 1, 2].map((k) => (!reduced && f === k ? 1.35 : 1));
    let scale = reduced ? 1 : f < 5 ? bubbleScale[f] : 1;
    if (!reduced && f < QUIET_START && contactFrames.includes(f)) scale = 1.02;
    const opacity = reduced ? Math.min(1, 0.3 + f * 0.25) : f < 5 ? bubbleOpacity[f] : 1;
    return { bubbleScale: r3(scale), bubbleOpacity: r3(opacity), trail, trailScale };
  });
}

// ---------------------------------------------------------------- assemble
function buildTimeline(story, reduced) {
  const objectFrames = reduced ? reducedObjects(story) : fullObjects(story);
  const punctuation = [...SHARED_PUNCTUATION, ...story.punctuation];
  const symbolTracks = [...momentumTicks(objectFrames, reduced), ...punctuation.map((p, n) => punctuationTrack(p, n, reduced))];
  const contactFrames = punctuation.filter((p) => p.role === 'interaction' && p.f).map((p) => p.f);
  const treatment = treatmentFrames(reduced, contactFrames);
  return objectFrames.map((objects, f) => ({
    frame: f,
    timeMs: (f * 1000) / FPS,
    storyPhase: STORY_PHASE(f),
    quietTail: f >= QUIET_START,
    treatment: treatment[f],
    objects,
    symbols: symbolTracks.map((track) => track[f]),
  }));
}

const stories = {};
const metrics = {};
for (const [key, spec] of Object.entries(STORIES)) {
  const base = v2.stories[key];
  const supportIds = Object.keys(spec.supports);
  for (const id of supportIds) {
    const component = base.elements.find((e) => e !== base.hero && e !== base.resolved && e.includes(id));
    if (!component) throw new Error(`No pack picture for ${key}/${id}`);
    spec.supports[id].component = component;
  }
  spec.hero = base.hero; spec.resolved = base.resolved;
  const contacts = [
    ...spec.contacts.map(([x, y, f0, f1]) => ({ a: x, b: y, frames: [f0, f1] })),
    // The fold, the burst and the result's exit from the hero are touching on purpose.
    ...supportIds.flatMap((id, i) => [{ a: id, b: 'hero', frames: [29, 32] }, { a: id, b: 'result', frames: [30, 33] },
      ...supportIds.slice(i + 1).map((other) => ({ a: id, b: other, frames: [29, 32] }))]),
    { a: 'result', b: 'hero', frames: [31, 34] },
  ];
  const timelines = { bubble: { full: buildTimeline(spec, false), reduced: buildTimeline(spec, true) } };
  stories[key] = {
    label: base.label,
    targetAssetLabel: base.targetAssetLabel,
    targetAssetId: base.targetAssetId,
    elements: base.elements,
    hero: base.hero,
    resolved: base.resolved,
    supports: Object.fromEntries(supportIds.map((id) => [id, { component: spec.supports[id].component, lane: spec.supports[id].lane }])),
    storyBeats: spec.beats,
    sfx: base.sfx.map((cue) => ({ ...cue, frame: spec.sfx[cue.cue] ?? cue.frame })),
    contacts,
    timelines,
  };
  metrics[key] = {
    full: measureTimeline(timelines.bubble.full, components, contacts),
    reduced: measureTimeline(timelines.bubble.reduced, components, contacts),
  };
}

// Codex's V2 bubble, measured the same way and remapped onto pack files, for the side-by-side.
const srcBySourceUrl = Object.fromEntries(manifest.assets.filter((a) => a.sourceUrl).map((a) => [a.sourceUrl, local(a.file)]));
const v2Compare = { set: v2.set, status: v2.status, stories: {}, metrics: {} };
for (const [key, story] of Object.entries(v2.stories)) {
  v2Compare.stories[key] = { label: story.label, storyBeats: story.storyBeats, sfx: story.sfx, timelines: { bubble: story.timelines.bubble } };
  v2Compare.metrics[key] = { full: measureTimeline(story.timelines.bubble.full, components), reduced: measureTimeline(story.timelines.bubble.reduced, components) };
}
v2Compare.components = Object.fromEntries([...Object.entries(v2.inheritedComponents), ...Object.entries(v2.symbols)]
  .map(([id, item]) => [id, { src: srcBySourceUrl[item.src] }]));
v2Compare.bubble = { connectorLeftPx: v2.callout.bubbleRefinement.connectorLeftPx, mainFill: v2.callout.bubbleRefinement.mainFill };

const catalogue = {
  schema: 'lighthouse-keeper/keeper-prime-rear-action-choreography@2',
  set: SET,
  status: 'model-test-draft-not-approved',
  author: 'Claude Code (claude-opus-5-5), from Codex model-test pack',
  sourcePack: { dir: PACK_REPO, manifestSha256: sha256(path.join(PACK, 'asset-manifest.json')), v2CatalogueSha256: sha256(path.join(PACK, 'metadata/v2-catalogue.json')) },
  sequence,
  actionStartIndex: v2.actionStartIndex,
  callout: {
    frames: FRAMES, fps: FPS, quietTailFrames: FRAMES - QUIET_START, quietTailRange: [QUIET_START, FRAMES - 1],
    startsWithAction: true, placement: 'raised-above-cap', treatments: ['bubble'], motionModes: ['full', 'reduced'],
    origin: { cloudX: 182, cloudY: 193, note: 'head-aligned connector mouth; heroes and supports are born here in full motion' },
    lanes: LANE, heroHome: HERO, heroEnd: HERO_END, resultEnd: RESULT_END,
    reducedMotion: 'no travel or spin: fade in place, swap poses while invisible, punctuation static, no momentum ticks; same quiet tail as full',
  },
  components,
  stories,
  defaultStory: 'garden-bbq',
  controls: ['body', 'hero-result', 'supporting-objects', 'symbols', 'treatment-marks', 'sfx-declaration', 'speed', 'loop', 'reduced-motion', 'path-overlay', 'timeline', 'compare-v2'],
  separation: { bodySilent: true, bodyLayerIndependent: true, heroResultLayerIndependent: true, supportingObjectLayerIndependent: true, symbolLayerIndependent: true, treatmentLayerIndependent: true, sfxDeclarationIndependent: true, contextBakedIntoKeeper: false },
  approvalBoundary: { candidateApproved: false, runtimeChanged: false, finalChanged: false, kitchenChanged: false, primeAuthorityChanged: false, packChanged: false, deployed: false },
  metrics,
};

fs.writeFileSync(path.join(HERE, 'catalogue.json'), JSON.stringify(catalogue) + '\n');
fs.writeFileSync(path.join(HERE, 'compare-v2.json'), JSON.stringify(v2Compare) + '\n');
const summary = Object.fromEntries(Object.keys(stories).map((k) => [k, {
  c1: { overlap: metrics[k].full.maxUndeclaredOverlap, rawOverlap: metrics[k].full.maxObjectOverlap, heavyFrames: metrics[k].full.framesWithHeavyOverlap, outside: metrics[k].full.objectFramesOutsideBubble, symbols: metrics[k].full.symbolInstancesUsed },
  v2: { rawOverlap: v2Compare.metrics[k].full.maxObjectOverlap, heavyFrames: v2Compare.metrics[k].full.framesWithHeavyOverlap, outside: v2Compare.metrics[k].full.objectFramesOutsideBubble, symbols: v2Compare.metrics[k].full.symbolInstancesUsed },
}]));
console.log(JSON.stringify(summary, null, 1));

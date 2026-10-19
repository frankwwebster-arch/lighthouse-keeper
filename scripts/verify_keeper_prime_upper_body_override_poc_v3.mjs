#!/usr/bin/env node
/** Verify POC V3's rear-seam registration and one-shot advancing playback. */
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const root = path.resolve(import.meta.dirname, '..');
const v1Pack = 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v1';
const v2Pack = 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v2';
const v3Pack = 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v3';
const read = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const text = file => fs.readFileSync(path.join(root, file), 'utf8');
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex');
const v1Data = read(`${v1Pack}/keeper-prime-upper-body-override-poc-v1.json`);
const v2Data = read(`${v2Pack}/keeper-prime-upper-body-override-poc-v2.json`);
const data = read(`${v3Pack}/keeper-prime-upper-body-override-poc-v3.json`);
const v1Register = read(`${v1Pack}/batch-register.json`);
const register = read(`${v3Pack}/batch-register.json`);
const reviewer = text(`${v3Pack}/reviewer.html`);
const shell = text('public/keeper-review/keeper-prime-upper-body-override-poc-v3/index.html');

assert.equal(data.set, 'keeper-prime-upper-body-override-poc-v3');
assert.equal(register.set, data.set);
assert.equal(register.supersedes.set, v2Data.set);
assert.equal(register.correction.frameArtworkChanged, false);
assert.equal(register.correction.routeOrderChanged, false);
assert.equal(register.correction.routeTimingChanged, false);
assert.equal(register.correction.walkRootMotionChanged, false);
assert.equal(register.correction.rearSeam.playbackFrame, 18);
assert.equal(register.correction.rearSeam.presentationOffsetXLp, -1);
assert.equal(register.correction.playback.mode, 'one-shot');
for (const value of Object.values(register.approvalBoundary)) assert.equal(value, false);
for (const evidence of Object.values(register.provenance)) assert.equal(sha(evidence.file), evidence.sha256);
assert.equal(sha(register.candidate.route.file), register.candidate.route.sha256);
assert.equal(sha(register.candidate.reviewer.file), register.candidate.reviewer.sha256);

// V3 owns no new Keeper pixels or media.
assert.deepEqual(data.frames, v1Data.frames);
assert.deepEqual(register.candidate.frames, v1Register.candidate.frames);
assert.deepEqual(register.publishedAssets, v1Register.publishedAssets);
for (const asset of register.publishedAssets) assert.equal(sha(asset.source), asset.sourceSha256);

assert.equal(data.route.length, 33);
for (let i = 0; i < data.route.length; i++) {
  const current = data.route[i];
  const prior = v2Data.route[i];
  for (const key of ['recordId', 'mirror', 'rootXLp', 'phase', 'durationMs', 'sourceAnchorXLp']) {
    assert.deepEqual(current[key], prior[key], `route frame ${i + 1} changed ${key}`);
  }
  assert.equal(current.presentationOffsetXLp, i === 17 ? -1 : 0);
  assert.equal(current.renderAnchorXLp, prior.renderAnchorXLp + (i === 17 ? 1 : 0));
}

const rightWalk = data.route.slice(0, 8);
const leftWalk = data.route.slice(25);
for (let i = 1; i < rightWalk.length; i++) assert.equal(rightWalk[i].rootXLp - rightWalk[i - 1].rootXLp, 2.625);
for (let i = 1; i < leftWalk.length; i++) assert.equal(leftWalk[i - 1].rootXLp - leftWalk[i].rootXLp, 2.625);
assert.equal(rightWalk.at(-1).rootXLp - rightWalk[0].rootXLp, 18.375);
assert.equal(89 - rightWalk[0].rootXLp, 21);

function alphaCentroid(frame) {
  const image = PNG.sync.read(fs.readFileSync(path.join(root, data.frames[frame.recordId].candidate.file)));
  let sum = 0;
  let count = 0;
  for (let y = 0; y < image.height; y++) for (let x = 0; x < image.width; x++) {
    if (image.data[(y * image.width + x) * 4 + 3] > 0) { sum += x; count++; }
  }
  const local = frame.mirror ? image.width - 1 - sum / count : sum / count;
  return frame.rootXLp - frame.renderAnchorXLp + local / 8;
}
const seam = data.route.slice(16, 19).map(alphaCentroid);
assert.ok(Math.abs(seam[1] - seam[0]) < 0.5, `frame 17→18 centroid jump ${seam[1] - seam[0]}`);
assert.ok(Math.abs(seam[2] - seam[1]) < 0.5, `frame 18→19 centroid jump ${seam[2] - seam[1]}`);

for (const token of [
  'POC V3', 'V3 corrects the remaining visible rear seam and false walk-loop reset',
  'root x ${frame.rootXLp} lp', 'if(i===sequence.length-1){stop();return}',
  'if(i===sequence.length-1)i=0', 'presentationOffsetXLp',
  'Large inspection · 6 px/lp', 'Gameplay scale · 4 px/lp', 'Literal 1× · 1 px/lp',
  'Previous-frame ghost', 'Loading and decoding every unique frame', 'img.decode',
]) assert.ok(reviewer.includes(token), `reviewer omits ${token}`);
assert.ok(!reviewer.includes('i=(i+1)%sequence.length;show();timer=setTimeout(tick'));
assert.match(shell, /lighthouse-keeper\/[0-9a-f]{8,40}\/art\/drafts\/keeper-prime-upper-body-override-poc-2026-10-19-v3\/reviewer\.html/);
assert.doesNotMatch(shell, /__POC_V3_COMMIT__|\/main\/art\/drafts/);

console.log(`Prime held-implement POC V3 verified: standard ±2.625-lp gait advance retained, rear seam centroid deltas ${seam.slice(1).map((x, i) => (x - seam[i]).toFixed(3)).join(', ')} lp, one-shot playback, and no new Keeper pixels.`);

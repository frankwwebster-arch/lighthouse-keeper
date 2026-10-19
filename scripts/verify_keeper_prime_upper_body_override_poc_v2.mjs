#!/usr/bin/env node
/** Verify POC V2's presentation-only mirror-anchor correction. */
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const v1Pack = 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v1';
const v2Pack = 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v2';
const v1Set = 'keeper-prime-upper-body-override-poc-v1';
const v2Set = 'keeper-prime-upper-body-override-poc-v2';
const read = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const text = file => fs.readFileSync(path.join(root, file), 'utf8');
const hashBytes = value => crypto.createHash('sha256').update(value).digest('hex');
const sha = file => hashBytes(fs.readFileSync(path.join(root, file)));

const v1Data = read(`${v1Pack}/${v1Set}.json`);
const v2Data = read(`${v2Pack}/${v2Set}.json`);
const register = read(`${v2Pack}/batch-register.json`);
const reviewer = text(`${v2Pack}/reviewer.html`);
const shell = text(`public/keeper-review/${v2Set}/index.html`);

assert.equal(v2Data.set, v2Set);
assert.equal(v2Data.status, 'versioned-reversible-presentation-correction-not-approved');
assert.equal(register.set, v2Set);
assert.equal(register.supersedes.set, v1Set);
assert.equal(register.supersedes.status, 'immutable-unapproved-provenance');
for (const value of Object.values(register.approvalBoundary)) assert.equal(value, false);
assert.equal(register.correction.scope, 'reviewer-coordinate-only');
assert.equal(register.correction.frameArtworkChanged, false);
assert.equal(register.correction.routeTimingChanged, false);
assert.equal(register.correction.compensatedErrorLogicalPixels, 10.5);

for (const evidence of Object.values(register.provenance)) assert.equal(sha(evidence.file), evidence.sha256);
assert.equal(sha(register.candidate.route.file), register.candidate.route.sha256);
assert.equal(sha(register.candidate.reviewer.file), register.candidate.reviewer.sha256);

// V2 must reuse V1 artwork and review media exactly; only presentation metadata differs.
assert.deepEqual(register.candidate.frames, read(`${v1Pack}/batch-register.json`).candidate.frames);
assert.deepEqual(register.publishedAssets, read(`${v1Pack}/batch-register.json`).publishedAssets);
for (const asset of register.publishedAssets) assert.equal(sha(asset.source), asset.sourceSha256);
assert.deepEqual(v2Data.frames, v1Data.frames);
assert.equal(v2Data.route.length, 33);
for (let i = 0; i < v1Data.route.length; i++) {
  const { sourceAnchorXLp, renderAnchorXLp, ...routeCore } = v2Data.route[i];
  assert.deepEqual(routeCore, v1Data.route[i], `route frame ${i + 1} changed`);
  assert.equal(sourceAnchorXLp, 18.75);
  assert.equal(renderAnchorXLp, routeCore.mirror ? 29.25 : 18.75);

  // Model the CSS placement: mirroring maps source x to cellWidth - source x.
  const localRenderedRoot = routeCore.mirror ? 48 - sourceAnchorXLp : sourceAnchorXLp;
  const screenRoot = routeCore.rootXLp - renderAnchorXLp + localRenderedRoot;
  assert.ok(Math.abs(screenRoot - routeCore.rootXLp) < 1e-9, `frame ${i + 1} root drift`);
}
const frame17 = v2Data.route[16];
const frame18 = v2Data.route[17];
assert.equal(frame17.mirror, false);
assert.equal(frame18.mirror, true);
assert.equal(frame17.rootXLp, frame18.rootXLp);
const onScreenRoot = frame => frame.rootXLp - frame.renderAnchorXLp + (frame.mirror ? 48 - frame.sourceAnchorXLp : frame.sourceAnchorXLp);
assert.equal(onScreenRoot(frame17), onScreenRoot(frame18));

for (const token of [
  'POC V2', 'V2 corrects reviewer anchoring only',
  'const anchor=frame.renderAnchorXLp',
  "img.style.left=(frame.rootXLp-anchor)*stage.scale+'px'",
  'Large inspection · 6 px/lp', 'Gameplay scale · 4 px/lp', 'Literal 1× · 1 px/lp',
  'Previous-frame ghost', 'Loading and decoding every unique frame', 'img.decode',
]) assert.ok(reviewer.includes(token), `reviewer omits ${token}`);
assert.ok(!reviewer.includes("frame.rootXLp-18.75)*stage.scale"));
assert.match(shell, /lighthouse-keeper\/[0-9a-f]{8,40}\/art\/drafts\/keeper-prime-upper-body-override-poc-2026-10-19-v2\/reviewer\.html/);
assert.doesNotMatch(shell, /__POC_V2_COMMIT__|\/main\/art\/drafts/);

console.log('Prime held-implement POC V2 verified: V1 artwork/timing preserved byte-for-byte and all 33 frames retain their declared on-screen root through the mirrored turn boundary.');

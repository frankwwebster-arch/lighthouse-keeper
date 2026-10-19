import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

const root = process.cwd();
const v1Rel = 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v1';
const v2Rel = 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v2';
const v1 = join(root, v1Rel);
const v2 = join(root, v2Rel);
const dataName = 'keeper-prime-upper-body-override-poc-v2.json';
const shellRel = 'public/keeper-review/keeper-prime-upper-body-override-poc-v2/index.html';
const sha = value => createHash('sha256').update(value).digest('hex');
const write = (file, value) => {
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, value);
};

const v1Data = JSON.parse(readFileSync(join(v1, 'keeper-prime-upper-body-override-poc-v1.json')));
const data = structuredClone(v1Data);
data.set = 'keeper-prime-upper-body-override-poc-v2';
data.status = 'versioned-reversible-presentation-correction-not-approved';
data.correction = {
  scope: 'reviewer-coordinate-only',
  reason: 'Frame 18 begins mirrored playback; V1 mirrored the complete 48-lp cell around its centre while retaining the unmirrored 18.75-lp anchor, creating an artificial 10.5-lp lateral leap.',
  cellWidthLogicalPixels: 48,
  sourceRootLogicalPixels: 18.75,
  mirroredRootLogicalPixels: 29.25,
  compensatedErrorLogicalPixels: 10.5,
  affectedPlaybackFrames: [18, 33],
  frameArtworkChanged: false,
  routeTimingChanged: false,
};
data.route = v1Data.route.map(frame => ({
  ...frame,
  sourceAnchorXLp: 18.75,
  renderAnchorXLp: frame.mirror ? 29.25 : 18.75,
}));
data.reviewInstruction = 'V2 is the same immutable POC frame art and timing as V1. Judge the held-state motion after the reviewer-only mirror-anchor correction removes the false 10.5-lp leap at frames 17 to 18. Nothing is approved or promoted.';

let reviewer = readFileSync(join(v1, 'reviewer.html'), 'utf8');
reviewer = reviewer
  .replaceAll('POC V1', 'POC V2')
  .replace('This tests motion feasibility, not production art.</strong>', 'V2 corrects reviewer anchoring only.</strong> The frame artwork, route and timing are byte-identical to V1; the mirrored half now retains the same root position. This still tests motion feasibility, not production art.')
  .replace('const DATA=' + JSON.stringify(v1Data), 'const DATA=' + JSON.stringify(data))
  .replace(
    "img.style.left=(frame.rootXLp-18.75)*stage.scale+'px'",
    "const anchor=frame.renderAnchorXLp;img.style.left=(frame.rootXLp-anchor)*stage.scale+'px'",
  );
if (!reviewer.includes('const anchor=frame.renderAnchorXLp')) throw new Error('Reviewer anchor replacement failed');
if (reviewer.includes('const DATA=' + JSON.stringify(v1Data))) throw new Error('Reviewer data replacement failed');
write(join(v2, dataName), JSON.stringify(data, null, 2) + '\n');
write(join(v2, 'reviewer.html'), reviewer);

const v1Register = JSON.parse(readFileSync(join(v1, 'batch-register.json')));
const register = structuredClone(v1Register);
register.set = data.set;
register.status = 'prime-upper-body-override-poc-v2-awaiting-frank';
register.purpose = 'Presentation-only correction to the valuable V1 motion POC: preserve every frame and duration while maintaining the root anchor when the 48-lp cell is mirrored.';
register.supersedes = {
  set: v1Data.set,
  status: 'immutable-unapproved-provenance',
  reason: data.correction.reason,
};
register.correction = data.correction;
register.construction = {
  ...register.construction,
  v1FrameArtworkReusedByteForByte: true,
  v1RouteAndTimingPreserved: true,
  presentationFormula: 'left = rootXLp - (mirror ? 48 - 18.75 : 18.75)',
};
register.candidate.route = {
  file: `${v2Rel}/${dataName}`,
  sha256: sha(Buffer.from(JSON.stringify(data, null, 2) + '\n')),
};
register.candidate.reviewer = {
  file: `${v2Rel}/reviewer.html`,
  sha256: sha(Buffer.from(reviewer)),
};
register.candidate.reviewUrl = 'https://lighthouse-keeper-mu.vercel.app/keeper-review/keeper-prime-upper-body-override-poc-v2/index.html';
register.provenance = {
  v1Data: { file: `${v1Rel}/keeper-prime-upper-body-override-poc-v1.json`, sha256: sha(readFileSync(join(v1, 'keeper-prime-upper-body-override-poc-v1.json'))) },
  v1Reviewer: { file: `${v1Rel}/reviewer.html`, sha256: sha(readFileSync(join(v1, 'reviewer.html'))) },
  v1PublicShell: { file: 'public/keeper-review/keeper-prime-upper-body-override-poc-v1/index.html', sha256: sha(readFileSync(join(root, 'public/keeper-review/keeper-prime-upper-body-override-poc-v1/index.html'))) },
};
register.rollback = `Delete only ${v2Rel}, public/keeper-review/keeper-prime-upper-body-override-poc-v2 and the V2 builder/verifier scripts. V1 remains immutable.`;
write(join(v2, 'batch-register.json'), JSON.stringify(register, null, 2) + '\n');

write(join(v2, 'HANDOFF.md'), `# Prime Keeper upper-body override POC V2\n\nV2 changes no animation artwork, route order, root path or timing. It corrects only the V1 reviewer's mirrored-cell placement.\n\nThe source anchor is 18.75 lp inside a 48 lp cell. Under CSS horizontal mirroring that point becomes 29.25 lp. V1 continued subtracting 18.75 lp, so playback jumped 10.5 lp at frame 18. V2 subtracts 29.25 lp for every mirrored frame, preserving the declared root position across frame 17 to 18 and throughout the mirrored return.\n\nFrank described V1 as a valuable POC and requested this correction. That feedback is not recorded as formal approval. No production or runtime assets change.\n`);

const shell = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper upper-body override POC V2</title><style>html,body,iframe{margin:0;width:100%;height:100%;border:0;background:#07131b;color:#edf8fb;font:14px system-ui}#loading{padding:24px}iframe{display:none}</style><p id="loading">Loading immutable Prime Keeper upper-body override POC V2…</p><iframe id="review" title="Prime Keeper upper-body override POC V2 reviewer"></iframe><script>fetch("https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/__POC_V2_COMMIT__/art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v2/reviewer.html").then(r=>{if(!r.ok)throw Error(\'reviewer \'+r.status);return r.text()}).then(t=>{document.querySelector(\'#review\').srcdoc=t;document.querySelector(\'#review\').style.display=\'block\';document.querySelector(\'#loading\').remove()}).catch(e=>document.querySelector(\'#loading\').textContent=\'Reviewer failed to load: \'+e.message)</script></html>\n';
write(join(root, shellRel), shell);

console.log(`Built ${data.set}`);

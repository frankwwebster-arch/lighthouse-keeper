import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

const root = process.cwd();
const v1Rel = 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v1';
const v2Rel = 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v2';
const v3Rel = 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v3';
const v2 = join(root, v2Rel);
const v3 = join(root, v3Rel);
const dataName = 'keeper-prime-upper-body-override-poc-v3.json';
const shellRel = 'public/keeper-review/keeper-prime-upper-body-override-poc-v3/index.html';
const shaBytes = value => createHash('sha256').update(value).digest('hex');
const shaFile = file => shaBytes(readFileSync(join(root, file)));
const write = (file, value) => { mkdirSync(dirname(file), { recursive: true }); writeFileSync(file, value); };

const v2Data = JSON.parse(readFileSync(join(v2, 'keeper-prime-upper-body-override-poc-v2.json')));
const data = structuredClone(v2Data);
data.set = 'keeper-prime-upper-body-override-poc-v3';
data.status = 'versioned-reversible-motion-presentation-correction-not-approved';
data.correction = {
  scope: 'rear-seam-registration-and-one-shot-review-playback',
  frameArtworkChanged: false,
  routeOrderChanged: false,
  routeTimingChanged: false,
  walkRootMotionChanged: false,
  rearSeam: {
    playbackFrame: 18,
    recordId: 'turn8',
    mirror: true,
    presentationOffsetXLp: -1,
    reason: 'The planted root was correct in V2, but the generated proxy silhouette centroid still moved 1.333 lp right at the rear crossing. A one-lp presentation registration removes the visible leap without changing a pixel or duration.',
  },
  playback: {
    mode: 'one-shot',
    reason: 'An isolated advancing walk must stop at its translated endpoint; wrapping directly to frame 1 falsely reads as walking on the spot.',
  },
};
data.route = v2Data.route.map((frame, index) => ({
  ...frame,
  presentationOffsetXLp: index === 17 ? -1 : 0,
  renderAnchorXLp: frame.renderAnchorXLp + (index === 17 ? 1 : 0),
}));
data.reviewInstruction = 'V3 preserves all V1 artwork, approved gait order, turn order, timings and standard 2.625-lp walk advance. It corrects the remaining visible rear seam at playback frame 18 and makes playback one-shot so advancing walk clips stop at their translated endpoint rather than snapping back to frame 1. Nothing is approved or promoted.';
const dataText = JSON.stringify(data, null, 2) + '\n';
write(join(v3, dataName), dataText);

let reviewer = readFileSync(join(v2, 'reviewer.html'), 'utf8');
reviewer = reviewer
  .replaceAll('POC V2', 'POC V3')
  .replace(
    'V2 corrects reviewer anchoring only.</strong> The frame artwork, route and timing are byte-identical to V1; the mirrored half now retains the same root position. This still tests motion feasibility, not production art.',
    'V3 corrects the remaining visible rear seam and false walk-loop reset.</strong> Frame artwork, gait order, turn order and timing remain byte-identical to V1. Playback now stops at the translated endpoint instead of snapping back to the start. This still tests motion feasibility, not production art.',
  );
const dataStart = reviewer.indexOf('const DATA=');
const sequenceStart = reviewer.indexOf(';let sequence=', dataStart);
if (dataStart < 0 || sequenceStart < 0) throw new Error('Could not locate embedded reviewer data');
reviewer = reviewer.slice(0, dataStart) + 'const DATA=' + JSON.stringify(data) + reviewer.slice(sequenceStart);
reviewer = reviewer
  .replace(
    "document.querySelector('#caption').textContent=`${i+1}/${sequence.length} · ${frame.phase} · ${record.id} · visible hand components ${record.hands.visibleComponentCount}`;",
    "document.querySelector('#caption').textContent=`${i+1}/${sequence.length} · ${frame.phase} · ${record.id} · root x ${frame.rootXLp} lp · visible hand components ${record.hands.visibleComponentCount}`;",
  )
  .replace(
    "function tick(){const frame=sequence[i];i=(i+1)%sequence.length;show();timer=setTimeout(tick,frame.durationMs/Number(document.querySelector('#speed').value))}document.querySelector('#play').onclick=()=>{if(timer)stop();else{document.querySelector('#play').textContent='Pause';tick()}};",
    "function tick(){const frame=sequence[i];show();if(i===sequence.length-1){stop();return}timer=setTimeout(()=>{i+=1;tick()},frame.durationMs/Number(document.querySelector('#speed').value))}document.querySelector('#play').onclick=()=>{if(timer)stop();else{if(i===sequence.length-1)i=0;document.querySelector('#play').textContent='Pause';tick()}};",
  );
for (const token of ['POC V3', 'root x ${frame.rootXLp} lp', 'if(i===sequence.length-1){stop();return}', 'presentationOffsetXLp']) {
  if (!reviewer.includes(token)) throw new Error(`Reviewer V3 replacement failed: ${token}`);
}
write(join(v3, 'reviewer.html'), reviewer);

const v2Register = JSON.parse(readFileSync(join(v2, 'batch-register.json')));
const register = structuredClone(v2Register);
register.set = data.set;
register.status = 'prime-upper-body-override-poc-v3-awaiting-frank';
register.purpose = 'Preserve the valuable held-state POC while removing the remaining visible rear-crossing leap and the isolated-walk reset that read as walking on the spot.';
register.supersedes = {
  set: v2Data.set,
  status: 'immutable-unapproved-provenance',
  reason: 'V2 corrected the mirrored cell anchor but retained a one-frame silhouette-mass shift at playback frame 18 and looped advancing walk clips directly back to their starting coordinate.',
};
register.correction = data.correction;
register.construction = {
  ...register.construction,
  v1FrameArtworkReusedByteForByte: true,
  v1RouteOrderAndTimingPreserved: true,
  standardWalkAdvanceLogicalPixelsPerFrame: 2.625,
  reviewPlayback: 'one-shot; replay restarts from frame 1',
  rearSeamPresentationOffsetLogicalPixels: -1,
};
register.candidate.route = { file: `${v3Rel}/${dataName}`, sha256: shaBytes(dataText) };
register.candidate.reviewer = { file: `${v3Rel}/reviewer.html`, sha256: shaBytes(reviewer) };
register.candidate.reviewUrl = 'https://lighthouse-keeper-mu.vercel.app/keeper-review/keeper-prime-upper-body-override-poc-v3/index.html';
register.provenance = {
  v1Data: { file: `${v1Rel}/keeper-prime-upper-body-override-poc-v1.json`, sha256: shaFile(`${v1Rel}/keeper-prime-upper-body-override-poc-v1.json`) },
  v1Reviewer: { file: `${v1Rel}/reviewer.html`, sha256: shaFile(`${v1Rel}/reviewer.html`) },
  v2Data: { file: `${v2Rel}/keeper-prime-upper-body-override-poc-v2.json`, sha256: shaFile(`${v2Rel}/keeper-prime-upper-body-override-poc-v2.json`) },
  v2Reviewer: { file: `${v2Rel}/reviewer.html`, sha256: shaFile(`${v2Rel}/reviewer.html`) },
  v2PublicShell: { file: 'public/keeper-review/keeper-prime-upper-body-override-poc-v2/index.html', sha256: shaFile('public/keeper-review/keeper-prime-upper-body-override-poc-v2/index.html') },
};
register.rollback = `Delete only ${v3Rel}, public/keeper-review/keeper-prime-upper-body-override-poc-v3 and the V3 builder/verifier scripts. V1 and V2 remain immutable.`;
write(join(v3, 'batch-register.json'), JSON.stringify(register, null, 2) + '\n');

write(join(v3, 'HANDOFF.md'), `# Prime Keeper upper-body override POC V3\n\nV3 changes no Keeper pixel, gait order, turn order, root-motion speed or duration. It makes two review-presentation corrections requested by Frank:\n\n1. Playback frame 18 receives a one-logical-pixel left registration. V2 fixed the mathematical cell mirror, but the generated proxy's visible silhouette still moved 1.333 lp right at the rear crossing. The V3 correction reduces the adjacent full-silhouette centroid changes to +0.333 and -0.408 lp.\n2. Playback is one-shot. Walk-right stops after the standard 21-lp cycle at its translated endpoint; replay restarts from frame 1. It no longer wraps immediately to the start and therefore no longer reads as walking on the spot.\n\nThis remains a non-production POC. Frank has not formally approved it.\n`);

const shell = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper upper-body override POC V3</title><style>html,body,iframe{margin:0;width:100%;height:100%;border:0;background:#07131b;color:#edf8fb;font:14px system-ui}#loading{padding:24px}iframe{display:none}</style><p id="loading">Loading immutable Prime Keeper upper-body override POC V3…</p><iframe id="review" title="Prime Keeper upper-body override POC V3 reviewer"></iframe><script>fetch("https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/__POC_V3_COMMIT__/art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v3/reviewer.html").then(r=>{if(!r.ok)throw Error(\'reviewer \'+r.status);return r.text()}).then(t=>{document.querySelector(\'#review\').srcdoc=t;document.querySelector(\'#review\').style.display=\'block\';document.querySelector(\'#loading\').remove()}).catch(e=>document.querySelector(\'#loading\').textContent=\'Reviewer failed to load: \'+e.message)</script></html>\n';
write(join(root, shellRel), shell);

console.log(`Built ${data.set}`);

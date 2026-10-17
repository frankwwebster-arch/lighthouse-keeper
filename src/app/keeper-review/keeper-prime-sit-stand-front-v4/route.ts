import { GET as getV3 } from '../keeper-prime-sit-stand-front-v3/route'

export async function GET() {
  const response = await getV3()
  let html = await response.text()
  html = html
    .replaceAll('keeper-prime-sit-stand-front-v3', 'keeper-prime-sit-stand-front-v4')
    .replaceAll('front sit ↔ stand V3', 'front sit ↔ stand V4')
    .replace('Complete-context width-smoothed Prime redraw · review only · nothing promoted', 'Frame-32 elbow-width-locked Prime redraw · review only · nothing promoted')
    .replace('F2 and F4–F5 retain V2 exactly; F3 is newly redrawn from the Prime authorities to remove the complete-context frame 29→30 width snap.', 'F2–F5 are newly redrawn from the Prime authorities with their outer elbow span locked to exact frame 32/F6; lowering is articulated instead of scaling the Keeper.')
    .replace('F2 and corrected F4–F5 show their exact inherited V2 cells; corrected F3 shows its new generated source beside the deterministic narrow registered cell.', 'F2–F5 show each new complete generated source beside its frame-32-width-locked registered cell; F1 and F6 show immutable exact endpoints.')
    .replace('Front V1 and V2 are rejected for width drift; Front V3 is a new candidate only.', 'Front V1–V3 are rejected for width drift; Front V4 is a new candidate only.')
    .replace('<strong>6 action poses</strong><br>exact Prime endpoints', '<strong>143 px elbow span</strong><br>frames 28–32 match exact F6')
    .replace('<label><input id="primeGhost" type="checkbox" disabled> Standing Prime ghost</label><label><input id="adjacentGhost" type="checkbox" disabled> Previous-frame ghost</label>', '<label><input id="primeGhost" type="checkbox" disabled> Standing Prime ghost</label><label><input id="seatedGhost" type="checkbox" checked disabled> Frame 32 seated-Prime ghost</label><label><input id="adjacentGhost" type="checkbox" disabled> Previous-frame ghost</label>')
    .replace("['ghost prime','ghost adjacent','actor']", "['ghost prime','ghost seated','ghost adjacent','actor']")
    .replace("prime=stage.querySelector('.prime'),adjacent=stage.querySelector('.adjacent')", "prime=stage.querySelector('.prime'),seated=stage.querySelector('.seated'),adjacent=stage.querySelector('.adjacent')")
    .replace("else prime.hidden=true;if(document.querySelector('#adjacentGhost').checked", "else prime.hidden=true;if(document.querySelector('#seatedGhost').checked)place(seated,{src:data.action.frames[5].src,rootXLp:frame.rootXLp,bottomLp:frame.bottomLp},z);else seated.hidden=true;if(document.querySelector('#adjacentGhost').checked")
    .replace("['primeGhost','adjacentGhost','guides']", "['primeGhost','seatedGhost','adjacentGhost','guides']")
  return new Response(html, { headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' } })
}

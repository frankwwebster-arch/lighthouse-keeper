import { GET as getV2 } from '../keeper-prime-sit-stand-front-v2/route'

export async function GET() {
  const response = await getV2()
  let html = await response.text()
  html = html
    .replaceAll('keeper-prime-sit-stand-front-v2', 'keeper-prime-sit-stand-front-v3')
    .replaceAll('front sit ↔ stand V2', 'front sit ↔ stand V3')
    .replace('Width-corrected reversible Prime redraw · review only · nothing promoted', 'Complete-context width-smoothed Prime redraw · review only · nothing promoted')
    .replace('F2–F3 retain V1 exactly; F4–F5 are newly redrawn from those Prime authorities to remove the rejected width drift.', 'F2 and F4–F5 retain V2 exactly; F3 is newly redrawn from the Prime authorities to remove the complete-context frame 29→30 width snap.')
    .replace('F2–F3 show their exact inherited V1 cells; corrected F4–F5 show each retained generated source beside its deterministic narrow registered cell.', 'F2 and corrected F4–F5 show their exact inherited V2 cells; corrected F3 shows its new generated source beside the deterministic narrow registered cell.')
    .replace('Front V1 is rejected for width drift; Front V2 is a new candidate only.', 'Front V1 and V2 are rejected for width drift; Front V3 is a new candidate only.')
  return new Response(html, { headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' } })
}

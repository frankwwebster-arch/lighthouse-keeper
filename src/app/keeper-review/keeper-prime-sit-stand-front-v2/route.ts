import { GET as getV1 } from '../keeper-prime-sit-stand-front-v1/route'

export async function GET() {
  const response = await getV1()
  let html = await response.text()
  html = html
    .replaceAll('keeper-prime-sit-stand-front-v1', 'keeper-prime-sit-stand-front-v2')
    .replaceAll('front sit ↔ stand V1', 'front sit ↔ stand V2')
    .replace('New reversible Prime redraw · review only · nothing promoted', 'Width-corrected reversible Prime redraw · review only · nothing promoted')
    .replace('F2–F5 are newly drawn from those Prime authorities.', 'F2–F3 retain V1 exactly; F4–F5 are newly redrawn from those Prime authorities to remove the rejected width drift.')
    .replace('F2–F5 show each retained generated source beside its deterministic 256×320 registered candidate cell.', 'F2–F3 show their exact inherited V1 cells; corrected F4–F5 show each retained generated source beside its deterministic narrow registered cell.')
    .replace('Front V1 is a new candidate only.', 'Front V1 is rejected for width drift; Front V2 is a new candidate only.')
  return new Response(html, { headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' } })
}

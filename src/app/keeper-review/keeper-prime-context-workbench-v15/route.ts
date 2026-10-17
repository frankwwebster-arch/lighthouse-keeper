const html = `<!doctype html><meta charset="utf-8"><title>Prime Keeper Context Workbench V15</title><body><script>fetch('/keeper-review/keeper-prime-context-workbench-v11/loader.js').then(r=>r.text()).then(s=>eval(s.replaceAll('/keeper-review/keeper-prime-sit-stand-side-v2/','/keeper-review/keeper-prime-sit-stand-side-v6/').replaceAll('side-right sit ↔ stand V2','side-right sit ↔ stand V6').replaceAll('prime-side-sit-stand-v2','prime-side-sit-stand-v6').replaceAll('candidate · chair geometry corrected','candidate · measured seat support').replaceAll('V1 Keeper frames and motion unchanged; chair top is 11 lp above floor and its 11-lp seat depth runs only from the spine contact to the back-of-knee line.','Exact V2/V1 Keeper frames and route unchanged; chair support begins at the first transparent row below the seated pelvis, 7.75 lp above floor.').replaceAll('V11 retains every prior route and replaces the sitting link with V2. The animation is byte-identical to V1; only the measured chair proxy changes.','V15 retains every prior route and replaces only the active sitting link with V6. Keeper frames, timing and root motion remain exact; only the chair support plane moves to the measured seated underside.').replaceAll('replaces-side-sit-stand-with-chair-corrected-v2','replaces-side-sit-stand-with-measured-support-v6').replaceAll('V11','V15'))).catch(e=>document.body.textContent='Workbench locked: '+e.message)</script></body>`

export const dynamic = 'force-dynamic'

export function GET() {
  return new Response(html, {
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'no-store',
    },
  })
}

const html = `<!doctype html><meta charset="utf-8"><title>Prime Keeper Context Workbench V14</title><body><script>fetch('/keeper-review/keeper-prime-context-workbench-v11/loader.js').then(r=>r.text()).then(s=>eval(s.replaceAll('/keeper-review/keeper-prime-sit-stand-side-v2/','/keeper-review/keeper-prime-sit-stand-side-v5/').replaceAll('side-right sit ↔ stand V2','side-right sit ↔ stand V5').replaceAll('V11','V14'))).catch(e=>document.body.textContent='Workbench locked: '+e.message)</script></body>`

export const dynamic = 'force-dynamic'

export function GET() {
  return new Response(html, {
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'no-store',
    },
  })
}

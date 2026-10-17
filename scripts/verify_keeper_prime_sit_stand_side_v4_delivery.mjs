import assert from 'node:assert/strict'
import fs from 'node:fs'

const sitRoute = fs.readFileSync('src/app/keeper-review/keeper-prime-sit-stand-side-v4/route.ts', 'utf8')
const workbenchRoute = fs.readFileSync('src/app/keeper-review/keeper-prime-context-workbench-v13/route.ts', 'utf8')
assert.ok(sitRoute.includes("new URL('/keeper-review/keeper-prime-sit-stand-side-v2/index.html', `${protocol}://${host}`)"))
assert.ok(sitRoute.includes('NextResponse.redirect(target, 307)'))
assert.ok(workbenchRoute.includes("replaceAll('/keeper-review/keeper-prime-sit-stand-side-v2/','/keeper-review/keeper-prime-sit-stand-side-v4/')"))
assert.ok(workbenchRoute.includes("replaceAll('side-right sit ↔ stand V2','side-right sit ↔ stand V4')"))
assert.ok(workbenchRoute.includes("replaceAll('V11','V13')"))
assert.equal(fs.existsSync('public/keeper-review/keeper-prime-sit-stand-side-v4'), false)
assert.equal(fs.existsSync('public/keeper-review/keeper-prime-context-workbench-v13'), false)
console.log('Keeper Prime sit/stand V4 delivery verified: absolute app-route redirect to immutable V2 review; Workbench V13 selects V4; no public payload growth.')

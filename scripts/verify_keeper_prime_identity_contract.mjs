#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = process.cwd()
const contractPath = path.join(ROOT, 'data/keeper_prime_identity_contract.json')
const contract = JSON.parse(fs.readFileSync(contractPath, 'utf8'))
const fail = (message) => { console.error(`Prime identity contract failed: ${message}`); process.exit(1) }
const sha256 = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

if (contract.schema !== 'lighthouse-keeper/prime-identity-contract@1') fail('unexpected schema')
if (JSON.stringify(contract.coordinateSystem.logicalCell) !== '[32,40]') fail('logical cell changed')
if (JSON.stringify(contract.coordinateSystem.authoringCell) !== '[256,320]') fail('authoring cell changed')
if (JSON.stringify(contract.coordinateSystem.runtimeCell) !== '[128,160]') fail('runtime cell changed')
if (JSON.stringify(contract.coordinateSystem.authoringAnchor) !== '[128,320]') fail('authoring anchor changed')
if (contract.coordinateSystem.capTopY !== 18 || contract.coordinateSystem.opaqueFloorY !== 316) fail('vertical registration changed')

for (const [id, authority] of Object.entries(contract.authorities)) {
  const file = path.join(ROOT, authority.file)
  if (!fs.existsSync(file)) fail(`${id} authority is missing`)
  if (sha256(file) !== authority.sha256) fail(`${id} authority hash changed`)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 256 || png.height !== 320) fail(`${id} is not a 256x320 authoring cell`)
  let edgeAlpha = 0
  for (let x = 0; x < png.width; x += 1) edgeAlpha += (png.data[(x * 4) + 3] > 0 ? 1 : 0) + (png.data[(((png.height - 1) * png.width + x) * 4) + 3] > 0 ? 1 : 0)
  for (let y = 1; y < png.height - 1; y += 1) edgeAlpha += (png.data[((y * png.width) * 4) + 3] > 0 ? 1 : 0) + (png.data[((y * png.width + png.width - 1) * 4) + 3] > 0 ? 1 : 0)
  if (edgeAlpha) fail(`${id} has ${edgeAlpha} opaque cell-edge pixels`)
  if (authority.opaqueBoundsExclusive) {
    let minX = png.width; let minY = png.height; let maxX = -1; let maxY = -1
    for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
      if (png.data[((y * png.width + x) * 4) + 3] < 8) continue
      minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
    }
    const actual = [minX, minY, maxX + 1, maxY + 1]
    if (JSON.stringify(actual) !== JSON.stringify(authority.opaqueBoundsExclusive)) fail(`${id} bounds changed: ${actual}`)
  }
}

const expectedColours = {
  capCrownBlue: [0, 109, 231], capBandNavy: [59, 67, 99], jumperBlue: [0, 108, 230],
  jumperCream: [251, 232, 206], trouserNavy: [63, 75, 112], bootNavy: [63, 74, 111],
}
for (const [component, rgb] of Object.entries(expectedColours)) {
  if (JSON.stringify(contract.standardUniformColourReferences[component]) !== JSON.stringify(rgb)) fail(`${component} colour reference changed`)
}
if (!contract.authoringRules.ligneClaireCostumes || contract.authoringRules.ligneClaireCostumes.length !== 8) fail('the eight ligne-claire costume rules are incomplete')

console.log('Prime Keeper identity contract verified: 32x40 lp, 8x authoring/4x runtime, four hash-pinned view authorities, exact registration, safe gutters and locked standard-uniform colour references.')

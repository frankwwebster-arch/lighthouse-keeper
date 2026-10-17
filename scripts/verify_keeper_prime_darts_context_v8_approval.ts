#!/usr/bin/env node
/** Verify Frank's immutable approval of exact Keeper Prime Darts Context V8. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const DECISION = path.join(ROOT, 'docs/review/keeper-prime-darts-context-v8-approval-2026-10-17.json')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-darts-context-2026-10-17-v8')
const REGISTER = path.join(PACK, 'batch-register.json')
const ROUTE = path.join(PACK, 'keeper-prime-darts-context-v8.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-darts-context-v8')
const DART = path.join(PACK, 'sources/rendered/keeper_dart_prime_v1.png')
const BOARD = path.join(PACK, 'sources/rendered/keeper_dartboard_edge_on_v1.png')
const fail = (message: string): never => { throw new Error(`Keeper Prime Darts Context V8 approval: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [DECISION, REGISTER, ROUTE, DART, BOARD, path.join(PUBLIC, 'index.html'), path.join(PUBLIC, 'app.js'), path.join(PUBLIC, 'route.json')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const decision = JSON.parse(fs.readFileSync(DECISION, 'utf8')) as Record<string, any>
if (decision.schema !== 'lighthouse-keeper/review-decision@1' || decision.reviewedBy !== 'Frank' || decision.reviewedOn !== '2026-10-17') fail('review identity changed')
if (decision.candidate !== 'keeper-prime-darts-context-2026-10-17-v8' || decision.decision !== 'approved-as-contextual-darts-animation-authority' || decision.wording !== 'approved') fail('approval wording changed')
const pinned: Record<string, string> = {
  batchRegister: REGISTER,
  routeData: ROUTE,
  reviewPage: path.join(PUBLIC, 'index.html'),
  reviewApp: path.join(PUBLIC, 'app.js'),
  dart: DART,
  dartboard: BOARD,
}
for (const [key, file] of Object.entries(pinned)) if (decision.approvedHashes?.[key] !== hash(file)) fail(`${key} hash changed`)
if (hash(ROUTE) !== hash(path.join(PUBLIC, 'route.json'))) fail('published route differs from approved route')

const data = JSON.parse(fs.readFileSync(ROUTE, 'utf8')) as Record<string, any>
if (data.schema !== 'lighthouse-keeper/darts-context@8' || data.route?.length !== 181) fail('route identity or frame count changed')
const flights = data.route.filter((frame: Record<string, any>) => frame.flyingDart)
if (flights.length !== 30) fail('airborne frame count changed')
const endpoints = flights.filter((frame: Record<string, any>) => frame.flyingDart.progress === 1)
if (endpoints.length !== 6) fail('throw endpoint count changed')
for (const frame of flights) {
  const dart = frame.flyingDart
  const tail = dart.startXLp + (dart.targetXLp - dart.startXLp) * dart.progress
  if (tail + data.propGeometry.dartLengthLp > data.propGeometry.boardFaceXLp + 1e-9) fail('dart crosses approved board face')
}
for (const frame of endpoints) if (frame.flyingDart.targetXLp !== data.propGeometry.embeddedTailXLp) fail('airborne/embedded tail seam changed')
if (data.dartDesign?.sourceSha256 !== decision.approvedHashes.dart || data.boardDesign?.sourceSha256 !== decision.approvedHashes.dartboard) fail('route prop hashes changed')
for (const flag of ['contextualDartsRouteApproved', 'harmonisedDartApproved', 'segmentedDartboardApproved', 'workbenchV9RemainsReviewInfrastructure']) if (decision.approvalBoundary?.[flag] !== true) fail(`${flag} changed`)
for (const flag of ['finalChanged', 'runtimeChanged', 'productionChanged', 'promotionPerformed']) if (decision.approvalBoundary?.[flag] !== false) fail(`${flag} boundary changed`)
console.log('Keeper Prime Darts Context V8 approval verified: exact 181-frame route, harmonised dart and segmented board pinned; Final/runtime/production unchanged.')

#!/usr/bin/env node
/** Losslessly compact repeated reviewer data and its byte-identical audit mirror. */
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const publicFile = path.join(root, 'public/keeper-review/index.html')
const mirrorFile = path.join(root, 'docs/keeper-scale-audit/review.html')
const source = fs.readFileSync(publicFile, 'utf8')
if (source !== fs.readFileSync(mirrorFile, 'utf8')) throw new Error('reviewer and audit mirror differ before compaction')
const prefix = 'const DATA='
const delimiter = ';\nconst $='
const beforeData = source.split(prefix, 2)[0]
const remainder = source.split(prefix, 2)[1]
if (!remainder?.includes(delimiter)) throw new Error('canonical reviewer data boundary not found')
const [json, afterData] = remainder.split(delimiter, 2)
const data = JSON.parse(json)
const reference = JSON.stringify(data.originalReference)
let factored = 0
for (const asset of data.assets) {
  if (asset.leadIn && JSON.stringify(asset.leadIn) === reference) {
    delete asset.leadIn
    asset.leadInRef = 'originalReference'
    factored += 1
  }
}
if (factored < 100) throw new Error(`expected at least 100 repeated lead-ins, found ${factored}`)
const fallback = "const lead=asset.leadIn?[asset.leadIn]:asset.leadInRef==='originalReference'?[DATA.originalReference]:[];"
const hydratedTail = (`const $=${afterData}`).replace('const lead=asset.leadIn?[asset.leadIn]:[];', fallback)
if (!hydratedTail.includes(fallback)) throw new Error('reviewer lead-in hydration point not found')
const compact = `${beforeData}${prefix}${JSON.stringify(data)};\n${hydratedTail}`
if (compact.length >= source.length) throw new Error('reviewer compaction did not reduce bytes')
fs.writeFileSync(publicFile, compact)
fs.writeFileSync(mirrorFile, compact)
console.log(JSON.stringify({ factoredLeadIns: factored, beforeBytes: source.length, afterBytes: compact.length, savedBytes: source.length - compact.length }, null, 2))

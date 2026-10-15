#!/usr/bin/env node
/** Pin Frank's approval of exact V16 without duplicating or promoting artwork. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v17')
const v16 = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16')
const registerPath = path.join(pack, 'batch-register.json')
const v16RegisterPath = path.join(v16, 'batch-register.json')
const v16RigPath = path.join(v16, 'stair-contact-rig-v16.json')
const v16PagePath = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v16/index.html')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
for (const file of [registerPath, v16RegisterPath, v16RigPath, v16PagePath, path.join(pack, 'HANDOFF.md'), path.join(pack, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const approval = JSON.parse(fs.readFileSync(registerPath, 'utf8'))
const v16Register = JSON.parse(fs.readFileSync(v16RegisterPath, 'utf8'))
approval.approvedCandidate.registerSha256 = sha(v16RegisterPath)
approval.approvedCandidate.rigSha256 = sha(v16RigPath)
approval.approvedCandidate.reviewPageSha256 = sha(v16PagePath)
approval.approvedCandidate.frames = v16Register.assets.map((asset) => ({ role: asset.role, file: asset.source, sha256: asset.sourceSha256 }))
fs.writeFileSync(registerPath, `${JSON.stringify(approval, null, 2)}\n`)
console.log(JSON.stringify({ approval: rel(registerPath), approvedFrames: approval.approvedCandidate.frames.length, v16RegisterSha256: approval.approvedCandidate.registerSha256 }, null, 2))

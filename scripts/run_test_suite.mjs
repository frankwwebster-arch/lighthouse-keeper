#!/usr/bin/env node
/** Run the existing suite with archive-backed compatibility for immutable paths. */
import { spawnSync } from 'node:child_process'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const hook = pathToFileURL(path.join(root, 'scripts/review_archive_fs_hook.mjs')).href
const nodeOptions = [process.env.NODE_OPTIONS, `--import=${hook}`].filter(Boolean).join(' ')
const result = spawnSync('npm', ['run', 'test:core'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (result.error) throw result.error
process.exit(result.status ?? 1)

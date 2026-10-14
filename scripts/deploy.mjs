#!/usr/bin/env node
// Release the current `main` to production.
//
//   npm run deploy                     (default note)
//   npm run deploy -- "review batch 4" (custom note)
//
// It makes one empty commit whose message carries the [deploy] marker and
// pushes it to origin/main. Vercel's Ignored Build Step
// (scripts/vercel-ignore-build.mjs) builds only commits like this.
// Nothing else on Vercel changes. See docs/DEPLOYMENT.md.

import { execFileSync } from 'node:child_process'

const git = (...args) => execFileSync('git', args, { encoding: 'utf8' }).trim()
const run = (...args) => execFileSync('git', args, { stdio: 'inherit' })

const note = process.argv.slice(2).join(' ').trim() || 'release current main'

const branch = git('rev-parse', '--abbrev-ref', 'HEAD')
if (branch !== 'main') {
  console.error(`Deploy runs from main only (you are on "${branch}").`)
  process.exit(1)
}

if (git('status', '--porcelain', '--untracked-files=no')) {
  console.error('Commit or stash your changes first; deploy releases what is on origin/main.')
  process.exit(1)
}

run('pull', '--rebase', 'origin', 'main')
run('commit', '--allow-empty', '-m', `Deploy: ${note} [deploy]`)
run('push', 'origin', 'main')

console.log('\nPushed a [deploy] commit. Vercel will build production in a few minutes:')
console.log('https://lighthouse-keeper-mu.vercel.app')

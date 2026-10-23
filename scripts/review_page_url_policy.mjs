import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

// These pages predate the root-absolute URL rule and are immutable. The tree
// digest lets them remain available without allowing any new relative asset
// URL—or any mutation of a grandfathered page—to pass publication checks.
// Kitchen review history was deliberately consolidated on 24 October 2026;
// its relative-URL pages were deleted rather than grandfathered forever.
const LEGACY_RELATIVE_PAGE_COUNT = 15
const LEGACY_RELATIVE_PAGE_TREE_SHA256 = '7f062cb0ac45f9d6e02b57f1cb6309aba5df32c913e61cc4aca9cd9f74fe7485'
const RELATIVE_ASSET_URL = /["'](?:\.\/)?assets\//

const posix = value => value.split(path.sep).join('/')
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')

function walk(directory) {
  if (!fs.existsSync(directory)) return []
  const files = []
  for (const entry of fs.readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    const absolute = path.join(directory, entry.name)
    if (entry.isDirectory()) files.push(...walk(absolute))
    else if (entry.isFile()) files.push(absolute)
  }
  return files
}

export function verifyRootAbsoluteReviewUrls(root) {
  const reviewRoot = path.join(root, 'public', 'keeper-review')
  const legacyPages = walk(reviewRoot)
    .filter(file => file.endsWith('.html') && RELATIVE_ASSET_URL.test(fs.readFileSync(file, 'utf8')))
    .sort()
  const digest = crypto.createHash('sha256')
  for (const file of legacyPages) {
    digest.update(posix(path.relative(root, file)))
    digest.update('\0')
    digest.update(sha256(fs.readFileSync(file)))
    digest.update('\0')
  }
  const treeSha256 = digest.digest('hex')
  if (legacyPages.length !== LEGACY_RELATIVE_PAGE_COUNT || treeSha256 !== LEGACY_RELATIVE_PAGE_TREE_SHA256) {
    throw new Error(
      'Review-page URL policy: a new or modified relative assets/ URL was found. ' +
      'Vercel removes trailing slashes, so every new review payload URL must be root-absolute ' +
      '(for example /keeper-review/<set>/assets/<name>). Preserve grandfathered pages byte-for-byte.',
    )
  }
  return { legacyPageCount: legacyPages.length, legacyPageTreeSha256: treeSha256 }
}

const invokedDirectly = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)
if (invokedDirectly) {
  const result = verifyRootAbsoluteReviewUrls(process.cwd())
  console.log(`Review-page URL policy verified: ${result.legacyPageCount} immutable legacy pages; new pages require root-absolute assets.`)
}

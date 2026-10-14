import archiveIndex from '../../review-archive/index.json'

type ArchiveEntry = {
  sha256: string
  extension: string
  bytes: number
  object: string
  url: string
}

const entries = archiveIndex.legacyPaths as Record<string, ArchiveEntry>

export function reviewArchiveEntry(pathname: string): ArchiveEntry | null {
  if (!pathname.startsWith('/keeper-review/')) return null
  return entries[pathname] ?? null
}

export const reviewArchiveStats = archiveIndex.stats

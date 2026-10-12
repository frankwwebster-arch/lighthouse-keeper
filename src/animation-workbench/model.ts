export type Lane = 'draft' | 'final'
export type TransitionPolicy = 'required' | 'door-hidden'

export type SpriteAsset = {
  id: string
  name: string
  file: string
  sha256: string
  w: number
  h: number
  frames: number
  fps: number
  density: number
  anchor: [number, number]
  startPose?: string
  endPose?: string
  outfit?: string
  loop: boolean
  mirrorSafe: boolean
  source: string
  immutable: boolean
}

export type TimelineEntry = { id: string; frame: number }
export type SectionLoop = { id: string; startId: string; endId: string; repeats: number }
export type RouteSegment = {
  id: string
  label: string
  assetId: string
  frames: number[]
  repeats: number
  mirror: boolean
  fps?: number
}

export type Approval = {
  approvedBy: string
  approvedOn: string
  wording: string
  scope: string
}

export type WorkbenchItem = {
  id: string
  lane: Lane
  name: string
  title: string
  description: string
  assetId: string
  timeline: TimelineEntry[]
  sectionLoops: SectionLoop[]
  overallLoop: boolean
  transitionPolicy: TransitionPolicy
  transitionReason: string
  transitionRoute: RouteSegment[]
  approval?: Approval
  sourceDraft?: string
  sourceFinalId?: string
  tags: string[]
  updatedAt?: string
}

export type WorkbenchCatalogue = {
  version: number
  platformId: string
  title: string
  updatedOn: string
  separateFrom: string
  lanes: { final: WorkbenchItem[]; draft: WorkbenchItem[] }
  assets: SpriteAsset[]
  principles: Record<string, string>
  storage: Record<string, string>
  featureContract: Record<string, unknown>
}

export type PlaybackFrame = {
  key: string
  assetId: string
  frame: number
  fps: number
  label: string
  mirror: boolean
  sourceEntryId?: string
}

export type LoopRange = SectionLoop & { start: number; end: number }

export function resolvedLoops(timeline: TimelineEntry[], loops: SectionLoop[]): LoopRange[] {
  return loops.flatMap((loop) => {
    const a = timeline.findIndex((entry) => entry.id === loop.startId)
    const b = timeline.findIndex((entry) => entry.id === loop.endId)
    if (a < 0 || b < 0 || loop.repeats < 2) return []
    return [{ ...loop, start: Math.min(a, b), end: Math.max(a, b), repeats: Math.max(2, Math.round(loop.repeats)) }]
  }).sort((left, right) => left.start - right.start || left.end - right.end)
}

export function loopConflicts(timeline: TimelineEntry[], loops: SectionLoop[]) {
  const ranges = resolvedLoops(timeline, loops)
  return ranges.flatMap((range, index) => ranges.slice(index + 1).flatMap((other) => (
    other.start <= range.end ? [`${range.id}:${other.id}`] : []
  )))
}

export function expandTimeline(timeline: TimelineEntry[], loops: SectionLoop[]) {
  if (!timeline.length) return []
  const ranges = resolvedLoops(timeline, loops)
  const conflicts = new Set(loopConflicts(timeline, loops).flatMap((pair) => pair.split(':')))
  const byStart = new Map(ranges.filter((range) => !conflicts.has(range.id)).map((range) => [range.start, range]))
  const expanded: TimelineEntry[] = []
  for (let index = 0; index < timeline.length;) {
    const loop = byStart.get(index)
    if (!loop) {
      expanded.push(timeline[index])
      index += 1
      continue
    }
    const section = timeline.slice(loop.start, loop.end + 1)
    for (let repeat = 0; repeat < loop.repeats; repeat += 1) expanded.push(...section)
    index = loop.end + 1
  }
  return expanded
}

export function copyTimelineEntry(item: WorkbenchItem, entryId: string, newId: string): WorkbenchItem {
  const index = item.timeline.findIndex((entry) => entry.id === entryId)
  if (index < 0) return item
  const original = item.timeline[index]
  return { ...item, timeline: [...item.timeline.slice(0, index + 1), { ...original, id: newId }, ...item.timeline.slice(index + 1)] }
}

export function removeTimelineEntry(item: WorkbenchItem, entryId: string): WorkbenchItem {
  if (item.timeline.length <= 1) return item
  return {
    ...item,
    timeline: item.timeline.filter((entry) => entry.id !== entryId),
    sectionLoops: item.sectionLoops.filter((loop) => loop.startId !== entryId && loop.endId !== entryId),
  }
}

export function moveTimelineEntry(item: WorkbenchItem, entryId: string, direction: -1 | 1): WorkbenchItem {
  const index = item.timeline.findIndex((entry) => entry.id === entryId)
  const target = index + direction
  if (index < 0 || target < 0 || target >= item.timeline.length) return item
  const timeline = [...item.timeline]
  ;[timeline[index], timeline[target]] = [timeline[target], timeline[index]]
  return { ...item, timeline }
}

export function copyToDraft(item: WorkbenchItem, id: string, timestamp: string): WorkbenchItem {
  return {
    ...item,
    id,
    lane: 'draft',
    title: `${item.title} — working copy`,
    approval: undefined,
    sourceFinalId: item.id,
    timeline: item.timeline.map((entry, index) => ({ ...entry, id: `${id}-frame-${index + 1}` })),
    sectionLoops: [],
    overallLoop: true,
    updatedAt: timestamp,
    tags: [...new Set([...item.tags, 'working-copy'])],
  }
}

function mirroredPose(pose: string | undefined, mirror: boolean) {
  if (!pose || !mirror) return pose
  return pose.replace('side-right', 'SIDE').replace('side-left', 'side-right').replace('SIDE', 'side-left')
}

export function transitionWarnings(item: WorkbenchItem, assets: Map<string, SpriteAsset>) {
  if (item.transitionPolicy === 'door-hidden') return []
  const warnings: string[] = []
  for (let index = 0; index < item.transitionRoute.length - 1; index += 1) {
    const current = item.transitionRoute[index]
    const next = item.transitionRoute[index + 1]
    const a = assets.get(current.assetId)
    const b = assets.get(next.assetId)
    if (!a || !b) {
      warnings.push(`Missing route asset between ${current.label} and ${next.label}.`)
      continue
    }
    const from = mirroredPose(a.endPose, current.mirror)
    const to = mirroredPose(b.startPose, next.mirror)
    if (from && to && from !== to) warnings.push(`${current.label} ends ${from}; ${next.label} starts ${to}.`)
    if (a.outfit && b.outfit && a.outfit !== b.outfit) warnings.push(`${current.label} uses ${a.outfit}; ${next.label} uses ${b.outfit}.`)
  }
  return warnings
}

export function itemPlayback(item: WorkbenchItem, asset: SpriteAsset): PlaybackFrame[] {
  return expandTimeline(item.timeline, item.sectionLoops).map((entry, index) => ({
    key: `${entry.id}-${index}`,
    assetId: asset.id,
    frame: Math.max(0, Math.min(asset.frames - 1, entry.frame)),
    fps: asset.fps || 4,
    label: item.title,
    mirror: false,
    sourceEntryId: entry.id,
  }))
}

export function transitionPlayback(item: WorkbenchItem, assets: Map<string, SpriteAsset>): PlaybackFrame[] {
  if (item.transitionPolicy === 'door-hidden') return []
  const expandedItem = expandTimeline(item.timeline, item.sectionLoops)
  return item.transitionRoute.flatMap((segment) => {
    const asset = assets.get(segment.assetId)
    if (!asset) return []
    const frames = segment.assetId === item.assetId ? expandedItem.map((entry) => entry.frame) : segment.frames
    return Array.from({ length: Math.max(1, segment.repeats) }, (_, repeat) => frames.map((frame, index) => ({
      key: `${segment.id}-${repeat}-${index}`,
      assetId: asset.id,
      frame: Math.max(0, Math.min(asset.frames - 1, frame)),
      fps: segment.fps || asset.fps || 4,
      label: segment.label,
      mirror: segment.mirror,
    }))).flat()
  })
}

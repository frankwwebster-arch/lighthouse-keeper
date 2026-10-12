import { describe, expect, it } from 'vitest'
import { copyTimelineEntry, copyToDraft, expandTimeline, loopConflicts, moveTimelineEntry, removeTimelineEntry, transitionPlayback, transitionWarnings, type SpriteAsset, type WorkbenchItem } from './model'

const item: WorkbenchItem = {
  id: 'final', lane: 'final', name: 'turn', title: 'Turn', description: '', assetId: 'turn',
  timeline: [0, 1, 2, 3].map((frame) => ({ id: `f${frame}`, frame })), sectionLoops: [], overallLoop: false,
  transitionPolicy: 'required', transitionReason: '', tags: [],
  transitionRoute: [
    { id: 'walk', role: 'walk', label: 'Walk (runtime length)', assetId: 'walk', frames: [0, 1], repeats: 1, mirror: false, distanceMode: 'runtime-placement', entryOcclusion: 'door-left' },
    { id: 'stop', role: 'stop', label: 'Stop', assetId: 'walk', frames: [1], repeats: 1, mirror: false },
    { id: 'turn', role: 'action', label: 'Action: turn', assetId: 'turn', frames: [0, 1, 2, 3], repeats: 1, mirror: false },
  ],
}

const assets = new Map<string, SpriteAsset>([
  ['walk', { id: 'walk', name: 'walk', file: '', sha256: '', w: 32, h: 40, frames: 2, fps: 8, density: 4, anchor: [16, 40], startPose: 'standing-side-right', endPose: 'standing-side-right', outfit: 'standard', loop: true, mirrorSafe: true, source: '', immutable: true }],
  ['turn', { id: 'turn', name: 'turn', file: '', sha256: '', w: 32, h: 40, frames: 4, fps: 4, density: 4, anchor: [16, 40], startPose: 'standing-side-right', endPose: 'standing-front', outfit: 'standard', loop: false, mirrorSafe: false, source: '', immutable: true }],
])

describe('animation workbench timeline', () => {
  it('copies, moves and removes frame references without touching source frames', () => {
    const copied = copyTimelineEntry(item, 'f1', 'copy')
    expect(copied.timeline.map((entry) => entry.frame)).toEqual([0, 1, 1, 2, 3])
    const moved = moveTimelineEntry(copied, 'copy', 1)
    expect(moved.timeline.map((entry) => entry.id)).toEqual(['f0', 'f1', 'f2', 'copy', 'f3'])
    expect(removeTimelineEntry(moved, 'copy').timeline.map((entry) => entry.frame)).toEqual([0, 1, 2, 3])
  })

  it('expands a selected section for an exact number of passes', () => {
    const loop = { id: 'loop', startId: 'f1', endId: 'f2', repeats: 3 }
    expect(expandTimeline(item.timeline, [loop]).map((entry) => entry.frame)).toEqual([0, 1, 2, 1, 2, 1, 2, 3])
    expect(loopConflicts(item.timeline, [loop])).toEqual([])
  })

  it('keeps overlapping section loops fail-closed', () => {
    const loops = [
      { id: 'a', startId: 'f0', endId: 'f2', repeats: 2 },
      { id: 'b', startId: 'f1', endId: 'f3', repeats: 2 },
    ]
    expect(loopConflicts(item.timeline, loops)).toEqual(['a:b'])
    expect(expandTimeline(item.timeline, loops).map((entry) => entry.frame)).toEqual([0, 1, 2, 3])
  })

  it('copies Final into an editable Draft without carrying approval', () => {
    const draft = copyToDraft({ ...item, approval: { approvedBy: 'Frank', approvedOn: '2026-10-12', wording: 'Approved', scope: 'Final' } }, 'draft-1', 'now')
    expect(draft.lane).toBe('draft')
    expect(draft.sourceFinalId).toBe('final')
    expect(draft.approval).toBeUndefined()
    expect(draft.timeline).not.toBe(item.timeline)
  })

  it('compiles repeated route segments and checks pose seams', () => {
    expect(transitionPlayback(item, assets)).toHaveLength(7)
    expect(transitionPlayback(item, assets)[0]).toMatchObject({ role: 'walk', entryOcclusion: 'door-left', travelProgress: 0 })
    expect(transitionPlayback(item, assets)[1]).toMatchObject({ role: 'walk', travelProgress: 1 })
    expect(transitionWarnings(item, assets)).toEqual([])
    const broken = { ...item, transitionRoute: [...item.transitionRoute, { id: 'walk2', role: 'walk' as const, label: 'Walk again', assetId: 'walk', frames: [0], repeats: 1, mirror: false }] }
    expect(transitionWarnings(broken, assets)).toEqual(['Action: turn ends standing-front; Walk again starts standing-side-right.'])
  })
})

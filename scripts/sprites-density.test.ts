import { execFileSync, spawnSync } from 'node:child_process'
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { PNG } from 'pngjs'
import { expect, test } from 'vitest'

function workspace() {
  const dir = mkdtempSync(join(tmpdir(), 'keeper-sprite-density-'))
  const raw = join(dir, 'raw'), out = join(dir, 'out')
  mkdirSync(raw)
  return { dir, raw, out, env: { ...process.env, SPRITES_RAW: raw, SPRITES_OUT: out } }
}
function png(w: number, h: number) {
  const p = new PNG({ width: w, height: h })
  // Nonuniform detail verifies the pipeline retains source resolution.
  for (let i = 0; i < p.data.length; i += 4) {
    p.data[i] = (i / 4) % 2 ? 30 : 180
    p.data[i + 1] = 80; p.data[i + 2] = 110; p.data[i + 3] = 255
  }
  return PNG.sync.write(p)
}

test('detailed strips retain source pixels and logical footprints alongside legacy rooms', () => {
  const w = workspace()
  try {
    writeFileSync(join(w.raw, 'obj_tv_on_f4.png'), png(448, 92))
    writeFileSync(join(w.raw, 'obj_tv_on_f4.json'), JSON.stringify({ density: 4, w: 28, h: 23, frames: 4, fps: 8, anchor: [14, 23], keeperUsePoint: [14, 0] }))
    writeFileSync(join(w.raw, 'room_test.png'), png(105, 35))
    execFileSync(process.execPath, ['scripts/sprites.ts'], { env: w.env })
    const manifest = JSON.parse(readFileSync(join(w.out, 'manifest.json'), 'utf8'))
    expect(manifest.obj_tv_on).toMatchObject({ density: 4, w: 28, h: 23, frames: 4, fps: 8, anchor: [14, 23] })
    const detail = PNG.sync.read(readFileSync(join(w.out, 'obj_tv_on.png')))
    expect([detail.width, detail.height]).toEqual([448, 92])
    expect(detail.data[0]).not.toBe(detail.data[4])
    expect(manifest.room_test).toMatchObject({ w: 105, h: 35, frames: 1 })
    const first = readFileSync(join(w.out, 'obj_tv_on.png'))
    execFileSync(process.execPath, ['scripts/sprites.ts'], { env: w.env })
    expect(readFileSync(join(w.out, 'obj_tv_on.png'))).toEqual(first)
  } finally { rmSync(w.dir, { recursive: true, force: true }) }
})

test('invalid density contract fails before deleting previous usable exports', () => {
  const w = workspace()
  try {
    mkdirSync(w.out)
    writeFileSync(join(w.out, 'keep.png'), png(1, 1))
    const original = JSON.stringify({ keep: { file: 'keep.png' } })
    writeFileSync(join(w.out, 'manifest.json'), original)
    writeFileSync(join(w.raw, 'obj_tv_on_f4.png'), png(112, 92))
    writeFileSync(join(w.raw, 'obj_tv_on_f4.json'), JSON.stringify({ density: 4, w: 28, h: 23, frames: 4, fps: 8 }))
    const result = spawnSync(process.execPath, ['scripts/sprites.ts'], { env: w.env, encoding: 'utf8' })
    expect(result.status).not.toBe(0)
    expect(result.stderr).toContain('Invalid density/frame contract')
    expect(readFileSync(join(w.out, 'manifest.json'), 'utf8')).toBe(original)
    expect(PNG.sync.read(readFileSync(join(w.out, 'keep.png'))).width).toBe(1)
  } finally { rmSync(w.dir, { recursive: true, force: true }) }
})

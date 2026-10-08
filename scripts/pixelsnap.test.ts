import { describe, expect, it } from 'vitest'
import { bbox, blank, detectScale, parseName, pivotFor, snap, type Img } from './pixelsnap.ts'

type RGBA = [number, number, number, number]
const RED: RGBA = [200, 40, 40, 255]
const BLUE: RGBA = [40, 60, 200, 255]
const CLEAR: RGBA = [0, 0, 0, 0]
const MAGENTA: RGBA = [255, 0, 255, 255]

/** A small picture from rows of letters. */
function art(rows: string[], key: Record<string, RGBA>): Img {
  const img = blank(rows[0].length, rows.length)
  rows.forEach((r, y) => [...r].forEach((ch, x) => img.data.set(key[ch], (y * img.w + x) * 4)))
  return img
}

/** Blow each pixel up into an s × s block. */
function upscale(img: Img, s: number): Img {
  const out = blank(img.w * s, img.h * s)
  for (let y = 0; y < out.h; y++)
    for (let x = 0; x < out.w; x++) {
      const i = (Math.floor(y / s) * img.w + Math.floor(x / s)) * 4
      out.data.set(img.data.subarray(i, i + 4), (y * out.w + x) * 4)
    }
  return out
}

const KEY = { r: RED, b: BLUE, '.': CLEAR, m: MAGENTA }
const tiny = art(['..rr..', '.rbbr.', 'rbbbbr', '.r..r.', '.r..r.'], KEY)
const same = (a: Img, b: Img) => a.w === b.w && a.h === b.h && a.data.every((v, i) => v === b.data[i])

describe('pixel snap', () => {
  it('reads names and frame counts', () => {
    expect(parseName('obj_tv_on_f4.png')).toEqual({ name: 'obj_tv_on', frames: 4 })
    expect(parseName('Keeper_Front_Torso.PNG')).toEqual({ name: 'keeper_front_torso', frames: 1 })
  })

  it('finds the block size of clean upscaled art and shrinks it back exactly', () => {
    for (const s of [2, 4, 7]) {
      const big = upscale(tiny, s)
      expect(detectScale(big).scale).toBe(s)
      expect(same(snap('thing.png', big).img, tiny)).toBe(true)
    }
  })

  it('leaves true 1x art alone', () => {
    const r = snap('thing.png', art(['..rr..', '.rbbr.', 'rbbbbr', '.r..r.', '.r..r.'], KEY))
    expect(r.scale).toBe(1)
    expect(same(r.img, tiny)).toBe(true)
  })

  it('removes a magenta background', () => {
    const r = snap('thing.png', art(['mmrrmm', 'mrbbrm', 'rbbbbr', 'mrmmrm', 'mrmmrm'], KEY))
    expect(same(r.img, tiny)).toBe(true)
  })

  it('copes with soft edges by trusting the brief size', () => {
    const big = upscale(tiny, 4)
    // smear every block edge with an in-between colour
    for (let y = 0; y < big.h; y++)
      for (let x = 0; x < big.w; x++) if (x % 4 === 0 && (x + y) % 3 === 0) big.data.set([120, 50, 120, 255], (y * big.w + x) * 4)
    const g = detectScale(big, { h: 5 })
    expect(g.scale).toBe(4)
  })

  it('uses the asset kit joints for keeper parts and none for anything else', () => {
    expect(pivotFor('keeper_front_arm_l')).toEqual([10, 15])
    expect(pivotFor('keeper_back_leg_r')).toEqual([19, 25])
    expect(pivotFor('keeper_front_head_happy')).toEqual([16, 11])
    expect(pivotFor('keeper_back_head')).toEqual([16, 11])
    expect(pivotFor('keeper_walk')).toBeUndefined()
    expect(pivotFor('obj_tv_on')).toBeUndefined()
    expect(bbox(blank(3, 3))).toBeNull()
    expect(bbox(art(['...', '.r.'], KEY))).toEqual({ x: 1, y: 1, w: 1, h: 1 })
  })

  it('gives strips their frame rate', () => {
    expect(snap('keeper_walk_f8.png', blank(256, 40)).fps).toBe(10)
    expect(snap('obj_tv_on_f4.png', blank(112, 23)).fps).toBe(8)
    expect(snap('obj_tv_standard_f1.png', blank(28, 23)).fps).toBe(0)
  })

  it('splits a strip into frames and warns when it does not divide', () => {
    const strip = art(['rrbbrrb', 'rrbbrrb'], KEY)
    expect(snap('obj_x_on_f2.png', strip).warnings.join()).toMatch(/equal frames/)
    const ok = snap('obj_x_on_f2.png', art(['rrbbrrbb', 'rrbbrrbb'], KEY))
    expect(ok.frameW).toBe(4)
    expect(ok.warnings).toEqual([])
  })

  it('checks keeper parts against the 32 × 40 canvas', () => {
    const wrong = snap('keeper_front_torso.png', blank(30, 40))
    expect(wrong.warnings.join()).toMatch(/width 30, brief says 32/)
  })
})

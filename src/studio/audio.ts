/**
 * The recipe studio's sound: plays a timeline's cues in step with the
 * picture, each trimmed, delayed and looped as the recipe says. A cue whose
 * sound has no file yet plays a short placeholder blip (its own pitch per
 * name), so timing can be judged before the real sound exists.
 */

import type { TimedCue } from './recipe'

const PLACEHOLDER = { length: 0.12, every: 0.6 }

/** A pitch from a name, so each placeholder sounds different and stays the same. */
const pitchOf = (name: string) => {
  let h = 0
  for (const c of name) h = (h * 31 + c.charCodeAt(0)) >>> 0
  return 330 + (h % 12) * 55
}

export class Mixer {
  private ctx: AudioContext | null = null
  private buffers = new Map<string, Promise<AudioBuffer | null>>()
  private live: AudioScheduledSourceNode[] = []

  private audio(): AudioContext {
    if (!this.ctx) this.ctx = new AudioContext()
    if (this.ctx.state === 'suspended') void this.ctx.resume()
    return this.ctx
  }

  /** Fetch and decode a sound once (cached by its address). */
  load(url: string): Promise<AudioBuffer | null> {
    let p = this.buffers.get(url)
    if (!p) {
      p = fetch(url)
        .then((r) => (r.ok ? r.arrayBuffer() : Promise.reject(new Error(String(r.status)))))
        .then((b) => this.audio().decodeAudioData(b))
        .catch(() => null)
      this.buffers.set(url, p)
    }
    return p
  }

  stop(): void {
    for (const s of this.live) {
      try {
        s.stop()
      } catch {
        // already finished
      }
    }
    this.live = []
  }

  /** Play every cue from timeline time `from` (seconds), as if the picture started there now. */
  async play(cues: readonly TimedCue[], from: number, urlOf: (sound: string) => string | undefined): Promise<void> {
    const ctx = this.audio()
    const buffers = await Promise.all(cues.map((c) => (urlOf(c.sound) ? this.load(urlOf(c.sound)!) : Promise.resolve(null))))
    const now = ctx.currentTime + 0.02
    cues.forEach((c, i) => {
      const b = buffers[i]
      if (b) this.clip(ctx, b, c, from, now)
      else this.placeholder(ctx, c, from, now)
    })
  }

  private clip(ctx: AudioContext, b: AudioBuffer, c: TimedCue, from: number, now: number) {
    const start = Math.min(Math.max(0, c.trimStart), b.duration)
    const end = Math.min(b.duration, c.trimEnd ?? b.duration)
    const len = end - start
    if (len <= 0.005) return
    const stopAt = c.loop ? (c.until ?? c.time + len) : c.time + len
    if (from >= stopAt) return
    const late = Math.max(0, from - c.time)
    const src = ctx.createBufferSource()
    src.buffer = b
    const gain = ctx.createGain()
    gain.gain.value = Math.max(0, Math.min(1.5, c.volume))
    src.connect(gain).connect(ctx.destination)
    const when = now + Math.max(0, c.time - from)
    if (c.loop) {
      src.loop = true
      src.loopStart = start
      src.loopEnd = end
      src.start(when, start + (late % len))
    } else {
      src.start(when, start + late, len - late)
    }
    src.stop(now + (stopAt - from))
    this.live.push(src)
  }

  private placeholder(ctx: AudioContext, c: TimedCue, from: number, now: number) {
    const times = c.loop && c.until !== null ? Array.from({ length: Math.max(1, Math.ceil((c.until - c.time) / PLACEHOLDER.every)) }, (_, k) => c.time + k * PLACEHOLDER.every) : [c.time]
    for (const t of times) {
      if (t < from || (c.until !== null && t >= c.until)) continue
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()
      osc.frequency.value = pitchOf(c.sound)
      osc.type = 'triangle'
      const when = now + (t - from)
      gain.gain.setValueAtTime(0.0001, when)
      gain.gain.exponentialRampToValueAtTime(0.25 * Math.max(0.05, c.volume), when + 0.01)
      gain.gain.exponentialRampToValueAtTime(0.0001, when + PLACEHOLDER.length)
      osc.connect(gain).connect(ctx.destination)
      osc.start(when)
      osc.stop(when + PLACEHOLDER.length + 0.02)
      this.live.push(osc)
    }
  }

  /** Hear one cue on its own, trimmed as set. */
  async preview(c: Pick<TimedCue, 'sound' | 'trimStart' | 'trimEnd' | 'volume' | 'loop'>, url: string | undefined): Promise<void> {
    this.stop()
    await this.play([{ ...c, id: 'preview', at: 0, stepId: '', time: 0, until: c.loop ? 3 : null }], 0, () => url)
  }
}

/** Loudness peaks for drawing a waveform: `n` values from 0 to 1. */
export function peaksOf(b: AudioBuffer, n: number): number[] {
  const data = b.getChannelData(0)
  const per = Math.max(1, Math.floor(data.length / n))
  const out: number[] = []
  for (let i = 0; i < n; i++) {
    let m = 0
    for (let j = i * per; j < Math.min(data.length, (i + 1) * per); j++) m = Math.max(m, Math.abs(data[j]))
    out.push(m)
  }
  return out
}

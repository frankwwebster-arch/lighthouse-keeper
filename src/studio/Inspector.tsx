import type { ReactNode } from 'react'
import type { Mixer } from './audio'
import { isFront, isSolid, newCue, newId, withStep, type Cue, type Recipe, type StageObject, type Step, type StepKind, type Target } from './recipe'
import { Waveform } from './SoundLibrary'
import type { Sel } from './StageView'

const TARGETS: { v: Target; label: string }[] = [
  { v: 'action', label: 'the action point' },
  { v: 'doorIn', label: 'inside the door' },
  { v: 'doorOut', label: 'outside the door (stairway)' },
  { v: 'stairs', label: 'the stairs' },
  { v: 'innerIn', label: 'inside the inner door' },
  { v: 'innerOut', label: 'beyond the inner door' },
]
export const KIND_LABEL: Record<StepKind, string> = { walk: 'Walk', play: 'Play once', loop: 'Loop', hide: 'Through a doorway (hidden)', wait: 'Stand still', macro: 'Macro' }

const Row = ({ label, children, hint }: { label: string; children: ReactNode; hint?: string }) => (
  <label className="st-row">
    <span>{label}{hint && <small> {hint}</small>}</span>
    {children}
  </label>
)
function Num({ value, onChange, step = 1, min, max, disabled }: { value: number; onChange: (n: number) => void; step?: number; min?: number; max?: number; disabled?: boolean }) {
  const clamp = (n: number) => Math.min(max ?? Infinity, Math.max(min ?? -Infinity, n))
  return (
    <span className="st-num">
      <button type="button" className="st-mini" disabled={disabled} onClick={() => onChange(clamp(Math.round((value - step) * 100) / 100))}>−</button>
      <input type="number" step={step} value={value} disabled={disabled} onChange={(e) => e.target.value !== '' && onChange(clamp(Number(e.target.value)))} />
      <button type="button" className="st-mini" disabled={disabled} onClick={() => onChange(clamp(Math.round((value + step) * 100) / 100))}>+</button>
    </span>
  )
}

/** Everything about whatever is selected: the recipe, a step, a sound cue or an object. */
export function Inspector({ doc, sel, macros, clips, outfits, sounds, mixer, editable, onChange, onSelect, onOpenMacro }: {
  doc: Recipe
  sel: Sel | null
  macros: Recipe[]
  clips: string[]
  outfits: string[]
  sounds: { id: string; url?: string }[]
  mixer: Mixer
  editable: boolean
  onChange: (doc: Recipe) => void
  onSelect: (s: Sel | null) => void
  onOpenMacro: (id: string) => void
}) {
  const ro = !editable
  const stepId = sel?.type === 'step' ? sel.id : sel?.type === 'cue' ? sel.stepId : undefined
  const step = stepId ? doc.steps.find((s) => s.id === stepId) : undefined
  const setStep = (patch: Partial<Step>) => step && onChange(withStep(doc, step.id, (s) => ({ ...s, ...patch })))
  const clipField = (value: string | undefined, set: (v: string | undefined) => void, optional = false) => (
    <input list="st-clips" value={value ?? ''} placeholder={optional ? '(the outfit’s own)' : 'keeper_…'} disabled={ro} onChange={(e) => set(e.target.value || undefined)} className={value && !clips.includes(value) ? 'st-bad' : ''} />
  )
  const outfitSelect = (value: string, set: (v: string) => void, extra: { v: string; label: string }[] = []) => (
    <select value={value} disabled={ro} onChange={(e) => set(e.target.value)}>
      {extra.map((x) => <option key={x.v} value={x.v}>{x.label}</option>)}
      {outfits.map((o) => <option key={o} value={o}>{o}</option>)}
    </select>
  )

  if (sel?.type === 'cue') {
    const owner = doc.steps.find((s) => s.id === sel.stepId)
    const cue = owner?.cues?.find((c) => c.id === sel.cueId)
    if (!owner || !cue) {
      const m = owner?.kind === 'macro' ? owner.macro : undefined
      return (
        <div className="st-inspector">
          <h3>Sound cue</h3>
          {sel.cueId.startsWith('clip-') ? <p className="st-dim">This sound is marked on the animation’s own sheet (its sidecar’s sfxCues), so every recipe that uses the clip plays it. Codex changes it there. Fill its file in the sound library.</p> : <p className="st-dim">This cue belongs to a macro, so changing it changes every recipe that uses the macro.</p>}
          {m && <button type="button" onClick={() => onOpenMacro(m)}>Open the {m.replace(/_/g, ' ')} macro</button>}
        </div>
      )
    }
    const setCue = (patch: Partial<Cue>) => onChange(withStep(doc, owner.id, (s) => ({ ...s, cues: (s.cues ?? []).map((c) => (c.id === cue.id ? { ...c, ...patch } : c)) })))
    const url = sounds.find((s) => s.id === cue.sound)?.url
    return (
      <div className="st-inspector">
        <h3>Sound cue <small>in “{owner.label ?? owner.kind}”</small></h3>
        <Row label="Sound">
          <input list="st-sounds" value={cue.sound} disabled={ro} onChange={(e) => setCue({ sound: e.target.value.toLowerCase().replace(/[^a-z0-9_-]/g, '_') })} />
        </Row>
        <Row label="Starts" hint="seconds into the step"><Num value={cue.at} step={0.05} min={0} onChange={(at) => setCue({ at })} disabled={ro} /></Row>
        <Waveform url={url} mixer={mixer} trimStart={cue.trimStart} trimEnd={cue.trimEnd} onTrim={(trimStart, trimEnd) => !ro && setCue({ trimStart, trimEnd })} />
        <Row label="Trim start" hint="s"><Num value={cue.trimStart} step={0.01} min={0} onChange={(trimStart) => setCue({ trimStart })} disabled={ro} /></Row>
        <Row label="Trim end" hint={cue.trimEnd === null ? '(the end)' : 's'}>
          <Num value={cue.trimEnd ?? 0} step={0.01} min={0} onChange={(v) => setCue({ trimEnd: v > 0 ? v : null })} disabled={ro} />
        </Row>
        <Row label="Volume"><span className="st-inline"><input type="range" min={0} max={1.5} step={0.05} value={cue.volume} disabled={ro} onChange={(e) => setCue({ volume: Number(e.target.value) })} /><b>{Math.round(cue.volume * 100)}%</b></span></Row>
        <Row label="Repeat until the step ends"><input type="checkbox" checked={cue.loop} disabled={ro} onChange={(e) => setCue({ loop: e.target.checked })} /></Row>
        <div className="st-buttons">
          <button type="button" onClick={() => void mixer.preview(cue, url)}>▶ Hear it</button>
          {editable && <button type="button" onClick={() => { onChange(withStep(doc, owner.id, (s) => ({ ...s, cues: (s.cues ?? []).filter((c) => c.id !== cue.id) }))); onSelect({ type: 'step', id: owner.id }) }}>Remove cue</button>}
        </div>
      </div>
    )
  }

  if (sel?.type === 'object') {
    const o = doc.objects.find((x) => x.id === sel.id)
    if (!o) return null
    const setObj = (patch: Partial<StageObject>) => onChange({ ...doc, objects: doc.objects.map((x) => (x.id === o.id ? { ...x, ...patch } : x)) })
    return (
      <div className="st-inspector">
        <h3>Object: {o.label}</h3>
        <Row label="Name"><input value={o.label} disabled={ro} onChange={(e) => setObj({ label: e.target.value })} /></Row>
        <Row label="Across" hint="px from the left wall (bottom-centre)"><Num value={o.x} onChange={(x) => setObj({ x })} disabled={ro} /></Row>
        <Row label="Width"><Num value={o.w} min={1} onChange={(w) => setObj({ w })} disabled={ro} /></Row>
        <Row label="Height"><Num value={o.h} min={1} onChange={(h) => setObj({ h })} disabled={ro} /></Row>
        <Row label="Where it sits">
          <select value={o.layer ?? 'back'} disabled={ro} onChange={(e) => setObj({ layer: e.target.value as 'back' | 'front' })}>
            <option value="back">Against the back wall: he passes in front</option>
            <option value="front">Side wall or nearer the camera: in front of him, opaque</option>
          </select>
        </Row>
        <Row label="Solid" hint={isFront(o) ? '(always, in front)' : '(he cannot walk through it)'}><input type="checkbox" checked={isSolid(o)} disabled={ro || isFront(o)} onChange={(e) => setObj({ solid: e.target.checked })} /></Row>
        <Row label="Sprite" hint="(placeholder box until it exists)"><input value={o.sprite ?? ''} placeholder="e.g. armchair" disabled={ro} onChange={(e) => setObj({ sprite: e.target.value || undefined })} /></Row>
        <Row label="Contact heights" hint="label=px, comma separated">
          <input value={(o.marks ?? []).map((m) => `${m.label}=${m.y}`).join(', ')} disabled={ro} onChange={(e) => setObj({ marks: e.target.value.split(',').map((p) => p.split('=')).filter((p) => p.length === 2 && p[0].trim() && Number.isFinite(Number(p[1]))).map(([label, y]) => ({ label: label.trim(), y: Number(y) })) })} />
        </Row>
        {editable && (
          <div className="st-buttons">
            <button type="button" disabled={doc.action.object === o.id} onClick={() => onChange({ ...doc, action: { ...doc.action, object: o.id, dx: 0 } })}>{doc.action.object === o.id ? 'He uses this one' : 'Make this the one he uses'}</button>
            <button type="button" onClick={() => { onChange({ ...doc, objects: doc.objects.filter((x) => x.id !== o.id) }); onSelect(null) }}>Remove object</button>
          </div>
        )}
      </div>
    )
  }

  if (sel?.type === 'step' && step) {
    const kind = step.kind
    return (
      <div className="st-inspector">
        <h3>{KIND_LABEL[kind]}{step.main ? ' · the activity' : ''}</h3>
        <Row label="Label"><input value={step.label ?? ''} disabled={ro} onChange={(e) => setStep({ label: e.target.value })} /></Row>
        {kind === 'macro' && (
          <>
            <Row label="Macro">
              <select value={step.macro ?? ''} disabled={ro} onChange={(e) => setStep({ macro: e.target.value })}>
                {macros.map((m) => <option key={m.id} value={m.id}>{m.title}</option>)}
              </select>
            </Row>
            <Row label="Changes into" hint="(while hidden in its doorway)">{outfitSelect(step.params?.swapTo ?? '', (v) => setStep({ params: { ...step.params, swapTo: v } }), [{ v: '', label: '(keeps his outfit)' }])}</Row>
            {step.macro && <button type="button" onClick={() => onOpenMacro(step.macro!)}>Open this macro</button>}
          </>
        )}
        {kind === 'walk' && (
          <>
            <Row label="To">
              <select value={typeof step.to === 'number' ? 'x' : step.to ?? 'action'} disabled={ro} onChange={(e) => setStep({ to: e.target.value === 'x' ? 55 : (e.target.value as Target) })}>
                {TARGETS.map((x) => <option key={String(x.v)} value={String(x.v)}>{x.label}</option>)}
                <option value="x">a spot I choose</option>
              </select>
            </Row>
            {typeof step.to === 'number' && <Row label="Spot" hint="px"><Num value={step.to} onChange={(to) => setStep({ to })} disabled={ro} /></Row>}
            <Row label="Speed" hint={`px a second (recipe: ${doc.walkSpeed})`}><Num value={step.speed ?? doc.walkSpeed} min={1} onChange={(speed) => setStep({ speed })} disabled={ro} /></Row>
            <Row label="Walk clip">{clipField(step.clip, (clip) => setStep({ clip }), true)}</Row>
          </>
        )}
        {(kind === 'play' || kind === 'loop' || kind === 'wait') && (
          <>
            <Row label="Clip">{clipField(step.clip, (clip) => setStep({ clip }), kind === 'wait')}</Row>
            {kind === 'play' && <Row label="Backwards" hint="(stand up = sit down reversed)"><input type="checkbox" checked={!!step.reverse} disabled={ro} onChange={(e) => setStep({ reverse: e.target.checked })} /></Row>}
            {kind !== 'play' && <Row label={step.untilStopped ? 'Preview length' : 'How long'} hint="seconds"><Num value={step.seconds ?? 2} step={0.5} min={0} onChange={(seconds) => setStep({ seconds })} disabled={ro} /></Row>}
            <Row label="Faces">
              <select value={step.facing ?? 'auto'} disabled={ro} onChange={(e) => setStep({ facing: e.target.value as Step['facing'] })}>
                <option value="auto">as he was</option>
                <option value="right">right</option>
                <option value="left">left</option>
              </select>
            </Row>
            <Row label="Nudge across" hint="px (← → keys)"><Num value={step.dx ?? 0} onChange={(dx) => setStep({ dx })} disabled={ro} /></Row>
            <Row label="Nudge up" hint="px (↑ ↓ keys)"><Num value={step.dy ?? 0} onChange={(dy) => setStep({ dy })} disabled={ro} /></Row>
            {kind === 'loop' && (
              <>
                <Row label="This is the activity" hint="(Stop now ends it)"><input type="checkbox" checked={!!step.main} disabled={ro} onChange={(e) => onChange({ ...doc, steps: doc.steps.map((s) => ({ ...s, main: s.id === step.id ? e.target.checked : e.target.checked ? false : s.main })) })} /></Row>
                {step.main && <Row label="Runs until the player stops it"><input type="checkbox" checked={!!step.untilStopped} disabled={ro} onChange={(e) => setStep({ untilStopped: e.target.checked })} /></Row>}
              </>
            )}
          </>
        )}
        {kind === 'hide' && (
          <>
            <Row label="Through"><select value={step.through ?? 'door'} disabled={ro} onChange={(e) => setStep({ through: e.target.value as 'door' | 'inner' })}><option value="door">the door</option><option value="inner">the inner door</option></select></Row>
            <Row label="How long hidden" hint="seconds"><Num value={step.seconds ?? 0.6} step={0.1} min={0.1} onChange={(seconds) => setStep({ seconds })} disabled={ro} /></Row>
            <Row label="Comes out in">{outfitSelect(step.swapTo ?? '', (v) => setStep({ swapTo: v }), [{ v: '', label: '(the same outfit)' }, ...(doc.kind === 'macro' ? [{ v: '$swapTo', label: '(whatever the recipe asks)' }] : [])])}</Row>
          </>
        )}
        {(kind === 'play' || kind === 'hide' || kind === 'wait') && (
          <Row label="Then the door">
            <select value={step.doorAfter ?? ''} disabled={ro} onChange={(e) => setStep({ doorAfter: (e.target.value || undefined) as Step['doorAfter'] })}>
              <option value="">stays as it is</option>
              <option value="open">opens</option>
              <option value="close">closes</option>
            </select>
          </Row>
        )}
        <p className="st-dim">Sounds: drag one from the library onto the timeline. {(step.cues ?? []).length ? `${step.cues!.length} on this step.` : ''}</p>
        {editable && (
          <div className="st-buttons">
            <button type="button" onClick={() => setStep({ cues: [...(step.cues ?? []), newCue('new_sound', 0)] })}>Add a placeholder sound</button>
            <button type="button" onClick={() => { onChange({ ...doc, steps: doc.steps.filter((s) => s.id !== step.id) }); onSelect(null) }}>Remove step</button>
          </div>
        )}
      </div>
    )
  }

  // The recipe itself.
  const set = (patch: Partial<Recipe>) => onChange({ ...doc, ...patch })
  return (
    <div className="st-inspector">
      <h3>{doc.kind === 'macro' ? 'Macro' : 'Recipe'}</h3>
      <Row label="Title"><input value={doc.title} disabled={ro} onChange={(e) => set({ title: e.target.value })} /></Row>
      <Row label="Notes"><textarea rows={3} value={doc.notes} disabled={ro} onChange={(e) => set({ notes: e.target.value })} /></Row>
      {doc.kind === 'recipe' && <Row label="Game activity" hint="(interaction id)"><input value={doc.activity ?? ''} disabled={ro} onChange={(e) => set({ activity: e.target.value || undefined })} /></Row>}
      <Row label="Starts in">{outfitSelect(doc.outfit, (outfit) => set({ outfit }))}</Row>
      <Row label="Starts at">
        <select value={typeof doc.startAt === 'number' ? 'x' : doc.startAt} disabled={ro} onChange={(e) => set({ startAt: e.target.value === 'x' ? 55 : (e.target.value as Target) })}>
          {TARGETS.map((x) => <option key={String(x.v)} value={String(x.v)}>{x.label}</option>)}
          <option value="x">a spot I choose</option>
        </select>
      </Row>
      <Row label="Facing"><select value={doc.facing} disabled={ro} onChange={(e) => set({ facing: e.target.value as Recipe['facing'] })}><option value="right">right</option><option value="left">left</option></select></Row>
      <Row label="Room"><input value={doc.room.name} disabled={ro} onChange={(e) => set({ room: { ...doc.room, name: e.target.value } })} /></Row>
      <Row label="Inner door on the right"><input type="checkbox" checked={doc.room.inner} disabled={ro} onChange={(e) => set({ room: { ...doc.room, inner: e.target.checked } })} /></Row>
      <Row label="Walking speed" hint="px a second"><Num value={doc.walkSpeed} min={1} onChange={(walkSpeed) => set({ walkSpeed })} disabled={ro} /></Row>
      {doc.kind === 'recipe' && (
        <>
          <Row label="He uses">
            <select value={doc.action.object} disabled={ro} onChange={(e) => set({ action: { ...doc.action, object: e.target.value } })}>
              {doc.objects.map((o) => <option key={o.id} value={o.id}>{o.label}</option>)}
            </select>
          </Row>
          <Row label="Action point" hint="px from its centre (drag the red diamond)"><Num value={doc.action.dx} onChange={(dx) => set({ action: { ...doc.action, dx } })} disabled={ro} /></Row>
          <Row label="Faces it"><select value={doc.action.facing} disabled={ro} onChange={(e) => set({ action: { ...doc.action, facing: e.target.value as Recipe['facing'] } })}><option value="right">right</option><option value="left">left</option></select></Row>
          {editable && <button type="button" onClick={() => set({ objects: [...doc.objects, { id: newId('obj'), label: 'New object', x: 55, w: 20, h: 20, layer: 'back' }] })}>Add an object</button>}
        </>
      )}
    </div>
  )
}

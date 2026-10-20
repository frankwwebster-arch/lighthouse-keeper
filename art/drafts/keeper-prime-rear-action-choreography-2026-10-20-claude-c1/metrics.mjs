// Shared geometry and legibility metrics for bubble choreography timelines.
// Positions are cloud-local pixels measured from the cloud centre (180, 115),
// exactly as the review pages render them: translate, then rotate, then scale.

export const OBJECT_BOX = 140;
export const SYMBOL_BOX = 92;
export const FRAMES = 42;
export const FPS = 8;
export const QUIET_START = 37;
// Inside of the bubble, as an ellipse around the cloud centre.
export const BUBBLE = { cx: 0, cy: 2.5, a: 149, b: 92.5 };
// Where the head-to-bubble connector meets the bubble (head x 182 in cloud pixels).
export const ORIGIN = { x: 2, y: 78 };
export const VISIBLE = 0.15;

// Axis-aligned bounds of an item's visible pixels after scale and rotation.
export function itemBounds(item, bbox, box) {
  const [x0, y0, x1, y1] = bbox;
  const k = (box * item.scale) / 256;
  const w = (x1 - x0 + 1) * k;
  const h = (y1 - y0 + 1) * k;
  const ox = ((x0 + x1 + 1) / 2 - 128) * k;
  const oy = ((y0 + y1 + 1) / 2 - 128) * k;
  const rad = (item.rotation * Math.PI) / 180;
  const c = Math.cos(rad);
  const s = Math.sin(rad);
  const cx = item.x + ox * c - oy * s;
  const cy = item.y + ox * s + oy * c;
  const hw = (Math.abs(c) * w + Math.abs(s) * h) / 2;
  const hh = (Math.abs(s) * w + Math.abs(c) * h) / 2;
  return { x0: cx - hw, y0: cy - hh, x1: cx + hw, y1: cy + hh, cx, cy };
}

export function overlapRatio(a, b) {
  const w = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0);
  const h = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
  if (w <= 0 || h <= 0) return 0;
  const area = (r) => (r.x1 - r.x0) * (r.y1 - r.y0);
  return (w * h) / Math.min(area(a), area(b));
}

export function insideBubble(r, margin = 1) {
  const corners = [[r.x0, r.y0], [r.x1, r.y0], [r.x0, r.y1], [r.x1, r.y1]];
  return corners.every(([x, y]) => ((x - BUBBLE.cx) / BUBBLE.a) ** 2 + ((y - BUBBLE.cy) / BUBBLE.b) ** 2 <= margin);
}

function declared(contacts, a, b, frame) {
  return (contacts || []).some((c) => c.frames[0] <= frame && frame <= c.frames[1] &&
    ((c.a === a && c.b === b) || (c.a === b && c.b === a)));
}

const round = (v, d = 3) => Math.round(v * 10 ** d) / 10 ** d;

// Measures one 42-frame timeline. `components` maps component id -> { bbox }.
export function measureTimeline(frames, components, contacts = []) {
  const result = {
    maxObjectOverlap: 0,
    maxUndeclaredOverlap: 0,
    framesWithHeavyOverlap: 0,
    objectFramesOutsideBubble: 0,
    pathLength: {},
    firstVisibleDistanceFromOrigin: {},
    symbolInstancesUsed: 0,
    symbolInstancesByComponent: {},
    maxSymbolsOnOneFrame: 0,
    tailStatic: true,
    tailSymbolsSilent: true,
  };
  const seenSymbols = new Set();
  const last = {};
  frames.forEach((frame, f) => {
    const visible = frame.objects.filter((o) => o.opacity > VISIBLE)
      .map((o) => ({ o, r: itemBounds(o, components[o.component].bbox, OBJECT_BOX) }));
    let heavy = false;
    for (let i = 0; i < visible.length; i++) {
      if (!insideBubble(visible[i].r)) result.objectFramesOutsideBubble++;
      for (let j = i + 1; j < visible.length; j++) {
        const ratio = overlapRatio(visible[i].r, visible[j].r);
        result.maxObjectOverlap = Math.max(result.maxObjectOverlap, ratio);
        if (ratio > 0.25) heavy = true;
        if (!declared(contacts, visible[i].o.instance, visible[j].o.instance, f))
          result.maxUndeclaredOverlap = Math.max(result.maxUndeclaredOverlap, ratio);
      }
    }
    if (heavy) result.framesWithHeavyOverlap++;
    for (const { o } of visible) {
      if (!(o.instance in result.firstVisibleDistanceFromOrigin))
        result.firstVisibleDistanceFromOrigin[o.instance] = round(Math.hypot(o.x - ORIGIN.x, o.y - ORIGIN.y), 1);
      if (last[o.instance]) result.pathLength[o.instance] = (result.pathLength[o.instance] || 0) +
        Math.hypot(o.x - last[o.instance].x, o.y - last[o.instance].y);
      last[o.instance] = o;
    }
    const lit = frame.symbols.filter((s) => s.opacity > 0.2);
    result.maxSymbolsOnOneFrame = Math.max(result.maxSymbolsOnOneFrame, lit.length);
    for (const s of lit) {
      if (seenSymbols.has(s.instance)) continue;
      seenSymbols.add(s.instance);
      result.symbolInstancesByComponent[s.component] = (result.symbolInstancesByComponent[s.component] || 0) + 1;
    }
    if (f >= QUIET_START) {
      if (frame.symbols.some((s) => s.opacity > 0)) result.tailSymbolsSilent = false;
      const key = JSON.stringify(frame.objects.map(({ instance, x, y, scale, rotation, opacity }) => [instance, x, y, scale, rotation, opacity]));
      if (f > QUIET_START && key !== result._tailKey) result.tailStatic = false;
      result._tailKey = key;
    }
  });
  delete result._tailKey;
  result.symbolInstancesUsed = seenSymbols.size;
  result.maxObjectOverlap = round(result.maxObjectOverlap);
  result.maxUndeclaredOverlap = round(result.maxUndeclaredOverlap);
  for (const k of Object.keys(result.pathLength)) result.pathLength[k] = Math.round(result.pathLength[k]);
  return result;
}

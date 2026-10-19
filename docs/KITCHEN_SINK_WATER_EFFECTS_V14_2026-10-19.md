# Kitchen Sink Water Effects V14

Date: 19 October 2026

Status: reversible animated visual-review draft; unapproved and unpromoted

Review route: `/keeper-review/kitchen-sink-water-effects-v14/`

V14 preserves the complete standalone V13 sink cabinet byte-for-byte in every
state. The tap and basin never break, detach or move. State is expressed only
through separate water-only animation strips:

- On: a gentle narrow stream registered beneath the actual tap outlet, with a
  restrained splash inside the basin;
- Broken: three irregular jets originate inside the basin and shoot upward,
  making the plumbing fault readable without changing the sink object.

Both strips contain 40 isolated 92 × 108-pixel cells at 4 fps, forming a
ten-second source loop. Review playback permits a 0.1×–4× multiplier without
changing the source strip. Every frame retains transparent gutters and contains
no tap, basin, cabinet, worktop, wall or floor pixels.

Named SFX placeholders are `kitchen_sink_water_gentle_loop` and
`kitchen_sink_pipe_burst_loop`. Final and runtime remain unchanged.

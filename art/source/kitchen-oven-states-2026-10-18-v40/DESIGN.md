# Kitchen oven V40 source design

V40 is a new coordinated Off/On/Broken oven family. It does not reuse V35
object pixels. The approved V39 complete room supplies the exact fitted-galley
context, palette and geometry; the basic V21 oven was used only as a scale and
single-oven reference during generation.

All three states are selected from one generated source sheet and normalised
to a `104 × 112` transparent cell. Their common opaque bounds are
`(10,4)–(94,99)`, so each occupies exact room bounds `x=336–420`,
`y=123–218` when composited at `(326,119)`. The prior oven and hob are removed
before any V40 state is inserted.

- Off: dark cavity, upright rotary dials and unlit indicator.
- On: turned dials, red indicator, amber cavity and a visible roasting tin.
- Broken: attached askew door and one failed right rotary dial hanging below
  its empty fascia socket by two short wires.

The oven body never animates. Billowing cavity smoke, two hob flame clusters,
and the broken warning/cavity light are separate reusable `40`-frame, `4 fps`,
ten-second strips in `120 × 144` cells with transparent safety gutters. The
warning strip uses irregular rapid red bursts and only five brief amber cavity
flickers in forty frames.

Selected source:
`generated/oven-three-state-hanging-dial-source-v2.png`

SHA-256:
`d21f2ba12fb4fd2b2c5e1483b0792717cd316e964f59c63d75f40dec9ffcca78`

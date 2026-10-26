# Image-generation record

Mode: built-in image-generation tool. Use case for all calls:
`stylized-concept`, except the sink correction (`precise-object-edit`).

References supplied to every new asset:

1. `sources/style-authority-user-reference.png` — absolute ink, detail and
   material-quality authority;
2. `sources/approved-style-calibration.png` — approved palette and room-look
   authority.

Common final prompt contract:

> Create one isolated modular 2D game asset in the approved adult-playful
> modern ligne-claire style: strong organic near-black ink, substantial
> bevelled/layered construction, dense purposeful line detail, clean fills,
> restrained upper-left highlight and one internal shadow tone. Use strict
> front elevation with only the specified shallow top reveal. Return genuine
> transparent alpha with generous gutter. No cast, contact, wall or floor
> shadow; no exterior glow; no perspective side face; no text, logo or
> watermark.

Per-asset final subject instructions:

- `cooker`: narrow 0.50 × 0.60 × 0.90 m slot-in cooker; blue hob and plinth;
  two black hotplates; three copper dials, red indicator and copper handle;
  cream fascia/door; dark OFF window and rack lines.
- `utility`: narrow royal-blue 2.00 m cupboard; three bevelled panel zones and
  copper handle; closed state.
- `fridge`: narrow cream 1.80 m fridge-freezer; two sealed doors and two copper
  handles; closed state.
- `drawers`: one-bay front only; three blue bevelled drawers and copper pulls;
  no worktop, plinth or outer side panel.
- `cupboard`: one-bay front only; two blue inset doors and paired copper
  handles; no worktop, plinth or outer side panel.
- `sink-front`: two-bay front only; cream Belfast apron over two blue doors;
  no bowl, taps, worktop or plinth.
- `dishwasher`: one-bay cream front only; bevelled door, copper handle and
  three dark OFF indicator lenses.
- `sink-insert`: broad two-bay cream rim; one bowl and taps wholly over the left
  bay; right integrated draining board; no cabinet or worktop.
- `toaster`: compact cream two-slot toaster with copper trim/lever and shallow
  top reveal.
- `kettle`: compact vintage cream kettle with copper lid, small spout and blue
  handle.
- `pet-bowl`: low blue enamel bowl with cyan inner accent, shallow oval top.
- `pedal-bin`: narrow blue bin with silver lid, bevelled body and dark pedal.
- `utility-open-door`: tall blue camera-facing foreground door overlay with
  bevelled panel and copper handle; no cabinet or interior.
- `worktop`: straight tileable cyan one-bay segment, 84:31 proportion, 17-unit
  reveal plus 14-unit front slab; no cut-out or end caps.
- `plinth`: straight tileable blue one-bay shallow segment; no end caps.
- `window`: square traditional timber four-pane frame and sill; no view,
  scenery or shadow. Generated pane colour was rejected and replaced by the
  deterministic technical key.
- `oven-overlay`: only the lit cavity contents inside a landscape rectangle:
  amber glow, rack bars and one loaf in a cream tray; no cooker body.

Corrective edit applied to the first sink source:

> Keep the exterior rim and approved finish. Replace the invented right bowl
> with an integrated draining board; retain one bowl on the left and centre
> both orange knobs and the silver arched spout above it. Change nothing else.

The first cooker generation and its attempted shadow-removal edit are retained
as provenance. Production normalisation, rather than model alpha, enforces the
no-shadow boundary.


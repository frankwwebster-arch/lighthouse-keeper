# Kitchen Ligne-Claire Complete Review V59 — 22 October 2026

V59 is the immutable fitted-carcase predecessor now inherited by active V60.
It replaced V56 in the short review route without approving, registering or
promoting any new production asset; its versioned route remains available.

## Fitted-kitchen construction

- Cabinet V11 is the shell authority for both appliances: the common worktop,
  blue side construction and plinth come from the cabinet geometry and palette.
- The approved oven remains the insert authority for its hob, controls, fascia,
  cavity, door and state art. Translucent/glossy pixels belonging to its former
  separate blue cooker slab are deliberately excluded.
- Dishwasher V8 remains the insert authority for Off, On and Broken. The closed
  insert stops above the exact cabinet plinth; its failed Broken door may hang in
  front of the plinth. Cupboard-specific orange hinges and knobs are excluded
  from appliance shells.
- The oven and dishwasher controls now share the same room-height baseline.

## Join correction

The old healer's foreground cap began with a light opaque row, interrupting the
dark rear worktop edge at every placement perimeter. V59 replaces that row in
the flat cap and both neighbour cleanup masks with one composite-matched dark
row. Because the oven now uses the same cabinet shell, it also uses the ordinary
flat cabinet join; the obsolete oven-only triangular join is no longer selected.

## Preserved behaviour and approval boundary

Kettle V47 art and the approved V46 motion/SFX presentation are unchanged.
Dishwasher state semantics, Broken movement lock, repair transition, tremor,
independent SFX toggle, drop-in placeholder replacement, suds ownership and
all other kitchen interactions are unchanged. Approved oven, cabinet,
dishwasher and kettle source files and production selectors remain untouched.

V59 is an immutable review candidate. Registration and promotion remain closed
until Frank explicitly approves it. Reject it by discarding only the V59 draft,
review shell and archive set; all predecessors remain available.

## Verification

`scripts/build_kitchen_ligne_claire_complete_review_v59.py --verify` checks the
closed gate, complete review/archive coverage, exact cabinet plinth inheritance,
absence of cupboard hardware on appliance stiles, opaque-only oven-top insert
pixels, the flat join selector and root-absolute archived delivery.

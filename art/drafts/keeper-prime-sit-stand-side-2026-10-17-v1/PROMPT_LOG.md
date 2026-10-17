# Keeper Prime side-right sit/stand V1 prompt log

Generated with OpenAI's built-in image generation on 17 October 2026. Each
request used three local image references: the approved smooth Prime
side-right standing authority, the registered Prime side-right seated
endpoint, and one isolated frame from the legacy six-frame side-sit strip.
The legacy image supplied choreography only; none of its pixels were reused.

Shared instruction for F2–F5:

> Preserve the exact adult Prime Keeper identity, cap and badge, solid dark
> rectangular eye, separate moustache and closed mouth, beard mass, one cream
> jumper stripe, standard single-band colour palette, smooth antialiased black
> outlines and side-right view. Draw one isolated full-body transparent PNG.
> Preserve the planted floor and progress naturally from the standing
> authority to the seated authority. No chair, floor, shadow, props, text,
> duplicate body parts or extra limbs.

- F2: shallow crouch; knees beginning to flex; hips moving slightly down and
  back; hands moving forward for balance.
- F3: deeper crouch; hips farther down and back; both boots planted; hands
  continuing toward the lap.
- F4: near-seat lowering; hips immediately above the 11-lp seat plane; boots
  slightly forward; hands above thighs.
- F5: first seat contact; pelvis at the seated endpoint's 11-lp seat height;
  torso fractionally forward; hands settling onto lap; boots on common floor.

Deterministic post-processing removes alpha at or below 16, crops to visible
bounds, resamples with Lanczos to the documented target height and width, centres visible
bounds at x=127.5, and registers the lowest opaque row at y=315 in a transparent
256 × 320 cell. F1 and F6 bypass post-processing and are byte-identical copies
of their endpoint authorities.

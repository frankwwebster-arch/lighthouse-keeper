# Prompt log

Built-in image generation was used for two exploratory upper-landing bridge studies on 15 October 2026. The studies asked for a compact, transparent side-left pose transferring the trailing foot from the last stair tread onto the flat upper landing while preserving the approved V16 and Prime side identities.

Neither study was selected. One materially widened and redrew the Keeper and is retained as `sources/rejected/keeper-prime-top-landing-pass-too-wide.png`. The later edit faced the wrong direction and contained three arms; it is retained as `sources/rejected/keeper-prime-top-landing-pass-rejected-three-arms.png`. Neither image is copied to the review page, referenced by the animation timeline or eligible for promotion.

The delivered landing candidate instead uses exact approved Walk V6 F3 pixels with a browser `scaleX(-1)` transform for the compact landing-pass frame.

After Frank required the hallway endpoint to include an actual door-opening action, built-in image generation produced two side-right reach drawings from the exact approved Prime side neutral, using the historical `keeper_door_open_side` strip only as a choreography reference. Both prompts explicitly required exactly two arms, two hands and two legs, with the nearer/right arm replacing the neutral hanging arm rather than being added to it. The resulting source files are:

- `sources/generated/keeper-prime-door-reach-right-partial-generated.png` — SHA-256 `7b6bafe9e247a1935708f74ca62b16f3ac2c8675fae9bd891e084325e99e88f4`;
- `sources/generated/keeper-prime-door-reach-right-full-generated.png` — SHA-256 `3d5a3455497dd8b7268b867b189c2ddca4998982c2ad9d46415af86103dfe7de`.

The builder normalises those sources with Lanczos resampling into independent 256 × 320 transparent candidate cells. They are used only for the labelled right-hand reach/retract action. Walk, stair, neutral, turn, acceleration and deceleration drawings remain exact pinned authorities. The reach drawings are not approved and cannot enter Final or runtime through this pack.

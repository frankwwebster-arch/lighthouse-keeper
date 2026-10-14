# Prompt log — Keeper Prime Walk V5

Mode: built-in image generation, identity-preserving precise edits.

Each selected source used the exact V4 frame as the edit target and the matching deterministic V5 red/cyan joint guide as the pose authority. Prompts required both arms to follow the guide while preserving the complete head, torso identity, palette, trousers, accepted leg pose, boots, scale, floor anchor, transparency and safety gutter.

- F2 required the large foreground arm to move back/down and the smaller rear arm to move forward.
- F3 required both arms at their first near-vertical passing pose.
- F4 required the foreground arm moving forward and rear arm moving back.
- F6 required both arms returning from the opposite contact.
- F7 required the opposite near-vertical passing pose.
- F8 reused the successful F2 source as its symmetric loop partner after two direct F8 generations repeatedly reversed foreground/background arm roles; both failed F8 attempts are retained as rejected provenance.

Final output is not the generated full character. Generated sources are registered to the accepted frame, then composited only through declared arm/occlusion polygons. F1 and F5 are copied byte-for-byte.

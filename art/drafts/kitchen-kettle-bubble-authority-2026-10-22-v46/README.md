# Kitchen kettle Bubble authority V46

**Status:** superseded unapproved history; not promoted or wired

Frank asked to reuse the approved Bubble-story `tea-kettle` V2 as the actual
kitchen kettle and agreed to the state/effect adaptation boundary. This pack
uses that exact kettle body for Off and On. It removes only the detached steam
component, preserves that component separately, and leaves all retained body
RGBA bytes unchanged. A new Broken derivative follows the same flat-palette
language. The six V45 40-frame/4-fps effect strips and all placement,
interaction, support and Broken-lock contracts are copied or hash-pinned.

Frank liked its broken handle but asked for less restrained damage and a fully
detached lid so steam could pour from the open top. V47 supersedes this Broken
candidate without editing it. V45, Bubble V2, production and runtime are
untouched.

Build or verify with:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_kitchen_kettle_bubble_authority_v46.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_kitchen_kettle_bubble_authority_v46.py --verify
```

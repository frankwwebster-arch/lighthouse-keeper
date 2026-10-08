# Decisions made while building

- Standalone Vite + React + TypeScript app; engine is pure and seeded, so every behaviour is testable.
- No AI at runtime: typed commands go through a typo-tolerant matcher over a fixed command book. Close misses ask "did you mean?", nonsense gets a shrug.
- Quiz gating: only treats wait for an answered question; loo, food, wash and bed never do, so he cannot get stuck. Three wrong tries reveal the answer, which is typed in for no points.
- Questions appear after about 25 seconds idle and at least 150 seconds apart; times-table heavy.
- Chat questions follow the real clock (weekday afternoon asks about school, Saturday morning about football).
- Day is 07:00 to 21:30 game time, 8 real minutes. Bed from 19:00, annoyance from 20:00, forced to bed 21:30.
- Score out of 100 (mood 30, ship 20, friends 10, pet 10, house 10, brain 10, bedtime 10). Next day's allowance is 10 + 30% of the score. Up to 40 credits carry over.
- Camera: whole tower at rest; zooms to the object while used (not on the loo walk).
- Saves to the browser (localStorage) every 4 seconds and at day end.
- Sprites are vector placeholders; real art drops in via the manifest.
- Allowance is now driven by green need bars, not the overall score. Each of the 7 needs has a day-average; at or above the green line (default 50%) it is green. Tomorrow's allowance = guaranteed base + bonus x (greens / 7). One neglected need only costs one seventh of the bonus. The 100-point score stays as a fun rating with bonus marks.
- Grown-ups panel (Menu, then Grown-ups, PIN starts as 1234): dials for the base allowance, all-green bonus, green line, first-day credits, carry-over cap, price scale and per-food prices, plus gifting credits. Kept separately in the browser so new games keep the dials. Upgrade prices and gifting upgrades are to be added when upgrades exist (tiers on existing objects, no furniture shop).

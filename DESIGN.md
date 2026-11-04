\# Dodger: Design Document



\## Pitch

Slide sideways to dodge falling rocks. One hit ends the run.



\## Goal and scoring

\- Score = seconds survived

\- Best score kept in memory while the game is open (no saving to disk)



\## Technical decisions

\- Pygame-ce, packaged for the browser with pygbag

\- Window: 480x800 portrait, pygame.SCALED

\- Target devices: PC, laptop, tablet, phone



\## Controls

\- Arrows or A/D: move at a fixed speed

\- Finger or mouse pressed: player follows pointer x

\- Tap, click or SPACE: start and restart



\## Game objects

\- Player: rectangle near the bottom, moves sideways only, clamped to screen

\- Rock: rectangle with random size and speed, spawns above the top, removed below the bottom



\## Rules

\- Player touches a rock: game over

\- One life



\## States

\- menu -> playing (SPACE or tap)

\- playing -> gameover (collision)

\- gameover -> playing (SPACE or tap, full reset)



\## Timers

\- Survival timer: time since the run started

\- Spawn timer: controls when the next rock appears



\## Milestones

\- \[ ] 1. Window and game loop

\- \[ ] 2. Player moves and stays on screen

\- \[ ] 3. One falling rock, removed off-screen

\- \[ ] 4. Many rocks (list) with spawn timer

\- \[ ] 5. Collision

\- \[ ] 6. States and reset

\- \[ ] 7. Score display and best score

\- \[ ] 8. Polish: difficulty, sound, browser test



\## Ideas for later

\- Difficulty ramp

\- Sound effects

\- Art instead of rectangles


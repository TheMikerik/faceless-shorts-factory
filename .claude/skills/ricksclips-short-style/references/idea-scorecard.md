# Idea scorecard (the 10/10 gate)

Used at step 2 of `--cv`. **Show the user only ideas that score 10/10, and at least two of them.** If fewer than two reach 10/10, keep generating and fixing. Never show the rest and never mention them.

"10/10" is not a feeling. It means the idea passed every gate and scored the maximum on the points below, with a written reason for each one. A score of 9 is a 9, not "almost 10".

## Procedure

1. **Read what was done.** `scripts/ideas_used.json` (question, steps, mechanics of every past "What if" video) and `videos/*/script.txt`.
2. **Generate 8 to 10 candidates** silently. Spread them over different areas (body, animals, food, Earth, space, sea, weather, home, school) and settings; none may repeat the area or setting of the last 3 videos. Then do a **basic plausibility check** (web search) of the candidates you want to keep: is the real consequence of each step roughly what you think? The full claim-by-claim check comes after the user chooses (see "Facts" in `CLAUDE.md`).
3. **Mechanical check.** Write the candidates into the scratchpad as `candidates.json` (fields: `title, hook, rule, ladder, twist, mechanics, puppets, places, side_characters`; `rule` = the one change to the world, `ladder` = 3–4 steps, `twist` = the finale) and run:
   ```
   .venv/bin/python scripts/idea_check.py <scratchpad>/candidates.json
   ```
   Drop every FAIL, or fix it and run again. Treat a `!` warning as a point lost below unless you can argue it away in one line.
   `mechanics` = 2 to 4 honest tags of the topic (e.g. `body-size`, `no-sun`, `shrinking`, `endless-rain`). Do not invent odd tags just to dodge the novelty check: if the core question is the same as a past video, it fails.

4. **Score with the card below.** For every line, write one concrete reason (quote the hook, name the scene). "Yes" alone does not count.
5. **Critic pass.** Switch roles: you are a bored 13-year-old scrolling at 1 AM. For each surviving idea, write the strongest reason to swipe away at second 2, the moment where a half-watching viewer gets lost, and the reason the ending feels flat. Every real hit costs the point it belongs to.
6. **Fix or drop.** Rewrite ideas at 8 or 9 (usually the hook or the finale) and go back to step 3. Drop ideas at 7 or less. Generate new candidates if the pool runs dry.
7. **Show** only 10/10 ideas (at least 2, at most 3), in the exact `--cv` output format. `Hodnocení: 10/10`.
8. **After the user chooses**, register the idea: `.venv/bin/python scripts/idea_check.py --add <file with that one candidate> NNN`.

## Gates (all must pass, otherwise the idea is dead)

| # | Gate |
| --- | --- |
| G1 | The hook starts with **"What if"**, max **10 words**, simple English, and meets at least **3 of 4** hook criteria (`CLAUDE.md`, "Strong hooks") |
| G1b | **First frame**: write what is visible at 0:00. It must show Tlama in the most extreme moment of the what-if, not a setup. The whole script fits **110–130 words (max 35 s)** |
| G2 | **One change to the world**, sayable in one sentence. No second what-if |
| G3 | **One ladder**: 3–4 steps on one scale (time or size), each bigger and each drawable |
| G4 | **Honest**: there is a real, checkable answer; the plausibility check found no step that is wrong or pure guessing |
| G5 | Max 3 places, max 2 side characters, all puppets exist in `PUPPETS.md` (no Higgsfield needed); props come from `props/` or primitives |
| G6 | **New**: `idea_check.py` passes; the question was not used in any past video, and the area/setting differs from the last 3 |
| G7 | Retell test in 3 sentences works, and every sentence can be drawn |
| G8 | Safe for kids and monetization: no gore or detailed death, no real fear, no health advice, nothing dangerous to copy, no politics, religion, tragedies, real people or brands |

## Points (10 = all of them)

| Pts | Criterion | The question to answer |
| --- | --- | --- |
| 2 | **2-second stop** | Does a muted viewer understand the question from the first picture and want to stay? |
| 1 | **Curiosity** | Would a ten-year-old have wondered about this, or wonder now? |
| 1 | **No obvious answer** | Is the viewer unable to guess what happens at the last step? |
| 1 | **Rising stakes** | Is the last step huge, not just "more of the same"? |
| 1 | **Surprising fact** | Is there at least one true thing that makes the viewer say "really?" |
| 1 | **Open loop holds** | Is there a question the viewer still wants answered right before "But here is the real problem"? |
| 1 | **Last-line loop** | Does the last line lead back into the hook, so the replay feels seamless? |
| 1 | **Comment trigger** | Is there an obvious thing to comment ("I would…", "now do the Moon")? |
| 1 | **Visual payoff** | Is there one big moment the stage can show well (something huge, flying, a crowd, a swap)? |

## Baseline

The first 10 "What if" videos keep the format unchanged. The log and targets are in `z_info/hook_tests.md`; read it before step 2.

## Calibration

After a video has been out for 7 days, add a row here (views, average % viewed). Every few videos, compare: if 10/10 ideas do not beat the rest, find which criterion failed to predict it and change the card.

| Video | Idea | Score | Views (7 d) | Avg % viewed | Note |
| --- | --- | --- | --- | --- | --- |

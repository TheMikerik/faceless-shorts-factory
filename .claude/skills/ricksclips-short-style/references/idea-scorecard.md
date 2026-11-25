# Idea scorecard (the 10/10 gate)

Used at step 2 of `--cv`. **Show the user only ideas that score 10/10, and at least two of them.** If fewer than two reach 10/10, keep generating and fixing. Never show the rest and never mention them.

"10/10" is not a feeling. It means the idea passed every gate and scored the maximum on the points below, with a written reason for each one. A score of 9 is a 9, not "almost 10".

## Procedure

1. **Read what was done.** `scripts/ideas_used.json` (rule + mechanics of every past video) and `videos/*/script.txt`.
2. **Generate 8 to 10 candidates** silently. **Choose the setting first** (see "Setting variety" in the project `CLAUDE.md`): spread the candidates over different `props/` packs and places (factory, pirate ship, forest, graveyard, kitchen, school, space...), not over "town" variants. At most 1 candidate may be a town/city story, and none may repeat the setting of the last 3 videos. Also vary the everyday situation (breakfast, school, bedtime, a trip, a pet, a birthday) and the kind of magic rule. Do not show them.
3. **Mechanical check.** Write the candidates into the scratchpad as `candidates.json` (fields: `title, hook, rule, twist, mechanics, puppets, places, side_characters`) and run:
   ```
   .venv/bin/python scripts/idea_check.py <scratchpad>/candidates.json
   ```
   Drop every FAIL, or fix it and run again. Treat a `!` warning as a point lost below unless you can argue it away in one line.
   `mechanics` = 2 to 4 honest tags of what makes the story tick (e.g. `mouth-sound`, `growing-object`, `teleport`, `role-swap`). Do not invent odd tags just to dodge the novelty check: if the core idea is the same as a past video, it fails.
4. **Score with the card below.** For every line, write one concrete reason (quote the hook, name the scene). "Yes" alone does not count.
5. **Critic pass.** Switch roles: you are a bored 13-year-old scrolling at 1 AM. For each surviving idea, write the strongest reason to swipe away at second 2, the moment where a half-watching viewer gets lost, and the reason the ending feels flat. Every real hit costs the point it belongs to.
6. **Fix or drop.** Rewrite ideas at 8 or 9 (usually the hook or the twist) and go back to step 3. Drop ideas at 7 or less. Generate new candidates if the pool runs dry.
7. **Show** only 10/10 ideas (at least 2, at most 3), in the exact `--cv` output format. `Hodnocení: 10/10`.
8. **After the user chooses**, register the idea: `.venv/bin/python scripts/idea_check.py --add <file with that one candidate> NNN`.

## Gates (all must pass, otherwise the idea is dead)

| # | Gate |
| --- | --- |
| G1 | The hook meets at least **4 of 5** hook criteria (middle of action, exaggerated + concrete, stakes/clock, open loop, Tlama in danger/at center), max 15 words, simple English |
| G2 | **One magic rule**, sayable in one sentence. No second magic |
| G3 | **Rule of three**: the same kind of event three times, each bigger |
| G4 | The **twist uses only what was already shown** and lands back on the hook, so the Short loops |
| G5 | Max 3 places, max 3 side characters, all puppets exist in `PUPPETS.md` (no Higgsfield needed) |
| G5b | **Setting variety**: not a default town/city/mayor story (max 1 of the 3 shown), and a different setting from the last 3 videos; the setting uses a `props/` pack and changes what happens |
| G6 | **New**: `idea_check.py` passes; the core mechanic was not used in any past video |
| G7 | Retell test in 3 sentences works, and every sentence can be drawn |
| G8 | Safe for kids and monetization (no violence, fear for real, gross-out, real people/brands) |

## Points (10 = all of them)

| Pts | Criterion | The question to answer |
| --- | --- | --- |
| 2 | **2-second stop** | Is the first sentence a picture so strange that a muted viewer stops too? (picture, not only words) |
| 1 | **Instant rule** | Can a viewer guess the rule from the first escalation, before "You see…"? (they enjoy predicting the next step) |
| 1 | **Everyday base** | Is the starting point something every kid knows (breakfast, homework, a lie, hiccups, a pet)? |
| 1 | **Rising stakes** | Is step 3 huge (whole town, the sky, the mayor), not just "more of the same"? |
| 1 | **Open loop holds** | Is there a question the viewer still wants answered right before "You see…"? |
| 1 | **Reversal twist** | Does the ending flip Tlama's position (winner→loser, scared→scary, cure→cause)? |
| 1 | **Last-line loop** | Does the last line almost repeat the first line, so the replay feels seamless? |
| 1 | **Comment trigger** | Is there an obvious thing to comment ("what would you do?", "wait, so that's why…", "do it again")? |
| 1 | **Visual payoff** | Is there one big moment the stage can show well (a crowd, something huge, something flying, a swap)? |

## Calibration

After a video has been out for 7 days, add a row here (views, average % viewed). Every few videos, compare: if 10/10 ideas do not beat the rest, find which criterion failed to predict it and change the card.

| Video | Idea | Score | Views (7 d) | Avg % viewed | Note |
| --- | --- | --- | --- | --- | --- |

# Long-form idea scorecard (the 10/10 gate)

Used at step 2 of `--clv`. **Show the user only ideas that score 10/10, and at least two of them** (at most three). If fewer than two reach 10/10, keep generating and fixing. Never show the rest and never mention them.

"10/10" is not a feeling. It means the idea passed every gate and scored the maximum on the points below, with a written reason for each one. A score of 9 is a 9, not "almost 10".

## Procedure

1. **Read what was done.** `scripts/ideas_used_longform.json` (rule, mechanics, ladder of every past long-form video) and `longform/*/script.txt`. Long-form ideas are compared only with long-form videos; developing a topic that was once a Short is allowed.
2. **Generate 8 to 10 candidates** silently. Spread them out: different everyday situations and different kinds of magic rule. Do not show them.
3. **Mechanical check.** Write the candidates into the scratchpad as `candidates.json` and run:
   ```
   .venv/bin/python scripts/idea_check.py --longform <scratchpad>/candidates.json
   ```
   Fields: `title, hook, rule, twist, mechanics, puppets, places, side_characters` (as for Shorts) plus `ladder` (5-7 short escalation steps, same kind of event, each bigger) and `midpoint` (the turn at ~3:00).
   Drop every FAIL, or fix it and run again. Treat a `!` warning as a point lost below unless you can argue it away in one line.
   `mechanics` = 2 to 4 honest tags of what makes the story tick. Do not invent odd tags to dodge the novelty check.
4. **Score with the card below.** For every line, write one concrete reason (quote the hook, name the step or the scene). "Yes" alone does not count.
5. **Critic pass.** Switch roles: you are a bored 13-year-old with a long video open. For each surviving idea write: why you would leave at **0:30**, at **2:00** and at **4:00**; where a half-watching viewer gets lost; why the ending feels flat. Every real hit costs the point it belongs to.
6. **Fix or drop.** Rewrite ideas at 8 or 9 (usually the ladder, the midpoint or the twist) and go back to step 3. Drop ideas at 7 or less. Generate new candidates if the pool runs dry.
7. **Show** only 10/10 ideas in the exact `--clv` output format. `Hodnocení: 10/10`.
8. **After the user chooses**, register the idea: `.venv/bin/python scripts/idea_check.py --longform --add <file with that one candidate> LNNN`.

## Gates (all must pass, otherwise the idea is dead)

| # | Gate |
| --- | --- |
| G1 | The **hook** meets at least **4 of 5** hook criteria (middle of action, exaggerated + concrete, stakes/clock, open loop, Tlama in danger/at center), max 15 words, simple English |
| G2 | **One magic rule**, sayable in one sentence. No second magic |
| G3 | **Escalation ladder**: 6 steps (5-7) of the same kind of event, each bigger, grouped into 3 acts (small → bigger → huge). The rule gives 6 different showable situations without filler |
| G4 | **Every act ends with an open question** that carries the viewer into the next act |
| G5 | **Midpoint turn** (~3:00) changes what is at stake, with the same rule and no second magic (e.g. Tlama's plan backfires, the rule has a catch) |
| G6 | The **twist uses only what was already shown**, and the last line comes back to the hook |
| G7 | Max 5 places, max 5 side characters, all puppets exist in `PUPPETS.md` (no Higgsfield needed). Nobody new after "You see…" |
| G8 | **New**: `idea_check.py --longform` passes; the core mechanic was not used in any past long-form video |
| G9 | **Retell test in 5 sentences** works (act 1, act 2, act 3, "You see…", the end), and every ladder step can be drawn |
| G10 | Safe for kids and monetization (no violence, real fear, gross-out, real people/brands) |

## Points (10 = all of them)

| Pts | Criterion | The question to answer |
| --- | --- | --- |
| 2 | **First 30 s** | Do the hook and the first ladder step land within 30 s, with the rule already clear? (Long videos lose most viewers in the first 30 s, so this counts double.) |
| 1 | **Everyday base** | Is the starting point something every kid knows (breakfast, homework, a lie, hiccups, a pet)? |
| 1 | **The ladder climbs** | Is the last step huge (whole town, the sky), and is every step visibly bigger than the one before? |
| 1 | **Cliffhangers** | Do all 3 acts end on a question the viewer needs answered? |
| 1 | **Midpoint turn** | Does the turn at ~3:00 bring new energy without adding new magic? |
| 1 | **Running gag** | Do 1-2 side characters have one clear reaction that keeps coming back? |
| 1 | **Reversal + loop** | Does the ending flip Tlama's position, and does the last line come back to the hook? |
| 1 | **Visual variety** | Does every act have one big moment the stage can show well, and are the places clearly different from each other? |

## Calibration

7 days after a long-form video is out, add a row. Every few videos, compare: if 10/10 ideas do not beat the rest, find which criterion failed to predict it and change the card.

| Video | Idea | Score | Views (7 d) | CTR | Avg view duration | Still watching at 0:30 | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |

# Hook tests (retention experiments)

Goal: swipe-away under **33 %** on YouTube Shorts (YouTube Studio → the video → Engagement → "Viewed vs swiped away").

## Rules of the test

1. **One change per block, and every block is exactly 3 videos.** One video proves nothing. All 3 videos in a block use the same changed rule; everything else stays as it is.
2. **Read the numbers the same way every time:** at 500+ views and about 2 hours after upload (the ratio is stable by then: video 015 had 36 / 64 at both 333 and 539 views). Write down "Stayed to watch" %. Also write the average view duration if you have it.
3. **Decision after the 3rd video of a block:** compare the block's average swipe-away with the previous block.
   - Improved by 5 points or more → **keep the rule** (it becomes a standing rule in `CLAUDE.md`).
   - Within ±5 points → **no effect**, keep the simpler option and move on to the next test.
   - Worse by 5 points or more → **drop the rule** and go back.
4. **Only YouTube counts** for the decision (TikTok and Instagram show videos to your followers first, so their numbers are not comparable). Optionally note them in the last column.
5. Do not run two tests in the same video. `--cv` marks each new video with the active test (see the table below), and the script must follow its rule.

## Test queue (in this order)

| Block | Rule under test | How the script must follow it | Videos | Avg swipe-away | Decision |
| --- | --- | --- | --- | --- | --- |
| T0 (baseline) | Current format (110–130 words, ≤ 35 s, first frame = absurd thing) | no change | 015 + two more | | |
| T1 | **Concrete hook the muted viewer understands** | first sentence names a visible thing doing a visible action ("A giant chicken follows me."); no abstract wording ("it rains me") | | | |
| T2 | **Rule clear within 5 s** | the magic rule is stated or shown in the first 2 sentences, not only at "You see…" | | | |
| T3 | **First 3 s = the most extreme picture** | first shot is the biggest absurd moment of the story (not the setup), with movement from frame 1 | | | |

Order can change after the data, but never more than one active test at a time. T0 is the baseline: until 3 videos with the unchanged format exist, compare against 015 alone and treat the result as a rough guide only.

## Video log

One row per video, filled in after reading the numbers (the first column is the active block).

| Video           | Block | Hook (first sentence)                             | Views at read | Stayed % | Swiped % | Avg view duration |
| --------------- | ----- | ------------------------------------------------- | ------------- | -------- | -------- | ----------------- |
| 015 It Rains Me | T0    | "I fell in the rain machine. Today, it rains me." | 640 (~1,5 h)  | 37       | 63       |                   |
| 016 Nine More Minutes | T0 | "I have nine minutes before a hundred skeletons wake up." | | | | |

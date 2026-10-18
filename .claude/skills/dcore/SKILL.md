---
name: dcore
description: Turn a recorded debate, townhall or podcast on YouTube into one HTML page with the argument branches (each distinct claim once, with its challenges, replies and unanswered questions, each timestamped) and a "how this debate went" report with per-voice stats. Use when asked to map, break down or report on a video debate or discussion.
---

# dcore

You do the judgment work; the scripts do the plumbing. Never hand-count a stat
or hand-write HTML: `check.py` and `render.py` compute those from the file you
write. There is no fact-checking here: the map shows what was said and done,
not whether it is true.

Everything lives in one folder, `debates/<id>/`:

| File | Written by |
| --- | --- |
| `transcript.json`, `transcript.txt` | `fetch.py` |
| `map.json` | you |
| `page.html` | `render.py` |

Scripts are in `.claude/skills/dcore/scripts/` and need only Python 3.10+
(plus `youtube-transcript-api` to fetch captions).

## Principles (non-negotiable)

- **Actions, not labels.** The page describes what someone did, with a time:
  "no direct answer; turned to fuel prices at 12:40". Never "dodged", "lied",
  "biased", "propaganda". A private `label` on a point may carry your tag
  (`"dodge"`, `"loaded question"`); it is never shown. `check.py` warns when a
  label word leaks into shown text.
- **Take no sides.** No winner, no score, no verdict on a person or a side. The
  report is "how this debate went", never "the anchor failed".
- **Anonymous voices.** Voice A, B, C. No names, even if the video says them.
- **Fair paraphrase.** Each point in words its own speaker would accept, in the
  language of the person asking. Keep the original words in `quote`.
- **Say what you inferred.** Voices come from context, so every count is
  approximate, and each voice's `basis` says how you told it apart.

## Steps

1. **Fetch.** `python fetch.py <youtube-url> --out debates/<id> --title "..." --channel "..."`.
   If YouTube is blocked (common from cloud machines) it says so. Then ask for
   the transcript: on YouTube, "... > Show transcript", copy it all, paste it;
   or a `.vtt`/`.srt` file. Save it and rerun with `--from <file> --lang hi`.
   `<id>` is a short kebab-case slug of the topic.

2. **Read** `transcript.txt` end to end before writing anything.

3. **Voices.** Work out the distinct voices from context: who asks and hands
   the floor (usually the anchor), who answers which line of argument,
   addressing ("aap bataiye..."), stance continuity. Use as few voices as the
   transcript supports. Don't guess when it's unclear: give the stretch to the
   most likely voice and say so in `basis`.

4. **Turns.** Mark who held the floor, in order, covering the talk:
   `{"voice": "B", "start": 61.0, "end": 118.5}`. Use caption start times.

5. **Branches.** The map is not the conversation in order. It's a tree of the
   distinct claims and how they were contested, so a reader sees each line of
   argument once:
   - `position`: one of the answers on offer to the topic ("defend the rupee",
     "let it float"). Top level, `parent: null`. Add positions only when the
     debate has them; otherwise top-level claims hang straight off the topic.
   - `claim`: a statement offered as true or as a reason. Under a position its
     `stance` is `for` or `against`; under a claim or question it is
     `supports`, `challenges`, `answers` or `concedes`.
   - `question`: a question put to someone, as a move on the claim it presses
     (`stance: "challenges"` usually). Needs `to` (or `null` for the room),
     `outcome` (`answered`, `partly`, `not_answered`) and `followed_up` (did
     anyone come back to it). Put the answer under it with `stance: "answers"`.
   - **One node per distinct point.** When a point is repeated, add the moment
     to its `said` list instead of a new node: `said: [{"voice": "B", "t": 275,
     "quote": "..."}, ...]`. The page shows "said 3 times" with each time.
   - `also`: ids of other branches a point bears on (a claim about reserves
     that matters to two positions).
   - `note` (shown) describes an action, e.g. "Voice D returned to the previous
     government's record". Drop small talk and procedure.
   The scripts work out each claim's state from the moves under it (not
   challenged, challenged with no reply, challenged and replied to, conceded);
   don't write it yourself.

6. **Moments.** Talk-overs and turns in the debate:
   `{"t": 402, "kind": "interruption", "by": "C", "of": "B", "note": "..."}`.
   Kinds: `interruption` (needs `by` and `of`), `crosstalk`, `topic_change`,
   `other`. Only mark what the captions show (cut-off sentences, "let me
   finish", a new voice mid-answer); crosstalk often garbles captions.

7. **Report.** `summary` (3 to 5 sentences: what was discussed and how it
   went), `takeaways` (3 to 6: what a viewer should notice), `actions` (2 to 5
   concrete things a viewer could do next: what to check, which question to
   ask), optional `left_open` (questions the debate raised and never settled).
   Describe the debate's actions; don't judge people.

8. **Check and render.** `python check.py debates/<id>` until it prints OK
   and the warnings are dealt with, then `python render.py debates/<id>`.
   Read the page once as someone on either side would. If either side would
   call a line unfair, rewrite it.

## map.json

```json
{
  "topic": "Neutral one-line question the debate is about",
  "voices": [
    {"id": "A", "role": "anchor", "basis": "Asks the questions and hands the floor"}
  ],
  "turns": [{"voice": "A", "start": 0, "end": 42.5}],
  "points": [
    {"id": "S1", "parent": null, "kind": "position", "text": "Defend a level with reserves"},
    {"id": "C1", "parent": "S1", "kind": "claim", "stance": "for",
     "said": [{"voice": "D", "t": 240, "quote": "..."}], "text": "Defending the rupee steadies import prices"},
    {"id": "C2", "parent": "C1", "kind": "claim", "stance": "challenges", "also": ["S2"],
     "said": [{"voice": "B", "t": 275}, {"voice": "C", "t": 700}], "text": "Defending a level spends reserves"},
    {"id": "Q1", "parent": "C2", "kind": "question", "stance": "challenges", "to": "D",
     "said": [{"voice": "A", "t": 320}], "text": "How many months of imports do reserves cover?",
     "outcome": "not_answered", "followed_up": false,
     "note": "Voice D spoke about the previous government instead", "label": "dodge"}
  ],
  "moments": [{"t": 95, "kind": "interruption", "by": "C", "of": "B", "note": "..."}],
  "report": {"summary": "...", "takeaways": ["..."], "actions": ["..."], "left_open": ["..."]}
}
```

Roles: `anchor`, `panelist`, `guest`, `audience`, `other`.

## Stats the page shows (computed, per voice)

Talk time and share, turns, talked over others, was talked over, questions
asked, questions put to them (answered, partly, no direct answer) and how many
of the unanswered ones were asked again. The last one, read across voices, shows
how the moderation went without anyone saying so.

## Limits

- No speaker labels in captions, so voices and every count are approximate.
- Crosstalk garbles auto-captions; the map is thinnest where it was loudest.
- No fact-checking: a claim on the map is what was said, not what is true.

---
name: dcore
description: Turn a debate, townhall or podcast transcript (or a YouTube link) into one calm HTML page showing what was claimed and how each point fared, a timeline of how the argument moved, and plain answers to a viewer's questions. Use when asked to map, break down, explain or report on a video debate or discussion.
---

# dcore

The reader is someone who missed the discussion and wants to know what happened:
what each side argued, what stood up, what fell away, and what was never
answered. You read the transcript and write one JSON object; `template.html`
turns it into the page. Don't write HTML or change the template.

There is no fact-checking. "Stands" means no one in the discussion knocked a
point down, not that it is true.

## Principles (non-negotiable)

- **Anonymous voices.** No names of people in the discussion, even when the
  video says them. Refer to a voice by its role in this discussion when that
  helps ("the anchor", "the ruling-party side", "the former official",
  "a panelist"). People who are talked about are named by office, not by name
  ("the CEC", "the opposition leader").
- **Actions, not labels.** Describe what happened, with a time: "Not
  answered; the reply turned to past elections." Never "dodged", "lied",
  "propaganda", "biased" or "hypocrite".
- **Take no sides.** No winner, no score, no verdict on a person or a side.
  Word every point the way its own speaker would accept.
- **Claims are reported, not endorsed.** "Said 13 crore names were removed",
  not "13 crore names were removed". A number that wasn't questioned is still
  only a claim.
- **Write in the reader's language.** Use the language of the person asking,
  whatever the transcript's language. Translate quotes faithfully.

## Steps

1. **Get the transcript.** Use pasted text or a file if you were given one.
   For a YouTube link, run
   `python .claude/skills/dcore/scripts/fetch.py <url> --out debates/<id>` and
   read `debates/<id>/transcript.txt`. If YouTube is blocked (common from
   cloud machines), ask for YouTube's "... > Show transcript" text or a
   `.vtt`/`.srt` file, then rerun with `--from <file> --lang <code>`. `<id>`
   is a short kebab-case slug of the topic.

2. **Read it all** before writing anything. Captions are often split into
   2-3 word lines; read them as running speech. Work out the voices from
   context: who asks and hands over the floor, who argues which line, who
   is addressed. Voices stay internal; the page never shows a voice list.

3. **Find the question and the options.** State the question the discussion
   was really about, as a neutral question (`topic`). Then name 2 or 3
   options people argued for, as short neutral phrases ("Resign now", "Wait
   for the commission's side"). Use the options the discussion actually
   weighed, even if the anchor framed it differently.

4. **Collect the points.** A point is one distinct claim that pushes for or
   against an option. Each distinct claim appears once, however many times
   it was repeated; merge repeats into its trail. Put it under the option it
   bears on most, as `for` or `against`. Aim for 2 to 5 points per side;
   leave out asides, greetings, and process talk. If an option had nothing
   raised against it, leave `against` empty.

5. **Trace each point.** `steps` is the trail that got the point where it
   ended, in time order, one short line each, starting with a verb or an
   outcome word: "Raised: ...", "Challenged: ...", "Asked: ...", "Answered:
   ...", "Not answered; ...", "Repeated ...", "Accepted by ...". Use the
   caption's start time (`m:ss` or `h:mm:ss`). Keep 1 to 6 steps; keep only
   steps that changed how the point stood.

6. **Decide where each point ended** (`end`), from the discussion alone:
   - `holds` (shown "stands"): another voice accepted or repeated it, or
     every challenge to it was answered and not pressed again.
   - `challenged` (shown "disputed"): a challenge was left standing without
     a reply, or the reply was itself disputed.
   - `fails` (shown "fell away"): its own side gave it up, or a challenge
     was accepted.
   - `open` (shown "never taken up"): no other voice engaged with it at
     all, or it was a question that was never answered.

   Then write `outcome`: the end state in a word or two, then the reason in
   one short sentence ("Disputed. No reply came.").

7. **Write each option's `lean`**: one neutral sentence on where the option
   stands as a whole ("Its main support fell away; the cost to families still
   stands."). Never say which option won.

8. **Pick the moments** for the timeline: 3 to 6 points where the argument
   changed direction, not every exchange. Each gets a short title, 1 to 3
   sentences, and a `shift` line saying what changed ("Falls away: ...",
   "Left disputed: ...", "Ends open: ..."). Mark at most one moment
   `"kind": "turn"` (the turning point) and at most one `"common"` (where
   people agreed); leave the rest `""`.

9. **Answer the viewer's questions.** Write 4 to 6 questions a viewer would
   ask, in their words, each answered in one or two sentences from the
   discussion alone, with an `answer` tag: `settled`, `leans yes`,
   `leans no`, `disputed` or `open`. Include at least one question the
   discussion left open.

10. **Build the page.** Copy `template.html` to `debates/<id>/index.html` and
    replace only the JSON inside `<script id="deliberation">`. Check that the
    JSON parses (`python -c "import json,sys; ..."` or similar) and that
    every point follows the rules above. Then share the page (publish it as
    an artifact when that tool is available), with one line saying what the
    discussion was about.

## JSON schema

```json
{
  "topic": "Should the CEC resign over the commissioners' objections?",
  "about": "A 21-minute Hindi TV panel: an anchor, a former official, two party spokespeople and an analyst.",
  "source": "From a pasted YouTube transcript.",
  "video": "https://www.youtube.com/watch?v=VIDEO_ID",
  "options": [
    {
      "title": "Resign now",
      "lean": "One neutral sentence on where this option stands.",
      "for": [
        {
          "say": "The point, in words its speaker would accept",
          "end": "holds | challenged | fails | open",
          "steps": [{ "t": "2:06", "did": "Raised: ..." }, { "t": "4:10", "did": "Challenged: ..." }],
          "outcome": "Disputed. No reply came."
        }
      ],
      "against": []
    }
  ],
  "moments": [
    { "t": "10:30", "title": "Short title", "text": "1-3 sentences.", "shift": "What changed.", "kind": "turn | common | (empty)" }
  ],
  "questions": [
    { "q": "A viewer's question?", "a": "One or two sentences.", "answer": "settled | leans yes | leans no | disputed | open" }
  ]
}
```

`video` is optional: when set, every timestamp opens the video at that
moment. `source` is a short line for the footer. The template ships with a
made-up sample; replace all of it.

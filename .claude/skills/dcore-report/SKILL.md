---
name: dcore-report
description: Turn a debate, discussion, panel or deliberation transcript (or a YouTube link) into a one-screen "60-second report card" for busy citizens - progress reached vs missed, where the time went, and how each voice did, with tap-to-expand detail. Use when asked for a report card, scorecard or accountability report on a discussion.
---

# dcore-report (60-second report card)

## Why this exists

Debates, discussions and deliberations are all conversations. Most end in shouting and slogans that people consume without thinking. This report shows a community what a conversation actually achieved, what it could have achieved if everyone had argued in good faith (keeping their own views), and who moved it forward or held it back.

The goal is a habit, not a document: people who are busy, with little time **and little attention**, should learn to ask "was the question answered, did anyone reply, did anyone agree?" instead of picking up the slogan. The report card also holds participants and the moderator accountable. It must never discourage disagreement, only irrational moves.

Think of a chess engine's game review: it doesn't tell you which side to play, it shows the better move you missed and what it cost.

## Principles (never break these)

- **Take no sides.** Grade moves, never positions. Anyone may argue for or against. Criticism should land on every side where it is earned, the moderator included.
- **Actions, not labels.** Describe what was done ("changed the subject"), never who someone is ("liar"). Name voices by role (Host, Ruling party, Opposition, Analyst, Former official, Resident 1...), not personal names.
- **The ideal is simulated.** The "could have" path is one plausible better path, not the truth. Say so in the footer.
- **Be accurate; don't overgeneralise.** "More distrust in elections", not "people stop trusting elections". Numbers quoted by speakers are unchecked unless you checked them; say so.
- **Be specific everywhere.** Every line must stand alone, because people skim and do not read cohesively. No "it", "they", "this" without the noun. Name the institution, the question, the thing.
- **Provenance for every judgement.** Each step, each dot, each time segment and each distraction must trace back to a timestamped moment in the real conversation. The page shows these behind toggles; `provenance.md` holds the rest.
- **Plain words only.** No jargon, and no fancy debate vocabulary either: say "Changed the subject", not "Red herring"; "Attacked motives, not the argument", not "Ad hominem".

## How this differs from `dcore`

`dcore` explains a discussion to someone who missed it and never judges people. `dcore-report` deliberately holds participants and the moderator accountable: it grades **moves** against a visible good-faith checklist and compares what happened with a simulated good-faith version. It still never labels a person or grades a position.

## Input

A transcript, ideally with timestamps (YouTube "Show transcript" text, .vtt/.srt, or pasted text). For a YouTube link, run `python .claude/skills/dcore/scripts/fetch.py <url> --out debates/<id>` (or `--from pasted.txt`) and read `debates/<id>/transcript.txt`; if YouTube is blocked, ask for the pasted transcript. If there are no timestamps, estimate from position in the text and say timings are approximate. If the transcript is in Hindi or another language, work from it directly and write the report in the language the user asks for (default English).

## Process

1. **Read the whole transcript.** Identify the central question, the voices (by role), and the context (what triggered the debate) in one or two sentences.
2. **Find what was settled.** Progress means only: a point all sides **agreed**, or a question that was **answered** (and the answer accepted or not challenged). On-topic talk that nobody engaged with is NOT progress.
3. **Simulate the good-faith version.** Same voices, same positions, but each one: answers the question asked, backs up a claim or says it's unchecked, doesn't repeat, gives ground when a point lands, argues the issue not motives or record, says what would change their mind; the moderator keeps their own view out and sums up. From this, list 2-4 **steps within reach** (agreements a fair panel could plausibly reach: a shared list of questions, a shared test, a condition, a next action). Mark each step reached or missed.
4. **Write consequences for each step.** For reached steps: "What this leads to" plus 1-2 lines. For missed steps: "Because <the miss>" followed by 2-3 lines that escalate ("So ... So ..."). Harm compounds non-linearly, so each line is a step worse. If two or more misses lead to the same end, write one shared **outcome** (accurate, not overgeneralised).
5. **Back each step with the real moments.** For every step, list the timestamped moments from the actual conversation that show it was reached, or how close the panel came and where it let go (role + what was said). Moments without a time are things nobody said ("The Opposition never said what would make it drop the demand"). Optionally add a list the panel could have signed, or a note on another step within reach. These are real, not simulated; they sit behind the step's "What was said on the night" toggle.
6. **Slice the time.** Walk through the transcript and assign every stretch to one of:
   - `fwd`: progress (agreed or answered)
   - `talk`: on topic, but nobody engaged
   - `side`: distraction
   - `idle`: intro, network trouble, goodbyes
   Record `[start_sec, end_sec, type]` segments covering the whole run time.
7. **List the distractions** two ways: (a) the kinds that occurred, as plain labels with an optional short gloss, no who-did-what, e.g. Changed the subject (instead of answering), Slogans and claims with no source, Attacked motives, not the argument, Mocked instead of answering, Host took a side (instead of moderating), Same point repeated, Moved the goalposts. Only list kinds that occurred. (b) Each instance with time, who, label, what happened and how long; these sit behind the "Who did what, and when" toggle.
8. **Find the biggest hidden loss.** Usually it is not the shouting but points left unanswered. Write it as a titled insight, naming one concrete example.
9. **Score each voice.** Count notable moves: green = moved it forward (answered, gave a checkable fact, conceded, proposed a fair test/condition, asked a specific question); red = held it back (changed the subject, overstated or unsupported claim, attacked motives or record, mocked, dodged or ignored a question; for the moderator also taking a side, letting detours run, not summing up). One dot = one timestamped move. For each red dot write the **better move** (keeping the same view) and its **cost**. Write a one-line remark per voice ("pushed for evidence, but took a side"), short enough to fit one line.
10. **Write the "next time you watch a debate, ask" questions** in two groups that teach people to spot what this report found. Default:
    - To spot a distraction: Was the question answered, or did the talk move to something else? / When someone made a strong claim, did they back it up, or just repeat it louder? / Did they argue the point, or attack and mock the other side? / Did the host ask questions, or argue for one side?
    - To spot talk that went nowhere: When someone made a point, did anyone reply to it? / Did anyone agree on anything, even one small fact? / At the end, did anyone say what was settled and what is still open?
    Don't ask about citing numbers; people rarely do.
11. **Write the provenance file** (`provenance.md`): every segment with a one-line reason, every dot with the rule it met or broke, plus the questions each side faced marked Answered / Dodged (replied but didn't answer) / Ignored, with the reply when there was one. Questions-each-side-faced stays in this file, not on the page.

## Output

Copy `template.html` to `debates/<id>/report.html` and replace only the JSON inside `<script id="report">` and the `<title>` (a 2 to 4 word name, such as "CEC Debate Report Card"). Don't change the rendering code or styles. Check that the JSON parses, then share the page (publish it as an artifact when that tool is available). Write `debates/<id>/provenance.md` next to it.

- The sample JSON already in `template.html` is a worked example: a Hindi TV panel on whether the Chief Election Commissioner should resign.
- The `//` notes in the shape below are explanations only; the real JSON must not contain them.

```json
{
  "eyebrow": "TV debate · 21 minutes · quick read · tap ▸ for detail",
  "question": "Should the Election Commission chief resign?",
  "context": "One or two plain sentences: what triggered the debate.",
  "steps_caption": "Three steps were within reach. The panel took one.",
  "steps": [
    {"status": "reached", "text": "Everyone agreed: ...", "because": "What this leads to", "chain": ["...", "So ..."],
     "detail": [{"heading": "Moments from the real debate", "items": [{"t": "7:49", "text": "Ruling party: \"...\""}]}]},
    {"status": "missed", "text": "Agree ...", "because": "Because no ... was agreed", "chain": ["...", "So ...", "So ..."],
     "detail": [
       {"heading": "The list both parties could have signed", "ordered": true, "items": ["Question 1?", "Question 2?"]},
       {"heading": "Moments from the real debate", "items": [{"t": "15:34", "text": "..."}, {"text": "Nobody said what would ..."}]},
       {"heading": "Also within reach", "note": "..."}
     ]}
  ],
  "outcome": "Shared end of the misses, accurate wording",
  "outcome_note": "Each step makes the next harder to undo. ...",
  "total_seconds": 1265,
  "segments": [[0, 28, "idle"], [28, 140, "talk"], [140, 223, "side"], [469, 615, "fwd"]],
  "distractions": [{"label": "Changed the subject", "gloss": "instead of answering"}, {"label": "Mocked instead of answering"}],
  "distraction_moments": [{"t": "5:34", "who": "Ruling party", "label": "Changed the subject", "what": "Listed the Opposition's election losses", "length": "1.8 min"}],
  "insight": {"title": "The biggest loss was not the shouting", "text": "..."},
  "voices": [{"name": "Host", "note": "pushed for evidence, but took a side",
    "forward": [{"t": "3:15", "what": "Asked \"how?\" when ..."}],
    "back": [{"t": "14:40", "what": "Argued a personal view that ...", "better": "Keep the host's own view out; ask ...", "cost": "The moderator became a debater ..."}]}],
  "ask": {"distraction": ["...4 questions..."], "nowhere": ["...3 questions..."]},
  "footer": "The missed steps come from a simulated better version of the same debate, not the truth. Each side keeps its view; only the arguing improves. Timings are approximate. Numbers quoted were not checked."
}
```

If the template file is not available, build the same page by hand in the school-marksheet look (ruled paper, red margin line, typewriter headings, handwritten red remarks and percentages, "REACHED"/"MISSED" rubber stamps), as one 640px column where the title, section headings and boxes share the same left and right edges:
- Header: eyebrow, question, context, double rule.
- "How far they got": reached steps (green ✓) then missed steps (red ✕). Each step shows its consequence chain on a vertical rail of dots that grow bigger and redder, and a "What was said on the night" toggle with the real moments. The shared outcome sits in a red stamped block below the misses.
- "Where the N minutes went": three horizontal bars with percentages (progress green, on topic but nobody engaged orange, distractions red), a line "The other X% was the intro and tech trouble". A "Minute by minute" toggle holds the timeline ribbon (same colours, idle black), axis and legend. Then a box listing the distraction kinds with a "Who did what, and when" toggle, and the insight callout.
- "Report card": one row per voice (name, a fixed-width column of green then red dots, one-line remark) so dots line up; each row is a toggle listing every move with its time, and for red moves the better move and the cost.
- "Next time you watch a debate, ask": the two question groups.
- Footer caveat.

## Format and tone rules (from the person who designed this)

- Lead with pictures; words are labels. Collapsed, the page must read in about a minute; detail lives behind toggles that open the corresponding long version in place.
- Compact boxes, so section headers stand out; headers and boxes aligned on one column.
- Red means bad or missed everywhere; green only for things that really happened and helped. Never show a missed step in green. Orange is on-topic talk nobody engaged with; black is intro and tech trouble.
- Consequences sit inside the step they follow from, never in a separate picture.
- Percentages are fine; never show numeric scores or grades for people. Dots and words instead.
- No who-did-what on the collapsed page: distraction kinds only; who/when sits behind the toggle.
- No link to a separate full report, and no tug of war, replay or checklist on the page.
- Before publishing, check: does each line stand alone? Is every judgement traceable to a real moment? Is any side spared criticism it earned? Is any wording overgeneralised or jargon?

## Reply to the user

Give the link and three lines: what the debate reached, the biggest miss, and the time split. Mention that "could have" is simulated and where the provenance file is.

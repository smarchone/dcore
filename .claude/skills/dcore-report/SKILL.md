---
name: dcore-report
description: Turn a debate, discussion, panel or deliberation transcript (or a YouTube link) into a one-screen "60-second report card" for busy citizens - progress reached vs missed and what that leads to, where the time went, and how each voice did. Use when asked for a report card, scorecard or accountability report on a discussion.
---

# dcore-report (60-second report card)

## Why this exists

Debates, discussions and deliberations are all conversations. Most end in shouting and slogans that people consume without thinking. This report shows a community what a conversation actually achieved, what it could have achieved if everyone had argued in good faith (keeping their own views), and who moved it forward or held it back.

The goal is a habit, not a document: people who are busy, with little time **and little attention**, should learn to ask "what was actually argued, what got dodged, what did it lead to?" instead of picking up the slogan. The report card also holds participants and the moderator accountable. It must never discourage disagreement, only irrational moves.

Think of a chess engine's game review: it doesn't tell you which side to play, it shows the better move you missed and what it cost.

## Principles (never break these)

- **Take no sides.** Grade moves, never positions. Anyone may argue for or against. Criticism should land on every side where it is earned, the moderator included.
- **Actions, not labels.** Describe what was done ("changed the subject"), never who someone is ("liar"). Name voices by role (Host, Ruling party, Opposition, Analyst, Former official, Resident 1...), not personal names.
- **The ideal is simulated.** The "could have" path is one plausible better path, not the truth. Say so in the footer.
- **Be accurate; don't overgeneralise.** "More distrust in elections", not "people stop trusting elections". Numbers quoted by speakers are unchecked unless you checked them; say so.
- **Be specific everywhere.** Every line must stand alone, because people skim and do not read cohesively. No "it", "they", "this" without the noun. Name the institution, the question, the thing.
- **Provenance for every judgement.** Each dot, each time segment and each distraction must trace back to a timestamped moment. Provenance goes in a separate file, not on the quick page.
- **Plain words.** No jargon on the page except named debate fallacies, which always carry a short plain gloss.

## How this differs from `dcore`

`dcore` explains a discussion to someone who missed it and never judges people. `dcore-report` deliberately holds participants and the moderator accountable: it grades **moves** against a visible good-faith checklist and compares what happened with a simulated good-faith version. It still never labels a person or grades a position.

## Input

A transcript, ideally with timestamps (YouTube "Show transcript" text, .vtt/.srt, or pasted text). For a YouTube link, run `python .claude/skills/dcore/scripts/fetch.py <url> --out debates/<id>` (or `--from pasted.txt`) and read `debates/<id>/transcript.txt`; if YouTube is blocked, ask for the pasted transcript. If there are no timestamps, estimate from position in the text and say timings are approximate. If the transcript is in Hindi or another language, work from it directly and write the report in the language the user asks for (default English).

## Process

1. **Read the whole transcript.** Identify the central question, the voices (by role), and the context (what triggered the debate) in one or two sentences.
2. **Find what was settled.** Progress means only: a point all sides **agreed**, or a question that was **answered** (and the answer accepted or not challenged). On-topic talk that nobody engaged with is NOT progress.
3. **Simulate the good-faith version.** Same voices, same positions, but each one: answers the question asked, gives a source or says it's unchecked, doesn't repeat, gives ground when a point lands, argues the issue not motives or record, says what would change their mind; the moderator keeps their own view out and sums up. From this, list 2-4 **steps within reach** (agreements a fair panel could plausibly reach: a shared list of questions, a shared test, a condition, a next action). Mark each step reached or missed.
4. **Write consequences for each step.** For reached steps: what this leads to (1-2 lines). For missed steps: "Because <the miss>" followed by 2-3 lines that escalate ("So ... So ..."). Harm compounds non-linearly, so each line is a step worse. If two or more misses lead to the same end, write one shared **outcome** (accurate, not overgeneralised).
5. **Slice the time.** Walk through the transcript and assign every stretch to one of:
   - `fwd`: progress (agreed or answered)
   - `talk`: on topic, but nobody engaged
   - `side`: distraction
   - `idle`: intro, network trouble, goodbyes
   Record `[start_sec, end_sec, type]` segments covering the whole run time.
6. **Name the distractions by type,** using formal debate and argumentation terms, each with a short plain gloss and no who-did-what. Typical: Red herring, Whataboutism, Ad hominem, Appeal to ridicule, Straw man, Unsupported claims and loaded language, Moving the goalposts, Gish gallop, Moderator bias. Only list types that actually occurred.
7. **Find the biggest hidden loss.** Usually it is not the shouting but points left unanswered. Write it as a titled insight, naming one concrete example.
8. **Score each voice.** Count notable moves: green = moved it forward (answered, gave a checkable fact, conceded, proposed a fair test/condition, asked a specific question); red = held it back (changed the subject, overstated or unsourced claim, attacked motives or record, mocked, dodged or ignored a question; for the moderator also taking a side, letting detours run, not summing up). One dot = one timestamped move in the provenance file. Write a one-line remark per voice ("pushed for evidence, but took a side"), short enough to fit one line.
9. **Write three "next time you watch a debate, ask" questions** that build the habit (default: Did they answer the question asked? Did they say where a number came from? Did anyone agree on anything?).
10. **Write the provenance file** (`provenance.md`): every step with the moments behind it, every segment with a one-line reason, every distraction instance with who/when/what, every dot with who/when/what and the rule it met or broke, plus the questions each side faced marked Answered / Dodged (replied but didn't answer) / Ignored, with the reply when there was one.

## Output

Copy `template.html` to `debates/<id>/report.html` and replace only the JSON inside `<script id="report">` and the `<title>` (a 2 to 4 word name, such as "CEC Debate Report Card"). Don't change the rendering code or styles. Check that the JSON parses, then share the page (publish it as an artifact when that tool is available). Write `debates/<id>/provenance.md` next to it.

- The sample JSON already in `template.html` is a worked example: a Hindi TV panel on whether the Chief Election Commissioner should resign.
- The `//` notes in the shape below are explanations only; the real JSON must not contain them.

```json
{
  "style": "marksheet",            // "marksheet" (school report card look, preferred) or "plain"
  "eyebrow": "TV debate · 21 minutes · quick read",
  "question": "Should the Election Commission chief resign?",
  "context": "One or two plain sentences: what triggered the debate.",
  "steps_caption": "Three steps were within reach. The panel took one.",
  "steps": [
    {"status": "reached", "text": "Everyone agreed: ...", "because": "What this leads to", "chain": ["...", "So ..."]},
    {"status": "missed", "text": "Agree ...", "because": "Because no ... was agreed", "chain": ["...", "So ...", "So ..."]}
  ],
  "outcome": "Shared end of the misses, accurate wording",
  "outcome_note": "Each step makes the next harder to undo. ...",
  "total_seconds": 1265,
  "segments": [[0, 28, "idle"], [28, 140, "talk"], [140, 223, "side"], [469, 615, "fwd"]],
  "distractions": [{"term": "Red herring", "gloss": "switching to an unrelated topic instead of answering"}],
  "insight": {"title": "The biggest loss was not the shouting", "text": "..."},
  "voices": [{"name": "Host", "forward": 3, "back": 3, "note": "pushed for evidence, but took a side"}],
  "ask": ["Did they answer the question asked?", "Did they say where a number came from?", "Did anyone agree on anything?"],
  "footer": "The missed steps come from a simulated better version of the same debate, not the truth. Each side keeps its view; only the arguing improves. Timings are approximate. Numbers quoted were not checked.",
  "full_report_url": "",            // optional link to a fuller report
  "full_report_label": "Read the full report"
}
```

If the template file is not available, build the same page by hand: header (eyebrow, question, context); "How far they got" with reached steps (green ✓) and missed steps (red ✕), each with its consequence chain on a vertical rail of dots that grow bigger and redder, and the shared outcome in a red block below the misses; "Where the N minutes went" as one horizontal ribbon (green progress, grey-blue on topic but unengaged, red distractions, light grey idle), three big percentages, a light-red box listing distraction types, and the insight callout; "Report card" with one row per voice (name, a fixed-width column of green then red dots, one-line remark) so dots line up; the "next time you watch, ask" box; footer.

## Format and tone rules (from the person who designed this)

- Lead with pictures; words are labels. Keep it to roughly one phone screen per section, phone-first.
- Red means bad or missed everywhere; green only for things that really happened and helped. Never show a missed step in green.
- Consequences sit inside the step they follow from, never in a separate picture.
- Percentages are fine; never show numeric scores or grades for people. Dots and words instead.
- No who-did-what on the quick page: distractions are types, questions-each-side-faced and the who/when lists belong in the provenance or full report.
- Before publishing, check: does each line stand alone? Is every judgement traceable? Is any side spared criticism it earned? Is any wording overgeneralised?

## Reply to the user

Give the link and three lines: what the debate reached, the biggest miss, and the time split. Mention that "could have" is simulated and where the provenance file is.

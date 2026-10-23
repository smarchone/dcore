# Building the page

Copy `template.html` to `debates/<id>/citizen.html` and replace only the JSON
inside `<script id="report">` and the `<title>` (a 2 to 4 word name, such as
"CEC Citizen Report"). Don't change the rendering code or styles. The template
ships with a worked example (a Hindi TV panel on whether the Chief Election
Commissioner should resign); replace all of it.

`template-compact.html` is a variant that reads the same JSON: summary tiles,
one line per step, a single stacked time bar, thin thread rows, plain type.
Use it instead when the user asks for the compact page.

Check that the JSON parses and that every `thread` field names an `id` in
`threads`. The `//` notes below are explanations only; the real JSON must not
contain them.

## Limits

- 3 to 6 threads.
- `progress`: every reached step, plus 2 to 4 missed steps.
- Consequence `chain`: 1 to 2 lines for reached, 2 to 3 for missed.
- Replay: 3 to 6 lines; one per thread that ended `stuck` or `dropped`.
- Thread `flow`: 2 to 7 moments, only the ones that changed where the thread
  stood.

## Shape

```json
{
  "eyebrow": "TV debate · 21 minutes · quick read · tap any row for detail",
  "question": "Should the Election Commission chief resign?",
  "context": "One or two plain sentences: what triggered the conversation.",

  "progress_caption": "Five steps were within reach. The panel took two.",
  "progress": [
    {"status": "reached", "thread": "explain",
     "text": "Everyone agreed: the Commission must explain itself in public",
     "because": "What this leads to", "chain": ["...", "So ..."],
     "detail": [{"heading": "Moments from the real debate", "items": [{"t": "7:49", "text": "Ruling party: \"...\""}]}]},
    {"status": "missed", "thread": "questions",
     "text": "Agree a list of questions the Commission must answer",
     "lost": {"t": "16:29", "label": "Changed the subject"},   // when and how it slipped; label from definitions.md, or "Nobody took it up"
     "because": "Because no list was agreed", "chain": ["...", "So ...", "So ..."],
     "detail": [
       {"heading": "The list both sides could have signed", "ordered": true, "items": ["Question 1?"]},
       {"heading": "Moments from the real debate", "items": [{"t": "15:34", "text": "..."}, {"text": "Nobody said ..."}]},
       {"heading": "Also within reach", "note": "..."}
     ]}
  ],
  "outcome": "Shared end of the misses, accurate wording",
  "outcome_note": "Each step makes the next harder to undo.",

  "total_seconds": 1265,
  // [start_sec, end_sec, type, thread id or "", label (only for "side")]; covers the whole run time
  "segments": [[0, 28, "idle", "", ""], [140, 223, "side", "rigging", "Slogans and numbers with no source"]],

  "threads": [
    {"id": "majority", "title": "Why didn't the two commissioners use their majority?",
     "end": "converged | clarified | bounded | stuck | dropped",
     "summary": "One line: where the thread got to.",
     "pulled": "One line: where distractions pulled it off course (or that nothing did).",
     "flow": [{"t": "10:43", "mark": "talk", "text": "Former CEC asked ..."}, {"t": "13:46", "mark": "side", "text": "Opposition moved to ..."}],
     // mark: fwd | talk | gap | side; a moment with no "t" is something nobody said
     "replay": {"from": "13:46", "lines": [{"who": "Opposition", "says": "..."}], "ends": "clarified", "note": "Optional one line."}}
  ],

  // the conduct ledger: one entry per distraction, the only source for red dots from distractions
  "distractions": [
    {"t": "13:46", "who": "Opposition", "kind": "dodge | unprompted", "label": "Changed the subject",
     "thread": "majority", "victim": "The former CEC's question about the commissioners' majority",  // dodges only
     "what": "Brought up a scarf worn at a Bihar victory event", "length": "27 sec",
     "better": "Answer it, or say ...", "cost": "The strongest challenge ... was never addressed"}
  ],

  // weighty bids that got no reply at all; each becomes an orange dot for its owner
  "moderator": "Host",    // owner of bids aimed at nobody in particular
  "unanswered": [
    {"t": "9:46", "by": "Analyst", "to": "",   // "to": the voice it was aimed at, or "" for the whole panel
     "thread": "test", "bid": "Proposed the files test: show majority or full approval behind each disputed order",
     "matters": true,     // could have led to a step within reach
     "cost": "The one test on the table was left alone"}   // optional; worth writing when "matters"
  ],

  // answers that engaged with a bid but left a specific part open; each becomes a hollow orange dot for the answerer ("to")
  "gaps": [
    {"t": "12:10", "by": "Host", "to": "Ruling party", "thread": "questions",
     "bid": "Asked when the disputed files will be made public",
     "answer": "Said the Commission is committed to transparency",
     "label": "Gave intent, not the fact asked for",   // label from definitions.md
     "gap": "Asked for a date; gave a commitment, not a date",   // one line, in the asker's terms
     "follow_up": "So by what date will the files be public?",   // the move that would have closed it
     "matters": true,
     "cost": "The release stayed an open promise"}   // optional; worth writing when "matters"
  ],

  "insight": {"title": "The biggest loss was not the shouting", "text": "..."},

  // orange dots = unanswered bids this voice owns; hollow orange = gaps where this voice is "to"; red dots = this voice's distractions (matched by "who") + "missed" (omissions)
  "voices": [
    {"name": "Host", "note": "pushed for evidence, but took a side",
     "forward": [{"t": "3:15", "what": "Asked \"how?\" when ..."}],
     "missed": [{"t": "20:56", "what": "Closed without summing up", "better": "...", "cost": "..."}]}
  ],

  "ask": {"distraction": ["..."], "nowhere": ["..."]},
  "youtube": "",          // the video link, if any; timestamps then open the video at that second
  "transcript": [[0, "First ~20 seconds of the raw transcript"]],  // only when there is no YouTube link
  "footer": "The replays and missed steps show one fair way the same debate could have gone, not what happened. ..."
}
```

The page computes the time shares, the share of each distraction label, and
each thread's lane from `segments`, so keep segments, `flow` and
`distractions` consistent: a distraction at 13:46 should sit inside a `side`
segment with the same label and thread.

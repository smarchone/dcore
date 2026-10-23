---
name: dcore-citizen
description: Turn a debate, panel, townhall or deliberation transcript (or a YouTube link) into a one-minute citizen report that follows each thread of the conversation - what progress was made, what was missed because of distractions and what that cost, where the time went by distraction type, who pulled each thread off course (with timestamps), and a simulated replay of one fair path per thread. Use when asked for a citizen report, distraction analysis, thread analysis or missed-opportunity report on a discussion.
---

# dcore-citizen

A conversation is several threads running side by side, like rivers. Each
thread either reaches somewhere (agreement, or a clearer disagreement) or
gets pulled off course by distractions. This report follows each thread and
shows a busy citizen, in about a minute:

- **Progress.** The good: what was reached. The bad: what was within reach
  and missed, which distraction cost it, and what that leads to.
- **Distractions.** How much of the time went to them, by label; each thread
  with its distractions laid over it; who made each one, with the timestamp.
- **Replay.** For a thread that got stuck or dropped, one fair way it could
  have gone with the same voices and views.

Think of a chess engine's game review: it doesn't tell you which side to
play. It shows the better move you missed and what it cost.

## Files

The steps below stay fixed. The parts you tune live in their own files; read
all four before starting:

- `definitions.md`: what a thread, a bid, a distraction and progress are, and
  the plain labels the page uses.
- `judgement.md`: how each call is made (dodges, missed steps, replays, time).
- `tone.md`: principles, wording, and what makes the page effortless to read.
- `schema.md`: the JSON the page is built from, and its limits.

If one of these files contradicts this one, the specific file wins for its
subject.

## Input

A transcript, ideally with timestamps (YouTube "Show transcript" text,
.vtt/.srt, or pasted text). For a YouTube link, run
`python .claude/skills/dcore/scripts/fetch.py <url> --out debates/<id>` (or
`--from pasted.txt`) and read `debates/<id>/transcript.txt`; if YouTube is
blocked, ask for the pasted transcript. If there are no timestamps, estimate
from position in the text and say timings are approximate. Work from the
transcript in its own language; write the report in the language the user asks
for (default English).

## Steps

1. **Read the whole transcript.** Note the central question, the voices (by
   role), and what triggered the conversation, in one or two sentences.
2. **Split it into threads.** Name 3 to 6 threads by their questions. Link
   returns to a thread across gaps.
3. **Mark the moves.** Walk through each thread in time order. Mark every bid
   (question or point) and whether it was engaged with, every good move, and
   every distraction with its kind and label (`definitions.md`), who made it,
   and which thread it pulled away from. List every weighty bid that got no
   reply at all, with its owner, and every answer that left a gap, with the
   follow-up that would have closed it (`judgement.md`).
4. **Decide where each thread ended** (`converged`, `clarified`, `bounded`,
   `stuck`, `dropped`), and write one line on where it got to and one on
   where it was pulled off course.
5. **Find the missed steps.** At each distraction and each bid nobody took
   up, ask what progress was one or two moves away using only what had been
   said so far (`judgement.md`). Keep the 2 to 4 that matter most, each with
   the moment it was lost.
6. **Write the consequences** for every reached and missed step, and the
   shared outcome if misses lead to the same end.
7. **Replay** each `stuck` or `dropped` thread from the moment it went wrong:
   3 to 6 lines by role, ending in the state the replay reaches.
8. **Slice the time.** Cover the whole run time with segments (`fwd`, `talk`,
   `side`, `idle`), each carrying its thread, and a label for `side`.
9. **Fill the voices.** Good moves as green dots; omissions as red dots with
   the better move and its cost. Distractions become red dots, and unanswered
   bids orange dots and gaps hollow orange dots, automatically from their
   lists.
10. **Name the biggest hidden loss** as a titled insight with one concrete
    example (usually a thread dropped without any shouting).
11. **Write the "next time you watch, ask" questions** that teach the reader to
    spot what this report found. Default:
    - To spot a distraction: Was the question answered, or did the talk move
      to something else? / Did the answer cover what was asked, or only part of
      it, or a promise? / When someone made a strong claim, did they back it
      up, or just repeat it louder? / Did they argue the point, or attack and
      mock the other side? / Did the host ask questions, or argue for one
      side?
    - To spot talk that went nowhere: When someone made a point, did anyone
      reply to it? / When a question was dropped, did anyone bring it back? /
      At the end, did anyone say what was settled and what is still open?
12. **Link every timestamp to its source.** Put the video link in `youtube`.
    Without one, put the raw transcript in `transcript` as `[start_sec, text]`
    chunks (`python3 .claude/skills/dcore-report/transcript_chunks.py
    debates/<id>/transcript.txt` prints them for `[m:ss] text` lines).
13. **Build the page** as `schema.md` says, then run the checks in `tone.md`.
14. **Write `debates/<id>/citizen-provenance.md`**: each thread with every
    marked move and its time; every segment with a one-line reason; every
    distraction with the rule it met; every bid marked Engaged / Dodged /
    Nobody took it up; and the reasoning behind each missed step.

## Output

`debates/<id>/citizen.html` and `debates/<id>/citizen-provenance.md`. Keep
the page local: don't publish it as an artifact or share it unless the user
asks. Open it in the browser with `open debates/<id>/citizen.html`.

## Reply to the user

Give the file path and three lines: what was reached, the biggest miss and what
cost it, and the share of time lost to distractions. Mention that the replays
are one fair path, not what happened, and where the provenance file is.

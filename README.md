# dcore

The [`dcore`](.claude/skills/dcore/SKILL.md) skill turns a
debate, panel, townhall or deliberation transcript (or a YouTube link) into a
one-minute report for a busy citizen. It follows each thread of the
conversation, like a chess engine's game review: it doesn't say which side to
take, it shows the better move that was missed and what it cost.

- **Progress:** what each thread reached (agreed, clearer, agreed to differ)
  and what was one or two moves away but missed, with when it slipped, how,
  and what that leads to.
- **Distractions:** how much of the run time went to them, by plain label
  ("changed the subject", "host took a side"), who made each one, with
  timestamps.
- **Left open:** points nobody replied to, and answers that left a gap.
- **Replay:** for each stuck or dropped thread, one fair way it could have
  gone with the same voices and views.
- **Accountability:** each voice's good moves and misses as dots, never a
  score, each miss with the better move and its cost.

It grades moves, never positions. Every timestamp links to the video at that
second, and every judgement traces to a moment in a provenance file.

**Example:** [`docs/examples/civic-sense/`](docs/examples/civic-sense/) is the
report on a WTF Discourse studio debate, "Indian cities are broken because
Indians lack civic sense" ([video](https://www.youtube.com/watch?v=rBPLwZI5whY)):
the [page](docs/examples/civic-sense/citizen.html) and its
[provenance](docs/examples/civic-sense/citizen-provenance.md). Open the page in
a browser.

## Run it

In Claude Code, from this repo:

```
/dcore https://www.youtube.com/watch?v=<id>
```

Claude fetches the captions, writes `debates/<id>/citizen.html` and
`debates/<id>/citizen-provenance.md`, and opens the page. Add "upload to
artifact" to also publish it as a private claude.ai artifact.

To fetch captions yourself (needs `youtube-transcript-api` 1.x):

```bash
uv run --python 3.12 --with "youtube-transcript-api>=1.0" \
  python .claude/skills/dcore/scripts/fetch.py <youtube-url> --out debates/<id>
# or, with a pasted transcript or .vtt/.srt:
python .claude/skills/dcore/scripts/fetch.py <youtube-url> --out debates/<id> --from pasted.txt
```

## How it's built

Claude reads the transcript and writes one JSON object into a copy of
[`template-compact.html`](.claude/skills/dcore/template-compact.html)
([`template.html`](.claude/skills/dcore/template.html) is the fuller
variant); there's no other build step. The parts you tune live beside
`SKILL.md`:

| File | Holds |
| --- | --- |
| `definitions.md` | What a thread, bid, distraction and progress are; the page's labels |
| `judgement.md` | How each call is made: dodges, gaps, missed steps, replays, time |
| `tone.md` | Principles, wording, and the pre-publish checks |
| `schema.md` | The JSON the page is built from, and its limits |

`scripts/transcript_chunks.py` turns `[m:ss] text` lines into transcript
chunks for pages without a video link. Nothing is fact-checked: numbers are
reported as speakers said them.

Tests: `uv run --with pytest pytest -q tests`.

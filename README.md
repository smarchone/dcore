# dcore

The [`dcore`](.claude/skills/dcore/SKILL.md) skill turns a debate, townhall or
podcast transcript (or a YouTube link) into one calm HTML page for someone who
missed it:

- **How each point fared:** for each option argued, the points for and against
  it, each with a short timestamped trail and where it ended (stands, disputed,
  fell away, never taken up).
- **Timeline:** the few moments where the argument changed direction.
- **Your questions, answered:** plain answers to what a viewer would ask.

Claude reads the transcript and writes one JSON object into a copy of
[`template.html`](.claude/skills/dcore/template.html); there's no other build
step. `scripts/fetch.py` is optional plumbing that gets YouTube captions or
reads a pasted transcript. It doesn't fact-check.

```bash
python .claude/skills/dcore/scripts/fetch.py <youtube-url> --out debates/<id>   # or --from pasted.txt
# Claude writes debates/<id>/index.html from the template (see the skill)
```

Tests: `pip install pytest && pytest -q tests`.

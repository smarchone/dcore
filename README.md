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

## dcore-report

The [`dcore-report`](.claude/skills/dcore-report/SKILL.md) skill turns the same
kind of transcript into a one-screen report card for busy citizens:

- **How far they got:** the steps a good-faith panel could have reached, each
  marked reached or missed, with what each one leads to.
- **Where the time went:** progress, on-topic talk nobody engaged with, and
  distractions (named by type: red herring, ad hominem and so on).
- **Report card:** each voice's moves that moved the debate forward or held it
  back, traced to timestamps in a separate `provenance.md`.

Unlike `dcore`, it grades moves (never positions) to hold participants and the
moderator accountable. The "could have" part is a simulated good-faith version,
labelled as such. Claude fills the JSON in
[`template.html`](.claude/skills/dcore-report/template.html), as with `dcore`.

Tests: `pip install pytest && pytest -q tests`.

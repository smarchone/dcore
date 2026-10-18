# dcore

The [`dcore`](.claude/skills/dcore/SKILL.md) skill turns a recorded debate,
townhall or podcast on YouTube into one HTML page: each distinct claim once,
as a branch with its challenges, replies and questions (each timestamped and
linked into the video), plus a "how this debate went" report with per-voice stats.

Claude does the judging; three small stdlib scripts do the plumbing. `fetch.py`
gets captions or reads a pasted transcript, `check.py` validates the map and
counts the stats, and `render.py` draws the page. It doesn't fact-check.

```bash
S=.claude/skills/dcore/scripts
python $S/fetch.py <youtube-url> --out debates/<id>     # or --from pasted.txt
# Claude writes debates/<id>/map.json (see the skill)
python $S/check.py debates/<id>
python $S/render.py debates/<id>                         # debates/<id>/page.html
```

Tests: `pip install pytest && pytest -q tests`.

"""Check a debate map (debates/<id>/map.json) against its transcript.

    python check.py debates/my-debate

Errors stop the render; warnings are worth a look. Also computes the per-voice
stats the page shows, so the counts always come from the map, never by hand.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# A map is a tree of branches: the topic at the root, positions (the answers on
# offer), claims under them, and the moves made on each claim.
KINDS = {"position", "claim", "question"}
# How a point relates to its parent.
STANCES = {"for", "against", "supports", "challenges", "answers", "concedes"}
OUTCOMES = {"answered", "partly", "not_answered"}
MOMENT_KINDS = {"interruption", "crosstalk", "topic_change", "other"}
ROLES = {"anchor", "panelist", "guest", "audience", "other"}

# Words that judge a person instead of describing what they did. They may sit
# in a point's private "label", never in text the page shows.
LABEL_WORDS = re.compile(
    r"\b(liar|lied|lying|lies|dodg\w*|evad\w*|evasive|propagand\w*|biased|"
    r"dishonest|hypocri\w*|shameful|disgrace\w*|winner|loser|"
    r"misleading|sycophan\w*|godi|anti-national|troll\w*)\b",
    re.I,
)
SHOWN = ("text", "note")


def load(folder: Path) -> tuple[dict, dict]:
    tr = json.loads((folder / "transcript.json").read_text(encoding="utf-8"))
    m = json.loads((folder / "map.json").read_text(encoding="utf-8"))
    return tr, m


def check(tr: dict, m: dict) -> tuple[list[str], list[str]]:
    err: list[str] = []
    warn: list[str] = []
    dur = float(tr["duration"]) + 5

    for key in ("topic", "voices", "turns", "points", "report"):
        if key not in m:
            err.append(f"missing {key!r}")
    if err:
        return err, warn

    voices = {}
    for v in m["voices"]:
        if v.get("id") in voices:
            err.append(f"voice {v.get('id')} listed twice")
        voices[v.get("id")] = v
        if v.get("role") not in ROLES:
            err.append(f"voice {v.get('id')}: role must be one of {sorted(ROLES)}")
        if not v.get("basis"):
            warn.append(f"voice {v.get('id')}: say what the voice was inferred from in 'basis'")
        if v.get("name"):
            warn.append(f"voice {v.get('id')}: has a name; this skill keeps voices anonymous")

    def voice_ok(where: str, vid, allow_none=False):
        if vid is None and allow_none:
            return
        if vid not in voices:
            err.append(f"{where}: unknown voice {vid!r}")

    def time_ok(where: str, t):
        if not isinstance(t, (int, float)) or t < 0 or t > dur:
            err.append(f"{where}: time {t!r} is outside the video (0 to {int(dur)}s)")

    last = -1.0
    for i, t in enumerate(m["turns"]):
        w = f"turn {i + 1}"
        voice_ok(w, t.get("voice"))
        time_ok(w, t.get("start"))
        time_ok(w, t.get("end"))
        if isinstance(t.get("start"), (int, float)) and isinstance(t.get("end"), (int, float)):
            if t["end"] <= t["start"]:
                err.append(f"{w}: ends before it starts")
            if t["start"] < last - 0.5:
                err.append(f"{w}: starts before the previous turn ends; turns must be in order")
            last = max(last, t["end"])

    pts = {}
    for p in m["points"]:
        pid = p.get("id")
        if not pid or pid in pts:
            err.append(f"point id {pid!r} is missing or repeated")
        pts[pid] = p
    for pid, p in pts.items():
        w = f"point {pid}"
        kind = p.get("kind")
        if kind not in KINDS:
            err.append(f"{w}: kind must be one of {sorted(KINDS)}")
        if not p.get("text"):
            err.append(f"{w}: needs text")
        par = p.get("parent")
        if par is not None and par not in pts:
            err.append(f"{w}: parent {par!r} doesn't exist")
        if kind == "position":
            if par is not None:
                err.append(f"{w}: a position sits at the top, under the topic (parent null)")
        else:
            if par is not None and p.get("stance") not in STANCES:
                err.append(f"{w}: stance must be one of {sorted(STANCES)}")
            if not p.get("said"):
                err.append(f"{w}: 'said' needs at least one {{voice, t}} for when it was said")
        for j, s_ in enumerate(p.get("said") or []):
            voice_ok(f"{w} said[{j}]", s_.get("voice"))
            time_ok(f"{w} said[{j}]", s_.get("t"))
        for a in p.get("also") or []:
            if a not in pts:
                err.append(f"{w}: also {a!r} doesn't exist")
        if kind == "question":
            voice_ok(f"{w} 'to'", p.get("to"), allow_none=True)
            if p.get("outcome") not in OUTCOMES:
                err.append(f"{w}: a question needs outcome, one of {sorted(OUTCOMES)}")
            answered = any(c.get("parent") == pid and c.get("stance") == "answers" for c in pts.values())
            if p.get("outcome") in ("answered", "partly") and not answered:
                warn.append(f"{w}: add the answer as a point under it with stance 'answers'")
            if p.get("outcome") != "answered" and "followed_up" not in p:
                warn.append(f"{w}: say whether anyone came back to it in 'followed_up'")
        for k in SHOWN:
            hit = LABEL_WORDS.search(p.get(k) or "")
            if hit:
                warn.append(f"{w}: '{hit.group(0)}' in {k} reads as a label; describe the action instead")

    # Parent chains must not loop.
    for pid in pts:
        seen, cur = set(), pid
        while cur is not None:
            if cur in seen:
                err.append(f"point {pid}: parent chain loops")
                break
            seen.add(cur)
            cur = pts.get(cur, {}).get("parent")

    for i, mo in enumerate(m.get("moments", [])):
        w = f"moment {i + 1}"
        if mo.get("kind") not in MOMENT_KINDS:
            err.append(f"{w}: kind must be one of {sorted(MOMENT_KINDS)}")
        time_ok(w, mo.get("t"))
        voice_ok(f"{w} 'by'", mo.get("by"), allow_none=True)
        voice_ok(f"{w} 'of'", mo.get("of"), allow_none=True)
        if mo.get("kind") == "interruption" and not (mo.get("by") and mo.get("of")):
            err.append(f"{w}: an interruption needs 'by' and 'of'")
        hit = LABEL_WORDS.search(mo.get("note") or "")
        if hit:
            warn.append(f"{w}: '{hit.group(0)}' in note reads as a label; describe the action instead")

    rep = m["report"]
    for k in ("summary", "takeaways", "actions"):
        if not rep.get(k):
            err.append(f"report: needs {k!r}")
    for k, val in rep.items():
        for line in [val] if isinstance(val, str) else val or []:
            hit = LABEL_WORDS.search(line if isinstance(line, str) else "")
            if hit:
                warn.append(f"report {k}: '{hit.group(0)}' reads as a label; describe the action instead")

    if not any(p.get("kind") == "question" for p in pts.values()):
        warn.append("no questions marked; the answered/unanswered counts will be empty")
    return err, warn


def stats(tr: dict, m: dict) -> list[dict]:
    """Per-voice actions, counted from the map. Approximate: voices are inferred."""
    rows = {v["id"]: {"voice": v["id"], "role": v["role"], "seconds": 0.0, "turns": 0,
                      "interrupted_others": 0, "was_interrupted": 0, "asked": 0,
                      "put_to": 0, "answered": 0, "partly": 0, "not_answered": 0,
                      "followed_up": 0}
            for v in m["voices"]}
    for t in m["turns"]:
        r = rows[t["voice"]]
        r["seconds"] += t["end"] - t["start"]
        r["turns"] += 1
    for mo in m.get("moments", []):
        if mo["kind"] == "interruption":
            rows[mo["by"]]["interrupted_others"] += 1
            rows[mo["of"]]["was_interrupted"] += 1
    for p in m["points"]:
        if p["kind"] != "question":
            continue
        rows[p["said"][0]["voice"]]["asked"] += 1
        to = p.get("to")
        if to:
            r = rows[to]
            r["put_to"] += 1
            r[p["outcome"]] += 1
            if p["outcome"] != "answered" and p.get("followed_up"):
                r["followed_up"] += 1
    total = sum(r["seconds"] for r in rows.values()) or 1
    for r in rows.values():
        r["share"] = r["seconds"] / total
    return list(rows.values())


def state(m: dict, pid: str) -> tuple[str, str]:
    """Where a claim stands in the discourse, from the moves under it.

    Not whether it's true: only whether it was challenged and whether anyone
    came back to the challenge. Returns (key, words).
    """
    kids = [p for p in m["points"] if p.get("parent") == pid]
    if any(k.get("stance") == "concedes" for k in kids):
        return "conceded", "Conceded"
    chal = [k for k in kids if k.get("stance") == "challenges"]
    if not chal:
        return "clear", "Not challenged"
    replied = [c for c in chal if any(p.get("parent") == c["id"] for p in m["points"])]
    if len(replied) == len(chal):
        return "replied", "Challenged, replied to"
    return "open", "Challenged, no reply"


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__)
        return 2
    tr, m = load(Path(argv[0]))
    err, warn = check(tr, m)
    for w in warn:
        print("warning:", w)
    for e in err:
        print("error:", e)
    if not err:
        print(f"OK: {len(m['points'])} points, {len(m['voices'])} voices, {len(m.get('moments', []))} moments")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())

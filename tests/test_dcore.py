"""Tests for the dcore skill: transcript parsing and the page template's sample data."""

import json
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1] / ".claude/skills/dcore"
sys.path.insert(0, str(SKILL / "scripts"))
import fetch  # noqa: E402

def test_video_id_forms():
    for u in ["abcdefghijk", "https://youtu.be/abcdefghijk?t=3",
              "https://www.youtube.com/watch?v=abcdefghijk&t=10s",
              "https://www.youtube.com/live/abcdefghijk"]:
        assert fetch.video_id(u) == "abcdefghijk"


def test_parse_panel_both_layouts():
    two_line = "0:00\nnamaste\n0 seconds\n0:05\naaj ki bahas\n1:02:03\nend"
    segs = fetch.parse_given(two_line)
    assert [s["start"] for s in segs] == [0, 5, 3723]
    assert segs[1]["text"] == "aaj ki bahas" and segs[0]["dur"] == 5
    one_line = fetch.parse_given("0:00 hello there\n0:04 next line\ncontinued")
    assert one_line[1]["text"] == "next line continued"


def test_parse_vtt_drops_repeats():
    vtt = ("WEBVTT\n\n00:00:01.000 --> 00:00:03.500\n<c>hello</c>\n\n"
           "00:00:03.500 --> 00:00:05.000\nhello\n\n00:00:05.000 --> 00:00:07.000\nworld\n")
    segs = fetch.parse_given(vtt)
    assert [(s["start"], s["text"]) for s in segs] == [(1.0, "hello"), (5.0, "world")]


def sample():
    html = (SKILL / "template.html").read_text(encoding="utf-8")
    start = html.index('<script id="deliberation" type="application/json">')
    body = html[html.index(">", start) + 1:html.index("</script>", start)]
    return json.loads(body)


def test_template_sample_follows_schema():
    d = sample()
    assert d["topic"] and d["about"] and d["options"] and d["moments"] and d["questions"]
    for o in d["options"]:
        assert o["title"]
        for p in o["for"] + o["against"]:
            assert p["end"] in {"holds", "challenged", "fails", "open"}
            assert p["say"] and p["outcome"] and p["steps"]
            assert all(s["t"] and s["did"] for s in p["steps"])
    assert all(m["kind"] in {"", "turn", "common"} for m in d["moments"])
    assert all(q["answer"] in {"settled", "leans yes", "leans no", "disputed", "open"} for q in d["questions"])


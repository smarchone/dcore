"""Tests for the dcore skill: transcript parsing and the report pages' data."""

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


EXAMPLE = Path(__file__).resolve().parents[1] / "docs/examples/civic-sense/citizen.html"


def citizen_report(path):
    html = path.read_text(encoding="utf-8")
    start = html.index('<script id="report" type="application/json">')
    body = html[html.index(">", start) + 1:html.index("</script>", start)]
    return json.loads(body)


@pytest.mark.parametrize("path", [SKILL / "template-compact.html", SKILL / "template.html", EXAMPLE],
                         ids=["template-compact", "template", "example"])
def test_citizen_report_follows_schema(path):
    d = citizen_report(path)
    ids = {t["id"] for t in d["threads"]}
    assert d["question"] and d["context"] and 3 <= len(ids) <= 6
    assert {p["status"] for p in d["progress"]} <= {"reached", "missed"}
    for p in d["progress"]:
        assert p["thread"] in ids and p["text"] and p["chain"]
        if p["status"] == "missed":
            assert p["lost"]["t"] and p["lost"]["label"]
    segs = d["segments"]
    assert all(t in {"fwd", "talk", "side", "idle"} for _, _, t, _, _ in segs)
    assert segs[0][0] == 0 and segs[-1][1] == d["total_seconds"]
    assert all(a[1] == b[0] for a, b in zip(segs, segs[1:])), "segments must be contiguous"
    assert all(th in ids for _, _, _, th, _ in segs if th)
    for t in d["threads"]:
        assert t["end"] in {"converged", "clarified", "bounded", "stuck", "dropped"}
        assert all(m.get("mark") in {"fwd", "talk", "gap", "side"} for m in t["flow"] if "t" in m)
        if t["end"] in {"stuck", "dropped"}:
            assert 3 <= len(t["replay"]["lines"]) <= 6
    for x in d["distractions"] + d.get("unanswered", []) + d.get("gaps", []):
        assert x["thread"] in ids
    assert all(x["label"] and x["who"] and x["better"] and x["cost"] for x in d["distractions"])
    assert d["insight"]["title"] and d["insight"]["text"]
    assert all(v["name"] and v["note"] for v in d["voices"])
    assert d["ask"]["distraction"] and d["ask"]["nowhere"] and d["footer"]
    assert d["youtube"] or d["transcript"], "timestamps need a source to link to"


def test_transcript_chunks(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("tc", SKILL / "scripts/transcript_chunks.py")
    tc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tc)
    f = tmp_path / "t.txt"
    f.write_text("[0:00] a\n[0:05] b\n[0:21] c\n[1:02:03] d\n", encoding="utf-8")
    assert tc.chunks(str(f)) == [[0, "a b"], [21, "c"], [3723, "d"]]

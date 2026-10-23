# dcore

**A review for public debates.** Give it a debate, panel or townhall, and
in about a minute you see what the conversation actually achieved, what it
missed, and why.

A chess engine doesn't tell you which side to play. It shows the better move
you missed and what it cost. dcore does the same for a conversation:

- **What was reached:** where the speakers agreed, or at least sharpened their
  disagreement.
- **What was missed:** progress that was one or two moves away, the moment it
  slipped, and what that leads to.
- **Where the time went:** how much went to progress, to talk nobody replied
  to, and to distractions like "changed the subject" or "host took a side".
- **Who did what:** each voice's good moves and misses, host included, with
  the better move each time. No scores, no verdicts on people.
- **A fair replay:** for each thread that got stuck, one way it could have gone
  with the same people and the same views.

It grades moves, never positions. Every line links to the exact second in the
video.

## Example

[Are Indian cities broken because Indians lack civic sense?](docs/examples/civic-sense/citizen.html)
A 49-minute studio debate ([video](https://www.youtube.com/watch?v=rBPLwZI5whY)).

- **Reached:** both sides agreed civic sense is learned, not inborn, and that
  citizens should demand accountability rather than do the government's job.
- **Missed:** one side blamed cheap bribes and the other cheap fines. It was
  the same point, and nobody noticed before the host moved on.
- **The result:** the audience poll barely moved, from 27% to 29%.

## Try it

In [Claude Code](https://claude.com/claude-code), from this repo:

```
/dcore https://www.youtube.com/watch?v=<id>
```

A pasted transcript works too.

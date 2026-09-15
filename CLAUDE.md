# Project: ink-and-wash motion comic series

Illustrated storytelling series for YouTube (16:9) and TikTok/Shorts (9:16). Static painted
panels, slow camera moves, small isolated animated elements — a motion comic, not full
character animation.

Read `HANDOVER.md` first for full context, measured costs and account state.
The style block and prompt scaffolding live in `docs/style-prompt.md`.

## Rules that decide most things here

**A shot that is only a camera move must use `scripts/kenburns.py`, never AI generation.**
It is free, and more faithful: AI re-renders every frame, so paper grain and ink hatching
boil (crawl and redraw). A real crop over a fixed painting cannot boil. Roughly 65% of
shots qualify.

Spend AI generation only where motion is the point — lantern flicker, moving water,
drifting fog, a character actually moving. Keep camera moves slow and simple; painterly
styles fall apart under fast motion.

Prefer image-to-video seeded from an approved still over text-to-video.

**Never bake text into generation.** Titles and captions are a separate motion-graphics
layer. Always include the no-text block from `docs/style-prompt.md`.

## Cost discipline

Generation is ~99% of the cost of an episode; everything else is a rounding error.
Always state a credit and dollar estimate **before** spending, and wait for approval.
Measured rates are in `HANDOVER.md` §5.

## Images and context

Never inline base64 image data into the conversation to feed a video API — it costs
~11–32k tokens per image. Write a script that reads the file from disk and POSTs it.

## Secrets

API keys come from environment variables. Never hardcode them, never echo them, never
write them into committed files.

## Layout

```
stills/   source panels from Google Flow
shots/    shot lists / episode breakdowns
scripts/  tooling (kenburns.py)
out/      rendered clips and assembled episodes  (git-ignored)
docs/     style-prompt.md
```

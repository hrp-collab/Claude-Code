# Style prompt blocks

Reusable prompt components for the series. Proven to reproduce the look from text alone —
no reference image required.

## A. Style block (use verbatim)

```
hand-drawn 2D storybook illustration, expressive ink-and-wash with gouache on cold-press
watercolor paper. Sketchy ink linework, intricate pen hatching, soft charcoal shading,
visible paper grain. High-contrast composition with deep ebony shadows, misty gradients,
and restrained accents of warm yellow and plum. Organic watercolor blooms, intentional ink
splatters. Characters ignore the camera, candid framing, uncropped, textless, no
letterboxing.
```

## B. No-text block (always append)

```
ABSOLUTELY NO TEXT of any kind — no title, no words, no letters, no numbers, no logos, no
watermark, no captions. No letterboxing or black bars. No borders or frames. Not a
photograph, not 3D, not digital airbrush — traditional hand-painted media only.
```

## C. Texture-lock block (append for any AI video generation)

The single most important block for video. Without it the paper grain boils.

```
CRITICAL: the ink linework, hatching, paper grain and watercolor texture must stay STABLE
and locked to the image, as though a real painting is being gently moved past the camera.
The texture must NOT shimmer, crawl, boil, morph or re-draw itself frame to frame. Do not
smooth it into glossy digital painting, CGI, 3D render or photorealism. Traditional
hand-painted media only.
```

## D. Motion restraint block (append for any AI video generation)

```
CAMERA: one single continuous very slow dolly push-in. No cuts. No shake. No whip pans. No
zoom snaps.

MOTION (keep minimal and restrained): [name only the one or two things that actually move].
The character stays almost perfectly still — only the faintest shift of weight and a slow
breath. He never turns toward camera. He never looks at the camera.
```

## E. Full-bleed modifier (optional)

Generated stills come back with a white deckled paper border. Charming on a print panel, a
white margin in video. To avoid it:

```
full bleed, image extends to all four edges, no paper border, no white margin
```

Or leave it and let the Ken Burns zoom crop it out.

## F. Ambient audio block (for models that generate audio)

```
AUDIO: [ambient sounds only]. No music. No voices. No narration.
```

---

## Worked example — the test still

Scene description used with blocks A + B:

```
Interior of an old lighthouse tower: a narrow cast-iron spiral staircase winding steeply
upward into darkness. A lone keeper in a heavy weathered coat stands at the bottom of the
stairs, back to us, holding a small oil lantern raised slightly, looking up the spiral.
Warm yellow lantern glow pools on the iron treads and catches the curve of the railing;
everything beyond falls into deep ebony shadow. Faint misty daylight bleeds from a small
window high above. Damp stone walls, flaking paint, rust streaks.
```

Result: `stills/s01_stairwell.png`. Strong match on the first attempt.

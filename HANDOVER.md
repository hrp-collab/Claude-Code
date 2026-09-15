# Handover — ink-and-wash motion comic series

Paste this file (or point a local Claude Code session at this repo) to pick up where the
previous chat left off. Everything below was established or measured in that session on
2026-09-15.

---

## 1. The project

An illustrated storytelling series for YouTube (16:9) and TikTok/Shorts (9:16), in a
hand-drawn ink-and-wash style. Working reference material is a four-panel comic page,
"THE RELIEF KEEPER" — a lighthouse story (relief keeper arrives, cut cable, a name in the
logbook: MARA VOSS).

Target output is a **motion comic**: static painted panels with slow camera moves and
small isolated animated elements, not full character animation.

## 2. The style prompt — the most important asset here

Use this verbatim. It reproduces the look reliably on its own, with **no reference image
required** (proven — see §3).

> hand-drawn 2D storybook illustration, expressive ink-and-wash with gouache on cold-press
> watercolor paper. Sketchy ink linework, intricate pen hatching, soft charcoal shading,
> visible paper grain. High-contrast composition with deep ebony shadows, misty gradients,
> and restrained accents of warm yellow and plum. Organic watercolor blooms, intentional
> ink splatters. Characters ignore the camera, candid framing, uncropped, textless, no
> letterboxing.

Always append an explicit **no-text block** — no words, letters, numbers, titles, logos,
watermark, captions, borders or letterboxing. Generated text warps badly. Titles and
captions go on as a separate motion-graphics layer.

## 3. What has actually been proven

- **Style reproduces from text alone.** A test still (`stills/s01_stairwell.png`) was
  generated from the paragraph above plus a scene description. No reference image needed.
  This removes a whole class of plumbing.
- **The free camera-move path works.** `scripts/kenburns.py` renders a slow push-in over a
  still with ffmpeg. Verified on the test still: start and end frames show the zoom, and
  the ink linework and paper grain are pixel-faithful because it is a real crop, not a
  re-render.
- **A 4s AI clip was generated** via vidIQ gemini-omni-flash (80 credits). Its quality was
  never confirmed — the environment's egress proxy blocked the host, so nobody viewed it.
  Treat it as unverified.

## 4. Animation rules (learned the hard way — do not relitigate)

1. **Never use text-to-video for a shot that is just a camera move.** Use
   `scripts/kenburns.py`. It is free, and it is *more* faithful: AI re-renders every frame,
   so paper grain and hatching "boil" — crawl and redraw. A real crop cannot boil.
2. **Spend AI generation only where motion is the point**: lantern flicker, moving water,
   drifting fog/dust, a character actually moving.
3. **Keep motion minimal and camera moves slow and simple.** Painterly styles fall apart
   under fast motion or full character animation.
4. **Prefer image-to-video over text-to-video** when generating, seeding from an approved
   still so the artwork is preserved.
5. Always add: *"ink linework, hatching, paper grain and watercolor texture must stay
   STABLE and locked to the image… must NOT shimmer, crawl, boil, morph or re-draw itself
   frame to frame."*
6. Generated stills come back with a **white deckled paper border**. Lovely for a print
   panel, a white margin in video. Add *"full bleed, image extends to all four edges"* if
   you want edge-to-edge, or let the Ken Burns zoom crop it out.

## 5. Cost data (measured 2026-09-15, not guessed)

**vidIQ MCP**, at the $10/2000-credit rate (= $0.005/credit):

| Model | credits/sec | $/sec |
|---|---|---|
| gemini-omni-flash | 20 | $0.10 |
| seedance-2-fast | ~29 | $0.147 |
| veo-3.1 | 80 | $0.40 |

Clip length caps: omni 3–10s, veo-3.1 4/6/8s, seedance 1–15s.

**Higgsfield** (Plus $59/mo, 1,200 credits, ≈$0.049/credit — from public pricing pages,
verify at higgsfield.ai/pricing):

| Model | $/sec |
|---|---|
| Kling 3.0 720p | ~$0.079 |
| Seedance 2.0 Fast | ~$0.167 |
| Seedance 2.0 720p | ~$0.216 |

**Near-free on vidIQ:** `vidiq_video_upload` 0, `vidiq_instagram_publish_reel` 0, script
1/min, voiceover 14/1k chars, music 25/track, thumbnail 22.

### The economics of a 3-minute episode

180s finished, assume a 1.5× retry factor ≈ 270s generated.

- All-AI on vidIQ omni: ~5,400 credits — **2.7 months** of the $10 plan. Not viable.
- All-AI on vidIQ veo-3.1: ~21,600 credits ≈ $108/episode.
- All-AI on Higgsfield Kling 3.0: ~432 credits ≈ **$21**, about a third of a Plus month.
- **Hybrid (~65% ffmpeg / 35% AI ≈ 95s generated): ~$7.50/episode on Higgsfield Kling —
  roughly 8 episodes a month on Plus.** This is the recommended shape.

The headline: vidIQ's *rate* is roughly market, but its monthly *cap* makes a 3-minute
episode impossible inside one month. Higgsfield removes the cap and is cheaper on Kling.

## 6. Account state

- vidIQ authenticated as **housnypomare2@gmail.com**, **48 credits** remaining, cap
  150/month on the free tier, renews **2026-10-15**.
- **No YouTube channel authorized. No Instagram account connected.** Both lists returned
  empty. Publishing will fail until these are connected at app.vidiq.com.
- Character/location/prop stills are being built in **Google Flow** and already exist —
  they were never transferred into the previous session.

## 7. Recommended stack

| Stage | Tool | Notes |
|---|---|---|
| Stills | Google Flow (already in use) | the expensive half, already solved |
| Static-camera shots | `scripts/kenburns.py` | free, texture-safe, ~65% of shots |
| Animated hero shots | Higgsfield API (Kling 3.0) | has camera-motion presets + webhooks |
| Assembly | ffmpeg | local |
| Titles / captions | motion-graphics layer | never bake text into generation |
| Voiceover / music | vidIQ, or ElevenLabs direct | cheap |
| Titles, thumbnails, SEO | vidIQ | cheap, genuinely good |
| YouTube + Reels publishing | vidIQ | **0 credits** |
| TikTok | Zapier | no native tool |

**Why Higgsfield over raw APIs:** its identity is cinematic camera-motion presets — dolly
in, orbit, crash zoom — which is exactly the vocabulary this style needs. You specify the
move as a parameter instead of begging a text prompt for it. It also has a real API
(cloud.higgsfield.ai, 100+ models, image-to-video, webhooks), so it can be scripted.

**Two caveats:** Higgsfield's "unlimited" is 365-day on *image* models (Plus and above) and
only 7–33 day windows on select video models — it is aimed at a problem already solved by
Flow. And the unlimited language specifies *web-app* generations, so **verify whether API
calls draw from subscription credits** before committing. Credits do not roll over.

## 8. A hard constraint worth knowing

Video APIs take a start frame as **inline base64**. Passing images through a chat context
costs ~11–32k tokens each, which makes batch image-to-video impractical *in conversation*.

**The fix:** a local script reads the file off disk and POSTs it. The image data never
enters the context. This is the single strongest argument for a local setup over doing this
in chat, and it is why this repo exists.

## 9. Open decisions

1. Higgsfield vs. direct API (fal.ai / Replicate / Google Gemini) — leaning Higgsfield for
   the camera controls.
2. Whether Higgsfield API usage bills separately from the subscription. **Unverified.**
3. Where the Flow stills live and how they reach this repo (`stills/`).
4. Episode length and cadence.

## 10. Repo layout

```
stills/     source panels from Flow (s01_stairwell.png is the test still)
shots/      shot list / per-episode breakdown
scripts/    kenburns.py — free camera moves over stills
out/        rendered clips and assembled episodes
docs/       style-prompt.md — the style block + prompt scaffolding
```

## 11. Good first task for the new session

Have the stills dropped into `stills/`, then produce a shot breakdown that marks each shot
**FFMPEG** (free camera move) or **AI** (needs real motion), with a credit/dollar estimate
for the AI shots *before* anything is charged. Then batch-render the ffmpeg shots.

---

**One caution:** don't paste API keys into chat. Put them in environment variables and have
scripts read them from there.

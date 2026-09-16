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
- **AI animation of the style works, and the cheap model is good enough.** A 4s clip was
  generated via vidIQ `gemini-omni-flash` (80 credits, $0.10/sec) and **confirmed by the
  user to look great**. This is the single most useful result here: the budget tier holds
  the ink-and-wash style. Do not assume veo-3.1 (4× the price) is required — start at omni
  and only escalate on shots that visibly fail.

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

**Google Flow / Veo — cheapest route, see §7a.** Veo 3.1 Lite ~$0.03/sec on the API; Flow
AI Pro $19.99/mo (1,000 credits ≈ 100 Lite videos) ≈ $0.025/sec effective. Free tier: 50
daily credits on Veo 3.1. Flow credits and Gemini API billing are separate wallets.

Clip length caps: omni 3–10s, veo-3.1 4/6/8s, seedance 1–15s.

**Higgsfield** — ⚠️ **unverified and likely stale.** Third-party sources conflict and
pricing has been restructured repeatedly; the first-party site was unreachable from the
research environment. Figures below assume Plus $59/mo, 1,200 credits (≈$0.049/credit).
Confirm at higgsfield.ai/pricing before relying on any of it. Note these are *subscription*
rates — API/MCP bills a separate wallet (§7).

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
- **Hybrid (~65% ffmpeg / 35% AI ≈ 95s generated) on vidIQ omni: ~1,890 credits — fits
  inside a single $10/2000 month**, with ~110 credits spare for a thumbnail and voiceover.
  Quality at omni is user-confirmed. **This is the recommended shape and the cheapest
  verified path: roughly one 3-minute episode per month for $10.**

The headline: the hybrid split is what makes this affordable. All-AI is 3× the budget at
the same runtime; ffmpeg does the majority of shots for free *and* renders them more
faithfully.

For more throughput than one episode a month, either buy additional vidIQ credits or move
generation to a metered API (see §7 on Higgsfield billing).

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
| Characters / props / locations | Google Flow **Ingredients** | the consistency system — see §7a |
| Stills / storyboard | Google Flow | the expensive half, already solved |
| Static-camera shots | `scripts/kenburns.py` | free, texture-safe, ~65% of shots |
| Animated hero shots | Flow **Ingredients to Video** (Veo 3.1) | ~$0.03/sec — cheapest, keeps consistency |
| Fallback if Lite fails on style | vidIQ `gemini-omni-flash` | verified good, $0.10/sec |
| Only if camera presets needed | Higgsfield metered API | costs consistency + a second bill |
| Assembly | ffmpeg | local |
| Titles / captions | motion-graphics layer | never bake text into generation |
| Voiceover / music | vidIQ, or ElevenLabs direct | cheap |
| Titles, thumbnails, SEO | vidIQ | cheap, genuinely good |
| YouTube + Reels publishing | vidIQ | **0 credits** |
| TikTok | Zapier | no native tool |

### 7a. Stay inside Flow for animation — it is not just a stills tool

Veo 3.1 **Ingredients to Video** takes up to three reference images (character, object,
style reference) and generates video from them, with identity consistency across scenes,
**native 9:16** for TikTok/Shorts, and 1080p/4K upscaling. The Ingredients built for the
storyboard feed straight into video generation in the same tool.

**This is why exporting stills to another platform is usually a mistake.** The moment a
flat PNG is handed to Higgsfield (or anything else), the Ingredients system no longer
applies — and keeping the same keeper, lighthouse and lantern consistent across a whole
series is the hardest problem here and the thing Flow is uniquely good at. Leaving also
means a second video bill, manual round-trip friction per shot, and a fresh style-drift
risk at the handoff.

**Flow is also the cheapest option by a wide margin:** Veo 3.1 Lite is ~$0.03/sec on the
API, and AI Pro at $19.99/mo (1,000 credits ≈ 100 Lite videos) works out to ~$0.025/sec
effective. That is 3–4× cheaper than vidIQ omni. A free tier exists at 50 daily credits
running Veo 3.1 — benchmark there before paying.

Caveats: **Veo 3.1 Lite is the budget tier** and may not hold ink-and-wash the way full Veo
does — test it against the style the same way omni was tested, do not assume. **Flow credits
and Gemini API billing are not interchangeable** (a Flow subscription does not convert into
API seconds, and API spend does not top up Flow credits — the same wallet-separation trap as
Higgsfield). The free tier's daily cap prevents bursting a full episode in one sitting.

**None of this changes the ffmpeg rule.** ~65% of shots are camera-only and should never
touch Flow *or* Higgsfield.

**Why Higgsfield over raw APIs:** its identity is cinematic camera-motion presets — dolly
in, orbit, crash zoom — which is exactly the vocabulary this style needs. You specify the
move as a parameter instead of begging a text prompt for it. It also has a real API
(cloud.higgsfield.ai, 100+ models, image-to-video, webhooks), so it can be scripted.

**Higgsfield billing — resolved, and it matters.** Credit wallets are separated by access
path:

- **Website / Creator Hub UI** → subscription credits (Starter / Plus / Ultra allocation).
- **API and MCP** → authenticate by API key or client config, mapping to a **separate
  metered wallet or boost pool**. These do not automatically drain the subscription
  balance.
- **Trials and promos** → some specialised workflows and MCP promotional pools run on
  standalone buckets. Worth hunting for: a promo pool would let you benchmark Higgsfield
  against omni at no cost.

Consequences:

- The subscription's credits (Plus = 1,200) are for **web-app** generations. A subscription
  does **not** subsidise an API-driven pipeline.
- Any per-episode figure derived from subscription credits is wrong for automation. An
  earlier estimate of "~8 episodes a month on Plus" assumed the API drew on those 1,200
  credits — **it does not.** Disregard it.
- Only buy a subscription if you also intend to work by hand in the web app. For a scripted
  pipeline, price the metered API wallet on its own merits.
- Higgsfield's "unlimited" is 365-day on *image* models (Plus and above) and only 7–33 day
  windows on select video models — aimed at a problem Flow already solves. Credits do not
  roll over.

**Treat all Higgsfield pricing in this document as unreliable.** Third-party sources
contradict each other (Starter $15 vs $19, Plus ~$49 vs $59) and the company has
restructured pricing repeatedly since launch. higgsfield.ai is blocked by this
environment's egress proxy, so nothing here was confirmed first-party. **Verify on
higgsfield.ai/pricing before spending.**

**Best available estimate of the metered rate:** top-up packs run ~$5 per 100 credits
(≈$0.05/credit, expiring ~90 days) — near the Plus effective rate, so the metered wallet is
probably priced similarly. At 6–10 credits per 5s Kling 3.0 clip that implies roughly
**$0.06–0.10/sec**. This is an inference from top-up pricing, not a published API rate.

**So the strategic picture has shifted.** Higgsfield is likely at rough *parity* with vidIQ
omni ($0.10/sec, verified), not meaningfully cheaper. Its case now rests on two things
only:

1. **Camera-motion presets** — specify "dolly in" as a parameter instead of coaxing a text
   prompt. A genuine fit for this style.
2. **No monthly cap** — the metered wallet scales past one episode a month.

It is not the cheaper option. Choose it for control and throughput, or stay on vidIQ omni.

Higgsfield also exposes an **MCP server**, so it can connect to Claude directly rather than
through a custom script — that would remove most of the integration work. Note that routing
MCP usage onto subscription credits instead of the separate wallet is a known open question
in the community; assume you cannot until proven otherwise.

## 8. A hard constraint worth knowing

Video APIs take a start frame as **inline base64**. Passing images through a chat context
costs ~11–32k tokens each, which makes batch image-to-video impractical *in conversation*.

**The fix:** a local script reads the file off disk and POSTs it. The image data never
enters the context. This is the single strongest argument for a local setup over doing this
in chat, and it is why this repo exists.

## 9. Open decisions

1. **What does the Higgsfield metered API wallet actually cost per generation?** Estimated
   at ~$0.06–0.10/sec from top-up pricing, which is roughly parity with verified vidIQ omni
   — so Higgsfield probably wins on camera control and throughput rather than price. Get
   the real number first-party; everything published third-party conflicts.
   Check for an **MCP trial/promo pool** — a free benchmark against omni would settle this
   without spending anything.
2. Whether to use the **Higgsfield MCP** (direct Claude connection, little integration work)
   or a custom script against the REST API (more control, batching, webhooks).
3. Where the Flow stills live and how they reach this repo (`stills/`).
4. Episode length and cadence. At the verified hybrid rate, $10/month ≈ one 3-minute
   episode; a weekly cadence needs roughly 4× that budget.

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

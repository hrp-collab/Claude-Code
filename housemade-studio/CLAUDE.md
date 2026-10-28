# Housemade Studio

House Pomare's design studio (Lake Monticello / Charlottesville, VA). Separate from the
motion comic project at the repo root; the root CLAUDE.md rules on video generation
don't apply here.

## Brand

- Name: Housemade Studio. Logo: gold roofline over a purple H (`brand/logo/`).
  Regenerate with `brand/make_logo.py`; never redraw the mark by hand.
- Colors: ivory `#fbf9f3` ground, Ravens purple `#241773` type and buttons,
  antique gold `#c79a2c` for corner marks and lines (gold text on ivory is
  `#7d611c`), black `#000000`, plum `#351047` supporting, stone `#f1ece3` panels.
- Type: Barlow Condensed for headings, Barlow for text.
- Family: Pomare Portraits leads with black (Jost and Lato); House Frames leads with
  purple (Bebas Neue and Montserrat); the studio leads with ivory. Keep the fonts apart.
- Signature shape: gold corner marks. Square corners.

## Design Hub

See `design-hub/README.md`. Edit `hub.dc.html`, run `python3 design-hub/build.py`,
publish `design-hub/dist/housemade-hub.html` to the same artifact URL.
Published hub: https://claude.ai/artifact/58JiLBgbLriq1QhdyoRLyt (private; db, sample,
downloads and mcp capabilities as listed in the README; restate all of them on every
publish). Plans made in chat go to its `plans` collection with `fromChat: true` via
ArtifactData. Client status lives on each intake in `intakes/<id>` (`a.track`, `sum`).

## Voice

Plain, first person, short sentences. No emoji in client-facing copy.

# Housemade Design Hub

The client-call tool for Housemade Studio: intake → brief → proposal, plus a call
guide, playbooks, formats & looks, "For me" plans and Settings. It started as the
Claude Design project "Design Hub v7" (standalone Claude Design closes December 14, 2026).

## Files

- `hub.dc.html`: the source. A template (`<x-dc>`) plus one logic class.
- `support.js`: the Claude Design runtime that renders it with React 18.3.1 from unpkg.
  Generated upstream; don't edit it. `build.py` patches the copy it inlines.
- `styles/housemade.css`: Housemade tokens and components (ivory, Ravens purple,
  antique gold corner marks, Barlow Condensed and Barlow), light and dark.
- `for-me-plans.json`: the plans that were made in chat before the hub went online.
  Online they live in the hub's own storage; this file is only read by a local copy.
- `build.py`: builds `dist/housemade-hub.html`, the single page that gets published.

## Run it locally

```sh
cd housemade-studio/design-hub
python3 -m http.server 8000
# open http://localhost:8000/hub.dc.html
```

A local copy saves to the browser. "Ask Claude" in For me and saving to the account
only work in the published version.

## Publish

```sh
python3 build.py
```

Then publish `dist/housemade-hub.html` as an artifact with these capabilities:

```json
{"db": {"rules": [{"path": "", "read": "admin", "write": "admin"}]}, "sample": {}, "downloads": true}
```

`db` stores everything so phone and computer match; the rule keeps client data to
the owner and editors. `sample` powers "Ask Claude" in For me. `downloads` saves
briefs and proposals as HTML files.

## Where things are saved (db)

| Path | What |
| --- | --- |
| `hub/settings` | Studio details, terms, price rules and price list overrides |
| `intakes/<id>` | One intake: `{ id, a, mode, pos, at }` |
| `plans/<id>` | One For me plan: `{ id, at, text, ans, rec, fromChat? }` |

Plans made in chat are written to `plans/` with `fromChat: true`; the hub shows them
under For me without any copy and paste.

## Prices

Defaults live in `PRICES` in the logic class (Simple, Standard, Complex per item) and
the rules in `DEF`. Settings overrides both. Market ranges come from 2026 US freelance
pricing guides; map, 3D, handoff and "connect their code" are estimates.

# Housemade Design Hub

The client-call tool for Housemade Studio: intake → brief → proposal, a Clients
board that tracks every client from lead to paid, plus a call guide, playbooks,
formats & looks, "For me" plans and Settings. Briefs and proposals download as PDFs
and send from Gmail; project dates go to Google Calendar. It started as the
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

A local copy saves to the browser. "Ask Claude" in For me, saving to the account,
Gmail and Google Calendar only work in the published version. PDF downloads work
locally when the page can reach cdn.jsdelivr.net (html2pdf.js is loaded on first use).

## Publish

```sh
python3 build.py
```

Then publish `dist/housemade-hub.html` as an artifact with these capabilities:

```json
{"db": {"rules": [{"path": "", "read": "admin", "write": "admin"}]}, "sample": {}, "downloads": true,
 "mcp": {"servers": [{"server": "Gmail", "tools": ["send_message", "create_draft"]},
                     {"server": "Google Calendar", "tools": ["create_event"]}]}}
```

`db` stores everything so phone and computer match; the rule keeps client data to
the owner and editors. `sample` powers "Ask Claude" in For me. `downloads` saves
briefs and proposals as PDFs. `mcp` sends email and adds calendar events through
the viewer's own claude.ai connectors; each asks once before its first use. Every
publish must restate the whole set: anything left out is switched off.

## Where things are saved (db)

| Path | What |
| --- | --- |
| `hub/settings` | Studio details, terms, price rules and price list overrides |
| `intakes/<id>` | One intake: `{ id, a, mode, pos, at, created, sum }` |
| `plans/<id>` | One For me plan: `{ id, at, text, ans, rec, fromChat? }` |

Plans made in chat are written to `plans/` with `fromChat: true`; the hub shows them
under For me without any copy and paste.

An intake's client tracking lives in `a.track`:
`{ stage, dates: { brief, proposal, booked, active, delivered, paid, lost }, kickoff,
rounds, note, quote: { total, dep }, mailed, cal }`. Stages run lead → brief →
proposal → booked → active → delivered → paid, or lost. Dates are `YYYY-MM-DD`.
`sum` repeats the useful parts in plain fields (name, business, email, stage, total,
deposit, turnaround, rounds, kickoff, note, and `due` dates for the proposal expiry,
final files and the end of free fixes). The Monday summary reads `sum`; it's
refreshed every time the intake saves.

## Monday summary

A scheduled task, "Housemade Monday summary", runs every Monday at 7:35 AM Eastern.
It reads `intakes/` and `hub/settings` from the hub's storage and sends House what
needs attention this week: always as a push notification, and by email once Gmail
is added to the task in claude.ai (scheduled tasks can't be given connectors from a
Claude Code session in this organization). It never writes to the hub.

## Prices

Defaults live in `PRICES` in the logic class (Simple, Standard, Complex per item) and
the rules in `DEF`. Settings overrides both. Market ranges come from 2026 US freelance
pricing guides; map, 3D, handoff and "connect their code" are estimates.

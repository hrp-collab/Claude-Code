# Design Hub v7

Export of the Claude Design project "Design Hub v7" (`Design Hub v7.dc.html`), saved here because standalone Claude Design closes December 14, 2026.

A client-call tool: intake → brief → proposal, with a call guide, playbooks, formats & looks, and the "For me" plans list.

## Files

- `Design Hub v7.dc.html` — the page
- `support.js` — Claude Design runtime (loads React 18.3.1 and Babel from unpkg)
- `_ds/industry-…/` — design-system styles
- `for-me-plans.json` — plans shown under **For me**

## Open it

The page fetches `for-me-plans.json`, so serve the folder rather than opening the file directly:

```sh
cd design-hub-v7
python3 -m http.server 8000
# then open http://localhost:8000/Design%20Hub%20v7.dc.html
```

Needs internet access for React (unpkg) and Google Fonts. Saved intakes and past work live in the browser's local storage, not in these files.

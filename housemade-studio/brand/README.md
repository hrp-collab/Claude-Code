# Housemade Studio logo

A gold roofline over a purple H: the house, and House's initial.

| File | Use |
| --- | --- |
| `logo/housemade-horizontal-color.svg` / `.png` | Default, on ivory or white |
| `logo/housemade-horizontal-reverse.svg` / `.png` | On purple, black or photos with a solid band |
| `logo/housemade-stacked-*.svg` / `.png` | Square-ish spaces: social posts, signage |
| `logo/housemade-mark-*.svg` | The mark alone, when the name is already nearby |
| `logo/housemade-icon.svg`, `logo/png/housemade-icon-*.png` | Avatar, favicon, app icon (purple square, safe for circle crops) |
| `*-black` / `*-white` | One-color printing |

SVGs have the letters outlined, so they look the same everywhere without the fonts.
PNGs are transparent (the icon has its purple square).

Keep clear space of at least the height of the H on every side. Don't recolor,
stretch, outline or add shadows.

## Rebuild

```sh
npm pack @fontsource/barlow-condensed@5.1.0 @fontsource/barlow@5.1.0
# extract files/barlow-condensed-latin-700-normal.woff2 and files/barlow-latin-600-normal.woff2 into FONTS
pip install fonttools brotli
python make_logo.py FONTS logo
```

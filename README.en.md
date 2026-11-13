# Kasane

[日本語](README.md) | English

A design system for websites and web apps. It separates content by layering surfaces, and the accent color can be chosen from 9 palettes.

- No borders or shadows: content is separated by differences in surface color (only input controls have a border).
- 9 accents: Yamabuki, Tachibana, Kobai, Fuji, Ai, Sora, Seiji, Moegi and Sumi. Every palette is checked for text contrast of 4.5:1 or more, in both light and dark.
- Fonts: LINE Seed JP. Titles use Zen Maru Gothic 900, and numbers in columns use Inter’s tabular figures.
- Thorough automatic checks (CSS and HTML rules, image quality, Lighthouse minimum scores) keep the quality up even when AI writes all the code.

## Usage

```html
<html lang="en" data-accent="ai">
<head>
  <link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://kasane.y-n0.de/v1/fonts/line-seed-jp.css">
  <link rel="stylesheet" href="https://kasane.y-n0.de/v1/kasane.min.css">
</head>
<body>
  <button class="k-btn k-btn-primary" type="button">Save</button>
</body>
</html>
```

- `data-accent`: the palette name (defaults to `yamabuki`)
- `data-theme`: `light` or `dark` (defaults to the device setting; in products, leave it out and add no toggle)

See the [documentation site](https://kasane.y-n0.de/en/) and the [spec](https://kasane.y-n0.de/v1/kasane.en.md) ([Japanese](https://kasane.y-n0.de/v1/kasane.md)) for details. How to build Kasane into a product (the default color, where users change it) is on the documentation site’s “[Integration and examples](https://kasane.y-n0.de/en/integrate/)” page.

## Using it with AI

Add this to your project’s `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex):

```markdown
## UI

Before building or changing UI, read this spec to the end and follow its rules.
https://kasane.y-n0.de/v1/kasane.en.md

Load this CSS:
https://kasane.y-n0.de/v1/kasane.min.css

At the end of the work, go through every item in the spec’s end-of-work checklist.
```

## Automatic checks (kasane-lint)

Stylelint checks the CSS and `kasane-check` checks the HTML against the rules.

```bash
npm install --save-dev stylelint https://kasane.y-n0.de/v1/kasane-lint-1.2.0.tgz
```

```json
{ "extends": ["kasane-lint/stylelint"] }
```

```bash
npx stylelint "src/**/*.css"
npx kasane-check "src/**/*.html"
```

- CSS: raw colors, shadows, borders on anything but input controls, radius / spacing / text size / motion duration not from tokens, `outline: none`, fonts not from tokens
- HTML: the number of primary buttons, state icons, colors in `style` attributes, labels, switch structure, `k-` classes Kasane does not have, Lucide icon names that do not exist, dialog and tab attributes

The same package also checks images and speed.

```bash
npm install --save-dev sharp ssim.js lighthouse
npx kasane-image photo.jpg --out public/img        # AVIF / WebP; picks the lowest quality with SSIM ≥ 0.99
npx kasane-lighthouse http://localhost:3000/       # Lighthouse CLI, mobile and desktop
```

Lighthouse minimums: Performance 90, Accessibility 100, Best Practices 95, SEO 90.

When you change a rule, bump `version` in `lint/package.json`. The version is part of the file name, so what people installed never changes on its own.

## Icons

Icons are [Lucide](https://lucide.dev/icons/) (ISC License) only, with a stroke width of 2.5.

## Files

| Path | Contents |
|---|---|
| `v1/kasane.css` / `kasane.min.css` | All tokens and components |
| `v1/kasane.md` | The spec, in Japanese (for AI and people) |
| `v1/kasane.en.md` | The spec in English (same content; fewer tokens for AI) |
| `v1/tokens.json` | Token values (W3C Design Tokens format) |
| `v1/fonts/` | LINE Seed JP, split by character range |
| `site/` | The documentation site (one HTML file per page, English under `en/`, sitemap.xml, robots.txt, icons, share image) |
| `llms.txt` | Tells AI tools where the spec is |
| `lint/` | `kasane-lint` (Stylelint rules, `kasane-check`, `kasane-image`, `kasane-lighthouse`), served as `v1/kasane-lint-<version>.tgz` by `npm run dist` |
| `tools/` | The sources that generate the files above. The English site is built from the translations in `tools/i18n/en.json` |

## Development

```bash
npm install
npm run build   # generate v1/ and site/ from tools/
npm run icons   # remake the icons and share image (only when the logo or default palette changes)
npm test        # Stylelint and kasane-check rules, kasane-image, contrast of every palette, ja/en specs in sync
npm run dist && npm run lighthouse   # does the documentation site meet the Lighthouse minimums?
```

The documentation is written in Japanese. When you change or add Japanese text, add its translation to `tools/i18n/en.json`; the build stops and lists anything missing in `tools/.out/i18n-missing-en.json`.

It is served by Cloudflare Workers static assets (configured in `wrangler.jsonc`; the `dist/` built by `npm run dist` is served as is) and updates when you push to `main`. To serve it elsewhere, rebuild with `KASANE_BASE_URL=https://… npm run build`.

## License

- Kasane itself (CSS, specs, documentation, Stylelint plugin, build scripts): MIT License (`LICENSE`)
- LINE Seed JP: SIL Open Font License 1.1 (`v1/fonts/LICENSE-LINE-Seed-JP.txt`)
- Zen Maru Gothic and Inter load from Google Fonts (both SIL Open Font License 1.1).

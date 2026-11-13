# Kasane v1 — Rules and spec for building UI

Kasane is a design system for websites and web apps.
It separates information by layering surfaces, and the accent colour can be chosen from 9 palettes.

This file is the spec for AI tools and people who build UI with Kasane. It is the English edition of `https://kasane.y-n0.de/v1/kasane.md` (Japanese). Both say the same thing; this one uses fewer tokens.
**Read this whole file before you build or change any UI.**
For anything not covered here, follow "8. Building a component Kasane does not have".

Docs: https://kasane.y-n0.de/ · Source: https://github.com/yamamotoxqx/design-system-kasane (MIT License)

---

## 0. Priority

When in doubt, the higher item wins.

1. Instructions from the user (the person who asked you)
2. "2. Rules you must follow"
3. The rest of this spec
4. Your own judgement

If the user's instructions conflict with a Kasane rule, follow the instructions and say in one line which rule you departed from.

---

## 1. Loading

```html
<!doctype html>
<html lang="ja" data-accent="yamabuki">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Apply the colour the user chose before first paint (no flash) -->
  <script>
    try {
      var a = localStorage.getItem("kasane-accent");
      if (a) document.documentElement.dataset.accent = a;
    } catch (e) {}
  </script>
  <link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://kasane.y-n0.de/v1/fonts/line-seed-jp.css">
  <link rel="stylesheet" href="https://kasane.y-n0.de/v1/kasane.min.css">
</head>
```

| File | Contents |
|---|---|
| `https://kasane.y-n0.de/v1/kasane.css` | All tokens and components (readable) |
| `https://kasane.y-n0.de/v1/kasane.min.css` | Same, minified. Use this in production |
| `https://kasane.y-n0.de/v1/fonts/line-seed-jp.css` | LINE Seed JP (400 / 700 / 800) |
| `https://kasane.y-n0.de/v1/tokens.json` | Token values (W3C Design Tokens format) |

### Colour and theme

| Attribute | Values | When omitted |
|---|---|---|
| `<html data-accent="…">` | `yamabuki` `tachibana` `kobai` `fuji` `ai` `sora` `seiji` `moegi` `sumi` | `yamabuki` |
| `<html data-theme="…">` | `light` `dark` | Follows the device (`prefers-color-scheme`) |

- Put the default colour the designer chose in `data-accent`. How to let users change it is in "14. Embedding in a product".
- Light and dark follow the device. **Do not add a light/dark toggle to products.** `data-theme` is for things like taking screenshots to check your work.

---

## 2. Rules you must follow

Each rule has a reason. Rewording code to get around the reason is also forbidden.

1. **Always use tokens (`var(--…)`) for colour.** Never write `#fff`, `rgb()`, `hsl()`, `oklch()` or colour names (`white` etc.).
   Reason: raw colours do not change with the palette or theme, and become unreadable.
2. **No borders or shadows on cards, lists, panels or buttons.** That includes framing with `border`, `box-shadow`, `outline`, and divider lines (`hr`, `border-top`). Separate things with the difference between surface colours.
   Reason: this is the foundation of Kasane's look. Lines and shadows make it look like another design system.
3. **Only input controls have a border.** Text inputs, selects, checkboxes, radio buttons. 2px, colour `--line`.
   Reason: so people can see at a glance where they can type.
4. **Use fill tokens and text tokens for their own jobs.** Accent fill is `--accent`, text on it is `--on-accent`, accent-coloured text and links are `--accent-ink`. Never use `--accent` as a text colour.
   Reason: a yellow or light-blue `--accent` is unreadable as text.
5. **Never show state with colour alone.** Success, error and info always have an icon and words.
   Reason: colour looks different to different people and screens.
6. **Fonts by role.** LINE Seed JP by default. Only page titles and section headings use `.k-title` (Zen Maru Gothic 900). Numbers in columns use `.k-num` (Inter tabular figures).
7. **Radius, spacing, text size and motion duration come from the tokens.** Do not invent new values.
8. **Never remove the focus ring.** Do not write `outline: none`. Tap targets are at least 44px tall (36px for small buttons).
9. **At most one primary button (`.k-btn-primary`) per screen.**
10. **Build new components by combining existing tokens and components.**
11. **Icons are Lucide only. Fetch the SVG and paste it.**
    Reason: shapes drawn from memory break easily, and mixing icon sets gives uneven stroke styles.

---

## 3. Colour

### Tokens

Values change with palette and theme. Always use them by token name.

| Token | Use | Example |
|---|---|---|
| `--bg` | Page background | `body` |
| `--surface` | Cards, panels, dialogs, inside inputs | `.k-card` |
| `--surface-2` | Surfaces inside cards, list rows, default buttons, tab track | `.k-list-item` |
| `--surface-3` | Hover and pressed on `--surface-2` | `:hover` |
| `--ink` | Text | Body, headings |
| `--muted` | Secondary text | Descriptions, dates, label hints |
| `--line` | Input borders, switch off | `.k-input` |
| `--accent` | Accent fill | Primary button, check, switch on, progress bar |
| `--on-accent` | Text and marks on `--accent` | Primary button text |
| `--accent-soft` | Light accent surface | Selected nav item, highlighted badge |
| `--accent-ink` | Accent-coloured text | Links, text on `--accent-soft` |
| `--focus` | Focus ring | `:focus-visible` |
| `--notice-head` | Notice heading | Text colour in light, accent in dark |
| `--ok` / `--ok-soft` | Success text / surface | Done, Saved |
| `--danger` / `--danger-soft` | Error and delete text / surface | Delete button, input errors |
| `--info` / `--info-soft` | Info text / surface | Supplementary notices |

Pairings are fixed. Do not use any pairing not in this table.

| Surface | Text allowed on it |
|---|---|
| `--bg` `--surface` `--surface-2` | `--ink` `--muted` `--accent-ink` |
| `--surface-3` | `--ink` |
| `--accent` | `--on-accent` |
| `--accent-soft` | `--accent-ink` |
| `--ok-soft` / `--danger-soft` / `--info-soft` | `--ok` / `--danger` / `--info` |

### Palettes

| Name (Japanese) | `data-accent` | Feel |
|---|---|---|
| 山吹 Yamabuki | `yamabuki` | Default. Bright yellow |
| 橘 Tachibana | `tachibana` | Orange |
| 紅梅 Kobai | `kobai` | Rose |
| 藤 Fuji | `fuji` | Purple |
| 藍 Ai | `ai` | Blue |
| 空 Sora | `sora` | Sky blue |
| 青磁 Seiji | `seiji` | Celadon (blue-green) |
| 萌黄 Moegi | `moegi` | Yellow-green |
| 墨 Sumi | `sumi` | No hue (black and grey) |

Every palette, in light and dark, meets 4.5:1 for text and 3:1 for input borders and the focus ring.

**Note:** with bright palettes (yamabuki, seiji, moegi…) in light mode, the `--accent` fill is close to the surface colour. Do not show "selected" or "on" by fill colour alone; combine it with a check mark, knob position, font weight, an `--accent-soft` surface, etc.

---

## 4. Surface layering

```
--bg (page)
└ --surface (card, radius --r-lg)
   └ --surface-2 (inner surface, list rows, radius --r-md)
      └ --surface-3 (hover, pressed)
```

- Each level inward uses the next surface. Never stack the same surface directly on itself.
- Dialogs are `--surface`, over a translucent black backdrop (`.k-scrim`).
- Never put `--surface-2` directly on the page background; put `--surface` between them.

---

## 5. Type and text

| Role | Font | How |
|---|---|---|
| Default (body, headings, buttons) | LINE Seed JP 400 / 700 / 800 | `--font-body` (already set on `body`) |
| Page titles, section headings | Zen Maru Gothic 900 | `.k-title` / `--font-title` |
| Numbers in columns (prices, counts, dates, stats) | Inter + `tabular-nums` | `.k-num` / `--font-num` |

| Token | Size | Where | Weight |
|---|---|---|---|
| `--text-2xl` | 32px | Page title | `.k-title` |
| `--text-xl` | 24px | Section heading | `.k-title` |
| `--text-lg` | 18px | Card heading | 800 |
| `--text-base` | 16px | Body | 400 |
| `--text-sm` | 14px | Labels, hints | 400 / 700 |
| `--text-xs` | 12px | Notes, dates | 400 |

- Body line height 1.8, titles 1.3. Long text: `max-width: 38em`.
- Never use `.k-title` for headings inside cards or for body text.

---

## 6. Radius, spacing, size, motion

| Radius | Value | Where |
|---|---|---|
| `--r-lg` | 28px | Cards, panels, dialogs, notices |
| `--r-md` | 18px | Inner surfaces, list rows |
| `--r-sm` | 14px | Inputs |
| `--r-full` | 999px | Buttons, badges, tabs, switches, progress bars |

Circles (icon backgrounds etc.) may use `50%`.

| Spacing | Value | Where |
|---|---|---|
| `--space-1` | 4px | Between icon and text |
| `--space-2` | 8px | Between buttons |
| `--space-3` | 12px | Inside list rows, between elements in a card |
| `--space-4` | 16px | Inside inner surfaces, between cards |
| `--space-5` | 24px | Inside cards |
| `--space-6` | 32px | Between large groups |
| `--space-7` | 56px | Between sections |

- Spacing between components comes from the parent's `gap`. Components have no outer `margin`.
- Tap target heights: button 44px, small 36px, large 54px, input 46px.
- At least 16px side margins. Reflow to one column on phones around 400px wide.

| Motion | Value | Where |
|---|---|---|
| `--motion-fast` | 150ms | Button colour and press, switches |
| `--motion-base` | 220ms | Opening dialogs and menus |
| `--motion-slow` | 450ms | Page transitions, components appearing (`.k-enter`) |
| `--ease-out` | `cubic-bezier(.2, .7, .3, 1)` | All motion |

- Animate only opacity and position. No blinking or looping. Closing disappears without animation.
- Stop motion under `@media (prefers-reduced-motion: reduce)`.

---

## 7. Components

Classes start with `k-`. Use the HTML here as is. Sample text is in English; write UI text in the product's language.

### Buttons

```html
<button class="k-btn k-btn-primary" type="button">Save</button>      <!-- Main action. One per screen -->
<button class="k-btn" type="button">Save as draft</button>            <!-- Default -->
<button class="k-btn k-btn-quiet" type="button">Cancel</button>       <!-- Dismiss. No border, no fill -->
<button class="k-btn k-btn-danger" type="button">Delete</button>      <!-- Delete -->

<button class="k-btn k-btn-sm" type="button">Small</button>           <!-- 36px -->
<button class="k-btn k-btn-lg k-btn-primary" type="button">Large</button> <!-- 54px -->
<button class="k-btn" type="button" disabled>Unavailable</button>

<!-- With icon (18px, before the text) -->
<button class="k-btn k-btn-primary" type="button"><svg …(plus)></svg>Add event</button>
<!-- Icon only (aria-label required) -->
<button class="k-btn k-btn-icon" type="button" aria-label="Open menu"><svg …(menu)></svg></button>
```

- In a row, dismiss goes on the left and the action on the right.
- Button labels say what happens, as a verb (never "OK" or "Yes").
- `<a class="k-btn">` may be used to make a link look like a button.

### Inputs

```html
<label class="k-field">Name
  <input class="k-input" type="text" placeholder="e.g. Hanako Yamada">
  <span class="k-hint">It does not have to be your real name.</span>
</label>

<!-- Error: red border, plus what is wrong and how to fix it -->
<label class="k-field">Email
  <input class="k-input" type="email" aria-invalid="true" aria-describedby="mail-error">
  <span class="k-error" id="mail-error"><svg …(circle-alert)></svg>Enter a domain after the "@".</span>
</label>

<!-- Multi-line -->
<label class="k-field">Notes<textarea class="k-input" rows="4"></textarea></label>

<!-- Select -->
<label class="k-field">Location
  <span class="k-select"><select class="k-input"><option>Tokyo</option><option>Osaka</option></select></span>
</label>
```

### Checkboxes, radio buttons, switches

```html
<label class="k-option"><input class="k-check" type="checkbox" checked> Receive notifications</label>
<label class="k-option"><input class="k-radio" type="radio" name="density" checked> Comfortable</label>

<!-- Switch: for settings that apply immediately. span.k-switch-track is required -->
<label class="k-switch">
  <input type="checkbox" checked>
  <span class="k-switch-track" aria-hidden="true"></span>
  Save automatically
</label>
```

### Cards, lists, inner surfaces, notices

```html
<div class="k-card">
  <h3 class="k-card-title">This week</h3>
  <p class="k-card-text">The library closes at 5 pm on Friday.</p>
  <ul class="k-list">
    <li class="k-list-item"><span class="k-list-item-main">Return library books</span><span class="k-list-item-sub">Due Nov 5</span></li>
    <li class="k-list-item"><span class="k-list-item-main">Review slides</span><span class="k-list-item-sub">Due Nov 8</span></li>
  </ul>
  <div class="k-nest">Notifications arrive together at 8 am every morning.</div>
</div>

<div class="k-notice">
  <h3 class="k-notice-title">Notice</h3>
  <div>The weekly summary arrives on Sunday evening.</div>
</div>
```

- List rows are separated by a 6px gap (built into `.k-list`). No divider lines.

### Badges

```html
<span class="k-badge">Draft</span>
<span class="k-badge k-badge-accent">Featured</span>
<span class="k-badge k-badge-ok"><svg …(check)></svg>Done</span>
<span class="k-badge k-badge-danger"><svg …(circle-alert)></svg>Error</span>
<span class="k-badge k-badge-info"><svg …(info)></svg>Info</span>
```

### Tabs and two-way toggles

```html
<!-- Tabs (put .k-seg on --surface) -->
<div class="k-seg" role="tablist" aria-label="Details">
  <button type="button" role="tab" id="tab-a" aria-controls="panel-a" aria-selected="true">Overview</button>
  <button type="button" role="tab" id="tab-b" aria-controls="panel-b" aria-selected="false" tabindex="-1">Usage</button>
</div>
<div class="k-nest" role="tabpanel" id="panel-a" aria-labelledby="tab-a">…</div>
<div class="k-nest" role="tabpanel" id="panel-b" aria-labelledby="tab-b" hidden>…</div>

<!-- Two-way toggle (sort order etc.) -->
<div class="k-seg" role="group" aria-label="Sort order">
  <button type="button" aria-pressed="true">Newest</button>
  <button type="button" aria-pressed="false">Oldest</button>
</div>
```

Tabs move with the left and right arrow keys. The selected background slides sideways like a knob (5 items max).

### Colour picker

Lets users choose the accent colour. Where to put it and how to save the choice: follow "14. Embedding in a product".

```html
<fieldset class="k-palette">            <!-- add k-palette-compact for swatches only -->
  <legend>Theme colour</legend>
  <div class="k-palette-items">
    <label class="k-palette-item">
      <input type="radio" name="accent" value="yamabuki" checked>
      <span class="k-palette-swatch" data-swatch="yamabuki"></span>
      <span class="k-palette-name">Yamabuki</span>
    </label>
    <!-- List all 9 the same way (value and data-swatch are palette ids; names are in "3. Colour") -->
  </div>
</fieldset>
```

- It is a radio group: selection shows with a check mark and surface colour, and arrow keys work.
- `.k-palette-compact` hides the names visually; keep `.k-palette-name` for screen readers.

### Progress bar

```html
<div class="k-bar-head"><span>Components</span><span class="k-num">72%</span></div>
<div class="k-bar" role="progressbar" aria-label="Components" aria-valuenow="72" aria-valuemin="0" aria-valuemax="100"><i style="width:72%"></i></div>
```

Show progress as a number too. `style="width:…"` here is the only inline style allowed in components.

### Dialogs, toasts

```html
<div class="k-scrim">
  <div class="k-dialog" role="dialog" aria-modal="true" aria-labelledby="dialog-title">
    <h3 class="k-dialog-title" id="dialog-title">Delete this note?</h3>
    <p class="k-dialog-text">You cannot undo this.</p>
    <div class="k-dialog-actions">
      <button class="k-btn k-btn-quiet" type="button">Cancel</button>
      <button class="k-btn k-btn-danger" type="button">Delete</button>
    </div>
  </div>
</div>

<div class="k-toast" role="status">Saved</div>
```

- When a dialog opens, move focus to its first button; Esc closes it.
- Toasts disappear after a few seconds. Do not use them for important content.

### Entrance motion

```html
<div class="k-card k-enter">…</div>
```

### Icons

Use **Lucide** (1.71.0) only. Do not mix icon sets or draw your own.

- **Never draw SVG from memory; fetch it and paste it.** Once you pick a name, fetch `https://unpkg.com/lucide-static@1.71.0/icons/<name>.svg` (list: https://lucide.dev/icons/).
- Keep `class="lucide lucide-<name>"` from the fetched SVG. The automatic check uses it to confirm the name exists.
- You may remove `width` `height` `xmlns`. Add `aria-hidden="true"`.
- `kasane.css` sets stroke width 2.5. Colour is `currentColor`. No filled icons.
- Use icons with text. Icon-only buttons need `aria-label`.

| Use | Name |
|---|---|
| Success, check | `check` |
| Error, warning | `circle-alert` |
| Info | `info` |
| Close | `x` |
| Add / edit / delete | `plus` / `pencil` / `trash-2` |
| Search / settings / notifications | `search` / `settings` / `bell` |
| Person / people | `user` / `users` |
| Menu / next | `menu` / `chevron-right` |

Size depends on placement (14px in badges, 16px in error text, 18px in buttons, 22px in icon-only buttons). Inside Kasane components this is automatic.

```html
<svg aria-hidden="true" class="lucide lucide-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
```

---

## 8. Building a component Kasane does not have

When you need something not listed here (tables, tags, navigation, calendars…), decide in this order.

1. **Check whether existing components can do it.** For example, selectable tags can be built from `.k-badge` and `.k-seg`.
2. **Pick the surface.** Decide which surface it sits on and use the next one inward ("4. Surface layering").
3. **Write it with tokens only.** Colour, radius, spacing, text size and motion all come from existing tokens.
4. **Separate with surfaces and gaps.** No borders, shadows or divider lines.
5. **Do not use the `k-` prefix.** `k-` is reserved for Kasane itself. Use your project's name or similar.

Example: table

```css
.app-table { width: 100%; border-collapse: separate; border-spacing: 0 var(--space-1); }
.app-table th { text-align: left; font-size: var(--text-xs); color: var(--muted); padding: 0 var(--space-3); }
.app-table td { background: var(--surface-2); padding: var(--space-2) var(--space-3); }
.app-table td:first-child { border-radius: var(--r-md) 0 0 var(--r-md); }
.app-table td:last-child  { border-radius: 0 var(--r-md) var(--r-md) 0; }
.app-table .amount { font-family: var(--font-num); font-variant-numeric: tabular-nums; text-align: right; }
```

Example: side navigation

```css
.app-nav a { display: flex; align-items: center; min-height: 40px; padding: 0 var(--space-3);
             border-radius: var(--r-sm); color: var(--ink); text-decoration: none; font-weight: 700; }
.app-nav a:hover { background: var(--surface-2); }
.app-nav a[aria-current="page"] { background: var(--accent-soft); color: var(--accent-ink); }
```

---

## 9. Writing

- Write UI text in the product's language. For Japanese, use です・ます style.
- Short sentences, one idea per sentence.
- Use words the user knows. Do not expose internal terms or unexplained abbreviations.
- Buttons say what happens, as a verb: "Confirm booking". Never "OK" or "Yes".
- Errors say what happened and how to fix it. Never blame the user.
- Use half-width digits. Show the weekday with dates (Japanese: 「11月5日(木)」).
- No emoji as heading decoration.

---

## 10. Common mistakes

| Tempting | Correct |
|---|---|
| `background: #ffffff;` | `background: var(--surface);` |
| `color: var(--accent);` (links) | `color: var(--accent-ink);` |
| `.card { border: 1px solid #ddd; }` | Remove the border; `background: var(--surface);` |
| `.card { box-shadow: 0 2px 8px rgba(0,0,0,.1); }` | Remove the shadow; separate with surface colour |
| `.list li + li { border-top: 1px solid var(--line); }` | `.k-list` (rows as surfaces, separated by gaps) |
| `border-radius: 8px;` | `border-radius: var(--r-md);` etc. |
| `padding: 20px;` | `padding: var(--space-5);` etc. |
| `font-family: sans-serif;` | Do not set it (already on `body`) or `var(--font-body)` |
| A price column without styling | Add `.k-num` |
| `<span style="color:green">●</span> Done` | `<span class="k-badge k-badge-ok"><svg …(check)></svg>Done</span>` |
| Drawing icon SVG from memory | Fetch from Lucide and paste |
| `button:focus { outline: none; }` | Do not write it |
| Two primary buttons side by side | Make one `.k-btn` or `.k-btn-quiet` |
| White text on a yellow button | `color: var(--on-accent);` |

---

## 11. Checks at the end of your work

Before you hand over UI, confirm every item.

- [ ] No colour values (`#`, `rgb(`, `hsl(`, `oklch(`, colour names)
- [ ] No `border`, `box-shadow` or divider lines except on input controls
- [ ] `--accent` is never a text colour. Text on `--accent` is `--on-accent`
- [ ] Radius, spacing, text size and motion duration are token values
- [ ] States (success, error, info) have an icon and words
- [ ] Every icon is fetched from Lucide (has `class="lucide lucide-…"`)
- [ ] At most one primary button per screen
- [ ] `.k-title` only on page titles and section headings. `.k-num` on numbers in columns
- [ ] No `outline: none`. Tap targets at least 44px tall
- [ ] Readable with `data-theme="dark"` and with other `data-accent` values
- [ ] No light/dark toggle. No screen that asks users to pick a colour first
- [ ] No horizontal scroll at 375px wide
- [ ] Images processed with `kasane-image` (AVIF / WebP, SSIM ≥ 0.99, `width` `height` `alt`)
- [ ] `kasane-lighthouse` minimums met (performance 90, accessibility 100, best practices 95, SEO 90)

### Check with screenshots (if you can)

If you can take screenshots (Playwright, browser control…), capture the screens you built and review them.

Combinations:

| Width | Theme | Palette |
|---|---|---|
| 1280px | Light | Yamabuki (`yamabuki`) |
| 1280px | Dark | Yamabuki (`yamabuki`) |
| 375px | Light | Ai (`ai`) |
| 375px | Dark | Sumi (`sumi`) |

Look for:

- [ ] No clipped, overlapping or overflowing text
- [ ] No horizontal scroll
- [ ] Text and buttons readable in every combination (no white text on bright yellow, etc.)
- [ ] Cards and lists distinguishable by surface colour
- [ ] Same kind of component has matching size, spacing and radius
- [ ] Primary button stands out; dismiss button is quiet
- [ ] Holds up with empty states, long names and many items (swap the data and capture again)

Fix what you find and capture again. If you cannot take screenshots, say so in your report.

Playwright example:

```js
// npx playwright install chromium, then node shot.mjs
import { chromium } from "playwright";
const url = "http://localhost:3000/users";   // the screen you built
const cases = [[1280, "light", "yamabuki"], [1280, "dark", "yamabuki"], [375, "light", "ai"], [375, "dark", "sumi"]];
const browser = await chromium.launch();
for (const [width, theme, accent] of cases) {
  const page = await browser.newPage({ viewport: { width, height: 900 } });
  await page.goto(url);
  await page.evaluate(([t, a]) => { document.documentElement.dataset.theme = t; document.documentElement.dataset.accent = a; }, [theme, accent]);
  await page.waitForTimeout(500);
  await page.screenshot({ path: `shot-${width}-${theme}-${accent}.png`, fullPage: true });
}
await browser.close();
```

---

## 12. Automatic checks

`kasane-lint` checks many rules mechanically: Stylelint for CSS, `kasane-check` for HTML.

```bash
npm install --save-dev stylelint https://kasane.y-n0.de/v1/kasane-lint-1.2.0.tgz
```

```json
// .stylelintrc.json
{ "extends": ["kasane-lint/stylelint"] }
```

```bash
npx stylelint "src/**/*.css"
npx kasane-check "src/**/*.html"
```

**At the end of your work, run both commands and fix everything they report** (in projects that have `kasane-lint`). If HTML lives inside JavaScript (React etc.), build and pass the output HTML to `kasane-check`.

### CSS rules (Stylelint)

| Rule | Finds |
|---|---|
| `kasane/no-raw-color` | Raw colours (`#…`, `rgb()`, `hsl()`, `oklch()`, colour names) |
| `kasane/no-shadow` | `box-shadow` |
| `kasane/border-only-on-inputs` | `border` outside input controls, and divider lines |
| `kasane/use-tokens` | Raw radius, spacing, text size, motion duration (warning) |
| `kasane/no-outline-none` | `outline: none` / `outline: 0` |
| `kasane/font-family-token` | `font-family` that is not a token |

### HTML rules (kasane-check)

| Rule | Finds |
|---|---|
| `kasane/one-primary` | Two or more primary buttons (`k-btn-primary`) in one file |
| `kasane/status-icon` | `k-badge-ok` `k-badge-danger` `k-badge-info` `k-error` without an icon (`<svg>`) |
| `kasane/inline-style` | Colour, shadow, border or font in a `style` attribute |
| `kasane/icon-button-label` | Buttons or links with no text and no `aria-label` |
| `kasane/form-label` | Inputs without a label |
| `kasane/switch-structure` | `k-switch` without `input[type=checkbox]` and `k-switch-track` |
| `kasane/unknown-class` | `k-` classes that Kasane does not have |
| `kasane/lucide-icon` | Lucide names that do not exist, non-Lucide icons inside components |
| `kasane/dialog-label` | `role="dialog"` without a name |
| `kasane/tab-aria` | `role="tab"` without `aria-selected` or `aria-controls` |
| `kasane/img-alt` | `<img>` without `alt` (decorative images use `alt=""`) |
| `kasane/img-size` | `<img>` without `width` and `height` |
| `kasane/img-format` | JPEG, PNG or GIF used directly (no AVIF / WebP via `<picture>`) |

Where you must depart from a rule for a reason, add `data-kasane-ignore="rule-name"` (empty for all rules) to exclude that element and its contents. State the reason in your report.

---

## 13. Images and performance

Aim for fast display and no layout shift while loading.

### Lighthouse minimums

Evaluate your screens with the Lighthouse CLI and stay at or above these scores **on both mobile and desktop**.

| Category | Minimum |
|---|---|
| Performance | 90 |
| Accessibility | 100 |
| Best practices | 95 |
| SEO | 90 |

```bash
npm install --save-dev lighthouse
npx kasane-lighthouse http://localhost:3000/ http://localhost:3000/users   # --runs 3 smooths out noise
```

When a category falls short, the causes are listed. Fix until the minimums are met. If Chrome is not found, set `CHROME_PATH`. Target metrics: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1.

### Images

Never use images as they are. **Always process them with `kasane-image` first.**

| Rule | Detail |
|---|---|
| Format | Photos and illustrations: AVIF and WebP. Icons and logos: SVG. Animation: video, not GIF |
| Size | Up to 2× the displayed size. At most 3 widths |
| Quality | SSIM ≥ 0.99 against the original (`kasane-image` checks this). Finally check by eye |
| Bytes | Over 100 KB per image: see if the width can be smaller |
| Attributes | Always `width` `height` `alt`. Off-screen images `loading="lazy"`, the first large visible image `fetchpriority="high"` |

```bash
npm install --save-dev sharp ssim.js
npx kasane-image photo.jpg --out public/img --widths 640,1280     # export, check SSIM, print <picture>
npx kasane-image --compare original.png public/img/photo.avif     # SSIM only
```

For each width and format, `kasane-image` picks the lowest quality with SSIM ≥ 0.99 and prints a `<picture>` you can paste.

### Other

- Load the font CSS without blocking: `<link rel="stylesheet" href="https://kasane.y-n0.de/v1/fonts/line-seed-jp.css" media="print" onload="this.media='all'">` (plus a normal `<link>` in `<noscript>`)
- Loading, empty and error states use the same space; never insert components above content later
- Use `kasane.min.css` in production. Add `defer` to JavaScript

---

## 14. Embedding in a product

With Kasane, the designer can set the colour and users can change it. Decide these two things first. If the request does not say, build with yamabuki as the default and no user choice, and say so in your report.

| Decision | How |
|---|---|
| Default colour | Write it in `<html data-accent="…">` |
| Can users change the colour? | If yes, put a colour picker (`.k-palette`) on the settings page or in the page footer |

### Choosing the default

| Situation | Palette |
|---|---|
| The brand has a colour | The palette closest to its hue |
| Trust, calm (booking, finance, health…) | `ai` `sora` |
| Bright, friendly (learning, everyday life…) | `yamabuki` `tachibana` `moegi` |
| Gentle, social (communities…) | `kobai` `fuji` |
| Focus on information (business tools, admin) | `sumi` |

### Where the picker goes

| Product | Place | Component |
|---|---|---|
| Has a settings page | In a group such as "Display" on the settings page | `.k-palette` (names visible) |
| No settings page | Page footer | `.k-palette.k-palette-compact` |

- Start with the default colour right away. No screen or dialog asking users to pick a colour first.
- Put the picker in one place only. Not in the header, not on every screen.
- No light/dark toggle (follow the device).

### Saving the choice

Put the script from "1. Loading" in `<head>`. Connect the picker with this JavaScript.

```js
const root = document.documentElement;
const current = root.dataset.accent || "yamabuki";
document.querySelectorAll('.k-palette input[name="accent"]').forEach((radio) => {
  radio.checked = radio.value === current;
  radio.addEventListener("change", () => {
    root.dataset.accent = radio.value;
    try { localStorage.setItem("kasane-accent", radio.value); } catch (e) {}
  });
});
```

In products with sign-in, also save the choice as a user setting on the server and write it into `data-accent` when serving HTML, so it follows the user across devices.

---

## 15. Supporting multiple languages

When one product ships in several languages, do the following. If the request does not mention languages, build in one language only.

| Decision | Rule |
|---|---|
| `<html lang>` | Write the page language. Words in another language get `lang` on their element |
| URL | The default language as is (`/pricing/`), other languages with a language code in front (`/en/pricing/`). Each page points to the same page in other languages with `hreflang` |
| Language switch | One place: the right side of the header or the footer. It goes to the same page in the other language. Never redirect based on browser settings |
| Language names | Written in that language (“English”, “日本語”), with `lang`. No flags |
| Text | Read it from translation files, not hard-coded. Never join pieces of sentences. No text in images |
| Width | No fixed widths on buttons or labels. Also screenshot the language with the longest text |
| Fonts | LINE Seed JP covers Japanese and Latin. For other scripts, add a font for that language only, as in `:root:lang(ko) { --font-body: … }` |
| Numbers and dates | Pass the page language to `Intl.DateTimeFormat` / `Intl.NumberFormat`. Use `.k-num` in columns |
| Right-to-left languages | Not checked in v1. If needed, check that mirrored screens hold up, and report |

```html
<html lang="ja">
<head>
  <link rel="canonical" href="https://example.com/pricing/">
  <link rel="alternate" hreflang="ja" href="https://example.com/pricing/">
  <link rel="alternate" hreflang="en" href="https://example.com/en/pricing/">
  <link rel="alternate" hreflang="x-default" href="https://example.com/pricing/">
</head>
<!-- Language switch (fetch Lucide's languages icon and paste it) -->
<a class="k-btn k-btn-quiet" href="/en/pricing/" hreflang="en" lang="en"><svg …(languages)></svg>English</a>
```

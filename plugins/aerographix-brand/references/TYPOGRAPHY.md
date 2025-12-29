# Aerographix Typography

## Primary Typeface

**DM Sans** — A low-contrast geometric sans-serif with balanced proportions.

### Import
```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000&display=swap" rel="stylesheet">
```

### Font Stack
```css
--font-display: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
--font-body: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
```

## Type Scale (Fluid)

| Token | Size Range | Usage |
|-------|------------|-------|
| `--text-5xl` | 48–80px | Hero headlines |
| `--text-4xl` | 40–64px | Section titles (H2) |
| `--text-3xl` | 32–48px | Subsection titles (H3) |
| `--text-2xl` | 24–32px | Card titles (H4) |
| `--text-xl` | 20–24px | Large body, taglines |
| `--text-lg` | 18–20px | Emphasized body |
| `--text-base` | 16–18px | Body text |
| `--text-sm` | 14–16px | Captions, nav links |
| `--text-xs` | 12–14px | Labels, badges |

## Typography Styles

### Headlines
```css
.headline {
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: #F5F5F7;
}
```

### Body Text
```css
.body {
  font-family: 'DM Sans', sans-serif;
  font-weight: 400;
  line-height: 1.6;
  max-width: 65ch;
  color: #8B8B9E;
}
```

### Labels & Buttons
```css
.label {
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

### Section Labels
```css
.section-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: #00A8E8;
}
```

### Gradient Text (for headlines/stats)
```css
.gradient-text {
  background: linear-gradient(135deg, #00A8E8, #00D9FF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

## CSS Custom Properties

```css
:root {
  /* Font families */
  --font-display: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Font sizes */
  --text-xs: clamp(12px, 1vw, 14px);
  --text-sm: clamp(14px, 1.2vw, 16px);
  --text-base: clamp(16px, 1.4vw, 18px);
  --text-lg: clamp(18px, 1.6vw, 20px);
  --text-xl: clamp(20px, 2vw, 24px);
  --text-2xl: clamp(24px, 2.5vw, 32px);
  --text-3xl: clamp(32px, 3.5vw, 48px);
  --text-4xl: clamp(40px, 5vw, 64px);
  --text-5xl: clamp(48px, 6vw, 80px);

  /* Font weights */
  --font-regular: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Line heights */
  --leading-tight: 1.2;
  --leading-normal: 1.5;
  --leading-relaxed: 1.6;

  /* Letter spacing */
  --tracking-tight: -0.02em;
  --tracking-normal: 0;
  --tracking-wide: 0.05em;
  --tracking-wider: 0.1em;
  --tracking-widest: 0.2em;
}
```

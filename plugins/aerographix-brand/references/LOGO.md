# Aerographix Logo

## Primary Logo (AGX Wordmark)

The primary logo consists of the **AGX** wordmark framed by two flow lines that trace a hexagonal pattern, symbolizing air flow through the graphene-enhanced filter membrane.

```
Logo Components:
├── Top flow line (air intake)
├── AGX wordmark (the membrane)
└── Bottom flow line (purified air output)
```

## Logo Concept: "The Invisible Membrane"

The three horizontal elements represent:
1. **Top line** — Contaminated air entering the filter
2. **Center** — The graphene-HEPA filtration membrane (AGX wordmark)
3. **Bottom line** — Purified air exiting

## The Hidden Hexagon

Like the famous hidden arrow in the FedEx logo, the Aerographix logo contains a **secret hexagon** formed by the negative space between the flow lines.

```
         ╱╲
        ╱  ╲         ← Top line traces upper hexagon edges
       ╱    ╲
      │      │       ← Implied vertical sides
      │ AGX  │
      │      │
       ╲    ╱
        ╲  ╱         ← Bottom line traces lower hexagon edges
         ╲╱
```

The hexagon is never explicitly drawn—it emerges from the geometry of the flow lines. This references:
- **Graphene's molecular structure** — A honeycomb lattice of carbon atoms
- **The filter membrane** — The invisible barrier that purifies air
- **Scientific precision** — Clean geometric relationships

### Hexagon Vertices (Icon logo, 80×80 viewport)

| Position | Coordinates |
|----------|-------------|
| Top | (40, 18) |
| Upper-right | (59, 29) |
| Lower-right | (59, 51) |
| Bottom | (40, 62) |
| Lower-left | (21, 51) |
| Upper-left | (21, 29) |

All six implied sides are approximately 32px, forming a regular hexagon with radius 22px centered at (40, 40).

## Logo Variants

| Variant | File | Use Case |
|---------|------|----------|
| **Full Logo** | `logo-full.svg` | Primary use, website hero, presentations |
| **Icon Only** | `logo-icon.svg` | App icons, social avatars, compact spaces |
| **Favicon** | `favicon.svg` | Browser tabs, bookmarks |

## Logo Specifications

- **Full Logo Dimensions:** 140×80 viewport
- **Icon Dimensions:** 80×80 viewport (hexagon radius: 22px, center: 40,40)
- **Minimum Clear Space:** Equal to the height of the AGX text around all sides
- **Minimum Size:**
  - Full logo: 120px width
  - Icon only: 32px width

## Logo Colors

The logo uses a gradient flow from Electric Blue to Plasma Cyan:
- Gradient start: `#00A8E8` (30% opacity at edges)
- Gradient mid: `#00A8E8` to `#00D9FF`
- Gradient end: `#00D9FF` (30% opacity at edges)

```svg
<linearGradient id="logo-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stop-color="#00A8E8" stop-opacity="0.3"/>
  <stop offset="30%" stop-color="#00A8E8"/>
  <stop offset="70%" stop-color="#00D9FF"/>
  <stop offset="100%" stop-color="#00D9FF" stop-opacity="0.3"/>
</linearGradient>
```

## Logo Animation (Web)

When animated, the logo should:
1. **Top line** draws left-to-right (air intake)
2. **Bottom line** draws right-to-left (purified output)
3. **AGX text** reveals from center outward (membrane opening)
4. Subtle glow effect on hover

### Animation CSS

```css
.logo-line {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: draw-line 1s ease forwards;
}

@keyframes draw-line {
  to { stroke-dashoffset: 0; }
}

.logo:hover {
  filter: drop-shadow(0 0 8px rgba(0, 217, 255, 0.5));
}
```

## Usage Guidelines

1. **Preserve the hidden hexagon** — When recreating, ensure angled segments align
2. **Maintain clear space** — Logo should breathe
3. **Dark backgrounds preferred** — The gradient reads best on Carbon Black
4. **No distortion** — Always scale proportionally

# Aerographix Color System

## Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Electric Blue** | `#00A8E8` | 0, 168, 232 | Primary accent, links, CTAs |
| **Plasma Cyan** | `#00D9FF` | 0, 217, 255 | Highlights, gradients, glow effects |

## Neutral Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Carbon Black** | `#0A0A0F` | 10, 10, 15 | Primary background |
| **Graphite** | `#1A1A24` | 26, 26, 36 | Secondary background, cards |
| **Steel** | `#2D2D3A` | 45, 45, 58 | Borders, dividers |
| **Silver** | `#8B8B9E` | 139, 139, 158 | Body text, secondary text |
| **White** | `#F5F5F7` | 245, 245, 247 | Headlines, primary text |

## Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| **Success Teal** | `#00C9A7` | Success states, positive metrics |
| **Heat Orange** | `#FF6B35` | Thermal/defoul mode, warnings |
| **Heat Amber** | `#FF8C42` | Secondary thermal accent |

## Gradients

```css
/* Primary Gradient - buttons, highlights, text */
--gradient-primary: linear-gradient(135deg, #00A8E8, #00D9FF);

/* Dark Background Gradient */
--gradient-dark: linear-gradient(180deg, #0A0A0F 0%, #0D0D14 100%);

/* Card Gradient */
--gradient-card: linear-gradient(145deg, #1A1A24 0%, rgba(26, 26, 36, 0.8) 100%);

/* Heat Gradient (thermal/defoul states) */
--gradient-heat: linear-gradient(135deg, #FF6B35, #FF8C42);
```

## Logo Gradient
The logo uses a gradient flow from Electric Blue to Plasma Cyan:
- Gradient start: `#00A8E8` (30% opacity at edges)
- Gradient mid: `#00A8E8` to `#00D9FF`
- Gradient end: `#00D9FF` (30% opacity at edges)

## Usage Guidelines

1. **Dark Mode First** — The brand is designed dark-mode native. Light backgrounds should be used sparingly.

2. **Gradient Text** — Headlines and statistics can use the primary gradient:
```css
background: linear-gradient(135deg, #00A8E8, #00D9FF);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```

3. **Glow Effects** — Use `box-shadow` with Electric Blue/Plasma Cyan at low opacity for interactive elements:
```css
box-shadow: 0 0 30px rgba(0, 168, 232, 0.3);
```

4. **Contrast** — Ensure WCAG AA compliance. Silver (#8B8B9E) on Carbon Black meets accessibility standards.

## CSS Custom Properties

```css
:root {
  /* Primary */
  --color-electric-blue: #00A8E8;
  --color-plasma-cyan: #00D9FF;

  /* Neutrals */
  --color-carbon-black: #0A0A0F;
  --color-graphite: #1A1A24;
  --color-steel: #2D2D3A;
  --color-silver: #8B8B9E;
  --color-white: #F5F5F7;

  /* Semantic */
  --color-success: #00C9A7;
  --color-heat: #FF6B35;
  --color-heat-secondary: #FF8C42;

  /* Gradients */
  --gradient-primary: linear-gradient(135deg, #00A8E8, #00D9FF);
  --gradient-dark: linear-gradient(180deg, #0A0A0F 0%, #0D0D14 100%);
  --gradient-card: linear-gradient(145deg, #1A1A24, rgba(26, 26, 36, 0.8));
  --gradient-heat: linear-gradient(135deg, #FF6B35, #FF8C42);
}
```

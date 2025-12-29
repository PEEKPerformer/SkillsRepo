# Aerographix Components

## Buttons

### Primary Button
```css
.btn-primary {
  background: linear-gradient(135deg, #00A8E8, #00D9FF);
  color: #0A0A0F;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  box-shadow: 0 0 30px rgba(0, 168, 232, 0.3);
  transform: translateY(-2px);
}
```

### Secondary Button
```css
.btn-secondary {
  background: transparent;
  color: #F5F5F7;
  padding: 12px 24px;
  border: 1px solid #2D2D3A;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  border-color: #00A8E8;
  color: #00A8E8;
}
```

## Cards

### Standard Card
```css
.card {
  background: linear-gradient(145deg, #1A1A24, rgba(26, 26, 36, 0.8));
  border: 1px solid #2D2D3A;
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
}

.card:hover {
  border-color: #00A8E8;
  box-shadow: 0 8px 40px rgba(0, 168, 232, 0.15);
}
```

### Stat Card
```css
.stat-card {
  background: linear-gradient(145deg, #1A1A24, rgba(26, 26, 36, 0.8));
  border: 1px solid #2D2D3A;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
}

.stat-value {
  font-size: 48px;
  font-weight: 700;
  background: linear-gradient(135deg, #00A8E8, #00D9FF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: #8B8B9E;
  margin-top: 8px;
}
```

## Icons

- **Style:** Line icons, 2px stroke weight
- **Corner style:** Rounded (`stroke-linecap: round; stroke-linejoin: round`)
- **Color:** Electric Blue (#00A8E8) or Silver (#8B8B9E)
- **Sizes:** 16px (inline), 24px (standard), 48px (featured)

```css
.icon {
  stroke: #00A8E8;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}
```

## Glow Effects

```css
/* Standard glow */
.glow {
  box-shadow: 0 0 30px rgba(0, 168, 232, 0.3);
}

/* Logo/icon glow */
.icon-glow {
  filter: drop-shadow(0 0 8px rgba(0, 217, 255, 0.5));
}

/* Focus state glow */
.focus-glow:focus {
  outline: 2px solid #00D9FF;
  outline-offset: 3px;
  box-shadow: 0 0 12px rgba(0, 217, 255, 0.4);
}
```

## Shadows

```css
--shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
--shadow-md: 0 4px 20px rgba(0, 0, 0, 0.4);
--shadow-lg: 0 8px 40px rgba(0, 0, 0, 0.5);
```

## Spacing System

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | 6px | Tight spacing, inline elements |
| `--space-sm` | 12px | Small gaps, button padding |
| `--space-md` | 16px | Standard spacing |
| `--space-lg` | 24px | Section content gaps |
| `--space-xl` | 32px | Major section padding |
| `--space-2xl` | 40px | Section margins |
| `--space-3xl` | 48px | Large section gaps |
| `--space-4xl` | 64px | Page-level spacing |

## Layout

- **Container max-width:** 1200px
- **Container padding:** 16px–48px (fluid)
- **Border radius (standard):** 8px
- **Border radius (large/cards):** 16px

```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 clamp(16px, 4vw, 48px);
}
```

## Animation & Motion

### Transitions
```css
--transition-fast: 0.15s ease;    /* Micro-interactions */
--transition-base: 0.3s ease;     /* Standard transitions */
--transition-slow: 0.5s ease;     /* Page/section animations */
```

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Hexagon Pattern (Background Texture)

For subtle graphene honeycomb background:

```css
/* Hexagon dimensions */
Hexagon side: ~18px
Stroke: 1px
Color: Electric Blue at 50% opacity (#00A8E880)
```

Use sparingly as a subtle background texture or in technical diagrams.

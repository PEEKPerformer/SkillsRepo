# Color Palettes Reference

Six colorblind-safe palettes tested for deuteranopia, protanopia, and tritanopia.

## Palette Selection Guide

| Palette | Best For |
|---------|----------|
| Ocean | Default choice, professional scientific figures |
| Earth | Geological, environmental, organic data |
| Okabe-Ito | Maximum accessibility, multiple data series |
| Tol Bright | High contrast, many categories |
| Vibrant | Presentations, posters, eye-catching |
| Monochrome | Sequential data, minimal distraction |

## Usage

```python
from scripts.style_config import apply_style, get_palette, get_colors

# Apply style and get palette
palette = apply_style('okabe_ito')

# Use colors
ax.plot(x, y, color=palette['primary'])
ax.plot(x2, y2, color=palette['secondary'])

# Get list of colors for multiple series
colors = get_colors('okabe_ito', n=5)
```

---

## Ocean (Default)

Analogous blue palette with complementary orange highlight.

| Role | Hex | Color |
|------|-----|-------|
| Primary | `#0077B6` | Deep ocean blue |
| Secondary | `#00B4D8` | Cyan accent |
| Tertiary | `#90E0EF` | Light sky |
| Highlight | `#FF6B35` | Orange (emphasis) |
| Neutral | `#6C757D` | Gray |

**Color Theory**: Analogous blues create harmony; complementary orange provides contrast for key data points.

---

## Earth

Warm analogous palette for geological and environmental data.

| Role | Hex | Color |
|------|-----|-------|
| Primary | `#8B4513` | Saddle brown |
| Secondary | `#D2691E` | Chocolate |
| Tertiary | `#F4A460` | Sandy brown |
| Highlight | `#228B22` | Forest green |
| Neutral | `#696969` | Dim gray |

**Best For**: Soil data, geological samples, organic materials, environmental studies.

---

## Okabe-Ito

The gold standard for colorblind accessibility in scientific publishing.

| Role | Hex | Color |
|------|-----|-------|
| Primary | `#0072B2` | Blue |
| Secondary | `#E69F00` | Orange |
| Tertiary | `#009E73` | Bluish green |
| Highlight | `#D55E00` | Vermillion |
| Neutral | `#999999` | Gray |
| Extra 1 | `#CC79A7` | Pink |
| Extra 2 | `#F0E442` | Yellow |
| Extra 3 | `#56B4E9` | Sky blue |

**Why Use**: Designed specifically for scientific figures. All 8 colors remain distinguishable under all forms of color blindness.

**Reference**: Okabe & Ito (2008) "Color Universal Design"

---

## Tol Bright

Paul Tol's optimized high-contrast qualitative palette.

| Role | Hex | Color |
|------|-----|-------|
| Primary | `#4477AA` | Blue |
| Secondary | `#EE6677` | Red |
| Tertiary | `#228833` | Green |
| Highlight | `#CCBB44` | Yellow |
| Neutral | `#BBBBBB` | Gray |
| Extra 1 | `#66CCEE` | Cyan |
| Extra 2 | `#AA3377` | Purple |

**Best For**: Categorical data with many groups, maximizing visual distinction.

**Reference**: Paul Tol's Notes on Color Schemes

---

## Vibrant

High saturation palette for maximum visual impact.

| Role | Hex | Color |
|------|-----|-------|
| Primary | `#0051A5` | Vibrant blue |
| Secondary | `#FF6B35` | Bright orange |
| Tertiary | `#00A878` | Teal green |
| Highlight | `#9B59B6` | Purple |
| Neutral | `#808080` | Gray |

**Best For**: Presentations, posters, situations where visual impact matters more than subtlety.

---

## Monochrome

Single-hue gradient for sequential or minimal color needs.

| Role | Hex | Color |
|------|-----|-------|
| Primary | `#1A365D` | Dark blue |
| Secondary | `#2B6CB0` | Medium blue |
| Tertiary | `#63B3ED` | Light blue |
| Highlight | `#E53E3E` | Red (single emphasis) |
| Neutral | `#718096` | Blue-gray |

**Best For**: Sequential data, time series, when color shouldn't distract from the data pattern.

---

## Color Theory Principles

### Analogous
Colors adjacent on the color wheel (e.g., Ocean blues). Creates harmony and cohesion.

### Complementary
Colors opposite on the wheel (e.g., blue + orange). Creates contrast and emphasis.

### Triadic
Three colors equally spaced (e.g., blue, red, yellow). Balanced contrast.

### When to Use Which

| Goal | Palette |
|------|---------|
| Safe default | Ocean |
| Accessibility priority | Okabe-Ito |
| Many categories (5+) | Tol Bright or Okabe-Ito |
| Emphasis on one point | Monochrome + highlight |
| Presentation impact | Vibrant |
| Domain-specific (geology) | Earth |

---

## Colorblind Simulation

To verify your figure works for colorblind viewers:

1. **Coblis** (Color Blindness Simulator): https://www.color-blindness.com/coblis-color-blindness-simulator/
2. **Sim Daltonism** (macOS app)
3. **matplotlib**: Use `plt.style.use('seaborn-colorblind')`

All palettes in this guide have been tested against:
- Deuteranopia (red-green, most common)
- Protanopia (red-green)
- Tritanopia (blue-yellow, rare)

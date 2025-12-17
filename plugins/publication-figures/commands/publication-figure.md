---
description: Generate publication-quality scientific figures with matplotlib. Use when creating plots, charts, graphs for papers, posters, or scientific visualization. Supports scatter, line, bar, dual-axis, log-scale plots with error bars, colorbars, insets, and annotations. Includes 6 colorblind-safe color palettes. Optional SEM (Scanning Electron Microscopy) image processing for microscopy figures.
---

# Publication Figure Generation

Generate publication-ready scientific figures following rigorous style guidelines.

## Quick Start

```python
from scripts.style_config import apply_style, get_palette
from scripts.export_figure import export_figure
from scripts.plot_helpers import add_panel_letter, configure_legend

# Apply style with chosen palette
palette = apply_style('okabe_ito')  # or 'ocean', 'vibrant', etc.

# Create figure...
fig, ax = plt.subplots()
ax.plot(x, y, color=palette['primary'])

# Export with mandatory preview
export_figure(fig, 'output/my_figure')
# Creates: my_figure.pdf, my_figure.png, my_figure.svg, my_figure_preview.png
```

## CRITICAL: Image Reading Protocol

After generating figures:
- **ONLY read `*_preview.png` files** for visual verification
- **NEVER read high-res PNG/PDF/SVG** - may crash session
- Preview is 72 DPI, safe to load

## Workflow

1. **Assess data** - Read CSV/data files, determine plot type
2. **Select palette** - Choose from 6 colorblind-safe options (see `references/COLOR_PALETTES.md`)
3. **Apply style** - Call `apply_style(palette_name)`
4. **Create plot** - Use helpers from `scripts/plot_helpers.py`
5. **Export** - Call `export_figure()` which auto-generates preview

## Available Palettes

| Name | Best For |
|------|----------|
| `ocean` | Default, professional blue tones |
| `earth` | Geological, environmental data |
| `okabe_ito` | Maximum colorblind accessibility |
| `tol_bright` | High contrast, many categories |
| `vibrant` | Presentations, eye-catching |
| `monochrome` | Sequential data, minimal color |

## Reference Files

- `references/STYLE_GUIDE.md` - Typography, lines, layout rules
- `references/COLOR_PALETTES.md` - Detailed palette info with hex codes
- `references/PLOT_EXAMPLES.md` - Code snippets for each plot type
- `references/ADVANCED_TECHNIQUES.md` - Path effects, fancy arrows, transforms, custom colormaps
- `references/SEM_GUIDE.md` - SEM image processing (optional module)

## SEM Image Processing (Optional)

For microscopy figures, use the SEM module:

```python
from scripts.sem import (
    load_sem_tiff,           # Load with optional info bar cropping
    apply_clahe,             # Enhance contrast
    InteractiveScaleBarSelector,  # Click to measure scale bar
    find_zoom_region,        # Auto-detect zoom box location
    draw_scale_bar,          # Add scale bar annotation
)

# Load image (crops info bar by default)
img = load_sem_tiff('image.tif', crop_info_bar=True)

# Measure scale bar interactively
from scripts.sem import measure_scale_bar_from_clicks
calibration = measure_scale_bar_from_clicks(img, physical_size=10, physical_unit='um')
```

## Key Style Rules

- **Fonts**: Arial, 20pt minimum, 32pt bold for panel letters
- **Lines**: 2pt minimum, 3.5pt for data
- **Markers**: White edges (2.5pt), circles for primary data
- **Bar charts**: Use `draw_rounded_bar()` for uniform rounded corners (set axis limits first)
- **All spines visible** - no hidden axes
- **No grids** - clean appearance
- **Export**: 300 DPI for publication, 72 DPI preview for Claude

## Elevating Your Figures

When a figure needs extra polish—annotations on busy backgrounds, connections between subplots, or highlighted regions—consider techniques from `references/ADVANCED_TECHNIQUES.md`:

- **Path effects**: Text halos/outlines for legibility over data
- **FancyArrowPatch / ConnectionPatch**: Curved arrows, cross-axes links
- **axhspan / axvspan**: Subtle background bands for regions of interest
- **Blended transforms**: Axis-spanning highlights with data-specific x/y bounds
- **Custom colormaps**: Quick gradients from a few colors

These aren't always needed, but when the standard approach feels limited, they can make the difference between a good figure and a great one.

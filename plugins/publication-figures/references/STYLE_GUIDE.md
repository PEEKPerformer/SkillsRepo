# Figure Style Guide

Publication-quality style rules for scientific figures.

## Typography

### Font Sizes
| Element | Size | Weight |
|---------|------|--------|
| Panel letters (A, B, C, D) | 32pt | Bold |
| Axis labels | 22pt | Normal |
| Tick labels | 20pt | Normal |
| Annotations | 18pt | Normal |
| Legend text | 20pt | Normal |
| Colorbar labels | 22pt | Normal |
| Inset labels | 16pt | Normal |

### Font Family
- **Primary**: Arial (universal compatibility)
- **Fallback**: sans-serif

### Panel Letters
- Position: (0.03, 0.97) in axes coordinates (top-left)
- Use `add_panel_letter(ax, 'A')` from plot_helpers

## Line Properties

| Element | Width |
|---------|-------|
| Data lines | 3.5pt |
| Axis spines | 2.0pt |
| Tick marks | 2.0pt |
| Marker edges | 2.5pt |
| Legend frame | 2.5pt |
| Reference lines | 3.0pt |
| Annotation arrows | 2.5pt |

### Line Styles
- **Primary data**: Solid
- **Secondary data**: Solid, lower alpha (0.7)
- **Reference lines**: Dashed `--` or dotted `:`
- **Connecting lines**: Solid, 30-40% alpha

## Markers

| Data Type | Marker | Size |
|-----------|--------|------|
| Primary data | Circle `o` | 12pt |
| Comparison | Square `s` | 12pt |
| Tertiary | Triangle `^` | 12pt |
| Scatter plots | - | 200-400 (s parameter) |

- **Edge color**: White (`markeredgecolor='white'`)
- **Edge width**: 2.5pt

## Layout

### Figure Size
- Default: 18 x 14 inches (2x2 grid)
- Aspect ratio: 9:7

### GridSpec Parameters
```python
GridSpec(2, 2, figure=fig,
         hspace=0.28,  # Vertical spacing
         wspace=0.35,  # Horizontal spacing
         left=0.08, right=0.94,
         top=0.96, bottom=0.06)
```

### Spines
- **All spines visible** (top, right, bottom, left)
- No hidden axes - creates clean frame

## Axes

### Tick Parameters
- Major tick size: 7pt
- Major tick width: 2pt
- Direction: outward (default)

### Axis Labels
- Format: `Quantity (Units)` not `Quantity [Units]`
- Use Unicode: ° (degree), Δ (delta), μ (micro), ², ³

### Logarithmic Axes
- Use when data spans >2 orders of magnitude
- `ax.set_xscale('log')` or `ax.set_yscale('log')`

## Legends

```python
legend = ax.legend(frameon=True, loc='upper right',
                   fontsize=20, fancybox=False, shadow=False)
legend.get_frame().set_linewidth(2.5)
legend.get_frame().set_edgecolor('black')
legend.get_frame().set_facecolor('white')
legend.get_frame().set_alpha(0.95)
```

- Frame: Always on, black border
- Background: White, 95% opacity
- No shadow, no fancy box

## Colorbars

```python
cbar = fig.colorbar(mappable, ax=ax, pad=0.02, aspect=30, shrink=0.95)
cbar.set_label('Label', fontsize=22, rotation=270, labelpad=30)
```

- Position: Right of axes
- Label rotation: 270° (bottom-to-top)

## Annotations

### Text Boxes
```python
bbox=dict(boxstyle='round,pad=0.4',
          facecolor='white',
          edgecolor=color,  # Match data color
          linewidth=2.5,
          alpha=0.95)
```

### Arrows
```python
arrowprops=dict(arrowstyle='->',
                color=color,
                lw=2.5)
```

## Visual Hierarchy (Z-ordering)

1. **Foreground** (zorder=10): Primary data points
2. **Mid-ground** (zorder=5): Connecting lines, secondary data
3. **Background** (default): Reference lines, grid (if any)

## Alpha (Transparency)

| Element | Alpha |
|---------|-------|
| Primary data | 0.9-1.0 |
| Connecting lines | 0.3-0.4 |
| Reference lines | 0.4-0.6 |
| Annotation boxes | 0.95 |

## Export Settings

- **DPI**: 300 (publication), 72 (preview)
- **Formats**: PDF (vector), PNG (raster), SVG (editable)
- **Background**: White (`facecolor='white'`)
- **Bounding**: Tight (`bbox_inches='tight'`)

## Anti-Patterns to Avoid

### Typography
- Font sizes < 18pt
- Bold axis labels
- Mixing font families

### Colors
- jet/rainbow colormaps
- More than 4-5 colors per figure
- Low contrast on white background

### Layout
- Hidden spines
- Grid lines (visual clutter)
- Inconsistent margins

### Data
- Lines < 2pt (invisible when printed)
- Markers without white edges
- Overlapping annotations

# Advanced Matplotlib Techniques

Lesser-known matplotlib features that can elevate figures from functional to polished. Use these selectively—they add refinement when the situation calls for it, but standard approaches are often sufficient.

## When to Reach for These

Consider advanced techniques when:
- Annotations need to stand out on busy backgrounds
- You're connecting elements across multiple subplots
- Highlighting specific data regions would aid interpretation
- Standard arrows/shapes feel too rigid or plain
- You need precise positioning that's independent of data coordinates

---

## Path Effects

The `matplotlib.patheffects` module adds visual depth to text and lines. Particularly useful for legibility on varied backgrounds.

```python
import matplotlib.patheffects as pe

# Text with outline/halo - great for labels over data
text = ax.text(x, y, 'Label', fontsize=18)
text.set_path_effects([
    pe.withStroke(linewidth=4, foreground='white'),  # White outline
])

# Subtle glow effect (layered strokes)
text.set_path_effects([
    pe.withStroke(linewidth=6, foreground='white', alpha=0.3),
    pe.withStroke(linewidth=3, foreground='white'),
    pe.Normal(),
])

# Drop shadow on lines
line, = ax.plot(x, y, color='black', linewidth=2)
line.set_path_effects([pe.SimpleLineShadow(), pe.Normal()])
```

**When to use:** Labels placed over plotted data, text on images/heatmaps, emphasis on specific annotations.

---

## Fancy Arrows and Connections

### FancyArrowPatch

More control than basic `annotate` arrows. Supports curved paths and various head styles.

```python
from matplotlib.patches import FancyArrowPatch

# Curved arrow with custom style
arrow = FancyArrowPatch(
    (x1, y1), (x2, y2),
    connectionstyle='arc3,rad=0.3',  # Curved path
    arrowstyle='-|>',                # Arrow head style
    mutation_scale=20,               # Head size
    color=palette['primary'],
    linewidth=2,
)
ax.add_patch(arrow)

# Connection styles: 'arc3', 'angle', 'angle3', 'bar'
# Arrow styles: '->', '-|>', '<->', 'fancy', 'simple', 'wedge'
```

### ConnectionPatch

Draw arrows between different axes—essential for linking related data across subplots.

```python
from matplotlib.patches import ConnectionPatch

# Arrow from point in ax1 to point in ax2
arrow = ConnectionPatch(
    xyA=(x1, y1), xyB=(x2, y2),
    coordsA='data', coordsB='data',
    axesA=ax1, axesB=ax2,
    arrowstyle='->',
    color='gray',
    linewidth=1.5,
)
fig.add_artist(arrow)
```

**When to use:** Showing data flow between panels, linking overview with detail view, callouts to specific features.

---

## Annotation Box Styles

The `bbox` argument in `ax.annotate()` accepts all FancyBboxPatch styles:

```python
# Rounded box (default-ish but explicit)
ax.annotate('Note', xy=(x, y), xytext=(x+1, y+1),
    arrowprops=dict(arrowstyle='->', color='black'),
    bbox=dict(boxstyle='round,pad=0.3', fc='wheat', ec='black', lw=1.5))

# Available box styles:
# 'round'      - Rounded corners
# 'round4'     - More rounded
# 'roundtooth' - Wavy edges
# 'sawtooth'   - Zigzag edges
# 'larrow'     - Left-pointing arrow shape
# 'rarrow'     - Right-pointing arrow shape
# 'darrow'     - Double arrow (left+right)
# 'circle'     - Circular/elliptical

# Arrow box pointing at data
ax.annotate('Peak', xy=(peak_x, peak_y),
    bbox=dict(boxstyle='rarrow,pad=0.3', fc='white', ec=palette['primary'], lw=2))
```

**When to use:** Callouts that need visual distinction, directional annotations, styled legends.

---

## Shapes and Patches

Beyond rectangles—for radial elements, regions, and custom shapes.

```python
from matplotlib.patches import Wedge, Arc, Ellipse, FancyBboxPatch

# Pie-like wedge (angles in degrees)
wedge = Wedge((cx, cy), r=1.0, theta1=0, theta2=90,
              facecolor=palette['primary'], alpha=0.3, edgecolor='black')
ax.add_patch(wedge)

# Arc (unfilled wedge)
arc = Arc((cx, cy), width=2, height=2, angle=0, theta1=0, theta2=180,
          linewidth=2, color=palette['secondary'])
ax.add_patch(arc)

# Ellipse
ellipse = Ellipse((cx, cy), width=2, height=1, angle=45,
                  facecolor='none', edgecolor=palette['tertiary'], linewidth=2)
ax.add_patch(ellipse)

# Fancy box with explicit style
box = FancyBboxPatch((x, y), width, height,
                      boxstyle='round,pad=0.02,rounding_size=0.1',
                      facecolor='white', edgecolor='black', linewidth=1.5)
ax.add_patch(box)
```

**When to use:** Phase diagrams, angular data, highlighting circular/radial regions, custom callout shapes.

**Note:** For bar charts with rounded corners, use `draw_rounded_bar()` from `scripts/plot_helpers.py` instead—it handles aspect ratio compensation automatically.

---

## Transforms and Coordinate Mixing

### Blended Transforms

Mix data coordinates on one axis with axes coordinates on the other. Perfect for shaded regions that span full height/width but specific data ranges.

```python
from matplotlib.transforms import blended_transform_factory

# X in data coords, Y spans full axes height
trans = blended_transform_factory(ax.transData, ax.transAxes)

# Shaded region from x=10 to x=20, full height
ax.axvspan(10, 20, alpha=0.2, color=palette['highlight'])  # Simple way

# Or with more control:
from matplotlib.patches import Rectangle
rect = Rectangle((10, 0), width=10, height=1, transform=trans,
                  facecolor=palette['highlight'], alpha=0.2)
ax.add_patch(rect)
```

### Scaled Translation

Offset elements by points/inches rather than data units. Useful for consistent label positioning regardless of data scale.

```python
from matplotlib.transforms import ScaledTranslation

# Offset text by 5 points right and 5 points up
offset = ScaledTranslation(5/72, 5/72, fig.dpi_scale_trans)
trans = ax.transData + offset

ax.text(x, y, 'Label', transform=trans)
```

**When to use:** Background bands for experimental conditions, consistent annotation offsets, axis-spanning highlights.

---

## Spine Customization

Beyond just hiding spines—truncate, offset, or bound them.

```python
# Offset spines outward (away from data)
ax.spines['left'].set_position(('outward', 10))    # 10 points out
ax.spines['bottom'].set_position(('outward', 10))

# Hide top/right (common for clean look)
ax.spines[['top', 'right']].set_visible(False)

# Truncated spine (only spans data range)
ax.spines['bottom'].set_bounds(0, 10)  # Spine from 0 to 10 only
ax.spines['left'].set_bounds(0, 100)

# Centered spines (origin at zero)
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
```

**When to use:** Minimalist scientific style, emphasizing specific data ranges, origin-centered plots.

---

## Background Regions and Bands

Subtle highlighting without overwhelming the data.

```python
# Horizontal band (full width)
ax.axhspan(ymin=50, ymax=75, alpha=0.15, color=palette['highlight'],
           label='Target range')

# Vertical band (full height)
ax.axvspan(xmin=10, xmax=20, alpha=0.15, color=palette['secondary'],
           label='Treatment period')

# Gradient background via imshow
import numpy as np
gradient = np.linspace(0, 1, 256).reshape(1, -1)
ax.imshow(gradient, aspect='auto', cmap='Blues', alpha=0.1,
          extent=[ax.get_xlim()[0], ax.get_xlim()[1],
                  ax.get_ylim()[0], ax.get_ylim()[1]],
          zorder=0)
```

**When to use:** Indicating experimental phases, threshold regions, baseline periods, acceptable ranges.

---

## Custom Colormaps

Quick gradients from a few colors without hunting for the perfect built-in.

```python
from matplotlib.colors import LinearSegmentedColormap

# Two-color gradient
cmap = LinearSegmentedColormap.from_list('custom', ['#2E86AB', '#F24236'])

# Multi-stop gradient
cmap = LinearSegmentedColormap.from_list('custom',
    ['#1a1a2e', '#16213e', '#0f3460', '#e94560'])

# With explicit positions (0-1 range)
colors = [(0, '#2E86AB'), (0.5, '#FFFFFF'), (1, '#F24236')]
cmap = LinearSegmentedColormap.from_list('diverging',
    [c[1] for c in colors])

# Use it
scatter = ax.scatter(x, y, c=values, cmap=cmap)
```

**When to use:** Brand colors, custom diverging scales, matching existing figure schemes.

---

## Anchored Elements

Position elements relative to axes corners robustly, regardless of data range.

```python
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredText
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker

# Simple anchored text
anchored_text = AnchoredText('n = 150', loc='upper left', frameon=True,
                              prop=dict(fontsize=16))
anchored_text.patch.set_boxstyle('round,pad=0.3')
anchored_text.patch.set_edgecolor('black')
ax.add_artist(anchored_text)

# Multiple text elements packed together
texts = [TextArea('Mean: 42.3', textprops=dict(fontsize=14)),
         TextArea('SD: 5.7', textprops=dict(fontsize=14))]
box = HPacker(children=texts, align='left', pad=5, sep=5)
anchored = AnchoredOffsetbox(loc='upper right', child=box, frameon=True)
ax.add_artist(anchored)
```

**When to use:** Statistics boxes, sample size annotations, any text that should stay in a corner regardless of axis limits.

---

## Quick Reference

| Technique | Import | Primary Use |
|-----------|--------|-------------|
| Path effects | `matplotlib.patheffects` | Text legibility, shadows |
| FancyArrowPatch | `matplotlib.patches` | Curved/styled arrows |
| ConnectionPatch | `matplotlib.patches` | Cross-axes arrows |
| Wedge/Arc/Ellipse | `matplotlib.patches` | Radial shapes |
| blended_transform_factory | `matplotlib.transforms` | Mixed coordinate systems |
| axhspan/axvspan | Built-in | Background bands |
| LinearSegmentedColormap | `matplotlib.colors` | Custom gradients |
| AnchoredText | `mpl_toolkits.axes_grid1` | Fixed-position annotations |

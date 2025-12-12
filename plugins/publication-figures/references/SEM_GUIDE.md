# SEM Image Processing Guide

Optional module for Scanning Electron Microscopy figure generation.

## Quick Start

```python
from scripts.sem import (
    load_sem_tiff,
    apply_clahe,
    draw_scale_bar,
    draw_panel_label,
    InteractiveScaleBarSelector,
    find_zoom_region,
)
```

## Loading Images

### Basic Load

```python
# Load and crop info bar (default)
img = load_sem_tiff('image.tif')

# Keep info bar for scale bar measurement
img_full = load_sem_tiff('image.tif', crop_info_bar=False)

# Custom crop position
img = load_sem_tiff('image.tif', crop_y=900)
```

### Image Info

```python
from scripts.sem import get_image_info

info = get_image_info('image.tif')
# Returns: size, shape, dtype, min, max, mean, mode
```

## Image Enhancement

### Gamma Correction

For lifting shadows in dark images:

```python
from scripts.sem import apply_gamma

# gamma < 1 brightens shadows
enhanced = apply_gamma(img, gamma=0.85)
```

### CLAHE (Adaptive Histogram Equalization)

For revealing detail under bright particles:

```python
from scripts.sem import apply_clahe

# Useful for bright particles on dark background
enhanced = apply_clahe(img, clip_limit=0.02)
```

### Auto Enhancement

```python
from scripts.sem import enhance_sem_image

# Automatically chooses method based on image statistics
enhanced = enhance_sem_image(img, method='auto')
# Options: 'auto', 'gamma', 'clahe', 'none'
```

## Scale Bar Measurement

### Interactive Selection

Click left and right edges of the scale bar:

```python
from scripts.sem import InteractiveScaleBarSelector

selector = InteractiveScaleBarSelector(img)
result = selector.run()
# Returns: {'pixel_width': 344, 'points': [(x1, y1), (x2, y2)]}
```

### With Calibration

```python
from scripts.sem import measure_scale_bar_from_clicks

calibration = measure_scale_bar_from_clicks(
    'image.tif',
    physical_size=10,
    physical_unit='um'
)
# Returns: pixel_width, physical_size, pixels_per_unit
```

### Calculate Programmatically

```python
from scripts.sem import calculate_scale_bar_pixels

# If you know the image calibration
bar_px = calculate_scale_bar_pixels(
    physical_size=10,       # 10 um bar
    physical_unit='um',
    image_width_px=1024,
    image_width_physical=30  # 30 um field of view
)
```

## Drawing Annotations

### Scale Bar

```python
import matplotlib.pyplot as plt
from scripts.sem import draw_scale_bar

fig, ax = plt.subplots()
ax.imshow(img, cmap='gray')

draw_scale_bar(ax,
               scale_text='10 um',
               pixel_width=344,
               position='bottom-right')
```

### Panel Label

```python
from scripts.sem import draw_panel_label

draw_panel_label(ax, 'A',
                 position='top-left',
                 fontsize=24,
                 text_color='white',
                 bg_color='black')
```

### Zoom Box

```python
from scripts.sem import draw_zoom_box

draw_zoom_box(ax,
              box_coords=(606, 554, 708, 642),
              color='gold',
              linewidth=2,
              alpha=0.3)
```

## Zoom Region Detection

Automatically find where a high-magnification image corresponds to in a low-magnification overview:

```python
from scripts.sem import find_zoom_region, validate_zoom_match

# Load both images
low_mag = load_sem_tiff('overview_5000x.tif')
high_mag = load_sem_tiff('detail_50000x.tif')

# Find zoom region
result = find_zoom_region(low_mag, high_mag, scale_range=(8, 12))
# Returns: box, scale, correlation, center

# Validate match
validation = validate_zoom_match(low_mag, high_mag, result['box'])
print(f"Valid: {validation['valid']}, Correlation: {validation['correlation']:.3f}")
```

### Algorithm Details

1. **Gradient extraction**: Sobel edge detection (consistent across magnifications)
2. **Multi-scale search**: Tests scale factors in given range
3. **FFT cross-correlation**: O(n log n) efficient matching
4. **Peak detection**: Finds best correlation location

## Complete Example

```python
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scripts.sem import (
    load_sem_tiff, apply_clahe, enhance_sem_image,
    draw_scale_bar, draw_panel_label, draw_zoom_box,
    find_zoom_region
)
from scripts.export_figure import export_figure

# Load images
panel_a = load_sem_tiff('sample_top.tif')
panel_b = enhance_sem_image(load_sem_tiff('sample_bottom.tif'), method='gamma')
panel_c = load_sem_tiff('overview_5000x.tif')
panel_d = apply_clahe(load_sem_tiff('detail_50000x.tif'))

# Detect zoom region
zoom = find_zoom_region(panel_c, panel_d)

# Create figure
fig = plt.figure(figsize=(12, 10))
gs = GridSpec(2, 2, figure=fig, hspace=0.1, wspace=0.1)

# Panel A
ax_a = fig.add_subplot(gs[0, 0])
ax_a.imshow(panel_a, cmap='gray')
ax_a.axis('off')
draw_panel_label(ax_a, 'A')
draw_scale_bar(ax_a, '10 um', 344)

# Panel B
ax_b = fig.add_subplot(gs[0, 1])
ax_b.imshow(panel_b, cmap='gray')
ax_b.axis('off')
draw_panel_label(ax_b, 'B')
draw_scale_bar(ax_b, '10 um', 344)

# Panel C (with zoom box)
ax_c = fig.add_subplot(gs[1, 0])
ax_c.imshow(panel_c, cmap='gray')
ax_c.axis('off')
draw_panel_label(ax_c, 'C')
draw_scale_bar(ax_c, '10 um', 344)
draw_zoom_box(ax_c, zoom['box'], color='gold')

# Panel D
ax_d = fig.add_subplot(gs[1, 1])
ax_d.imshow(panel_d, cmap='gray')
ax_d.axis('off')
draw_panel_label(ax_d, 'D')
draw_scale_bar(ax_d, '1 um', 344)

export_figure(fig, 'output/sem_figure')
```

## Common Issues

### Info Bar Cropping
- Default crop at y=875 works for 1024x943 images
- Adjust `crop_y` for different image sizes
- Set `crop_info_bar=False` to measure scale bar from metadata region

### Scale Bar Detection
- Automated detection unreliable - use interactive tool
- Typical values: ~343-344 px for 10 um on 1024 px wide images

### Enhancement Choices
| Condition | Method | Settings |
|-----------|--------|----------|
| Dark overall | Gamma | 0.85 |
| Bright particles crushing background | CLAHE | clip_limit=0.02 |
| Good contrast | None | - |

### Zoom Matching
- Works best with 8-12x magnification difference
- Gradient-based: handles different contrast levels
- Validate with `validate_zoom_match()` before using

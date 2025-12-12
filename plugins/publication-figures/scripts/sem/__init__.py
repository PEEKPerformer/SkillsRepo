"""
SEM (Scanning Electron Microscopy) image processing module.

Optional component for processing and annotating SEM images
in publication-quality figure generation.

Key functions:
- load_sem_tiff: Load TIFF with optional info bar cropping (crop_info_bar=True by default)
- apply_gamma, apply_clahe: Image enhancement
- draw_scale_bar, draw_panel_label: Annotation
- InteractiveScaleBarSelector: Click to measure scale bar width
- find_zoom_region: Auto-detect where high-mag image is in low-mag
"""

from .image_processing import (
    load_sem_tiff,
    apply_gamma,
    apply_clahe,
    enhance_sem_image,
    get_image_info,
)
from .scale_bar import (
    draw_scale_bar,
    draw_panel_label,
    draw_zoom_box,
    draw_zoom_connector,
    calculate_scale_bar_pixels,
    InteractiveScaleBarSelector,
    interactive_scale_bar_measurement,
    measure_scale_bar_from_clicks,
)
from .template_matching import (
    find_zoom_region,
    validate_zoom_match,
)

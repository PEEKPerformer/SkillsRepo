"""
Scale bar and panel label utilities for SEM figures.

Provides functions for drawing scale bars and panel labels
on microscopy images.
"""

import numpy as np


def draw_scale_bar(ax, scale_text, pixel_width, img_width=1024,
                   position='bottom-right', bar_color='white',
                   outline_color='black', fontsize=14, bar_height=8):
    """
    Draw a scale bar on an SEM image.

    Args:
        ax: matplotlib Axes object
        scale_text: Scale bar label (e.g., '10 um', '1 um')
        pixel_width: Width of scale bar in pixels
        img_width: Total image width in pixels. Default: 1024
        position: Bar position ('bottom-right', 'bottom-left'). Default: 'bottom-right'
        bar_color: Color of the scale bar. Default: 'white'
        outline_color: Color of the bar outline. Default: 'black'
        fontsize: Font size for label. Default: 14
        bar_height: Height of the bar in pixels. Default: 8

    Returns:
        tuple: (bar_line, text) matplotlib objects
    """
    # Get axes limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Calculate positions (assuming origin at top-left for images)
    margin = 30  # pixels from edge

    if position == 'bottom-right':
        x2 = xlim[1] - margin
        x1 = x2 - pixel_width
        y = ylim[0] - margin  # Bottom of image (higher y value)
    else:  # bottom-left
        x1 = xlim[0] + margin
        x2 = x1 + pixel_width
        y = ylim[0] - margin

    # Draw bar with outline
    outline_width = 4
    bar_width = 2

    # Outline
    line_outline = ax.plot([x1, x2], [y, y], color=outline_color,
                           linewidth=outline_width + 2, solid_capstyle='butt')[0]

    # Main bar
    line_bar = ax.plot([x1, x2], [y, y], color=bar_color,
                       linewidth=outline_width, solid_capstyle='butt')[0]

    # Text label
    mid_x = (x1 + x2) / 2
    text = ax.text(mid_x, y - 15, scale_text,
                   ha='center', va='top',
                   fontsize=fontsize, fontweight='bold',
                   color=bar_color,
                   path_effects=[
                       # Text outline for visibility
                   ])

    # Add text outline using path_effects if available
    try:
        import matplotlib.patheffects as pe
        text.set_path_effects([
            pe.withStroke(linewidth=3, foreground=outline_color),
        ])
    except ImportError:
        pass

    return line_bar, text


def draw_panel_label(ax, label, position='top-left', fontsize=24,
                     text_color='white', bg_color='black', padding=5):
    """
    Draw a panel label (A, B, C, D) on an SEM image.

    Creates a label with background box for visibility on varying backgrounds.

    Args:
        ax: matplotlib Axes object
        label: Panel label ('A', 'B', 'C', 'D')
        position: Label position. Default: 'top-left'
        fontsize: Font size. Default: 24
        text_color: Text color. Default: 'white'
        bg_color: Background color. Default: 'black'
        padding: Padding around text. Default: 5

    Returns:
        Text object
    """
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    margin = 15

    if position == 'top-left':
        x = xlim[0] + margin
        y = ylim[1] + margin  # Top of image (lower y value for imshow)
        ha, va = 'left', 'top'
    elif position == 'top-right':
        x = xlim[1] - margin
        y = ylim[1] + margin
        ha, va = 'right', 'top'
    else:
        x = xlim[0] + margin
        y = ylim[1] + margin
        ha, va = 'left', 'top'

    text = ax.text(
        x, y, label,
        fontsize=fontsize,
        fontweight='bold',
        color=text_color,
        ha=ha, va=va,
        bbox=dict(
            facecolor=bg_color,
            edgecolor='none',
            alpha=0.8,
            pad=padding,
        )
    )

    return text


def draw_zoom_box(ax, box_coords, color='gold', linewidth=2, alpha=0.3):
    """
    Draw a box indicating a zoom region.

    Args:
        ax: matplotlib Axes object
        box_coords: (x1, y1, x2, y2) box coordinates
        color: Box color. Default: 'gold'
        linewidth: Line width. Default: 2
        alpha: Fill alpha. Default: 0.3

    Returns:
        Rectangle patch
    """
    from matplotlib.patches import Rectangle

    x1, y1, x2, y2 = box_coords
    width = x2 - x1
    height = y2 - y1

    rect = Rectangle(
        (x1, y1), width, height,
        linewidth=linewidth,
        edgecolor=color,
        facecolor=color,
        alpha=alpha,
    )
    ax.add_patch(rect)

    return rect


def draw_zoom_connector(ax_from, ax_to, box_coords, color='gold', linewidth=1.5):
    """
    Draw connector lines between a zoom box and its detailed panel.

    Args:
        ax_from: Source axes (with zoom box)
        ax_to: Target axes (detailed view)
        box_coords: (x1, y1, x2, y2) box coordinates in source axes
        color: Line color. Default: 'gold'
        linewidth: Line width. Default: 1.5

    Returns:
        list: Line objects
    """
    from matplotlib.patches import ConnectionPatch

    x1, y1, x2, y2 = box_coords

    # Get corners of target axes
    target_xlim = ax_to.get_xlim()
    target_ylim = ax_to.get_ylim()

    lines = []

    # Connect top-left of box to top-left of target
    con1 = ConnectionPatch(
        xyA=(x1, y1), xyB=(target_xlim[0], target_ylim[1]),
        coordsA='data', coordsB='data',
        axesA=ax_from, axesB=ax_to,
        color=color, linewidth=linewidth,
    )
    ax_from.figure.add_artist(con1)
    lines.append(con1)

    # Connect bottom-right of box to bottom-right of target
    con2 = ConnectionPatch(
        xyA=(x2, y2), xyB=(target_xlim[1], target_ylim[0]),
        coordsA='data', coordsB='data',
        axesA=ax_from, axesB=ax_to,
        color=color, linewidth=linewidth,
    )
    ax_from.figure.add_artist(con2)
    lines.append(con2)

    return lines


def calculate_scale_bar_pixels(physical_size, physical_unit, image_width_px,
                               image_width_physical):
    """
    Calculate scale bar width in pixels.

    Args:
        physical_size: Desired scale bar size (e.g., 10)
        physical_unit: Unit string (e.g., 'um')
        image_width_px: Image width in pixels
        image_width_physical: Image width in physical units

    Returns:
        int: Scale bar width in pixels
    """
    pixels_per_unit = image_width_px / image_width_physical
    return int(physical_size * pixels_per_unit)


class InteractiveScaleBarSelector:
    """
    Interactive tool for measuring scale bars in SEM images.

    Usage:
        selector = InteractiveScaleBarSelector(image)
        result = selector.run()
        # Click left edge, then right edge of scale bar
        print(f"Scale bar width: {result['pixel_width']} pixels")
    """

    def __init__(self, image, title="Click LEFT then RIGHT edge of scale bar"):
        """
        Initialize the interactive selector.

        Args:
            image: Image array to display
            title: Window title
        """
        self.image = image
        self.title = title
        self.points = []
        self.result = None

    def run(self):
        """
        Run the interactive selection.

        Returns:
            dict: {'pixel_width': int, 'points': [(x1, y1), (x2, y2)]}
                  or None if cancelled
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(12, 10))
        ax.imshow(self.image, cmap='gray')
        ax.set_title(self.title)

        self.points = []
        self.markers = []

        def onclick(event):
            if event.inaxes != ax:
                return

            x, y = event.xdata, event.ydata
            self.points.append((x, y))

            # Draw marker
            marker, = ax.plot(x, y, 'r+', markersize=20, markeredgewidth=3)
            self.markers.append(marker)

            if len(self.points) == 1:
                ax.set_title("Now click RIGHT edge of scale bar")
            elif len(self.points) == 2:
                # Draw line between points
                x1, y1 = self.points[0]
                x2, y2 = self.points[1]
                ax.plot([x1, x2], [y1, y2], 'r-', linewidth=2)

                pixel_width = abs(x2 - x1)
                ax.set_title(f"Scale bar width: {pixel_width:.1f} pixels (close window to confirm)")

                self.result = {
                    'pixel_width': int(pixel_width),
                    'points': self.points.copy(),
                }

            fig.canvas.draw()

        fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()

        return self.result


def interactive_scale_bar_measurement(image_path, crop_info_bar=False):
    """
    Interactively measure a scale bar in an SEM image.

    Args:
        image_path: Path to the SEM image
        crop_info_bar: Whether to crop info bar before display. Default: False

    Returns:
        dict: Measurement result with pixel_width and points
    """
    from .image_processing import load_sem_tiff

    img = load_sem_tiff(image_path, crop_info_bar=crop_info_bar)

    selector = InteractiveScaleBarSelector(img)
    result = selector.run()

    if result:
        print(f"\nScale bar measurement:")
        print(f"  Pixel width: {result['pixel_width']} px")
        print(f"  Left point:  ({result['points'][0][0]:.1f}, {result['points'][0][1]:.1f})")
        print(f"  Right point: ({result['points'][1][0]:.1f}, {result['points'][1][1]:.1f})")

    return result


def measure_scale_bar_from_clicks(image, physical_size, physical_unit='um'):
    """
    Measure scale bar and calculate pixels-per-unit calibration.

    Args:
        image: Image array or path to image
        physical_size: Physical size the scale bar represents (e.g., 10)
        physical_unit: Unit string. Default: 'um'

    Returns:
        dict: {
            'pixel_width': int,
            'physical_size': float,
            'physical_unit': str,
            'pixels_per_unit': float,
        }
    """
    if isinstance(image, str):
        from .image_processing import load_sem_tiff
        image = load_sem_tiff(image, crop_info_bar=False)

    selector = InteractiveScaleBarSelector(
        image,
        title=f"Click LEFT then RIGHT edge of {physical_size} {physical_unit} scale bar"
    )
    result = selector.run()

    if result is None:
        return None

    pixels_per_unit = result['pixel_width'] / physical_size

    calibration = {
        'pixel_width': result['pixel_width'],
        'physical_size': physical_size,
        'physical_unit': physical_unit,
        'pixels_per_unit': pixels_per_unit,
        'points': result['points'],
    }

    print(f"\nCalibration result:")
    print(f"  {result['pixel_width']} px = {physical_size} {physical_unit}")
    print(f"  Resolution: {pixels_per_unit:.2f} px/{physical_unit}")

    return calibration

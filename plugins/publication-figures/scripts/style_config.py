"""
Publication-quality figure style configuration.

Contains 6 colorblind-safe palettes and matplotlib rcParams for scientific figures.
All palettes tested for deuteranopia, protanopia, and tritanopia.
"""

import matplotlib.pyplot as plt

# =============================================================================
# COLOR PALETTES - All colorblind-safe
# =============================================================================

PALETTES = {
    # Palette 1: Ocean (Default) - Analogous blue with complementary orange
    'ocean': {
        'primary': '#0077B6',      # Deep ocean blue
        'secondary': '#00B4D8',    # Cyan accent
        'tertiary': '#90E0EF',     # Light sky
        'highlight': '#FF6B35',    # Complementary orange (emphasis)
        'neutral': '#6C757D',      # Gray (reference/literature)
    },

    # Palette 2: Earth - Warm analogous browns/greens
    'earth': {
        'primary': '#8B4513',      # Saddle brown
        'secondary': '#D2691E',    # Chocolate
        'tertiary': '#F4A460',     # Sandy brown
        'highlight': '#228B22',    # Forest green (complementary)
        'neutral': '#696969',      # Dim gray
    },

    # Palette 3: Okabe-Ito - Gold standard for accessibility
    'okabe_ito': {
        'primary': '#0072B2',      # Blue
        'secondary': '#E69F00',    # Orange
        'tertiary': '#009E73',     # Bluish green
        'highlight': '#D55E00',    # Vermillion
        'neutral': '#999999',      # Gray
        'extra': ['#CC79A7', '#F0E442', '#56B4E9'],  # Pink, Yellow, Sky blue
    },

    # Palette 4: Tol Bright - High contrast qualitative
    'tol_bright': {
        'primary': '#4477AA',      # Blue
        'secondary': '#EE6677',    # Red
        'tertiary': '#228833',     # Green
        'highlight': '#CCBB44',    # Yellow
        'neutral': '#BBBBBB',      # Gray
        'extra': ['#66CCEE', '#AA3377'],  # Cyan, Purple
    },

    # Palette 5: Vibrant - Eye-catching for presentations
    'vibrant': {
        'primary': '#0051A5',      # Vibrant blue
        'secondary': '#FF6B35',    # Bright orange
        'tertiary': '#00A878',     # Teal green
        'highlight': '#9B59B6',    # Purple
        'neutral': '#808080',      # Gray
    },

    # Palette 6: Monochrome - Single-hue gradient
    'monochrome': {
        'primary': '#1A365D',      # Dark blue
        'secondary': '#2B6CB0',    # Medium blue
        'tertiary': '#63B3ED',     # Light blue
        'highlight': '#E53E3E',    # Red (single emphasis)
        'neutral': '#718096',      # Blue-gray
    },
}

# =============================================================================
# FONT SIZES - Publication hierarchy
# =============================================================================

FONT_SIZES = {
    'panel_letter': 32,   # A, B, C, D labels
    'axis_label': 22,     # X/Y axis labels
    'tick_label': 20,     # Tick numbers
    'annotation': 18,     # Data annotations
    'legend': 20,         # Legend text
    'colorbar': 22,       # Colorbar label
    'inset': 16,          # Inset axes labels
}

# =============================================================================
# LINE WIDTHS - Heavy for visibility
# =============================================================================

LINE_WIDTHS = {
    'data': 3.5,          # Primary data lines
    'spine': 2.0,         # Axes borders
    'tick': 2.0,          # Tick marks
    'marker_edge': 2.5,   # White marker edges
    'legend_frame': 2.5,  # Legend border
    'reference': 3.0,     # Reference lines (dashed)
    'arrow': 2.5,         # Annotation arrows
}

# =============================================================================
# MARKER PROPERTIES
# =============================================================================

MARKERS = {
    'primary': 'o',       # Circles for main data
    'secondary': 's',     # Squares for comparison
    'tertiary': '^',      # Triangles for third dataset
    'size': 12,           # Base marker size
    'scatter_size': 200,  # Scatter plot marker size (s parameter)
    'edge_color': 'white', # Marker edge color
}

# =============================================================================
# FIGURE LAYOUT
# =============================================================================

LAYOUT = {
    'figsize': (18, 14),  # Default 2x2 figure size (inches)
    'dpi_screen': 100,    # Screen display DPI
    'dpi_export': 300,    # Publication export DPI
    'dpi_preview': 72,    # Preview for Claude (safe to load)
    'gridspec': {
        'hspace': 0.28,   # Vertical spacing
        'wspace': 0.35,   # Horizontal spacing
        'left': 0.08,
        'right': 0.94,
        'top': 0.96,
        'bottom': 0.06,
    },
    'panel_letter_pos': (0.03, 0.97),  # Top-left corner
}


def get_palette(name='ocean'):
    """
    Get a color palette by name.

    Args:
        name: Palette name ('ocean', 'earth', 'okabe_ito', 'tol_bright', 'vibrant', 'monochrome')

    Returns:
        dict: Palette with 'primary', 'secondary', 'tertiary', 'highlight', 'neutral' keys
    """
    name = name.lower().replace('-', '_').replace(' ', '_')
    if name not in PALETTES:
        available = ', '.join(PALETTES.keys())
        raise ValueError(f"Unknown palette '{name}'. Available: {available}")
    return PALETTES[name]


def get_colors(palette_name='ocean', n=5):
    """
    Get a list of colors from a palette for plotting multiple series.

    Args:
        palette_name: Palette name
        n: Number of colors needed

    Returns:
        list: List of hex color strings
    """
    p = get_palette(palette_name)
    colors = [p['primary'], p['secondary'], p['tertiary'], p['highlight'], p['neutral']]
    if 'extra' in p:
        colors.extend(p['extra'])
    return colors[:n]


def apply_style(palette='ocean'):
    """
    Apply publication-quality matplotlib style.

    Args:
        palette: Palette name to use for default colors

    Returns:
        dict: The selected palette for use in plotting
    """
    p = get_palette(palette)

    plt.rcParams.update({
        # Font
        'font.family': 'Arial',
        'font.size': FONT_SIZES['tick_label'],

        # Axes
        'axes.linewidth': LINE_WIDTHS['spine'],
        'axes.labelsize': FONT_SIZES['axis_label'],
        'axes.titlesize': FONT_SIZES['axis_label'],
        'axes.prop_cycle': plt.cycler(color=get_colors(palette)),

        # Ticks
        'xtick.major.size': 7,
        'xtick.major.width': LINE_WIDTHS['tick'],
        'ytick.major.size': 7,
        'ytick.major.width': LINE_WIDTHS['tick'],
        'xtick.labelsize': FONT_SIZES['tick_label'],
        'ytick.labelsize': FONT_SIZES['tick_label'],

        # Lines
        'lines.linewidth': LINE_WIDTHS['data'],
        'lines.markersize': MARKERS['size'],

        # Legend
        'legend.fontsize': FONT_SIZES['legend'],
        'legend.frameon': True,
        'legend.fancybox': False,
        'legend.shadow': False,

        # Figure
        'figure.figsize': LAYOUT['figsize'],
        'figure.dpi': LAYOUT['dpi_screen'],
        'savefig.dpi': LAYOUT['dpi_export'],
        'savefig.facecolor': 'white',
        'savefig.bbox': 'tight',

        # No grid by default
        'axes.grid': False,
    })

    return p


def suggest_palette(data_type=None, context=None):
    """
    Suggest a palette based on data type or context.

    Args:
        data_type: Type of data ('comparison', 'sequential', 'categorical', etc.)
        context: Use context ('presentation', 'publication', 'web', etc.)

    Returns:
        str: Recommended palette name
    """
    if context == 'presentation':
        return 'vibrant'
    if data_type == 'comparison':
        return 'okabe_ito'  # Max distinguishability
    if data_type == 'sequential':
        return 'monochrome'
    if data_type in ('geological', 'environmental', 'organic'):
        return 'earth'
    return 'ocean'  # Default


if __name__ == '__main__':
    # Demo: print all palettes
    print("Available Palettes:\n")
    for name, palette in PALETTES.items():
        print(f"  {name}:")
        for key, value in palette.items():
            if isinstance(value, list):
                print(f"    {key}: {', '.join(value)}")
            else:
                print(f"    {key}: {value}")
        print()

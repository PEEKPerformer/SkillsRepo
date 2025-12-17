"""
Common plotting helper functions for publication-quality figures.

Provides utilities for panel letters, legends, dual axes, insets, and more.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset


def add_panel_letter(ax, letter, fontsize=32, position=(0.03, 0.97)):
    """
    Add a panel letter (A, B, C, D) to the top-left corner of an axes.

    Args:
        ax: matplotlib Axes object
        letter: Letter to display ('A', 'B', 'C', 'D')
        fontsize: Font size. Default: 32
        position: Position in axes coordinates. Default: (0.03, 0.97)
    """
    ax.text(
        position[0], position[1], letter,
        transform=ax.transAxes,
        fontsize=fontsize,
        fontweight='bold',
        verticalalignment='top',
        horizontalalignment='left',
    )


def configure_legend(ax, loc='upper right', fontsize=20, alpha=0.95):
    """
    Configure a publication-quality legend with framed box.

    Args:
        ax: matplotlib Axes object
        loc: Legend location. Default: 'upper right'
        fontsize: Font size. Default: 20
        alpha: Background alpha. Default: 0.95

    Returns:
        Legend object
    """
    legend = ax.legend(
        frameon=True,
        loc=loc,
        fontsize=fontsize,
        fancybox=False,
        shadow=False,
    )
    legend.get_frame().set_linewidth(2.5)
    legend.get_frame().set_edgecolor('black')
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(alpha)
    return legend


def configure_spines(ax, linewidth=2.0, visible=True):
    """
    Configure axes spines for publication quality.

    Args:
        ax: matplotlib Axes object
        linewidth: Spine line width. Default: 2.0
        visible: Whether all spines should be visible. Default: True
    """
    for spine in ['top', 'right', 'bottom', 'left']:
        ax.spines[spine].set_visible(visible)
        ax.spines[spine].set_linewidth(linewidth)


def draw_rounded_bar(ax, x, height, width=0.6, bottom=0, rounding_size=None, **kwargs):
    """
    Draw a bar with visually uniform rounded corners.

    Uses FancyBboxPatch with mutation_aspect to ensure corners appear
    square regardless of different x/y data scales.

    IMPORTANT: Set axis limits (ax.set_xlim/ylim) BEFORE calling this function,
    as mutation_aspect depends on knowing the final axis ranges.

    Args:
        ax: matplotlib Axes object
        x: bar center x position
        height: bar height (not including bottom offset)
        width: bar width. Default: 0.6
        bottom: bar bottom y position. Default: 0
        rounding_size: corner radius in x data units. Default: width * 0.1
        **kwargs: passed to FancyBboxPatch (facecolor, edgecolor, linewidth, etc.)

    Returns:
        FancyBboxPatch object

    Example:
        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(0, 100)
        draw_rounded_bar(ax, 0, 75, facecolor='steelblue', edgecolor='black')
    """
    if rounding_size is None:
        rounding_size = width * 0.1

    # Get data and visual aspect ratios
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    x_range = xlim[1] - xlim[0]
    y_range = ylim[1] - ylim[0]

    # Get axes dimensions in display coords
    fig = ax.figure
    bbox = ax.get_window_extent(renderer=fig.canvas.get_renderer())

    # mutation_aspect compensates for the difference between data and visual aspect
    # This makes corner rounding appear visually square
    mutation_aspect = (y_range / x_range) * (bbox.width / bbox.height)

    box = FancyBboxPatch(
        (x - width/2, bottom), width, height,
        boxstyle=f'round,pad=0,rounding_size={rounding_size}',
        mutation_aspect=mutation_aspect,
        **kwargs
    )
    ax.add_patch(box)
    return box


def add_dual_axis(ax, ylabel, color, fontsize=22):
    """
    Create a twin y-axis with color-coordinated labels.

    Args:
        ax: Primary matplotlib Axes object
        ylabel: Label for the secondary y-axis
        color: Color for the secondary axis and its labels
        fontsize: Font size for labels. Default: 22

    Returns:
        Secondary Axes object
    """
    ax_twin = ax.twinx()
    ax_twin.set_ylabel(ylabel, fontsize=fontsize, color=color)
    ax_twin.tick_params(axis='y', labelcolor=color, width=2.0, labelsize=20)
    ax_twin.spines['right'].set_color(color)
    return ax_twin


def add_inset(ax, bounds, loc='upper right', borderpad=0.8,
              width='45%', height='40%', connect=False, connect_locs=(2, 1)):
    """
    Add an inset axes to a plot.

    Args:
        ax: Parent matplotlib Axes object
        bounds: Data bounds to highlight (xmin, xmax, ymin, ymax) or None
        loc: Inset location. Default: 'upper right'
        borderpad: Padding from axes border. Default: 0.8
        width: Inset width (percent or inches). Default: '45%'
        height: Inset height. Default: '40%'
        connect: Whether to draw connector lines. Default: False
        connect_locs: Corners to connect (loc1, loc2). Default: (2, 1)

    Returns:
        Inset Axes object
    """
    axins = inset_axes(ax, width=width, height=height, loc=loc, borderpad=borderpad)

    if connect and bounds is not None:
        # Set limits to zoomed region
        xmin, xmax, ymin, ymax = bounds
        axins.set_xlim(xmin, xmax)
        axins.set_ylim(ymin, ymax)
        # Draw connector lines
        mark_inset(ax, axins, loc1=connect_locs[0], loc2=connect_locs[1],
                   fc='none', ec='gray', linewidth=1.5)

    return axins


def add_colorbar(fig, mappable, ax, label, fontsize=22, pad=0.02, aspect=30):
    """
    Add a styled colorbar to a plot.

    Args:
        fig: matplotlib Figure object
        mappable: The ScalarMappable (scatter, imshow result)
        ax: Axes to attach colorbar to
        label: Colorbar label
        fontsize: Label font size. Default: 22
        pad: Padding from axes. Default: 0.02
        aspect: Height-to-width ratio. Default: 30

    Returns:
        Colorbar object
    """
    cbar = fig.colorbar(mappable, ax=ax, pad=pad, aspect=aspect, shrink=0.95)
    cbar.set_label(label, fontsize=fontsize, rotation=270, labelpad=30)
    cbar.ax.tick_params(width=2.0, labelsize=20)
    return cbar


def multiplicative_error_bars(y_data, y_error):
    """
    Calculate multiplicative error bars for log-scale plots.

    On log scale, additive error bars appear asymmetric. This function
    computes error bar bounds that are symmetric in log space.

    Args:
        y_data: Data values (array)
        y_error: Error values (standard deviation, array)

    Returns:
        tuple: (yerr_lower, yerr_upper) for use with errorbar yerr=[lower, upper]
    """
    y_data = np.asarray(y_data)
    y_error = np.asarray(y_error)

    # Relative standard deviation
    rel_errors = y_error / y_data

    # Multiplicative bounds (symmetric in log space)
    lower_bounds = y_data / (1 + rel_errors)
    upper_bounds = y_data * (1 + rel_errors)

    # Error bar lengths
    yerr_lower = y_data - lower_bounds
    yerr_upper = upper_bounds - y_data

    return yerr_lower, yerr_upper


def add_annotation_box(ax, text, xy, xytext, color, fontsize=18, arrow=True):
    """
    Add an annotation with a styled box and optional arrow.

    Args:
        ax: matplotlib Axes object
        text: Annotation text
        xy: Point to annotate (x, y)
        xytext: Text position offset in points
        color: Box border and arrow color
        fontsize: Font size. Default: 18
        arrow: Whether to draw arrow. Default: True

    Returns:
        Annotation object
    """
    arrowprops = None
    if arrow:
        arrowprops = dict(arrowstyle='->', color=color, lw=2.5)

    ann = ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        textcoords='offset points',
        fontsize=fontsize,
        bbox=dict(
            boxstyle='round,pad=0.4',
            facecolor='white',
            edgecolor=color,
            linewidth=2.5,
            alpha=0.95
        ),
        arrowprops=arrowprops,
    )
    return ann


def create_gridspec_figure(rows=2, cols=2, figsize=(18, 14), **gridspec_kwargs):
    """
    Create a figure with GridSpec layout for multi-panel figures.

    Args:
        rows: Number of rows. Default: 2
        cols: Number of columns. Default: 2
        figsize: Figure size in inches. Default: (18, 14)
        **gridspec_kwargs: Additional GridSpec parameters

    Returns:
        tuple: (fig, gs) - Figure and GridSpec objects
    """
    # Default GridSpec parameters
    gs_params = {
        'hspace': 0.28,
        'wspace': 0.35,
        'left': 0.08,
        'right': 0.94,
        'top': 0.96,
        'bottom': 0.06,
    }
    gs_params.update(gridspec_kwargs)

    fig = plt.figure(figsize=figsize)
    gs = GridSpec(rows, cols, figure=fig, **gs_params)

    return fig, gs


def plot_with_fit(ax, x, y, fit_func, color, label=None, show_r2=True):
    """
    Plot data with a fit line and optional R-squared annotation.

    Args:
        ax: matplotlib Axes object
        x: X data
        y: Y data
        fit_func: Function to fit (e.g., from scipy.stats.linregress)
        color: Color for data and fit
        label: Data label. Default: None
        show_r2: Whether to show R-squared. Default: True

    Returns:
        tuple: (scatter, line) plot objects
    """
    from scipy import stats

    # Scatter plot
    scatter = ax.scatter(x, y, color=color, s=200, alpha=0.9,
                         edgecolors='white', linewidth=2.5, label=label, zorder=10)

    # Fit line
    result = stats.linregress(x, y)
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = result.slope * x_fit + result.intercept
    line, = ax.plot(x_fit, y_fit, color=color, linewidth=2, linestyle='--', alpha=0.7)

    if show_r2:
        ax.text(0.95, 0.05, f'R² = {result.rvalue**2:.3f}',
                transform=ax.transAxes, fontsize=16,
                ha='right', va='bottom',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return scatter, line


def set_axis_style(ax, xlabel=None, ylabel=None, title=None,
                   fontsize_label=22, fontsize_tick=20):
    """
    Apply consistent axis styling.

    Args:
        ax: matplotlib Axes object
        xlabel: X-axis label
        ylabel: Y-axis label
        title: Axes title
        fontsize_label: Label font size. Default: 22
        fontsize_tick: Tick label font size. Default: 20
    """
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=fontsize_label)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=fontsize_label)
    if title:
        ax.set_title(title, fontsize=fontsize_label)

    ax.tick_params(labelsize=fontsize_tick, width=2.0)
    configure_spines(ax)

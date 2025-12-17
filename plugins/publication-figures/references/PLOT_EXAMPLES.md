# Plot Type Examples

Code snippets for common scientific plot types.

## Table of Contents
1. [Basic Setup](#basic-setup)
2. [Scatter Plot with Error Bars](#scatter-plot-with-error-bars)
3. [Line Plot with Markers](#line-plot-with-markers)
4. [Dual-Axis Plot](#dual-axis-plot)
5. [Log-Scale Plot](#log-scale-plot)
6. [Bar Chart](#bar-chart)
7. [Multi-Panel GridSpec](#multi-panel-gridspec)
8. [Inset Axes](#inset-axes)
9. [Time Series with FFT](#time-series-with-fft)
10. [Scatter with Colorbar](#scatter-with-colorbar)

---

## Basic Setup

```python
import matplotlib.pyplot as plt
import numpy as np
from scripts.style_config import apply_style
from scripts.export_figure import export_figure
from scripts.plot_helpers import add_panel_letter, configure_legend, configure_spines

# Apply publication style
palette = apply_style('ocean')
```

---

## Scatter Plot with Error Bars

```python
fig, ax = plt.subplots(figsize=(8, 6))

x = np.array([1, 2, 3, 4, 5])
y = np.array([2.1, 4.2, 5.8, 8.1, 10.3])
yerr = np.array([0.3, 0.4, 0.5, 0.6, 0.7])

ax.errorbar(x, y, yerr=yerr, fmt='o',
            color=palette['primary'],
            markersize=12,
            markeredgecolor='white',
            markeredgewidth=2.5,
            capsize=8, capthick=2,
            elinewidth=2,
            label='Experimental')

ax.set_xlabel('X Variable (units)')
ax.set_ylabel('Y Variable (units)')
configure_legend(ax)
configure_spines(ax)
add_panel_letter(ax, 'A')

export_figure(fig, 'output/scatter_example')
```

### Multiplicative Error Bars (Log Scale)

```python
from scripts.plot_helpers import multiplicative_error_bars

# For log-scale, use multiplicative errors
yerr_lower, yerr_upper = multiplicative_error_bars(y, yerr)
ax.errorbar(x, y, yerr=[yerr_lower, yerr_upper], fmt='o', ...)
ax.set_yscale('log')
```

---

## Line Plot with Markers

```python
fig, ax = plt.subplots(figsize=(8, 6))

x = np.linspace(0, 10, 50)
y1 = np.sin(x)
y2 = np.cos(x)

ax.plot(x, y1, 'o-', color=palette['primary'],
        markersize=8, markeredgecolor='white', markeredgewidth=2,
        linewidth=3.5, label='Signal A')

ax.plot(x, y2, 's--', color=palette['secondary'],
        markersize=8, markeredgecolor='white', markeredgewidth=2,
        linewidth=3.5, label='Signal B')

ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
configure_legend(ax)
configure_spines(ax)

export_figure(fig, 'output/line_example')
```

---

## Dual-Axis Plot

```python
from scripts.plot_helpers import add_dual_axis

fig, ax = plt.subplots(figsize=(10, 6))

x = np.linspace(0, 100, 100)
temp = 20 + 0.5 * x + np.random.normal(0, 2, 100)
rate = np.gradient(temp)

# Primary axis (left) - Temperature
ax.plot(x, temp, color=palette['primary'], linewidth=3.5, label='Temperature')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Temperature (°C)', color=palette['primary'])
ax.tick_params(axis='y', labelcolor=palette['primary'])

# Secondary axis (right) - Rate
ax2 = add_dual_axis(ax, 'Heating Rate (°C/s)', palette['secondary'])
ax2.plot(x, rate, color=palette['secondary'], linewidth=3.5, alpha=0.8)

configure_spines(ax)
export_figure(fig, 'output/dual_axis_example')
```

---

## Log-Scale Plot

```python
fig, ax = plt.subplots(figsize=(8, 6))

x = np.logspace(-2, 2, 50)
y = x ** 2

ax.scatter(x, y, s=100, color=palette['primary'],
           edgecolors='white', linewidth=2, label='Data')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Current Density (A/cm²)')
ax.set_ylabel('Power (W)')

configure_legend(ax)
configure_spines(ax)

export_figure(fig, 'output/log_scale_example')
```

---

## Bar Chart

Uses `draw_rounded_bar()` for a cleaner, modern look with uniform rounded corners.

```python
from scripts.plot_helpers import draw_rounded_bar

fig, ax = plt.subplots(figsize=(8, 6))

categories = ['Control', 'Treatment A', 'Treatment B']
values = [45, 72, 63]
errors = [5, 8, 6]
colors = [palette['neutral'], palette['primary'], palette['secondary']]

# Floating bars: extend y-axis slightly negative so bars float above x-axis
# but y=0 is correctly at bar bottoms
float_gap = 2
bar_positions = range(len(categories))

# MUST set axis limits BEFORE drawing rounded bars
ax.set_xlim(-0.5, len(categories) - 0.5)
ax.set_ylim(-float_gap, 90)

# Draw rounded bars
for i, (val, err, color) in enumerate(zip(values, errors, colors)):
    draw_rounded_bar(ax, i, val, width=0.6, bottom=0,
                     facecolor=color, edgecolor='black', linewidth=1.5)
    ax.errorbar(i, val, yerr=err, fmt='none', color='black', capsize=6, capthick=1.5)

ax.set_xticks(bar_positions)
ax.set_xticklabels(categories)
ax.set_ylabel('Response (units)')
ax.set_yticks([0, 20, 40, 60, 80])  # Don't show negative region
configure_spines(ax)

export_figure(fig, 'output/bar_chart_example')
```

---

## Multi-Panel GridSpec

```python
from scripts.plot_helpers import create_gridspec_figure

fig, gs = create_gridspec_figure(rows=2, cols=2)

# Panel A
ax_a = fig.add_subplot(gs[0, 0])
ax_a.plot([1, 2, 3], [1, 4, 9], 'o-', color=palette['primary'])
add_panel_letter(ax_a, 'A')
configure_spines(ax_a)

# Panel B
ax_b = fig.add_subplot(gs[0, 1])
ax_b.bar([1, 2, 3], [3, 5, 2], color=palette['secondary'])
add_panel_letter(ax_b, 'B')
configure_spines(ax_b)

# Panel C
ax_c = fig.add_subplot(gs[1, 0])
ax_c.scatter([1, 2, 3], [2, 3, 1], s=200, color=palette['tertiary'])
add_panel_letter(ax_c, 'C')
configure_spines(ax_c)

# Panel D
ax_d = fig.add_subplot(gs[1, 1])
ax_d.hist(np.random.randn(100), bins=20, color=palette['primary'], edgecolor='white')
add_panel_letter(ax_d, 'D')
configure_spines(ax_d)

export_figure(fig, 'output/multipanel_example')
```

---

## Inset Axes

```python
from scripts.plot_helpers import add_inset

fig, ax = plt.subplots(figsize=(10, 8))

# Main data
x = np.linspace(0, 100, 1000)
y = np.sin(x / 5) + np.random.normal(0, 0.1, 1000)

ax.plot(x, y, color=palette['primary'], linewidth=2, alpha=0.7)
ax.set_xlabel('X')
ax.set_ylabel('Y')
configure_spines(ax)

# Zoom inset
axins = add_inset(ax, bounds=(40, 60, -0.5, 0.5),
                  loc='upper right', width='40%', height='35%',
                  connect=True)

# Plot same data in inset
mask = (x >= 40) & (x <= 60)
axins.plot(x[mask], y[mask], color=palette['primary'], linewidth=2)
axins.set_xlim(40, 60)
axins.set_ylim(-0.5, 0.5)
axins.tick_params(labelsize=14)

export_figure(fig, 'output/inset_example')
```

---

## Time Series with FFT

```python
from scripts.data_helpers import compute_fft, savgol_smooth, find_signal_peaks

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Generate sample signal
dt = 0.01
t = np.arange(0, 10, dt)
signal = np.sin(2 * np.pi * 2 * t) + 0.5 * np.sin(2 * np.pi * 5 * t)
signal += np.random.normal(0, 0.3, len(t))

# Time domain
smoothed = savgol_smooth(signal, window=51)
ax1.plot(t, signal, color=palette['neutral'], alpha=0.5, label='Raw')
ax1.plot(t, smoothed, color=palette['primary'], linewidth=3, label='Smoothed')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.legend()
add_panel_letter(ax1, 'A')
configure_spines(ax1)

# Frequency domain
freq, power = compute_fft(signal, dt)
ax2.plot(freq, power, color=palette['secondary'], linewidth=3)
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Power')
ax2.set_xlim(0, 10)
add_panel_letter(ax2, 'B')
configure_spines(ax2)

export_figure(fig, 'output/timeseries_fft_example')
```

---

## Scatter with Colorbar

```python
from scripts.plot_helpers import add_colorbar

fig, ax = plt.subplots(figsize=(10, 8))

x = np.random.randn(100)
y = np.random.randn(100)
c = np.random.rand(100) * 100  # Color values

scatter = ax.scatter(x, y, c=c, s=200, cmap='viridis',
                     edgecolors='white', linewidth=2)

ax.set_xlabel('X Variable')
ax.set_ylabel('Y Variable')
configure_spines(ax)

add_colorbar(fig, scatter, ax, 'Parameter Value')

export_figure(fig, 'output/scatter_colorbar_example')
```

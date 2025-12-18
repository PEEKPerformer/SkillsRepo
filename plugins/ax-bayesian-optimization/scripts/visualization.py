#!/usr/bin/env python3
"""
Optimization visualization for Ax experiments.

Generates publication-quality plots for Bayesian optimization progress.
Uses colorblind-safe palettes and exports both high-res and preview images.

Usage:
    python visualization.py progress --experiment experiments/my_exp/ --output plots/
    python visualization.py pareto --experiment experiments/my_exp/ --output plots/
    python visualization.py sensitivity --experiment experiments/my_exp/ --output plots/
    python visualization.py contour --experiment experiments/my_exp/ --param1 x --param2 y --output plots/
"""

import json
import argparse
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import numpy as np
except ImportError:
    print("ERROR: matplotlib or numpy not installed. Run: pip install matplotlib numpy")
    sys.exit(1)

try:
    from ax.api.client import Client
except ImportError:
    print("ERROR: ax-platform not installed. Run: pip install ax-platform")
    sys.exit(1)


# Colorblind-safe palette (Okabe-Ito)
COLORS = {
    'primary': '#0072B2',      # Blue
    'secondary': '#E69F00',    # Orange
    'tertiary': '#009E73',     # Bluish green
    'highlight': '#D55E00',    # Vermillion
    'neutral': '#999999',      # Gray
}

# Publication-quality style settings
STYLE = {
    'font.family': 'Arial',
    'font.size': 14,
    'axes.linewidth': 1.5,
    'axes.labelsize': 16,
    'axes.titlesize': 18,
    'xtick.major.size': 6,
    'xtick.major.width': 1.5,
    'ytick.major.size': 6,
    'ytick.major.width': 1.5,
    'lines.linewidth': 2.5,
    'lines.markersize': 10,
    'legend.fontsize': 12,
    'legend.frameon': True,
    'figure.figsize': (10, 7),
    'savefig.dpi': 300,
    'savefig.facecolor': 'white',
    'savefig.bbox': 'tight',
}


def apply_style():
    """Apply publication-quality matplotlib style."""
    plt.rcParams.update(STYLE)


def save_figure(fig, output_path: str, name: str):
    """Save figure in multiple formats with preview."""
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    # High-res outputs
    fig.savefig(output_dir / f"{name}.png", dpi=300)
    fig.savefig(output_dir / f"{name}.pdf")

    # Preview for Claude (72 DPI)
    fig.savefig(output_dir / f"{name}_preview.png", dpi=72)

    print(f"Saved: {name}.png, {name}.pdf, {name}_preview.png")


def plot_progress(experiment_path: str, output_path: str) -> None:
    """
    Plot optimization progress over trials.

    Shows objective value vs trial number with best-so-far line.
    Automatically detects maximization vs minimization from objective string.
    """
    apply_style()

    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"
    config_file = exp_dir / "config.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))

    # Get trial data
    summary_df = client.summarize()

    if summary_df.empty:
        print("ERROR: No trials to plot yet")
        sys.exit(1)

    # Check if minimization from config
    is_minimization = False
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
        objective_str = config.get("objective", "")
        is_minimization = objective_str.startswith("-")

    # Extract trial indices and objective values
    trial_indices = summary_df.index.tolist()

    # Find the objective column (usually the first metric column)
    metric_cols = [col for col in summary_df.columns if col not in ['arm_name', 'trial_status']]
    if not metric_cols:
        print("ERROR: No metric data found")
        sys.exit(1)

    objective_col = metric_cols[0]
    objective_values = summary_df[objective_col].tolist()

    # Calculate best-so-far (cumulative min for minimization, max for maximization)
    best_so_far = []
    if is_minimization:
        current_best = float('inf')
        for val in objective_values:
            if val < current_best:
                current_best = val
            best_so_far.append(current_best)
    else:
        current_best = float('-inf')
        for val in objective_values:
            if val > current_best:
                current_best = val
            best_so_far.append(current_best)

    # Create plot
    fig, ax = plt.subplots()

    ax.scatter(trial_indices, objective_values, c=COLORS['primary'],
               s=100, label='Trial result', zorder=3, edgecolors='white', linewidth=1.5)
    ax.plot(trial_indices, best_so_far, c=COLORS['highlight'],
            linewidth=2.5, linestyle='--', label='Best so far', zorder=2)

    ax.set_xlabel('Trial')
    ax.set_ylabel(objective_col.replace('_', ' ').title())
    ax.set_title('Optimization Progress')

    # Style legend
    legend = ax.legend(loc='lower right', frameon=True, fancybox=False)
    legend.get_frame().set_linewidth(1.5)
    legend.get_frame().set_edgecolor('black')

    # Ensure integer x-axis for trial numbers
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    save_figure(fig, output_path, 'progress')
    plt.close(fig)


def plot_pareto(experiment_path: str, output_path: str) -> None:
    """
    Plot Pareto frontier for multi-objective optimization.

    Shows trade-off between objectives.
    """
    apply_style()

    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))

    summary_df = client.summarize()

    if summary_df.empty:
        print("ERROR: No trials to plot yet")
        sys.exit(1)

    # Find metric columns
    metric_cols = [col for col in summary_df.columns if col not in ['arm_name', 'trial_status']]

    if len(metric_cols) < 2:
        print("ERROR: Pareto plot requires at least 2 objectives")
        sys.exit(1)

    obj1, obj2 = metric_cols[0], metric_cols[1]
    x_vals = summary_df[obj1].tolist()
    y_vals = summary_df[obj2].tolist()

    # Create plot
    fig, ax = plt.subplots()

    ax.scatter(x_vals, y_vals, c=COLORS['primary'], s=100,
               edgecolors='white', linewidth=1.5, zorder=3)

    ax.set_xlabel(obj1.replace('_', ' ').title())
    ax.set_ylabel(obj2.replace('_', ' ').title())
    ax.set_title('Pareto Frontier (Multi-Objective)')

    # Try to get and highlight Pareto frontier
    try:
        frontier = client.get_pareto_frontier()
        if frontier:
            frontier_x = [metrics[obj1][0] for _, metrics, _, _ in frontier]
            frontier_y = [metrics[obj2][0] for _, metrics, _, _ in frontier]
            ax.scatter(frontier_x, frontier_y, c=COLORS['highlight'], s=150,
                       marker='*', label='Pareto optimal', zorder=4, edgecolors='white', linewidth=1.5)
            legend = ax.legend(loc='best', frameon=True, fancybox=False)
            legend.get_frame().set_linewidth(1.5)
    except Exception:
        pass  # May not have enough data for Pareto yet

    save_figure(fig, output_path, 'pareto')
    plt.close(fig)


def plot_sensitivity(experiment_path: str, output_path: str) -> None:
    """
    Plot parameter sensitivity analysis.

    Shows which parameters have the largest effect on the objective.
    Uses simple correlation-based sensitivity for quick visualization.
    """
    apply_style()

    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))

    summary_df = client.summarize()

    if summary_df.empty or len(summary_df) < 3:
        print("ERROR: Need at least 3 trials for sensitivity analysis")
        sys.exit(1)

    # Get experiment to access parameter names
    experiment = client._experiment

    # Extract parameter values from arms
    param_names = list(experiment.search_space.parameters.keys())

    # Build parameter data matrix
    param_data = {name: [] for name in param_names}
    for _, row in summary_df.iterrows():
        arm_name = row.get('arm_name', '')
        # Get arm from experiment
        for trial in experiment.trials.values():
            if hasattr(trial, 'arm') and trial.arm and trial.arm.name == arm_name:
                for pname in param_names:
                    val = trial.arm.parameters.get(pname)
                    # Convert categorical to numeric
                    if isinstance(val, str):
                        param_data[pname].append(hash(val) % 100)  # Simple encoding
                    else:
                        param_data[pname].append(val)
                break

    # Find objective column
    metric_cols = [col for col in summary_df.columns if col not in ['arm_name', 'trial_status']]
    if not metric_cols:
        print("ERROR: No metric data found")
        sys.exit(1)

    objective_col = metric_cols[0]
    obj_values = summary_df[objective_col].tolist()

    # Calculate correlations
    sensitivities = {}
    for pname, pvals in param_data.items():
        if len(pvals) == len(obj_values) and len(set(pvals)) > 1:
            correlation = np.corrcoef(pvals, obj_values)[0, 1]
            sensitivities[pname] = abs(correlation) if not np.isnan(correlation) else 0
        else:
            sensitivities[pname] = 0

    # Sort by sensitivity
    sorted_params = sorted(sensitivities.items(), key=lambda x: x[1], reverse=True)
    names = [p[0] for p in sorted_params]
    values = [p[1] for p in sorted_params]

    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, max(6, len(names) * 0.5)))

    y_pos = np.arange(len(names))
    bars = ax.barh(y_pos, values, color=COLORS['primary'], edgecolor='white', linewidth=1.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([n.replace('_', ' ').title() for n in names])
    ax.set_xlabel('Sensitivity (|correlation|)')
    ax.set_title('Parameter Sensitivity Analysis')
    ax.set_xlim(0, 1)

    # Invert y-axis so most important is at top
    ax.invert_yaxis()

    save_figure(fig, output_path, 'sensitivity')
    plt.close(fig)


def plot_contour(experiment_path: str, param1: str, param2: str, output_path: str) -> None:
    """
    Plot 2D contour showing how two parameters affect the objective.

    Uses simple interpolation of observed data points.
    """
    apply_style()

    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))

    summary_df = client.summarize()

    if summary_df.empty or len(summary_df) < 4:
        print("ERROR: Need at least 4 trials for contour plot")
        sys.exit(1)

    experiment = client._experiment

    # Extract parameter values
    p1_vals, p2_vals = [], []
    for _, row in summary_df.iterrows():
        arm_name = row.get('arm_name', '')
        for trial in experiment.trials.values():
            if hasattr(trial, 'arm') and trial.arm and trial.arm.name == arm_name:
                p1_val = trial.arm.parameters.get(param1)
                p2_val = trial.arm.parameters.get(param2)
                if p1_val is not None and p2_val is not None:
                    p1_vals.append(float(p1_val) if not isinstance(p1_val, str) else 0)
                    p2_vals.append(float(p2_val) if not isinstance(p2_val, str) else 0)
                break

    # Find objective
    metric_cols = [col for col in summary_df.columns if col not in ['arm_name', 'trial_status']]
    if not metric_cols:
        print("ERROR: No metric data found")
        sys.exit(1)

    objective_col = metric_cols[0]
    obj_values = summary_df[objective_col].tolist()[:len(p1_vals)]

    if len(p1_vals) < 4:
        print("ERROR: Not enough numeric data points for contour")
        sys.exit(1)

    # Create scatter plot with color-coded points
    fig, ax = plt.subplots()

    scatter = ax.scatter(p1_vals, p2_vals, c=obj_values, s=150,
                         cmap='viridis', edgecolors='white', linewidth=2, zorder=3)

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax, pad=0.02)
    cbar.set_label(objective_col.replace('_', ' ').title(), fontsize=14)

    ax.set_xlabel(param1.replace('_', ' ').title())
    ax.set_ylabel(param2.replace('_', ' ').title())
    ax.set_title(f'{objective_col.replace("_", " ").title()} vs Parameters')

    save_figure(fig, output_path, f'contour_{param1}_{param2}')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Optimization visualization for Ax experiments")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # progress command
    progress_parser = subparsers.add_parser("progress", help="Plot optimization progress")
    progress_parser.add_argument("--experiment", required=True, help="Path to experiment directory")
    progress_parser.add_argument("--output", required=True, help="Output directory for plots")

    # pareto command
    pareto_parser = subparsers.add_parser("pareto", help="Plot Pareto frontier")
    pareto_parser.add_argument("--experiment", required=True, help="Path to experiment directory")
    pareto_parser.add_argument("--output", required=True, help="Output directory for plots")

    # sensitivity command
    sens_parser = subparsers.add_parser("sensitivity", help="Plot parameter sensitivity")
    sens_parser.add_argument("--experiment", required=True, help="Path to experiment directory")
    sens_parser.add_argument("--output", required=True, help="Output directory for plots")

    # contour command
    contour_parser = subparsers.add_parser("contour", help="Plot 2D contour")
    contour_parser.add_argument("--experiment", required=True, help="Path to experiment directory")
    contour_parser.add_argument("--param1", required=True, help="First parameter name")
    contour_parser.add_argument("--param2", required=True, help="Second parameter name")
    contour_parser.add_argument("--output", required=True, help="Output directory for plots")

    args = parser.parse_args()

    if args.command == "progress":
        plot_progress(args.experiment, args.output)
    elif args.command == "pareto":
        plot_pareto(args.experiment, args.output)
    elif args.command == "sensitivity":
        plot_sensitivity(args.experiment, args.output)
    elif args.command == "contour":
        plot_contour(args.experiment, args.param1, args.param2, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

"""
Multi-format figure export with mandatory preview generation.

CRITICAL: Always generates a low-DPI preview that Claude should read
instead of the high-resolution files (which may crash the session).
"""

import os
from pathlib import Path


def export_figure(fig, base_path, formats=None, dpi_export=300, dpi_preview=72):
    """
    Export figure in multiple formats with mandatory low-DPI preview.

    CRITICAL: Claude should ONLY read the *_preview.png file.
    High-resolution files (PDF, PNG, SVG) may crash the session.

    Args:
        fig: matplotlib Figure object
        base_path: Base path without extension (e.g., 'output/my_figure')
        formats: List of formats to export. Default: ['pdf', 'png', 'svg']
        dpi_export: DPI for high-resolution export. Default: 300
        dpi_preview: DPI for Claude-safe preview. Default: 72

    Returns:
        dict: Paths to all exported files
    """
    if formats is None:
        formats = ['pdf', 'png', 'svg']

    base = Path(base_path)
    output_dir = base.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        'high_res': [],
        'preview': None,
    }

    # Export high-resolution versions
    for fmt in formats:
        path = base.with_suffix(f'.{fmt}')
        if fmt == 'svg':
            # SVG is vector, DPI doesn't apply the same way
            fig.savefig(path, format='svg', bbox_inches='tight', facecolor='white')
        else:
            fig.savefig(path, dpi=dpi_export, bbox_inches='tight', facecolor='white')
        outputs['high_res'].append(str(path))
        print(f"Saved: {path}")

    # MANDATORY: Generate low-DPI preview for Claude
    preview_path = base.parent / f"{base.stem}_preview.png"
    fig.savefig(preview_path, dpi=dpi_preview, bbox_inches='tight', facecolor='white')
    outputs['preview'] = str(preview_path)
    print(f"Saved preview ({dpi_preview} DPI): {preview_path}")

    # CRITICAL WARNING
    print("\n" + "=" * 60)
    print(">>> CLAUDE: Read ONLY the *_preview.png file <<<")
    print(">>> DO NOT read high-res PNG/PDF/SVG (may crash session) <<<")
    print("=" * 60 + "\n")

    return outputs


def get_output_paths(base_name, output_dir='output'):
    """
    Generate standardized output paths for a figure.

    Args:
        base_name: Base name for the figure (e.g., 'conductivity_figure')
        output_dir: Output directory. Default: 'output'

    Returns:
        dict: Dictionary with 'pdf', 'png', 'svg', 'preview' paths
    """
    output_dir = Path(output_dir)
    return {
        'pdf': str(output_dir / f"{base_name}.pdf"),
        'png': str(output_dir / f"{base_name}.png"),
        'svg': str(output_dir / f"{base_name}.svg"),
        'preview': str(output_dir / f"{base_name}_preview.png"),
        'base': str(output_dir / base_name),
    }


def quick_export(fig, name, output_dir='output'):
    """
    Quick export with default settings.

    Args:
        fig: matplotlib Figure object
        name: Figure name (no extension)
        output_dir: Output directory. Default: 'output'

    Returns:
        str: Path to the preview file (safe for Claude to read)
    """
    paths = get_output_paths(name, output_dir)
    outputs = export_figure(fig, paths['base'])
    return outputs['preview']


if __name__ == '__main__':
    # Demo usage
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([1, 2, 3], [1, 4, 9], 'o-')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    outputs = export_figure(fig, 'demo/test_figure')
    print("\nExported files:")
    for key, value in outputs.items():
        print(f"  {key}: {value}")

    plt.close()

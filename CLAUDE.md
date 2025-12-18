# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Claude Code skills/plugins marketplace repository. It contains custom skills that extend Claude's capabilities through the plugin system.

## Repository Structure

```
.claude-plugin/marketplace.json  # Registry of all plugins
plugins/
  <skill-name>/
    plugin.json          # Skill metadata
    commands/            # Slash command definitions (.md files)
    references/          # Reference documentation for the skill
    scripts/             # Python modules (if applicable)
```

## Plugin Development

### Creating a New Plugin

1. Create a directory under `plugins/<skill-name>/`
2. Add `plugin.json` with metadata:
```json
{
  "name": "skill-name",
  "description": "What the skill does",
  "version": "1.0.0",
  "author": { "name": "Author Name" },
  "commands": "./commands/"
}
```
3. Register in `.claude-plugin/marketplace.json` under the `plugins` array
4. Add command files in `commands/` as markdown with YAML frontmatter

### Command File Format

Commands are markdown files with a `description` in YAML frontmatter:
```markdown
---
description: Brief description shown in command list
---

# Command Title

Instructions for Claude when this command is invoked...
```

## Publication-Figures Skill

The main skill generates publication-quality scientific figures. Key modules:

- `scripts/style_config.py` - 6 colorblind-safe palettes, font/line constants, `apply_style()`
- `scripts/export_figure.py` - Multi-format export with auto-preview generation
- `scripts/plot_helpers.py` - Panel letters, legends, common plot utilities
- `scripts/data_helpers.py` - CSV parsing and data manipulation
- `scripts/sem/` - SEM image processing (scale bars, CLAHE, template matching)

### Style Rules Summary

- Fonts: Arial, 20pt minimum, 32pt bold panel letters
- Lines: 2pt minimum, 3.5pt for data
- Markers: White edges (2.5pt), circles for primary data
- All spines visible, no grids
- Export: 300 DPI publication, 72 DPI preview

### Figure Workflow

```python
from scripts.style_config import apply_style
from scripts.export_figure import export_figure

palette = apply_style('okabe_ito')  # Returns palette dict
fig, ax = plt.subplots()
# ... create plot ...
export_figure(fig, 'output/figure_name')  # Creates .pdf, .png, .svg, *_preview.png
```

**Critical**: Only read `*_preview.png` files for verification - high-res outputs may crash sessions.

## Git Conventions

- Generated figures go in `output/` or `outputs/` directories (gitignored)
- Keep `*.tif/*.tiff` files out of git (too large)

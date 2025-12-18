---
description: Start or continue a Bayesian optimization experiment for materials science. Use when optimizing material properties, formulations, process parameters, or any black-box optimization. Supports composites, 3D printing, alloys, and more.
---

# Bayesian Optimization for Materials Science

Guide the researcher through Bayesian optimization using Meta Ax. Claude handles all code; researcher just reports measurements.

## Workflow

### If Starting New Experiment

1. Ask: "What are you trying to optimize?" (e.g., tensile strength, hardness)
2. Ask: "What parameters can you control? What are their ranges?"
3. Ask: "Any constraints on outcomes?" (e.g., cost <= 100, weight <= 10)
4. Ask: "Do you have any existing experimental data?"

Create config.json and initialize:
```bash
python scripts/experiment_manager.py create --config config.json --output experiments/{name}/
```

### If Continuing Experiment

1. Load existing experiment from `experiments/{name}/`
2. Check current state with `summary` command
3. Continue optimization loop

### Optimization Loop

1. Get suggested trials:
```bash
python scripts/experiment_manager.py next --experiment experiments/{name}/ --n 3
```

2. **CRITICAL: Validate feasibility with researcher**
   - "Can you actually set temperature to X°C?"
   - "Is material type Y available in your lab?"
   - "Does this combination make physical sense?"

3. Researcher runs experiments and reports results (simple or with SEM):
```bash
python scripts/experiment_manager.py complete --experiment experiments/{name}/ --trial N --results '{"metric": value}'
python scripts/experiment_manager.py complete --experiment experiments/{name}/ --trial N --results '{"metric": [value, sem]}'
```

   If trial fails (equipment error): `failed --experiment X --trial N --reason "..."`
   If infeasible (impossible combo): `abandoned --experiment X --trial N --reason "..."`

4. Generate visualization:
```bash
python scripts/visualization.py progress --experiment experiments/{name}/ --output experiments/{name}/plots/
```

5. Commit to git:
```bash
git add experiments/{name}/
git commit -m "Trials X-Y: best={value}"
```

6. Repeat until convergence or budget exhausted

### Analysis

```bash
python scripts/experiment_manager.py best --experiment experiments/{name}/
python scripts/experiment_manager.py pareto --experiment experiments/{name}/  # multi-objective
python scripts/experiment_manager.py predict --experiment experiments/{name}/ --parameters '{"temp": 120}'
python scripts/visualization.py sensitivity --experiment experiments/{name}/ --output experiments/{name}/plots/
```

## Reference Files

- `references/PARAMETERS.md` - Parameter types, constraints, multi-objective
- `references/WORKFLOW.md` - Detailed workflow steps
- `references/EXAMPLES.md` - Composite, 3D printing, alloy examples

## Requirements

```bash
pip install ax-platform matplotlib numpy
```

## Key Principles

1. **Validate before executing** - Always confirm feasibility with researcher
2. **Document everything** - Use experiment_log.md for notes
3. **Commit often** - Track progress in git
4. **Read previews only** - Only read `*_preview.png` files (72 DPI)

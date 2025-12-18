---
name: ax-bayesian-optimization
description: Bayesian optimization partner for materials science experiments using Meta Ax. Use when researchers want to optimize material properties, formulations, or process parameters. Supports (1) Composite formulation optimization, (2) 3D printing parameter tuning, (3) Alloy composition design, (4) Any black-box optimization with continuous/categorical parameters. Handles the full workflow - setup experiments, suggest trials, validate feasibility with researcher, track results in git, generate visualizations.
---

# Ax Bayesian Optimization

Conversational Bayesian optimization for materials science. Claude handles all code; researcher just reports measurements.

## Quick Start

### 1. Setup Experiment

Create `config.json`:
```json
{
    "name": "my_optimization",
    "parameters": [
        {"name": "temp", "type": "float", "bounds": [80, 180]},
        {"name": "time", "type": "float", "bounds": [1, 8]},
        {"name": "conc", "type": "float", "bounds": [0.01, 100], "scaling": "log"},
        {"name": "type", "type": "choice", "values": ["A", "B", "C"]}
    ],
    "parameter_constraints": ["temp + time <= 185"],
    "objective": "strength",
    "outcome_constraints": ["cost <= 100"],
    "generation_strategy": {"method": "fast", "random_seed": 42}
}
```

Initialize:
```bash
python scripts/experiment_manager.py create --config config.json --output experiments/my_exp/
```

### 2. Optimization Loop

Get next trials:
```bash
python scripts/experiment_manager.py next --experiment experiments/my_exp/ --n 3
```

**CRITICAL: Validate with researcher before they run experiments.**
- "Can you set temp=125.5°C?"
- "Is type B available?"

Report results (simple or with SEM for uncertainty):
```bash
python scripts/experiment_manager.py complete --experiment experiments/my_exp/ --trial 0 --results '{"strength": 45.2, "cost": 78}'
python scripts/experiment_manager.py complete --experiment experiments/my_exp/ --trial 0 --results '{"strength": [45.2, 1.3], "cost": [78, 2]}'
```

### 3. Analyze

```bash
python scripts/experiment_manager.py best --experiment experiments/my_exp/
python scripts/visualization.py progress --experiment experiments/my_exp/ --output experiments/my_exp/plots/
```

## Conversation Flow

### Setup Phase
1. Ask: "What are you optimizing?"
2. Ask: "What parameters can you control? What are their ranges?"
3. Ask: "Any constraints on outcomes?"
4. Ask: "Do you have existing data?"
5. Create config, initialize experiment

### Each Iteration
1. Get suggested trials from Ax
2. **Validate feasibility** with researcher
3. Researcher runs experiments
4. Researcher reports results
5. Update model, generate plots, commit to git

### Completion
1. Get best parameters
2. Generate final visualizations
3. Summarize in experiment_log.md
4. Commit to git

## Scripts

### experiment_manager.py

| Command | Description |
|---------|-------------|
| `create --config X --output Y` | Create new experiment |
| `attach --experiment X --data Y` | Attach existing data |
| `baseline --experiment X --parameters '{...}'` | Set baseline for relative constraints |
| `next --experiment X --n N` | Get N suggested trials |
| `complete --experiment X --trial N --results '{...}'` | Report trial results (supports SEM) |
| `failed --experiment X --trial N --reason "..."` | Mark trial as failed (equipment error) |
| `abandoned --experiment X --trial N --reason "..."` | Mark trial as abandoned (infeasible) |
| `best --experiment X` | Get best parameters |
| `pareto --experiment X` | Get Pareto frontier (multi-objective) |
| `predict --experiment X --parameters '{...}'` | Predict outcome without running |
| `summary --experiment X` | Show experiment summary |

### visualization.py

| Command | Description |
|---------|-------------|
| `progress --experiment X --output Y` | Plot optimization progress |
| `pareto --experiment X --output Y` | Plot Pareto frontier (multi-objective) |
| `sensitivity --experiment X --output Y` | Plot parameter sensitivity |
| `contour --experiment X --param1 A --param2 B --output Y` | Plot 2D parameter space |

All plots generate `*_preview.png` at 72 DPI (safe for Claude to read).

## Project Structure

```
experiments/{name}/
├── experiment.json      # Ax state (for persistence)
├── config.json          # Original config
├── experiment_log.md    # Human-readable log
└── plots/
    ├── progress.png
    └── progress_preview.png
```

## Git Integration

After each batch of trials:
```bash
git add experiments/{name}/
git commit -m "Trials N-M: best={value}"
```

## References

- [PARAMETERS.md](references/PARAMETERS.md) - Parameter types, constraints, multi-objective
- [WORKFLOW.md](references/WORKFLOW.md) - Detailed workflow steps
- [EXAMPLES.md](references/EXAMPLES.md) - Composite, 3D printing, alloy examples

## Handling Measurement Noise

Lab measurements have variability. Ax handles this natively via its Gaussian Process model.

**Report SEM when available** (format: `[mean, sem]`):
```bash
python scripts/experiment_manager.py complete --experiment exp/ --trial 0 \
    --results '{"strength": [45.2, 1.3], "cost": [78, 2.5]}'
```

For best results:
1. **Report SEM if known**: Calculated as `std_dev / sqrt(n_replicates)`
2. **Run replicates**: Same parameters, multiple measurements help Ax estimate noise
3. **Don't discard outliers prematurely**: Ax learns from variability

## Stopping Criteria

Stop optimization when any of:
- **Convergence**: Last 5-10 trials show <5% improvement in objective
- **Budget**: Reached max experiments (typically 20-50 for 3-5 parameters)
- **Satisfaction**: Found parameters meeting all requirements
- **Physical limits**: Hit bounds of feasible parameter space

Rule of thumb: Budget = 10 × number_of_parameters for initial exploration.

## Handling Failed Trials

**Equipment failure, contaminated sample:**
```bash
python scripts/experiment_manager.py failed --experiment exp/ --trial 0 --reason "Equipment malfunction"
```

**Physically impossible parameter combination:**
```bash
python scripts/experiment_manager.py abandoned --experiment exp/ --trial 0 --reason "Mixture too viscous to process"
```

Ax learns from both. For systematic failures, consider tightening the search space.

## Requirements

```bash
pip install ax-platform matplotlib numpy
```

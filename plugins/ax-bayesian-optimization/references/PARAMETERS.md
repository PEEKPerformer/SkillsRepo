# Parameter Guide

## Parameter Types

### Range Parameters (continuous/integer)

For numerical values with upper and lower bounds.

```json
{
    "name": "temperature",
    "type": "float",
    "bounds": [80, 180]
}
```

```json
{
    "name": "num_layers",
    "type": "int",
    "bounds": [1, 10]
}
```

#### Log-Scale Parameters

For parameters spanning orders of magnitude (e.g., concentration, learning rate):

```json
{
    "name": "concentration",
    "type": "float",
    "bounds": [0.001, 1000],
    "scaling": "log"
}
```

#### Step Size (Discrete Steps)

For parameters that can only take discrete values:

```json
{
    "name": "layer_count",
    "type": "int",
    "bounds": [0, 100],
    "step_size": 5
}
```

This restricts values to 0, 5, 10, 15, ..., 100.

### Choice Parameters (categorical)

For discrete options.

```json
{
    "name": "resin_type",
    "type": "choice",
    "values": ["epoxy", "vinyl_ester", "polyester"]
}
```

#### Ordered Choice Parameters

For ordinal categories where order matters:

```json
{
    "name": "quality_level",
    "type": "choice",
    "values": ["low", "medium", "high"],
    "is_ordered": true
}
```

## Parameter Constraints

Constraints on parameters (not outcomes). Defined in config.json:

```json
{
    "parameters": [...],
    "parameter_constraints": [
        "x + y <= 100",
        "min_temp <= max_temp"
    ]
}
```

### Sum Constraints

When parameters must sum to a value (e.g., compositions):

```json
"parameter_constraints": ["cr + ni + mo <= 100"]
```

### Order Constraints

When one parameter must be less than another:

```json
"parameter_constraints": ["min_temp <= max_temp"]
```

## Outcome Constraints

Constraints on the results (not parameters). Defined in config.json.

### Absolute Constraints

```json
"outcome_constraints": ["weight <= 10", "cost <= 50"]
```

### Relative Constraints (vs baseline)

First set a baseline:
```bash
python experiment_manager.py baseline --experiment exp/ --parameters '{"temp": 100, "time": 4}'
```

Then use relative constraints:
```json
"outcome_constraints": ["cost <= 1.1 * baseline"]
```

This limits cost to at most 10% above baseline.

## Multi-Objective Optimization

Optimize multiple objectives simultaneously.

```json
"objective": "strength, -cost"
```

To minimize an objective, prefix with `-`. Results are returned as a Pareto frontier (set of non-dominated solutions).

Use `pareto` command to get Pareto-optimal solutions:
```bash
python experiment_manager.py pareto --experiment exp/
```

## Generation Strategy Options

Control how Ax suggests trials:

```json
{
    "generation_strategy": {
        "method": "fast",
        "random_seed": 42
    }
}
```

**Methods:**
- `"fast"` (default): Bayesian optimization, good balance of exploration/exploitation
- `"quality"`: More thorough Bayesian optimization, better for expensive experiments
- `"random_search"`: Pure random sampling, useful as baseline

**Random seed:** For reproducibility. Same seed + same data = same suggestions.

## Reporting Results with Measurement Uncertainty

When reporting trial results, you can include standard error of mean (SEM):

### Simple format (just values):
```bash
python experiment_manager.py complete --experiment exp/ --trial 0 \
    --results '{"strength": 45.2, "cost": 78}'
```

### With SEM (mean and standard error):
```bash
python experiment_manager.py complete --experiment exp/ --trial 0 \
    --results '{"strength": [45.2, 1.3], "cost": [78, 2.5]}'
```

Format is `[mean, sem]` for each metric. SEM helps Ax better model measurement uncertainty and make more informed suggestions.

**Calculating SEM from replicates:**
```
SEM = standard_deviation / sqrt(n_replicates)
```

## Complete Config File Example

```json
{
    "name": "composite_optimization",
    "description": "Optimize fiber-reinforced composite for tensile strength",
    "parameters": [
        {"name": "fiber_volume", "type": "float", "bounds": [0.1, 0.6]},
        {"name": "fiber_type", "type": "choice", "values": ["carbon", "glass", "aramid"]},
        {"name": "cure_temp", "type": "float", "bounds": [80, 180]},
        {"name": "cure_time", "type": "float", "bounds": [1, 8]},
        {"name": "additive_conc", "type": "float", "bounds": [0.01, 10], "scaling": "log"}
    ],
    "parameter_constraints": ["cure_temp + cure_time <= 185"],
    "objective": "tensile_strength",
    "outcome_constraints": ["cost <= 100", "density <= 1.8"],
    "generation_strategy": {
        "method": "fast",
        "random_seed": 42
    }
}
```

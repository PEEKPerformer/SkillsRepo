# Optimization Workflow

## Phase 1: Setup

### 1.1 Gather Requirements

Ask the researcher:
1. "What are you trying to optimize?" (objective)
2. "Should we maximize or minimize it?"
3. "What parameters can you control?" (search space)
4. "What are the bounds or options for each parameter?"
5. "Any constraints on outcomes?" (e.g., weight, cost limits)
6. "Do you have any existing data from previous experiments?"

### 1.2 Create Config File

```json
{
    "name": "experiment_name",
    "description": "Brief description",
    "parameters": [...],
    "objective": "metric_name",
    "outcome_constraints": [...]
}
```

### 1.3 Initialize Experiment

```bash
python scripts/experiment_manager.py create \
    --config config.json \
    --output experiments/my_experiment/
```

Creates:
- `experiments/my_experiment/experiment.json` - Ax state
- `experiments/my_experiment/config.json` - Original config
- `experiments/my_experiment/experiment_log.md` - Human log
- `experiments/my_experiment/plots/` - Visualization directory

## Phase 2: Attach Existing Data (Optional)

If the researcher has prior data:

### 2.1 Format Data

```json
[
    {
        "parameters": {"temp": 100, "time": 4, "type": "A"},
        "results": {"strength": 45.2, "weight": 5.1}
    },
    ...
]
```

### 2.2 Attach to Experiment

```bash
python scripts/experiment_manager.py attach \
    --experiment experiments/my_experiment/ \
    --data existing_data.json
```

## Phase 3: Optimization Loop

Repeat until optimal found or budget exhausted:

### 3.1 Get Suggested Trials

```bash
python scripts/experiment_manager.py next \
    --experiment experiments/my_experiment/ \
    --n 3
```

Returns suggested parameters for next experiments:
```json
{
    "0": {"temp": 120.5, "time": 5.2, "type": "B"},
    "1": {"temp": 95.3, "time": 3.8, "type": "A"},
    "2": {"temp": 145.0, "time": 6.1, "type": "C"}
}
```

### 3.2 Validate Feasibility

**CRITICAL**: Before researcher runs experiments, validate:
- "Can you actually set temperature to 120.5°C?"
- "Is type B available in your lab?"
- "Does this combination make physical sense?"

If not feasible, discuss adjustments or mark trial as failed.

### 3.3 Execute Experiments

Researcher runs physical experiments with suggested parameters.

### 3.4 Report Results

```bash
python scripts/experiment_manager.py complete \
    --experiment experiments/my_experiment/ \
    --trial 0 \
    --results '{"strength": 52.3, "weight": 4.8}'
```

Repeat for each trial.

### 3.5 Generate Visualizations

```bash
python scripts/visualization.py progress \
    --experiment experiments/my_experiment/ \
    --output experiments/my_experiment/plots/
```

### 3.6 Commit to Git

```bash
git add experiments/my_experiment/
git commit -m "Add trials 0-2 results: best strength=52.3"
```

## Phase 4: Analysis

### 4.1 Get Best Parameters

```bash
python scripts/experiment_manager.py best \
    --experiment experiments/my_experiment/
```

### 4.2 View Summary

```bash
python scripts/experiment_manager.py summary \
    --experiment experiments/my_experiment/
```

### 4.3 Generate All Plots

```bash
# Progress plot
python scripts/visualization.py progress \
    --experiment experiments/my_experiment/ \
    --output experiments/my_experiment/plots/

# Sensitivity analysis
python scripts/visualization.py sensitivity \
    --experiment experiments/my_experiment/ \
    --output experiments/my_experiment/plots/

# 2D contour (for two parameters)
python scripts/visualization.py contour \
    --experiment experiments/my_experiment/ \
    --param1 temp --param2 time \
    --output experiments/my_experiment/plots/
```

### 4.4 Update Experiment Log

Add final summary to `experiment_log.md`:
- Best parameters found
- Predicted optimal value
- Key insights from sensitivity analysis
- Recommendations for future work

### 4.5 Final Git Commit

```bash
git add experiments/my_experiment/
git commit -m "Complete experiment: optimal temp=125°C, time=5h"
```

## Stopping Criteria

Stop optimization when:
1. **Convergence**: Last N trials show minimal improvement
2. **Budget**: Reached max number of experiments
3. **Satisfaction**: Found parameters meeting requirements
4. **Physical limits**: Hit bounds of feasible parameter space

## Troubleshooting

### "Not enough data for analysis"
Need at least 3-5 completed trials before sensitivity/contour plots work well.

### "Trial results seem wrong"
- Verify measurement procedure
- Check for outliers
- Consider marking bad trials as failed

### "Suggestions seem unreasonable"
- Check parameter bounds
- Review attached prior data
- Consider tightening search space

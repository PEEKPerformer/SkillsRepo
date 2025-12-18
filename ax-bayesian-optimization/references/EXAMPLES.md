# Domain Examples

## 1. Composite Formulation

Optimize fiber-reinforced polymer composite for tensile strength.

### Parameters

| Parameter | Type | Range/Values | Notes |
|-----------|------|--------------|-------|
| fiber_volume_fraction | float | 0.1 - 0.6 | Volume fraction of reinforcing fiber |
| fiber_type | choice | carbon, glass, aramid | Reinforcement material |
| resin_type | choice | epoxy, vinyl_ester, polyester | Matrix material |
| cure_temp | float | 80 - 180 | Cure temperature (°C) |
| cure_time | float | 1 - 8 | Cure duration (hours) |

### Config

```json
{
    "name": "composite_tensile_optimization",
    "description": "Optimize CFRP composite for maximum tensile strength",
    "parameters": [
        {"name": "fiber_volume_fraction", "type": "float", "bounds": [0.1, 0.6]},
        {"name": "fiber_type", "type": "choice", "values": ["carbon", "glass", "aramid"]},
        {"name": "resin_type", "type": "choice", "values": ["epoxy", "vinyl_ester", "polyester"]},
        {"name": "cure_temp", "type": "float", "bounds": [80, 180]},
        {"name": "cure_time", "type": "float", "bounds": [1, 8]}
    ],
    "objective": "tensile_strength",
    "outcome_constraints": ["cost <= 100", "density <= 1.8"]
}
```

### Typical Results Format

```json
{
    "tensile_strength": 450.5,
    "cost": 78.2,
    "density": 1.65
}
```

---

## 2. 3D Printing Parameters

Optimize FDM print settings for part strength.

### Parameters

| Parameter | Type | Range/Values | Notes |
|-----------|------|--------------|-------|
| infill_density | float | 10 - 100 | Interior fill percentage |
| layer_height | float | 0.1 - 0.4 | Layer thickness (mm) |
| infill_type | choice | honeycomb, gyroid, lines, rectilinear | Fill pattern |
| print_speed | float | 30 - 100 | Print speed (mm/s) |
| nozzle_temp | float | 190 - 230 | Nozzle temperature (°C) |

### Config

```json
{
    "name": "3d_print_strength",
    "description": "Maximize compressive strength of 3D printed parts",
    "parameters": [
        {"name": "infill_density", "type": "float", "bounds": [10, 100]},
        {"name": "layer_height", "type": "float", "bounds": [0.1, 0.4]},
        {"name": "infill_type", "type": "choice", "values": ["honeycomb", "gyroid", "lines", "rectilinear"]},
        {"name": "print_speed", "type": "float", "bounds": [30, 100]},
        {"name": "nozzle_temp", "type": "float", "bounds": [190, 230]}
    ],
    "objective": "compressive_strength",
    "outcome_constraints": ["weight <= 15", "print_time <= 180"]
}
```

### Typical Results Format

```json
{
    "compressive_strength": 42.3,
    "weight": 12.5,
    "print_time": 95
}
```

---

## 3. Alloy Composition

Optimize stainless steel alloy for hardness and corrosion resistance (multi-objective).

### Parameters

| Parameter | Type | Range/Values | Notes |
|-----------|------|--------------|-------|
| cr_content | float | 10 - 20 | Chromium (wt%) |
| ni_content | float | 5 - 15 | Nickel (wt%) |
| mo_content | float | 0 - 5 | Molybdenum (wt%) |
| c_content | float | 0.01 - 0.15 | Carbon (wt%) |
| heat_treat_temp | float | 900 - 1100 | Solution treatment temp (°C) |

Note: For composition constraints (e.g., Cr + Ni + Mo <= 35), use parameter constraints in the Ax API directly.

### Config

```json
{
    "name": "alloy_optimization",
    "description": "Optimize stainless steel for hardness and corrosion resistance",
    "parameters": [
        {"name": "cr_content", "type": "float", "bounds": [10, 20]},
        {"name": "ni_content", "type": "float", "bounds": [5, 15]},
        {"name": "mo_content", "type": "float", "bounds": [0, 5]},
        {"name": "c_content", "type": "float", "bounds": [0.01, 0.15]},
        {"name": "heat_treat_temp", "type": "float", "bounds": [900, 1100]}
    ],
    "objective": "hardness, corrosion_resistance"
}
```

### Multi-Objective Notes

With multiple objectives, results are a Pareto frontier - no single "best" solution, but a set of optimal trade-offs. Use `get_pareto_frontier()` to see all optimal combinations.

### Typical Results Format

```json
{
    "hardness": 58.5,
    "corrosion_resistance": 8.2
}
```

---

## Attaching Existing Data

If prior experiments exist, format as:

```json
[
    {
        "parameters": {
            "fiber_volume_fraction": 0.35,
            "fiber_type": "carbon",
            "resin_type": "epoxy",
            "cure_temp": 120,
            "cure_time": 4
        },
        "results": {
            "tensile_strength": 380.2,
            "cost": 85.0,
            "density": 1.58
        }
    }
]
```

Then attach:
```bash
python scripts/experiment_manager.py attach \
    --experiment experiments/composite/ \
    --data prior_data.json
```

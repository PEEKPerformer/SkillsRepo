#!/usr/bin/env python3
"""
Ax experiment manager for materials science Bayesian optimization.

Provides a simple CLI wrapper around Meta's Ax library for human-in-the-loop
optimization experiments. Handles experiment creation, trial management,
and JSON persistence for git version control.

Usage:
    python experiment_manager.py create --config config.json --output experiments/my_exp/
    python experiment_manager.py next --experiment experiments/my_exp/ --n 3
    python experiment_manager.py complete --experiment experiments/my_exp/ --trial 0 --results '{"strength": 45.2}'
    python experiment_manager.py best --experiment experiments/my_exp/
    python experiment_manager.py summary --experiment experiments/my_exp/
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    from ax.api.client import Client
    from ax.api.configs import RangeParameterConfig, ChoiceParameterConfig
except ImportError:
    print("ERROR: ax-platform not installed. Run: pip install ax-platform")
    sys.exit(1)


def create_experiment(config_path: str, output_path: str) -> None:
    """
    Create a new experiment from a JSON configuration file.

    Config format:
    {
        "name": "experiment_name",
        "description": "What we're optimizing",
        "parameters": [
            {"name": "x", "type": "float", "bounds": [0, 100]},
            {"name": "x_log", "type": "float", "bounds": [0.001, 1000], "scaling": "log"},
            {"name": "x_step", "type": "int", "bounds": [0, 100], "step_size": 5},
            {"name": "category", "type": "choice", "values": ["a", "b", "c"]}
        ],
        "parameter_constraints": ["x + y <= 100"],  # optional
        "objective": "strength",  # prefix with - to minimize
        "outcome_constraints": ["weight <= 10"],  # optional
        "generation_strategy": {  # optional
            "method": "fast",  # "fast", "quality", or "random_search"
            "random_seed": 42  # for reproducibility
        }
    }
    """
    config_file = Path(config_path)
    output_dir = Path(output_path)

    if not config_file.exists():
        print(f"ERROR: Config file not found: {config_path}")
        sys.exit(1)

    with open(config_file) as f:
        config = json.load(f)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize Ax Client
    client = Client()

    # Build parameter configs
    parameters = []
    for p in config["parameters"]:
        if p["type"] in ("float", "int"):
            parameters.append(RangeParameterConfig(
                name=p["name"],
                parameter_type=p["type"],
                bounds=tuple(p["bounds"]),
                step_size=p.get("step_size"),  # optional: discrete steps
                scaling=p.get("scaling"),  # optional: "log" or "linear"
            ))
        elif p["type"] == "choice":
            parameters.append(ChoiceParameterConfig(
                name=p["name"],
                parameter_type="str",
                values=p["values"],
                is_ordered=p.get("is_ordered"),  # optional: ordinal vs categorical
            ))

    # Configure experiment
    param_constraints = config.get("parameter_constraints", [])
    client.configure_experiment(
        name=config.get("name", "optimization_experiment"),
        description=config.get("description", ""),
        parameters=parameters,
        parameter_constraints=param_constraints if param_constraints else None,
    )

    # Configure optimization
    objective = config["objective"]
    constraints = config.get("outcome_constraints", [])

    client.configure_optimization(
        objective=objective,
        outcome_constraints=constraints if constraints else None
    )

    # Configure generation strategy (always configure to ensure valid JSON save)
    gen_config = config.get("generation_strategy", {})
    client.configure_generation_strategy(
        method=gen_config.get("method", "fast"),
        initialization_random_seed=gen_config.get("random_seed"),
    )

    # Save experiment state
    experiment_file = output_dir / "experiment.json"
    client.save_to_json_file(str(experiment_file))

    # Save original config for reference
    config_copy = output_dir / "config.json"
    with open(config_copy, 'w') as f:
        json.dump(config, f, indent=2)

    # Initialize experiment log
    log_file = output_dir / "experiment_log.md"
    with open(log_file, 'w') as f:
        f.write(f"# Experiment: {config.get('name', 'Optimization')}\n\n")
        f.write(f"**Created:** {datetime.now().isoformat()}\n\n")
        f.write(f"**Description:** {config.get('description', 'N/A')}\n\n")
        f.write(f"**Objective:** {objective}\n\n")
        if constraints:
            f.write(f"**Outcome Constraints:** {', '.join(constraints)}\n\n")
        if param_constraints:
            f.write(f"**Parameter Constraints:** {', '.join(param_constraints)}\n\n")
        if gen_config:
            f.write(f"**Generation Strategy:** method={gen_config.get('method', 'fast')}")
            if gen_config.get('random_seed'):
                f.write(f", seed={gen_config['random_seed']}")
            f.write("\n\n")
        f.write("## Parameters\n\n")
        for p in config["parameters"]:
            if p["type"] in ("float", "int"):
                extras = []
                if p.get("scaling"):
                    extras.append(f"scaling={p['scaling']}")
                if p.get("step_size"):
                    extras.append(f"step={p['step_size']}")
                extra_str = f" [{', '.join(extras)}]" if extras else ""
                f.write(f"- **{p['name']}** ({p['type']}): {p['bounds'][0]} to {p['bounds'][1]}{extra_str}\n")
            else:
                ordered_str = " (ordered)" if p.get("is_ordered") else ""
                f.write(f"- **{p['name']}** (choice{ordered_str}): {', '.join(p['values'])}\n")
        f.write("\n## Trial History\n\n")

    # Create plots directory
    (output_dir / "plots").mkdir(exist_ok=True)

    print(f"Experiment created at: {output_dir}")
    print(f"  - experiment.json: Ax state (for persistence)")
    print(f"  - config.json: Original configuration")
    print(f"  - experiment_log.md: Human-readable log")


def attach_data(experiment_path: str, data_path: str) -> None:
    """
    Attach existing trial data to an experiment.

    Data format (JSON):
    [
        {
            "parameters": {"x": 10, "category": "a"},
            "results": {"strength": 45.2, "weight": 5.1}
        },
        ...
    ]
    """
    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    with open(data_path) as f:
        data = json.load(f)

    client = Client.load_from_json_file(str(exp_file))

    log_file = exp_dir / "experiment_log.md"

    for entry in data:
        trial_index = client.attach_trial(parameters=entry["parameters"])
        client.complete_trial(trial_index=trial_index, raw_data=entry["results"])

        # Log the attached trial
        with open(log_file, 'a') as f:
            f.write(f"### Trial {trial_index} (attached existing data)\n\n")
            f.write(f"**Parameters:** {json.dumps(entry['parameters'])}\n\n")
            f.write(f"**Results:** {json.dumps(entry['results'])}\n\n")
            f.write("---\n\n")

    client.save_to_json_file(str(exp_file))
    print(f"Attached {len(data)} existing trials to experiment")


def get_next_trials(experiment_path: str, n: int = 1) -> dict:
    """
    Get the next suggested trials from Ax.

    Returns a dict mapping trial_index -> parameters.
    """
    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))

    trials = client.get_next_trials(max_trials=n)

    # Save updated state
    client.save_to_json_file(str(exp_file))

    # Log suggested trials
    log_file = exp_dir / "experiment_log.md"
    with open(log_file, 'a') as f:
        f.write(f"### Suggested Trials ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n")
        for trial_index, params in trials.items():
            f.write(f"**Trial {trial_index}:** {json.dumps(params)}\n\n")
        f.write("---\n\n")

    # Output for Claude/user
    print(json.dumps(trials, indent=2))
    return trials


def complete_trial(experiment_path: str, trial_index: int, results: dict) -> None:
    """
    Report results for a completed trial.

    results: dict mapping metric names to values.

    Two formats supported:
    1. Simple: {"strength": 45.2, "weight": 5.1}
    2. With SEM (standard error of mean): {"strength": [45.2, 1.3], "weight": [5.1, 0.2]}
       - Format is [mean, sem] for each metric
       - SEM helps Ax better model measurement uncertainty
    """
    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))

    # Convert [mean, sem] lists to (mean, sem) tuples for Ax API
    processed_results = {}
    for metric, value in results.items():
        if isinstance(value, list) and len(value) == 2:
            processed_results[metric] = tuple(value)
        else:
            processed_results[metric] = value

    client.complete_trial(trial_index=trial_index, raw_data=processed_results)

    # Save updated state
    client.save_to_json_file(str(exp_file))

    # Log completed trial
    log_file = exp_dir / "experiment_log.md"
    with open(log_file, 'a') as f:
        f.write(f"### Trial {trial_index} Completed ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n")
        f.write(f"**Results:** {json.dumps(results)}\n\n")
        f.write("---\n\n")

    print(f"Trial {trial_index} completed with results: {results}")


def get_best(experiment_path: str) -> dict:
    """
    Get the best parameters found so far.

    Returns dict with best_parameters, prediction, trial_index, and arm_name.
    """
    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))

    try:
        best_params, prediction, trial_idx, arm_name = client.get_best_parameterization()
        result = {
            "best_parameters": best_params,
            "prediction": {k: {"mean": v[0], "variance": v[1]} for k, v in prediction.items()},
            "trial_index": trial_idx,
            "arm_name": arm_name
        }
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"ERROR: Could not determine best parameters: {e}")
        print("(This may happen if no trials have been completed yet)")
        sys.exit(1)


def summarize(experiment_path: str) -> str:
    """
    Generate a summary of the experiment.
    """
    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))

    # Get summary dataframe
    summary_df = client.summarize()

    print("=== Experiment Summary ===\n")
    print(summary_df.to_string())

    return summary_df.to_string()


def mark_failed(experiment_path: str, trial_index: int, reason: str = "") -> None:
    """
    Mark a trial as FAILED.

    Use when equipment fails, sample is contaminated, or measurement is invalid.
    Failed trials inform the model but won't be re-suggested.
    """
    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))
    client.mark_trial_failed(trial_index=trial_index, failed_reason=reason)
    client.save_to_json_file(str(exp_file))

    # Log
    log_file = exp_dir / "experiment_log.md"
    with open(log_file, 'a') as f:
        f.write(f"### Trial {trial_index} FAILED ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n")
        if reason:
            f.write(f"**Reason:** {reason}\n\n")
        f.write("---\n\n")

    print(f"Trial {trial_index} marked as FAILED" + (f": {reason}" if reason else ""))


def mark_abandoned(experiment_path: str, trial_index: int, reason: str = "") -> None:
    """
    Mark a trial as ABANDONED.

    Use when parameter combination is physically impossible or infeasible.
    Abandoned trials won't be re-suggested.
    """
    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))
    client.mark_trial_abandoned(trial_index=trial_index)  # Note: Ax API doesn't accept reason
    client.save_to_json_file(str(exp_file))

    # Log
    log_file = exp_dir / "experiment_log.md"
    with open(log_file, 'a') as f:
        f.write(f"### Trial {trial_index} ABANDONED ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n")
        if reason:
            f.write(f"**Reason:** {reason}\n\n")
        f.write("---\n\n")

    print(f"Trial {trial_index} marked as ABANDONED" + (f": {reason}" if reason else ""))


def predict(experiment_path: str, parameters: str) -> dict:
    """
    Predict outcome for a parameter combination without running experiment.

    Useful for exploring "what if" scenarios.
    """
    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    try:
        params = json.loads(parameters)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in --parameters: {e}")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))

    try:
        predictions = client.predict(points=[params])
        result = {
            "parameters": params,
            "predictions": {k: {"mean": v[0], "variance": v[1]} for k, v in predictions[0].items()}
        }
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"ERROR: Could not predict: {e}")
        print("(Need at least a few completed trials for predictions)")
        sys.exit(1)


def get_pareto(experiment_path: str) -> list:
    """
    Get Pareto frontier for multi-objective optimization.

    Returns list of optimal trade-off solutions.
    """
    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))

    try:
        frontier = client.get_pareto_frontier()
        results = []
        for params, metrics, trial_idx, arm_name in frontier:
            results.append({
                "parameters": params,
                "metrics": {k: {"mean": v[0], "variance": v[1]} for k, v in metrics.items()},
                "trial_index": trial_idx,
                "arm_name": arm_name
            })
        print(json.dumps(results, indent=2))
        return results
    except Exception as e:
        print(f"ERROR: Could not get Pareto frontier: {e}")
        print("(This requires multi-objective optimization with completed trials)")
        sys.exit(1)


def set_baseline(experiment_path: str, parameters: str) -> None:
    """
    Set baseline parameters for relative constraints.

    After setting baseline, you can use constraints like:
    "cost <= 1.1 * baseline" (max 10% cost increase)
    """
    exp_dir = Path(experiment_path)
    exp_file = exp_dir / "experiment.json"

    if not exp_file.exists():
        print(f"ERROR: Experiment not found: {exp_file}")
        sys.exit(1)

    try:
        params = json.loads(parameters)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in --parameters: {e}")
        print("Example format: '{\"temp\": 100, \"time\": 4}'")
        sys.exit(1)

    client = Client.load_from_json_file(str(exp_file))

    client.attach_baseline(parameters=params)

    # Save updated state
    client.save_to_json_file(str(exp_file))

    # Log baseline
    log_file = exp_dir / "experiment_log.md"
    with open(log_file, 'a') as f:
        f.write(f"### Baseline Set ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n")
        f.write(f"**Parameters:** {json.dumps(params)}\n\n")
        f.write("Relative constraints (e.g., `cost <= 1.1 * baseline`) now use these values.\n\n")
        f.write("---\n\n")

    print(f"Baseline set: {params}")
    print("You can now use relative constraints like: cost <= 1.1 * baseline")


def main():
    parser = argparse.ArgumentParser(description="Ax experiment manager for materials science optimization")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # create command
    create_parser = subparsers.add_parser("create", help="Create new experiment")
    create_parser.add_argument("--config", required=True, help="Path to config JSON file")
    create_parser.add_argument("--output", required=True, help="Output directory for experiment")

    # attach command
    attach_parser = subparsers.add_parser("attach", help="Attach existing data")
    attach_parser.add_argument("--experiment", required=True, help="Path to experiment directory")
    attach_parser.add_argument("--data", required=True, help="Path to data JSON file")

    # next command
    next_parser = subparsers.add_parser("next", help="Get next suggested trials")
    next_parser.add_argument("--experiment", required=True, help="Path to experiment directory")
    next_parser.add_argument("--n", type=int, default=1, help="Number of trials to suggest")

    # complete command
    complete_parser = subparsers.add_parser("complete", help="Complete a trial with results")
    complete_parser.add_argument("--experiment", required=True, help="Path to experiment directory")
    complete_parser.add_argument("--trial", type=int, required=True, help="Trial index")
    complete_parser.add_argument("--results", required=True, help="Results JSON string")

    # best command
    best_parser = subparsers.add_parser("best", help="Get best parameters found")
    best_parser.add_argument("--experiment", required=True, help="Path to experiment directory")

    # summary command
    summary_parser = subparsers.add_parser("summary", help="Show experiment summary")
    summary_parser.add_argument("--experiment", required=True, help="Path to experiment directory")

    # baseline command
    baseline_parser = subparsers.add_parser("baseline", help="Set baseline for relative constraints")
    baseline_parser.add_argument("--experiment", required=True, help="Path to experiment directory")
    baseline_parser.add_argument("--parameters", required=True, help="Baseline parameters JSON string")

    # failed command
    failed_parser = subparsers.add_parser("failed", help="Mark trial as failed")
    failed_parser.add_argument("--experiment", required=True, help="Path to experiment directory")
    failed_parser.add_argument("--trial", type=int, required=True, help="Trial index")
    failed_parser.add_argument("--reason", default="", help="Reason for failure")

    # abandoned command
    abandoned_parser = subparsers.add_parser("abandoned", help="Mark trial as abandoned (infeasible)")
    abandoned_parser.add_argument("--experiment", required=True, help="Path to experiment directory")
    abandoned_parser.add_argument("--trial", type=int, required=True, help="Trial index")
    abandoned_parser.add_argument("--reason", default="", help="Reason for abandonment")

    # predict command
    predict_parser = subparsers.add_parser("predict", help="Predict outcome for parameters")
    predict_parser.add_argument("--experiment", required=True, help="Path to experiment directory")
    predict_parser.add_argument("--parameters", required=True, help="Parameters JSON string")

    # pareto command
    pareto_parser = subparsers.add_parser("pareto", help="Get Pareto frontier (multi-objective)")
    pareto_parser.add_argument("--experiment", required=True, help="Path to experiment directory")

    args = parser.parse_args()

    if args.command == "create":
        create_experiment(args.config, args.output)
    elif args.command == "attach":
        attach_data(args.experiment, args.data)
    elif args.command == "next":
        get_next_trials(args.experiment, args.n)
    elif args.command == "complete":
        try:
            results = json.loads(args.results)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in --results: {e}")
            print("Example format: '{\"strength\": 45.2, \"weight\": 5.1}'")
            sys.exit(1)
        complete_trial(args.experiment, args.trial, results)
    elif args.command == "baseline":
        set_baseline(args.experiment, args.parameters)
    elif args.command == "failed":
        mark_failed(args.experiment, args.trial, args.reason)
    elif args.command == "abandoned":
        mark_abandoned(args.experiment, args.trial, args.reason)
    elif args.command == "predict":
        predict(args.experiment, args.parameters)
    elif args.command == "pareto":
        get_pareto(args.experiment)
    elif args.command == "best":
        get_best(args.experiment)
    elif args.command == "summary":
        summarize(args.experiment)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

# Best Practices for Bayesian Optimization

Practical guidance for getting better experimental results. These recommendations are drawn from foundational BO literature and real-world materials science applications.

## Before Starting

### Is BO Right for This Problem?

**Good fit:**
- Experiments are expensive (time, cost, materials)
- Want to minimize number of trials to find optimum
- Continuous or mixed parameter space
- Single or few objectives to optimize

**Poor fit:**
- Experiments are cheap (just run more)
- >15 parameters (BO struggles in high dimensions)
- Purely discrete/combinatorial space with no structure
- No clear objective metric

### Designing the Search Space

| Guideline | Why It Matters |
|-----------|----------------|
| Keep parameters ≤10 | BO effectiveness drops rapidly above 10-15 dimensions |
| Use tight, realistic bounds | Wide bounds waste experiments exploring infeasible regions |
| Use log-scale for concentrations, rates, time constants spanning >2 orders of magnitude | Linear spacing wastes trials at high end |
| Encode constraints explicitly | `parameter_constraints` prevents impossible combinations |
| Consider which parameters actually matter | Run screening experiments first if unsure |

### Initial Data

**Critical:** BO needs initial data before suggestions become reliable.

- **Minimum:** 5 trials (absolute floor for fitting the GP model)
- **Recommended:** 2-3× number of parameters (e.g., 10-15 trials for 5 parameters)
- **With prior data:** Attach existing experiments even if not perfectly systematic

**Initial trial strategies:**
1. **Random:** Simple, unbiased coverage
2. **Latin Hypercube:** Better space coverage than pure random
3. **Factorial corners:** Test extremes of parameter space
4. **Domain knowledge:** Include conditions you expect to work well

## During Optimization

### Interpreting Suggestions

**Early optimization (<10 trials):**
- Suggestions are exploratory—expect variety
- Don't be alarmed by "strange" combinations
- BO is mapping the space, not exploiting yet

**Mid optimization (10-30 trials):**
- Suggestions should start clustering near promising regions
- Mix of exploitation (refining good areas) and exploration (checking unexplored regions)

**Late optimization (>30 trials):**
- Suggestions should converge
- Similar suggestions repeatedly = likely near optimum
- Diminishing returns expected

### Red Flags

| Observation | Likely Cause | Action |
|-------------|--------------|--------|
| Suggestions always at parameter bounds | Bounds too tight, or optimum outside range | Expand bounds, verify physical limits |
| Wildly varying suggestions | High uncertainty, insufficient data | Run more trials before trusting suggestions |
| Same suggestion repeated exactly | May have converged, or model overconfident | Check if results are actually improving |
| Suggestions violate physics | Missing constraints in config | Add parameter constraints |
| Results much worse than expected | Measurement error, or model misfit | Verify experimental procedure |

### Handling Measurement Uncertainty

**Always report SEM when possible:**
```bash
# With 3+ replicates, calculate SEM = std_dev / sqrt(n)
--results '{"strength": [45.2, 1.3]}'  # [mean, sem]
```

**Why it matters:**
- BO weights uncertain measurements less heavily
- Prevents overconfidence in noisy data
- Leads to better exploration decisions

**Replicate strategy:**
- Run 3+ replicates for key trials (best candidates, validation)
- Single measurements OK for screening
- If measurement noise is high, more replicates are essential

### When Trials Fail

**Equipment failure / contaminated sample:**
```bash
python experiment_manager.py failed --experiment exp/ --trial N --reason "furnace malfunction"
```
- Informs model that this region wasn't actually tested
- May suggest similar parameters again

**Infeasible combination:**
```bash
python experiment_manager.py abandoned --experiment exp/ --trial N --reason "materials incompatible"
```
- Tells model to avoid this region
- Document why for future reference

**Always document the reason** — this is scientific record-keeping.

## Stopping Criteria

### When to Stop

| Criterion | How to Check |
|-----------|--------------|
| **Convergence** | Last 5-10 trials show <5% improvement in objective |
| **Budget exhausted** | Reached max experiments you can afford |
| **Satisficing** | Found parameters meeting your requirements (even if not optimal) |
| **Physical limits** | Hitting equipment/material constraints repeatedly |
| **Diminishing returns** | Improvement per trial dropping below meaningful threshold |

### Signs of Convergence

- Suggestions cluster tightly around one region
- Best value plateaus across multiple trials
- Sensitivity analysis shows you're near a local/global maximum
- Model uncertainty in best region is low

## Validation

### Before Declaring Success

1. **Run replicates:** Test "best" parameters 3-5 times to confirm
2. **Check reproducibility:** Can you get the same result tomorrow?
3. **Verify physically:** Do the optimal parameters make scientific sense?
4. **Document uncertainty:** Report mean ± SEM for final result

### Final Validation Protocol

```bash
# Get best parameters
python experiment_manager.py best --experiment exp/

# Run 3-5 replicates at best parameters
# Report: mean, std dev, SEM, and range

# Document in experiment_log.md:
# - Best parameters
# - Validation results (mean ± SEM)
# - Whether result is statistically distinguishable from alternatives
```

## Common Mistakes

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| Starting BO with 0 initial data | Poor early suggestions, wasted trials | Run 5-10 initial experiments first |
| Too many parameters | BO can't model the space effectively | Reduce to ≤10, screen first if needed |
| Ignoring measurement noise | Overconfident model, missed optima | Report SEM, run replicates |
| Bounds too wide | Wastes trials in infeasible regions | Use realistic equipment/material limits |
| Stopping too early | May not have found optimum | Check convergence criteria |
| Not validating final result | "Best" may be noise, not signal | Run replicates at optimal parameters |
| Not documenting failures | Lose scientific context | Always log why trials failed |

## Quick Reference

**Minimum viable optimization:**
1. Define ≤10 parameters with realistic bounds
2. Run 5-10 initial trials
3. Get BO suggestions in batches of 1-3
4. Report results with SEM when possible
5. Stop when converged or budget exhausted
6. Validate best result with replicates

**Rule of thumb for trial count:**
- Screening: 2× number of parameters
- Good optimization: 5-10× number of parameters
- Thorough optimization: 20× number of parameters

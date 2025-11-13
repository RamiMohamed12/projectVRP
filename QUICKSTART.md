# Quick Start Guide

## Setup

1. **Install dependencies:**
   ```bash
   pip install numpy vrplib pyyaml pandas matplotlib seaborn jupyter
   ```

2. **Verify data files:**
   - Ensure VRP instances are in the `data/` folder
   - Check that corresponding `.sol` files exist for optimal solutions

## Running the Solver

### Option 1: Run Main Solver (cvrp_solver.ipynb)

1. Open Jupyter:
   ```bash
   jupyter notebook cvrp_solver.ipynb
   ```

2. Run all cells or step by step:
   - **Cells 1-3**: Import libraries and load configuration
   - **Cells 4-10**: Define solver components
   - **Cells 11-13**: Test on sample instances
   - **Cell 14**: Solve all CVRP instances
   - **Cell 15-16**: View and export summary

3. Check results in:
   - `solutions/` folder for computed solutions
   - `solutions/summary_results.csv` for summary

### Option 2: Run Statistical Analysis (statistical_analysis.ipynb)

1. Open Jupyter:
   ```bash
   jupyter notebook statistical_analysis.ipynb
   ```

2. Run experiments:
   - **Experiment 1**: Initial Temperature (cells vary)
   - **Experiment 2**: Cooling Rate Alpha
   - **Experiment 3**: Tabu Tenure
   - **Experiment 4**: Iterations per Temperature
   - **Final cells**: Heatmaps and recommendations

3. Check results in:
   - `analysis_results/plots/` for visualizations
   - `analysis_results/csv/` for data tables
   - `analysis_results/recommended_config.yaml` for best parameters

## Customization

### Modify Parameters

Edit `config.yaml`:

```yaml
# Example: Increase temperature for harder instances
simulated_annealing:
  initial_temperature: 2000.0  # Changed from 1000.0
  
# Example: Use fewer neighborhoods for speed
vnd:
  neighborhoods:
    - swap
    - relocate
    # Removed two_opt and cross_exchange for speed
```

### Test Single Instance

In `cvrp_solver.ipynb`, modify:

```python
# Instead of solving all instances
test_instance = 'data/E-n13-k4.vrp'
result = solve_cvrp(test_instance)
save_solution(result)
```

### Change Time Limits

In `config.yaml`:

```yaml
general:
  time_limit_seconds: 600  # 10 minutes per instance
```

## Understanding Output

### Solution File Format

```
Route #1: 1 
Route #2: 8 5 3 
Route #3: 9 12 10 6 
Route #4: 11 4 7 2 
Cost 247
```

- Each route starts and ends at depot (0), not shown
- Numbers are customer IDs
- Cost is total distance traveled

### Summary CSV Columns

- **Instance**: Problem file name
- **Computed Cost**: Our solution cost
- **Optimal Cost**: Known best solution (if available)
- **Gap (%)**: Percentage difference from optimal
- **Routes**: Number of vehicles used
- **Time (s)**: Computation time

### Gap Calculation

```
Gap (%) = ((Computed Cost - Optimal Cost) / Optimal Cost) × 100
```

Target: Gap ≤ 7%

## Troubleshooting

### Issue: "Module not found"
**Solution**: Install missing package
```bash
pip install <package_name>
```

### Issue: "No such file or directory"
**Solution**: Check paths are correct
```python
# Use absolute paths if needed
instance_path = os.path.abspath('data/E-n13-k4.vrp')
```

### Issue: Solution quality is poor
**Solutions**:
1. Increase time limit in config.yaml
2. Increase initial temperature
3. Decrease alpha (slower cooling)
4. Increase iterations per temperature

### Issue: Solver too slow
**Solutions**:
1. Reduce number of neighborhoods in VND
2. Decrease iterations per temperature
3. Use smaller test instances first
4. Reduce time limit for initial testing

## Best Practices

1. **Start small**: Test with E-n13-k4.vrp before large instances
2. **Run analysis**: Use statistical_analysis.ipynb to find best parameters
3. **Save results**: Always keep CSV summaries for comparison
4. **Document changes**: Note parameter changes when testing
5. **Verify feasibility**: Check that all solutions respect capacity

## Performance Tips

### For Fast Testing:
```yaml
simulated_annealing:
  initial_temperature: 500
  alpha: 0.90  # Faster cooling
  iterations_per_temperature: 50
  
general:
  time_limit_seconds: 30
```

### For Best Quality:
```yaml
simulated_annealing:
  initial_temperature: 2000
  alpha: 0.97  # Slower cooling
  iterations_per_temperature: 200
  
general:
  time_limit_seconds: 300
```

## Next Steps

1. ✅ Run main solver on all CVRP instances
2. ✅ Check if gaps are within 7%
3. ✅ Run statistical analysis to tune parameters
4. ✅ Apply recommended config and re-run
5. ⏭️ Extend to CVRP with time windows (future work)

## File Checklist

Before running:
- [ ] `config.yaml` exists
- [ ] `data/` folder contains .vrp files
- [ ] `data/` folder contains corresponding .sol files
- [ ] `solutions/` folder exists (auto-created)
- [ ] `analysis_results/` folders exist (auto-created)

After running:
- [ ] Solutions saved in `solutions/`
- [ ] Summary CSV created
- [ ] Analysis plots generated
- [ ] Gaps within target range

## Support

If you encounter issues:
1. Check the README.md for detailed information
2. Verify all dependencies are installed
3. Ensure data files are in correct format
4. Review the vrplib.md documentation

---

**Ready to solve VRP! 🚀**

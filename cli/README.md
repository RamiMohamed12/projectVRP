# CVRP CLI Solver

This CLI provides a runnable version of the CVRP solver from `cvrp_solver.ipynb`.

Usage:

- List available instances:

```
python cli/solve_cvrp.py --list
```

- Solve a specific instance and show plots:

```
python cli/solve_cvrp.py --instance data/B-n31-k5.vrp --plot
```

- Interactively select an instance and run solver:

```
python cli/solve_cvrp.py
```

Notes:
- The script reads `config.yaml` from the repository root.
- The script requires `vrplib` to parse instances; install it with:

```
pip install vrplib
```

- Output plots are saved in `plots/` and computed solutions in `solutions/`.

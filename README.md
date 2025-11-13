# CVRP Solver - Hybrid Metaheuristic Approach

A comprehensive solution for solving Capacitated Vehicle Routing Problems (CVRP) using a hybrid metaheuristic algorithm combining Local Search, Variable Neighborhood Descent (VND), Simulated Annealing (SA), and Tabu Search.

## 🎯 Objective

Find high-quality solutions for CVRP instances **without time windows** that are within **7% gap** from the optimal solution.

## 📁 Project Structure

```
projectVRP/
├── config.yaml                      # Algorithm parameters configuration
├── cvrp_solver.ipynb               # Main CVRP solver notebook
├── statistical_analysis.ipynb      # Parameter tuning and analysis
├── data/                           # VRP instances and optimal solutions
│   ├── *.vrp                      # VRPLIB format instances
│   ├── *.sol                      # Optimal solutions
│   └── *.txt                      # Solomon format instances
├── solutions/                      # Computed solutions output
│   ├── *_computed.sol             # Solutions found by our algorithm
│   └── summary_results.csv        # Summary of all results
└── analysis_results/               # Statistical analysis results
    ├── plots/                      # Visualization plots
    ├── csv/                        # Experiment data in CSV format
    └── recommended_config.yaml     # Best parameter configuration
```

## 🚀 Getting Started

### Prerequisites

Install required Python packages:

```bash
pip install numpy vrplib pyyaml pandas matplotlib seaborn jupyter
```

### Quick Start

1. **Run the CVRP Solver:**
   Open `cvrp_solver.ipynb` and run all cells to:
   - Load CVRP instances from the data folder
   - Apply the hybrid metaheuristic algorithm
   - Save computed solutions to the solutions folder
   - Compare with optimal solutions and calculate gaps

2. **Perform Statistical Analysis:**
   Open `statistical_analysis.ipynb` and run all cells to:
   - Test different parameter configurations
   - Generate plots showing parameter impacts
   - Export results to CSV files
   - Get recommended parameter values

## 🧮 Algorithm Components

### 1. Initial Solution Construction
- **Nearest Neighbor Heuristic**: Constructs feasible initial routes
- Configurable randomness for diversification

### 2. Variable Neighborhood Descent (VND)
Systematic exploration of multiple neighborhoods:
- **Swap**: Exchange customers between different routes
- **Relocate**: Move a customer to another route
- **2-opt**: Intra-route optimization
- **Cross-exchange**: Exchange segments between routes

### 3. Simulated Annealing (SA)
- Accepts worse solutions with decreasing probability
- Helps escape local optima
- Cooling schedule: T = T × α

### 4. Tabu Search
- Memory structure to avoid cycling
- Dynamic tabu tenure with randomization
- Aspiration criterion for accepting tabu moves

## ⚙️ Configuration

Edit `config.yaml` to adjust algorithm parameters:

```yaml
simulated_annealing:
  initial_temperature: 1000.0      # Starting temperature
  final_temperature: 0.1           # Stopping temperature
  alpha: 0.95                      # Cooling rate
  iterations_per_temperature: 100  # Iterations at each temp

tabu_search:
  tabu_tenure: 20                  # Tabu list size
  tabu_tenure_random_range: 10     # Random variation
  aspiration_enabled: true         # Accept tabu if best so far

vnd:
  neighborhoods:                   # Neighborhood order
    - swap
    - relocate
    - two_opt
    - cross_exchange
  max_iterations_without_improvement: 50

local_search:
  max_iterations: 1000
  max_iterations_without_improvement: 200

quality:
  target_gap_percentage: 7.0       # Target quality (%)
```

## 📊 Statistical Analysis

The `statistical_analysis.ipynb` notebook performs comprehensive parameter tuning:

### Experiments Conducted:
1. **Initial Temperature Impact**: Tests values from 100 to 5000
2. **Cooling Rate (Alpha) Impact**: Tests values from 0.85 to 0.99
3. **Tabu Tenure Impact**: Tests values from 5 to 50
4. **Iterations per Temperature Impact**: Tests values from 50 to 300

### Outputs:
- **Plots**: Line charts, box plots, and heatmaps showing parameter effects
- **CSV Files**: Detailed results for each experiment
- **Recommended Config**: Best parameter values based on experiments

## 📈 Results

The solver generates:

1. **Solution Files** (`.sol` format):
   ```
   Route #1: 3 5 8 12
   Route #2: 2 7 11 4
   Cost 247
   ```

2. **Summary CSV** with metrics:
   - Instance name
   - Computed cost
   - Optimal cost (if available)
   - Gap percentage
   - Number of routes
   - Computation time

3. **Visualizations**:
   - Cost convergence over iterations
   - Parameter sensitivity analysis
   - Gap distribution box plots
   - Parameter interaction heatmaps

## 🎓 Understanding the Algorithm

### Why This Combination?

1. **Local Search**: Fast improvement within neighborhoods
2. **VND**: Systematic exploration prevents premature convergence
3. **Simulated Annealing**: Probabilistic acceptance enables escaping local optima
4. **Tabu Search**: Memory prevents cycling and revisiting solutions

### Key Features:

- ✅ Handles CVRP without time windows
- ✅ Respects vehicle capacity constraints
- ✅ Configurable via YAML file
- ✅ Automatic solution quality comparison
- ✅ Comprehensive statistical analysis
- ✅ Reproducible results (random seed control)

## 📝 Solution Format

Solutions are saved in VRPLIB format for easy comparison:

```
Route #1: 1
Route #2: 8 5 3
Route #3: 9 12 10 6
Route #4: 11 4 7 2
Cost 247
```

## 🔍 Validation

The solver automatically:
- Verifies capacity constraints
- Compares with optimal solutions (if available)
- Calculates gap percentage
- Reports whether target gap (7%) is achieved

## 🛠️ Extending the Solver

### For CVRP with Time Windows:
After validating the CVRP solver, you can extend it to handle time windows by:
1. Adding time window constraints to feasibility checks
2. Incorporating time calculations in neighborhood operators
3. Penalizing time window violations in the objective function

### Adding New Neighborhoods:
1. Define the operator function following the existing pattern
2. Add it to the `neighborhoods` dictionary in VND
3. Include it in the `config.yaml` neighborhood list

## 📚 References

- **VRPLIB**: http://vrp.galgos.inf.puc-rio.br/index.php/en/
- **VRP Documentation**: See `vrplib.md` for format details
- **Test Instances**: Located in `data/` folder

## 🤝 Contributing

To improve the solver:
1. Run experiments with different parameter values
2. Test on various instance sizes
3. Compare results and update recommended config
4. Document findings in the analysis notebook

## 📄 License

This project is for academic and research purposes.

## ✨ Features Summary

- 🧩 Hybrid metaheuristic combining 4 optimization techniques
- 📦 Handles multiple VRP instance formats
- ⚡ Configurable parameters via YAML
- 📊 Statistical analysis and parameter tuning
- 💾 Automatic solution saving and comparison
- 📈 Comprehensive visualization
- 🎯 Target: ≤ 7% gap from optimal solutions

---

**Happy Optimizing! 🚛📦**

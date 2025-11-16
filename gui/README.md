# VRP GUI

A lightweight Tkinter GUI to run the CVRP CLI solver and visualize results.

Usage:

- Run GUI using Python:
```
python gui/vrp_gui.py
```

- Then select an instance from the data/ folder, press Run Selected, and click Show Routes & Cost to view the plots.

Notes:
- The GUI imports `cli.solve_cvrp.solve_cvrp`, `plot_routes`, `plot_cost_history`, and `save_solution`. Ensure that your `PYTHONPATH` includes the repo root (script already tries to add it). If `vrplib` is not installed, the solver will raise an error.
- Output is logged to the embedded console within the GUI.

Building an exe:
You can build a Windows exe of the GUI using the scripts in `tools/` with PyInstaller:

```powershell
.\tools\build_exe.ps1 -target gui
```

This will create a single-file exe in `dist\projectVRP-GUI.exe` that includes the `data/` and `config.yaml` resources.

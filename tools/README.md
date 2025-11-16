# Build executables (Windows)

This folder contains scripts to build Windows executables for the CLI and GUI using PyInstaller.

Prerequisites
- Activate the project's venv: `.venv\Scripts\Activate.ps1` (PowerShell)
- Install PyInstaller: `pip install pyinstaller`

Build
- GUI exe (single-file, windowed):

```
# PowerShell
.\build_exe.ps1 -target gui

# or batch
build_exe.bat gui
```

- CLI exe (single-file, console):

```
.\build_exe.ps1 -target cli
# or
build_exe.bat cli
```

Notes
- The scripts use `--add-data` to include `data/` and `config.yaml` so the exe can read instances and config.
- The code contains a `get_resource_path` helper to locate resources whether run from source or from a bundled exe.
- The output exe will be in `dist\projectVRP-GUI.exe` (GUI) or `dist\projectVRP-CLI.exe` (CLI).

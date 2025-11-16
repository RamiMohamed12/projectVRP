param (
    [string]$target = 'gui'
)

# Build executables with PyInstaller
# Usage: .\build_exe.ps1 -target gui | cli

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "PyInstaller not found. Installing in current venv..."
    python -m pip install pyinstaller
}

# Clean prior build
if (Test-Path dist) { Remove-Item -Recurse -Force dist }
if (Test-Path build) { Remove-Item -Recurse -Force build }
Get-ChildItem -Filter "*.spec" -Recurse | Remove-Item -Force

$baseWd = (Resolve-Path "..").Path
cd $baseWd

if ($target -eq 'gui') {
    $entry = 'gui\vrp_gui.py'
    $windowed = '--windowed'
    $name = 'projectVRP-GUI'
} else {
    $entry = 'cli\solve_cvrp.py'
    $windowed = ''
    $name = 'projectVRP-CLI'
}

# Add data and config to build
$addDataParams = @(
    "data;data",
    "config.yaml;."
)

# Build command
$addDataArgs = $addDataParams | ForEach-Object { "--add-data `"$_`"" }
$addDataStr = $addDataArgs -join ' '

$cmd = "pyinstaller --noconfirm --onefile $windowed --name $name $addDataStr $entry"
Write-Host "Running: $cmd"
Invoke-Expression $cmd

Write-Host "Build finished. Check dist\$name.exe"
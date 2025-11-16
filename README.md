# CVRP Solver – Approche Métaheuristique Hybride

Une solution complète pour résoudre les problèmes de routage de véhicules capacitaires (CVRP) en utilisant un algorithme métaheuristique hybride combinant la recherche locale, le Variable Neighborhood Descent (VND), le Recuit Simulé (SA) et la Recherche Tabou.

## 🎯 Objectif

Trouver des solutions de haute qualité pour des instances de CVRP sans fenêtres de temps, avec un écart maximum de 7 % par rapport à la solution optimale.

## 📁 Structure du Projet

```
projectVRP/
├── config.yaml                      # Configuration des paramètres de l'algorithme
├── cvrp_solver.ipynb               # Notebook principal du solveur CVRP
├── statistical_analysis.ipynb      # Analyse et réglage des paramètres
├── data/                           # Instances VRP et solutions optimales
│   ├── *.vrp                      # Instances au format VRPLIB
│   ├── *.sol                      # Solutions optimales
│   └── *.txt                      # Instances au format Solomon
├── solutions/                      # Résultats calculés
│   ├── *_computed.sol             # Solutions trouvées par l'algorithme
│   └── summary_results.csv        # Résumé de tous les résultats
└── analysis_results/               # Résultats d'analyse statistique
    ├── plots/                      # Graphiques de visualisation
    ├── csv/                        # Données d'expérience au format CSV
    └── recommended_config.yaml     # Configuration recommandée
```

## 🚀 Démarrage

### Prérequis

Installer les packages Python nécessaires :

```bash
pip install numpy vrplib pyyaml pandas matplotlib seaborn jupyter
```

### Lancement Rapide

1. **Exécuter le Solveur CVRP :**
   - Charger les instances CVRP depuis le dossier data
   - Appliquer l’algorithme métaheuristique hybride
   - Sauvegarder les solutions dans le dossier solutions
   - Comparer avec les solutions optimales et calculer les écarts

2. **Effectuer l’Analyse Statistique :**
   - Tester différentes configurations de paramètres
   - Générer des graphiques montrant l’impact des paramètres
   - Exporter les résultats au format CSV
   - Obtenir les valeurs de paramètres recommandées

## 🧮 Composants de l’Algorithme

### 1. Construction de la Solution Initiale
- Heuristique du Plus Proche Voisin
- Aléa configurable pour diversifier les solutions

### 2. Variable Neighborhood Descent (VND)
- Swap, Relocate, 2-opt, Cross-exchange

### 3. Recuit Simulé (SA)
- Acceptation probabiliste de solutions moins bonnes
- Échappe aux optima locaux
- Programme de refroidissement : T = T × α

### 4. Recherche Tabou
- Mémoire pour éviter les cycles
- Durée tabou dynamique avec randomisation
- Critère d’aspiration pour accepter les mouvements tabous

## ⚙️ Configuration

Modifier `config.yaml` pour ajuster les paramètres :

```yaml
simulated_annealing:
  initial_temperature: 1000.0
  final_temperature: 0.1
  alpha: 0.95
  iterations_per_temperature: 100

tabu_search:
  tabu_tenure: 20
  tabu_tenure_random_range: 10
  aspiration_enabled: true

vnd:
  neighborhoods:
    - swap
    - relocate
    - two_opt
    - cross_exchange
  max_iterations_without_improvement: 50

local_search:
  max_iterations: 1000
  max_iterations_without_improvement: 200

quality:
  target_gap_percentage: 7.0
```

## 📊 Analyse Statistique

- Tests d’impact de la température initiale, du taux de refroidissement, de la durée tabou et du nombre d’itérations
- Génération de graphiques et export CSV
- Configuration recommandée basée sur les expériences

## 📈 Résultats

- Fichiers de solution `.sol` et résumé CSV
- Visualisations : convergence du coût, sensibilité aux paramètres, distribution des écarts

## 🎓 Comprendre l’Algorithme

- Recherche Locale : amélioration rapide
- VND : exploration systématique
- Recuit Simulé : échappement aux optima locaux
- Recherche Tabou : évite les cycles

## 📝 Format des Solutions

```
Route #1: 1
Route #2: 8 5 3
Route #3: 9 12 10 6
Route #4: 11 4 7 2
Cost 247
```

## 🔍 Validation

- Vérification des contraintes de capacité
- Comparaison avec solutions optimales
- Calcul de l’écart en pourcentage
- Vérification de l’écart cible (7 %)

## 🛠️ Extension du Solveur

- CVRP avec fenêtres de temps : ajouter contraintes et pénalisation
- Nouveaux voisinages : définir fonction et ajouter au VND et config.yaml

## 📚 Références

- VRPLIB : http://vrp.galgos.inf.puc-rio.br/index.php/en/
- Documentation VRP : voir `vrplib.md`
- Instances de test : dossier `data/`

## 🤝 Contribution

- Expériences avec différents paramètres
- Test sur diverses tailles d’instances
- Comparaison et mise à jour de la config recommandée
- Documentation dans notebook d’analyse

## 📄 Licence

Projet à usage académique et recherche.

## ✨ Résumé des Fonctionnalités

- Métaheuristique hybride (4 techniques)
- Support multiples formats VRP
- Paramètres configurables via YAML
- Analyse statistique et tuning
- Sauvegarde et comparaison automatique
- Visualisation complète
- Objectif : ≤ 7 % d’écart par rapport à optimal

**Bonne optimisation ! 🚛📦**

## 🖥️ CLI (exécutable)

Le dossier `cli/` contient un script exécutable `solve_cvrp.py` qui reprend les fonctionnalités du notebook pour exécuter une instance depuis le terminal et produire des visualisations.

Exemples:

```
python cli/solve_cvrp.py --list
python cli/solve_cvrp.py --instance data/B-n31-k5.vrp --plot
```

## 🖥️ Simple GUI

There's a minimal GUI in `gui/vrp_gui.py` that offers a VS-Code-like quick run interface for the solver:

```
python gui/vrp_gui.py
```

The GUI lists instances in `data/`, lets you run the solver, capture console output, and visualize routes and cost history inside the app.

## 🧩 Build Windows executables (.exe)

You can package the CLI or the GUI into a single-file Windows executable using PyInstaller. This repository includes helper scripts under `tools/`.

1) Activate venv and install PyInstaller:

```powershell
.venv\Scripts\Activate.ps1
pip install pyinstaller
```

2) Build GUI exe:

```powershell
.\tools\build_exe.ps1 -target gui
```

3) Build CLI exe:

```powershell
.\tools\build_exe.ps1 -target cli
```

This produces a single executable in `dist\` (e.g., `dist\projectVRP-GUI.exe`). The build process includes the `data/` directory and `config.yaml` via PyInstaller `--add-data` flags and the code uses a resource helper to find these files when running from the bundled exe.
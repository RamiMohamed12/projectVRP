#!/usr/bin/env python3
"""
CLI CVRP Solver - Hybrid metaheuristic (port of cvrp_solver.ipynb)

Usage:
  python cli/solve_cvrp.py --instance data/B-n31-k5.vrp
  python cli/solve_cvrp.py --list
  python cli/solve_cvrp.py --instance data/B-n31-k5.vrp --plot

This script provides a CLI to run the algorithm and visualize the final routes and the cost-history.
"""

import argparse
import os
import random
import math
import time
from copy import deepcopy
from typing import List, Dict, Tuple, Optional
import yaml
import sys
import numpy as np
import matplotlib.pyplot as plt

# Try import vrplib
try:
    import vrplib
except Exception:
    print("Warning: vrplib not available. Please install vrplib for reading instances.")
    vrplib = None

# Load config.yaml (we expect config.yaml in the repository root)
def get_resource_path(rel_path: str) -> str:
    """Return absolute path to a resource, whether running from source or from a PyInstaller bundle."""
    if getattr(sys, 'frozen', False):
        # PyInstaller places data into a temporary folder and sets _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(base_path, rel_path) if rel_path else base_path

# Load config.yaml (we expect config.yaml in the repository root)
CONFIG_PATH = get_resource_path('config.yaml')
with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

random.seed(config['general']['random_seed'])
np.random.seed(config['general']['random_seed'])

# Data and helper classes
class CVRPSolution:
    def __init__(self, routes: List[List[int]], distance_matrix: np.ndarray):
        self.routes = routes
        self.distance_matrix = distance_matrix
        self.cost = self.calculate_cost()

    def calculate_cost(self) -> float:
        total_cost = 0.0
        for route in self.routes:
            if len(route) == 0:
                continue
            total_cost += self.distance_matrix[0, route[0]]
            for i in range(len(route) - 1):
                total_cost += self.distance_matrix[route[i], route[i+1]]
            total_cost += self.distance_matrix[route[-1], 0]
        return float(total_cost)

    def update_cost(self):
        self.cost = self.calculate_cost()

    def is_feasible(self, demands: np.ndarray, capacity: int) -> bool:
        for route in self.routes:
            route_demand = sum(demands[c] for c in route)
            if route_demand > capacity:
                return False
        return True

    def copy(self):
        return CVRPSolution([r.copy() for r in self.routes], self.distance_matrix)


def calculate_distance_matrix(instance: Dict) -> np.ndarray:
    if 'edge_weight' in instance:
        return instance['edge_weight']
    elif 'node_coord' in instance:
        coords = np.array(instance['node_coord'])
        n = len(coords)
        dist_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    dist_matrix[i, j] = math.sqrt(((coords[i] - coords[j])**2).sum())
        return dist_matrix
    else:
        raise ValueError("Instance must have either 'edge_weight' or 'node_coord'")


def nearest_neighbor_solution(instance: Dict, distance_matrix: np.ndarray) -> CVRPSolution:
    n_customers = instance['dimension'] - 1
    capacity = instance['capacity']
    demands = np.array(instance['demand'])

    unvisited = set(range(1, n_customers + 1))
    routes = []

    while unvisited:
        route = []
        current_load = 0
        current_node = 0
        while True:
            best_customer = None
            best_distance = float('inf')
            for customer in list(unvisited):
                if current_load + demands[customer] <= capacity:
                    dist = distance_matrix[current_node, customer]
                    randomness = config['initial_solution'].get('randomness', 0.0)
                    dist *= (1 + randomness * random.random())
                    if dist < best_distance:
                        best_distance = dist
                        best_customer = customer
            if best_customer is None:
                break
            route.append(best_customer)
            current_load += demands[best_customer]
            current_node = best_customer
            unvisited.remove(best_customer)
        if route:
            routes.append(route)
    return CVRPSolution(routes, distance_matrix)

# Neighborhood operators (swap, relocate, 2-opt, cross-exchange)
def swap_operator(solution: CVRPSolution, demands: np.ndarray, capacity: int) -> Optional[CVRPSolution]:
    if len(solution.routes) < 2:
        return None
    best_solution = None
    best_cost = solution.cost
    for i in range(len(solution.routes)):
        for j in range(i + 1, len(solution.routes)):
            route_i = solution.routes[i]
            route_j = solution.routes[j]
            if len(route_i) == 0 or len(route_j) == 0:
                continue
            for pos_i in range(len(route_i)):
                for pos_j in range(len(route_j)):
                    new_solution = solution.copy()
                    new_solution.routes[i][pos_i], new_solution.routes[j][pos_j] = new_solution.routes[j][pos_j], new_solution.routes[i][pos_i]
                    if new_solution.is_feasible(demands, capacity):
                        new_solution.update_cost()
                        if new_solution.cost < best_cost:
                            best_cost = new_solution.cost
                            best_solution = new_solution
    return best_solution


def relocate_operator(solution: CVRPSolution, demands: np.ndarray, capacity: int) -> Optional[CVRPSolution]:
    best_solution = None
    best_cost = solution.cost
    for i in range(len(solution.routes)):
        route_i = solution.routes[i]
        if len(route_i) == 0:
            continue
        for pos_i in range(len(route_i)):
            customer = route_i[pos_i]
            for j in range(len(solution.routes)):
                if i == j:
                    continue
                for pos_j in range(len(solution.routes[j]) + 1):
                    new_solution = solution.copy()
                    removed = new_solution.routes[i].pop(pos_i)
                    new_solution.routes[j].insert(pos_j, removed)
                    if new_solution.is_feasible(demands, capacity):
                        new_solution.update_cost()
                        if new_solution.cost < best_cost:
                            best_cost = new_solution.cost
                            best_solution = new_solution
    return best_solution


def two_opt_operator(solution: CVRPSolution, demands: np.ndarray, capacity: int) -> Optional[CVRPSolution]:
    best_solution = None
    best_cost = solution.cost
    for route_idx in range(len(solution.routes)):
        route = solution.routes[route_idx]
        if len(route) < 2:
            continue
        for i in range(len(route) - 1):
            for j in range(i + 1, len(route)):
                new_solution = solution.copy()
                new_solution.routes[route_idx][i:j+1] = list(reversed(new_solution.routes[route_idx][i:j+1]))
                new_solution.update_cost()
                if new_solution.cost < best_cost:
                    best_cost = new_solution.cost
                    best_solution = new_solution
    return best_solution


def cross_exchange_operator(solution: CVRPSolution, demands: np.ndarray, capacity: int) -> Optional[CVRPSolution]:
    if len(solution.routes) < 2:
        return None
    best_solution = None
    best_cost = solution.cost
    for i in range(len(solution.routes)):
        for j in range(i + 1, len(solution.routes)):
            route_i = solution.routes[i]
            route_j = solution.routes[j]
            if len(route_i) < 2 or len(route_j) < 2:
                continue
            for seg_len in [1, 2]:
                for pos_i in range(len(route_i) - seg_len + 1):
                    for pos_j in range(len(route_j) - seg_len + 1):
                        new_solution = solution.copy()
                        seg_i = new_solution.routes[i][pos_i:pos_i+seg_len]
                        seg_j = new_solution.routes[j][pos_j:pos_j+seg_len]
                        new_solution.routes[i][pos_i:pos_i+seg_len] = seg_j
                        new_solution.routes[j][pos_j:pos_j+seg_len] = seg_i
                        if new_solution.is_feasible(demands, capacity):
                            new_solution.update_cost()
                            if new_solution.cost < best_cost:
                                best_cost = new_solution.cost
                                best_solution = new_solution
    return best_solution


# VND

def vnd(solution: CVRPSolution, demands: np.ndarray, capacity: int) -> CVRPSolution:
    neighborhoods = {
        'swap': swap_operator,
        'relocate': relocate_operator,
        'two_opt': two_opt_operator,
        'cross_exchange': cross_exchange_operator
    }
    neighborhood_order = config['vnd']['neighborhoods']
    max_no_improve = config['vnd']['max_iterations_without_improvement']
    current_solution = solution
    k = 0
    no_improve_count = 0
    while k < len(neighborhood_order) and no_improve_count < max_no_improve:
        neighborhood_name = neighborhood_order[k]
        operator = neighborhoods[neighborhood_name]
        new_solution = operator(current_solution, demands, capacity)
        if new_solution is not None and new_solution.cost < current_solution.cost:
            current_solution = new_solution
            k = 0
            no_improve_count = 0
        else:
            k += 1
            no_improve_count += 1
    return current_solution


# Tabu list
class TabuList:
    def __init__(self, tenure: int):
        self.tenure = tenure
        self.tabu_dict = {}
        self.current_iteration = 0

    def add(self, move: Tuple, tenure_variation: int = 0):
        actual_tenure = self.tenure + random.randint(-tenure_variation, tenure_variation)
        self.tabu_dict[move] = self.current_iteration + actual_tenure

    def is_tabu(self, move: Tuple) -> bool:
        if move not in self.tabu_dict:
            return False
        return self.tabu_dict[move] > self.current_iteration

    def increment_iteration(self):
        self.current_iteration += 1
        expired = [move for move, expiration in self.tabu_dict.items() if expiration <= self.current_iteration]
        for move in expired:
            del self.tabu_dict[move]


def acceptance_probability(current_cost: float, new_cost: float, temperature: float) -> float:
    if new_cost < current_cost:
        return 1.0
    return math.exp((current_cost - new_cost) / temperature)


def simulated_annealing_with_tabu(initial_solution: CVRPSolution, demands: np.ndarray, capacity: int, time_limit: float = None) -> Tuple[CVRPSolution, List[float], List[float]]:
    temp = config['simulated_annealing']['initial_temperature']
    final_temp = config['simulated_annealing']['final_temperature']
    alpha = config['simulated_annealing']['alpha']
    iterations_per_temp = config['simulated_annealing']['iterations_per_temperature']
    tabu_tenure = config['tabu_search']['tabu_tenure']
    tabu_tenure_variation = config['tabu_search']['tabu_tenure_random_range']
    aspiration_enabled = config['tabu_search']['aspiration_enabled']
    max_iterations = config['local_search']['max_iterations']
    max_no_improve = config['local_search']['max_iterations_without_improvement']

    current_solution = initial_solution
    best_solution = current_solution.copy()
    tabu_list = TabuList(tabu_tenure)
    cost_history = [best_solution.cost]  # best-so-far improvement history
    iter_cost_history = [current_solution.cost]  # cost at each iteration (for convergence plot)
    no_improve_count = 0
    total_iterations = 0
    start_time = time.time()

    operators = [swap_operator, relocate_operator, two_opt_operator, cross_exchange_operator]

    while temp > final_temp and total_iterations < max_iterations:
        if time_limit and (time.time() - start_time) > time_limit:
            break
        if no_improve_count >= max_no_improve:
            break
        for _ in range(iterations_per_temp):
            if total_iterations % 50 == 0:
                current_solution = vnd(current_solution, demands, capacity)

            operator = random.choice(operators)
            new_solution = operator(current_solution, demands, capacity)
            if new_solution is None:
                continue
            move_id = (operator.__name__, hash(str(new_solution.routes)))
            is_tabu = tabu_list.is_tabu(move_id)
            aspiration = aspiration_enabled and new_solution.cost < best_solution.cost
            if (not is_tabu or aspiration):
                if random.random() < acceptance_probability(current_solution.cost, new_solution.cost, temp):
                    current_solution = new_solution
                    tabu_list.add(move_id, tabu_tenure_variation)
                    # append at acceptance
                    iter_cost_history.append(current_solution.cost)
                    if current_solution.cost < best_solution.cost:
                        best_solution = current_solution.copy()
                        cost_history.append(best_solution.cost)
                        no_improve_count = 0
                        if config['general']['verbose']:
                            print(f"  Nouveau meilleur : {best_solution.cost:.2f} à l'itération {total_iterations}")
                    else:
                        no_improve_count += 1
            tabu_list.increment_iteration()
            # track cost at every iteration (append current solution cost)
            iter_cost_history.append(current_solution.cost)
            total_iterations += 1
        temp *= alpha

    return best_solution, cost_history, iter_cost_history


# Solve function

def solve_cvrp(instance_path: str, time_limit_override: Optional[float] = None) -> Dict:
    print('\n' + '=' * 60)
    print(f"Résolution : {os.path.basename(instance_path)}")
    print('=' * 60)

    if vrplib:
        try:
            instance = vrplib.read_instance(instance_path)
        except Exception:
            instance = vrplib.read_instance(instance_path, instance_format='solomon')
    else:
        raise RuntimeError('vrplib is required to read instances; install vrplib or place a parser here')

    distance_matrix = calculate_distance_matrix(instance)
    demands = np.array(instance['demand'])
    capacity = instance['capacity']

    print(f"Dimension : {instance['dimension']} nœuds")
    print(f"Capacité : {capacity}\n")

    print("Création de la solution initiale...")
    initial_solution = nearest_neighbor_solution(instance, distance_matrix)
    print(f"Coût initial : {initial_solution.cost:.2f}")
    print(f"Itinéraires initiaux : {len(initial_solution.routes)}\n")

    print("Application de VND...")
    improved_solution = vnd(initial_solution, demands, capacity)
    print(f"Coût après VND : {improved_solution.cost:.2f}\n")

    print("Application du Recuit Simulé avec Recherche Tabou...\n")
    time_limit = time_limit_override if time_limit_override is not None else config['general'].get('time_limit_seconds')
    start_time = time.time()
    final_solution, cost_history, iter_cost_history = simulated_annealing_with_tabu(improved_solution, demands, capacity, time_limit)
    elapsed_time = time.time() - start_time

    print(f"Coût final : {final_solution.cost:.2f}")
    print(f"Itinéraires finaux : {len(final_solution.routes)}")
    print(f"Temps écoulé : {elapsed_time:.2f} secondes\n")

    optimal_cost = None
    gap_percentage = None

    sol_path = instance_path.replace('.vrp', '.sol').replace('.txt', '.sol')
    if os.path.exists(sol_path):
        try:
            optimal_solution = vrplib.read_solution(sol_path)
            optimal_cost = optimal_solution['cost']
            gap_percentage = ((final_solution.cost - optimal_cost) / optimal_cost) * 100.0
            print(f"Coût optimal : {optimal_cost:.2f}")
            print(f"Écart : {gap_percentage:.2f}%")
            if gap_percentage <= config['quality']['target_gap_percentage']:
                print(f"✓ Solution dans l'écart cible de {config['quality']['target_gap_percentage']}%")
            else:
                print(f"✗ Solution dépasse l'écart cible de {config['quality']['target_gap_percentage']}%")
        except Exception as e:
            print(f"Impossible de lire la solution optimale : {e}")

    return {
        'instance_name': os.path.basename(instance_path),
        'solution': final_solution,
        'cost': final_solution.cost,
        'optimal_cost': optimal_cost,
        'gap_percentage': gap_percentage,
        'n_routes': len(final_solution.routes),
        'time_seconds': elapsed_time,
        'cost_history': cost_history,
        'iter_cost_history': iter_cost_history,
        'instance': instance
    }


def save_solution(result: Dict, output_dir: str = 'solutions') -> str:
    os.makedirs(output_dir, exist_ok=True)
    instance_name = result['instance_name'].replace('.vrp', '').replace('.txt', '')
    output_path = os.path.join(output_dir, f"{instance_name}_computed.sol")
    routes = result['solution'].routes
    with open(output_path, 'w') as f:
        for idx, route in enumerate(routes, 1):
            route_str = ' '.join(map(str, route))
            f.write(f"Route #{idx}: {route_str}\n")
        f.write(f"Cost {result['cost']:.0f}\n")
    print(f"Solution sauvegardée dans : {output_path}")
    return output_path


# Visualization functions

def plot_routes(result: Dict, show: bool = True, save_path: Optional[str] = None):
    instance = result['instance']
    routes = result['solution'].routes
    coords = np.array(instance['node_coord'])
    depot = coords[0]

    plt.figure(figsize=(8, 8))
    for idx, route in enumerate(routes):
        if len(route) == 0:
            continue
        route_coords = [depot] + [coords[c] for c in route] + [depot]
        xs = [p[0] for p in route_coords]
        ys = [p[1] for p in route_coords]
        plt.plot(xs, ys, marker='o', label=f'Route {idx+1}')
    plt.scatter(depot[0], depot[1], c='k', marker='s', s=80, label='Depot')
    plt.title(f"Routes - {result['instance_name']} (Cost: {result['cost']:.2f})")
    plt.legend()
    plt.axis('equal')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close()


def plot_cost_history(result: Dict, show: bool = True, save_path: Optional[str] = None):
    history = result.get('iter_cost_history') or result.get('cost_history')
    if not history:
        print('No cost history to plot')
        return
    plt.figure(figsize=(8, 4))
    plt.plot(history, marker='o')
    plt.xlabel('Improvement step')
    plt.ylabel('Cost')
    plt.title(f"Cost history - {result['instance_name']}")
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close()


# CLI

def list_instances(data_dir: str = 'data') -> List[str]:
    paths = []
    # If a relative directory is passed, resolve against resource path (useful for bundled exe)
    if not os.path.isabs(data_dir):
        data_dir = get_resource_path(data_dir)
    if os.path.exists(data_dir):
        for root, dirs, files in os.walk(data_dir):
            for f in files:
                if f.endswith('.vrp'):
                    paths.append(os.path.join(root, f))
    return sorted(paths)


# Main

def main():
    parser = argparse.ArgumentParser(description='CVRP CLI solver (hybrid metaheuristic)')
    parser.add_argument('--instance', '-i', help='Path to .vrp instance file', default=None)
    parser.add_argument('--plot', action='store_true', help='Show plots (routes + cost history)')
    parser.add_argument('--list', action='store_true', help='List available .vrp instances in data/')
    parser.add_argument('--no-save', action='store_true', help='Do not save computed solution')
    args = parser.parse_args()

    if args.list:
        instances = list_instances()
        print('Available .vrp instances:')
        for inst in instances:
            print('  -', inst)
        return

    inst_path = args.instance
    if inst_path is None:
        instances = list_instances()
        if not instances:
            print('No .vrp instances found in data/ folder.')
            return
        print('Select an instance (enter number):')
        for idx, inst in enumerate(instances):
            print(f" {idx+1:2d}. {inst}")
        sel = input('Instance number: ')
        try:
            sel_idx = int(sel.strip()) - 1
            inst_path = instances[sel_idx]
        except Exception:
            print('Invalid selection')
            return

    result = solve_cvrp(inst_path)

    if not args.no_save:
        save_solution(result)

    if args.plot:
        out_dir = 'plots'
        os.makedirs(out_dir, exist_ok=True)
        route_plot = os.path.join(out_dir, f"{result['instance_name']}_routes.png")
        hist_plot = os.path.join(out_dir, f"{result['instance_name']}_cost_history.png")
        plot_routes(result, save_path=route_plot)
        plot_cost_history(result, save_path=hist_plot)


if __name__ == '__main__':
    main()

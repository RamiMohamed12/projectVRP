"""
VRP GUI - a simple Tkinter app to run the CLI solver and visualize results

Features:
- List instances in data/ and let user pick
- Run solver in background thread while capturing stdout
- Show final route on a Matplotlib figure
- Show cost history per-iteration or best improvements
- Save computed solution and plots
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import time
from typing import Optional

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Add repo root or bundled resource base to sys.path so we can import CLI solver
def get_resource_base():
    if getattr(sys, 'frozen', False):
        return getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ROOT = get_resource_base()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Import the CLI solver functions
try:
    from cli.solve_cvrp import list_instances, solve_cvrp, plot_routes, plot_cost_history, save_solution
except Exception:
    # If we cannot import, define placeholders
    list_instances = None
    def solve_cvrp(instance_path):
        raise RuntimeError('Cannot import solver. Run pip install -e . or ensure repo root is in PYTHONPATH')
    def plot_routes(*a, **k):
        pass
    def plot_cost_history(*a, **k):
        pass
    def save_solution(*a, **k):
        pass


# Redirect stdout/stderr to Tk Text
class TextRedirect:
    def __init__(self, text_widget: ScrolledText):
        self.text_widget = text_widget

    def write(self, s: str):
        # append text to the widget; schedule on main thread
        def append():
            self.text_widget.insert(tk.END, s)
            self.text_widget.see(tk.END)
        self.text_widget.after(1, append)

    def flush(self):
        pass


class VRPGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('CVRP GUI - Hybrid Metaheuristic')
        self.geometry('1100x680')

        # UI layout
        self.left_frame = ttk.Frame(self, width=300)
        self.right_frame = ttk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Instances list in left frame
        ttk.Label(self.left_frame, text='Instances (data/):').pack(anchor=tk.W)
        self.instances_listbox = tk.Listbox(self.left_frame, height=20)
        self.instances_listbox.pack(fill=tk.BOTH, expand=True)

        self.refresh_btn = ttk.Button(self.left_frame, text='Refresh', command=self.refresh_instances)
        self.refresh_btn.pack(fill=tk.X, pady=4)

        self.run_btn = ttk.Button(self.left_frame, text='Run Selected', command=self.run_selected)
        self.run_btn.pack(fill=tk.X, pady=4)

        self.plot_btn = ttk.Button(self.left_frame, text='Show Routes & Cost', command=self.plot_selected)
        self.plot_btn.pack(fill=tk.X, pady=4)

        self.save_btn = ttk.Button(self.left_frame, text='Save Last Solution', command=self.save_last_solution)
        self.save_btn.pack(fill=tk.X, pady=4)

        # Controls: time limit and toggle save
        ttk.Label(self.left_frame, text='Options').pack(anchor=tk.W, pady=(6, 0))
        self.time_limit_var = tk.StringVar(value='None')
        ttk.Label(self.left_frame, text='Time limit (s):').pack(anchor=tk.W)
        self.time_limit_entry = ttk.Entry(self.left_frame, textvariable=self.time_limit_var)
        self.time_limit_entry.pack(fill=tk.X, padx=2)

        self.no_save_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.left_frame, text='Do not save solution', variable=self.no_save_var).pack(anchor=tk.W, pady=4)

        # Right frame: top area for Matplotlib figures; bottom area for logs
        self.figure_frame = ttk.Frame(self.right_frame)
        self.figure_frame.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.figure_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.log_frame = ttk.LabelFrame(self.right_frame, text='Console')
        self.log_frame.pack(fill=tk.BOTH, expand=False, pady=8)
        self.log_text = ScrolledText(self.log_frame, height=12, state=tk.NORMAL)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Restore stdout/stderr
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = TextRedirect(self.log_text)
        sys.stderr = TextRedirect(self.log_text)

        self.last_result = None
        self.solver_thread = None
        self.refresh_instances()

    def refresh_instances(self):
        self.instances_listbox.delete(0, tk.END)
        try:
            # Use an absolute path to the data directory relative to repo root
            data_dir = os.path.join(ROOT, 'data')  # ROOT is resource base (handles packaged exe)
            insts = list_instances(data_dir) if list_instances else []
            # If list_instances returns absolute paths, show relative ones for readability
            rel_insts = [os.path.relpath(p, ROOT) for p in insts]
            insts_to_show = rel_insts
            # If there are no instances found in the provided directory, try data under repo root as fallback
            if not insts:
                # Try the repo relative path
                fallback_dir = os.path.join(os.getcwd(), 'data')
                if fallback_dir != data_dir and os.path.exists(fallback_dir):
                    insts = list_instances(fallback_dir) if list_instances else []
                    rel_insts = [os.path.relpath(p, ROOT) for p in insts]
                    insts_to_show = rel_insts
        
            if not insts_to_show:
                self.instances_listbox.insert(tk.END, '(No .vrp instances found in data/)')
            else:
                for p in insts_to_show:
                    self.instances_listbox.insert(tk.END, p)
        except Exception as e:
            messagebox.showerror('Error listing instances', str(e))

    def get_selected_instance(self) -> Optional[str]:
        sel = self.instances_listbox.curselection()
        if not sel:
            return None
        entry = self.instances_listbox.get(sel[0])
        # If the entry is the no-instances placeholder, return None
        if entry.startswith('(') and 'No .vrp' in entry:
            return None
        # If entry is already absolute, return it
        if os.path.isabs(entry):
            return entry
        # Otherwise, assume it's relative to repo ROOT and return absolute path
        return os.path.join(ROOT, entry)

    def run_selected(self):
        inst = self.get_selected_instance()
        if not inst:
            messagebox.showinfo('Select instance', 'Please select a .vrp instance from the list')
            return
        # Validate that the selected path exists
        if not os.path.exists(inst):
            messagebox.showerror('Instance not found', f"Instance file not found: {inst}")
            return
        if self.solver_thread and self.solver_thread.is_alive():
            messagebox.showwarning('Solver running', 'A solver is currently running. Please wait')
            return

        # Prepare time limit
        time_limit = None
        tl = self.time_limit_var.get().strip()
        if tl.lower() not in ('none', ''):
            try:
                time_limit = float(tl)
            except Exception:
                messagebox.showerror('Invalid time limit', 'Time limit must be a number (seconds)')
                return

        # Show the relative path in logs for readability
        rel_path = os.path.relpath(inst, ROOT)
        self.log_text.insert(tk.END, f"\nStarting solver for {rel_path}...\n")
        self.log_text.see(tk.END)

        def worker():
            try:
                # Use CLI solver and pass time_limit override if provided
                res = solve_cvrp(inst, time_limit_override=time_limit)
                self.last_result = res
                # Save based on checkbox
                if not self.no_save_var.get():
                    save_solution(res)
                self.log_text.insert(tk.END, '\nSolver finished.\n')
            except Exception as e:
                self.log_text.insert(tk.END, f"Solver error: {e}\n")

        self.solver_thread = threading.Thread(target=worker, daemon=True)
        self.solver_thread.start()

    def plot_selected(self):
        if not self.last_result:
            messagebox.showinfo('No solution', 'No computed solution to plot. Run a solver first.')
            return
        # Clear figure
        self.fig.clf()
        # Make a routes plot
        try:
            # The CLI's plot functions call plt.show(); instead we generate two subplots locally
            inst = self.last_result['instance']
            routes = self.last_result['solution'].routes
            coords = inst['node_coord']
            ax1 = self.fig.add_subplot(121)
            depot = coords[0]
            ax1.set_title('Routes')
            for idx, route in enumerate(routes):
                if len(route) == 0:
                    continue
                route_coords = [depot] + [coords[c] for c in route] + [depot]
                xs = [p[0] for p in route_coords]
                ys = [p[1] for p in route_coords]
                ax1.plot(xs, ys, marker='o', label=f'Route {idx+1}')
            ax1.scatter(depot[0], depot[1], c='k', marker='s', s=80, label='Depot')
            ax1.legend(fontsize='small')
            ax1.axis('equal')

            # Cost history
            ax2 = self.fig.add_subplot(122)
            history = self.last_result.get('iter_cost_history') or self.last_result.get('cost_history')
            if history:
                ax2.plot(history, marker='o')
                ax2.set_title('Cost history')
                ax2.set_xlabel('Iteration')
                ax2.set_ylabel('Cost')
            else:
                ax2.text(0.5, 0.5, 'No cost history', ha='center')

            self.canvas.draw()
        except Exception as e:
            messagebox.showerror('Plot error', str(e))

    def save_last_solution(self):
        if not self.last_result:
            messagebox.showinfo('No solution', 'No computed solution to save. Run a solver first.')
            return
        # Save to folder (save_solution already writes to solutions/)
        try:
            out = save_solution(self.last_result)
            messagebox.showinfo('Saved', f'Solution saved to {out}')
        except Exception as e:
            messagebox.showerror('Save error', str(e))

    def on_closing(self):
        # restore stdout
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        self.destroy()


if __name__ == '__main__':
    app = VRPGUI()
    app.protocol('WM_DELETE_WINDOW', app.on_closing)
    app.mainloop()

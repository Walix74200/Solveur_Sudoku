import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, OptionMenu, StringVar, Scale, HORIZONTAL, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import psutil
import sys

# Charger les grilles avec et sans solutions depuis les fichiers CSV pour chaque niveau de difficulté
grilles_facile_sans_rep = pd.read_csv('grilles_facile_sans_rep.csv')
grilles_facile_avec_rep = pd.read_csv('grilles_facile_avec_rep.csv')

# Fonction pour convertir une chaîne de caractères en matrice NumPy
def string_to_matrix(sudoku_string):
    return np.array([int(char) if char != '.' else 0 for char in sudoku_string]).reshape(9, 9)

# Classe qui gère la résolution de Sudoku avec ou sans visualisation
class SudokuSolver:
    def __init__(self, board, viewer):
        self.board = board
        self.viewer = viewer
        self.history = [np.copy(self.board)]  # Stocke l'historique des étapes, avec l'état initial
        self.attempt_counter = 0  # Initialisation du compteur de cases écrites ou générées
        self.backtrack_counter = 0  # Compteur du nombre de fois où le backtracking est appelé
        self.recursive_calls = 0  # Counter for recursive calls
        self.node_expansions = 0  # Node expansions in the search tree
        self.max_depth = 0  # Maximum search depth
        self.current_depth = 0  # Current recursion depth
        self.total_branching_factor = 0  # Sum of all branching factors
        self.branching_points = 0  # Count of decision points (to calculate average)
        self.constraint_propagations = 0  # Count constraint propagation checks
        self.memory_usage = 0  # Memory usage

    def get_valid_numbers(self, row, col):
        if self.board[row, col] != 0:
            return set()

        possible_numbers = set(range(1, 10))
        possible_numbers -= set(self.board[row, :])
        possible_numbers -= set(self.board[:, col])

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        possible_numbers -= set(self.board[start_row:start_row + 3, start_col:start_col + 3].flatten())

        return possible_numbers

    def find_most_constrained_location(self):
        empty_positions = np.argwhere(self.board == 0)
        if empty_positions.size == 0:
            return None

        min_options = 10
        best_position = None

        for pos in empty_positions:
            row, col = pos
            valid_numbers = self.get_valid_numbers(row, col)
            num_options = len(valid_numbers)
            
            # Track constraint propagation efficiency
            self.constraint_propagations += 1
            self.total_branching_factor += num_options
            self.branching_points += 1
            
            if num_options < min_options:
                min_options = num_options
                best_position = (row, col)

        return best_position

    def solve_sudoku_detailed(self):
        self.recursive_calls += 1
        self.node_expansions += 1
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)

        empty = self.find_most_constrained_location()
        if not empty:
            self.current_depth -= 1
            return True

        row, col = empty

        self.viewer.highlight_cell(row, col)
        self.viewer.root.update()

        for num in self.get_valid_numbers(row, col):
            if self.viewer.paused:
                while self.viewer.paused and not self.viewer.step_forward:
                    self.viewer.root.update()
                    time.sleep(0.1)

            self.history.append(np.copy(self.board))

            self.board[row][col] = num
            self.attempt_counter += 1  # Incrémentation du compteur de cases écrites ou générées
            self.viewer.update_attempt_counter(self.attempt_counter)
            self.viewer.update_grid(self.board, row, col, color="blue")
            self.viewer.root.update()

            if self.viewer.step_forward:
                self.viewer.step_forward = False
                self.current_depth -= 1
                return False

            time.sleep(self.viewer.speed_scale.get() / 1000)

            if self.solve_sudoku_detailed():
                self.current_depth -= 1
                return True

            self.viewer.update_grid(self.board, row, col, color="red")
            self.viewer.root.update()

            time.sleep(self.viewer.speed_scale.get() / 1000)

            self.history.append(np.copy(self.board))

            self.board[row][col] = 0
            self.viewer.update_grid(self.board)
            self.viewer.root.update()

            self.backtrack_counter += 1  # Incrémentation du compteur de backtracking
            self.viewer.update_backtrack_counter(self.backtrack_counter)

            time.sleep(self.viewer.speed_scale.get() / 1000)

        self.current_depth -= 1
        return False

    def solve_sudoku(self):
        """Résout la grille sans visualisation."""
        self.recursive_calls += 1
        self.node_expansions += 1
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)

        empty = self.find_most_constrained_location()
        if not empty:
            self.current_depth -= 1
            return True

        row, col = empty
        for num in self.get_valid_numbers(row, col):
            self.board[row][col] = num
            self.attempt_counter += 1  # Incrémentation du compteur de cases écrites ou générées
            self.viewer.update_attempt_counter(self.attempt_counter)
            if self.solve_sudoku():
                self.current_depth -= 1
                return True
            self.board[row][col] = 0  # Backtracking

            self.backtrack_counter += 1  # Incrémentation du compteur de backtracking
            self.viewer.update_backtrack_counter(self.backtrack_counter)

        self.current_depth -= 1
        return False

    def undo_step(self):
        """Annuler le dernier pas."""
        if len(self.history) > 1:
            # Remove the current state and revert to the previous one
            self.history.pop()
            previous_board = self.history[-1]

            # Find the difference between the current and previous board to know which cell was cleared
            difference = self.board != previous_board
            affected_cell = np.argwhere(difference)

            # Update the board to the previous state
            self.board = np.copy(previous_board)
            self.viewer.update_grid(self.board)

            # If a cell was changed, highlight it in red (backtracking color)
            if len(affected_cell) > 0:
                row, col = affected_cell[0]
                self.viewer.update_grid(self.board, row, col, color="red")
                print(f"Cell ({row}, {col}) cleared")

            # Decrement the attempt counter and update
            self.attempt_counter -= 1
            self.viewer.update_attempt_counter(self.attempt_counter)


    def calculate_memory_usage(self):
        """Calculates the memory used by the current process."""
        process = psutil.Process()
        self.memory_usage = process.memory_info().rss / 1024 ** 2  # Convert to MB

    def get_average_branching_factor(self):
        if self.branching_points > 0:
            return self.total_branching_factor / self.branching_points
        return 0

# Application Tkinter
class SudokuViewer:
    def __init__(self, root):
        self.root = root
        self.index = 0
        self.level = 'Facile'
        self.grilles_sans_rep = grilles_facile_sans_rep
        self.grilles_avec_rep = grilles_facile_avec_rep
        self.paused = False
        self.step_forward = False
        self.solver = None

        sudoku_string = self.grilles_sans_rep['puzzle'].iloc[self.index]
        self.sudoku_matrix = string_to_matrix(sudoku_string)
        self.fixed_values = np.where(self.sudoku_matrix != 0, True, False)

        self.create_widgets()

    def create_widgets(self):
        # Frame for top control buttons (play, pause, speed)
        control_frame_top = Frame(self.root)
        control_frame_top.pack(side="top", pady=10)

        # Play button (pack on the left side)
        self.play_button = Button(control_frame_top, text="Play", command=self.play_solver)
        self.play_button.pack(side="left", padx=5)

        # Speed control (pack in the middle)
        self.speed_scale = Scale(control_frame_top, from_=0.1, to=1000, resolution=0.1, orient=HORIZONTAL, label="Vitesse (ms)")
        self.speed_scale.set(300)
        self.speed_scale.pack(side="left", expand=True, fill="x", padx=5)

        # Pause button (pack on the right side)
        self.pause_button = Button(control_frame_top, text="Pause", command=self.pause_solver)
        self.pause_button.pack(side="left", padx=5)

        # Frame for navigation buttons (to switch between puzzles) on the left
        control_frame_left = Frame(self.root)
        control_frame_left.pack(side="left", padx=10)

        # OptionMenu for difficulty level selection
        self.level_var = StringVar(self.root)
        self.level_var.set(self.level)  # Default value for the level

        # Add OptionMenu widget for selecting difficulty
        self.level_menu = OptionMenu(control_frame_left, self.level_var, "Facile", "Moyen", "Difficile", command=self.update_level)
        self.level_menu.pack(pady=10)  # Add it above the navigation buttons

        # Navigation buttons (Précédent, Suivant)
        self.prev_button = Button(control_frame_left, text="Précédent", command=self.prev_sudoku)
        self.prev_button.pack(pady=5)

        self.next_button = Button(control_frame_left, text="Suivant", command=self.next_sudoku)
        self.next_button.pack(pady=5)

        # Frame for step buttons on the right (advance and undo steps)
        control_frame_right = Frame(self.root)
        control_frame_right.pack(side="right", padx=10)

        self.prev_step_button = Button(control_frame_right, text="Étape Précédente", command=self.undo_step_solver)
        self.prev_step_button.pack(pady=5)

        self.next_step_button = Button(control_frame_right, text="Étape Suivante", command=self.advance_step)
        self.next_step_button.pack(pady=5)

        # Frame for the Sudoku grid
        self.canvas_frame = Frame(self.root)
        self.canvas_frame.pack(side="top", pady=10)

        # Frame for bottom control buttons (solve)
        control_frame_bottom = Frame(self.root)
        control_frame_bottom.pack(side="bottom", pady=10)

        self.solve_button = Button(control_frame_bottom, text="Résoudre", command=self.solve_current_sudoku)
        self.solve_button.pack(pady=5)

        self.solve_detailed_button = Button(control_frame_bottom, text="Résolution Détaillée", command=self.solve_detailed)
        self.solve_detailed_button.pack(pady=5)

        self.verification_label = Label(self.root, text="", fg="blue")
        self.verification_label.pack()

        # Counters displayed on the right side of the window
        self.attempt_counter_label = Label(self.root, text="Nombre de cases écrites ou générées : 0", fg="black")
        self.attempt_counter_label.pack(side="right", padx=5)

        self.backtrack_counter_label = Label(self.root, text="Nombre de backtrackings : 0", fg="black")
        self.backtrack_counter_label.pack(side="right", padx=5)

        self.execution_time_label = Label(self.root, text="Temps d'exécution : 0s", fg="black")
        self.execution_time_label.pack(side="right", padx=5)

        self.memory_usage_label = Label(self.root, text="Mémoire utilisée : 0 MB", fg="black")
        self.memory_usage_label.pack(side="right", padx=5)

        self.recursive_calls_label = Label(self.root, text="Appels récursifs : 0", fg="black")
        self.recursive_calls_label.pack(side="right", padx=5)

        self.display_sudoku()

    
    def pause_solver(self):
        self.paused = True

    def play_solver(self):
        self.paused = False
        self.solve_detailed()

    def advance_step(self):
        self.step_forward = True
        self.solve_detailed()

    def undo_step_solver(self):
        if self.solver:
            self.solver.undo_step()

    def update_level(self, selected_level):
        self.index = 0
        self.level = selected_level
        if self.level == "Facile":
            self.grilles_sans_rep = grilles_facile_sans_rep
            self.grilles_avec_rep = grilles_facile_avec_rep
        
        sudoku_string = self.grilles_sans_rep['puzzle'].iloc[self.index]
        self.sudoku_matrix = string_to_matrix(sudoku_string)
        self.fixed_values = np.where(self.sudoku_matrix != 0, True, False)
        self.display_sudoku()

    def display_sudoku(self, color=None):
        """Affiche la grille de Sudoku actuelle."""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.matshow(np.ones_like(self.sudoku_matrix), cmap="Blues", alpha=0.3)

        for i in range(9):
            for j in range(9):
                num = self.sudoku_matrix[i, j]
                if self.fixed_values[i, j]:
                    color_to_use = 'black'
                elif color and (i, j) == color[:2]:
                    color_to_use = color[2]
                else:
                    color_to_use = 'blue'
                if num != 0:
                    ax.text(j, i, str(num), va='center', ha='center', fontsize=16, color=color_to_use)

        for i in range(1, 9):
            lw = 2 if i % 3 == 0 else 0.5
            ax.axhline(i - 0.5, color='black', lw=lw)
            ax.axvline(i - 0.5, color='black', lw=lw)

        if color:
            ax.add_patch(plt.Rectangle((color[1] - 0.5, color[0] - 0.5), 1, 1, fill=False, edgecolor='red', lw=3))

        ax.set_xticks([])
        ax.set_yticks([])

        plt.title(f"Sudoku #{self.index + 1} - {self.level}")

        self.canvas_fig = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas_fig.get_tk_widget().pack()
        self.canvas_fig.draw()

        plt.close(fig)

    def update_grid(self, board, row=None, col=None, color='blue'):
        """Met à jour la grille affichée avec la matrice donnée."""
        self.sudoku_matrix = board
        if row is not None and col is not None:
            self.fixed_values[row, col] = False
        self.display_sudoku(color=(row, col, color) if row is not None and col is not None else None)


    def highlight_cell(self, row, col, backtrack=False):
        if backtrack:
            print(f"Backtracking à la case ({row}, {col})")
        else:
            print(f"Sélection de la case ({row}, {col})")

    def solve_current_sudoku(self):
        start_time = time.time()  # Start the timer
        self.solver = SudokuSolver(self.sudoku_matrix, self)
        
        if self.solver.solve_sudoku():
            print("Sudoku résolu avec succès !")
            self.verify_solution()
            self.animate_solution_success()  # Animation après la résolution
        else:
            print("Aucune solution n'existe.")
            self.verification_label.config(text="Aucune solution trouvée", fg="orange")
        self.display_sudoku()

        # Execution time
        execution_time = time.time() - start_time
        self.execution_time_label.config(text=f"Temps d'exécution : {execution_time:.4f}s")
        
        # Memory usage
        self.solver.calculate_memory_usage()
        self.memory_usage_label.config(text=f"Memory usage : {self.solver.memory_usage:.2f} MB")
        
        # Recursive calls
        self.recursive_calls_label.config(text=f"Appels récursifs : {self.solver.recursive_calls}")

    def solve_detailed(self):
        start_time = time.time()  # Start the timer
        self.solver = SudokuSolver(self.sudoku_matrix, self)
        
        if self.solver.solve_sudoku_detailed():
            print("Sudoku résolu avec succès !")
            self.verify_solution()
            self.animate_solution_success()  # Animation après la résolution
        else:
            print("Aucune solution n'existe.")
            self.verification_label.config(text="Aucune solution trouvée", fg="orange")

        # Execution time
        execution_time = time.time() - start_time
        self.execution_time_label.config(text=f"Temps d'exécution : {execution_time:.4f}s")
        
        # Memory usage
        self.solver.calculate_memory_usage()
        self.memory_usage_label.config(text=f"Memory usage : {self.solver.memory_usage:.2f} MB")
        
        # Recursive calls
        self.recursive_calls_label.config(text=f"Appels récursifs : {self.solver.recursive_calls}")

    def animate_solution_success(self):
        """Illumine toute la grille en vert pour indiquer que la solution est correcte."""
        self.update_grid(self.sudoku_matrix, color="green")
        self.root.update()

        # Reset to normal after 1 second
        self.root.after(1000, lambda: self.update_grid(self.sudoku_matrix))

    def verify_solution(self):
        correct_solution = string_to_matrix(self.grilles_avec_rep['solution'].iloc[self.index])
        if np.array_equal(self.sudoku_matrix, correct_solution):
            self.verification_label.config(text="Correspond bien à la correction", fg="green")
        else:
            self.verification_label.config(text="Ne correspond pas à la correction", fg="red")

    def next_sudoku(self):
        if self.index < len(self.grilles_sans_rep) - 1:
            self.index += 1
            sudoku_string = self.grilles_sans_rep['puzzle'].iloc[self.index]
            self.sudoku_matrix = string_to_matrix(sudoku_string)
            self.fixed_values = np.where(self.sudoku_matrix != 0, True, False)
            self.verification_label.config(text="")
            self.display_sudoku()

    def prev_sudoku(self):
        if self.index > 0:
            self.index -= 1
            sudoku_string = self.grilles_sans_rep['puzzle'].iloc[self.index]
            self.sudoku_matrix = string_to_matrix(sudoku_string)
            self.fixed_values = np.where(self.sudoku_matrix != 0, True, False)
            self.verification_label.config(text="")
            self.display_sudoku()

    def update_attempt_counter(self, count):
        self.attempt_counter_label.config(text=f"Nombre de cases écrites ou générées : {count}")

    def update_backtrack_counter(self, count):
        self.backtrack_counter_label.config(text=f"Nombre de backtrackings : {count}")

# Lancer l'application Tkinter
root = Tk()
app = SudokuViewer(root)
root.mainloop()
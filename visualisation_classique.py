import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, Scale, HORIZONTAL, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import psutil

# Charger les grilles avec et sans solutions depuis les fichiers CSV pour chaque niveau de difficulté
grilles_facile_sans_rep = pd.read_csv('grilles_facile_sans_rep.csv')
grilles_facile_avec_rep = pd.read_csv('grilles_facile_avec_rep.csv')

# Fonction pour convertir une chaîne de caractères en matrice NumPy
def string_to_matrix(sudoku_string):
    return np.array([int(char) if char != '.' else 0 for char in sudoku_string]).reshape(9, 9)

# Simple Classical Backtracking Solver (with optimizations for step-by-step visualization)
class ClassicBacktrackingSolver:
    def __init__(self, board, viewer):
        self.board = board
        self.viewer = viewer
        self.attempt_counter = 0
        self.backtrack_counter = 0
        self.recursive_calls = 0
        self.history = [np.copy(board)]  # Historique pour les étapes précédentes

    def is_safe(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num or self.board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
                return False
        return True

    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def solve_classic_step_by_step(self):
        """Résout la grille avec visualisation, pas à pas."""
        empty = self.find_empty_location()
        if not empty:
            return True
        row, col = empty

        self.recursive_calls += 1

        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.board[row][col] = num
                self.attempt_counter += 1
                self.viewer.update_attempt_counter(self.attempt_counter)
                self.viewer.update_grid(self.board, row, col, color="blue")
                self.viewer.root.update()

                # Stocker l'état de la grille dans l'historique pour "Étape Précédente"
                self.history.append(np.copy(self.board))

                if self.viewer.paused:
                    while self.viewer.paused and not self.viewer.step_forward:
                        self.viewer.root.update()
                        time.sleep(0.1)

                if self.viewer.step_forward:
                    self.viewer.step_forward = False
                    return False

                # Réduction de la vitesse pour une meilleure visualisation
                time.sleep(self.viewer.speed_scale.get() / 10000)

                if self.solve_classic_step_by_step():
                    return True

                # Backtracking
                self.viewer.update_grid(self.board, row, col, color="red")
                self.board[row][col] = 0
                self.backtrack_counter += 1
                self.viewer.update_backtrack_counter(self.backtrack_counter)
                time.sleep(self.viewer.speed_scale.get() / 10000)

        return False

    def solve_classic(self):
        """Résout la grille sans visualisation (résolution instantanée)."""
        empty = self.find_empty_location()
        if not empty:
            return True
        row, col = empty

        self.recursive_calls += 1

        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.board[row][col] = num
                self.attempt_counter += 1
                self.viewer.update_attempt_counter(self.attempt_counter)

                if self.solve_classic():
                    return True

                # Backtracking
                self.board[row][col] = 0
                self.backtrack_counter += 1
                self.viewer.update_backtrack_counter(self.backtrack_counter)

        return False

    def undo_step(self):
        """Annuler le dernier pas en utilisant l'historique."""
        if len(self.history) > 1:
            self.history.pop()  # Retirer l'état actuel
            previous_board = self.history[-1]
            self.board = np.copy(previous_board)  # Restaurer l'état précédent
            self.viewer.update_grid(self.board)  # Mettre à jour la grille affichée

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
        # Frame de contrôle (play, pause, vitesse)
        control_frame_top = Frame(self.root)
        control_frame_top.pack(side="top", pady=10)

        self.play_button = Button(control_frame_top, text="Play", command=self.play_solver)
        self.play_button.pack(side="left", padx=5)

        self.speed_scale = Scale(control_frame_top, from_=0.1, to=1000, resolution=0.1, orient=HORIZONTAL, label="Vitesse (ms)")
        self.speed_scale.set(300)
        self.speed_scale.pack(side="left", expand=True, fill="x", padx=5)

        self.pause_button = Button(control_frame_top, text="Pause", command=self.pause_solver)
        self.pause_button.pack(side="left", padx=5)

        control_frame_left = Frame(self.root)
        control_frame_left.pack(side="left", padx=10)

        self.prev_button = Button(control_frame_left, text="Précédent", command=self.prev_sudoku)
        self.prev_button.pack(pady=5)

        self.next_button = Button(control_frame_left, text="Suivant", command=self.next_sudoku)
        self.next_button.pack(pady=5)

        control_frame_right = Frame(self.root)
        control_frame_right.pack(side="right", padx=10)

        self.prev_step_button = Button(control_frame_right, text="Étape Précédente", command=self.undo_step_solver)
        self.prev_step_button.pack(pady=5)

        self.next_step_button = Button(control_frame_right, text="Étape Suivante", command=self.advance_step)
        self.next_step_button.pack(pady=5)

        self.canvas_frame = Frame(self.root)
        self.canvas_frame.pack(side="top", pady=10)

        control_frame_bottom = Frame(self.root)
        control_frame_bottom.pack(side="bottom", pady=10)

        self.solve_button = Button(control_frame_bottom, text="Résoudre", command=self.solve_current_sudoku)
        self.solve_button.pack(pady=5)

        self.solve_detailed_button = Button(control_frame_bottom, text="Résolution Détaillée", command=self.solve_detailed)
        self.solve_detailed_button.pack(pady=5)

        self.verification_label = Label(self.root, text="", fg="blue")
        self.verification_label.pack()

        # Affichage des compteurs
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

    def solve_current_sudoku(self):
        start_time = time.time()

        self.solver = ClassicBacktrackingSolver(self.sudoku_matrix, self)
        success = self.solver.solve_classic()

        if success:
            self.verify_solution()
            self.animate_solution_success()
        else:
            self.verification_label.config(text="Aucune solution trouvée", fg="orange")
        self.display_sudoku()

        execution_time = time.time() - start_time
        self.execution_time_label.config(text=f"Temps d'exécution : {execution_time:.4f}s")

        # Memory usage
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 ** 2
        self.memory_usage_label.config(text=f"Memory usage : {memory_usage:.2f} MB")

        self.recursive_calls_label.config(text=f"Appels récursifs : {self.solver.recursive_calls}")

    def solve_detailed(self):
        start_time = time.time()

        self.solver = ClassicBacktrackingSolver(self.sudoku_matrix, self)
        success = self.solver.solve_classic_step_by_step()

        if success:
            self.verify_solution()
            self.animate_solution_success()
        else:
            self.verification_label.config(text="Aucune solution trouvée", fg="orange")

        execution_time = time.time() - start_time
        self.execution_time_label.config(text=f"Temps d'exécution : {execution_time:.4f}s")

        # Memory usage
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 ** 2
        self.memory_usage_label.config(text=f"Memory usage : {memory_usage:.2f} MB")

        self.recursive_calls_label.config(text=f"Appels récursifs : {self.solver.recursive_calls}")

    def animate_solution_success(self):
        """Illumine toute la grille en vert pour indiquer que la solution est correcte."""
        self.update_grid(self.sudoku_matrix, color="green")
        self.root.update()

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

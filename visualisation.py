import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, OptionMenu, StringVar, Scale, HORIZONTAL
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

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
        self.viewer = viewer  # Référence au visualiseur pour afficher les étapes

    def get_valid_numbers(self, row, col):
        """Renvoie un ensemble des chiffres valides pour une case donnée."""
        if self.board[row, col] != 0:
            return set()

        possible_numbers = set(range(1, 10))
        possible_numbers -= set(self.board[row, :])
        possible_numbers -= set(self.board[:, col])

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        possible_numbers -= set(self.board[start_row:start_row + 3, start_col:start_col + 3].flatten())

        return possible_numbers

    def find_most_constrained_location(self):
        """Trouve la case vide avec le moins d'options possibles."""
        empty_positions = np.argwhere(self.board == 0)
        if empty_positions.size == 0:
            return None  # Aucune case vide

        min_options = 10  # Plus grand que n'importe quel nombre de possibilités (1 à 9)
        best_position = None

        for pos in empty_positions:
            row, col = pos
            valid_numbers = self.get_valid_numbers(row, col)
            num_options = len(valid_numbers)
            if num_options < min_options:
                min_options = num_options
                best_position = (row, col)

        return best_position

    def solve_sudoku_detailed(self):
        """Résout la grille en affichant chaque étape avec visualisation des erreurs (rouge) et ajouts (bleu)."""
        empty = self.find_most_constrained_location()
        if not empty:
            return True  # Plus de cases vides, la grille est résolue

        row, col = empty

        # Visualisation de la case active en rouge
        self.viewer.highlight_cell(row, col)  # Montre la case sélectionnée avec une bordure rouge
        self.viewer.root.update()  # Mise à jour de l'interface

        for num in self.get_valid_numbers(row, col):
            # Pause gérée ici
            if self.viewer.paused:  # Check if paused
                while self.viewer.paused:
                    self.viewer.root.update()  # Garde l'interface active pendant la pause

            # Ajout de la valeur en bleu pour une tentative
            self.board[row][col] = num
            self.viewer.update_grid(self.board, row, col, color="blue")  # Tentative en bleu
            self.viewer.root.update()  # Mise à jour de l'interface
            time.sleep(self.viewer.speed_scale.get() / 1000)  # Ajuste la vitesse via le slider

            if self.solve_sudoku_detailed():
                return True  # Si la solution est trouvée, arrêter

            # Backtracking : passer la valeur temporaire en rouge avant de la supprimer
            self.viewer.update_grid(self.board, row, col, color="red")  # Backtracking en rouge
            self.viewer.root.update()  # Mise à jour de l'interface
            time.sleep(self.viewer.speed_scale.get() / 1000)  # Ajuste la vitesse via le slider

            # Suppression de la valeur
            self.board[row][col] = 0  # Suppression
            self.viewer.update_grid(self.board)  # Affiche la suppression (case vide)
            self.viewer.root.update()  # Mise à jour de l'interface
            self.viewer.highlight_cell(row, col, backtrack=True)  # Surligne la case lors du backtracking
            self.viewer.root.update()  # Mise à jour de l'interface

        return False

    def solve_sudoku(self):
        """Résout la grille de Sudoku instantanément sans visualisation détaillée."""
        empty = self.find_most_constrained_location()
        if not empty:
            return True

        row, col = empty
        for num in self.get_valid_numbers(row, col):
            self.board[row][col] = num
            if self.solve_sudoku():
                return True
            self.board[row][col] = 0  # Backtracking
        return False

# Application Tkinter
class SudokuViewer:
    def __init__(self, root):
        self.root = root
        self.index = 0
        self.level = 'Facile'
        self.grilles_sans_rep = grilles_facile_sans_rep
        self.grilles_avec_rep = grilles_facile_avec_rep
        self.paused = False  # Ajout du drapeau de pause

        # Initialiser self.sudoku_matrix
        sudoku_string = self.grilles_sans_rep['puzzle'].iloc[self.index]
        self.sudoku_matrix = string_to_matrix(sudoku_string)

        # Pour marquer quelles valeurs sont fixes (noir) ou ajoutées (bleu)
        self.fixed_values = np.where(self.sudoku_matrix != 0, True, False)

        self.create_widgets()

    def create_widgets(self):
        self.level_var = StringVar(self.root)
        self.level_var.set(self.level)
        self.level_menu = OptionMenu(self.root, self.level_var, "Facile", "Moyen", "Difficile", command=self.update_level)
        self.level_menu.pack()

        self.canvas_frame = Label(self.root)
        self.canvas_frame.pack()

        self.prev_button = Button(self.root, text="Précédent", command=self.prev_sudoku)
        self.prev_button.pack(side="left")

        self.next_button = Button(self.root, text="Suivant", command=self.next_sudoku)
        self.next_button.pack(side="right")

        self.solve_button = Button(self.root, text="Résoudre", command=self.solve_current_sudoku)
        self.solve_button.pack(side="bottom")

        # Bouton pour la résolution détaillée
        self.solve_detailed_button = Button(self.root, text="Résolution Détaillée", command=self.solve_detailed)
        self.solve_detailed_button.pack(side="bottom")

        # Bouton Pause/Play sans icône, juste du texte
        self.pause_button = Button(self.root, text="Pause", command=self.pause_solver)
        self.pause_button.pack(side="left")

        self.play_button = Button(self.root, text="Play", command=self.play_solver)
        self.play_button.pack(side="right")

        # Slider pour ajuster la vitesse de la résolution, réduit à 1ms pour plus de vitesse
        self.speed_scale = Scale(self.root, from_=1, to=1000, orient=HORIZONTAL, label="Vitesse de Résolution (ms)")
        self.speed_scale.set(300)  # Définir une valeur initiale (300ms)
        self.speed_scale.pack()

        # Label pour afficher le message de vérification de la solution
        self.verification_label = Label(self.root, text="", fg="blue")
        self.verification_label.pack()

        self.display_sudoku()

    def pause_solver(self):
        """Met en pause la résolution."""
        self.paused = True

    def play_solver(self):
        """Relance la résolution après la pause."""
        self.paused = False

    def update_level(self, selected_level):
        self.index = 0
        self.level = selected_level
        if self.level == "Facile":
            self.grilles_sans_rep = grilles_facile_sans_rep
            self.grilles_avec_rep = grilles_facile_avec_rep
            sudoku_string = self.grilles_sans_rep['puzzle'].iloc[self.index]
            self.sudoku_matrix = string_to_matrix(sudoku_string)
            self.fixed_values = np.where(self.sudoku_matrix != 0, True, False)  # Marquer les cases fixes
            self.display_sudoku()

    def display_sudoku(self, color=None):
        """Affiche la grille de Sudoku actuelle, avec une option pour colorer une cellule spécifique."""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.matshow(np.ones_like(self.sudoku_matrix), cmap="Blues", alpha=0.3)

        # Si une couleur est spécifiée, elle est appliquée uniquement à la cellule en question
        for i in range(9):
            for j in range(9):
                num = self.sudoku_matrix[i, j]
                if self.fixed_values[i, j]:  # Fixe en noir
                    color_to_use = 'black'
                elif color and (i, j) == color[:2]:  # Applique la couleur spécifiée pour la cellule courante
                    color_to_use = color[2]
                else:  # Valeurs ajoutées confirmées en bleu
                    color_to_use = 'blue'
                if num != 0:
                    ax.text(j, i, str(num), va='center', ha='center', fontsize=16, color=color_to_use)

        # Dessiner les lignes de séparation des sous-grilles
        for i in range(1, 9):
            lw = 2 if i % 3 == 0 else 0.5
            ax.axhline(i-0.5, color='black', lw=lw)
            ax.axvline(i-0.5, color='black', lw=lw)

        ax.set_xticks([])
        ax.set_yticks([])

        plt.title(f"Sudoku #{self.index + 1} - {self.level}")

        self.canvas_fig = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas_fig.get_tk_widget().pack()
        self.canvas_fig.draw()

    def update_grid(self, board, row=None, col=None, color='blue'):
        """Met à jour la grille affichée avec la matrice donnée, et colore les ajouts en fonction de leur état."""
        self.sudoku_matrix = board
        if row is not None and col is not None:
            self.fixed_values[row, col] = False  # Marquer les cases modifiables
        self.display_sudoku(color=(row, col, color) if row is not None and col is not None else None)

    def highlight_cell(self, row, col, backtrack=False):
        """Surligne une cellule pour montrer qu'elle est sélectionnée avec une bordure rouge."""
        if backtrack:
            print(f"Backtracking à la case ({row}, {col})")
        else:
            print(f"Sélection de la case ({row}, {col})")

        # Affichage de la cellule avec bordure rouge
        self.update_grid(self.sudoku_matrix, row, col, color="red")

    def solve_current_sudoku(self):
        """Résout la grille instantanément et vérifie la solution."""
        solver = SudokuSolver(self.sudoku_matrix, self)
        if solver.solve_sudoku():
            print("Sudoku résolu avec succès !")
            self.verify_solution()
        else:
            print("Aucune solution n'existe.")
            self.verification_label.config(text="Aucune solution trouvée", fg="orange")
        self.display_sudoku()

    def solve_detailed(self):
        """Résout la grille en visualisant chaque étape."""
        solver = SudokuSolver(self.sudoku_matrix, self)
        if solver.solve_sudoku_detailed():
            print("Sudoku résolu avec succès !")
            self.verify_solution()
        else:
            print("Aucune solution n'existe.")
            self.verification_label.config(text="Aucune solution trouvée", fg="orange")

    def verify_solution(self):
        """Vérifie si la solution correspond à la correction."""
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
            self.fixed_values = np.where(self.sudoku_matrix != 0, True, False)  # Marquer les cases fixes
            self.verification_label.config(text="")
            self.display_sudoku()

    def prev_sudoku(self):
        if self.index > 0:
            self.index -= 1
            sudoku_string = self.grilles_sans_rep['puzzle'].iloc[self.index]
            self.sudoku_matrix = string_to_matrix(sudoku_string)
            self.fixed_values = np.where(self.sudoku_matrix != 0, True, False)  # Marquer les cases fixes
            self.verification_label.config(text="")
            self.display_sudoku()

# Lancer l'application Tkinter
root = Tk()
app = SudokuViewer(root)
root.mainloop()

import numpy as np
import pandas as pd

# Ton algorithme de résolution de Sudoku
def get_valid_numbers(board, row, col):
    """
    Renvoie un ensemble de valeurs possibles pour une case spécifique
    en fonction des valeurs déjà présentes dans la ligne, la colonne et la sous-grille.
    """
    if board[row, col] != 0:
        return set()

    possible_numbers = set(range(1, 10))

    # Supprime les numéros déjà présents dans la ligne
    possible_numbers -= set(board[row, :])

    # Supprime les numéros déjà présents dans la colonne
    possible_numbers -= set(board[:, col])

    # Supprime les numéros déjà présents dans la sous-grille 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    possible_numbers -= set(board[start_row:start_row + 3, start_col:start_col + 3].flatten())

    return possible_numbers

def find_most_constrained_location(board):
    """
    Trouve la case vide avec le moins d'options possibles pour faciliter le backtracking,
    en utilisant les fonctionnalités de NumPy pour l'optimisation.
    """
    empty_positions = np.argwhere(board == 0)
    if empty_positions.size == 0:
        return None  # Aucune case vide

    min_options = 10  # Plus grand que n'importe quel nombre de possibilités (de 1 à 9)
    best_position = None

    for pos in empty_positions:
        row, col = pos
        valid_numbers = get_valid_numbers(board, row, col)
        num_options = len(valid_numbers)
        if num_options < min_options:
            min_options = num_options
            best_position = (row, col)

        if min_options == 1:
            break

    return best_position

def solve_sudoku(board):
    """
    Résout la grille de Sudoku en utilisant une approche de backtracking optimisée.
    """
    empty = find_most_constrained_location(board)
    if not empty:
        return True  # Plus de cases vides, la grille est résolue
    row, col = empty

    for num in get_valid_numbers(board, row, col):
        board[row][col] = num

        if solve_sudoku(board):
            return True

        # Backtracking
        board[row][col] = 0

    return False

# Code de test pour utiliser ton algorithme avec une grille de ton dataset
# Charger les grilles depuis le fichier CSV (par exemple, les grilles difficiles)
sudoku_df = pd.read_csv('grilles_difficile_sans_rep.csv')

# Sélectionner une grille pour tester l'algorithme
sudoku_string = sudoku_df['puzzle'].iloc[0]  # Utiliser la première grille du dataset

# Fonction pour convertir une chaîne de caractères en matrice NumPy
def string_to_matrix(sudoku_string):
    return np.array([int(char) if char != '.' else 0 for char in sudoku_string]).reshape(9, 9)

# Convertir la grille en matrice NumPy
sudoku_matrix = string_to_matrix(sudoku_string)

print("Grille initiale :")
print(sudoku_matrix)

# Appeler l'algorithme de résolution
if solve_sudoku(sudoku_matrix):
    print("Sudoku résolu avec succès !")
else:
    print("Aucune solution n'existe.")

# Afficher la grille résolue
print("Grille résolue :")
print(sudoku_matrix)
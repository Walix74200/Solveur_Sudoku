import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# Variables globales pour évaluer les performances
iterations = 0  # Compteur pour le nombre d'itérations (placements)
execution_times = []  # Liste pour stocker les temps d'exécution pour chaque grille

# Ton algorithme de résolution de Sudoku avec évaluation des performances
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
    global iterations
    empty = find_most_constrained_location(board)
    if not empty:
        return True  # Plus de cases vides, la grille est résolue

    row, col = empty

    for num in get_valid_numbers(board, row, col):
        board[row][col] = num
        iterations += 1  # Incrémenter le compteur d'itérations pour chaque placement

        if solve_sudoku(board):
            return True

        # Backtracking
        board[row][col] = 0
        iterations += 1  # Compter le backtracking

    return False

# Fonction pour convertir une chaîne de caractères en matrice NumPy
def string_to_matrix(sudoku_string):
    return np.array([int(char) if char != '.' else 0 for char in sudoku_string]).reshape(9, 9)

# Fonction pour évaluer la performance et générer le graphe
def evaluate_performance(sudoku_string):
    global iterations
    iterations = 0  # Réinitialiser le compteur d'itérations
    
    # Convertir la grille en matrice NumPy
    sudoku_matrix = string_to_matrix(sudoku_string)

    # Mesurer le temps d'exécution
    start_time = time.time()
    
    # Appeler l'algorithme de résolution
    if solve_sudoku(sudoku_matrix):
        pass  # Résolu avec succès
    end_time = time.time()
    execution_time = end_time - start_time
    
    return iterations, execution_time

# Charger les grilles depuis le fichier CSV (par exemple, les grilles difficiles)
sudoku_df = pd.read_csv('grilles_difficile_sans_rep.csv')

# Sélectionner plusieurs grilles pour tester l'algorithme
num_grids = 50  # Nombre de grilles à tester
grids_to_test = sudoku_df['puzzle'].iloc[:num_grids]  # Tester les N premières grilles

iterations_list = []
times_list = []

# Test des grilles de Sudoku
for sudoku_string in grids_to_test:
    iter_count, exec_time = evaluate_performance(sudoku_string)
    iterations_list.append(iter_count)
    times_list.append(exec_time)

# Visualisation des performances avec Matplotlib
plt.figure(figsize=(14, 6))
# Graphique de la relation entre le nombre d'itérations et le temps d'exécution
plt.subplot(1, 2, 1)
plt.plot(iterations_list, times_list, marker='o', color='b', linestyle='--')
plt.title('Corrélation entre le nombre d\'itérations et le temps d\'exécution (50 grilles)')
plt.xlabel('Nombre d\'itérations')
plt.ylabel('Temps d\'exécution (secondes)')

# Graphique en scatter plot pour comparer l'efficacité des grilles
plt.subplot(1, 2, 2)
plt.scatter(iterations_list, times_list, color='g', s=50)
plt.title('Évaluation de l\'efficacité des grilles (50 grilles)')
plt.xlabel('Nombre d\'itérations')
plt.ylabel('Temps d\'exécution (secondes)')

plt.tight_layout()
plt.show()


#on a pu tester avec notre premier  algo sur 50 grilles de sudoku de différent niveau, on remarque directement une corrélation entre le nombre d'itération et le temps d'exécutions
#Le scatter plot montre comment certaines grilles ont un nombre élevé d'itérations tout en prenant beaucoup de temps, tandis que d'autres grilles, plus faciles, ont à la fois un nombre d'itérations et un temps d'exécution faibles.
#les grilles les plus faciles à résoudre sont concentrées en bas à gauche, avec des temps et des itérations faibles, tandis que les grilles plus complexes se situent vers le haut et la droite du graphique.
#nclusion générale :
 #corrélation linéaire entre le nombre d'itérations et le temps d'exécution est clairement visible dans les deux graphiques. Cela signifie que la complexité d'une grille de Sudoku (en termes de nombre d'itérations nécessaires pour la résoudre) est directement proportionnelle au temps requis pour sa résolution.
#le scatter plot montre également que certaines grilles (points plus éloignés) sont nettement plus complexes que d'autres, nécessitant à la fois plus d'itérations et plus de temps.
#Celaindique que l'algorithme fonctionne de manière cohérente, avec une performance prédictible en fonction de la difficulté des grilles testées.

 
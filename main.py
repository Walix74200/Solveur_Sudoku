import numpy as np

def is_valid(board, row, col, num):
    """
    Vérifie si un nombre peut être placé dans une position donnée sur la grille.
    Le nombre doit être unique dans sa ligne, sa colonne et sa sous-grille 3x3.
    """
    # Vérifie la ligne
    if num in board[row]:
        return False
    
    # Vérifie la colonne
    if num in board[:, col]:
        return False

    # Vérifie la sous-grille 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row + 3, start_col:start_col + 3]:
        return False
    
    return True

def find_empty_location(board):
    """
    Trouve une case vide dans la grille (représentée par 0).
    Retourne une tuple (ligne, colonne) ou None si la grille est complète.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve_sudoku(board):
    """
    Résout la grille de Sudoku en utilisant l'algorithme de backtracking.
    """
    empty = find_empty_location(board)
    if not empty:
        return True  # Plus de cases vides, la grille est résolue
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            # Backtracking
            board[row][col] = 0

    return False

# Exemple de grille de Sudoku (0 représente les cases vides)
board = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])

if solve_sudoku(board):
    print("La grille a été résolue :")
    print(board)
else:
    print("Aucune solution n'existe pour cette grille.")

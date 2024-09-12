# Solver for Sudoku

The aim of this project is to develop a Sudoku solver capable of solving grids of varying difficulty, using
using advanced backtracking and optimisation techniques. The project will focus on
algorithmic efficiency and visualisation of results.

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Results](#results)
- [Librairies] (#Librairies)

## Introduction
The backtracking method for solving a Sudoku involves filling in the empty squares one by one. For each cell, you try a number from 1 to 9. If the number respects the rules (no duplicates in the row, column or sub-grid), you continue with the next square. If you reach a dead end, go back to the previous square and try another number. This process is repeated until the entire grid is filled correctly.

## Requirements
- Python 3.10
- Networkx
- NumPy
- Pandas
- Matplotlib

## Installation
1. Clone the repository:
    ```sh
    git clone git@github.com:Walix74200/Solveur_Sudoku.git
    cd image-defect-detection
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Prepare your dataset:
    - Select the dataset with all the differents Sudoku grids
    

4. Run the visualisation script:
    ```sh
    python visualisation.py
    ```

## Project Structure

sudoku solver/
│
├── optimised backtracking
│   ├── correct/           # The algorithm starts in a part of the grid where there are the most restrictions
                             and then moves forward until it finds an error
│   └── error/             # When the algorithm has found an error, it backtracks until it finds the error
│
├── simple backtracking              
├── correct/       # The algorithm advances until it finds an error
└── error/              # When the algorithm has found an error, it backtracks until it finds the error
│

## How it works

1. **Find an empty cell**: The solver scans the grid and finds the first empty square (a square with no numbers). He always starts with the first available empty square in the order.
2. **Try a number**: For this empty square, the solver tries to place a number between 1 and 9. He starts with 1 and gradually moves up
3. **Check the Sudoku rules**: After placing a number in the square, the player checks that the number respects the Sudoku rules:
- No duplicates in the same row.
- No duplicates in the same column.
- No duplicates in the same 3x3 square (or sub-grid).
4. **Continue or go back**: If the number respects all the rules, the solver moves on to the next empty square and repeats the process.
If no number can be placed in the square without violating the rules, the current solution is not correct. The solver erases the previous number (goes backwards, hence the term ‘backtracking’) and tries another number in the previous square.
4. **Repeat the process**: The solver continues to try and check the numbers for each empty cell, backtracking when necessary, until the entire grid is filled correctly.
4. **Finish with a complete solution**: Once all the boxes have been filled in, and each number complies with the Sudoku rules, the solution is found and the grid is solved.

## Results

Backtracking does its job well here, because it can solve any type of sudoku grid with 3 different levels of difficulty (easy, medium, hard).

- **Easy**: 0,28 seconds
- **Medium**: 0.37 seconds
- **Hard**: 0.44 seconds

These measurements show that, depending on the level of difficulty, the algorithm will take more or less time

## libraries

We made this project possible thanks to this libraries:

- NumPy: A fundamental package for scientific computing in Python, providing support for arrays, matrices, and many mathematical functions to operate on them.
- Pandas: A powerful library for data manipulation and analysis, offering data structures like DataFrames for handling and analyzing data efficiently.
- NetworkX: A library for the creation, manipulation, and study of complex networks and graphs, providing tools for analyzing the structure and dynamics of networks.
- Matplotlib: A comprehensive library for creating static, animated, and interactive visualizations in Python. It is widely used for plotting and visualizing data.


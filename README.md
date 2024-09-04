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
- [Contributing](#contributing)
- [Acknowledgments] (#Acknowledgments)

## Introduction
The SudokuMaster project aims to create a sophisticated Sudoku solver capable of solving various grids using advanced techniques such as backtracking and optimisation. With its focus on algorithmic efficiency and visualisation of results, SudokuMaster offers a powerful and interactive solution for Sudoku enthusiasts and researchers.

## Requirements
- Python 3.10
- Networkx
- NumPy
- Pandas
- Matplotlib
- Seaborn

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
    

4. Run the main script:
    ```sh
    python main.py
    ```

## Project Structure

image-defect-detection/
│
├── images/
│   ├── correct/           # Directory for correct images
│   └── error/             # Directory for images with defects
│
├── main.py                # Main script for training and prediction
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

## How it works

1. **Feature Extraction**: ORB (Oriented FAST and Rotated BRIEF) is used to extract keypoints and descriptors from images. ORB is efficient and fast, making it suitable for real-time applications.
2. **Data Augmentation**: The imgaug library is used to augment the images. This includes random flips, rotations, scaling, and brightness adjustments to make the model more robust and generalize better to new data.
3. **Clustering**: Descriptors are clustered using K-means to create a fixed-size feature vector for each image. This helps in standardizing the input for the classifier.
4. **Classification**: An SVM (Support Vector Machine) is trained on the feature vectors. The SVM classifier is chosen for its effectiveness in high-dimensional spaces and its ability to handle cases where the number of dimensions exceeds the number of samples.

## Results

The model is evaluated on a test set to determine its accuracy in detecting printing defects. Here are the key results:

- **Accuracy**: XX%
- **Precision**: XX%
- **Recall**: XX%
- **F1 Score**: XX%

These metrics demonstrate the model's effectiveness in identifying printing defects with a high degree of accuracy.

## Contributing

We welcome contributions to improve this project! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a Pull Request.

Please ensure your pull request adheres to the following guidelines:

- Describe the purpose of the pull request and what it changes.
- Ensure the code follows the project's coding standards.
- Include tests for any new functionality.

## Acknowledgments

We would like to thank the following resources and libraries that made this project possible:

- NumPy: A fundamental package for scientific computing in Python, providing support for arrays, matrices, and many mathematical functions to operate on them.
- Pandas: A powerful library for data manipulation and analysis, offering data structures like DataFrames for handling and analyzing data efficiently.
- NetworkX: A library for the creation, manipulation, and study of complex networks and graphs, providing tools for analyzing the structure and dynamics of networks.
- Matplotlib: A comprehensive library for creating static, animated, and interactive visualizations in Python. It is widely used for plotting and visualizing data.
- Seaborn: A statistical data visualization library based on Matplotlib, offering a high-level interface for drawing attractive and informative statistical graphics..

If you have any questions or need further assistance, feel free to open an issue or contact the maintainers.
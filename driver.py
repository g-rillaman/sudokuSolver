import numpy as np

from SudokuPartialState import SudokuPartialState
from dfs import depth_first_search

def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    solved_sudoku = SudokuPartialState(board=sudoku)
    if solved_sudoku.no_repeats():
        solved_sudoku = depth_first_search(SudokuPartialState(board=sudoku))
    else:
        solved_sudoku = None
    
    if solved_sudoku is not None:    
        return solved_sudoku.board
    else:
        return np.full((9,9),-1)
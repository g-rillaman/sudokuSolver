import unittest

from AlgoX import *


class TestSolver(unittest.TestCase):
    def test_solve(self):
        X: set = {1,2,3,4,5,6,7}
        Y: dict = {
            'A': [1, 4, 7],
            'B': [1, 4],
            'C': [4, 5, 7],
            'D': [3, 5, 6],
            'E': [2, 3, 6, 7],
            'F': [2, 7]
        }
        
        # Transform X into the correct form
        X = {j: set() for j in X}
        for i in Y:
            for j in Y[i]:
                X[j].add(i)

        expected_solution: list = ['B', 'D', 'F']
        actual_solution: list = solve(X, Y, [])

        self.assertEqual(expected_solution, [choice for choice in actual_solution])

if __name__ == "__main__":
    unittest.main()
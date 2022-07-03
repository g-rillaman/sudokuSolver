from itertools import product

def solve_sudoku(size, grid):
    """An efficient Sudoku solver using Algorithm X."""
    num_rows, num_cols = size
    N = num_rows * num_cols

    # Create the representations
    X = (
            [("rc", rc) for rc in product(range(N), range(N))]              # `row-col` - Only one number in each cell
            + [("rn", rn) for rn in product(range(N), range(1, N + 1))]     # `row - number` - Each number appears once in each row
            + [("cn", cn) for cn in product(range(N), range(1, N + 1))]     # `col - number` - Each number appears once in each column
            + [("bn", bn) for bn in product(range(N), range(1, N + 1))]     # `box - number` - Each number appears once in each box
        )

    Y = dict()
    for row, col, number in product(range(N), range(N), range(1, N + 1)):
        box = (row // num_rows) * num_rows + (col // num_cols)
        Y[(row, col, number)] = [
            ("rc", (row, col)),
            ("rn", (row, number)),
            ("cn", (col, number)),
            ("bn", (box, number)),
        ]

    X = inverse_representation(Y, X)
    
    # Remove constraints that are already satisfied 
    try:
        for i, row in enumerate(grid):
            for j, n in enumerate(row):
                if n:
                    cover(X, Y, (i, j, n))
    except KeyError as e:
        # Key Error arises when we can't remove _____ - there is no solution
        yield [[-1]*9]*9
    
    for solution in solve(X, Y, []):
        for (row, col, number) in solution:
            grid[row][col] = number
        yield grid

def inverse_representation(constraints_per_choice, constraints):
    """Return the inverse representation of the constraints satisfied by each choice.
    
    That is, return a dictionary of k: v pairs where each v is the set of choices that satisfy each 
    constraint - the key."""
    choices_per_constraint= {constraint: set() for constraint in constraints}
    for choice, constraints in constraints_per_choice.items():
        for constraint in constraints:
            choices_per_constraint[constraint].add(choice)
    
    return choices_per_constraint

def solve(X, Y, solution) -> list:
    # If no more columns (constraints) left, we have a solution
    if not X:
        yield list(solution) 
    else:
        min_col = min(X, key=lambda col: len(X[col]))
        for row in list(X[min_col]):
            solution.append(row)
            removed_cols = cover(X, Y, row)

            for solution in solve(X, Y, solution):
                yield solution
            
            uncover(X, Y, row, removed_cols)

            solution.pop()

def cover(X, Y, row) -> list:
    removed_cols = [] # Keep track of columns removed
    for j in Y[row]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        removed_cols.append(X.pop(j))
    return removed_cols

def uncover(X, Y, row, removed_cols) -> None:
    # Insert the removed columns in the reverse order of when they were removed
    for j in reversed(Y[row]):
        X[j] = removed_cols.pop()
        # Add back the column names that satisfy this constraint
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

def test() -> None:
    valid_grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

    solved_grid = []
    for solution in solve_sudoku((3, 3), valid_grid):
        #print(*solution, sep='\n')
        solved_grid = solution
    print("Valid Grid: ")
    print(solved_grid)

    invalid_grid = [
        [8, 5, 2, 9, 7, 6, 2, 4, 3,],
        [6, 7, 9, 1, 4, 3, 2, 8, 5,],
        [0, 3, 1, 2, 5, 8, 7, 6, 9,],
        [3, 1, 4, 5, 2, 7, 8, 9, 6,],
        [7, 6, 8, 3, 9, 1, 4, 5, 0,],
        [9, 2, 5, 6, 0, 0, 3, 7, 1,],
        [5, 4, 3, 8, 6, 2, 9, 1, 7,],
        [1, 9, 7, 4, 3, 5, 0, 2, 8,],
        [2, 8, 6, 7, 1, 9, 5, 3, 4,],
        ]
    
    solved_grid = []
    for solution in solve_sudoku((3, 3), valid_grid):
        #print(*solution, sep='\n')
        solved_grid = solution
    print("Invalid Grid: ")
    print(solved_grid)

if __name__ == "__main__":
    test()
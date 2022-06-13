
import numpy as np

from AlgoX import solve_sudoku

SKIP_TESTS = False

if not SKIP_TESTS:
    import time
    difficulties = ['very_easy', 'easy', 'medium', 'hard']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")
        
        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")
        
        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)
            
            start_time = time.process_time()
            for solution in solve_sudoku((3, 3), sudoku):
                #print(*solution, sep='\n')
                your_solution = solution
            end_time = time.process_time()
            
            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)
            
            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])
            
            print("This sudoku took", end_time-start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        #if count < len(sudokus):
            #break
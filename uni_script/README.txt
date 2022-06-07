My choice of algorithm was to implement a constraint satisfaction with depth-first search 
backtracking.

When a partial sudoku is passed, the program will caculate all the possible values that
can be placed into any empty cells, and store these as part of the state object. At this 
stage, the program also 'validates' the sudoku, and so if there are any repeating values
any columns, rows and boxes, then the 9x9 array of -1s will be returned here. If this
is 'passed', then the recursive implementation of the DFS part starts.

The program will pick a random empty cell and from that a random possible value and create
a new state with this value in the cell. This state will update it's possible values by 
looking at the columns that cell can affect, rather than having to go through the whole
sudoku. Also, as the possible values are generated at the start, the program never has
validate that there are no repeating numbers. 
After this, the program will then calculate all of the empty cells with one possible value,
'singular cells' and fill these in, checking after every update the connected cells and updating the
singular cells as needed.

If the sudoku encounters a partial state where there is a cell with no possible values,
we know we have reached a non-possible state that cannot lead to the solution, and so
we backtrack to the previous state, and try a different value. If we encounter this for
all the next possible states from this current state, we backtrack again. This can
lead to the program identifying invalid sudokus.

The program knows it has reached the solution when the board is full, since no impossible
values are set, and so when this is achieved, it returns this state back through
all the recursive calls of the DFS.
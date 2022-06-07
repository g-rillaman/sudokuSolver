import copy

class SudokuPartialState:
    number = 0
    
    def __init__(self, board, n=9):
        self.n = n
        self.board = board 
        # Possible values for all empty cells
        self.possible_moves = {}
        self.calc_moves()
    
    def increment_count(self):
        SudokuPartialState.number += 1
        
    def is_row_valid(self, row):
        """
        Return true if all rows have no repeating values, false otherwise
        """
        digit_count = { 0:1, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0 }
        for c in range(9):
            digit_count[self.board[row][c]] += 1
        digit_count.pop(0, None) # disregard empty cells
        for i in digit_count:
            if digit_count[i] > 1:
                return False
        return True
    
    def is_col_valid(self, col):
        """
        Return true if all columns have no repeating values, false otherwise
        """
        digit_count = { 0:1, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0 }
        for r in range(9):
            digit_count[self.board[r][col]] += 1
        digit_count.pop(0, None) # disregard empty cells
        for i in digit_count:
            if digit_count[i] > 1:
                return False
        return True
    
    def is_box_valid(self, from_row, to_row, from_col, to_col):
        """
        Return true if all boxes have no repeating values, false otherwise
        """
        digit_count = { 0:1, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0 }
        for r in range(from_row, to_row):
            for c in range(from_col, to_col):
                digit_count[self.board[r][c]] += 1
        digit_count.pop(0, None) # disregard empty cells
        for i in digit_count:
            if digit_count[i] > 1:
                return False
            
        return True
    
    def no_repeats(self):
        """
        Return true if all rows, cols and boxes are valid, false otherwise
        """        
        # validate all rows        
        for c in range(9):
            if not self.is_row_valid(c):
                return False

        # validate all columns
        for r in range(9):
            if not self.is_col_valid(r):
                return False

        # validate all boxes
        for x in range(0, 7, 3):
            for y in range(0, 7, 3):
                if not self.is_box_valid(x, x+3, y, y+3):
                    return False
                
        return True
    
    def is_zero_moves(self):
        """
        Return true if at least one empty cell has zero possible values
        """
        zero_moves = False
        for cell in self.possible_moves:
            if len(self.possible_moves[cell]) == 0:
                zero_moves = True
        
        return zero_moves
    
    def is_valid(self):
        """
        Return true if all empty cells have at least one possible value and there are no repeating digits
        """   
        return (not self.is_zero_moves()) and self.no_repeats()        
    
    def is_goal(self):
        """
        Return true if there are both non-empty cells and all cells are valid
        """
        return (self.is_valid() and self.is_complete())
    
    def is_complete(self):
        """
        Return true if there are no more empty cells, otherwise false
        """
        return len(self.get_empty_cells()) == 0
        
    def get_possible_values(self, row, col):
        """
        Calculate all the possible values of a cell in position (row, col)
        """
        # Get numbers in row, column and box and remove them from possible values list
        possible_values = [i for i in range(1,10)]
        
        for num in self.board[row,:]:
            if num in possible_values:
                possible_values.remove(num)
        for num in self.board[:,col]:
            if num in possible_values:
                possible_values.remove(num)
        for x in range((row//3)*3, (row//3)*3 + 3):
            for y in range((col//3)*3, (col//3)*3 + 3):
                num = self.board[x][y]
                if num in possible_values:
                    possible_values.remove(num)
        
        return possible_values
    
    def calc_moves(self):
        """
        Get all the possible moves for every empty cell in the state
        """        
        for cell in self.get_empty_cells():
            self.possible_moves[(cell[0],cell[1])] = self.get_possible_values(cell[0],cell[1])
    
    def get_empty_cells(self):
        """
        Return tuples of (row, col) 
        """
        positions = []
        
        for r in range(9):
            for c in range(9):
                if self.board[r,c] == 0:
                    positions.append((r,c))
                    
        return positions                    
    
    def get_singleton_cells(self):
        """
        Return the empty cells that have only a singular possible value
        """
        return [k for k, v in self.possible_moves.items() if len(v) == 1]
    
    def update_connected_empty_cells(self, row, col):
        """
        Update the possible values for each of the empty cells connected to the input cell. 
        We say that the cells are connected if they are in the same row, column or box.
        'Updating' the values is done by removing the possible value in our input cell from the possible list of values
        of the current cell.
        """
        value = self.board[row, col]
        
        # Remove from row
        for c in range(9):
            if self.board[row, c] == 0:
                try:
                    self.possible_moves[(row, c)].remove(value) # remove value
                except ValueError:
                    pass
                
        # Remove from column
        for r in range(9):
            if self.board[r, col] == 0:
                try:
                    self.possible_moves[(r, col)].remove(value) # remove value
                except ValueError:
                    pass
                
        # Remove from box
        b_row = row//3 * 3
        b_col = col//3 * 3
        for y in range(b_row, b_row+3):
            for x in range(b_col, b_col+3):
                if self.board[y, x] == 0:
                    try:
                        self.possible_moves[(y, x)].remove(value) # remove value
                    except ValueError:
                        pass       
    
    def set_value(self, row, col, value):
        """ 
        Returns a new state with value in the cell specified
        """
        state = copy.deepcopy(self)
        
        # Update value with first possible one
        state.board[row, col] = value
        state.update_connected_empty_cells(row, col)
        
        # If new state has any cells with only 1 value, we put enter these too.
        singular_values = state.get_singleton_cells()
        while len(singular_values) > 0:
            cell = singular_values[0]
            state.board[cell[0], cell[1]] = state.possible_moves[cell][0]
            state.possible_moves.pop(cell) # remove this cell from possible moves
            state.update_connected_empty_cells(cell[0], cell[1])
            singular_values = state.get_singleton_cells()

        state.calc_moves()
        
        self.increment_count()
                
        return state
from typing import Optional
#import numpy as np

import logging

class LinkedListNode:
    def __init__(self) -> None:
        self.left = None
        self.right = None
        self.up = None
        self.down = None

        self.rowId = None
        self.colId = None
        self.node_count = 0
        self.column = None


class ToroidalMatrix:
    def __init__(self) -> None:
        self.matrix = None
        self.header = LinkedListNode()  # this is our entry point into the lattice

    def cover(self, node: LinkedListNode) -> None:
        logging.warning(f"covering")
        column = node.column

        # Unlink the column header node
        column.right.left = column.left
        column.left.right = column.right

        # Move down the column and remove each row by traversing right
        row = column.down
        while row != column:
            right_node = row.right
            while right_node != row:
                # Unlink the node
                right_node.up.down = right_node.down
                right_node.down.up = right_node.up

                self.matrix[0][right_node.col_Id].node_count -= 1
                right_node = right_node.right

            row = row.down

    def uncover(self, node: LinkedListNode) -> None :
        logging.warning(f"uncovering")
        column = node.column

        # Move up the column and add each row by traversing left
        row = column.up
        while row != column:
            left_node = row.left
            while left_node != row:
                # Relink the node
                left_node.up.down = left_node
                left_node.down.up = left_node

                self.matrix[0][left_node.col_Id].node_count += 1
                left_node = left_node.right

            row = row.up

        # Relink the column node, this must be done last
        column.right.left = column
        column.left.right = column

    def get_min_column(self):
        """Return the col_Id of the column with the least nodes, traversing right."""
        node = self.header
        min_col = self.header.right

        node = node.right.right
        while node != self.header:
            if node.node_count < min_col.node_count:
                min_col = node
            node = node.right
        
        return min_col

    def fill(self, constraint_matrix: list[list]) -> None:
        no_of_rows, no_of_cols = len(constraint_matrix), len(constraint_matrix[0])
        no_of_rows += 1  # Extra row for the header row 

        # Add an array of 1s to designate the position of header nodes
        constraint_matrix.insert(0, [True for _ in range(no_of_cols)])

        self.matrix = [[None for _ in range(no_of_cols)] for _ in range(no_of_rows)]
        
        # Fill header row with nodes
        for j in range(no_of_cols):
            self.matrix[0][j] = LinkedListNode()

        # Create node for every 1 in the constraint_matrix
        for i in range(no_of_rows):
            for j in range(no_of_cols):

                # Create node only if 1 in the constraint matrix
                if constraint_matrix[i][j]:
                    self.matrix[i][j] = LinkedListNode()

                    # Increment header node count if not a header node
                    if i:
                        self.matrix[0][j].node_count += 1

        # Link the nodes together
        for i in range(no_of_rows):
            for j in range(no_of_cols):

                    if self.matrix[i][j]:
                        # Add pointer to column header
                        self.matrix[i][j].column = self.matrix[0][j]

                        # Set row and column ID
                        self.matrix[i][j].row_Id = i
                        self.matrix[i][j].col_Id = j

                        # Connect Node to neighbours
                        a, b = i, j  # to keep track of the position we start

                        # Left
                        b = ToroidalMatrix.get_left(b, no_of_cols)
                        while (not constraint_matrix[a][b]) and (b != j):
                            b = self.get_left(b, no_of_cols)
                        self.matrix[i][j].left = self.matrix[i][b]

                        # Right
                        a, b = i, j

                        b = ToroidalMatrix.get_right(b, no_of_cols)
                        while (not constraint_matrix[a][b]) and (b != j):
                            b = self.get_right(b, no_of_cols)
                        self.matrix[i][j].right = self.matrix[i][b]

                        # Up
                        a, b = i, j

                        a = ToroidalMatrix.get_up(a, no_of_rows)
                        while (not constraint_matrix[a][b]) and (a != i):
                            a = self.get_up(a, no_of_rows)
                        self.matrix[i][j].up = self.matrix[a][j]     

                        # Down
                        a, b = i, j

                        a = ToroidalMatrix.get_down(a, no_of_rows)
                        while (not constraint_matrix[a][b]) and (a != i):
                            a = self.get_down(a, no_of_rows)
                        self.matrix[i][j].down = self.matrix[a][j]

        # We link the header between the first and last header columns
        self.header.right = self.matrix[0][0]
        self.header.left = self.matrix[0][no_of_cols-1]

        self.matrix[0][0].left = self.header
        self.matrix[0][no_of_cols-1].right = self.header
        
    @staticmethod
    def get_left(pos: int, no_of_cols: int):
        return no_of_cols - 1 if (pos - 1) < 0 else pos - 1

    @staticmethod
    def get_right(pos: int, no_of_cols: int):
        return (pos + 1) % no_of_cols

    @staticmethod
    def get_up(pos: int, no_of_rows: int):
        return no_of_rows - 1 if (pos - 1) < 0 else pos - 1

    @staticmethod
    def get_down(pos: int, no_of_rows: int):
        return (pos + 1) % no_of_rows


def search(k: int, toroidal_matrix: ToroidalMatrix):
    logging.warning(f"Level {k}")
    solutions = []
    if toroidal_matrix.header.right == toroidal_matrix.header:
        logging.warning("Found solution")
        print(solutions)
        return
    
    column = toroidal_matrix.get_min_column()
    toroidal_matrix.cover(column)

    row = column.down
    while row != column:
        solutions.append(row)

        right_node = row.right
        while right_node != row:
            toroidal_matrix.cover(right_node)
            right_node = right_node.right

    
        search(k+1, toroidal_matrix)

        # If solution is not possible, backtrack (uncover)
        # and remove the selected row from the solution
        solutions.remove(row)

        column = row.column

        left_node = row.left
        while left_node != row:
            toroidal_matrix.uncover(right_node)
            left_node = left_node.left

        toroidal_matrix.uncover(column)

        row = row.down



def test():
    """
    Example problem
  
    X = {1,2,3,4,5,6,7}
    set-1 = {1,4,7}
    set-2 = {1,4}
    set-3 = {4,5,7}
    set-4 = {3,5,6}
    set-5 = {2,3,6,7}
    set-6 = {2,7}
    set-7 = {1,4}
    """

    no_of_rows = 7
    no_of_cols = 7
    
    constraint_matrix = [
            [False for _ in range(no_of_cols)]
            for _ in range(no_of_rows)
            ]

    # Manually fill constraint matrix
    constraint_matrix[0][0] = True
    constraint_matrix[0][3] = True
    constraint_matrix[0][6] = True 
    constraint_matrix[1][0] = True
    constraint_matrix[1][3] = True 
    constraint_matrix[2][3] = True
    constraint_matrix[2][4] = True 
    constraint_matrix[2][6] = True
    constraint_matrix[3][2] = True 
    constraint_matrix[3][4] = True
    constraint_matrix[3][5] = True 
    constraint_matrix[4][1] = True
    constraint_matrix[4][2] = True 
    constraint_matrix[4][5] = True
    constraint_matrix[4][6] = True 
    constraint_matrix[5][1] = True
    constraint_matrix[5][6] = True 
    constraint_matrix[6][0] = True
    constraint_matrix[6][3] = True

    tor = ToroidalMatrix()
    tor.fill(constraint_matrix)

    search(0, tor)

if __name__ == "__main__":
    # TODO: Find out why no solution is being found
    matrix = test()
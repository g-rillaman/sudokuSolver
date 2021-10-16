import random 

def pick_next_cell(partial_state):
    """
    Pick the next cell to try to place values into.
    """
    #return min(partial_state.possible_moves.keys(), key=lambda x: len(partial_state.possible_moves[x])) # least possible moves   
    return random.choice(partial_state.get_empty_cells())

def order_values(partial_state, row, col):
    """
    Sorts the values - randomly in this case - in the order we will try them.
    """
    values = partial_state.possible_moves[(row, col)]
    random.shuffle(values)
    return values

def depth_first_search(partial_state):
    """
    Recursive implementation of DFS to search all of the possible states
    """
    (row,col) = pick_next_cell(partial_state) # pick the next cell to fill with a value
    values = order_values(partial_state, row, col)

    for value in values:
        new_state = partial_state.set_value(row, col, value)
        if new_state.is_goal():
            #print("Goal!")
            return new_state
        if new_state.is_valid():
            print('->')
            deep_state = depth_first_search(new_state)
            if deep_state is not None and deep_state.is_goal():
                return deep_state
        
    print('<<<')
    return None # This is returned if no valid solutions exist
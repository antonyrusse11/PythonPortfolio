import math
import os
import time
from random import randint

# Board state: Using a nested list to represent the 3x3 coordinate system
board = [
    ['.', '.', '.'],
    ['.', '.', '.'],
    ['.', '.', '.']
]

# Limit for the turn counter before we hit a draw state
MAX_SQUARES = 9 

def print_board(current_board):
    """Loop through the rows to draw the current board state."""
    for row in current_board:
        print(' '.join(row))

def number_to_coords(number):
    """
    Translates 1-9 keypad input into (row, col) matrix indices.
    I'm using floor division for the row and modulo for the column.
    """
    if not 1 <= number <= 9:
        return None, None
        
    idx = number - 1
    # Standard keypad has 1-3 at the bottom, so I'm inverting the Y-axis here
    row = 2 - (idx // 3)
    col = idx % 3
    return row, col

def check_win(current_board, marker):
    """
    Scans for 3-in-a-row across rows, columns, and diagonals.
    Using 'all()' for a cleaner way to check the markers along each vector.
    """
    # Check horizontal and vertical lines
    for i in range(3):
        if all(current_board[i][j] == marker for j in range(3)):
            return True
        if all(current_board[j][i] == marker for j in range(3)):
            return True

    # Diagonals: pivot on the center tile (1,1) for efficiency
    if current_board[1][1] == marker:
        if current_board[0][0] == current_board[2][2] == marker:
            return True
        if current_board[0][2] == current_board[2][0] == marker:
            return True

    return False

def take_human_turn(current_board, marker):
    """Input handler; includes basic validation so we don't crash on bad strings."""
    while True:
        try:
            val = int(input(f"Player {marker}, pick a spot (1-9): "))
            if not 1 <= val <= 9:
                raise ValueError
            
            r, c = number_to_coords(val)
            if current_board[r][c] != '.':
                print("That spot is taken.")
                continue
                
            current_board[r][c] = marker
            return True
        except ValueError:
            print("Just use numbers 1-9.")

def take_computer_turn(current_board, marker):
    """Picks a random available spot from the list of empty cells."""
    print(f"Computer ({marker}) is moving...")
    
    # Generate list of available (r, c) tuples
    options = [(r, c) for r in range(3) for c in range(3) if current_board[r][c] == '.']
    
    if options:
        # Simple random choice from the valid coordinate pairs
        r, c = options[randint(0, len(options) - 1)]
        current_board[r][c] = marker
        return True
    return False

# Execution logic
turn_count = 0 
winner = None

while turn_count < MAX_SQUARES and not winner:
    # Refresh console so the board stays in one place
    os.system('cls' if os.name == 'nt' else 'clear') 

    print("Current Match State:")
    print_board(board)
    print("-" * 15)

    # Alternate turns using the modulo of the turn counter
    is_human = turn_count % 2 == 0
    mark = 'X' if is_human else 'O'
    
    if is_human:
        take_human_turn(board, mark)
    else:
        time.sleep(0.6) # Small delay so the CPU move isn't instant
        take_computer_turn(board, mark)
        
    if check_win(board, mark):
        winner = mark
        
    turn_count += 1

# Final result output
os.system('cls' if os.name == 'nt' else 'clear') 
print("Final Board:")
print_board(board)

if winner:
    print(f"Result: {winner} wins.")
else:
    print("Result: Draw game.")

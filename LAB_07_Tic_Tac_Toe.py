import math
import os
import time
from random import randint

# Board init: Using list of lists for 3x3 grid
board = [
    ['.', '.', '.'],
    ['.', '.', '.'],
    ['.', '.', '.']
]

MAX_SQUARES = 9 

def print_board(current_board):
    for row in current_board:
        print(' '.join(row))

def number_to_coords(number):
    """Map 1-9 keypad to 2D array indices"""
    if not 1 <= number <= 9:
        return None, None
        
    idx = number - 1
    # Keypad mapping: 2 is bottom row, 0 is top
    row = 2 - (idx // 3)
    col = idx % 3
    return row, col

def check_win(current_board, marker):
    # Rows and Cols
    for i in range(3):
        if all(current_board[i][j] == marker for j in range(3)):
            return True
        if all(current_board[j][i] == marker for j in range(3)):
            return True

    # Diagonals
    if current_board[1][1] == marker:
        if current_board[0][0] == current_board[2][2] == marker:
            return True
        if current_board[0][2] == current_board[2][0] == marker:
            return True

    return False

def take_human_turn(current_board, marker):
    while True:
        try:
            val = int(input(f"Player {marker}, select (1-9): "))
            if not 1 <= val <= 9:
                raise ValueError
            
            r, c = number_to_coords(val)
            if current_board[r][c] != '.':
                print("Square occupied.")
                continue
                
            current_board[r][c] = marker
            return True
        except ValueError:
            print("Invalid input. Use 1-9.")

def take_computer_turn(current_board, marker):
    print(f"Computer ({marker}) moving...")
    
    # Identify empty slots
    options = [(r, c) for r in range(3) for c in range(3) if current_board[r][c] == '.']
    
    if options:
        # Simple random move selection
        r, c = options[randint(0, len(options) - 1)]
        current_board[r][c] = marker
        return True
    return False

# Execution
turn_count = 0 
winner = None

while turn_count < MAX_SQUARES and not winner:
    # Refresh console
    os.system('cls' if os.name == 'nt' else 'clear') 

    print("Current State:")
    print_board(board)
    print("-" * 15)

    # Human is 'X', Computer is 'O'
    is_human = turn_count % 2 == 0
    mark = 'X' if is_human else 'O'
    
    if is_human:
        take_human_turn(board, mark)
    else:
        time.sleep(0.6) # UX delay
        take_computer_turn(board, mark)
        
    if check_win(board, mark):
        winner = mark
        
    turn_count += 1

# Result output
os.system('cls' if os.name == 'nt' else 'clear') 
print("Final Board:")
print_board(board)

if winner:
    print(f"Result: {winner} wins.")
else:
    print("Result: Draw.")

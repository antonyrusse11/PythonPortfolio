from random import seed
from random import randint 
from IPython.display import display, clear_output
import os 
import time # **Required for the computer's 'thinking' delay**

# --- 1. SETUP ---

# Initialize the 3x3 game board using a list of lists.
board = [
    ['.', '.', '.'],  # Row 0 (7, 8, 9)
    ['.', '.', '.'],  # Row 1 (4, 5, 6)
    ['.', '.', '.']   # Row 2 (1, 2, 3)
]

# MAX_SQUARES is defined here (9 total squares)
MAX_SQUARES = 9 

def print_board(current_board):
    """Prints the current state of the game board."""
    for row in current_board:
        print(' '.join(row))

# --- 2. COORDINATE FORMULA (Computer Keypad) ---

def number_to_coords(number):
    """Converts a 1-9 number (computer keypad layout) to (row, col) indices."""
    if not 1 <= number <= 9:
        return None, None
        
    zero_based_index = number - 1
    
    # Row Formula: 2 - floor((N-1)/3)
    row = 2 - (zero_based_index // 3)
    
    # Column Formula: (N-1) % 3
    col = zero_based_index % 3
    
    return row, col

# --- 3. WIN CHECKING LOGIC ---

def check_win(current_board, marker):
    """Checks if the specified marker ('X' or 'O') has won (all 8 lines)."""
    
    # Check Rows (3 combinations)
    for r in range(3):
        if all(current_board[r][c] == marker for c in range(3)):
            return True

    # Check Columns (3 combinations)
    for c in range(3):
        if all(current_board[r][c] == marker for r in range(3)):
            return True

    # Check Diagonals (2 combinations)
    
    # Diagonal 1: Top-Left to Bottom-Right
    if (current_board[0][0] == marker and
        current_board[1][1] == marker and
        current_board[2][2] == marker):
        return True
        
    # Diagonal 2: Top-Right to Bottom-Left
    if (current_board[0][2] == marker and
        current_board[1][1] == marker and
        current_board[2][0] == marker):
        return True

    return False

# --- 4. PLAYER & COMPUTER MOVES ---

def take_human_turn(current_board, marker):
    """Handles human input validation and updates the board."""
    while True:
        try:
            player_choice = int(input(f"Player {marker} (Human), choose a square (1-9): "))
        except ValueError:
            print("❌ Invalid input. Please enter a whole number between 1 and 9.")
            continue
            
        if not 1 <= player_choice <= 9:
            print("❌ Number out of range. Please choose a number between 1 and 9.")
            continue
            
        r, c = number_to_coords(player_choice)
        
        # Check if square is unoccupied
        if current_board[r][c] != '.':
            print("⚠️ That square is already taken. Please choose an empty one.")
            continue
            
        current_board[r][c] = marker
        return True
        
def take_computer_turn(current_board, marker):
    """Computer moves: selects a random, unoccupied square."""
    print(f"Player {marker} (Computer) is thinking...")
    
    # Find all available square coordinates (row, col)
    available_moves = []
    for r in range(3):
        for c in range(3):
            if current_board[r][c] == '.':
                available_moves.append((r, c))
    
    if available_moves:
        # Select one available move randomly
        r, c = available_moves[randint(0, len(available_moves) - 1)]
        current_board[r][c] = marker
        return True
    
    return False

# --- 5. MAIN GAME LOOP ---

turn_count = 0 
winner = None

# Game continues until board is full OR a winner is found
while turn_count < MAX_SQUARES and winner is None:
    
    # Clear screen and display board (REQUIRED)
    try:
        clear_output(wait=True)
    except NameError:
        os.system('cls' if os.name == 'nt' else 'clear') 

    print("### Tic-Tac-Toe Board ###")
    print_board(board)
    print("-------------------------")

    # Human ('X') moves first (turn_count 0, 2, 4...)
    is_human_turn = turn_count % 2 == 0
    player_marker = 'X' if is_human_turn else 'O'
    
    # Take the turn
    if is_human_turn:
        take_human_turn(board, player_marker)
    else:
        time.sleep(0.5) # Simulate computer thinking
        take_computer_turn(board, player_marker)
        
    # Check for a winner after each move (REQUIRED)
    if check_win(board, player_marker):
        winner = player_marker
        
    turn_count += 1
    
# --- 6. GAME END ---

# Final display
try:
    clear_output(wait=True)
except NameError:
    os.system('cls' if os.name == 'nt' else 'clear') 

print("### FINAL BOARD ###")
print_board(board)
print("-------------------")

if winner:
    print(f"🎉 GAME OVER! Player {winner} WINS! 🎉")
elif turn_count == MAX_SQUARES:
    print("🤝 GAME OVER! It's a DRAW (Board is full). 🤝")

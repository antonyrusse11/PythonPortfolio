import os

# Class to handle the 2D spatial environment and player state
class Room:
    def __init__(self, w, h):
        # Setting grid constraints based on user input
        self.width = w
        self.height = h
        # Initialize player at top-left origin (0,0)
        self.px = 0
        self.py = 0
        self.last_msg = "Room initialized."

    def display(self):
        # Clears terminal to keep the UI from scrolling endlessly
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"Room: {self.width}x{self.height} | Pos: ({self.px}, {self.py})")
        print(f"Log: {self.last_msg}")
        
        # Draw the North wall using a simple string multiplier
        print("#" * (self.width + 2)) 

        # Rendering the floor matrix row by row
        for y in range(self.height):
            row = "#" # Start with West wall
            for x in range(self.width):
                # Check if the current loop coordinates match player location
                if x == self.px and y == self.py:
                    row += "@" # Standard roguelike icon for player
                else:
                    row += "." # Floor tile
            row += "#" # End with East wall
            print(row)

        # Draw the South wall
        print("#" * (self.width + 2)) 

    def move(self, dx, dy):
        # Calculate proposed next step before committing to state change
        nx, ny = self.px + dx, self.py + dy
        
        # Out-of-bounds check: ensure new coordinates are within 0 and width/height
        if 0 <= nx < self.width and 0 <= ny < self.height:
            self.px, self.py = nx, ny
            self.last_msg = f"Moved to {nx}, {ny}"
        else:
            # Rejection message if movement hits a boundary
            self.last_msg = "Blocked: Hit a wall."

# Script entry point logic
def main():
    try:
        # Collecting dimensions; using int() for raw numeric conversion
        w = int(input("Width: "))
        h = int(input("Height: "))
        # Logic check: room must be at least 2x2 for movement to be possible
        if w < 2 or h < 2: raise ValueError
    except ValueError:
        # Fallback to prevent crash on bad user input or strings
        print("Invalid dimensions. Defaulting to 5x5.")
        w, h = 5, 5

    room = Room(w, h)
    
    # Infinite loop to handle real-time user commands until 'Q' is pressed
    while True:
        room.display()
        # Capturing lowercase keys for WASD movement
        cmd = input("Controls (WASD to move, Q to quit): ").lower()
        
        if cmd == 'q':
            print("Exiting...")
            break
        # Applying coordinate deltas for each direction
        elif cmd == 'w': room.move(0, -1)
        elif cmd == 'a': room.move(-1, 0)
        elif cmd == 's': room.move(0, 1)
        elif cmd == 'd': room.move(1, 0)
        else:
            room.last_msg = "Unknown command."

if __name__ == "__main__":
    main()

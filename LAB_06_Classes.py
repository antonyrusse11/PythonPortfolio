import os

# Class to handle the 2D spatial environment and player state
class Room:
    def __init__(self, w, h):
        # Setting grid constraints based on user input
        self.width = w
        self.height = h
        # Start player at top-left origin (0,0)
        self.px = 0
        self.py = 0
        self.last_msg = "Room initialized."

    def display(self):
        # Clears terminal to keep the UI from scrolling/flickering
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"Room: {self.width}x{self.height} | Pos: ({self.px}, {self.py})")
        print(f"Log: {self.last_msg}")
        
        # North wall rendering
        print("#" * (self.width + 2)) 

        # Rendering the floor matrix row by row
        for y in range(self.height):
            row = "#" # West wall
            for x in range(self.width):
                # Check if the current loop coordinates match player position state
                if x == self.px and y == self.py:
                    row += "@" # Player icon
                else:
                    row += "." # Null space
            row += "#" # East wall
            print(row)

        # South wall
        print("#" * (self.width + 2)) 

    def move(self, dx, dy):
        """
        Calculates a potential state update. 
        Need the OOB check here so we don't break the grid.
        """
        nx, ny = self.px + dx, self.py + dy
        
        # Out-of-bounds check: ensures nx/ny stay within [0, width/height]
        if 0 <= nx < self.width and 0 <= ny < self.height:
            self.px, self.py = nx, ny
            self.last_msg = f"Moved to {nx}, {ny}"
        else:
            # Rejection message for wall collisions
            self.last_msg = "Blocked: Hit a boundary."

def main():
    """Entry point with basic input sanitization."""
    try:
        w = int(input("Width: "))
        h = int(input("Height: "))
        # Logic check: room needs to be at least 2x2 for actual movement
        if w < 2 or h < 2: raise ValueError
    except ValueError:
        # Fallback to prevent crash on strings or empty inputs
        print("Invalid dimensions. Defaulting to 5x5.")
        w, h = 5, 5

    room = Room(w, h)
    
    # Primary control loop utilizing ASCII input for state transitions
    while True:
        room.display()
        cmd = input("Command (WASD/Q): ").lower()
        
        if cmd == 'q':
            print("Terminating process...")
            break
        # Vector-based movement mapping
        elif cmd == 'w': room.move(0, -1)
        elif cmd == 'a': room.move(-1, 0)
        elif cmd == 's': room.move(0, 1)
        elif cmd == 'd': room.move(1, 0)
        else:
            room.last_msg = "Invalid Command."

if __name__ == "__main__":
    main()

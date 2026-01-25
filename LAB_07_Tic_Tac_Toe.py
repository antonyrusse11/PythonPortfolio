import os

# Class-based encapsulation of a 2D coordinate system and state machine
class Room:
    def __init__(self, w, h):
        """
        Initializes state vectors. 
        'px/py' define the player's position within the discrete grid.
        """
        self.width = w
        self.height = h
        self.px = 0
        self.py = 0
        self.last_msg = "System Ready."

    def display(self):
        """
        Synchronizes the internal coordinate state with the console output.
        Implements a nested loop for 2D matrix rendering.
        """
        # Cross-platform clear command for consistent UI state
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"Sub-system: Grid {self.width}x{self.height} | Vector: [{self.px}, {self.py}]")
        print(f"Diagnostic: {self.last_msg}")
        print("#" * (self.width + 2)) # North Boundary

        for y in range(self.height):
            row = "#" # West Boundary
            for x in range(self.width):
                # Conditional check for player coordinate match
                if x == self.px and y == self.py:
                    row += "@" # Entity Icon
                else:
                    row += "." # Null Space
            row += "#" # East Boundary
            print(row)

        print("#" * (self.width + 2)) # South Boundary

    def move(self, dx, dy):
        """
        Calculates a potential state update. 
        Includes a pre-update validation check to prevent boundary violations.
        """
        nx, ny = self.px + dx, self.py + dy
        
        # OOB (Out of Bounds) logical validation
        if 0 <= nx < self.width and 0 <= ny < self.height:
            self.px, self.py = nx, ny
            self.last_msg = f"Translation successful: New state {nx}, {ny}"
        else:
            self.last_msg = "Error: Motion exceeds grid boundaries."

def main():
    """Main execution entry point with input sanitization and exception handling."""
    try:
        # Standard input collection for grid dimensions
        w = int(input("Define width: "))
        h = int(input("Define height: "))
        # Prevent zero or negative scalar values
        if w < 2 or h < 2: raise ValueError
    except ValueError:
        print("Invalid scalar input. Reverting to 5x5 default.")
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
            room.last_msg = "Invalid Command String."

if __name__ == "__main__":
    main()

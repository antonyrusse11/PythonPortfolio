import os

# Using a standard class for room management
class Room:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        # Start player at origin
        self.px = 0
        self.py = 0
        self.last_msg = "Room initialized."

    def display(self):
        # Refresh the view - works for both Windows and Linux
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"Room: {self.width}x{self.height} | Pos: ({self.px}, {self.py})")
        print(f"Log: {self.last_msg}")
        print("#" * (self.width + 2)) # Top wall

        for y in range(self.height):
            row = "#" # Left wall
            for x in range(self.width):
                if x == self.px and y == self.py:
                    row += "@" # Player icon
                else:
                    row += "." # Empty floor
            row += "#" # Right wall
            print(row)

        print("#" * (self.width + 2)) # Bottom wall

    def move(self, dx, dy):
        nx, ny = self.px + dx, self.py + dy
        
        # OOB check
        if 0 <= nx < self.width and 0 <= ny < self.height:
            self.px, self.py = nx, ny
            self.last_msg = f"Moved to {nx}, {ny}"
        else:
            self.last_msg = "Blocked: Hit a wall."

# Entry point
def main():
    try:
        w = int(input("Width: "))
        h = int(input("Height: "))
        if w < 2 or h < 2: raise ValueError
    except ValueError:
        print("Invalid dimensions. Defaulting to 5x5.")
        w, h = 5, 5

    room = Room(w, h)
    
    # Control loop
    while True:
        room.display()
        cmd = input("Controls (WASD to move, Q to quit): ").lower()
        
        if cmd == 'q':
            print("Exiting...")
            break
        elif cmd == 'w': room.move(0, -1)
        elif cmd == 'a': room.move(-1, 0)
        elif cmd == 's': room.move(0, 1)
        elif cmd == 'd': room.move(1, 0)
        else:
            room.last_msg = "Unknown command."

if __name__ == "__main__":
    main()

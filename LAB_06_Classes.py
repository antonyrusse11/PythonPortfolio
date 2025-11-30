from IPython.display import clear_output 

# roguelike Room Objects - write your code here

#Take Room Dimensions
width = int(input("Enter room width"))
height = int(input("Enter room height"))

#Initialise Room Class

class Room:
    
    """
    Represents a 2D room with defined dimensions and a user's location.
    """    
    def __init__(self, width, height):
                
        """
        Initializes the Room object with a given width and height,
        and sets the user's starting position (x, y) to (0, 0).
        """
    
        #Define Room Size
        self.width = width
        self.height = height
        
        # Define the user's current location (class variables x, y)
        self.x = 0
        self.y = 0
    
        #Initialise Draw Function Within Class    
    
    def draw(self):
        
        """
        Clears the console and draws the room grid, marking the user's position.
        """
    
        clear_output()
        print(f"Current Room: {self.width}x{self.height} Grid")
        print("-" * (self.width * 2 + 1)) #Border line
    
        #Outer loop iterates through rows (y-coordinate)
        for y_coord in range(self.height):
            row_output = "|"
    
            for x_coord in range(self.width):
    
                if x_coord == self.x and y_coord == self.y:
                    row_output += "P"
    
                else:
                    # Print '.' for an empty space
                    row_output += ". "
    
            row_output += "|" # End of the row
    
            print(row_output)

    #Left Check
    def left(self):
        new_x = self.x - 1
        
        # Check if the new X is still 0 or greater
        if new_x >= 0:
            self.x = new_x
            # Optional: Update a status message for feedback
            self.message = "Moved left."
        else:
            print("Movement blocked: Hit the west wall!")

        #Right Check
    def right(self):
        new_x = self.x + 1
        
        # Check if the new X is still 0 or greater
        if new_x < self.width:
            self.x = new_x
            # Optional: Update a status message for feedback
            self.message = "Moved right."
        else:
            print("Movement blocked: Hit the east wall!")

    #Up Check
    def up(self):
            new_y = self.y - 1
            
            # Boundary Check: Check if the new Y is 0 or greater. (The top boundary)
            if new_y >= 0:
                self.y = new_y
                self.message = "Moved up."
            else:
                print("Movement blocked: Hit the north wall!")

    #Down Check
    def down(self):
        new_y = self.y + 1
        
        # Boundary Check: Check if the new Y is 0 or greater. (The top boundary)
        if new_y < self.height:
            self.y = new_y
            self.message = "Moved down."
        else:
            print("Movement blocked: Hit the south wall!")
        
myRoom = Room(width,height)
myRoom.draw()

while True:
    s = input()
    if s=='a': myRoom.left()
    if s=='s': myRoom.right()
    if s=='q': myRoom.up()
    if s=='z': myRoom.down()
    if s=='x': 
        print("all done")
        break
    myRoom.draw()

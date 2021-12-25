import math

class Position:
    def __init__(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading
   
    # returns a new Position object
    def move(self, r):
        x = r * math.cos(math.radians(self.heading))
        y = r * math.sin(math.radians(self.heading))
        return Position(int(self.x + x), int(self.y + y), self.heading)

import pygame
import math
import random

DRAW_FORWARD = "F"
MOVE_FORWARD = "f"
PLUS = "+"
MINUS = "-"
BRANCH_OPEN = "["
BRANCH_CLOSE = "]"

START_POINT = (50, 50)

STEP_LENGTH = 4

WIDTH = 11000 / 5
HEIGHT = 8000 / 5

class Position:
    def __init__(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading

class Rule:
    def __init__(self, sequence, probability=1):
        self.sequence = sequence
        self.probability = probability


def generate(n, initiator, rules):
    if n == 0:
        return initiator
    else:
        next = ""
        for c in initiator:
            if c in rules.keys():

                options = rules[c]

                if len(options) == 1:
                    next += rules[c][0].sequence
                else:
                    weights = [rule.probability for rule in options]
                    next += random.choices(rules[c], weights)[0].sequence
            else:
                next += c

        return generate(n-1, next, rules)

def polar_to_cart(position, r):
    x = r * math.cos(math.radians(position.heading))
    y = r * math.sin(math.radians(position.heading))
    return Position(position.x + x, position.y + y, position.heading)

def render(path, angle):
    white = (255, 255, 255)
    black = (0,0,0)

    size = width, height = 1000, 1000
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    # set the pygame window name
    pygame.display.set_caption('Render')

    screen.fill(white)

    startx = width / 2
    starty = height / 2
    startheading = -90

    # Define line size
    linesize = 1

    oldpos = Position(startx, starty, startheading)
    
    stack = []

    for c in path:
        if c.isupper():
            newpos = polar_to_cart(oldpos, STEP_LENGTH)
            pygame.draw.line(screen, black, (oldpos.x, oldpos.y), (newpos.x, newpos.y), linesize)
            pygame.display.flip()
            oldpos = newpos
        if c.islower():
            oldpos = polar_to_cart(oldpos, STEP_LENGTH)
        elif c == PLUS:
            oldpos = Position(oldpos.x, oldpos.y, oldpos.heading - angle)
        elif c == MINUS:
             oldpos = Position(oldpos.x, oldpos.y, oldpos.heading + angle)
        elif c == BRANCH_OPEN:
            stack.append(oldpos)
        elif c == BRANCH_CLOSE:
            dest = stack.pop()
            oldpos = dest

    while True :
        # copying the image surface object
        # to the display surface object at
        # (0, 0) coordinate.
        #display_surface.blit(crop, (0, 0))
    
        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get() :
    
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT :
    
                # deactivates the pygame library
                pygame.quit()
    
                # quit the program.
                quit()
    
            # Draws the surface object to the screen.  
            pygame.display.update() 



def run():
    #path = generate(4, "L", {"L":"L+R++R-L--LL-R+", "R":"-L+RR++R+L--L-R"})
    #path = generate(6, "X", {"X":"F[+X][-X]FX", "F":"FF"})
    #path = generate(5, "X", {"X":"F-[[X]+X]+F[+FX]-X", "F":"FF"})

    # P1 = Rule("F[+FFF+ff+FF]F[-F]F", 0.1)
    # P2 = Rule("F[+FF]F", 0.33)
    # P3 = Rule("F[-F]Ff+f+fF", 0.54)

    P1 = Rule("F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF")
    P2 = Rule("ffffff")

    path = generate(2, "F+F+F+F", {"F": [P1], "f":[P2]})

    print(path)
    render(path, 90)
        

if __name__ == "__main__":
    run()

    

#simulate robot moving
import random
WEST = 0
SOUTH = 1
NORTH = 2
EAST = 3

grid_size = 5

def is_straight_valid(x, y, h):
    if (x == 0 and h == NORTH) or (x == grid_size-1 and h == SOUTH) or (y == 0 and h == WEST) or (y == grid_size-1 and h == EAST):
        return False

    return True

def get_next_move(robot):
    straight = is_straight_valid(robot.x, robot.y, robot.h)
    next_move_chance = random.uniform(0, 1)

    if straight and next_move_chance <= 0.7:
        perform_move(robot)

    else:
        new_move(robot)

def perform_move(robot):
    if robot.h == WEST:
        robot.y = robot.y - 1

    elif robot.h == SOUTH:
        robot.x = robot.x + 1

    elif robot.h == NORTH:
        robot.x = robot.x - 1

    else:
        robot.y = robot.y + 1

def new_move(robot):
    valid_moves = []

    if robot.y != 0 and robot.h != WEST:
        valid_moves.append(WEST)

    if robot.y != grid_size-1 and robot.h != EAST:
        valid_moves.append(EAST)

    if robot.x != 0 and robot.h != NORTH:
        valid_moves.append(NORTH)

    if robot.x != grid_size-1 and robot.h != SOUTH:
        valid_moves.append(SOUTH)

    next_move = random.choice(valid_moves)

    robot.h = next_move
    perform_move(robot)

class Robot(object):
    def __init__(self):
        self.x = None
        self.y = None
        self.h = None
        self.grid = None

robot = Robot()
#grid = [[0 for i in range(5)] for j in range(5)]
x0, y0, h0 = random.randint(0,grid_size-1), random.randint(0,grid_size-1), random.randint(0,3)
robot.x, robot.y, robot.h = x0, y0, h0

while True:
    print("X = {}, Y = {}, H = {}".format(robot.x, robot.y, robot.h))
    wait = raw_input("PRESS ENTER TO MAKE NEXT MOVE")
    get_next_move(robot)
#print is_straight_valid(robot.x, robot.y, robot.h)
#transitions = [[[0,0,0,0] for i in range(grid_size)] for j in range(grid_size)]

#num_states = len(grid)**2

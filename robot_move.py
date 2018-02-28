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

def get_valid_moves(x, y, h):
    valid_moves = []

    if y != 0 and h != WEST:
        valid_moves.append(WEST)

    if y != grid_size-1 and h != EAST:
        valid_moves.append(EAST)

    if x != 0 and h != NORTH:
        valid_moves.append(NORTH)

    if x != grid_size-1 and h != SOUTH:
        valid_moves.append(SOUTH)

    return valid_moves

def new_move(robot):
    valid_moves = get_valid_moves(robot.x, robot.y, robot.h)
    next_move = random.choice(valid_moves)

    robot.h = next_move
    perform_move(robot)

def get_transition_matrix():
    transitions = [[0 for a in range((grid_size**2)*4)] for b in range((grid_size**2)*4)]
    matrix_size = len(transitions)

    for i in range(matrix_size):
        for j in range(matrix_size):
            index_i = i/grid_size-1
            index_j = j/grid_size-1
            if index_i != index_j:
                ix = index_i / grid_size
                jx = index_j / grid_size
                iy = index_i % grid_size
                jy = index_j % grid_size
                ih = i % grid_size-1
                jh = j % grid_size-1

                if abs(ix-jx) + abs(iy-jy) != 1:
                    continue

                if ih == jh:
                    if ((ih == WEST and (iy-jy == 1)) or (ih == SOUTH and (jx-ix == 1))
                        or (ih == NORTH and (ix-jx == 1)) or (ih == EAST and (jy-iy == 1))):
                        transitions[i][j] = 0.7

                elif ((jh == WEST and (iy-jy == 1)) or (jh == SOUTH and (jx-ix == 1))
                    or (jh == NORTH and (ix-jx == 1)) or (jh == EAST and (jy-iy == 1))):
                    moves = get_valid_moves(ix, iy, ih)
                    transitions[i][j] = 0.3/len(moves)
    return transitions

class Grid:
    def __init__(self, robot):
        self.robot = robot
        self.tran_matrix = get_transition_matrix
        self.obs_matrices = None

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

# while True:
#     print("X = {}, Y = {}, H = {}".format(robot.x, robot.y, robot.h))
#     wait = raw_input("PRESS ENTER TO MAKE NEXT MOVE")
#     get_next_move(robot)

transitions = get_transition_matrix()
print transitions
#print transitions[0].index(0.09999999999999999)

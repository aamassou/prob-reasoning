#simulate robot moving
import random
import numpy as np
from time import sleep

NORTH, EAST, SOUTH, WEST = range(4)
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

# WEST = 0
# SOUTH = 1
# NORTH = 2
# EAST = 3
# DIRECTIONS = [WEST, SOUTH, NORTH, EAST]

grid_size = 8

def is_dir_valid(x, y, h):
    if (y == 0 and h == NORTH) or (y == grid_size-1 and h == SOUTH) or (x == 0 and h == WEST) or (x == grid_size-1 and h == EAST):
        return False

    return True

# def get_next_move(robot):
#     straight = is_straight_valid(robot.x, robot.y, robot.h)
#     next_move_chance = random.uniform(0, 1)

#     if straight and next_move_chance <= 0.7:
#         perform_move(robot)

#     else:
#         new_move(robot)

# def perform_move(robot):
#     if robot.h == WEST:
#         robot.x = robot.x - 1

#     elif robot.h == SOUTH:
#         robot.y = robot.y + 1

#     elif robot.h == NORTH:
#         robot.y = robot.y - 1

#     else:
#         robot.x = robot.x + 1

# def get_valid_moves(x, y, h):
#     valid_moves = []

#     if x != 0 and h != WEST:
#         valid_moves.append(WEST)

#     if x != grid_size-1 and h != EAST:
#         valid_moves.append(EAST)

#     if y != 0 and h != NORTH:
#         valid_moves.append(NORTH)

#     if y != grid_size-1 and h != SOUTH:
#         valid_moves.append(SOUTH)

#     return valid_moves

# def new_move(robot):
#     valid_moves = get_valid_moves(robot.x, robot.y, robot.h)
#     next_move = random.choice(valid_moves)

#     robot.h = next_move
#     perform_move(robot)

# def create_transition_matrix():
#     matrix_size = (grid_size**2)*4
#     transitions = [[0 for a in range(matrix_size)] for b in range(matrix_size)]

#     for i in xrange(matrix_size):
#         for j in xrange(matrix_size):
#             index_i = i/4
#             index_j = j/4
#             if index_i != index_j:
#                 ix = index_i / grid_size
#                 jx = index_j / grid_size
#                 iy = index_i % grid_size
#                 jy = index_j % grid_size
#                 ih = i % 4
#                 jh = j % 4

#                 if abs(ix-jx) + abs(iy-jy) == 1:
#                     #continue
#                     if ih == jh:
#                         if ((ih == WEST and (iy-jy == 1)) or (ih == SOUTH and (jx-ix == 1))
#                             or (ih == NORTH and (ix-jx == 1)) or (ih == EAST and (jy-iy == 1))):
#                             transitions[i][j] = 0.7

#                     elif ((jh == WEST and (iy-jy == 1)) or (jh == SOUTH and (jx-ix == 1))
#                         or (jh == NORTH and (ix-jx == 1)) or (jh == EAST and (jy-iy == 1))):
#                         moves = get_valid_moves(ix, iy, ih)
#                         transitions[i][j] = 0.3/float(len(moves))
#     return transitions


def create_f_matrix():
    length = (grid_size**2)*4
    f = np.zeros(length)
    f.fill(1 / float(length))
    return f

def create_t_matrix():
    mat_dim = (grid_size**2)*4
    t = np.array(np.zeros(shape=(mat_dim, mat_dim)))

    for i in xrange(mat_dim):
        x = i / (grid_size * 4)
        y = (i / 4) % grid_size
        h = i % 4
        prev_states = probable_transitions((x, y, h))
        for (xcoord, ycoord, direction), probability in prev_states:
            t[i, xcoord * grid_size * 4 + ycoord * 4 + direction] = probability
    return t

def probable_transitions(state):
    """
    Finds the neighbors of particular coord.
    :param state: tuple of (x, y, heading)
    :return : list of empty squares that are adjacent to, with probability
    """
    x, y, direction = state
    # came from: NORTH, EAST, SOUTH, WEST
    neighbors = [(x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y)]
    # neighbors = [(x + 1, y), (x, y + 1), (x, y - 1), (x - 1, y)]
    # neighbors = [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]
    prev_square = neighbors[direction]
    prev_x, prev_y = prev_square

    # Check bounds
    if not coord_in_bounds(prev_x, prev_y):
        return []

    # Always 0.7 chance if coming in same direction.
    square_dir = [((prev_x, prev_y, direction), 0.7)]
    dirs_left = list(DIRECTIONS)
    dirs_left.remove(direction)
    # Check if any directions point to walls.
    faces_wall = []
    if WEST in dirs_left:
        if prev_x == 0:
            faces_wall.append((prev_x, prev_y, WEST))
        else:
            square_dir.append(((prev_x, prev_y, WEST), 0.1))
    if EAST in dirs_left:
        if prev_x == grid_size - 1:
            faces_wall.append((prev_x, prev_y, EAST))
        else:
            square_dir.append(((prev_x, prev_y, EAST), 0.1))
    if SOUTH in dirs_left:
        if prev_y == 0:
            faces_wall.append((prev_x, prev_y, SOUTH))
        else:
            square_dir.append(((prev_x, prev_y, SOUTH), 0.1))
    if NORTH in dirs_left:
        if prev_y == grid_size - 1:
            faces_wall.append((prev_x, prev_y, NORTH))
        else:
            square_dir.append(((prev_x, prev_y, NORTH), 0.1))

    for state in faces_wall:
        square_dir.append((state, float(1) / (4 - len(faces_wall))))
    return square_dir



def coord_in_bounds(x,y):
    result = 0 <= x < grid_size and 0 <= y < grid_size
    return result

def get_ls(x, y):
    ls = []
    for i in range(-1,2):
        for j in range(-1,2):
            ls.append((x+i, y+j))

    rand_loc = ls[random.randint(0, 7)]

    if not coord_in_bounds(rand_loc[0], rand_loc[1]):
        rand_loc = None

    for adj_x, adj_y in list(ls):
        if not coord_in_bounds(adj_x, adj_y):
            ls.remove((adj_x, adj_y))

    return ls, rand_loc

def get_ls2(x, y):
    ls2 = []
    for i in range(-2,3):
        for j in range(-2,3):
            ls2.append((x+i, y+j))

    rand_loc = ls2[random.randint(0, 15)]
    if not coord_in_bounds(rand_loc[0], rand_loc[1]):
        rand_loc = None

    for adj_x, adj_y in list(ls2):
        if not coord_in_bounds(adj_x, adj_y):
            ls2.remove((adj_x, adj_y))

    return ls2, rand_loc

def create_nothing_vector():
    mat_dim = (grid_size**2)*4
    o = np.zeros(shape=(mat_dim,mat_dim))
    for i in range(mat_dim):
        x = i / (grid_size * 4)
        y = (i / 4) % grid_size
        ls, _ = get_ls(x,y)
        ls2,_ = get_ls2(x,y)
        num_adj = 8 - len(ls)
        num_adj2 = 16 - len(ls2)

        o[i, i] = 0.1 + 0.05 * num_adj + 0.025 * num_adj2
        # o[i, i] = 1.0 - 0.1 - len(ls)*0.05 - len(ls2)*0.025
    return o

def set_diagonal(o, prob, coords):
    # print('coords: ',coords)
    for x, y in coords:
        index = x * grid_size * 4 + y * 4
        for i in range(4):
            o[index + i, index + i] = prob

def create_o_matrix(coord):
    x,y = coord
    mat_dim = (grid_size**2)*4
    o = np.zeros(shape=(mat_dim, mat_dim))

    ls, _ = get_ls(x,y)
    ls2, _ = get_ls2(x,y)

    set_diagonal(o, 0.1, [(x,y)])
    set_diagonal(o, 0.05, ls)
    set_diagonal(o, 0.025, ls2)

    return o

class Robot(object):
    def __init__(self):
        self.x = None
        self.y = None
        self.h = None
        self.grid = None
        self.prob_l = 0.1
        self.prob_ls = 0.05 * 8
        self.prob_ls2 = 0.025 * 16
        self.T = create_t_matrix()#create_transition_matrix()
        self.f = create_f_matrix()
        self.nothing_vector = create_nothing_vector()

    def move(self):
        rand = random.uniform(0,1)
        if rand <= 0.3:
            self.h = DIRECTIONS[random.randint(0,3)]
        # Changes direction until robot doesn't face wall.
        while not is_dir_valid(self.x, self.y, self.h):
            self.h = DIRECTIONS[random.randint(0,3)]

        x, y = self.x, self.y

        # Moves forward in robot's direction.
        # NORTH, EAST, SOUTH, WEST
        next_locations = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        self.x, self.y = next_locations[self.h]

    def sense(self):
        rand = random.uniform(0, 1)
        if rand <= self.prob_l:
            return self.x, self.y
        elif rand <= self.prob_l + self.prob_ls:
            _, rand_loc = get_ls(self.x, self.y)
            return rand_loc
        elif rand <= self.prob_l + self.prob_ls + self.prob_ls2:
            _, rand_loc2 = get_ls2(self.x, self.y)
            return rand_loc2
        else:
            return None

    def guess_move(self):
        sensed_location = self.sense()
        print "Sensor senses: ", sensed_location
        self.fwd_step(sensed_location)
        guessed_move, probability = self.most_probable()
        print "Robot thinks it's in: ", guessed_move, " with probability: ", probability
        return guessed_move, probability

    def fwd_step(self, coord):
        f = self.f
        T = self.T
        O = self.nothing_vector
        if coord != None:
            O = create_o_matrix(coord)

        self.f = np.dot(O,np.dot(T,f))/np.sum(f)

    def most_probable(self):
        f = self.f
        max_prob_idx = np.argmax(f)
        x = max_prob_idx / (grid_size * 4)
        y = (max_prob_idx / 4) % grid_size
        # print('f:', f)
        return (x, y), f[max_prob_idx]

if __name__ == '__main__':
    robot = Robot()
    robot.x, robot.y, robot.h = random.randint(0,grid_size-1), random.randint(0,grid_size-1), random.randint(0,3)

    guessed_right = 0
    moves = 0
    for _ in range(100):
    # while True:
        # get_next_move(robot)
        robot.move()
        moves += 1
        print("Move: ", moves)
        print "\nRobot is in: ", (robot.x, robot.y)
        guessed_move, probability = robot.guess_move()
        if guessed_move == (robot.x, robot.y):
            guessed_right += 1
        man_distance = abs(guessed_move[0] - robot.x) + abs(guessed_move[1] - robot.y)
        print "Manhattan distance: ", man_distance
        print "Robot has been correct:", float(guessed_right) / moves, "of the time."


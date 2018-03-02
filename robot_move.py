import random
import numpy as np

grid_size = 8
NORTH, EAST, SOUTH, WEST = range(4)
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]
prob_l = 0.1
prob_ls = 0.05 * 8
prob_ls2 = 0.025 * 16

def is_dir_valid(x, y, h):
    if (y == 0 and h == NORTH) or (y == grid_size-1 and h == SOUTH) or (x == 0 and h == WEST) or (x == grid_size-1 and h == EAST):
        return False
    return True

def create_f():
    length = (grid_size**2)*4
    f = np.zeros(length)
    f.fill(1 / float(length))
    return f

def create_T():
    mat_dim = (grid_size**2)*4
    t = np.array(np.zeros(shape=(mat_dim, mat_dim)))

    for i in xrange(mat_dim):
        x = i / (grid_size * 4)
        y = (i / 4) % grid_size
        h = i % 4
        prev_states = trans(x, y, h)
        for (xcoord, ycoord, direction), probability in prev_states:
            t[i, xcoord * grid_size * 4 + ycoord * 4 + direction] = probability
    return t

def trans(x,y,direction):
    # NORTH, EAST, SOUTH, WEST
    cardinals = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
    prev_loc = cardinals[direction]
    prev_x, prev_y = prev_loc

    if not coord_in_bounds(prev_x, prev_y):
        return []

    ret_val = [((prev_x, prev_y, direction), 0.7)]
    dirs_left = list(DIRECTIONS)
    dirs_left.remove(direction)
    wall_dirs = []
    for dirn in dirs_left:
        if not is_dir_valid(prev_x, prev_y, dirn):
            wall_dirs.append((prev_x, prev_y, dirn))
        else:
            ret_val.append(((prev_x, prev_y, dirn), 0.1))

    for state in wall_dirs:
        ret_val.append((state, 1/float(4 - len(wall_dirs))))
    return ret_val

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
        o[i, i] = 1.0 - 0.1 - len(ls)*0.05 - len(ls2)*0.025
    return o

def set_diagonal(o, prob, coords):
    for x, y in coords:
        index = x * grid_size * 4 + y * 4
        for i in range(4):
            o[index + i, index + i] = prob

def create_O(coord):
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
    def __init__(self, grid_size):
        self.x = random.randint(0, grid_size-1)
        self.y = random.randint(0, grid_size-1)
        self.h = random.randint(0, 3)
        self.T = create_T()
        self.f = create_f()
        self.nothing_vector = create_nothing_vector()

    def move(self):
        rand = random.random()
        if rand <= 0.3:
            self.h = DIRECTIONS[random.randint(0,3)]
        while not is_dir_valid(self.x, self.y, self.h):
            self.h = DIRECTIONS[random.randint(0,3)]

        x, y = self.x, self.y

        # NORTH, EAST, SOUTH, WEST
        next_locations = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        self.x, self.y = next_locations[self.h]

    def sense(self):
        rand = random.random()
        if rand <= prob_l:
            return self.x, self.y
        elif rand <= prob_l + prob_ls:
            _, rand_loc = get_ls(self.x, self.y)
            return rand_loc
        elif rand <= prob_l + prob_ls + prob_ls2:
            _, rand_loc2 = get_ls2(self.x, self.y)
            return rand_loc2
        else:
            return None

    def predict_location(self, sensed_location):
        f = self.f
        T = self.T
        O = self.nothing_vector
        if sensed_location != None:
            O = create_O(sensed_location)
        self.f = np.dot(O,np.dot(T,f))/np.sum(f)
        max_i = np.argmax(self.f)
        x = max_i / (grid_size * 4)
        y = (max_i / 4) % grid_size
        prob = self.f[max_i]
        return (x,y), prob

if __name__ == '__main__':
    robot = Robot(grid_size)
    num_correct = 0
    num_moves = 0
    steps = 2000
    m = []
    for _ in range(steps):
        num_moves += 1
        robot.move()
        print "\nTrue Location: ", (robot.x, robot.y)
        sensed_location = robot.sense()
        print "Sensed Location: ", sensed_location
        predicted_location, prob = robot.predict_location(sensed_location)
        print "Predicted Location: ", predicted_location
        print "Prediction Probability: ", prob
        if predicted_location == (robot.x, robot.y):
            num_correct += 1
        manhattan = abs(predicted_location[0] - robot.x) + abs(predicted_location[1] - robot.y)
        m.append(manhattan)
        print "Manhattan distance: ", manhattan
        print "Accuracy:", num_correct/float(num_moves)

    print "\nManhattan Mean: ", np.mean(m)
    print "Steps: ", steps

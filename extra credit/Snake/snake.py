# Snake - A through Y on a 5 x 5 grid
# You are given a 5 x 5 grid, and this grid should hold the letters A through Y.  
# Some of the cells in the grid are already filled out.  The others can go anywhere, 
# but the constraint is that adjacent letters (for example F and G) must be adjacent to each other, 
# either horizontally or vertically.  

# -    -    -    -    Y
# R    A    -    -    -
# -    -    -    -    -
# -    E    -    -    -
# -    -    -    -    K

# Design a solution for this constraint satisfaction problem.  
# (Solution should explain the variables, the domain values, the constraints, 
#  and how the constraint propagation would work.)


from copy import deepcopy
import heapq
from numpy import repeat


# constraint graph node
class Graph_Node():
    def __init__(self, variable):
        self.variable = variable
        self.domain = set((x, y) for x in range(5) for y in range(5))
        self.value = None

    def set_value(self, value):
        self.value = value
        self.domain = set([value])

    # compare two variable by the size of its domian
    def __lt__(self, other):
        return len(self.domain) < len(self.domain)

# CSP Search Tree Node


class CSP_Search_Tree_Node:
    def __init__(self, parent=None, variable=None, value=None, grid=None):
        self.parent = parent
        self.variable = variable
        self.value = value
        self.wait_list = []
        if parent is None:
            self.set_state(grid)
        else:
            self.state = deepcopy(parent.state)
            self.update_state(self.variable, self.value)
        self.get_priority_heap()
        self.get_grid()

    def set_state(self, grid):
        self.state = {i: Graph_Node(variable=i) for i in range(25)}
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] is not None:
                    letter = grid[i][j]
                    self.state[letter].set_value((i, j))
                    self.update_state(letter, (i, j))

    def update_state(self, variable, value):
        self.state[variable].set_value(value)
        state = self.state
        # The update the possible position for the nearby variable
        if variable-1 > 0:
            state[variable-1].domain = state[variable-1].domain.intersection(set(((value[0]-1, value[1]), (value[0]+1, value[1]),
                                                                                  (value[0], value[1]-1), (value[0], value[1]+1))))
        if variable+1 < 25:
            state[variable+1].domain = state[variable+1].domain.intersection(set(((value[0]-1, value[1]), (value[0]+1, value[1]),
                                                                                  (value[0], value[1]-1), (value[0], value[1]+1))))
        for key, item in self.state.items():
            if key == variable:
                continue
            else:
                item.domain.discard(value)
        self.state = state

    def get_grid(self):
        self.grid = [[None for j in range(5)] for i in range(5)]
        for key, item in self.state.items():
            if not item.value is None:
                self.grid[item.value[0]][item.value[1]] = key

    # get priority heap for variables
    def get_priority_heap(self):
        nodes = []
        for _, node in self.state.items():
            if node.value == None:
                nodes.append(node)
        heapq.heapify(nodes)
        self.gn_priority_heap = nodes

    def get_next(self):
        # get the next node in wait list
        if (not self.wait_list or self.wait_list == []):
            for key, value in self.state.items():
                if len(value.domain) == 0:
                    return -1
            if not self.gn_priority_heap:
                return -1
            gn = heapq.heappop(self.gn_priority_heap)
            if gn == None:
                return -1
            value_constrain = dict()
            for remain in gn.domain:
                value_constrain[remain] = 0
            # calculate least constrain value
            for key in value_constrain.keys():
                if key[0]-1 >= 0 and self.grid[key[0]-1][key[1]] is not None:
                    value_constrain[key] += 1
                if key[1]-1 >= 0 and self.grid[key[0]][key[1]-1] is not None:
                    value_constrain[key] += 1
                if key[0]+1 <= 4 and self.grid[key[0]+1][key[1]] is not None:
                    value_constrain[key] += 1
                if key[1]+1 <= 4 and self.grid[key[0]][key[1]+1] is not None:
                    value_constrain[key] += 1
            value_constrain = sorted(
                value_constrain, key=lambda k: value_constrain[k])
            # expend by order of least constrain value
            for remain in value_constrain:
                if self.AC_3(gn.variable, remain):
                    self.wait_list.append(
                        CSP_Search_Tree_Node(parent=self, variable=gn.variable, value=remain))
        # no legal color for this node
        if (not self.wait_list):
            return -1
        return self.wait_list.pop()

    # AC_3
    def AC_3(self, value, position):
        state = self.state
        for key, item in state.items():
            if item.value is not None:
                dis = abs(item.value[0]-position[0]) + \
                    abs(item.value[1]-position[1])
                if dis > abs(key-value):
                    return False
        return True


def read_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        grid = [[None if x == '0' else x.strip() for x in line.split()]
                for line in lines]
        return grid


def CSP():
    grid = read_file('./input.txt')
    grid = letter_to_number(grid)
    root_node = CSP_Search_Tree_Node(parent=None, grid=grid)
    depth = 0
    tree_list = list(repeat(-1, count_none(grid)+1))
    tree_list[depth] = root_node
    maxlevel = 0
    while depth > -1:
        next = tree_list[depth].get_next()
        if next == -1:
            depth -= 1
            continue
        depth += 1
        tree_list[depth] = next
        if depth == len(tree_list)-1:
            print('Result:')
            print_state(number_to_letter(tree_list[depth].grid))
            return
        if depth > maxlevel:
            maxlevel = depth
            print('level', maxlevel-1)
            print_state(number_to_letter(tree_list[depth].grid))

    return


def count_none(matrix):
    count = 0
    for row in matrix:
        for element in row:
            if element is None:
                count += 1
    return count


def letter_to_number(matrix):
    result = []
    for row in matrix:
        new_row = []
        for element in row:
            if element is None:
                new_row.append(None)
            else:
                position = ord(element) - ord('A')
                new_row.append(position)
        result.append(new_row)
    return result


def number_to_letter(matrix):
    result = []
    for row in matrix:
        new_row = []
        for element in row:
            if element is None:
                new_row.append(None)
            else:
                letter = chr(element + ord('A'))
                new_row.append(letter)
        result.append(new_row)
    return result


def print_state(state):
    for i in range(len(state)):
        print('[', end=' ')
        for node in state[i]:
            if node == None:
                print('_', end=' ')
            else:
                print(node, end=' ')
        print(']')
    print("-------------")


if __name__ == '__main__':
    CSP()

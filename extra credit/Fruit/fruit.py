# A* algorithm for fruit sorting
# You are given 10 apples of different sizes, 10 bananas of different sizes and 10 oranges of different sizes, 
# organized in a 3x10 array.  You want to organize them so that fruits go from top to bottom in ascending order of size.  
# Any fruit can be used in any column that you like.  The only move allowed is to swap two fruits horizontally or vertically.  
# You want to use A* algorithm to minimize the number of moves for this.  Explain your approach.


import copy
import heapq
import random
from itertools import chain


APPLE = 'A'
BANANA = 'B'
ORANGE = 'O'
FRUITS = (APPLE, BANANA, ORANGE)
FRUITS_NUMBER = {APPLE: 0, BANANA: 1, ORANGE: 2}


class Node():
    def __init__(self, parent, state, goal=None):
        self.parent = parent
        self.state = state
        if self.parent is not None:
            self.goal = parent.goal
            self.g = parent.g+1
        else:
            self.goal = goal
            self.g = 0
        self.heuristic()
        self.f = self.g+self.h

    # Heuristic Function: number of misplaced fruits.
    def heuristic(self):
        h = 0
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.goal[self.state[i][j][0]] != i:
                    h += 1
                if self.state[i][j][1] != j:
                    h += 1
        self.h = h

    def get_children(self):
        grid = self.state
        choices = []
        n = len(grid)
        m = len(grid[0])
        for i in range(n):
            for j in range(m):
                # Check if there are elements that suit to swap
                if i+1 < n:
                    new_grid = to_list(copy.deepcopy(grid))
                    # swap
                    new_grid[i][j], new_grid[i+1][j] = copy.deepcopy(
                        new_grid[i+1][j]), copy.deepcopy(new_grid[i][j])
                    # Add the new node to the set
                    choices.append(Node(self, to_tuple(new_grid)))

                if j+1 < m:
                    new_grid = to_list(copy.deepcopy(grid))
                    new_grid[i][j], new_grid[i][j+1] = copy.deepcopy(
                        new_grid[i][j+1]), copy.deepcopy(new_grid[i][j])
                    choices.append(Node(self, to_tuple(new_grid)))
        return choices

    def print_result(self):
        if self.parent is not None:
            state_list = self.parent.print_result()
        else:
            state_list = []
        print('step', self.g, '')
        for column in self.state:
            print(column)
        state_list.append(self.state)
        print("------------------------------")
        return state_list

    def __lt__(self, other):
        return self.f < other.f


# read file
def read_file(file_name):
    # Map fruit names to letters
    fruits = {'apple': 'A', 'banana': 'B', 'orange': 'O'}
    # create a grid and initialized to None
    grid = [[None for j in range(10)] for i in range(3)]
    # open file and read data
    with open(file_name, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            items = [(fruits[name], int(num)-1)
                     for name, num in [item.split(' ') for item in line.split(',')]]
            count = 0

            for item in items:
                grid[count][i] = item
                count += 1

    return to_tuple(grid)


# A* algorithm
def AStar(initial_state):
    open_set = []
    close_set = set()
    goal = get_fruits_columns_number(initial_state)
    root_node = Node(parent=None, state=initial_state, goal=goal)

    # use heapq push to change the open set into a heap
    heapq.heappush(open_set, root_node)
    current_node = None

    # BFS
    while open_set:
        # pop the node with lowest f
        current_node = heapq.heappop(open_set)
        # Not expending node in close set
        state_str = to_string(current_node.state)
        if state_str in close_set:
            continue
        close_set.add(state_str)

        # the goal
        if current_node.h == 0:
            state_list = current_node.print_result()
            if result(state_list):
                return current_node.g
            else:
                print('Search Failed')
                return False

        # Expend next nodes
        for new_state in current_node.get_children():
            if not to_string(new_state.state) in close_set:
                heapq.heappush(open_set, new_state)

    return -1


# Find the best goal for each fruit
def get_fruits_columns_number(state):
    summaries = [[0 for j in range(len(state))] for i in range(len(FRUITS))]
    for i in range(len(state)):
        for j in range(len(state[i])):
            for k in range(len(state)):
                summaries[k][FRUITS_NUMBER[state[i][j][0]]] += abs(k-i)
    rows, _ = find_min_sum_with_rows(summaries)
    goal = {}
    for i in range(len(rows)):
        goal[find_key(FRUITS_NUMBER, rows[i])] = i
    return goal


def find_min_sum_with_rows(grid):
    n = len(grid[0])
    dp = [[float('inf')] * n for _ in range(len(grid))]
    prev = [[None] * n for _ in range(len(grid))]
    for j in range(n):
        dp[0][j] = grid[0][j]
    for i in range(1, len(grid)):
        for j in range(n):
            min_prev = min(
                range(n), key=lambda k: dp[i-1][k] if k != j else float('inf'))
            dp[i][j] = grid[i][j] + dp[i-1][min_prev]
            prev[i][j] = min_prev
    min_sum = min(dp[-1])
    min_col = dp[-1].index(min_sum)
    rows = [None] * n
    rows[-1] = min_col
    for i in range(len(grid)-1, 0, -1):
        min_col = prev[i][min_col]
        rows[i-1] = min_col
    return rows, min_sum


def find_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
    return None


def result(state_list):
    for k in range(len(state_list)-1):
        state1, state2 = state_list[k], state_list[k+1]
        different_i, different_j = -1, -1
        change = 0
        for i in range(len(state1)):
            for j in range(len(state1[i])):
                if state1[i][j] != state2[i][j]:
                    if different_j == -1:
                        different_i, different_j = i, j
                    else:
                        a = abs(i-different_i)
                        b = abs(j-different_j)
                        if ((a == 0 and b == 1) or (a == 1 and b == 0)) and change == 0:
                            a = state1[i][j] == state2[different_i][different_j]
                            b = state2[i][j] == state1[different_i][different_j]
                            if a and b:
                                change += 1
                            else:
                                return False
                        else:
                            print('At step', k, ' Place: ', different_i,
                                  different_j, 'change = ', change)
                            return False
    return True


def to_tuple(list):
    return tuple(tuple(row) for row in list)


def to_list(tuple):
    return [list(row) for row in tuple]


def to_string(tuple):
    return ','.join(''.join(str(x) for x in inner_tuple) for inner_tuple in tuple)


def shuffle_grid(grid):
    flat_grid = list(chain(*grid))
    # Shuffle the elements in a one-dimensional list
    random.shuffle(flat_grid)
    row_len = len(grid[0])
    # Re-split the shuffled one-dimensional list into sublists
    shuffled_grid = [flat_grid[i:i+row_len]
                     for i in range(0, len(flat_grid), row_len)]
    return shuffled_grid


if __name__ == '__main__':
    fruits = read_file('./input.txt')
    AStar(fruits)

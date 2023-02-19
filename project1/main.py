import copy

# open_list and closed_list are stored for each node
open_list = []
closed_list = []


class Node:
    capacities = []

    def __init__(self, state,  parent=None, g=0):
        self.state = state  # the current water storage capacity of each pitcher
        self.parent = parent
        self.g = g
        if parent:
            self.SetParent(parent)
        self.h = self.GetH()
        self.f = self.GetF()

    def SetParent(self, parent):
        self.parent = parent
        self.g = parent.g + 1

    def GetH(self):
        remain = self.capacities[-1] - self.state[-1]
        gap = remain
        for x in self.state[:-1]:
            temp = abs(remain - x)
            if temp < gap:
                gap = temp
        # special condition
        for x in self.capacities[:-1]:
            for y in self.state[:-1]:
                if x + y + self.state[-1] == self.capacities[-1]:
                    gap = 0

        h = gap + remain  # h(n)
        return h

    # heuristic function
    def GetF(self):
        return self.g * 1.5 + self.h


# read fille, store pitchers and infinite pitcher to capacities
def read_file(filename):
    with open(filename, 'r') as f:
        input1 = f.readline().strip()
        capacities = [int(i) for i in input1.split(',')]
        input2 = f.readline().strip()
        capacities.append(int(input2))
    f.close()
    return capacities


# Check if the state already exists in the list
def exist(list, state):
    for i in range(len(list)):
        if list[i].state == state:
            return i
    return -1


# after every step, the list need to update
def update(node, state):
    # state is updated after each operation (be careful not to exceed the capacity)
    # Check if new_state exists in closed_list and open_list
    # If in closed_list, ignore this new_state
    # If not in open_list, add to open_list and update information
    # If in open_list, check if it is the optimal path
    if exist(closed_list, state) == -1:
        key = exist(open_list, state)
        if key == -1:
            open_list.append(Node(state, node))
            open_list.sort(key=lambda element: element.f)
        elif node.g + 1 < open_list[key].g:
            open_list[key].parent = node.parent
            open_list[key].g = node.g + 1


class Pitcher:
    # A _star algorithm
    def A_star(self, capacities):
        Node.capacities = capacities  # condition node
        open_list.clear()
        closed_list.clear()

        # put the initial node in open_list
        open_list.append(Node([0]*len(capacities)))

        while (open_list != []):
            # According to the value of F, get the top node of open_list
            curr_node = open_list.pop(0)

            # find the taget quantity
            if (curr_node.state[-1] == Node.capacities[-1]):
                # PrintPath(curr_node)
                return curr_node.g

            # search
            closed_list.append(curr_node)
            curr_state = curr_node.state
            pitcher_nums = len(curr_state) - 1
            # any two pitchers x and y have following 4 actions

            # 1. x has water, empty x
            for i in range(pitcher_nums):
                if curr_state[i] > 0:
                    new_state = copy.deepcopy(curr_state)
                    # new_state = copy.deepcopy(curr_state)
                    new_state[i] = 0
                    update(curr_node, new_state)

            # 2. x has water, pour to y
                    for j in range(pitcher_nums - 1):
                        if j == i:
                            break
                        remain = Node.capacities[j] - curr_state[j]
                        if remain > 0:
                            new_state = copy.deepcopy(curr_state)
                            if remain < curr_state[i]:
                                new_state[i] = curr_state[i] - remain
                                new_state[j] = Node.capacities[j]
                            else:
                                new_state[i] = 0
                                new_state[j] += curr_state[i]
                            update(curr_node, new_state)

            # 3. x has water, pour infinite pitcher
                    if curr_state[i] + curr_state[-1] <= Node.capacities[-1]:
                        new_state = copy.deepcopy(curr_state)
                        new_state[-1] += curr_state[i]
                        new_state[i] = 0
                        update(curr_node, new_state)

            # 4. x has no water, fill water
                new_state = copy.deepcopy(curr_state)
                new_state[i] = Node.capacities[i]
                update(curr_node, new_state)

        return -1


if __name__ == '__main__':
    capacities = read_file("input1.txt")
    pitcher = Pitcher()
    steps = pitcher.A_star(capacities)
    print(steps)

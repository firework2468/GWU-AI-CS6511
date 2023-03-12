from collections import defaultdict
import sys
import copy


# find the next node to assign color
# complement heuristics by min remaining values and least constraining value
def MRV(graph, constraint, result):
    min = sys.maxsize
    min_node: int
    for node in constraint.keys():
        # min remaining values
        if len(constraint[node]) < min and result.get(node) == None:
            min_node = node
        # tie breaking rule
        elif len(constraint[node]) == min and result.get(node) == None:
            if len(graph[node]) > len(graph[min_node]):
                min_node = node
    return min_node


# check arc consistency in CSP
def AC3(graph, constraint):
    # traversal the whole graph
    for x in graph.keys():
        for y in graph[x]:
            if remove(x, y, constraint):
                # if no value for x, then this plan is false
                if len(constraint[x]) == 0:
                    return False
    return True


# whether remove inconsistent values
def remove(x, y, constraint):
    flag = False
    # if there are more than one value for y, it means its value is not decided
    if len(constraint[y]) > 1:
        return flag
    # if the value of y is decided, check if x has the same value
    for c in constraint[x]:
        if c == constraint[y][0]:
            constraint[x].remove(c)
            flag = True
    return flag


# backtracking algorithm to complement CSP
def backtracking(result, graph, domain, constraint):
    # all node have been assigned color
    if len(result) == len(graph):
        return result, True

    back_constraint = copy.deepcopy(constraint)  # copy constraint
    # according to MRV, find the next node to assign
    node = MRV(graph, constraint, result)
    # according to least constraining value, find the suitable value to assign
    for value in constraint[node]:
        result[node] = value  # assign color
        constraint[node] = [value]  # upadate constraint
        # check consistency
        if AC3(graph, constraint):
            result, flag = backtracking(result, graph, domain, constraint)
            if flag:
                return result, True
        # wrong plan, back to previous and delete this value
        constraint = copy.deepcopy(back_constraint)
        constraint[node].remove(value)
        del result[node]
    return result, False


def CSP(filename):
    # read file
    graph = defaultdict(set)
    domain = []
    constraint = {}

    print("read file:", '', filename)
    with open(filename, 'r') as file:
        for line in file:
            if line[0] == "#":
                continue
            elif line[0] == "c":
                color = int(line[-2])
            else:
                edge = [int(i) for i in line.split(',')]
                graph[edge[0]].add(edge[1])
                graph[edge[1]].add(edge[0])
    file.close()

    # initial domain and constraint
    for i in range(color):
        domain.append(i)

    for node in graph.keys():
        constraint[node] = copy.deepcopy(domain)

    # call backtrackung
    result, flag = backtracking({}, graph, domain, constraint)
    return result, flag


if __name__ == '__main__':
    result, f = CSP("input6.txt")
    if f:
        for key in result.keys().__reversed__():
            print('', key, "and this node is:", '', result[key])
    else:
        print("There is no solution.")

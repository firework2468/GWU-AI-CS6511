# Fruit Sorting 
##### State: 
Each state represents the current position of each fruit in the 3 * 10 grid.
##### Actions: 
swap two fruits horizontally or vertically.
##### Goal State: 
The goal state is where the fruits are arranged from top to bottom in ascending order of size. The final position of the three fruits is determined by the number of fruits in each column in their initial state, i.e., the first column has more apples, then the final position of the apples is in the first column.
##### Heuristic Function: 
f(n) = h(n) + g(n)
h(n)= the number of misplaced fruits.
g(n) = the number of steps already used.


##### Admissibility:
In this case, the heuristic function h(n) gives the exact number of misplaced fruits in the current state. The maximum number of moves required to place a single misplaced fruit in its correct position is 2 (one swap horizontally and one swap vertically). Therefore, the actual cost to reach the goal state from the current state is at least h(n)/2.

Since the heuristic function h(n) gives the exact number of misplaced fruits, it provides a lower bound on the number of moves required. Hence, h(n)/2 is a lower bound on the actual cost.

Therefore, the heuristic function h(n) is admissible.


# Snake
##### Variables: 
The 20 cells in the grid that need to be filled.

##### Domain: 
In this case, the domain of each variable is the letters A to Y (excluding the already filled cells).

##### Constraints: 
Adjacent letters must be adjacent to each other, both horizontally and vertically. So for each variable, there are lists to store information about its neighbors.

##### CSP using constraint propagation:

Initialization:

  - Read data as a two-dimensional list list from the given file

Constraint Propagation (AC-3):  

   - For each unassigned variable:

    - Remove any values from its domain that violate the adjacency constraint.

       - If any of its neighbors have a value assigned, remove that value from the domain.

     - If a variable's domain becomes empty, backtrack to the previous assignment and try a different value.

Backtracking Search:
   - Choose an unassigned variable by the minimum size of its domain(MRV).

   - For each value in the domain:

     - Assign a value which is choosen by LCV to the variable.

     - Apply constraint propagation to update the domains of the remaining variables.

     - Recursively continue the search until a solution is found or a dead-end is reached.

     - If a dead-end is reached (no possible values for a variable), backtrack to the previous assignment and try a different value.

Solution:
   - Once all variables are assigned values, the grid represents a valid solution.




Task
-----
Implement a constraint solver for Sudoku puzzles using backtracking search. Pseudocode is given in `pseudocode.pdf`. 

When making decisions, we recommend using the heuristic of choosing an unassigned variable with the smallest domain. You can see the difference with and without this heuristic. But as long as you pass the following tests, you do not have to use this heuristic. 

For testing, there are four options you can use with "python main.py -t ...":
- 0: "Propagation only" test. A really simple test case that can be solved without search.
- 1: "Propagation and search" test. A hard test case that requires both propagation and search.
- 2: Provides 50 easy test cases. 
- 3: Provides 50 hard test cases. 

We are setting a 20 seconds timeout on each instance. To pass the tests, you can timeout on 2 instances in the easy class ('-t 2') and up to 30 instances in the hard class ('-t 3'), because the runtime may have large variance based on the branching heuristics.





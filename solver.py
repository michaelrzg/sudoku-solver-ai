#!/usr/bin/env python

from sudoku import *
from pysat.formula import CNF
from pysat.solvers import Glucose3


def exactly_one_constraint(variables):
    """variables is a list of integers.  return a list of clauses
    representing an exactly-one constraint on those varibales.

    input:
      variables = [1,2,3]
    output: 
      [ [1,2,3],     # (X_1 v X_2 v X_3)
        [-1,-2],     # (~X_1 v ~X_2)
        [-1,-3],     # (~X_1 v ~X_3)
        [-2,-3] ]    # (~X_2 v ~X_3)
    """

    # at-least-one constraint
    alo_constraint = list(variables)
    # at-most-one constraint
    # amo_constraint = [ [i,j] for i in variables for j in variables ]
    n = len(variables)
    # loop for all indices i < j
    amo_constraint = [[-variables[i], -variables[j]] for i in range(n) for j in range(i + 1, n)]
    return [alo_constraint] + amo_constraint


def sudoku_variable(i, j, digit):
    """given cell row (i), column (j) and digit, returns the
    corresponding sudoku variable (index)

    input:
      i = 1
      j = 2
      digit = 3
    output:
      123
    """
    # return int("%d%d%d" % (i,j,digit))
    return i * 100 + j * 10 + digit


def sudoku_constraints():
    """returns a CNF representing all the constraints of a sudoku board
    `(this does not generate any unit clauses of a partially filled-in
    sudoku board

    """

    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    all_constraints = []
    # per-cell constraints
    for i in digits:
        for j in digits:
            variables = [sudoku_variable(i, j, digit) for digit in digits]
            clauses = exactly_one_constraint(variables)
            all_constraints += clauses
    # per-square constraints
    for x in [1, 4, 7]:
        for y in [1, 4, 7]:
            for digit in digits:
                variables = [sudoku_variable(i, j, digit) for i in range(x, x + 3) for j in range(y, y + 3)]
                clauses = exactly_one_constraint(variables)
                all_constraints += clauses
    # per-row constraints
    for i in digits:
        for digit in digits:
            variables = [sudoku_variable(i, j, digit) for j in digits]
            clauses = exactly_one_constraint(variables)
            all_constraints += clauses
    # per-column constraints
    for j in digits:
        for digit in digits:
            variables = [sudoku_variable(i, j, digit) for i in digits]
            clauses = exactly_one_constraint(variables)
            all_constraints += clauses

    return all_constraints


def diagonal_constraints():
    """returns a CNF representing both diagonal constraints"""
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    constraints = []


# YOUR CODE HERE
    for digit in digits:

        variables = [sudoku_variable(i,i,digit) for i in range(10)]
        variables2 = [sudoku_variable(i,(10-i),digit) for i in range(10)]
        constraints += exactly_one_constraint(variables) + exactly_one_constraint(variables2)

    return constraints


def easy_example():
    """This is an example of solving an easy sudoku using only
    unit-propagation (this does not use the full SAT solver)

    """

    board = """
+---+---+---+
|1.4|6..|...|
|9..|5..|6..|
|...|93.|4.2|
+---+---+---+
|29.|...|85.|
|..1|..4|.2.|
|..6|7.5|.1.|
+---+---+---+
|.83|...|..7|
|7..|.6.|5.8|
|.2.|.87|..3|
+---+---+---+
"""

    board = Sudoku(board)
    assumptions = board.assumptions()

    clauses = sudoku_constraints()
    cnf = CNF(from_clauses=clauses)
    # cnf.to_file("tmp.cnf")

    # do unit-propagation
    g = Glucose3(bootstrap_with=cnf.clauses)
    solution = g.propagate(assumptions=assumptions)
    learned_cells = solution[1]

    print("sudoku puzzle (easy):")
    print(board)
    board.parse_solution(learned_cells)
    print("sudoku puzzle (easy) solution:")
    print(board)


def hard_example():
    """We can solve the "world's hardest sudoku" according to:
      https://www.conceptispuzzles.com/index.aspx?uri=info/article/424

    In this puzzle, unit-propagation learns the value of no new cells,
    but running the SAT solver can still solve it quickly.

    """

    board = """
+---+---+---+
|8..|...|...|
|..3|6..|...|
|.7.|.9.|2..|
+---+---+---+
|.5.|..7|...|
|...|.45|7..|
|...|1..|.3.|
+---+---+---+
|..1|...|.68|
|..8|5..|.1.|
|.9.|...|4..|
+---+---+---+
"""

    board = Sudoku(board)
    unit_clauses = board.unit_clauses()

    clauses = sudoku_constraints()
    cnf = CNF(from_clauses=clauses)
    # cnf.to_file("tmp.cnf")
    cnf.extend(unit_clauses)  # add the board to the CNF

    # run the SAT solver
    g = Glucose3(bootstrap_with=cnf.clauses)
    g.solve()
    model = g.get_model()

    print("sudoku puzzle (hard):")
    print(board)
    board.parse_solution(model)
    print("sudoku puzzle (hard) solution:")
    print(board)


def super_hard_example():
    """
    Turn in the solution to this puzzle.
    """

    board = """
+---+---+---+
|...|...|...|
|...|...|...|
|...|...|...|
+---+---+---+
|...|...|...|
|...|...|..1|
|..2|345|...|
+---+---+---+
|56.|...|...|
|1..|...|.7.|
|...|8..|23.|
+---+---+---+
"""

    board = Sudoku(board)
    unit_clauses = board.unit_clauses()

    clauses = sudoku_constraints()
    cnf = CNF(from_clauses=clauses)
    # cnf.to_file("tmp.cnf")
    d_constraints = diagonal_constraints()
    cnf.extend(d_constraints)  # add the diagonal constraints
    cnf.extend(unit_clauses)  # add the board to the CNF

    # run the SAT solver
    g = Glucose3(bootstrap_with=cnf.clauses)
    g.solve()
    model = g.get_model()

    print("sudoku puzzle (super-hard):")
    print(board)
    board.parse_solution(model)
    print("sudoku puzzle (super-hard) solution:")
    print(board)

    one, two = board.diagonals()
    one = sorted(set(one))
    two = sorted(set(two))
    print("diagonal-one contains: %s (%d/9 expected digits)" % ("".join(one), len(one)))
    print("diagonal-two contains: %s (%d/9 expected digits)" % ("".join(two), len(two)))
    if len(one) == 9 and len(two) == 9:
        print("solution passes check")
    else:
        print("INVALID SOLUTION (CHECK DIAGONALS)")


easy_example()
hard_example()
super_hard_example()

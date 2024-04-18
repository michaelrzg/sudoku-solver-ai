#!/usr/bin/env python

class Sudoku:
    empty = """
+---+---+---+
|...|...|...|
|...|...|...|
|...|...|...|
+---+---+---+
|...|...|...|
|...|...|...|
|...|...|...|
+---+---+---+
|...|...|...|
|...|...|...|
|...|...|...|
+---+---+---+
"""

    def __init__(self,st=empty):
        rows = [1,2,3,5,6,7,9,10,11]
        board = st.strip().split("\n")
        board = [ board[i].replace('|','') for i in rows ]
        self.board = board

    def __repr__(self):
        """This prints out a sudoku board with borders"""
        separator = "+---+---+---+"
        st = []
        st.append(separator)
        for row in self.board[:3]:
            row = "|%s|%s|%s|" % (row[:3],row[3:6],row[6:])
            st.append(row)
        st.append(separator)
        for row in self.board[3:6]:
            row = "|%s|%s|%s|" % (row[:3],row[3:6],row[6:])
            st.append(row)
        st.append(separator)
        for row in self.board[6:]:
            row = "|%s|%s|%s|" % (row[:3],row[3:6],row[6:])
            st.append(row)
        st.append(separator)
        return "\n".join(st)

    def tuples(self):
        """This is a generator that returns the CNF variables for board cells
        that have been filled in

        """
        for i,row in enumerate(self.board):
            for j,cell in enumerate(row):
                if cell == '.': continue
                digit = int(cell)
                yield (i+1,j+1,digit)

    @staticmethod
    def _sudoku_variable(i,j,digit):
        return i*100 + j*10 + digit

    def unit_clauses(self):
        """This returns all the CNF variables as a list of unit clauses"""
        return [ [Sudoku._sudoku_variable(i,j,digit)] for i,j,digit in self.tuples() ]

    def assumptions(self):
        """This returns all the CNF variables as a list"""
        return [ Sudoku._sudoku_variable(i,j,digit) for i,j,digit in self.tuples() ]

    def parse_solution(self,sol):
        """Given a (partial) solution returned by a SAT solver, fills in the
        sudoku board

        """
        for lit in sol:
            if lit < 0: continue
            digit = lit % 10
            lit /= 10
            j = int(lit % 10)
            lit /= 10
            i = int(lit)
            if i == 0 or j == 0: continue
            row = self.board[i-1]
            self.board[i-1] = row[:j-1] + str(digit) + row[j:]

    def diagonals(self):
        one = [ self.board[i][i] for i in range(9) ]
        two = [ self.board[8-i][i] for i in range(9) ]
        return (one,two)

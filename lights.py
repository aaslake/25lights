#!/usr/bin/env python

import json


class Board(object):
    def __init__(self, num_rows, num_cols, all_solutions=False):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.all_solutions = all_solutions
        self.board = [
            [False for _ in range(self.num_cols)]
            for r in range(self.num_rows)
        ]
        # list of row-col tuples that we have pushed
        self.pushes = []
        self.solutions = []

    @classmethod
    def solve(cls, num_rows, num_cols, all_solutions=False):
        board = Board(num_rows, num_cols, all_solutions=all_solutions)
        board._search(0, 0)
        return board.solutions

    @classmethod
    def str_pushes(cls, num_rows, num_cols, pushes):
        """Renders the given pushes."""
        board = Board(num_rows, num_cols)
        for row, col in pushes:
            board.set(row, col)

        return str(board)

    def __str__(self):
        """Print board."""
        return "\n".join(
            ["+" + ("-" * self.num_cols) + "+"] +
            [
                "|" + "".join(["*" if cell else " " for cell in row]) + "|"
                for row in self.board
            ] +
            ["+" + ("-" * self.num_cols) + "+"]
        )

    def set(self, row, col):
        """Sets the cell."""
        self.board[row][col] = True

    def push(self, row, col):
        """Push the light at row-col."""
        self.board[row][col] ^= True

        if row > 0:
            self.board[row - 1][col] ^= True

        if row < self.num_rows - 1:
            self.board[row + 1][col] ^= True

        if col > 0:
            self.board[row][col - 1] ^= True

        if col < self.num_cols - 1:
            self.board[row][col + 1] ^= True

    def _search(self, row, col):
        """Searches for solutions from row-col."""
        if self.solutions and not self.all_solutions:
            return

        if row >= self.num_rows:
            # tried it all
            if all(all(row) for row in self.board):
                self.solutions.append(self.pushes[:])

        elif col >= self.num_cols:
            # wrap around
            self._search(row + 1, 0)
        else:
            if row >= 2:
                if any(not cell for cell in self.board[row - 2]):
                    # impossible to solve
                    return

            # try not pushing this
            self._search(row, col + 1)
            
            # try pushing this
            self.push(row, col)
            self.pushes.append((row, col))
            self._search(row, col + 1)
            self.pushes.pop()
            self.push(row, col)


def solve_size(num_rows, num_cols, all_solutions=True):
    """Finds all solutions to boards of the given size."""
    solutions = Board.solve(num_rows, num_cols, all_solutions=True)
    print "row:", num_rows, "cols:", num_cols, "solutions:", len(solutions)
    for solution in solutions:
        print Board.str_pushes(num_rows, num_cols, solution)

    with open("board_%d_%d.json" % (num_rows, num_cols), "w") as out_file:
        out_file.write(json.dumps(solutions))

    return solutions


if True:
    # solve a single board size
    solve_size(5, 5, all_solutions=True)
else:
    # solve all sizes in a square
    max_size = 5
    num_solutions = {}
    for num_rows in range(1, max_size + 1):
        for num_cols in range(1, max_size + 1):
            solutions = solve_size(num_rows, num_cols)
            num_solutions["%d-%d" % (num_rows, num_cols)] = len(solutions)

            with open("num_solutions.json", "w") as out_file:
                out_file.write(json.dumps(num_solutions, indent=2))

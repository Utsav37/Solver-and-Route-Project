#!/bin/env python3
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
# Its running for board 2 ,4, 6 very fats but taking around 27 mins in board 12.
#Implementation has been done using heuristic as absolute manhattan distance for which geeksforgeeks has been referred.
#Code is not in optimal form.Some part is redundant and has been commented

from queue import PriorityQueue
import sys
from random import randrange, sample
import string


# shift a specified row left (1) or right (-1)
def shift_row(state, row, dir):
    change_row = state[(row * 4):(row * 4 + 4)]
    return (state[:(row * 4)] + change_row[-dir:] + change_row[:-dir] + state[(row * 4 + 4):],
            ("L" if dir == -1 else "R") + str (row + 1))

# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list (state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple (s), ("U" if dir == -1 else "D") + str (col + 1))


# pretty-print board state
def print_board(row):
    for j in range (0, 16, 4):
        print('%3d %3d %3d %3d' % (row[j:(j + 4)]))

# def compare_man(b1, b2):
#     m = 0
#     tuf = len(b2)
#     for row in b1:
#         for col in row:
#             col_int = int(col)
#             if col_int != 0:
#
#                 coordinate1 = [board1.index(row), row.index(col)]
#
#
#                 coordinate2 = [(col_int - 1) // tuf, (col_int - 1) % upper_limit]
#
#                 m += calc_man_dis(coordinate1, coordinate2)
#     return sum_manhattan



# basic algorithm for heuristic referred from geeksforgeeks and various video tutorials
def algo_h(successor1):

    dm = 0
    for value in range (0, 16):
        given_value = successor1[value]
        goalcord = final.index (given_value)
        xcord_final, ycord_final = original_cord[goalcord]
        xcord_state, ycord_state = original_cord[value]
        dm += (abs (xcord_state - xcord_final) + abs (ycord_state - ycord_final))
    dm_final = float(dm)/4
    return(dm_final)

def successorsfinal(state):
    return [shift_row (state, i, d) for i in range (0, 4) for d in (1, -1)] + [shift_col (state, i, d) for i in
                                                                               range (0, 4) for d in (1, -1)]


# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate (string.maketrans ("UDLR", "DURL"))


# check if we've reached the goal
def is_goal(state):
    return sorted (state) == list (state)


# The solver! - using BFS right now
def solve(initial_board):
    priorityqueue1 = PriorityQueue ()
    priorityqueue1.put ((0, (initial_board, "")))
    while not (priorityqueue1.empty ()):
        (priority, (state, route_so_far)) = priorityqueue1.get ()
        for (successor, takenmove) in successorsfinal (state):
            if is_goal (successor):
                return (route_so_far + " " + takenmove)
            length = len(route_so_far.split())
            priorityqueue1.put ((algo_h (successor) + length, (successor, route_so_far + " " + takenmove)))

    return False


# test cases
k = 0
original_cord = {}
for i in range (4):
    for j in range (4):
        original_cord[k] = (i, j)
        k += 1

start_state = []
with open (sys.argv[1], 'r') as file:
    for line in file:
        start_state += [int (i) for i in line.split ()]

if len (start_state) != 16:
    print("Error: couldn't parse start state file")

print("Start state: ")
print_board (tuple (start_state))
final = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
print("Solving...")
route = solve (tuple (start_state))

print("Solution found in " + str (len (route) / 3) + " moves:" + "\n" + route)

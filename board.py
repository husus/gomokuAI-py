# from enum import Enum

# class BoardState(Enum):
# 	#three possible states for a given intersection
#     EMPTY = 0
#     AI = 1
#     HUMAN = -1


# The board is defined with size N * N
N = 15


'''
Each position inside the board can be referenced in two ways:
- with an ordinal number, starting from the top-left position (index 0) to the bottom-right (index N*N-1)
- with coordinates (i,j)

The following two functions are meant to convert to a number given i and j, and viceversa
'''
# Return the ordinal number given the position
def get_number(row, col, N):
    return N * row + col

# Return position [row, col] given the ordinal number
def get_position(number, N):
    return [number // N, number % N]

# Return all possible moves [i,j] that can be made in a given board status given the boundary
def child_nodes(self, bound):
    for pos in sorted(bound.items(), key=lambda el: el[1], reverse=True):
        yield get_position(pos[0], N)

# To check whether a position (i, j) is valid, i.e. whether it's inside the board
# and whether it's an empty position
# def is_valid(i, j):
#     if i<0 or i>14 or j<0 or j>14:
#         return False
#     if self.__boardMap[i][j] != 0:
#         return False
#     else:
#         return True

class Board(object):

    def __init__(self):
        self.__value = 0
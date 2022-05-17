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
def get_number(col, row, N):
    return N * row + col

# Return position [col, row] given the ordinal number
def get_position(number, N):
    return [number % N, number // N]


# To check whether a position (i, j) is valid, i.e. whether it's inside the board
# and whether it's an empty position
# def is_valid(i, j):
#     if i<0 or i>14 or j<0 or j>14:
#         return False
#     if self.__boardMap[i][j] != 0:
#         return False
#     else:
#         return True

# this counting method takes in x,y position and counts number of possible patterns (horizontally, vertically
# and diagonally) containing that position
# the flag parameter indicates whether to add or remove the score to or from the bound
def counting(x_position, y_position, pattern, COL, ROW, status, score, bound, flag):
    # set unit directions
    dir = [[1, 0], [1, 1], [0, 1], [-1, 1]]
    # prepare column, row, length, count
    length = len(pattern)
    count = 0

    # loop through all 4 directions
    for direction in range(4):
        # find number of squares that we can go back to check for patterns in a particular direction
        if dir[direction][0] * dir[direction][1] == 0:
            numberOfGoBack = dir[direction][0] * min(5, x_position) + dir[direction][1] * min(5, y_position)
        elif dir[direction][0] == 1:
            numberOfGoBack = min(5, x_position, y_position)
        else:
            numberOfGoBack = min(5, COL - 1 - x_position, y_position)
        # very first starting point after finding out numberOfGoBack
        x_starting = x_position - numberOfGoBack * dir[direction][0]
        y_starting = y_position - numberOfGoBack * dir[direction][1]
        # move through all possible patterns in a row/col/diag
        i = 0
        while i < (numberOfGoBack+1):
            # get a new starting point
            row1 = y_starting + i*dir[direction][1]
            col1 = x_starting + i*dir[direction][0]
            index = 0
            # create a list storing empty positions that are fitted in a pattern
            remember = []
            # see if every square in a checked row/col/diag has the same status to a pattern
            while index < length and ultility.checkInBound(col1, row1, COL, ROW) \
                    and status[col1][row1] == pattern[index]:
                # first check if it's the empty position to store
                # score is also a flag indicating whether modifying the bound
                if status[col1][row1] == 0:
                    remember.append(ultility.getNumber(col1, row1, COL))
                # go through every square
                row1 = row1 + dir[direction][1]
                col1 = col1 + dir[direction][0]
                index += 1
            # if we found one pattern
            if index == length:
                count += 1
                for pos in remember:
                    if not(pos in bound):
                        bound[pos] = 0
                    bound[pos] += flag*score  # update better percentage later
                i += index
            else:
                i += 1
    return count
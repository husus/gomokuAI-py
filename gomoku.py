from boardstate import *
from minimax import ab_pruning

class Gomoku(object):
    def __init__(self):
        # self.__boardMap = [[BoardState.EMPTY.name for j in range(N)] for i in range(N)]
        self.__boardMap = [['.' for j in range(N)] for i in range(N)]
        self.__currentI = -1
        self.__currentJ = -1
        # self.__currentState = BoardState.EMPTY.name
        self.__currentState = '.'

    # def get_board_map(self):
    #     return self.__boardMap

    def draw_board(self):
        for i in range(N):
            for j in range(N):
                print('{}|'.format(self.__boardMap[i][j]), end=" ")
            print()
        print() 

    def get_board_state(self, i, j):
        return self.__boardMap[i][j]
    
    def is_valid(self, i, j):
        if i<0 or i>14 or j<0 or j>14:
            return False
        if self.__boardMap[i][j] != ".":
            return False
        else:
            return True

    def set_board_state(self, i, j, state):
        '''
        States:
        . = empty
        x = black
        o = white
        '''
        self.__boardMap[i][j] = state
        self.__currentI = i
        self.__currentJ = j
        self.__currentState = state

    def count_direction(self, i, j, xdir, ydir, color):
        count = 0
        # look for 4 more steps on a certain direction
        for step in range(1, 5): 
            if xdir != 0 and (j + xdir*step < 0 or j + xdir*step >= N): # ensure move inside the board
                break
            if ydir != 0 and (i + ydir*step < 0 or i + ydir*step >= N):
                break
            if self.__boardMap[i + ydir*step][j + xdir*step] == color:
                count += 1
            else:
                break
        return count

    def is_five(self, i, j, color):
        # 4 directions: horizontal, vertical, 2 diagonals
        directions = [[(-1, 0), (1, 0)], \
                      [(0, -1), (0, 1)], \
                      [(-1, 1), (1, -1)], \
                      [(-1, -1), (1, 1)]]

        for axis in directions:
            axis_count = 1
            for (xdir, ydir) in axis:
                axis_count += self.count_direction(i, j, xdir, ydir, color)
                if axis_count >= 5:
                    return True

        return False

    def get_result(self):
        if self.is_five(self.__currentI, self.__currentJ, self.__currentState):
            return self.__currentState
        else:
            return '.'

    def ab_pruning(position, depth, alpha, beta, maximizingPlayer):
        if depth<=0: #or end game
            return eval #evaluation of current position
        if maximizingPlayer:
            max_val = float("-inf")
            for child in position:
                eval = ab_pruning(child, depth-1, alpha, beta, False)
                max_val = max(max_val, eval)
                alpha = max(alpha, eval)
            return max_val
        else:
            min_val = float("inf")
            for child in position:
                eval = ab_pruning                                                                                                                 (child, depth-1, alpha, beta, True)
                min_val = min(min_val, eval)
                beta = min(beta, eval)
            return min_val
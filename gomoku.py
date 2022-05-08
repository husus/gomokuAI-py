from board_state import *

class Gomoku(object):
    def __init__(self):
        self.__boardMap = [[BoardState.EMPTY for j in range(N)] for i in range(N)]
        self.__currentI = -1
        self.__currentJ = -1
        self.__currentState = BoardState.EMPTY

    def get_board_map(self):
        return self.__boardMap

    def get_board_state(self, i, j):
        return self.__boardMap[i][j]

    def set_board_state(self, i, j, state):
        self.__boardMap[i][j] = state
        self.__currentI = i
        self.__currentJ = j
        self.__currentState = state
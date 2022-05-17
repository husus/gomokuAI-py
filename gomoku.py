from board import *
from evaluation import *
import math

class Gomoku(object):
    def __init__(self, depth):
        self.__depth = depth   
        # self.__boardMap = [[BoardState.EMPTY.name for j in range(N)] for i in range(N)]
        self.__boardMap = [[0 for j in range(N)] for i in range(N)]
        self.__currentI = -1
        self.__currentJ = -1
        # self.__currentState = BoardState.EMPTY.name
        self.__currentState = 0

    def get_board_map(self):
        return self.__boardMap

    def draw_board(self):
        for i in range(N):
            for j in range(N):
                if self.__boardMap[i][j] == 1:
                    state = 'x'
                if self.__boardMap[i][j] == -1:
                    state = 'o'
                if self.__boardMap[i][j] == 0:
                    state = '.'
                print('{}|'.format(state), end=" ")
            print()
        print() 

    def get_state(self, i, j):
        return self.__boardMap[i][j]
    
    def is_valid(self, i, j):
        if i<0 or i>14 or j<0 or j>14:
            return False
        if self.__boardMap[i][j] != 0:
            return False
        else:
            return True

    # maybe useless
    def set_pos_state(self, i, j, state):
        '''
        States:
        0 = empty (.)
        1 = AI (x)
        -1 = human (o)
        '''
        assert state in (-1,0,1), 'The state inserted is not -1, 0 or 1'
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


    # TODO: function to be reviewed
    # this counting method takes in x,y position and counts number of possible patterns  
    # (horizontally, vertically and diagonally) containing that position
    def counting(self, xdir, ydir, pattern, score, bound, flag):
        '''
        pattern = key of patternDict --> tuple of patterns of various length
        score = value of patternDict --> associated score to pattern
        bound = dictionary with ordinal position numbers as key
                and integers (should be the score associated to the position) as value
        flag = +1 if want to add the score, -1 if want to remove the score from the bound
        '''
        # set unit directions
        direction = [[1, 0], [1, 1], [0, 1], [-1, 1]]
        # prepare column, row, length, count
        length = len(pattern)
        count = 0

        # loop through all 4 directions
        for dir in range(4):
            # find number of squares that we can go back to check for patterns in a particular direction
            if direction[dir][0] * direction[dir][1] == 0:
                numberOfGoBack = direction[dir][0] * min(5, xdir) + direction[dir][1] * min(5, ydir)
            elif direction[dir][0] == 1:
                numberOfGoBack = min(5, xdir, ydir)
            else:
                numberOfGoBack = min(5, N-1-xdir, ydir)
            # very first starting point after finding out numberOfGoBack
            x_starting = xdir - numberOfGoBack * direction[dir][0]
            y_starting = ydir - numberOfGoBack * direction[dir][1]
            # move through all possible patterns in a row/col/diag
            i = 0
            while i < (numberOfGoBack+1):
                # get a new starting point
                row1 = y_starting + i*direction[dir][1]
                col1 = x_starting + i*direction[dir][0]
                index = 0
                # create a list storing empty positions that are fitted in a pattern
                remember = []
                # see if every square in a checked row/col/diag has the same status to a pattern
                while index < length and self.is_valid(col1, row1) \
                        and self.__boardMap[col1][row1] == pattern[index]:
                    # first check if it's the empty position to store
                    # score is also a flag indicating whether modifying the bound
                    if self.__boardMap[col1][row1] == 0:
                        remember.append(get_number(col1, row1, N)) #transforming to ordinal number
                    # go through every square
                    row1 = row1 + direction[dir][1]
                    col1 = col1 + direction[dir][0]
                    index += 1
                # if we found one pattern
                if index == length:
                    count += 1
                    for pos in remember:
                        # check whether pos is already present in bound dict
                        if pos not in bound:
                            bound[pos] = 0
                        bound[pos] += flag*score  # update better percentage later
                    i += index
                else:
                    i += 1
        return count
    
    # TODO: rewrite function
    # Idea of having a current board score stored is time efficient?
    def evaluate(self, new_x, new_y, board_value, turn, bound):
        '''
        board_value = value of the board updated at each minimax, initialized as 0 
        turn = [1, -1] AI or human turn
        '''
        value_before = 0
        value_after = 0
        patternDict = create_pattern_dict() #from evalution.py
        # check for every pattern in patternDict
        for pattern in patternDict:
            score = patternDict[pattern]
            # for every pattern, count have many there are for new_x and new_y
            # and multiply them by the corresponding score
            value_before += self.counting(new_x, new_y, pattern, abs(score), bound, -1)*score
            # make the move then calculate valueAfter,
            # this time, also update the boundary percentage
            self.__boardMap[new_x][new_y] = turn
            value_after += self.counting(new_x, new_y, pattern, abs(score), bound, 1) *score
            # delete the move
            self.__boardMap[new_x][new_y] = 0
        return board_value + value_after - value_before

    def ab_pruning(self, bound, depth, value, alpha, beta, maximizingPlayer):
        if depth<=0 or (self.check_result() is not None): #or end game
            return  value #value of current position
        if maximizingPlayer:
            max_val = -math.inf
            for child in self.child_positions(bound):
                i, j = child[0], child[1]
                new_bound = dict(bound)
                new_val = self.evaluate(i, j, value, 1, new_bound)
                self.__boardMap[i][j] = 1 
                # TODO: add update boundary 
                value = self.ab_pruning(new_bound, new_val, depth-1, alpha, beta, False)
                max_val = max(max_val, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return max_val
        else:
            min_val = math.inf
            for child in bound:
                value = self.ab_pruning(child, depth-1, alpha, beta, True)                                                                                                             (child, depth-1, alpha, beta, True)
                min_val = min(min_val, value)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return min_val

    # TODO: method to create children board maps
    def child_positions(self, bound):
        for pos in sorted(bound.items(), key=lambda el: el[1], reverse=True):
            i, j = get_position(pos[0], N)
            yield self.__boardMap[i][j]



    def check_result(self):
        if self.is_five(self.__currentI, self.__currentJ, self.__currentState):
            return self.__currentState
        else:
            return None

from evaluation import *

N = 15

class GomokuAI():
    def __init__(self, depth):
        self.depth = depth   
        # self.boardMap = [[BoardState.EMPTY.name for j in range(N)] for i in range(N)]
        self.boardMap = [[0 for j in range(N)] for i in range(N)]
        self.currentI = -1
        self.currentJ = -1
        self.currentState = 0
        self.nextValue = 0 # board value
        self.nextBound = {}
        self.colorState = {} #key: player, value: color
        self.emptyCells = N*N

    def draw_board(self):
        '''
        States:
        0 = empty (.)
        1 = AI (x)
        -1 = human (o)
        '''
        for i in range(N):
            for j in range(N):
                if self.boardMap[i][j] == 1:
                    state = 'x'
                if self.boardMap[i][j] == -1:
                    state = 'o'
                if self.boardMap[i][j] == 0:
                    state = '.'
                print('{}|'.format(state), end=" ")
            print()
        print() 
    
    def is_valid(self, i, j, state=True):
        if i<0 or i>14 or j<0 or j>14:
            return False
        if state:
            if self.boardMap[i][j] != 0:
                return False
            else:
                return True
        else:
            return True

    def set_pos_state(self, i, j, state):
        '''
        States:
        0 = empty (.)
        1 = AI (x)
        -1 = human (o)
        '''
        assert state in (-1,0,1), 'The state inserted is not -1, 0 or 1'
        self.boardMap[i][j] = state
        self.currentI = i
        self.currentJ = j
        self.currentState = state
        if state == 0 and self.emptyCells<N*N:
            self.emptyCells += 1
        if state != 0:
            self.emptyCells -= 1

    def count_direction(self, i, j, xdir, ydir, state):
        count = 0
        # look for 4 more steps on a certain direction
        for step in range(1, 5): 
            if xdir != 0 and (j + xdir*step < 0 or j + xdir*step >= N): # ensure move inside the board
                break
            if ydir != 0 and (i + ydir*step < 0 or i + ydir*step >= N):
                break
            if self.boardMap[i + ydir*step][j + xdir*step] == state:
                count += 1
            else:
                break
        return count

    def is_five(self, i, j, state):
        # 4 directions: horizontal, vertical, 2 diagonals
        directions = [[(-1, 0), (1, 0)], \
                      [(0, -1), (0, 1)], \
                      [(-1, 1), (1, -1)], \
                      [(-1, -1), (1, 1)]]
        for axis in directions:
            axis_count = 1
            for (xdir, ydir) in axis:
                axis_count += self.count_direction(i, j, xdir, ydir, state)
                if axis_count >= 5:
                    return True

        return False

    # Return all possible child moves (i,j) in a board status given the bound
    # Sorted in ascending order based on their value
    def child_nodes(self, bound):
        for pos in sorted(bound.items(), key=lambda el: el[1], reverse=True):
            yield pos[0]

    # Update new boundary for possible moves given the recently-played move
    def update_bound(self, new_i, new_j, bound):
        # get rid of the played position
        played = (new_i, new_j)
        if played in bound:
            bound.pop(played)
        # check to add new position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1), (-1, -1), (1, 1)]
        # check at 2 more steps on a certain direction
        # for i in range(1,3):
        for dir in directions:
            new_col = new_j + dir[0]
            new_row = new_i + dir[1]
            if self.is_valid(new_row, new_col)\
                and (new_row, new_col) not in bound:  # if not previously been updated in def evaluation
                bound[(new_row, new_col)] = 0
        # double check that positions in bound are valid + empty cells
        for pos in bound:
            if self.boardMap[pos[0]][pos[1]] != 0:
                bound.pop(pos)
    
    # this counting method takes in x,y position and check the presence of the pattern   
    # and how many there are around that position (horizontally, vertically and diagonally)
    def counting(self, i_0, j_0, pattern, score, bound, flag):
        '''
        pattern = key of patternDict --> tuple of patterns of various length
        score = value of patternDict --> associated score to pattern
        bound = dictionary with ordinal position numbers as key
                and integers (should be the score associated to the position) as value
        flag = +1 if want to add the score, -1 if want to remove the score from the bound
        '''
        # set unit directions
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1)]
        # prepare column, row, length, count
        length = len(pattern)
        count = 0

        # loop through all 4 directions
        for dir in directions:
            # find number of squares (max 5) that we can go back in each direction 
            # to check for the pattern indicated as parameter
            if dir[0] * dir[1] == 0:
                steps_back = dir[0] * min(5, j_0) + dir[1] * min(5, i_0)
            elif dir[0] == 1:
                steps_back = min(5, j_0, i_0)
            else:
                steps_back = min(5, N-1-j_0, i_0)
            # very first starting point after finding out number of steps to go back
            i_start = i_0 - steps_back * dir[1]
            j_start = j_0 - steps_back * dir[0]
            # move through all possible patterns in a row/col/diag
            z = 0
            while z <= steps_back:
                # get a new starting point
                i_new = i_start + z*dir[1]
                j_new = j_start + z*dir[0]
                index = 0
                # create a list storing empty positions that are fitted in a pattern
                remember = []
                # see if every square in a checked row/col/diag has the same status to a pattern
                while index < length and self.is_valid(i_new, j_new, state=False) \
                        and self.boardMap[i_new][j_new] == pattern[index]: 
                    # first check if it's the empty position to store
                    # score is also a flag indicating whether modifying the bound
                    if self.is_valid(i_new, j_new):
                        remember.append((i_new, j_new)) 
                    # go through every square
                    i_new = i_new + dir[1]
                    j_new = j_new + dir[0]
                    
                    index += 1

                # if we found one pattern
                if index == length:
                    count += 1
                    for pos in remember:
                        # check whether pos is already present in bound dict
                        if pos not in bound:
                            bound[pos] = 0
                            
                        bound[pos] += flag*score  # update better percentage later in evaluate()
                    z += index
                else:
                    z += 1
        return count
    
    # This method takes in current board's value and intended move, and returns the value after that move is made
    # The idea of this method is to calculate the difference in number of patterns, thus value, 
    # around checked position, then add that difference to current board's value
    # Idea of having a current board score stored is time efficient?
    def evaluate(self, new_i, new_j, board_value, turn, bound):
        '''
        board_value = value of the board updated at each minimax, initialized as 0 
        turn = [1, -1] AI or human turn
        bound = dict of empty playable cells with corresponding score
        '''
        value_before = 0
        value_after = 0
        patternDict = create_pattern_dict() #from evaluation.py
        # check for every pattern in patternDict
        for pattern in patternDict:
            score = patternDict[pattern]
            # for every pattern, count have many there are for new_i and new_j
            # and multiply them by the corresponding score
            value_before += self.counting(new_i, new_j, pattern, abs(score), bound, -1)*score
            # make the move then calculate valueAfter,
            # this time, also update the boundary percentage
            self.boardMap[new_i][new_j] = turn
            value_after += self.counting(new_i, new_j, pattern, abs(score), bound, 1) *score
            # delete the move
            self.boardMap[new_i][new_j] = 0
        return board_value + value_after - value_before

    def ab_pruning(self, depth, board_value, bound, alpha, beta, maximizingPlayer):
        if depth <= 0 or (self.check_result() != None): #or end game
            # print('board value: ',board_value)
            return  board_value #value of current position
        # the maximizing player is AI
        if maximizingPlayer:
            # initializing max value
            max_val = float("-inf")
            # look through the child nodes using function in board.py
            for child in self.child_nodes(bound):
                # child HAVE to be in format of (i,j) or (row, col)
                i, j = child[0], child[1]
                # create a new bound with updated values
                # and evaluate the position if making the move
                new_bound = dict(bound)
                new_val = self.evaluate(i, j, board_value, 1, new_bound)
                self.set_pos_state(i,j,1)
                # update bound based on the new move (i,j)
                self.update_bound(i, j, new_bound) 
                # evaluate position going now at depth-1 when it's the opponent's turn
                eval = self.ab_pruning(depth-1, new_val, new_bound, alpha, beta, False)
                max_val = max(max_val, eval)
                
                if depth == self.depth: # and self.is_valid(i,j):
                    # bound_sorted = sorted(new_bound.items(), key=lambda el: el[1], reverse=True)
                    self.currentI = i
                    self.currentJ = j
                    self.nextValue = new_val
                    self.nextBound = new_bound

                alpha = max(alpha, eval)
                self.set_pos_state(i,j,0) #undoing the move

                if beta <= alpha:
                    break
            return max_val

        else:
            # initializing min value
            min_val = float("inf")
            # look through the child nodes using function in board.py
            for child in self.child_nodes(bound):
                i, j = child[0], child[1]
                new_bound = dict(bound)
                new_val = self.evaluate(i, j, board_value, -1, new_bound)
                self.set_pos_state(i,j,-1) #human
                self.update_bound(i, j, new_bound)
                eval = self.ab_pruning(depth-1, new_val, new_bound, alpha, beta, True)
                min_val = min(min_val, eval)

                if depth == self.depth: # and self.is_valid(i,j):
                    self.currentI = i 
                    self.currentJ = j
                    self.nextValue = new_val
                    self.nextBound = new_bound
        
                beta = min(beta, eval)
                self.set_pos_state(i,j,0) #undoing the move

                if beta <= alpha:
                    break

            return min_val

    # def first_move(self):
    #     self.currentState = 1
    #     i, j = 7, 7
    #     if self.is_valid(i, j):
    #         self.boardMap[7][7] = 1

    def check_result(self):
        if self.is_five(self.currentI, self.currentJ, self.currentState) \
            and self.currentState in (-1, 1):
            return self.currentState
        elif self.emptyCells <= 0:
            # tie result
            return 0
        else:
            return None
    
    def get_winner(self):
        if self.check_result() == 1:
            winner = 'Gomoku AI! '
        if self.check_result() == -1:
            winner = 'Human! '
        return winner

        

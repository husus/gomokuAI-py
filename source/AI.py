import math
import sys
import source.utils as utils

sys.setrecursionlimit(1500)

N = 15 # board size 15x15

class GomokuAI():
    def __init__(self, depth=3):
        self.depth = depth # default depth set to 3
        self.boardMap = [[0 for j in range(N)] for i in range(N)]
        self.currentI = -1
        self.currentJ = -1
        self.nextBound = {} # to store possible moves to be checked (i,j)
        self.boardValue = 0 

        self.turn = 0 
        self.lastPlayed = 0
        self.emptyCells = N * N
        self.patternDict = utils.create_pattern_dict() # dictionary containing all patterns with corresponding score
        
        self.zobristTable = utils.init_zobrist()
        self.rollingHash = 0
        self.TTable = {}

    # Draw board in string format
    def drawBoard(self):
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
    
    # Check whether a move is inside the board and whether it is empty
    def isValid(self, i, j, state=True):
        '''
        if state=True, check also whether the position is empty
        if state=False, only check whether the move is inside the board
        '''
        if i<0 or i>=N or j<0 or j>=N:
            return False
        if state:
            if self.boardMap[i][j] != 0:
                return False
            else:
                return True
        else:
            return True

    # Given a position, change the state and "play" the move
    def setState(self, i, j, state):
        '''
        States:
        0 = empty (.)
        1 = AI (x)
        -1 = human (o)
        '''
        assert state in (-1,0,1), 'The state inserted is not -1, 0 or 1'
        self.boardMap[i][j] = state
        self.lastPlayed = state


    def countDirection(self, i, j, xdir, ydir, state):
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

    # Check whether there are 5 pieces connected (in all 4 directions)
    def isFive(self, i, j, state):
        # 4 directions: horizontal, vertical, 2 diagonals
        directions = [[(-1, 0), (1, 0)], \
                      [(0, -1), (0, 1)], \
                      [(-1, 1), (1, -1)], \
                      [(-1, -1), (1, 1)]]
        for axis in directions:
            axis_count = 1
            for (xdir, ydir) in axis:
                axis_count += self.countDirection(i, j, xdir, ydir, state)
                if axis_count >= 5:
                    return True
        return False

    # Return all possible child moves (i,j) in a board status given the bound
    # Sorted in ascending order based on their value
    def childNodes(self, bound):
        for pos in sorted(bound.items(), key=lambda el: el[1], reverse=True):
            yield pos[0]

    # Update boundary for new possible moves given the recently played move
    def updateBound(self, new_i, new_j, bound):
        # get rid of the played position
        played = (new_i, new_j)
        if played in bound:
            bound.pop(played)
        # check in all 8 directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1), (-1, -1), (1, 1)]
        for dir in directions:
            new_col = new_j + dir[0]
            new_row = new_i + dir[1]
            if self.isValid(new_row, new_col)\
                    and (new_row, new_col) not in bound: 
                bound[(new_row, new_col)] = 0
    
    # This method takes in (i, j) position and check the presence of the pattern   
    # and how many there are around that position (horizontally, vertically and diagonally)
    def countPattern(self, i_0, j_0, pattern, score, bound, flag):
        '''
        pattern = key of patternDict --> tuple of patterns of various length
        score = value of patternDict --> associated score to pattern
        bound = dictionary with (i, j) as key and associated cell value as value
        flag = +1 if want to add the score, -1 if want to remove the score from the bound
        '''
        # Set unit directions
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1)]
        # Prepare column, row, length, count
        length = len(pattern)
        count = 0

        # Loop through all 4 directions
        for dir in directions:
            # Find number of squares (max 5) that we can go back in each direction 
            # to check for the pattern indicated as parameter
            if dir[0] * dir[1] == 0:
                steps_back = dir[0] * min(5, j_0) + dir[1] * min(5, i_0)
            elif dir[0] == 1:
                steps_back = min(5, j_0, i_0)
            else:
                steps_back = min(5, N-1-j_0, i_0)
            # Very first starting point after finding out number of steps to go back
            i_start = i_0 - steps_back * dir[1]
            j_start = j_0 - steps_back * dir[0]

            # Move through all possible patterns in a row/col/diag
            z = 0
            while z <= steps_back:
                # Get a new starting point
                i_new = i_start + z*dir[1]
                j_new = j_start + z*dir[0]
                index = 0
                # Create a list storing empty positions that are fitted in a pattern
                remember = []
                # See if every square in a checked row/col/diag has the same status to a pattern
                while index < length and self.isValid(i_new, j_new, state=False) \
                        and self.boardMap[i_new][j_new] == pattern[index]: 
                    if self.isValid(i_new, j_new):
                        remember.append((i_new, j_new)) 
                    
                    i_new = i_new + dir[1]
                    j_new = j_new + dir[0]
                    index += 1

                # If we found one pattern
                if index == length:
                    count += 1
                    for pos in remember:
                        # Check whether pos is already present in bound dict
                        if pos not in bound:
                            bound[pos] = 0
                        bound[pos] += flag*score  # Update better percentage later in evaluate()
                    z += index
                else:
                    z += 1

        return count
    
    # This method takes in current board's value and intended move, and returns the value after that move is made
    # The idea of this method is to calculate the difference in number of patterns, thus value, 
    # around checked position, then add that difference to current board's value
    def evaluate(self, new_i, new_j, board_value, turn, bound):
        '''
        board_value = value of the board updated at each minimax and initialized as 0 
        turn = [1, -1] AI or human turn
        bound = dict of empty playable cells with corresponding score
        '''
        value_before = 0
        value_after = 0
        
        # Check for every pattern in patternDict
        for pattern in self.patternDict:
            score = self.patternDict[pattern]
            # For every pattern, count have many there are for new_i and new_j
            # and multiply them by the corresponding score
            value_before += self.countPattern(new_i, new_j, pattern, abs(score), bound, -1)*score
            # Make the move then calculate value_after
            self.boardMap[new_i][new_j] = turn
            value_after += self.countPattern(new_i, new_j, pattern, abs(score), bound, 1) *score
            
            # Delete the move
            self.boardMap[new_i][new_j] = 0

        return board_value + value_after - value_before

    ### MiniMax algorithm with AlphaBeta Pruning ###
    def alphaBetaPruning(self, depth, board_value, bound, alpha, beta, maximizingPlayer):

        if depth <= 0 or (self.checkResult() != None):
            return  board_value # Static evaluation
        
        # Transposition table of the format {hash: [score, depth]}
        if self.rollingHash in self.TTable and self.TTable[self.rollingHash][1] >= depth:
            return self.TTable[self.rollingHash][0] #return board value stored in TTable
        
        # AI is the maximizing player 
        if maximizingPlayer:
            # Initializing max value
            max_val = -math.inf

            # Look through the all possible child nodes
            for child in self.childNodes(bound):
                i, j = child[0], child[1]
                # Create a new bound with updated values
                # and evaluate the position if making the move
                new_bound = dict(bound)
                new_val = self.evaluate(i, j, board_value, 1, new_bound)
                
                # Make the move and update zobrist hash
                self.boardMap[i][j] = 1
                self.rollingHash ^= self.zobristTable[i][j][0] # index 0 for AI moves

                # Update bound based on the new move (i,j)
                self.updateBound(i, j, new_bound) 

                # Evaluate position going now at depth-1 and it's the opponent's turn
                eval = self.alphaBetaPruning(depth-1, new_val, new_bound, alpha, beta, False)
                if eval > max_val:
                    max_val = eval
                    if depth == self.depth: 
                        self.currentI = i
                        self.currentJ = j
                        self.boardValue = eval
                        self.nextBound = new_bound
                alpha = max(alpha, eval)

                # Undo the move and update again zobrist hashing
                self.boardMap[i][j] = 0 
                self.rollingHash ^= self.zobristTable[i][j][0]
                
                del new_bound
                if beta <= alpha: # prune
                    break

            # Update Transposition Table
            utils.update_TTable(self.TTable, self.rollingHash, max_val, depth)

            return max_val

        else:
            # Initializing min value
            min_val = math.inf
            # Look through the all possible child nodes
            for child in self.childNodes(bound):
                i, j = child[0], child[1]
                # Create a new bound with updated values
                # and evaluate the position if making the move
                new_bound = dict(bound)
                new_val = self.evaluate(i, j, board_value, -1, new_bound)

                # Make the move and update zobrist hash
                self.boardMap[i][j] = -1 
                self.rollingHash ^= self.zobristTable[i][j][1] # index 1 for human moves

                # Update bound based on the new move (i,j)
                self.updateBound(i, j, new_bound)

                # Evaluate position going now at depth-1 and it's the opponent's turn
                eval = self.alphaBetaPruning(depth-1, new_val, new_bound, alpha, beta, True)
                if eval < min_val:
                    min_val = eval
                    if depth == self.depth: 
                        self.currentI = i 
                        self.currentJ = j
                        self.boardValue = eval 
                        self.nextBound = new_bound
                beta = min(beta, eval)
                
                # Undo the move and update again zobrist hashing
                self.boardMap[i][j] = 0 
                self.rollingHash ^= self.zobristTable[i][j][1]

                del new_bound
                if beta <= alpha: # prune
                    break

            # Update Transposition Table
            utils.update_TTable(self.TTable, self.rollingHash, min_val, depth)

            return min_val

    # Set the first move of the AI in (7,7) the center of the board
    def firstMove(self):
        self.currentI, self.currentJ = 7,7
        self.setState(self.currentI, self.currentJ, 1)

    # Check whether the game has ended and returns the winner if there is
    # otherwise, if there are no empty cells left, it's tie
    def checkResult(self):
        if self.isFive(self.currentI, self.currentJ, self.lastPlayed) \
            and self.lastPlayed in (-1, 1):
            return self.lastPlayed
        elif self.emptyCells <= 0:
            # tie
            return 0
        else:
            return None
    
    def getWinner(self):
        if self.checkResult() == 1:
            return 'Gomoku AI! '
        if self.checkResult() == -1:
            return 'Human! '
        else:
            return 'None'

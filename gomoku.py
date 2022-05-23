from board import *
from AI import *
from evaluation import *
import math
import ast
import time



def move(ai, turn, bound):
    assert turn in [-1, 1], '`turn` argument must be -1 or 1'

    # while ai.check_result() == None:
    # AI's turn
    if turn == 1:
        start_time = time.time()
        print('AI bound before ab: ', bound.keys())
        ai.ab_pruning(depth, board_value, bound, -math.inf, math.inf, True)
        end_time = time.time()
        print('finished ab prune in: ', end_time - start_time)
        print('AI bound before move: ', bound.keys())
        
        if ai.is_valid(ai.currentI, ai.currentJ):
            move_i = ai.currentI
            move_j = ai.currentJ
            bound = ai.update_bound(move_i, move_j, bound)
            ai.nextBound = bound
            print('AI bound after: ', bound.keys())
        else:
            print('move not valid: ',ai.currentI,ai.currentJ)
            bound_sorted = sorted(bound.items() , key=lambda el: el[1], reverse=True)
            pos = get_position(bound_sorted[0][0],N)
            move_i = pos[0]
            move_j = pos[1]
            bound = ai.update_bound(move_i, move_j, bound)
            ai.nextBound = bound
            print('AI bound after: ', bound.keys())

            
        # board_value = ai.nextValue
        # bound = ai.nextBound
        # ai.boardMap[move_i][move_j] = 1        
        # setattr(ai, 'currentState', 1)
        # ai.set_pos_state(move_i, move_j, 1)
                
        # ai.draw_board()

    # Human's turn
    elif turn == -1:
        while True:
            human_move = ast.literal_eval(input("Type your move in the form `[row, col]`: "))
            move_i = human_move[0]
            move_j = human_move[1]
            if ai.is_valid(move_i, move_j):
                # print('human bond dict: ',bound)
                # if bound is None:
                #     bound = {get_number(row1, col1, N): 1}
                ai.currentI = move_i
                ai.currentJ = move_j
                print('user bound before: ', bound.keys())
                bound = ai.update_bound(move_i, move_j, bound)
                ai.set_pos_state(move_i, move_j, turn)
                ai.nextBound = bound
                print('user bound after: ', bound.keys())
                ai.nextValue = ai.evaluate(move_i, move_j, board_value, -1, bound) #creating problem with bound update
                # print('bound after evaluate: ', bound.keys())
                # ai.set_pos_state(row1, col1, -1)
                # print('human move value: ', ai.nextValue)
                # ai.draw_board()
                break
            else:
                print('Input not valid. Please enter your move again.')        

        # if ai.check_result() == None:
        #     ai.currentState = 1
        #     turn = ai.currentState
        #     move(ai, turn, bound)
        #     ai.draw_board()
        # else:
        #     pass

    print('output bound: ',ai.nextBound.keys())
    # print('output nextBound: ',ai.nextBound.keys())

    return move_i, move_j, bound

def get_winner(ai):
    if ai.check_result() == 1:
        winner = 'AI'
    if ai.check_result() == -1:
        winner = 'human'
    return winner


def play(ai):
    # AI = GomokuAI(3)
    # draw_board(board)
    bound = ai.nextBound
    board = ai.boardMap
    ai.draw_board()
    user_choice = input('Please choose black or white [b/w]: ')
    if user_choice == 'b':
        ai.currentState = -1
        turn = ai.currentState
        move_i, move_j, bound = move(ai, turn, bound)
        # human_move = ast.literal_eval(input("Type your move in the form `[row, col]`: "))
        # row1 = human_move[0]
        # col1 = human_move[1]
        # ai.boardMap[row1][col1] = -1

    elif user_choice == 'w':
        ai.currentState = 1
        turn = ai.currentState
        # AI makes first move in the center and saving in the board map
        move_i, move_j = 7, 7
        
        # initialize bound
        # bound = {get_number(7,7,N): 1}
        # ai.currentState = -1
        # turn = ai.currentState

    else:
        'Please enter a valid key, either b or w.'
    
    print('initial turn: ', turn)
    print('initial move i,j: ', move_i, move_j)
    # set_state(ai.boardMap, move_i, move_j, turn)
    ai.set_pos_state(move_i, move_j, turn)
    ai.currentI, ai.currentJ = move_i, move_j

    ai.draw_board()
    

    while ai.check_result() == None:
        print('currentState: ', ai.currentState)
        # ai.currentState *= -1 #switch the turn
        # turn = ai.currentState
        # print('turn: ', turn)
        turn *= -1
        # print('new currentState: ', ai.currentState)
        # if turn == -1:
        #     i, j = ai.currentI, ai.currentJ
        # print('new turn: ', turn)
        move_i, move_j, bound = move(ai, turn, bound)
        ai.currentI, ai.currentJ, ai.nextBound = move_i, move_j, bound
        # set_state(board, move_i, move_j, turn)
        ai.set_pos_state(move_i, move_j, turn)
        print('move i,j set: ', move_i, move_j)

        # print('following board print')
        ai.draw_board()
        ai.check_result()
        
    winner = get_winner(ai)
    print('The winner is: {}!'.format(winner))




AI = GomokuAI(2)
board_map = AI.boardMap
board_value = AI.nextValue
depth = AI.depth 
bound = {}
play(AI)


# TODO:
# - insert is_valid() when AI making a move, otherwise recheck for move validity

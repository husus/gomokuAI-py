from board import *
from AI import *
from evaluation import *
import math
import ast

AI = GomokuAI(3)
board_value = AI.nextValue
depth = AI.depth 
bound = {get_number(7,7,N): 1}


def move(ai, turn, bound):
    assert turn in [-1, 1], '`turn` argument must be -1 or 1'

    # while ai.check_result() == None:
    # AI's turn
    if turn == 1:
        ai.ab_pruning(depth, board_value, bound, -math.inf, math.inf, True)
        # print(value)
        # print('this is: ',bound)
        print('finished ab prune')
        move_i = ai.nextI
        move_j = ai.nextJ
        # board_value = ai.nextValue
        bound = ai.nextBound
        # ai.boardMap[move_i][move_j] = 1        
        # setattr(ai, 'currentState', 1)
        ai.set_pos_state(move_i, move_j, 1)
        ai.update_bound(move_i, move_j, bound)
        ai.draw_board()
        if ai.check_result() == None:
            ai.currentState = -1
            turn = ai.currentState
            move(ai, turn, bound)
        else:
            pass

    # Human's turn
    elif turn == -1:
        human_move = ast.literal_eval(input("Type your move in the form `[row, col]`: "))
        row1 = human_move[0]
        col1 = human_move[1]
        if ai.is_valid(row1, col1):
            # ai.set_pos_state(row1, col1, -1)
            print('human bond dict: ',bound)
            if bound is None:
                bound = {get_number(row1, col1, N): 1}
            ai.update_bound(row1, col1, bound)
            ai.nextValue = ai.evaluate(row1, col1, board_value, -1, bound)
            ai.boardMap[row1][col1] = -1
            print('human move value: ', ai.nextValue)
            ai.draw_board()
            # setattr(ai, 'currentState', -1)
            

            # if ai.check_result() == None:
            #     ai.currentState = 1
            #     turn = ai.currentState
            #     move(ai, turn, bound)
            #     ai.draw_board()
            # else:
            #     pass

    

def play(ai, bound):
    # AI = GomokuAI(3)
    ai.draw_board()
    user_choice = input('Please choose black or white [b/w]: ')
    if user_choice == 'b':
        ai.currentState = -1
        turn = ai.currentState
        # human_move = ast.literal_eval(input("Type your move in the form `[row, col]`: "))
        # row1 = human_move[0]
        # col1 = human_move[1]
        # ai.boardMap[row1][col1] = -1

    elif user_choice == 'w':
        # AI makes first move in the center
        ai.boardMap[7][7] = 1
        ai.draw_board()
        # initialize bound
        bound = {get_number(7,7,N): 1}
        ai.currentState = -1
        turn = ai.currentState

    else:
        'Please enter a valid key, either b or w.'
    
    move(ai, turn, bound)
    print('supposed  play second board print')
    # ai.draw_board()
    

    while ai.check_result() == None:
        ai.currentState *= -1 #switch the turn
        turn = ai.currentState
        move(ai, turn, bound)
        print('play following board print')
        ai.draw_board()
        ai.check_result()


    if ai.check_result() == 1:
        winner = 'AI'
    elif ai.check_result() == -1:
        winner = 'human'
    print('The winner is: {}!'.format(winner))
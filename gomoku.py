from board import *
from AI import *
from evaluation import *
import math
import ast

AI = GomokuAI(3)
# global board_value, depth, bound
board_value = AI.nextValue
depth = AI.depth 
bound = {get_number(7,7,N): 1}


def move(ai, turn, bound):
    assert turn in [-1, 1], 'Enter -1 or 1 for `turn` argument'

    while ai.check_result() != None:
        # AI's turn
        if turn == 1:
            ai.ab_pruning(depth, board_value, bound, -math.inf, math.inf, True)
            print('this is: ',bound)
            move_i = ai.nextI
            move_j = ai.nextJ
            # board_value = ai.nextValue
            # bound = ai.nextBound
            ai.boardMap[move_i][move_j] = 1        
            setattr(ai, 'currentState', 1)
            ai.update_bound(move_i, move_j, bound)
            ai.draw_board()
            if ai.check_result() == None:
                turn = -1
                move(ai, turn, bound)
            else:
                winner = 'AI' if ai.check_result==1 else 'human'
                break

        # Human's turn
        elif turn == -1:
            human_move = ast.literal_eval(input("Type your move in the form `[row, col]`: "))
            row1 = human_move[0]
            col1 = human_move[1]
            print('this is: 2 ',bound)
            if ai.is_valid(row1, col1):
                ai.boardMap[row1][col1] = -1
                print('this is: 3 ',bound)
                if bound is None:
                    bound = {get_number(row1, col1, N): 1}
                ai.update_bound(row1, col1, bound)
                ai.nextValue = ai.evaluate(row1, col1, board_value, -1, bound)
                setattr(ai, 'currentState', -1)
                ai.draw_board()

                if ai.check_result() == None:
                    turn = -1
                    move(ai, turn, bound)
                else:
                    winner = 'AI' if ai.check_result==1 else 'human'
                    print('The winner is: {}!'.format(winner))
                    break
    
    


def play(ai, bound):
    # AI = GomokuAI(3)
    ai.draw_board()
    user_choice = input('Please choose black or white [b/w]: ')
    if user_choice == 'b':
        turn = -1
        ai.currentState = turn
        human_move = ast.literal_eval(input("Type your move in the form `[row, col]`: "))
        row1 = human_move[0]
        col1 = human_move[1]
        # bound = {get_number(7,7,N): 1}
        ai.boardMap[row1][col1] = -1
        ai.draw_board()

    elif user_choice == 'w':
        turn = 1
        ai.currentState = turn
        ai.boardMap[7][7] = 1
        # bound = {get_number(7,7,N): 1}
        ai.draw_board()

    else:
        'Please enter a valid key, either b or w.'
    move(ai, turn, bound)
    ai.draw_board()

    while ai.check_result() == None:
        move(ai, turn, bound)
        ai.draw_board()
        turn *= -1
        ai.check_result()


    if ai.check_result() == 1:
        winner = 'AI'
    elif ai.check_result() == -1:
        winner = 'human'
    print('The winner is: {}!'.format(winner))
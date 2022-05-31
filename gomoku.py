from AI import *
from evaluation import *
import math
import ast
import time



def move(ai, turn, bound):
    assert turn in [-1, 1], '`turn` argument must be -1 or 1'

    if turn == 1:
        start_time = time.time()
        ai.ab_pruning(depth, board_value, bound, -math.inf, math.inf, True)
        end_time = time.time()
        print('finished ab prune in: ', end_time - start_time)
        
        if ai.is_valid(ai.currentI, ai.currentJ):
            bound_sorted = sorted(ai.nextBound.items(), key=lambda el: el[1], reverse=True)
            pos = bound_sorted[0][0]
            move_i = pos[0]
            move_j = pos[1]
            bound = ai.update_bound(move_i, move_j, bound)
            ai.nextBound = bound
            
        else:
            print('move not valid: ',ai.currentI,ai.currentJ)
            bound_sorted = sorted(bound.items() , key=lambda el: el[1], reverse=True)
            pos = bound_sorted[0][0]
            move_i = pos[0]
            move_j = pos[1]
            bound = ai.update_bound(move_i, move_j, bound)
            ai.nextBound = bound

    # Human's turn
    elif turn == -1:
        while True:
            human_move = ast.literal_eval(input("Type your move in the form `[row, col]`: "))
            move_i = human_move[0]
            move_j = human_move[1]

            if ai.is_valid(move_i, move_j):
                # ai.currentI = move_i
                # ai.currentJ = move_j
                ai.nextValue = ai.evaluate(move_i, move_j, board_value, -1, bound) #creating problem with bound update
                ai.set_pos_state(move_i, move_j, turn)
                bound = ai.update_bound(move_i, move_j, bound)
                ai.nextBound = bound
                break
            
            else:
                print('Input not valid. Please enter your move again.')        

    return move_i, move_j

def get_winner(ai):
    if ai.check_result() == 1:
        winner = 'AI'
    if ai.check_result() == -1:
        winner = 'human'
    else:
        winner = 'tie'
    return winner


def play(ai):
    bound = ai.nextBound
    ai.draw_board()

    while True:
        user_choice = input('Please choose black or white [b/w]: ')

        if user_choice == 'b':
            ai.currentState = -1
            turn = ai.currentState
            move_i, move_j = move(ai, turn, bound)
            break

        elif user_choice == 'w':
            ai.currentState = 1
            turn = ai.currentState
            # AI makes first move in the center and saving in the board map
            move_i, move_j = 7, 7
            break

        else:
            'Please enter a valid key, either b or w.'
    

    print('initial move i,j: ', move_i, move_j)
    ai.set_pos_state(move_i, move_j, turn)
    # ai.currentI, ai.currentJ = move_i, move_j

    ai.draw_board()
    

    while ai.check_result() == None:
        ai.currentState *= -1
        turn = ai.currentState
        
        move_i, move_j = move(ai, turn, ai.nextBound)
        ai.currentI, ai.currentJ = move_i, move_j
        ai.set_pos_state(move_i, move_j, turn)
        # add update bound? alreday incorporated in move()
        print('move i,j set: ', move_i, move_j)

        ai.draw_board()
        ai.check_result()
        
    winner = get_winner(ai)
    print('The winner is: {}!'.format(winner))




AI = GomokuAI(3)
board_map = AI.boardMap
board_value = AI.nextValue
depth = AI.depth 
bound = {}
play(AI)


# TODO:
# 
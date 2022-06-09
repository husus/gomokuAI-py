import math
import time
from AI import *
from interface import * 


def ai_move(ai):
    start_time = time.time()
    ai.AlphaBetaPruning(ai.depth, ai.boardValue, ai.nextBound, -math.inf, math.inf, True)
    end_time = time.time()
    print('finished ab prune in: ', end_time - start_time)
    
    if ai.isValid(ai.currentI, ai.currentJ):
        bound_sorted = sorted(ai.nextBound.items(), key=lambda el: el[1], reverse=True)
        pos = bound_sorted[0][0]
        move_i = pos[0]
        move_j = pos[1]
        ai.updateBound(move_i, move_j, ai.nextBound)
        # ai.nextBound = bound  
    else:
        print('Error: i and j not valid.')
        ai.AlphaBetaPruning(ai.depth, ai.boardValue, ai.nextBound, -math.inf, math.inf, True)

    return move_i, move_j

def check_human_move(ai, mouse_pos):
    # Human's turn
    # human_move = ast.literal_eval(input("Type your move in the form `[row, col]`: "))
    human_move = pos_pixel2map(mouse_pos[0], mouse_pos[1])
    move_i = human_move[0]
    move_j = human_move[1]
    
    bound = ai.nextBound
    if ai.isValid(move_i, move_j):
        ai.boardValue = ai.evaluate(move_i, move_j, ai.boardValue, -1, bound)
        ai.setState(move_i, move_j, -1)
        ai.updateBound(move_i, move_j, bound)
        ai.nextBound = bound
        return move_i, move_j

    else:
        print('Input not valid. Please select your move again.')  

import math
# import ast 
import time
import pygame
from AI import *
from evaluation import *
from interface import * 


def move(ai, turn, bound):
    # assert turn in [-1, 1], '`turn` argument must be -1 or 1'

    if turn == 1:
        start_time = time.time()
        ai.ab_pruning(ai.depth, ai.nextValue, bound, -math.inf, math.inf, True)
        end_time = time.time()
        print('finished ab prune in: ', end_time - start_time)
        
        if ai.is_valid(ai.currentI, ai.currentJ):
            bound_sorted = sorted(bound.items(), key=lambda el: el[1], reverse=True)
            pos = bound_sorted[0][0]
            move_i = pos[0]
            move_j = pos[1]
            ai.update_bound(move_i, move_j, bound)
            ai.nextBound = bound
            
        else:
            print('Error: i and j not valid.')

    # Human's turn
    elif turn == -1:
        # human_move = ast.literal_eval(input("Type your move in the form `[row, col]`: "))
        
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            mouse_pos = pygame.mouse.get_pos()
            human_move = pos_pixel2map(mouse_pos[0], mouse_pos[1])
            move_i = human_move[0]
            move_j = human_move[1]

            if ai.is_valid(move_i, move_j):
                ai.nextValue = ai.evaluate(move_i, move_j, ai.nextValue, -1, bound)
                ai.set_pos_state(move_i, move_j, turn)
                ai.update_bound(move_i, move_j, bound)
                ai.nextBound = bound

            else:
                print('Input not valid. Please select your move again.')   

    return move_i, move_j     

            


# To be removed??
# def first_move(ai, mouse_pos):
#     if ai.colorState[-1] == 'black':
#         ai.currentState = -1
#         turn = ai.currentState
#         move_i, move_j = move(ai, turn, mouse_pos, ai.nextBound)
#     if ai.colorState[-1] == 'white':
#         ai.currentState = 1
#         turn = ai.currentState
#         # AI makes first move in the center and saving in the board map
#         move_i, move_j = 7,7
#     return move_i, move_j 

# def play(ai):
#     bound = ai.nextBound
#     ai.draw_board()

#     while True:
#         user_choice = input('Please choose black or white [b/w]: ')

#         if user_choice == 'b':
#             ai.currentState = -1
#             turn = ai.currentState
#             move_i, move_j = move(ai, turn, bound)
#             break

#         elif user_choice == 'w':
#             ai.currentState = 1
#             turn = ai.currentState
#             # AI makes first move in the center and saving in the board map
#             move_i, move_j = 7, 7
#             break

#         else:
#             'Please enter a valid key, either b or w.'
    

#     ai.colorState[turn] = 'black'
#     ai.colorState[turn*-1] = 'white'
#     print('initial move i,j: ', move_i, move_j)
#     ai.set_pos_state(move_i, move_j, turn)
#     # ai.currentI, ai.currentJ = move_i, move_j

#     ai.draw_board()
    

#     while ai.check_result() == None:
#         ai.currentState *= -1
#         turn = ai.currentState
        
#         move_i, move_j = move(ai, turn, bound)
#         ai.currentI, ai.currentJ = move_i, move_j
#         ai.set_pos_state(move_i, move_j, turn)
#         # add update bound? alreday incorporated in move()
#         print('move i,j set: ', move_i, move_j)

#         ai.draw_board()
#         ai.check_result()
        
#     winner = get_winner(ai)
#     print('The winner is: {}!'.format(winner))




# if __name__ == '__main__':
#     AI = GomokuAI(3)
#     global depth, board_value, bound
#     depth = AI.depth
#     board_value = AI.nextValue
#     bound = AI.nextBound
#     play(AI)


# TODO:
# 
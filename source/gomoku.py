import math
import time
import pygame
from source.AI import *
from gui.interface import *
import source.utils as utils 

pygame.init()

def ai_move(ai):
    start_time = time.time()
    ai.alphaBetaPruning(ai.depth, ai.boardValue, ai.nextBound, -math.inf, math.inf, True)
    end_time = time.time()
    print('Finished ab prune in: ', end_time - start_time)
    
    if ai.isValid(ai.currentI, ai.currentJ):
        move_i, move_j = ai.currentI, ai.currentJ
        print(move_i, move_j)
        ai.updateBound(move_i, move_j, ai.nextBound)
        
    else:
        print('Error: i and j not valid. Given: ', ai.currentI, ai.currentJ)
        ai.updateBound(ai.currentI, ai.currentJ, ai.nextBound)
        bound_sorted = sorted(ai.nextBound.items(), key=lambda el: el[1], reverse=True)
        pos = bound_sorted[0][0]
        move_i = pos[0]
        move_j = pos[1]
        ai.currentI, ai.currentJ = move_i, move_j
        
        print(move_i, move_j)
    
    return move_i, move_j

def check_human_move(ai, mouse_pos):
    # Human's turn
    human_move = utils.pos_pixel2map(mouse_pos[0], mouse_pos[1])
    move_i = human_move[0]
    move_j = human_move[1]
    
    if ai.isValid(move_i, move_j):
        ai.boardValue = ai.evaluate(move_i, move_j, ai.boardValue, -1, ai.nextBound)
        ai.setState(move_i, move_j, -1)
        # ai.currentI, ai.currentJ = move_i, move_j
        ai.updateBound(move_i, move_j, ai.nextBound)
        # ai.nextBound = bound
        return move_i, move_j


def check_results(ui, result):
    if result == 0:
        print("it's a tie!")
        ui.drawResult(tie=True)
    else:
        ui.drawResult()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN\
                    and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                ui.restartChoice(mouse_pos)
    


from interface import *
from AI import *
import gomoku
import pygame

# Game initializer function
# Link interface with gomoku moves and AI
# Script to be run

# def play_gomoku(ai, ui):
#     # print(ai.currentState)
#     turn = ai.currentState
#     bound = ai.nextBound
#     i, j = gomoku.move(ai, turn, bound)
#     ai.set_pos_state(i, j, turn)
#     ui.draw_piece(ui.colorState[turn], i, j)
#     pygame.display.update()
#     ai.currentState *= -1
    

if __name__ == '__main__':

    ai = GomokuAI(3)
    game = GameUI(ai)
    game.screen.blit(game.board, (0,0))
    game.draw_menu()
    pygame.display.update()
    # global mapping
    # mapping = create_mapping()

    run = True
    end = False
    while run:
        if game.ai.currentState == 0: #if no move has been made yet
            game.menu_choice()
            continue
        
        result = game.ai.get_winner()
        while result is None and game.ai.currentState!=0:
            turn = game.ai.currentState
            color = game.colorState[turn]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if turn == 1:
                    move_i, move_j = gomoku.ai_move(game.ai)
                    game.ai.set_pos_state(move_i, move_j, turn)
                    # ai.currentI, ai.currentJ = move_i, move_j
                    game.ai.emptyCells -= 1
                    game.draw_piece(color, move_i, move_j)
                    result = game.ai.get_winner()
                    game.ai.currentState *= -1

                elif turn == -1:
                    if event.type == pygame.MOUSEBUTTONDOWN\
                        and pygame.mouse.get_pressed()[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        human_move = pos_pixel2map(mouse_pos[0], mouse_pos[1])
                        move_i = human_move[0]
                        move_j = human_move[1]
                        print(mouse_pos, move_i, move_j)

                        if game.ai.is_valid(move_i, move_j):
                            game.ai.nextValue = game.ai.evaluate(move_i, move_j, game.ai.nextValue, -1, game.ai.nextBound)
                            game.ai.update_bound(move_i, move_j, game.ai.nextBound)
                            # ai.nextBound = bound
                            game.ai.currentI, game.ai.currentJ = move_i, move_j
                            game.ai.set_pos_state(move_i, move_j, turn)
                            game.ai.emptyCells -= 1
                            game.draw_piece(color, move_i, move_j)
                            result = game.ai.get_winner()
                            game.ai.currentState *= -1
                    else:
                        continue
            
        # if result == 0:
        #     print("it's a tie!")
        #     game.draw_result(tie=True)
        #     end = True
        if result != None:
            print('play.py: ',result, game.ai.get_winner())
            game.draw_result()
            game.ai.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN\
                    and pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    game.restart_decision(mouse_pos)

            end = True

        # if end:
        #     pass
        pygame.display.update()
               
    pygame.quit()

from interface import *
from AI import *
import gomoku
import pygame

# Game initializer function
# Link interface with gomoku moves and AI
# Script to be run

def play_gomoku(ai, ui):
    # print(ai.currentState)
    turn = ai.currentState
    bound = ai.nextBound
    i, j = gomoku.move(ai, turn, bound)
    ai.set_pos_state(i, j, turn)
    ui.draw_piece(ui.colorState[turn], i, j)
    pygame.display.update()
    ai.currentState *= -1
    

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN\
                and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if ai.currentState == 0: #if no move has been made yet
                    game.check_color_choice(pos)
                    game.screen.blit(game.board, (0,0))
                    pygame.display.update()
                    if ai.currentState == 1:
                        # set the first move of the AI at the center
                        game.draw_piece('black', 7, 7)
                        pygame.display.update()
                        ai.currentState *= -1
                    continue

                play_gomoku(ai, game)
                
                if ai.check_result() == 0:
                    print("it's a tie!")
                    game.draw_result(tie=True)
                    end = True
                elif ai.check_result() in (-1, 1):
                    game.draw_result()
                    ai.draw_board()
                    print(ai.check_result())
                    end = True

        # if end:
        #     pass

               
    pygame.quit()

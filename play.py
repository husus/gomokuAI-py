from interface import *
from AI import *
import gomoku
import pygame

menu_font = pygame.font.SysFont("arial", 22)

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
    button_black = Button(game.buttonSurf, 200, 300, "BLACK", menu_font)
    button_white = Button(game.buttonSurf, 340, 300, "WHITE", menu_font)
    game.screen.blit(game.board, (0,0))
    game.drawMenu()
    pygame.display.update()

    run = True
    while run:
        if game.ai.currentState == 0: #if no move has been made yet
            game.drawButtons(button_black, button_white, game.screen)
            game.menuChoice()
            # pygame.display.update()
            continue
        
        result = game.ai.checkResult()
        while result is None and game.ai.currentState!=0:
            turn = game.ai.currentState
            color = game.colorState[turn]
            game.ai.updateBound(game.ai.currentI, game.ai.currentJ, game.ai.nextBound)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if turn == 1:
                    move_i, move_j = gomoku.ai_move(game.ai)
                    game.ai.setState(move_i, move_j, turn)
                    game.ai.rollingHash ^= game.ai.zobristTable[move_i][move_j][0]
                    # ai.currentI, ai.currentJ = move_i, move_j
                    game.ai.emptyCells -= 1
                    game.drawPiece(color, move_i, move_j)
                    result = game.ai.checkResult()
                    game.ai.currentState *= -1

                elif turn == -1:
                    if event.type == pygame.MOUSEBUTTONDOWN\
                        and pygame.mouse.get_pressed()[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        human_move = utils.pos_pixel2map(mouse_pos[0], mouse_pos[1])
                        move_i = human_move[0]
                        move_j = human_move[1]
                        print(mouse_pos, move_i, move_j)

                        if game.ai.isValid(move_i, move_j):
                            game.ai.boardValue = game.ai.evaluate(move_i, move_j, game.ai.boardValue, -1, game.ai.nextBound)
                            game.ai.updateBound(move_i, move_j, game.ai.nextBound)
                            # ai.nextBound = bound
                            game.ai.currentI, game.ai.currentJ = move_i, move_j
                            game.ai.setState(move_i, move_j, turn)
                            game.ai.rollingHash ^= game.ai.zobristTable[move_i][move_j][1]
                            game.ai.emptyCells -= 1
                            game.drawPiece(color, move_i, move_j)
                            result =  game.ai.checkResult()
                            game.ai.currentState *= -1
                else:
                    continue
    
        
        pygame.display.flip()
        print('result before: ', game.ai.currentState)
        game.ai.currentState *= -1
        print('result after: ', game.ai.currentState)
        last_screen = game.screen.copy()
        game.screen.blit(last_screen, (0,0))
        while result != None:
            if result == 0:
                print("it's a tie!")
                game.drawResult(tie=True)
            else:
                game.drawResult()
            # game.ai.drawBoard()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN\
                    and pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    choice = game.restartChoice(mouse_pos)
                    print(choice)
                    if not choice:
                        run = False
                    else:
                        run = True
                        print('YES')

        pygame.display.update()
               
    pygame.quit()

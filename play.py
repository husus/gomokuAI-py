from interface import *
from AI import *
from button import Button
import utils
import gomoku
import pygame

# Game initializer function
# Link interface with gomoku moves and AI
# Script to be run


pygame.init()

def startGame():
    pygame.init()
    ai = GomokuAI(3)
    game = GameUI(ai)
    button_black = Button(game.buttonSurf, 200, 290, "BLACK", 22)
    button_white = Button(game.buttonSurf, 340, 290, "WHITE", 22)
    game.drawMenu()
    game.drawButtons(button_black, button_white, game.screen)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN\
                    and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                game.checkColorChoice(button_black, button_white, mouse_pos)
                print(ai.currentState)
                game.screen.blit(game.board, (0,0))
                pygame.display.update()
                
                if game.ai.currentState == 1:
                    # set the first move of the AI at the center
                    game.drawPiece('black', 7, 7)
                    pygame.display.update()
                    game.ai.currentState *= -1
                
                main(ai, game)

                if game.ai.checkResult() != None:
                    last_screen = game.screen.copy()
                    game.screen.blit(last_screen, (0,0))
                    # endMenu(game, last_screen)
                    game.drawResult()
                    yes_button = Button(game.buttonSurf, 200, 155, "YES", 18)
                    no_button = Button(game.buttonSurf, 350, 155, "NO", 18)
                    game.drawButtons(yes_button, no_button, game.screen)
                    pygame.display.update()
                    mouse_pos = pygame.mouse.get_pos()
                    if yes_button.rect.collidepoint(mouse_pos):
                        print('Selected YES')
                        game.screen.blit(game.board, (0,0))
                        pygame.display.update()
                        startGame()
                    if no_button.rect.collidepoint(mouse_pos):
                        print('Selected NO')
                        pygame.quit()

    print('Out while loop')
    pygame.quit()

def endMenu(game, last_screen):
    pygame.init()
    game.screen.blit(last_screen, (0,0))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            game.drawResult()
            yes_button = Button(game.buttonSurf, 200, 155, "YES", 18)
            no_button = Button(game.buttonSurf, 350, 155, "NO", 18)
            game.drawButtons(yes_button, no_button, game.screen)
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN\
                    and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button.rect.collidepoint(mouse_pos):
                    print('Selected YES')
                    game.screen.blit(game.board, (0,0))
                    pygame.display.update()
                    startGame()
                if no_button.rect.collidepoint(mouse_pos):
                    print('Selected NO')
                    run = False
    pygame.quit()
    



def main(ai, game):
    pygame.init()
    end = False
    result = game.ai.checkResult()
    while not end:
        turn = ai.currentState
        color = game.colorState[turn]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if turn == 1:
                move_i, move_j = gomoku.ai_move(game.ai)
                game.ai.setState(move_i, move_j, turn)
                game.ai.rollingHash ^= game.ai.zobristTable[move_i][move_j][0]
                # ai.currentI, ai.currentJ = move_i, move_j
                game.ai.emptyCells -= 1
                game.drawPiece(color, move_i, move_j)
                result = game.ai.checkResult()
                game.ai.currentState *= -1

            if turn == -1:
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
            
            if result != None:
                end = True

    print('Game Over')


if __name__ == '__main__':
    startGame()

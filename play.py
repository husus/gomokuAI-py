from gui.interface import *
from source.AI import *
from gui.button import Button
import source.utils as utils
import source.gomoku as gomoku
import pygame

# Game initializer function
# Link interface with gomoku moves and AI
# Script to be run


pygame.init()

def startGame():
    pygame.init()
    # Initializations
    ai = GomokuAI()
    game = GameUI(ai)
    button_black = Button(game.buttonSurf, 200, 290, "BLACK", 22)
    button_white = Button(game.buttonSurf, 340, 290, "WHITE", 22)

    # Draw the starting menu
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
                # Check which color the user has chosen and set the states
                game.checkColorChoice(button_black, button_white, mouse_pos)
                game.screen.blit(game.board, (0,0))
                pygame.display.update()
                
                if game.ai.turn == 1:
                    game.ai.firstMove()
                    game.drawPiece('black', game.ai.currentI, game.ai.currentJ)
                    pygame.display.update()
                    game.ai.turn *= -1
                
                main(game)

                # When the game ends and there is a winner, draw the result board
                if game.ai.checkResult() != None:
                    last_screen = game.screen.copy()
                    game.screen.blit(last_screen, (0,0))
                    # endMenu(game, last_screen)
                    game.drawResult()

                    # Setting for asking to the player to restart the game or not 
                    yes_button = Button(game.buttonSurf, 200, 155, "YES", 18)
                    no_button = Button(game.buttonSurf, 350, 155, "NO", 18)
                    game.drawButtons(yes_button, no_button, game.screen)
                    mouse_pos = pygame.mouse.get_pos()
                    if yes_button.rect.collidepoint(mouse_pos):
                        # Restart the game
                        game.screen.blit(game.board, (0,0))
                        pygame.display.update()
                        game.ai.turn = 0
                        startGame()
                    if no_button.rect.collidepoint(mouse_pos):
                        # End the game
                        pygame.quit()
        pygame.display.update()   

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


### Main game play loop ###
def main(game):
    pygame.init()
    end = False
    result = game.ai.checkResult()

    while not end:
        turn = game.ai.turn
        color = game.colorState[turn] # black or white depending on player's choice
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # AI's turn
            if turn == 1:
                move_i, move_j = gomoku.ai_move(game.ai)
                # Make the move and update zobrist hash
                game.ai.setState(move_i, move_j, turn)
                game.ai.rollingHash ^= game.ai.zobristTable[move_i][move_j][0]
                game.ai.emptyCells -= 1

                game.drawPiece(color, move_i, move_j)
                result = game.ai.checkResult()
                # Switch turn
                game.ai.turn *= -1

            # Human's turn
            if turn == -1:
                if event.type == pygame.MOUSEBUTTONDOWN\
                        and pygame.mouse.get_pressed()[0]:
                    # Get human move played
                    mouse_pos = pygame.mouse.get_pos()
                    human_move = utils.pos_pixel2map(mouse_pos[0], mouse_pos[1])
                    move_i = human_move[0]
                    move_j = human_move[1]
                    # print(mouse_pos, move_i, move_j)

                    # Check the validity of human's move
                    if game.ai.isValid(move_i, move_j):
                        game.ai.boardValue = game.ai.evaluate(move_i, move_j, game.ai.boardValue, -1, game.ai.nextBound)
                        game.ai.updateBound(move_i, move_j, game.ai.nextBound)
                        game.ai.currentI, game.ai.currentJ = move_i, move_j
                        # Make the move and update zobrist hash
                        game.ai.setState(move_i, move_j, turn)
                        game.ai.rollingHash ^= game.ai.zobristTable[move_i][move_j][1]
                        game.ai.emptyCells -= 1
                        
                        game.drawPiece(color, move_i, move_j)
                        result =  game.ai.checkResult()
                        game.ai.turn *= -1
            
            if result != None:
                # End game
                end = True



if __name__ == '__main__':
    startGame()
import pygame
import os
# from AI import *
from button import *


SIZE = 540 #size of the board image
PIECE = 32 #size of the single pieces
N = 15
MARGIN = 23
GRID = (SIZE - 2 * MARGIN) / (N-1)

# Elements for the starting menu interface
# MENU_BOARD = pygame.image.load(os.path.join("assets", "menu_board.png")).convert_alpha()
# # MENU_BOARD = pygame.transform.scale(MENU_BOARD, (350, 100))
# BUTTON_SURF = pygame.image.load(os.path.join("assets", "button.png")).convert_alpha()
# BUTTON_SURF = pygame.transform.scale(BUTTON_SURF, (110, 60))


FPS = 60 #how many frames per second to update the window

def pixel_conversion(list_points, target):
    # point of the list from where start the search
    index = int((len(list_points)-1)//2) 

    while True:
        if target < list_points[0]:
            index = 0
            break
        elif target >= list_points[-1]:
            index = len(list_points)-2
            break

        elif list_points[index] > target:
            if list_points[index-1] <= target:
                index -= 1
                break
            else:
                index -= 1

        elif list_points[index] <= target:
            if list_points[index+1] > target:
                break
            else:
                index += 1
    
    return index

def pos_pixel2map(x, y):
    # transform pygame pixel to boardMap coordinates

    start = int(MARGIN - GRID//2)
    end = int(SIZE - MARGIN + GRID//2)
    list_points = [p for p in range(start, end+1, int(GRID))]

    i = pixel_conversion(list_points, y)
    j = pixel_conversion(list_points, x)
    return (i,j)

def pos_map2pixel(i, j):
    # transform boardMap to pygame pixel coordinates
    return (MARGIN + j * GRID - PIECE/2, MARGIN + i * GRID - PIECE/2)

def create_mapping():
    pos_mapping = {}
    for i in range(N):
        for j in range(N):
            spacing = [r for r in range(MARGIN, SIZE-MARGIN+1, int(GRID))]
            pos_mapping[(i,j)] = (spacing[j],spacing[i])
    
    return pos_mapping


class GameUI(object):
    def __init__(self, ai):
        self.ai = ai
        self.colorState = {} #key: turn; value: black/white
        self.mapping = create_mapping()
        
        # initialize pygame
        pygame.init()

        self.screen = pygame.display.set_mode((SIZE, SIZE))
        pygame.display.set_caption('Play Gomoku!')

        self.board = pygame.image.load(os.path.join("assets", 'board.jpg')).convert()
        self.blackPiece = pygame.image.load(os.path.join("assets", 'black_piece.png')).convert_alpha()
        self.whitePiece = pygame.image.load(os.path.join("assets", 'white_piece.png')).convert_alpha()
        self.menuBoard = pygame.image.load(os.path.join("assets", "menu_board.png")).convert_alpha()
        self.buttonSurf = pygame.image.load(os.path.join("assets", "button.png")).convert_alpha()
        self.screen.blit(self.board, (0,0))
        pygame.display.update()

    def draw_menu(self): 
        menu_board = pygame.transform.scale(self.menuBoard, (350,100))
        menu_board_rect = menu_board.get_rect(center = self.screen.get_rect().center)

        menu_font = pygame.font.SysFont("arial", 22)
        menu_text = menu_font.render('CHOOSE YOUR COLOR: ', True, 'white')
        menu_board.blit(menu_text, (50,25))
        self.screen.blit(menu_board, menu_board_rect)

        button_surface = pygame.transform.scale(self.buttonSurf, (110, 60)) 
        global button_black, button_white   
        button_black = Button(button_surface, 200, 300, "BLACK", menu_font)
        button_white = Button(button_surface, 340, 300, "WHITE", menu_font)
        button_white.draw_button(self.screen)
        button_black.draw_button(self.screen)
        
        pygame.display.update()

    def check_color_choice(self, pos):
        if button_black.rect.collidepoint(pos):
            self.colorState[-1] = 'black'
            self.colorState[1] = 'white'
            self.ai.currentState = -1
        elif button_white.rect.collidepoint(pos):
            self.colorState[-1] = 'white'
            self.colorState[1] = 'black'
            self.ai.currentState = 1
        print(self.colorState)

    def draw_piece(self, state, i, j):
        
        x, y = self.mapping[(i,j)]
        x = x - PIECE/2
        y = y - PIECE/2

        if state == 'black': 
            self.screen.blit(self.blackPiece, (x, y))
        elif state == 'white':
            self.screen.blit(self.whitePiece, (x, y))

        pygame.display.update()

    def draw_result(self, tie=False):
        menu_board = pygame.transform.scale(self.menuBoard, (400,190))
        # menu_board_rect = menu_board.get_rect(center = self.screen.get_rect().center)
        width, height = menu_board.get_size()
        font = pygame.font.SysFont('arial', 25, True)
        
        if tie:
            text = "It's a TIE! "
            render_text = font.render(str.upper(text), True, 'white')
            # text_rect = render_text.get_rect(center = menu_board.get_rect().center)
            text_size = render_text.get_size()
            (x, y) = (width//2 - text_size[0]//2, height//4 - text_size[1]//2)
            menu_board.blit(render_text, (x, y))
            
        else:
            text = 'The winner is: '
            render_text = font.render(str.upper(text), True, 'white')
            size1 = render_text.get_size()
            (x1, y1) = (width//2 - size1[0]//2, 30)

            winner = self.ai.get_winner()
            print('interface.py: ',winner)
            render_winner = font.render(str.upper(winner), True, 'white')
            size2 = render_winner.get_size()
            (x2, y2) = (width//2 - size2[0]//2, 30 + size1[1])

            menu_board.blit(render_text, (x1, y1))
            menu_board.blit(render_winner, (x2, y2))
        
        restart_font = pygame.font.SysFont('arial', 18)
        restart_text = 'Do you want to play again?'
        render_restart = restart_font.render(str.upper(restart_text), True, 'white')
        restart_size = render_restart.get_size()
        (x3, y3) = (width//2 - restart_size[0]//2, height//2) #- restart_size[1]//2)
        menu_board.blit(render_restart, (x3, y3))

        button_surface = pygame.transform.scale(self.buttonSurf, (90, 50))
        (x4, y4) = (width * 0.25 + 15, height * 0.75)
        (x5, y5) = (width * 0.75 - 15, height * 0.75)
        global yes_button, no_button
        yes_button = Button(button_surface, x4, y4, "YES", restart_font)
        no_button = Button(button_surface, x5, y5, "NO", restart_font)
        yes_button.draw_button(menu_board)
        no_button.draw_button(menu_board)

        self.screen.blit(menu_board, (SIZE//2 - width//2, MARGIN//2))
        pygame.display.update()

    def menu_choice(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN \
                and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                self.check_color_choice(pos)
                self.screen.blit(self.board, (0,0))
                pygame.display.update()
                if self.ai.currentState == 1:
                    # set the first move of the AI at the center
                    self.draw_piece('black', 7, 7)
                    pygame.display.update()
                    self.ai.currentState *= -1


    def restart_decision(self, pos):
        # for event in pygame.event.get():
        #     if event.type == pygame.MOUSEBUTTONDOWN \
        #         and pygame.mouse.get_pressed()[0]:
        # pos = pygame.mouse.get_pos()
        if yes_button.rect.collidepoint(pos):
            print('yes')
            # return True
        elif no_button.rect.collidepoint(pos):
            print('no')
            # return False

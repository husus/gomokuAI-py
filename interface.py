import pygame
import os
from AI import *

SIZE = 540 #size of the board image
PIECE = 32 #size of the single pieces
N = 15
MARGIN = 7
GRID = (SIZE - 2 * MARGIN) / N
# 35x35 size of squares in the board

'''
(23,23) start of internal square --> (7,7)
(517,23) top right end of internal square --> (533,7)
(23,517) bottom left start of internal square --> (7,533)
(517,517) bottom right end of internal square --> (533,533)
'''


SCREEN = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption('Play Gomoku!')

BG = pygame.image.load(os.path.join("assets", 'board.jpg')).convert() #set board image as bg
BLACK_PIECE = pygame.image.load(os.path.join("assets", 'black_piece.png')).convert_alpha()
# BLACK_PIECE = pygame.transform.scale(BLACK_PIECE,(35,35))

WHITE_PIECE = pygame.image.load(os.path.join("assets", 'white_piece.png')).convert_alpha()
# WHITE_PIECE = pygame.transform.scale(WHITE_PIECE,(35,35))

# FPS = 60 #how many frames per second to update the window

# def grid(screen, size, rows):
#     x = 7
#     y = 7
#     cell = size//rows
#     for l in range(rows):
#         x += cell
#         y += cell
#         pygame.draw.line(screen, (255,255,255), (x,7), (x,size))
#         pygame.draw.line(screen, (255,255,255), (7,y), (size,y))

def drawGrid():
    cell = 35 #Set the size of the grid block
    for x in range(SIZE-14):
        for y in range(SIZE-14):
            rect = pygame.Rect(x*cell+7, y*cell+7,
                               cell, cell)
            pygame.draw.rect(SCREEN, (255,255,255), rect, 1)

def draw_window():
    SCREEN.blit(BG, (0,0))
    # SCREEN.blit(BLACK_PIECE, 
    #         (SIZE/2-PIECE/2, SIZE/2-PIECE/2)) #central position of the black piece
    
    # SCREEN.blit(WHITE_PIECE, 
            # (517-PIECE/2,23-PIECE/2))
    
    # rect = pygame.Rect(7,7,526,526)
    # pygame.draw.rect(SCREEN, (255,255,255), rect, 2) #create a square for saving moves

    # grid(SCREEN, 526, N)

    drawGrid()  
    pygame.display.update()

def pos_pixel2map(x, y):
    # transform pygame pixel to boardMap coordinates

    (i, j) = (int(round((y - MARGIN + PIECE / 2) / GRID)),
                int(round((x - MARGIN + PIECE / 2) / GRID)))
    i -= 1
    j -= 1

    if i < 0 or i >= N or j < 0 or j >= N:
        return (None, None)
    else:
        return (i, j)

def pos_map2pixel(i, j):
    # transform boardMap to pygame pixel coordinates

    return (MARGIN + j * GRID - PIECE / 2, MARGIN + i * GRID
            - PIECE / 2)

def draw_piece(state, x, y):
    (x, y) = pygame.mouse.get_pos()

    if state == 1:
        SCREEN.blit(BLACK_PIECE, (x - PIECE / 2, y - PIECE / 2))
    
    elif state == -1:
        SCREEN.blit(WHITE_PIECE, (x - PIECE / 2, y - PIECE / 2))
    
def draw_result():
    pass

def main():
    pygame.init()
    # clock = pygame.time.Clock()
    run = True
    SCREEN.blit(BG, (0,0))
    pygame.display.update()
    state = 1
    while run:
        # clock.tick(FPS) #to control the speed of while loop, never go over that speed
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    (i, j) = pos_pixel2map(pos[0], pos[1])
                    print((i,j))
                    
                    # column = pos[0] // (SIZE + MARGIN)
                    # row = pos[1] // (SIZE + MARGIN)
                    # grid[row][column] = 1
                    # print("Click ", pos, "Grid coordinates: ", row, column)
        
                    draw_piece(state, i, j)
                    pygame.display.update()
                    state *= -1
        # draw_window()
        

    pygame.quit()


if __name__ == '__main__':
    main()